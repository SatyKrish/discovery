from __future__ import annotations
from temporalio import activity

@activity.defn
async def mcp_invoke(tool_name: str, args: dict) -> dict:
    from src.tools.registry import mcp_invoke_tool
    return mcp_invoke_tool(tool_name, args)
