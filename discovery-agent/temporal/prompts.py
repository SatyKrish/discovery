from __future__ import annotations

"""Prompt templates and rendering helpers for Temporal agents.

This module centralises the text templates used by the Temporal agent
workflows.  Templates are simple ``str.format`` strings with placeholders for
runtime values.  Helper functions safely render the templates while escaping
any curly braces in the provided values so that user content does not
interfere with ``str.format`` substitution.
"""

from typing import Iterable, Mapping, Sequence

__all__ = [
    "GENAI_PROMPT",
    "TOOL_COMPLETION_PROMPT",
    "render_genai_prompt",
    "render_tool_completion_prompt",
]

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

GENAI_PROMPT = (
    "You are an AI assistant.\n\n"
    "Current goal:\n{goal}\n\n"
    "Conversation so far:\n{history}\n\n"
    "You can use the following tools:\n{tools}\n\n"
    "Respond with the next action or final answer."
)

TOOL_COMPLETION_PROMPT = (
    "The tool \"{tool}\" has completed with result:\n\n"
    "{result}\n\n"
    "Continue assisting the user toward the goal:\n{goal}"
)


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

def render_genai_prompt(
    history: Sequence[Mapping[str, str]],
    goal: str,
    tools: Iterable[str],
) -> str:
    """Render ``GENAI_PROMPT`` with ``history``, ``goal`` and ``tools``.

    Args:
        history: Sequence of message mappings with ``role`` and ``content`` keys.
        goal: The current objective for the agent.
        tools: Iterable of tool names available to the agent.
    """

    history_lines = [f"{m['role']}: {m['content']}" for m in history]
    history_text = "\n".join(history_lines) if history_lines else "<no conversation>"
    tools_text = "\n".join(f"- {t}" for t in tools) if tools else "<no tools>"
    return GENAI_PROMPT.format(history=history_text, goal=goal, tools=tools_text)


def render_tool_completion_prompt(tool: str, result: str, goal: str) -> str:
    """Render ``TOOL_COMPLETION_PROMPT`` for a completed tool call."""

    return TOOL_COMPLETION_PROMPT.format(tool=tool, result=result, goal=goal)
