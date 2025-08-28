"""Minimal DeepAgent implementation used by Temporal workflows.

This version mirrors the capabilities of the LangGraph DeepAgent but is
implemented without any LangGraph dependency.  It maintains an in-memory
filesystem and todo list, exposes those via built-in tools, and can
recursively delegate work through a ``call_subagent`` tool.  The agent uses
OpenAI's tool-calling to decide when to invoke tools and stops when the model
returns a final message with no tool calls.

Subagents are configured via a registry mapping names to instruction strings
and optional metadata.  The ``router`` tool selects a subagent based on a
natural-language description.  ``call_subagent`` accepts either an explicit
subagent name or a description and dispatches to :func:`run_agent` with the
corresponding instructions.
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool, tool

from openai_model import get_default_model

# -------------------------------
# Subagent registry
# -------------------------------

SUBAGENTS: Dict[str, Dict[str, Any]] = {
    "code": {
        "instructions": "You are a coding specialist. Focus on writing and modifying code.",
        "keywords": ["code", "bug", "implement", "function", "module"],
    },
    "docs": {
        "instructions": "You write and update documentation and explanatory text.",
        "keywords": ["doc", "document", "explain", "write", "docs"],
    },
}


def _select_subagent(description: str) -> str:
    """Heuristically choose a subagent based on keywords in ``description``."""
    desc = description.lower()
    for name, cfg in SUBAGENTS.items():
        for kw in cfg.get("keywords", []):
            if kw in desc:
                return name
    # fallback to first registered subagent
    return next(iter(SUBAGENTS))

BASE_PROMPT = """
You are DeepAgent, an autonomous coding assistant.  You have access to a
virtual in-memory filesystem and a todo list.  Use these tools to plan and
edit files:

- write_todos(items: list[str]) -> record tasks in the shared todo list
- ls() -> list available filenames in the virtual filesystem
- read_file(path: str) -> read a file from the virtual filesystem
- write_file(path: str, content: str) -> create or overwrite a file
- edit_file(path: str, content: str) -> replace a file's contents
- router(description: str) -> choose a subagent name for a task
- call_subagent(question: str, subagent: str | None = None, description: str = "")
  -> delegate a subtask to another agent that shares the same state

Plan your work with ``write_todos`` and update files as needed.  When the
work is complete, respond with the final answer.
""".strip()


async def run_agent(
    question: str,
    instructions: str = "",
    tools: Sequence[BaseTool] | None = None,
    *,
    _state: Dict[str, Any] | None = None,
    _steps: int = 20,
) -> str:
    """Execute the DeepAgent loop and return the final response text."""

    state = _state or {"files": {}, "todos": []}
    files: Dict[str, str] = state["files"]
    todos: List[str] = state["todos"]
    extra_tools = list(tools or [])

    @tool
    def write_todos(items: List[str]) -> str:
        todos.extend(items)
        return f"Recorded {len(items)} todos"

    @tool
    def ls() -> List[str]:
        return list(files.keys())

    @tool
    def read_file(path: str) -> str:
        return files.get(path, "")

    @tool
    def write_file(path: str, content: str) -> str:
        files[path] = content
        return "ok"

    @tool
    def edit_file(path: str, content: str) -> str:
        files[path] = content
        return "ok"

    @tool
    def router(description: str) -> str:
        """Select the appropriate subagent name for ``description``."""
        return _select_subagent(description)

    @tool
    async def call_subagent(
        question: str, subagent: str | None = None, description: str = ""
    ) -> str:
        """Delegate ``question`` to a specialized subagent."""
        name = subagent or _select_subagent(description or question)
        config = SUBAGENTS.get(name, {})
        instr = config if isinstance(config, str) else config.get("instructions", "")
        return await run_agent(
            question,
            instr,
            extra_tools,
            _state=state,
            _steps=_steps,
        )

    builtin_tools: List[BaseTool] = [
        write_todos,
        ls,
        read_file,
        write_file,
        edit_file,
        router,
        call_subagent,
    ]
    all_tools: List[BaseTool] = builtin_tools + extra_tools
    tool_map = {t.name: t for t in all_tools}

    model = get_default_model().bind_tools(all_tools)

    system = BASE_PROMPT + ("\n\n" + instructions if instructions else "")
    messages: List[Any] = [SystemMessage(content=system), HumanMessage(content=question)]

    for _ in range(_steps):
        ai: AIMessage = await model.ainvoke(messages)
        messages.append(ai)
        if not ai.tool_calls:
            return ai.content or ""
        for call in ai.tool_calls:
            tool_obj = tool_map.get(call["name"])
            if not tool_obj:
                messages.append(
                    ToolMessage(
                        content=f"Unknown tool {call['name']}",
                        tool_call_id=call["id"],
                    )
                )
                continue
            result = await tool_obj.ainvoke(call.get("args", {}))
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return "Agent stopped: maximum steps exceeded"

