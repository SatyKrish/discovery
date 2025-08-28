"""Temporal workflow that runs the custom DeepAgent implementation.

The workflow delegates execution to an activity that instantiates and runs
our minimal DeepAgent powered by OpenAI's tool calling.  This provides the
same capabilities as the original LangGraph version while leveraging
Temporal's reliability semantics.

Connections to external [MCP](https://github.com/modelcontextprotocol)
servers can be supplied when starting the workflow.  Any tools returned from
the endpoints are merged with the agent's built-ins::

    await client.execute_workflow(
        DeepAgentWorkflow.run,
        "Say hello",
        mcp_endpoints=["http://localhost:8000/mcp"],
        id="demo-run",
        task_queue="deep-agent-task-queue",
    )
"""

from __future__ import annotations

from datetime import timedelta
from typing import Sequence

from temporalio import activity, workflow

from deep_agent import run_agent


@activity.defn
async def run_query(
    question: str,
    instructions: str = "",
    mcp_endpoints: Sequence[str] | None = None,
) -> str:
    """Execute the DeepAgent for the supplied question."""

    return await run_agent(
        question,
        instructions,
        mcp_endpoints=mcp_endpoints,
    )


@workflow.defn
class DeepAgentWorkflow:
    """Workflow that runs the DeepAgent loop as an activity."""

    @workflow.run
    async def run(
        self,
        question: str,
        instructions: str = "",
        mcp_endpoints: Sequence[str] | None = None,
    ) -> str:  # pragma: no cover - workflow entrypoint
        return await workflow.execute_activity(
            run_query,
            question,
            instructions,
            mcp_endpoints,
            schedule_to_close_timeout=timedelta(minutes=1),
        )
