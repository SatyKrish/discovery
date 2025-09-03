# ──────────────────────────────────────────────────────────────────────────────
# File: src/config.py (minimal settings used by LLM helper)
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass
class Settings:
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    default_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

settings = Settings()

# Helpers for activity processes that may run outside the workflow sandbox

def apply_openai_env_from_settings():
    if settings.openai_base_url:
        os.environ["OPENAI_BASE_URL"] = settings.openai_base_url
    if settings.openai_api_key:
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
