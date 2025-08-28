from __future__ import annotations

import asyncio
import os
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from temporalio.client import Client
from dotenv import load_dotenv

from temporal.temporal_workflow import DeepAgentWorkflow

# Load environment variables from .env if present
load_dotenv()

# ---------------------------------------------------------------------------
# Temporal client management
# ---------------------------------------------------------------------------
_client_lock = asyncio.Lock()
_temporal_client: Client | None = None


async def get_temporal_client() -> Client:
    """Return a cached Temporal client, connecting if necessary."""

    global _temporal_client
    if _temporal_client is None:
        async with _client_lock:
            if _temporal_client is None:
                address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
                try:
                    _temporal_client = await Client.connect(address)
                except Exception as exc:  # pragma: no cover - network errors
                    raise RuntimeError(f"Failed to connect to Temporal: {exc}")
    return _temporal_client


# ---------------------------------------------------------------------------
# Request and response models
# ---------------------------------------------------------------------------
class StartWorkflowRequest(BaseModel):
    question: Optional[str] = None
    instructions: str = ""
    tools: Optional[List[str]] = None
    mcp_endpoints: Optional[List[str]] = None
    workflow_id: Optional[str] = Field(default=None, description="Optional explicit workflow ID")


class WorkflowIdResponse(BaseModel):
    workflow_id: str


class PromptRequest(BaseModel):
    prompt: str


class ConfirmRequest(BaseModel):
    data: Optional[Dict[str, Any]] = None


class StatusResponse(BaseModel):
    status: str = "ok"


class HistoryResponse(BaseModel):
    history: List[Dict[str, str]]


# ---------------------------------------------------------------------------
# FastAPI application setup
# ---------------------------------------------------------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------
@app.post("/workflow/start", response_model=WorkflowIdResponse)
async def start_workflow(req: StartWorkflowRequest) -> WorkflowIdResponse:
    client = await get_temporal_client()
    wf_id = req.workflow_id or str(uuid.uuid4())
    try:
        # start_workflow takes (workflow|name, first_arg?, *, args=[...], id=..., task_queue=...)
        handle = await client.start_workflow(
            DeepAgentWorkflow.run,
            args=[
                req.question,
                req.instructions,
                req.tools,
                req.mcp_endpoints,
            ],
            id=wf_id,
            task_queue=os.getenv("TEMPORAL_TASK_QUEUE", "deep-agent-task-queue"),
        )
    except Exception as exc:  # pragma: no cover - network or workflow errors
        raise HTTPException(status_code=500, detail=str(exc))
    return WorkflowIdResponse(workflow_id=handle.id)


@app.post("/workflow/{workflow_id}/prompt", response_model=StatusResponse)
async def send_prompt(workflow_id: str, req: PromptRequest) -> StatusResponse:
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id)
    try:
        await handle.signal(DeepAgentWorkflow.user_prompt, req.prompt)
    except Exception as exc:  # pragma: no cover - signal errors
        raise HTTPException(status_code=500, detail=str(exc))
    return StatusResponse()


@app.post("/workflow/{workflow_id}/confirm", response_model=StatusResponse)
async def send_confirmation(workflow_id: str, req: ConfirmRequest) -> StatusResponse:
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id)
    try:
        await handle.signal(DeepAgentWorkflow.confirm, req.data)
    except Exception as exc:  # pragma: no cover - signal errors
        raise HTTPException(status_code=500, detail=str(exc))
    return StatusResponse()


@app.post("/workflow/{workflow_id}/end", response_model=StatusResponse)
async def end_chat(workflow_id: str) -> StatusResponse:
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id)
    try:
        await handle.signal(DeepAgentWorkflow.end_chat)
    except Exception as exc:  # pragma: no cover - signal errors
        raise HTTPException(status_code=500, detail=str(exc))
    return StatusResponse()


@app.get("/workflow/{workflow_id}/history", response_model=HistoryResponse)
async def get_history(workflow_id: str) -> HistoryResponse:
    client = await get_temporal_client()
    handle = client.get_workflow_handle(workflow_id)
    try:
        history = await handle.query(DeepAgentWorkflow.get_conversation_history)
    except Exception as exc:  # pragma: no cover - query errors
        raise HTTPException(status_code=500, detail=str(exc))
    return HistoryResponse(history=history)
