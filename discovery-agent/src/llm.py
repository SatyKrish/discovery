from __future__ import annotations
import json
from typing import Any, Dict
from src.config import settings

class LLMError(Exception):
    pass

class _OpenAI:
    def __init__(self):
        from openai import OpenAI
        # For local providers like Ollama, an API key may not be required.
        kwargs = {}
        if settings.openai_api_key:
            kwargs["api_key"] = settings.openai_api_key
        if settings.openai_base_url:
            kwargs["base_url"] = settings.openai_base_url
        self.client = OpenAI(**kwargs)

    def json(self, system: str, user: str, model: str) -> Dict[str, Any]:
        # Prefer Responses API when available; fallback to Chat Completions for Ollama/OpenAI-compatible servers
        try:
            resp = self.client.responses.create(
                model=model,
                response_format={"type": "json_object"},
                input=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            txt = getattr(resp, "output_text", None)
            if not txt:
                # Some servers don’t implement output_text; extract from content
                txt = "".join([getattr(p, "text", "") for p in getattr(resp, "output", [])])
            return json.loads(txt)
        except Exception:
            # Fallback path for Ollama and other compat servers without Responses API
            cmpl = self.client.chat.completions.create(
                model=model,
                temperature=0,
                messages=[
                    {"role": "system", "content": system + "\nReturn ONLY valid JSON."},
                    {"role": "user", "content": user},
                ],
            )
            content = None
            if cmpl.choices:
                # OpenAI SDK returns content as a string for chat
                content = cmpl.choices[0].message.content
                # Some compat servers might return list of parts
                if isinstance(content, list):
                    content = "".join(str(p) for p in content)
            if not content:
                raise LLMError("Empty response from model")
            return json.loads(_coerce_json(str(content)))

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
