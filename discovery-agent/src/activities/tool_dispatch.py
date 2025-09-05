from __future__ import annotations
from temporalio import activity
from src.models import ToolCall

@activity.defn
async def tool_dispatch(call: ToolCall) -> dict:
    from src.tools.registry import mcp_invoke_tool
    return mcp_invoke_tool(call.name, call.args)
