# Simplified Azure OpenAI configuration
from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class Settings:
    # OpenAI configuration
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")  # Azure deployment name

    # MCP providers
    mcp_stdio: List[Dict[str, Any]] = field(default_factory=list)
    mcp_http: List[Dict[str, Any]] = field(default_factory=list)

    # Temporal configuration
    temporal_target: str = os.getenv("TEMPORAL_TARGET", "localhost:7233")
    temporal_namespace: str = os.getenv("TEMPORAL_NAMESPACE", "default")
    task_queue: str = os.getenv("TEMPORAL_TASK_QUEUE", "agent-queue")

    # OTEL configuration
    otel_endpoint: str | None = os.getenv("OTEL_ENDPOINT")
    otel_service_name_worker: str = os.getenv("OTEL_SERVICE_NAME_WORKER", "discovery-agent-worker")
    otel_service_name_api: str = os.getenv("OTEL_SERVICE_NAME_API", "discovery-agent-api")

    # VFS configuration
    vfs_root: str = os.getenv("VFS_ROOT", "/tmp/agent_vfs")

settings = Settings()
