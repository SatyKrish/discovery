"""Minimal DeepAgent implementation used by Temporal workflows.

This module provides a very small yet capable autonomous agent that mirrors the
behaviour of the LangGraph DeepAgent.  It maintains an in-memory filesystem and
todo list, exposes those via built-in tools, and can recursively delegate work
through a ``call_subagent`` tool.  The agent uses OpenAI's tool-calling to
decide when to invoke tools and stops when the model returns a final message
with no tool calls.

Subagents are configured via a registry mapping names to instruction strings
and optional metadata.  The ``router`` tool selects a subagent based on a
natural-language description.  ``call_subagent`` accepts either an explicit
subagent name or a description and dispatches to :func:`run_agent` with the
corresponding instructions.

External MCP servers or direct :class:`~langchain_core.tools.BaseTool` instances
can augment the agent.  Any provided tools are merged with the built-ins before
the model is bound::

    from langchain_community.tools import RequestsGetTool

    agent = create_deep_agent(tools=[RequestsGetTool()])
    await agent("2 + 2?")

``create_deep_agent`` is a small factory that fixes the base prompt, language
model, subagent registry, default tools, and step limit.  It returns an async
callable that mirrors :func:`run_agent` but with those configuration options
pre-applied, making it easier for callers to construct agents with consistent
defaults.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Sequence, TypedDict

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool, tool
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from openai_model import get_default_model


class AgentState(TypedDict, total=False):
    """State container shared across agent invocations.

    Mirrors LangGraph's ``AgentState`` by persisting the conversation ``messages``,
    the remaining step budget, the evolving in-memory ``files``/``todos`` and the
    final ``response``.
    """

    files: Dict[str, str]
    todos: List[str]
    messages: List[Any]
    remaining_steps: int
    response: Dict[str, Any] | None

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


def _select_subagent(description: str, subagents: Dict[str, Dict[str, Any]]) -> str:
    """Heuristically choose a subagent based on keywords in ``description``."""
    desc = description.lower()
    for name, cfg in subagents.items():
        for kw in cfg.get("keywords", []):
            if kw in desc:
                return name
    # fallback to first registered subagent
    return next(iter(subagents))

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
    mcp_endpoints: Sequence[str] | None = None,
    *,
    allow_tools: Iterable[str] | None = None,
    on_tool_call: Callable[[str, Dict[str, Any]], tuple[bool, Dict[str, Any]]] | None = None,
    _state: Dict[str, Any] | None = None,
    _steps: int = 20,
    base_prompt: str = BASE_PROMPT,
    model: Any | None = None,
    subagents: Dict[str, Dict[str, Any]] = SUBAGENTS,
) -> str:
    """Execute the DeepAgent loop and return the final response text.

    Additional tools from ``tools`` and ``mcp_endpoints`` are merged with the
    agent's built-ins before the model is bound.  Tool execution can be
    restricted via ``allow_tools`` and inspected or modified with the
    ``on_tool_call`` callback.
    """

    state: AgentState = (
        _state
        if _state is not None
        else {
            "files": {},
            "todos": [],
            "messages": [],
            "remaining_steps": _steps,
            "response": None,
        }
    )
    state.setdefault("files", {})
    state.setdefault("todos", [])
    state.setdefault("messages", [])
    state.setdefault("remaining_steps", _steps)
    state.setdefault("response", None)
    files: Dict[str, str] = state["files"]
    todos: List[str] = state["todos"]
    messages: List[Any] = state["messages"]
    extra_tools: List[BaseTool] = list(tools or [])
    if mcp_endpoints:
        for endpoint in mcp_endpoints:
            async with streamablehttp_client(endpoint) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    listing = await session.list_tools()
            for remote in listing.tools:
                @tool(name=remote.name, description=remote.description or "")
                async def _mcp_tool(
                    _endpoint: str = endpoint,
                    _name: str = remote.name,
                    **kwargs: Any,
                ) -> str:
                    async with streamablehttp_client(_endpoint) as (r, w, _):
                        async with ClientSession(r, w) as session:
                            await session.initialize()
                            result = await session.call_tool(_name, kwargs)
                    parts = [
                        item.text for item in result.content if hasattr(item, "text")
                    ]
                    return "\n".join(parts)

                extra_tools.append(_mcp_tool)
    allowed_tool_set = set(allow_tools) if allow_tools is not None else None

    @tool
    def write_todos(items: List[str]) -> str:
        """Record tasks in the shared todo list."""
        todos.extend(items)
        return f"Recorded {len(items)} todos"

    @tool
    def ls() -> List[str]:
        """List available filenames in the virtual filesystem."""
        return list(files.keys())

    @tool
    def read_file(path: str) -> str:
        """Read ``path`` from the virtual filesystem."""
        return files.get(path, "")

    @tool
    def write_file(path: str, content: str) -> str:
        """Create or overwrite ``path`` with ``content``."""
        files[path] = content
        return "ok"

    @tool
    def edit_file(path: str, content: str) -> str:
        """Replace the contents of ``path`` with ``content``."""
        files[path] = content
        return "ok"

    @tool
    def router(description: str) -> str:
        """Select the appropriate subagent name for ``description``."""
        return _select_subagent(description, subagents)

    @tool
    async def call_subagent(
        question: str, subagent: str | None = None, description: str = ""
    ) -> str:
        """Delegate ``question`` to a specialized subagent."""
        name = subagent or _select_subagent(description or question, subagents)
        config = subagents.get(name, {})
        instr = config if isinstance(config, str) else config.get("instructions", "")
        result = await run_agent(
            question,
            instr,
            tools=tools,
            mcp_endpoints=mcp_endpoints,
            allow_tools=allow_tools,
            on_tool_call=on_tool_call,
            _state=state,
            _steps=state.get("remaining_steps", _steps),
            base_prompt=base_prompt,
            model=model,
            subagents=subagents,
        )
        parent_system = base_prompt + ("\n\n" + instructions if instructions else "")
        messages.append(SystemMessage(content=parent_system))
        return result

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

    bound_model = (model or get_default_model()).bind_tools(all_tools)

    system = base_prompt + ("\n\n" + instructions if instructions else "")
    messages.append(SystemMessage(content=system))
    messages.append(HumanMessage(content=question))

    while state["remaining_steps"] > 0:
        state["remaining_steps"] -= 1
        ai: AIMessage = await bound_model.ainvoke(messages)
        messages.append(ai)
        if not ai.tool_calls:
            state["response"] = {"content": ai.content or ""}
            return ai.content or ""
        for call in ai.tool_calls:
            name = call["name"]
            tool_obj = tool_map.get(name)
            if not tool_obj:
                messages.append(
                    ToolMessage(
                        content=f"Unknown tool {name}",
                        tool_call_id=call["id"],
                    )
                )
                continue
            if allowed_tool_set is not None and name not in allowed_tool_set:
                messages.append(
                    ToolMessage(
                        content=f"Tool {name} blocked",
                        tool_call_id=call["id"],
                    )
                )
                continue
            call_args = call.get("args", {})
            if on_tool_call:
                allowed, call_args = on_tool_call(name, call_args)
                if not allowed:
                    messages.append(
                        ToolMessage(
                            content=f"Tool {name} denied",
                            tool_call_id=call["id"],
                        )
                    )
                    continue
            result = await tool_obj.ainvoke(call_args)
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return "Agent stopped: maximum steps exceeded"


def create_deep_agent(
    *,
    base_prompt: str = BASE_PROMPT,
    model: Any | None = None,
    subagents: Dict[str, Dict[str, Any]] | None = None,
    tools: Sequence[BaseTool] | None = None,
    mcp_endpoints: Sequence[str] | None = None,
    step_limit: int = 20,
) -> Callable[..., Any]:
    """Factory returning a callable that executes :func:`run_agent`.

    Parameters mirror those of :func:`run_agent` but are applied up-front so
    callers need only provide the question (and optional instructions) each
    time the returned callable is invoked.
    """

    subagent_cfg = subagents or SUBAGENTS

    async def _agent(
        question: str,
        instructions: str = "",
        *,
        allow_tools: Iterable[str] | None = None,
        on_tool_call: Callable[[str, Dict[str, Any]], tuple[bool, Dict[str, Any]]] | None = None,
        _state: Dict[str, Any] | None = None,
    ) -> str:
        return await run_agent(
            question,
            instructions,
            tools=tools,
            mcp_endpoints=mcp_endpoints,
            allow_tools=allow_tools,
            on_tool_call=on_tool_call,
            _state=_state,
            _steps=step_limit,
            base_prompt=base_prompt,
            model=model,
            subagents=subagent_cfg,
        )

    return _agent

