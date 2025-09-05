from __future__ import annotations
from temporalio import activity

@activity.defn
async def discover_mcp_tools() -> dict:
    from src.tools.registry import mcp_discover_tools, mcp_list_prompts
    return {"success": True, "tools": mcp_discover_tools(), "prompts": mcp_list_prompts()}
