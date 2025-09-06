from __future__ import annotations
import hashlib
from temporalio import activity

@activity.defn
async def append_transcript(conversation_id: str, role: str, content: str) -> None:
    # Idempotency: derive stable key from input (example; replace with DB upsert)
    key = hashlib.sha256(f"{conversation_id}:{role}:{content}".encode()).hexdigest()
    activity.logger.debug("append_transcript key=%s", key)
    return None
