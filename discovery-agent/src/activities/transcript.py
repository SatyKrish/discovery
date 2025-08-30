from __future__ import annotations
from pathlib import Path
from temporalio import activity
from src.config import settings

@activity.defn
async def append_transcript(conversation_id: str, role: str, content: str) -> str:
    root = Path(settings.vfs_root) / "transcripts"
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{conversation_id}.log"
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{role}: {content}\n")
    return str(path)
