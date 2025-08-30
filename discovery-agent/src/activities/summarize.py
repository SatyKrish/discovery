from __future__ import annotations
from temporalio import activity

@activity.defn
async def summarize_activity(state_view: dict) -> str:
    plan_titles = ", ".join([p.get("title","?") for p in state_view.get("plan", [])])
    return f"turns={state_view.get('turns')}; plan=[{plan_titles}]"
