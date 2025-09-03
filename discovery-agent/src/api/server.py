from __future__ import annotations

import time
from datetime import timedelta
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from temporalio.client import Client, WithStartWorkflowOperation
from temporalio.common import WorkflowIDConflictPolicy
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin
from temporalio.contrib.pydantic import pydantic_data_converter
import asyncio
import json

from src.config import settings, apply_openai_env_from_settings
from src.otel import setup_tracing
from src.workflows.agent_orchestrator import AgentOrchestratorWorkflow, TurnResult
from src.models import Message  # your existing pydantic model


# Helper function to extract text from both content and parts formats
def _extract_text(msg: dict) -> str:
    """
    Extract text from message that may be in different formats:
    - Legacy format: { content: "text" }
    - Vercel AI format: { parts: [{ type: "text", text: "text" }] }
    """
    # Prefer 'content' if present (legacy format)
    content = msg.get("content")
    if isinstance(content, str) and content.strip():
        return content

    # Support Vercel AI 'parts' for multimodal messages
    parts = msg.get("parts")
    if isinstance(parts, list):
        chunks = []
        for p in parts:
            # text parts: { type: 'text', text: '...' }
            if isinstance(p, dict) and p.get("type") == "text":
                t = p.get("text")
                if isinstance(t, str):
                    chunks.append(t)
        if chunks:
            return " ".join(chunks)

    return ""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    print("🚀 Starting Discovery Agent API...")

    # Apply OpenAI environment settings
    apply_openai_env_from_settings()

    # Setup tracing
    setup_tracing(settings.otel_service_name_api, settings.otel_endpoint)

    # Connect to Temporal
    temporal_client = None
    try:
        print(f"🔗 Connecting to Temporal at {settings.temporal_target}...")
        temporal_client = await Client.connect(
            settings.temporal_target,
            namespace=settings.temporal_namespace,
            plugins=[OpenAIAgentsPlugin()],
            data_converter=pydantic_data_converter,
        )
        print("✅ Connected to Temporal successfully")
        app.state.temporal_client = temporal_client
    except Exception as e:
        print(f"❌ Failed to connect to Temporal: {e}")
        print("⚠️  API will start but Temporal features will be unavailable")
        app.state.temporal_client = None

    print("🎉 Discovery Agent API started successfully")
    yield

    # Cleanup
    if temporal_client:
        await temporal_client.close()
    print("👋 Discovery Agent API shut down")


app = FastAPI(
    title="Discovery Agent API",
    description="Synchronous Updates API for Discovery Agent",
    version="1.0.0",
    lifespan=lifespan
)


async def _client() -> Client:
    """Get Temporal client with error handling."""
    client = getattr(app.state, 'temporal_client', None)
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Temporal client not available. Please check Temporal server connection."
        )
    return client


# ---------- Schemas ----------

class ChatRequest(BaseModel):
    text: str
    workflow_id: Optional[str] = None
    goal: Optional[str] = "Have a helpful conversation"

class ConfirmRequest(BaseModel):
    workflow_id: str
    tool_call_id: str
    approved: bool = True
    args: Optional[dict] = None

class EndRequest(BaseModel):
    workflow_id: str

class ChatStreamRequest(BaseModel):
    id: Optional[str] = None
    messages: List[Dict[str, Any]] = []


# ---------- Endpoints ----------

@app.post("/chat/send-sync")
async def send_sync(req: ChatRequest):
    client = await _client()
    wid = req.workflow_id or f"session-{int(time.time() * 1000)}"

    from temporalio.common import WorkflowIDConflictPolicy

    start_op = WithStartWorkflowOperation(
        AgentOrchestratorWorkflow.run,
        req.goal or "Have a helpful conversation",
        id=wid,
        id_conflict_policy=WorkflowIDConflictPolicy.USE_EXISTING,
        task_queue=settings.task_queue,
        memo={"started_at": int(time.time()), "Goal": req.goal or ""},
    )

    try:
        # Execute @update user_turn with Update-with-Start semantics
        result: TurnResult = await client.execute_update_with_start_workflow(
            AgentOrchestratorWorkflow.user_turn,
            Message(role="user", content=req.text, ts=time.time()),
            start_workflow_operation=start_op,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"user_turn failed: {e}")

    # Return either assistant or pending_tool for the client to act upon
    out: Dict[str, Any] = {"workflow_id": wid}
    out["assistant"] = result.assistant.model_dump() if result.assistant else None
    out["pending_tool"] = result.pending_tool.model_dump() if result.pending_tool else None
    return out


@app.post("/chat/confirm")
async def confirm(req: ConfirmRequest):
    client = await _client()
    handle = client.get_workflow_handle(req.workflow_id)
    try:
        await handle.signal(
            AgentOrchestratorWorkflow.approve_tool,
            req.tool_call_id,
            req.approved,
            req.args,
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"confirm failed: {e}")
    return {"ok": True}


