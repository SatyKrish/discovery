import sys
import types
import pytest
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from pathlib import Path
from typing import Any


# Provide lightweight stubs for the optional MCP client modules so the
# deep_agent module can be imported without the dependency being installed.
mcp_module = types.ModuleType("mcp")
client_module = types.ModuleType("mcp.client")
session_module = types.ModuleType("mcp.client.session")
stream_module = types.ModuleType("mcp.client.streamable_http")
openai_stub = types.ModuleType("openai_model")
temporal_stub = types.ModuleType("temporalio")


def _stub_get_default_model():  # pragma: no cover - unused in tests
    class _Model:
        def bind_tools(self, tools):
            return self

        async def ainvoke(self, messages):
            return AIMessage(content="")

    return _Model()


openai_stub.get_default_model = _stub_get_default_model


class _DummyClientSession:
    async def __aenter__(self):  # pragma: no cover - unused in tests
        return self

    async def __aexit__(self, *args):  # pragma: no cover - unused
        pass

    async def initialize(self):  # pragma: no cover - unused
        pass

    async def list_tools(self):  # pragma: no cover - unused
        return types.SimpleNamespace(tools=[])

    async def call_tool(self, name, kwargs):  # pragma: no cover - unused
        return types.SimpleNamespace(content=[])


async def _dummy_streamable_client(*args, **kwargs):  # pragma: no cover - unused
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
sys.modules["openai_model"] = openai_stub
temporal_stub.activity = types.SimpleNamespace(defn=lambda f: f)
temporal_stub.workflow = types.SimpleNamespace(defn=lambda f: f, run=lambda f: f)
sys.modules["temporalio"] = temporal_stub

sys.path.append(str(Path(__file__).resolve().parent.parent / "temporal"))
from deep_agent import create_deep_agent, run_agent
import temporal_workflow


class DummyModel:
    """Simple stand-in model that records the prompt and returns a fixed reply."""

    def __init__(self, reply: str = "done") -> None:
        self.reply = reply
        self.last_messages = None
        self.bound_tools = None

    def bind_tools(self, tools):
        self.bound_tools = tools
        return self

    async def ainvoke(self, messages):
        self.last_messages = messages
        return AIMessage(content=self.reply)


@pytest.mark.asyncio
async def test_create_deep_agent_applies_base_prompt():
    model = DummyModel("hello")
    agent = create_deep_agent(base_prompt="BASE", model=model)
    result = await agent("question")
    assert result == "hello"
    # ensure the system message used our base prompt
    assert model.last_messages[0].content == "BASE"


@pytest.mark.asyncio
async def test_run_query_forwards_tools_and_endpoints(monkeypatch):
    called: dict[str, Any] = {}
    dummy_tool = object()

    def stub_load_tool(spec: str):
        called.setdefault("loaded", []).append(spec)
        return dummy_tool

    async def stub_agent(question, instructions="", **kwargs):
        called["agent_args"] = (question, instructions)
        return "ok"

    def stub_factory(**kwargs):
        called["factory_kwargs"] = kwargs
        return stub_agent

    monkeypatch.setattr(temporal_workflow, "_load_tool", stub_load_tool)
    monkeypatch.setattr(temporal_workflow, "create_deep_agent", stub_factory)

    result = await temporal_workflow.run_query(
        "Q", "I", tools=["pkg:tool"], mcp_endpoints=["http://server"]
    )
    assert result == "ok"
    assert called["agent_args"] == ("Q", "I")
    assert called["factory_kwargs"]["tools"] == [dummy_tool]
    assert called["factory_kwargs"]["mcp_endpoints"] == ["http://server"]
    assert called["loaded"] == ["pkg:tool"]


class ToolCallingModel:
    """Model that triggers a call_subagent tool call on first invoke."""

    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, tools):
        self.tools = tools
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
                        "args": {"question": "sub", "subagent": "code"},
                    }
                ],
            )
        elif self.calls == 2:
            return AIMessage(content="inner")
        return AIMessage(content="outer")


