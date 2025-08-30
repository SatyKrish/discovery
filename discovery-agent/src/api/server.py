from __future__ import annotations
import time
from fastapi import FastAPI
from pydantic import BaseModel
from temporalio.client import Client
from discovery_agent.config import settings
from discovery_agent.otel import setup_tracing
from discovery_agent.workflows.agent_orchestrator import AgentOrchestratorWorkflow
from discovery_agent.models import Message

app = FastAPI(title="Discovery Agent API")
setup_tracing(settings.otel_service_name_api, settings.otel_endpoint)

async def get_client() -> Client:
    return await Client.connect(settings.temporal_target, namespace=settings.temporal_namespace)

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
        search_attributes={
            "Goal": [req.goal],
            **({"Tenant": [req.tenant]} if req.tenant else {}),
            **({"UserId": [req.user_id]} if req.user_id else {}),
        },
        memo={"started_at": int(time.time())},
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
