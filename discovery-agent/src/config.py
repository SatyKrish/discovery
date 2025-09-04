"""Runtime configuration for the Discovery agent."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List


def _json_env(name: str, default):
    raw = os.getenv(name)
    if not raw:
        return default
    try:
        return json.loads(raw)
    except Exception:
        return default


@dataclass
class Settings:
    # OpenAI / Azure OpenAI (Responses API)
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    default_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

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

    # MCP provider configuration (stdio + http)
    mcp_stdio: List[Dict[str, Any]] = field(default_factory=lambda: _json_env("MCP_STDIO", []))
    mcp_http: List[Dict[str, Any]] = field(default_factory=lambda: _json_env("MCP_HTTP", []))


settings = Settings()


def apply_openai_env_from_settings():
    """Project configured OpenAI settings into environment variables."""
    if settings.openai_base_url:
        os.environ["OPENAI_BASE_URL"] = settings.openai_base_url
    if settings.openai_api_key:
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
