import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import types

import pytest

# Ensure repository root and temporal modules are importable
root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "temporal"))

# Remove any previously injected temporalio stub from other tests
sys.modules.pop("temporalio", None)
# Ensure any previous import of the workflow module using stubbed Temporal
# definitions is cleared so we can import the real implementation.
sys.modules.pop("temporal_workflow", None)
# Provide a lightweight stub for openai_model to avoid heavy dependency in tests
sys.modules.setdefault("openai_model", types.SimpleNamespace(get_default_model=lambda: None))

temporalio = pytest.importorskip("temporalio")
from temporalio.worker import Worker
from temporalio.testing import WorkflowEnvironment
from temporalio import workflow

from agent_activities import AgentActivities
from temporal_worker import dynamic_tool_dispatcher
from temporal_workflow import DeepAgentWorkflow, run_query


@workflow.defn
class DummyWorkflow:
    """Workflow used to verify activity registration."""

    @workflow.run
    async def run(self) -> int:  # pragma: no cover - exercised via Temporal
        await workflow.execute_activity(
            "agent_validatePrompt",
            '{"tool": "add", "args": {"a": 1, "b": 1}}',
            schedule_to_close_timeout=timedelta(seconds=5),
        )
        result = await workflow.execute_activity(
            "add",
            {"a": 1, "b": 1},
            schedule_to_close_timeout=timedelta(seconds=5),
        )
        return result


@pytest.mark.asyncio
async def test_worker_runs_and_dispatches_tools():
    """Smoke test ensuring worker starts and activities are callable."""

    try:
        env = await WorkflowEnvironment.start_time_skipping()
    except Exception as exc:  # pragma: no cover - environment failure
        pytest.skip(f"Temporal test server unavailable: {exc}")

    async with env:
        activities = AgentActivities()
        worker = Worker(
            env.client,
            task_queue="test-queue",
            workflows=[DeepAgentWorkflow, DummyWorkflow],
            activities=[
                run_query,
                dynamic_tool_dispatcher,
                activities.agent_toolPlanner,
                activities.agent_validatePrompt,
                activities.get_wf_env_vars,
            ],
            activity_executor=ThreadPoolExecutor(),
        )
        async with worker:
            result = await env.client.execute_workflow(
                DummyWorkflow.run,
                id="wf-id",
                task_queue="test-queue",
            )
            assert result == 2
