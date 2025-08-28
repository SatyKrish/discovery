from __future__ import annotations

"""Temporal activities used by the Discovery agent workflow.

This module exposes a small set of activities that help orchestrate the
agent's behaviour within a Temporal workflow.  Activities cover prompt
validation, planning tool calls and retrieving environment variables for the
workflow run.
"""

from dataclasses import dataclass
import json
import os
from typing import Any, Dict
import logging

from temporalio import activity

# Support both package and direct module imports
try:
    from .tool_registry import TOOL_REGISTRY
except Exception:  # pragma: no cover - fallback for test import style
    from tool_registry import TOOL_REGISTRY


@dataclass
class AgentActivities:
    """Collection of Temporal activities for the agent workflow."""

    def _sanitize_json(self, text: str) -> str:
        """Strip code fences and surrounding whitespace from ``text``.

        The agent may produce JSON wrapped in markdown code fences or preceded
        by a ``json`` language tag.  This helper removes those decorations so
        the remaining string can be parsed as valid JSON.
        """

        cleaned = text.strip()
        if cleaned.startswith("```") and cleaned.endswith("```"):
            cleaned = cleaned.strip("`\n")
            if "\n" in cleaned:
                first, rest = cleaned.split("\n", 1)
                if first.strip().lower() == "json":
                    cleaned = rest
                else:
                    cleaned = first + rest
        return cleaned

    def _parse_json(self, text: str) -> Dict[str, Any]:
        """Parse ``text`` into a JSON object after sanitisation."""

        try:
            return json.loads(self._sanitize_json(text))
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise ValueError("Invalid JSON") from exc

    def _dispatch_tool(self, name: str, args: Dict[str, Any]) -> Any:
        """Execute a tool from ``TOOL_REGISTRY``.

        Args:
            name: Name of the tool to execute.
            args: Arguments to pass to the tool handler.
        """

        logger = logging.getLogger(__name__)
        logger.info("activity.dispatch_tool.start", extra={"tool": name, "arg_keys": list(args.keys())})
        for definition, handler in TOOL_REGISTRY.items():
            if definition.name == name:
                try:
                    result = handler(**args)
                    logger.info("activity.dispatch_tool.completed", extra={"tool": name})
                    return result
                except Exception:
                    logger.exception("activity.dispatch_tool.error", extra={"tool": name})
                    raise
        logger.error("activity.dispatch_tool.unknown_tool", extra={"tool": name})
        raise KeyError(f"Unknown tool: {name}")

    @activity.defn
    async def agent_toolPlanner(self, prompt: str) -> Any:
        """Plan and execute a tool call based on ``prompt``.

        ``prompt`` should contain JSON with ``tool`` and optional ``args``
        fields.  The named tool is executed and its return value provided
        verbatim.
        """
        logger = logging.getLogger(__name__)
        logger.info("activity.agent_toolPlanner.start", extra={"prompt_len": len(prompt or "")})
        data = self._parse_json(prompt)
        tool_name = data.get("tool")
        if not tool_name:
            raise ValueError("Missing 'tool' field")
        args = data.get("args", {})
        if not isinstance(args, dict):
            raise ValueError("'args' must be an object")
        result = self._dispatch_tool(tool_name, args)
        logger.info("activity.agent_toolPlanner.completed", extra={"tool": tool_name})
        return result

    @activity.defn
    async def agent_validatePrompt(self, prompt: str) -> Dict[str, Any]:
        """Validate ``prompt`` and return the parsed structure.

        Validation ensures that the required ``tool`` key exists and that
        ``args`` is a JSON object if supplied.
        """
        logger = logging.getLogger(__name__)
        logger.info("activity.agent_validatePrompt.start", extra={"prompt_len": len(prompt or "")})
        data = self._parse_json(prompt)
        if "tool" not in data:
            raise ValueError("Missing 'tool' field")
        if "args" in data and not isinstance(data["args"], dict):
            raise ValueError("'args' must be an object")
        logger.info("activity.agent_validatePrompt.completed", extra={"has_args": "args" in data})
        return data

    @activity.defn
    async def get_wf_env_vars(self) -> Dict[str, str]:
        """Return relevant environment variables for the workflow."""
        logger = logging.getLogger(__name__)        
        keys = [
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_API_VERSION",
        ]
        redacted = {key: bool(os.environ.get(key)) for key in keys}
        logger.info("activity.get_wf_env_vars", extra={"keys_present": redacted})
        return {key: os.environ.get(key, "") for key in keys}
