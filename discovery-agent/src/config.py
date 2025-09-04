# ──────────────────────────────────────────────────────────────────────────────
# File: src/config.py (minimal settings used by LLM helper)
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os, json
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
    # OpenAI / Azure OpenAI (Responses API). For Azure, set base_url to your deployment endpoint
    # and OPENAI_MODEL to your *deployment name*.
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    default_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # MCP providers (stdio & http). Configure via env:
    # MCP_STDIO='[{"name":"local","cmd":["node","./mcp.js"],"cwd":"/srv","env":{"FOO":"1"}}]'
    # MCP_HTTP='[{"name":"meta","base_url":"https://mcp.example.com","headers":{"Authorization":"Bearer X"}}]'
    mcp_stdio: List[Dict[str, Any]] = field(default_factory=lambda: _json_env("MCP_STDIO", []))
    mcp_http: List[Dict[str, Any]] = field(default_factory=lambda: _json_env("MCP_HTTP", []))

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

# Helpers for activity processes that may run outside the workflow sandbox

def apply_openai_env_from_settings():
    """Apply OpenAI settings to environment variables, handling both standard and Azure configurations"""

    # Handle Azure OpenAI configuration
    az_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    az_key = os.environ.get("AZURE_OPENAI_API_KEY")

    if az_endpoint and not os.environ.get("OPENAI_BASE_URL"):
        # Convert Azure endpoint to OpenAI-compatible base URL
        os.environ["OPENAI_BASE_URL"] = az_endpoint.rstrip("/") + "/openai/v1/"

    if az_key and not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = az_key

    # Handle standard OpenAI configuration (fallback)
    if settings.openai_base_url:
        os.environ.setdefault("OPENAI_BASE_URL", settings.openai_base_url)
    if settings.openai_api_key:
        os.environ.setdefault("OPENAI_API_KEY", settings.openai_api_key)
