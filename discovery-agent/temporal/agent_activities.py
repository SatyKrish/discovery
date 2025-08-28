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

from temporalio import activity

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

        for definition, handler in TOOL_REGISTRY.items():
            if definition.name == name:
                return handler(**args)
        raise KeyError(f"Unknown tool: {name}")

    @activity.defn
    async def agent_toolPlanner(self, prompt: str) -> Any:
        """Plan and execute a tool call based on ``prompt``.

        ``prompt`` should contain JSON with ``tool`` and optional ``args``
        fields.  The named tool is executed and its return value provided
        verbatim.
        """

        data = self._parse_json(prompt)
        tool_name = data.get("tool")
        if not tool_name:
            raise ValueError("Missing 'tool' field")
        args = data.get("args", {})
        if not isinstance(args, dict):
            raise ValueError("'args' must be an object")
        return self._dispatch_tool(tool_name, args)

    @activity.defn
    async def agent_validatePrompt(self, prompt: str) -> Dict[str, Any]:
        """Validate ``prompt`` and return the parsed structure.

        Validation ensures that the required ``tool`` key exists and that
        ``args`` is a JSON object if supplied.
        """

        data = self._parse_json(prompt)
        if "tool" not in data:
            raise ValueError("Missing 'tool' field")
        if "args" in data and not isinstance(data["args"], dict):
            raise ValueError("'args' must be an object")
        return data

    @activity.defn
    async def get_wf_env_vars(self) -> Dict[str, str]:
        """Return relevant environment variables for the workflow."""

        keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
        return {key: os.environ.get(key, "") for key in keys}
