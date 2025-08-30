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
        self.last_response_id = None  # Track conversation state

    def create_response(self, user_message: str, model: str, tools=None, system_message=None):
        """Create a response using OpenAI Responses API with multi-turn state management"""
        input_messages = []

        # Add system message if provided (only for first turn)
        if system_message and not self.last_response_id:
            input_messages.append({"role": "system", "content": system_message})

        # Add user message
        input_messages.append({"role": "user", "content": user_message})

        # Prepare API call
        kwargs = {
            "model": model,
            "input": input_messages,
        }

        # Add previous response ID for multi-turn conversation
        if self.last_response_id:
            kwargs["previous_response_id"] = self.last_response_id

        # Add tools if provided
        if tools:
            kwargs["tools"] = tools

        try:
            resp = self.client.responses.create(**kwargs)

            # Store response ID for next turn (multi-turn state management)
            self.last_response_id = resp.id

            return resp
        except Exception as e:
            logging.getLogger(__name__).exception("OpenAI Responses API call failed")
            raise LLMError(str(e)) from e

    def json(self, system: str, user: str, model: str) -> Dict[str, Any]:
        """Legacy method for backward compatibility - creates response and extracts JSON"""
        try:
            resp = self.create_response(user, model, system_message=system)
            txt = getattr(resp, "output_text", None)
            if not txt:
                raise LLMError("Responses API returned no output_text")
            return json.loads(txt)
        except Exception as e:
            logging.getLogger(__name__).exception("OpenAI Responses API call failed")
            raise LLMError(str(e)) from e

    def get_last_response_id(self):
        """Get the last response ID for workflow state management"""
        return self.last_response_id

    def reset_conversation(self):
        """Reset conversation state (useful for new sessions)"""
        self.last_response_id = None


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
