"""Temporal workflow that runs the custom DeepAgent implementation.

The workflow delegates execution to an activity that instantiates and runs
our minimal DeepAgent powered by OpenAI's tool calling.  This provides the
same capabilities as the original LangGraph version while leveraging
Temporal's reliability semantics.

Connections to external [MCP](https://github.com/modelcontextprotocol)
servers or additional LangChain tools can be supplied when starting the
workflow.  ``tools`` should be import strings of callables that return
``BaseTool`` instances.  The activity loads these tools and merges them with
the agent's built-ins::

    await client.execute_workflow(
        DeepAgentWorkflow.run,
        "Say hello",
        tools=["my_tools.greetings:hello_tool"],
        mcp_endpoints=["http://localhost:8000/mcp"],
        id="demo-run",
        task_queue="deep-agent-task-queue",
    )
"""

from __future__ import annotations

from datetime import timedelta
from importlib import import_module
from typing import Sequence

from langchain_core.tools import BaseTool
from temporalio import activity, workflow

from deep_agent import create_deep_agent


def _load_tool(spec: str) -> BaseTool:
    module_name, attr_name = spec.split(":", 1)
    module = import_module(module_name)
    obj = getattr(module, attr_name)
    if isinstance(obj, BaseTool):
        return obj
    if callable(obj):
        tool_obj = obj()
        if isinstance(tool_obj, BaseTool):
            return tool_obj
    raise TypeError(f"{spec} did not resolve to a BaseTool")


@activity.defn
async def run_query(
    question: str,
    instructions: str = "",
    tools: Sequence[str] | None = None,
    mcp_endpoints: Sequence[str] | None = None,
) -> str:
    """Execute the DeepAgent for the supplied question."""
    tool_objs = [_load_tool(t) for t in tools] if tools else None
    agent = create_deep_agent(tools=tool_objs, mcp_endpoints=mcp_endpoints)
    return await agent(question, instructions)


@workflow.defn
class DeepAgentWorkflow:
    """Workflow that runs the DeepAgent loop as an activity."""

    @workflow.run
    async def run(
        self,
        question: str,
        instructions: str = "",
        tools: Sequence[str] | None = None,
        mcp_endpoints: Sequence[str] | None = None,
    ) -> str:  # pragma: no cover - workflow entrypoint
        return await workflow.execute_activity(
            run_query,
            question,
            instructions,
            tools,
            mcp_endpoints,
            schedule_to_close_timeout=timedelta(minutes=1),
        )