@app.post("/chat/wait-sync")
async def wait_sync(workflow_id: str):
    """
    Blocks until the next assistant message is produced after this call is received.
    Intended for use immediately after /chat/confirm when approval was required.
    """
    client = await _client()
    handle = client.get_workflow_handle(workflow_id)
    try:
        msg: Message = await handle.execute_update(AgentOrchestratorWorkflow.wait_for_assistant)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"wait_sync failed: {e}")
    return {"workflow_id": workflow_id, "assistant": msg.model_dump()}


@app.post("/chat/end")
async def end_chat(req: EndRequest):
    client = await _client()
    handle = client.get_workflow_handle(req.workflow_id)
    try:
        await handle.signal(AgentOrchestratorWorkflow.end_conversation)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"end failed: {e}")
    return {"ok": True}


@app.get("/sessions/{workflow_id}/history")
async def history(workflow_id: str) -> List[Dict[str, Any]]:
    client = await _client()
    handle = client.get_workflow_handle(workflow_id)
    try:
        msgs = await handle.query(AgentOrchestratorWorkflow.get_conversation_history)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"history failed: {e}")
    out: List[Dict[str, Any]] = []
    for m in msgs:
        out.append(m.model_dump() if hasattr(m, "model_dump") else dict(m))
    return out


@app.post("/chat/stream")
async def chat_stream(req: Request):
    """
    Accepts AI SDK payload: { id?: string, messages: [...] }
    - Uses Update-with-Start to run user_turn
    - If tool approval needed, streams a notice
    - Otherwise streams assistant content in chunks
    """
    body = await req.json()
    req_obj = ChatStreamRequest.model_validate(body)
    client = await _client()

    # Stable session/workflow id
    wid = req_obj.id or f"session-{int(time.time() * 1000)}"

    # Extract the last user message for this turn
    last_user = None
    for m in reversed(req_obj.messages):
        if m.get("role") == "user":
            last_user = m
            break
    if not last_user:
        raise HTTPException(status_code=400, detail="No user message found in 'messages'.")

    # Extract text from the user message (supports both content and parts formats)
    user_text = _extract_text(last_user)
    if not user_text:
        raise HTTPException(status_code=400, detail="Empty user message")

    # Goal = first message content when present (or default)
    goal = (_extract_text(req_obj.messages[0]) if req_obj.messages else None) or "Have a helpful conversation"

    # Prepare signal-with-start semantics
    start_op = WithStartWorkflowOperation(
        AgentOrchestratorWorkflow.run,
        goal,
        id=wid,
        id_conflict_policy=WorkflowIDConflictPolicy.USE_EXISTING,
        task_queue=settings.task_queue,
        memo={"started_at": int(time.time()), "Goal": goal},
        execution_timeout=timedelta(days=7),
    )

    # Drive the turn
    try:
        result: TurnResult = await client.execute_update_with_start_workflow(
            AgentOrchestratorWorkflow.user_turn,
            Message(role="user", content=user_text, ts=time.time()),
            start_workflow_operation=start_op,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"user_turn failed: {e}")

    async def ds():
        # Optional: signal step start
        yield 'data: {"type":"start-step"}\n\n'

        if result.pending_tool is not None:
            evt = {
                "type": "tool",
                "status": "pending",
                "tool_call_id": result.pending_tool.id,
                "name": result.pending_tool.name,
                "args": result.pending_tool.args,
                "requires_approval": result.pending_tool.requires_approval,
                "workflow_id": wid,
            }
            yield f"data: {json.dumps(evt, ensure_ascii=False)}\n\n"
            yield 'data: {"type":"finish"}\n\n'
            yield 'data: [DONE]\n\n'
            return

        # Get assistant text now or wait for it
        if result.assistant and result.assistant.content:
            text = result.assistant.content
        else:
            try:
                handle = client.get_workflow_handle(wid)
                waited = await handle.execute_update(AgentOrchestratorWorkflow.wait_for_assistant)
                text = waited.content or ""
            except Exception as e:
                text = f"[error waiting for assistant] {e}"

        # Stream as text events (following AI SDK format)
        if text:
            # Send text-start event
            yield f'data: {json.dumps({"type":"text-start","id":wid}, ensure_ascii=False)}\n\n'

            # Stream text-delta events
            for token in text.split(" "):
                delta = token + " "
                yield f'data: {json.dumps({"type":"text-delta","id":wid,"delta": delta}, ensure_ascii=False)}\n\n'
                await asyncio.sleep(0.02)

            # Send text-end event
            yield f'data: {json.dumps({"type":"text-end","id":wid}, ensure_ascii=False)}\n\n'

        # Always send finish and [DONE] to properly terminate the stream
        yield 'data: {"type":"finish"}\n\n'
        yield 'data: [DONE]\n\n'

    return StreamingResponse(
        ds(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
