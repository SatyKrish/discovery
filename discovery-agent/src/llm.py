from __future__ import annotations
import json
import logging
from typing import Any, Dict
from src.config import settings

class LLMError(Exception):
    pass

class _OpenAI:
    def __init__(self):
        from openai import OpenAI
        # Use OpenAI client for Azure and custom endpoints via base_url.
        kwargs: Dict[str, Any] = {}
        # Base URL resolution: explicit OPENAI base_url first
        if settings.openai_base_url:
            kwargs["base_url"] = settings.openai_base_url
        # API key resolution: pass through only if explicitly configured; otherwise rely on env
        if settings.openai_api_key:
            kwargs["api_key"] = settings.openai_api_key
        self.client = OpenAI(**kwargs)

    def json(self, system: str, user: str, model: str) -> Dict[str, Any]:
        # Use Responses API and require output_text
        try:
            resp = self.client.responses.create(
                model=model,
                input=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            txt = getattr(resp, "output_text", None)
            if not txt:
                raise LLMError("Responses API returned no output_text")
            return json.loads(txt)
        except Exception as e:
            logging.getLogger(__name__).exception("OpenAI Responses API call failed")
            raise LLMError(str(e)) from e


_def_provider = None

def _provider():
    global _def_provider
    if _def_provider:
        return _def_provider
    _def_provider = _OpenAI()
    return _def_provider

# naive JSON repair

def _coerce_json(txt: str) -> str:
    start = txt.find("{")
    end = txt.rfind("}")
    if start != -1 and end != -1 and end > start:
        return txt[start:end+1]
    raise LLMError("No JSON object found in LLM reply")

def llm_json(system: str, user: str, model: str) -> Dict[str, Any]:
    return _provider().json(system, user, model)
