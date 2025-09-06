from __future__ import annotations
from temporalio import activity

@activity.defn
async def get_prompt(prompt_id: str) -> dict:
    from src.tools.registry import mcp_get_prompt
    return mcp_get_prompt(prompt_id)
