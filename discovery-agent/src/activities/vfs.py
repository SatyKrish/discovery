from __future__ import annotations
import hashlib
from pathlib import Path
from temporalio import activity
from discovery_agent.config import settings
from discovery_agent.models import FileRef

@activity.defn
async def vfs_put(bytes_data: bytes, filename: str, mime: str) -> FileRef:
    Path(settings.vfs_root).mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(bytes_data).hexdigest()
    path = Path(settings.vfs_root) / f"{sha}_{filename}"
    with open(path, "wb") as f:
        f.write(bytes_data)
    return FileRef(uri=str(path), sha256=sha, size=len(bytes_data), mime=mime)
