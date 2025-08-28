"""MCP server exposing the Temporal DeepAgent over Streamable HTTP."""

from __future__ import annotations

import uuid

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools import Tool
from temporalio.client import Client

from temporal_workflow import DeepAgentWorkflow


async def ask_deep_agent(question: str) -> str:
    """Run the DeepAgent workflow for the supplied question."""
    client = await Client.connect("localhost:7233")
    return await client.execute_workflow(
        DeepAgentWorkflow.run,
        question,
        id=f"deep-agent-{uuid.uuid4()}",
        task_queue="deep-agent-task-queue",
    )


mcp = FastMCP(
    name="deep-agent-temporal",
    tools=[Tool.from_function(ask_deep_agent, name="ask", description="Query the DeepAgent workflow")],
)


if __name__ == "__main__":
    # Run the MCP server using the Streamable HTTP transport so clients can
    # connect over HTTP and receive streaming responses.
    mcp.run(transport="streamable-http")
