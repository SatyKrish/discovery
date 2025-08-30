import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio import activity
from temporalio.worker import Worker
from src.workflows.agent_orchestrator import AgentOrchestratorWorkflow
from temporalio.contrib.pydantic import pydantic_data_converter


# Stub out plan_activity to avoid external LLM calls in tests
@activity.defn(name="plan_activity")
async def plan_activity_stub(context: dict):
	return [
		{"id": 1, "title": "Step A", "status": "todo", "tool_hints": []},
		{"id": 2, "title": "Step B", "status": "todo", "tool_hints": []},
	]

# Stub decision_agents_activity to a harmless no-op that just increments turns
@activity.defn(name="decision_agents_activity")
async def decision_agents_activity_stub(state_view: dict) -> dict:
	return {"type": "assistant_message", "message": {"role": "assistant", "content": "ok", "ts": 0}}

@pytest.mark.asyncio
async def test_plan_initializes():
	async with await WorkflowEnvironment.start_time_skipping(data_converter=pydantic_data_converter) as env:
		# Start a worker on the same task queue with our workflow and stub activity
		async with Worker(
			env.client,
			task_queue="agent-queue",
			workflows=[AgentOrchestratorWorkflow],
			activities=[plan_activity_stub, decision_agents_activity_stub],
		):
			client = env.client
			handle = await client.start_workflow(
				AgentOrchestratorWorkflow.run,
				"Test goal",
				id="wf-test-1",
				task_queue="agent-queue",
			)
			# Advance time until the first activity has completed and plan is set
			status = await handle.query(AgentOrchestratorWorkflow.get_status)
			attempts = 0
			while (not status.plan) and attempts < 10:
				await env.sleep(1)
				status = await handle.query(AgentOrchestratorWorkflow.get_status)
				attempts += 1
			assert status.plan and len(status.plan) > 0
