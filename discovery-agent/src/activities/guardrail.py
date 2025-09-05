from __future__ import annotations
from temporalio import activity

@activity.defn
async def guardrail_check(payload: dict) -> bool:
    # Replace with real policy checks (PII, budget, allowed domains, etc.)
    goal = payload.get("goal", "")
    msg = payload.get("message", "")
    banned = ["delete all", "format drive", "wire money to"]
    return not any(b in msg.lower() for b in banned)
