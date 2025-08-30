from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os

# Ensure .env files are loaded before instantiating Settings
try:
    from dotenv import load_dotenv
    for f in (".env", ".env.local"):
        p = Path(f)
        if p.exists():
            load_dotenv(p)
except Exception:
    pass

class Settings(BaseSettings):
    # Only read from environment; external .env files should be loaded by entrypoints
    model_config = {"extra": "ignore"}

    temporal_target: str = "localhost:7233"
    temporal_namespace: str = "default"
    task_queue: str = "agent-queue"

    # LLM provider: OpenAI Responses API
    llm_provider: str = "openai"
    llm_model_decision: str = "gpt-4.1"
    llm_model_plan: str = "gpt-4.1"

    # OpenAI-compatible config (works for Azure/custom via base_url)
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None

    # OTEL (OTLP HTTP endpoint, e.g., http://localhost:4318/v1/traces)
    otel_endpoint: Optional[str] = None
    otel_service_name_worker: str = "discovery-agent-worker"
    otel_service_name_api: str = "discovery-agent-api"

    # VFS (local claim-check root)
    vfs_root: str = "/tmp/agent_vfs"

settings = Settings()

def apply_openai_env_from_settings() -> None:
    """Project configured Azure/OpenAI settings into standard env vars.

    This ensures third-party libraries (e.g., Temporal OpenAI plugin) and any
    code path relying on OPENAI_* see the correct base_url/api_key, including
    Azure endpoints.
    """
    # Base URL resolution: prefer explicit OPENAI_BASE_URL; otherwise rely on env as-is
    if settings.openai_base_url:
        os.environ.setdefault("OPENAI_BASE_URL", settings.openai_base_url)
    else:
        # If only Azure endpoint is provided via env, derive OPENAI_BASE_URL
        az_ep = os.environ.get("AZURE_OPENAI_ENDPOINT")
        if az_ep and not os.environ.get("OPENAI_BASE_URL"):
            os.environ.setdefault("OPENAI_BASE_URL", az_ep.rstrip("/") + "/openai/v1/")

    # API key resolution: prefer explicit OPENAI_API_KEY, else adopt AZURE_OPENAI_API_KEY if present
    if settings.openai_api_key:
        os.environ.setdefault("OPENAI_API_KEY", settings.openai_api_key)
    else:
        # If only AZURE_OPENAI_API_KEY is set in env, use it implicitly
        az_key = os.environ.get("AZURE_OPENAI_API_KEY")
        if az_key:
            os.environ.setdefault("OPENAI_API_KEY", az_key)
