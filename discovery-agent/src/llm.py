# ──────────────────────────────────────────────────────────────
# File: src/llm.py
# Azure/OpenAI Responses API — JSON-only (structured output)
# ──────────────────────────────────────────────────────────────
from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, Optional

from src.config import settings

log = logging.getLogger(__name__)

__all__ = ["generate_json"]

class LLMError(Exception):
    """Single error type for the LLM client."""
    pass


# ---------- internals ----------

def _normalize_azure_base_url(url: str) -> str:
    """
    Ensures Azure-style base URL ends with /openai/v1/
    Accepts:
      https://<resource>.openai.azure.com/
      https://<resource>.openai.azure.com/openai/
      https://<resource>.openai.azure.com/openai/v1/
    """
    url = url.rstrip("/") + "/"
    if "azure.com" in url and not url.endswith("openai/v1/"):
        if url.endswith("openai/"):
            url += "v1/"
        else:
            url += "openai/v1/"
    return url


def _client():
    from openai import OpenAI

    if not settings.openai_api_key:
        raise LLMError("Missing OPENAI_API_KEY/AZURE_OPENAI_API_KEY in config.")
    kwargs: Dict[str, Any] = {"api_key": settings.openai_api_key}

    if settings.openai_base_url:
        kwargs["base_url"] = _normalize_azure_base_url(settings.openai_base_url)

    try:
        return OpenAI(**kwargs)
    except Exception as e:
        raise LLMError(f"Failed to create OpenAI client: {e}") from e


def _response_format(json_schema: Optional[Dict[str, Any]], strict: bool) -> Dict[str, Any]:
    # Prefer schema when provided; otherwise force JSON object
    if json_schema:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "structured_output",
                "schema": json_schema,
                "strict": strict,
            },
        }
    return {"type": "json_object"}


def _retry(call, *, attempts: int = 3, base_delay: float = 1.0, max_delay: float = 30.0, backoff: float = 2.0):
    last = None
    for i in range(attempts):
        try:
            return call()
        except Exception as e:
            last = e
            msg = str(e).lower()
            retryable = any(s in msg for s in ("timeout", "connection", "network", "server error", "rate limit"))
            if i < attempts - 1 and retryable:
                delay = min(base_delay * (backoff ** i), max_delay)
                log.warning(f"LLM call failed (attempt {i+1}/{attempts}); retrying in {delay:.1f}s: {e}")
                time.sleep(delay)
                continue
            break
    raise LLMError(f"LLM call failed after {attempts} attempts: {last}") from last


def _require_non_empty(name: str, value: Any):
    if not isinstance(value, str) or not value.strip():
        raise LLMError(f"{name} must be a non-empty string")


# ---------- public API (JSON-only) ----------

def generate_json(
    system: str,
    user: str,
    model: str,
    *,
    json_schema: Optional[Dict[str, Any]] = None,
    strict_schema: bool = True,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    retry: bool = True,
) -> Dict[str, Any]:
    """
    Generate structured JSON via the Responses API.
    - If `json_schema` is provided, schema enforcement is used (strict by default).
    - Returns a parsed dict.
    """
    _require_non_empty("system", system)
    _require_non_empty("user", user)
    _require_non_empty("model", model)

    params: Dict[str, Any] = {
        "model": model,  # Azure deployment name
        "input": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": _response_format(json_schema, strict_schema),
    }
    if temperature is not None:
        if not (0.0 <= temperature <= 2.0):
            raise LLMError("temperature must be between 0.0 and 2.0")
        params["temperature"] = float(temperature)
    if max_output_tokens is not None:
        if max_output_tokens <= 0:
            raise LLMError("max_output_tokens must be positive")
        params["max_output_tokens"] = int(max_output_tokens)

    client = _client()
    call = lambda: client.responses.create(**params)
    resp = _retry(call) if retry else call()

    txt = getattr(resp, "output_text", None)
    if not txt:
        raise LLMError("Responses API returned no output_text")

    # With strict schema, this should be clean JSON; still guard-parse.
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        # Best effort salvage if strict=False and model added prose
        start, end = txt.find("{"), txt.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(txt[start : end + 1])
        raise LLMError("Could not parse JSON from model output")
