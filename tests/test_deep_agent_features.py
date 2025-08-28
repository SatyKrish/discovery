import sys
import types
from pathlib import Path
import pytest
from langchain_core.messages import AIMessage, ToolMessage

# Stubs for optional dependencies so deep_agent can be imported without them.
mcp_module = types.ModuleType("mcp")
client_module = types.ModuleType("mcp.client")
session_module = types.ModuleType("mcp.client.session")
stream_module = types.ModuleType("mcp.client.streamable_http")
openai_stub = types.ModuleType("openai_model")


class _DummyClientSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def initialize(self):
        pass

    async def list_tools(self):
        return types.SimpleNamespace(tools=[])

    async def call_tool(self, name, kwargs):
        return types.SimpleNamespace(content=[])


async def _dummy_streamable_client(*args, **kwargs):
    class _Ctx:
        async def __aenter__(self):
            return (None, None, None)

        async def __aexit__(self, *args):
            pass

    return _Ctx()


session_module.ClientSession = _DummyClientSession
stream_module.streamablehttp_client = _dummy_streamable_client
sys.modules["mcp"] = mcp_module
sys.modules["mcp.client"] = client_module
sys.modules["mcp.client.session"] = session_module
sys.modules["mcp.client.streamable_http"] = stream_module


def _stub_get_default_model():
    class _Model:
        def bind_tools(self, tools):
            return self

        async def ainvoke(self, messages):
            return AIMessage(content="")

    return _Model()


openai_stub.get_default_model = _stub_get_default_model
sys.modules["openai_model"] = openai_stub

# Make deep_agent importable
sys.path.append(str(Path(__file__).resolve().parents[1] / "discovery-agent/temporal"))
import deep_agent
from deep_agent import run_agent, SUBAGENTS


class FileTodoModel:
    """Model that writes a file and records todos before finishing."""

    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, tools):
        return self

    async def ainvoke(self, messages):
        self.calls += 1
        if self.calls == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "1",
                        "name": "write_file",
                        "args": {"path": "a.txt", "content": "hello"},
                    }
                ],
            )
        elif self.calls == 2:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "2",
                        "name": "write_todos",
                        "args": {"items": ["task1", "task2"]},
                    }
                ],
            )
        return AIMessage(content="done")


@pytest.mark.asyncio
async def test_file_and_todo_operations():
    state: dict = {}
    result = await run_agent("start", model=FileTodoModel(), _state=state, _steps=5)
    assert result == "done"
    assert state["files"]["a.txt"] == "hello"
    assert state["todos"] == ["task1", "task2"]


class RouterDelegationModel:
    """Model that delegates to a subagent selected by the router."""

    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, tools):
        return self

    async def ainvoke(self, messages):
        self.calls += 1
        if self.calls == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "1",
                        "name": "call_subagent",
                        "args": {"question": "inner", "description": "write docs"},
                    }
                ],
            )
        elif self.calls == 2:
            return AIMessage(content="inner done")
        return AIMessage(content="outer done")


@pytest.mark.asyncio
async def test_subagent_delegation_uses_router(monkeypatch):
    calls = []
    orig = deep_agent.run_agent

    async def recording_run_agent(*args, **kwargs):
        calls.append((args, kwargs))
        return await orig(*args, **kwargs)

    monkeypatch.setattr(deep_agent, "run_agent", recording_run_agent)

    model = RouterDelegationModel()
    result = await deep_agent.run_agent("task", model=model, _state={}, _steps=5)
    assert result == "outer done"
    assert len(calls) == 2
    inner_args, _ = calls[1]
    expected = SUBAGENTS["docs"]["instructions"]
    assert inner_args[1] == expected


class BlockToolModel:
    """Model that attempts to call a disallowed tool."""

    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, tools):
        return self

    async def ainvoke(self, messages):
        self.calls += 1
        if self.calls == 1:
            return AIMessage(
                content="",
                tool_calls=[{"id": "1", "name": "ls", "args": {}}],
            )
        return AIMessage(content="done")


@pytest.mark.asyncio
async def test_allow_list_blocks_tools():
    state: dict = {}
    result = await run_agent(
        "task", model=BlockToolModel(), allow_tools=["read_file"], _state=state, _steps=3
    )
    assert result == "done"
    tool_msgs = [m for m in state["messages"] if isinstance(m, ToolMessage)]
    assert any("blocked" in m.content for m in tool_msgs)


class InfiniteModel:
    """Model that never stops invoking tools."""

    def bind_tools(self, tools):
        return self

    async def ainvoke(self, messages):
        return AIMessage(content="", tool_calls=[{"id": "1", "name": "ls", "args": {}}])


@pytest.mark.asyncio
async def test_step_limit_enforced():
    result = await run_agent("task", model=InfiniteModel(), _state={}, _steps=1)
    assert result == "Agent stopped: maximum steps exceeded"
