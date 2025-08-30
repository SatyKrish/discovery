from __future__ import annotations
from temporalio import activity

@activity.defn
async def guardrail_check(payload: dict) -> bool:
    goal = (payload or {}).get("goal", "").lower()
    msg = (payload or {}).get("message", "").lower()
    return True if goal and msg else False
