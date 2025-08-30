from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Only read from environment; external .env files should be loaded by entrypoints
    model_config = {"extra": "ignore"}

    temporal_target: str = "localhost:7233"
    temporal_namespace: str = "default"
    task_queue: str = "agent-queue"

    # LLM provider: "openai" | "anthropic" (still used by plan activity)
    llm_provider: str = "openai"
    llm_model_decision: str = "gpt-4o-mini"
    llm_model_plan: str = "gpt-4o-mini"
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # OTEL (OTLP HTTP endpoint, e.g., http://localhost:4318/v1/traces)
    otel_endpoint: Optional[str] = None
    otel_service_name_worker: str = "discovery-agent-worker"
    otel_service_name_api: str = "discovery-agent-api"

    # VFS (local claim-check root)
    vfs_root: str = "/tmp/agent_vfs"

settings = Settings()
