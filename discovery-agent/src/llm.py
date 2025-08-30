from __future__ import annotations
import json
from typing import Any, Dict
from discovery_agent.config import settings

class LLMError(Exception):
    pass

class _OpenAI:
    def __init__(self):
        from openai import OpenAI
        if not settings.openai_api_key:
            raise LLMError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=settings.openai_api_key)

    def json(self, system: str, user: str, model: str) -> Dict[str, Any]:
        resp = self.client.responses.create(
            model=model,
            response_format={"type": "json_object"},
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        txt = resp.output_text
        return json.loads(txt)

class _Anthropic:
    def __init__(self):
        import anthropic
        if not settings.anthropic_api_key:
            raise LLMError("ANTHROPIC_API_KEY not set")
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def json(self, system: str, user: str, model: str) -> Dict[str, Any]:
        msg = self.client.messages.create(
            model=model,
            system=system,
            max_tokens=2048,
            messages=[{"role": "user", "content": user}],
        )
        content = "".join([b.text for b in msg.content if getattr(b, "type", None) == "text"])  # type: ignore[attr-defined]
        return json.loads(_coerce_json(content))

_def_provider = None

def _provider():
    global _def_provider
    if _def_provider:
        return _def_provider
    if settings.llm_provider.lower() == "anthropic":
        _def_provider = _Anthropic()
    else:
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
