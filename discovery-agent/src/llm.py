# ──────────────────────────────────────────────────────────────────────────────
# File: src/llm.py
# OpenAI Responses API helper with structured output + tools support
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import json
import logging
from typing import Any, Dict, Optional
from src.config import settings

log = logging.getLogger(__name__)

class LLMError(Exception):
    pass

class _OpenAI:
    def __init__(self):
        from openai import OpenAI
        kwargs: Dict[str, Any] = {}
        if settings.openai_base_url:
            kwargs["base_url"] = settings.openai_base_url
        if settings.openai_api_key:
            kwargs["api_key"] = settings.openai_api_key
        self.client = OpenAI(**kwargs)

    def json(self, system: str, user: str, model: str,
             *, json_schema: Optional[Dict[str, Any]] = None,
             temperature: Optional[float] = None,
             max_output_tokens: Optional[int] = None) -> Dict[str, Any]:
        try:
            params: Dict[str, Any] = {
                "model": model,
                "input": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "text": {
                    "format": {"type": "json_object"}
                },
            }

            if json_schema:
                params["text"] = {
                    "format": {
                        "type": "json_schema",
                        "name": "discovery_output",
                        "schema": json_schema,
                        "strict": False  # Relaxed for decision-making phase
                    }
                }
            else:
                params["text"] = {
                    "format": {"type": "json_object"}
                }
            if temperature is not None:
                params["temperature"] = temperature
            if max_output_tokens is not None:
                params["max_output_tokens"] = max_output_tokens

            resp = self.client.responses.create(**params)
            txt = getattr(resp, "output_text", None)
            if not txt:
                raise LLMError("Responses API returned no output_text")
            try:
                return json.loads(txt)
            except json.JSONDecodeError:
                salvaged = _coerce_json(txt)
                return json.loads(salvaged)
        except Exception as e:
            log.exception("OpenAI Responses API call failed")
            raise LLMError(str(e)) from e

    def tools(self, messages: list[dict], tools: list[dict], model: str,
              *, tool_choice: str = "auto") -> Any:
        try:
            resp = self.client.responses.create(
                model=model,
                input=messages,
                tools=tools,
                tool_choice=tool_choice,
            )
            return resp
        except Exception as e:
            log.exception("OpenAI Responses API (tools) call failed")
            raise LLMError(str(e)) from e

_def_provider: _OpenAI | None = None

def _provider() -> _OpenAI:
    global _def_provider
    if _def_provider:
        return _def_provider
    _def_provider = _OpenAI()
    return _def_provider

# naive JSON salvage when model wraps JSON in prose

def _coerce_json(txt: str) -> str:
    start = txt.find("{")
    end = txt.rfind("}")
    if start != -1 and end != -1 and end > start:
        return txt[start : end + 1]
    raise LLMError("No JSON object found in LLM reply")

# public convenience

def llm_json(system: str, user: str, model: str, **kw) -> Dict[str, Any]:
    return _provider().json(system, user, model, **kw)
