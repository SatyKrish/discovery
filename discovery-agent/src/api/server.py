from __future__ import annotations
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel
from temporalio.client import Client
from pathlib import Path
from src.config import settings, apply_openai_env_from_settings
from src.otel import setup_tracing
from src.workflows.agent_orchestrator import AgentOrchestratorWorkflow
from src.models import Message
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin
from temporalio.contrib.pydantic import pydantic_data_converter

# Load .env files at process start (outside workflow sandbox)
try:
    from dotenv import load_dotenv
    for f in (".env", ".env.local"):
        p = Path(f)
        if p.exists():
            load_dotenv(p)
except Exception:
    pass

app = FastAPI(title="Discovery Agent API")
setup_tracing(settings.otel_service_name_api, settings.otel_endpoint)

async def get_client() -> Client:
    # Ensure Azure/OpenAI env for data converter consistency
    apply_openai_env_from_settings()

    return await Client.connect(
        settings.temporal_target,
        namespace=settings.temporal_namespace,
        plugins=[OpenAIAgentsPlugin()],
        data_converter=pydantic_data_converter,
    )

class StartRequest(BaseModel):
    goal: str
    tenant: str | None = None
    user_id: str | None = None

@app.post("/sessions")
async def start_session(req: StartRequest):
    client = await get_client()
    workflow_id = f"session-{int(time.time()*1000)}"
    handle = await client.start_workflow(
        AgentOrchestratorWorkflow.run,
        req.goal,
        id=workflow_id,
        task_queue=settings.task_queue,
        # Use memo only; search attributes require pre-registration
        memo={
            "started_at": int(time.time()),
            "Goal": req.goal,
            **({"Tenant": req.tenant} if req.tenant else {}),
            **({"UserId": req.user_id} if req.user_id else {}),
        },
    )
    return {"workflow_id": handle.id}

class MessageRequest(BaseModel):
    text: str

@app.post("/sessions/{workflow_id}/messages")
async def send_user_message(workflow_id: str, req: MessageRequest):
    client = await get_client()
    handle = client.get_workflow_handle(workflow_id)
    await handle.signal(AgentOrchestratorWorkflow.user_message, Message(role="user", content=req.text, ts=time.time()))
    return {"ok": True}

class ApprovalRequest(BaseModel):
    tool_call_id: str
    approved: bool
    args: dict | None = None

@app.post("/sessions/{workflow_id}/approve")
async def approve_tool(workflow_id: str, req: ApprovalRequest):
    client = await get_client()
    handle = client.get_workflow_handle(workflow_id)
    await handle.signal(AgentOrchestratorWorkflow.approve_tool, req.tool_call_id, req.approved, req.args)
    return {"ok": True}

@app.get("/sessions/{workflow_id}/status")
async def get_status(workflow_id: str):
    client = await get_client()
    handle = client.get_workflow_handle(workflow_id)
    status = await handle.query(AgentOrchestratorWorkflow.get_status)
    try:
        return status.model_dump()
    except Exception:
        return status


class ChatRequest(BaseModel):
    session_id: str | None = None
    input: str
    goal: str | None = None


@app.post("/chat")
async def chat(req: ChatRequest, request: Request):
    client = await get_client()
    session_id = req.session_id
    goal = req.goal or "chat"
    if not session_id:
        session_id = f"session-{int(time.time()*1000)}"
        await client.start_workflow(
            AgentOrchestratorWorkflow.run,
            goal,
            id=session_id,
            task_queue=settings.task_queue,
            memo={"started_at": int(time.time()), "Goal": goal},
        )

    handle = client.get_workflow_handle(session_id)
    await handle.signal(
        AgentOrchestratorWorkflow.user_message,
        Message(role="user", content=req.input, ts=time.time()),
    )
    base = str(request.base_url).rstrip("/")
    status_url = f"{base}/sessions/{session_id}/status"
    return {"session_id": session_id, "status_url": status_url}
