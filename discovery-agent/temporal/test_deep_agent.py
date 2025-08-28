import sys
import types
import pytest
from langchain_core.messages import AIMessage
from pathlib import Path


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

sys.path.append(str(Path(__file__).resolve().parent.parent))
from deep_agent import create_deep_agent
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
async def test_run_query_uses_factory(monkeypatch):
    called = {}

    async def stub_agent(question, instructions=""):
        called["args"] = (question, instructions)
        return "ok"

    def stub_factory(**kwargs):
        called["factory_kwargs"] = kwargs
        return stub_agent

    monkeypatch.setattr(temporal_workflow, "create_deep_agent", stub_factory)

    result = await temporal_workflow.run_query("Q", "I")
    assert result == "ok"
    assert called["args"] == ("Q", "I")


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

