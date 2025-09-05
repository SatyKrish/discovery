from __future__ import annotations
from temporalio import activity

@activity.defn
async def summarize_activity(view: dict) -> str:
    # In prod, call model with strict schema for summary
    msgs = view.get("messages", [])
    last_user = next((m for m in reversed(msgs) if m.get("role") == "user"), None)
    return f"Summary up to {len(msgs)} msgs. Last user msg: {(last_user or {}).get('content','')}"
