"""Temporal workflow that runs the custom DeepAgent implementation.

The workflow delegates execution to an activity that instantiates and runs
our minimal DeepAgent powered by OpenAI's tool calling.  This provides the
same capabilities as the original LangGraph version while leveraging
Temporal's reliability semantics.
"""

from __future__ import annotations

from datetime import timedelta
from temporalio import activity, workflow

from deep_agent import run_agent


@activity.defn
async def run_query(question: str, instructions: str = "") -> str:
    """Execute the DeepAgent for the supplied question."""

    return await run_agent(question, instructions)


@workflow.defn
class DeepAgentWorkflow:
    """Workflow that runs the DeepAgent loop as an activity."""

    @workflow.run
    async def run(self, question: str, instructions: str = "") -> str:  # pragma: no cover - workflow entrypoint
        return await workflow.execute_activity(
            run_query,
            question,
            instructions,
            schedule_to_close_timeout=timedelta(minutes=1),
        )