@pytest.mark.asyncio
async def test_call_subagent_forwards_factory_config(monkeypatch):
    import deep_agent

    calls = []
    orig = deep_agent.run_agent

    async def recording_run_agent(*args, **kwargs):
        calls.append((args, kwargs))
        return await orig(*args, **kwargs)

    monkeypatch.setattr(deep_agent, "run_agent", recording_run_agent)

    model = ToolCallingModel()
    sub_cfg = {"code": {"instructions": "do code"}}
    agent = deep_agent.create_deep_agent(
        base_prompt="PROMPT", model=model, subagents=sub_cfg
    )
    result = await agent("task")
    assert result == "outer"
    assert len(calls) == 2
    _, inner_kwargs = calls[1]
    assert inner_kwargs.get("base_prompt") == "PROMPT"
    assert inner_kwargs.get("model") is model
    assert inner_kwargs.get("subagents") == sub_cfg


class RouterModel:
    """Model that omits the subagent name and relies on the router."""

    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, tools):
        self.tools = tools
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
                        "args": {"question": "sub", "description": "write docs"},
                    }
                ],
            )
        elif self.calls == 2:
            return AIMessage(content="inner done")
        return AIMessage(content="outer done")


@pytest.mark.asyncio
async def test_call_subagent_uses_router(monkeypatch):
    import deep_agent

    calls = []
    orig = deep_agent.run_agent

    async def recording_run_agent(*args, **kwargs):
        calls.append((args, kwargs))
        return await orig(*args, **kwargs)

    monkeypatch.setattr(deep_agent, "run_agent", recording_run_agent)

    model = RouterModel()
    agent = deep_agent.create_deep_agent(model=model)
    result = await agent("task")
    assert result == "outer done"
    assert len(calls) == 2
    inner_args, _ = calls[1]
    expected = deep_agent.SUBAGENTS["docs"]["instructions"]
    assert inner_args[1] == expected


class EchoModel:
    """Model that returns a fixed response."""

    def bind_tools(self, tools):
        return self

    async def ainvoke(self, messages):
        return AIMessage(content="done")


@pytest.mark.asyncio
async def test_run_agent_tracks_state():
    state = {}
    result = await run_agent("hi", model=EchoModel(), _state=state, _steps=3)
    assert result == "done"
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

    assert isinstance(state["messages"][0], SystemMessage)
    assert isinstance(state["messages"][1], HumanMessage)
    assert isinstance(state["messages"][2], AIMessage)
    assert state["remaining_steps"] == 2
    assert state["response"] == {"content": "done"}


class InstructionTrackingModel:
    """Model that records messages across calls and triggers a subagent."""

    def __init__(self) -> None:
        self.calls = []
        self.step = 0

    def bind_tools(self, tools):
        self.tools = tools
        return self

    async def ainvoke(self, messages):
        self.calls.append(list(messages))
        self.step += 1
        if self.step == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "1",
                        "name": "call_subagent",
                        "args": {"question": "inner", "subagent": "code"},
                    }
                ],
            )
        elif self.step == 2:
            return AIMessage(content="inner done")
        return AIMessage(content="outer done")


@pytest.mark.asyncio
async def test_subagent_instructions_preserved():
    model = InstructionTrackingModel()
    result = await run_agent(
        "outer task", instructions="parent", model=model, _state={}, _steps=5
    )
    assert result == "outer done"
    sub_call_msgs = model.calls[1]
    assert isinstance(sub_call_msgs[-2], SystemMessage)
    assert "coding specialist" in sub_call_msgs[-2].content
    outer_call_msgs = model.calls[2]
    assert isinstance(outer_call_msgs[-2], SystemMessage)
    assert "parent" in outer_call_msgs[-2].content


class BlockToolModel:
    """Model that attempts to invoke a disallowed tool."""

    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, tools):
        self.tools = tools
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
async def test_allow_tools_blocks_unlisted_tool():
    state = {}
    result = await run_agent(
        "task", model=BlockToolModel(), allow_tools=["read_file"], _state=state, _steps=3
    )
    assert result == "done"
    tool_msgs = [m for m in state["messages"] if isinstance(m, ToolMessage)]
    assert any("blocked" in m.content for m in tool_msgs)


class ModifyArgsModel:
    """Model that writes a file whose content is tweaked by a callback."""

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
                        "args": {"path": "a.txt", "content": "orig"},
                    }
                ],
            )
        return AIMessage(content="done")


@pytest.mark.asyncio
async def test_on_tool_call_can_modify_args():
    state = {}

    def approve(name, args):
        assert name == "write_file"
        args["content"] = "changed"
        return True, args

    result = await run_agent(
        "task", model=ModifyArgsModel(), on_tool_call=approve, _state=state, _steps=3
    )
    assert result == "done"
    assert state["files"]["a.txt"] == "changed"

