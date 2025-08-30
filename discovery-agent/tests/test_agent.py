import pytest
from temporalio.testing import WorkflowEnvironment
from src.workflows.agent_orchestrator import AgentOrchestratorWorkflow

@pytest.mark.asyncio
async def test_plan_initializes():
	async with await WorkflowEnvironment.start_time_skipping() as env:
		client = env.client
		handle = await client.start_workflow(
			AgentOrchestratorWorkflow.run,
			"Test goal",
			id="wf-test-1",
			task_queue="agent-queue",
		)
		status = await handle.query(AgentOrchestratorWorkflow.get_status)
		assert status.plan and len(status.plan) > 0
