import asyncio
import sys
import types
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Minimal Temporal stubs so the workflow module can be imported in tests
# ---------------------------------------------------------------------------
workflow_stub = types.SimpleNamespace(
    defn=lambda cls: cls,
    run=lambda f: f,
    signal=lambda f: f,
    query=lambda f: f,
)


async def _wait_condition(cond):
    while not cond():
        await asyncio.sleep(0)


async def _execute_activity(fn, *args, **kwargs):
    # Ignore Temporal activity options such as timeouts
    return await fn(*args)


workflow_stub.wait_condition = _wait_condition
workflow_stub.execute_activity = _execute_activity
workflow_stub.continue_as_new = lambda *a, **k: None

temporal_stub = types.ModuleType("temporalio")
temporal_stub.workflow = workflow_stub
temporal_stub.activity = types.SimpleNamespace(defn=lambda f: f)
sys.modules["temporalio"] = temporal_stub

# Provide a stub for the optional OpenAI module so imports succeed without
# requiring API keys or the real dependency.
openai_stub = types.ModuleType("openai_model")
openai_stub.get_default_model = lambda: None  # pragma: no cover - unused
sys.modules["openai_model"] = openai_stub


# Ensure the temporal modules are importable
sys.path.append(str(Path(__file__).resolve().parents[1] / "temporal"))

import importlib
import temporal_workflow as tw  # noqa: E402  - imported after stubbing
tw = importlib.reload(tw)


@pytest.mark.asyncio
async def test_signal_and_query_flow(monkeypatch):
    async def fake_run_query(question, instructions="", tools=None, mcp_endpoints=None):
        return f"resp:{question}", {"tool": question}

    monkeypatch.setattr(tw, "run_query", fake_run_query)

    wf = tw.DeepAgentWorkflow()

    task = asyncio.create_task(wf.run("q1", remaining_turns=2, continue_after=10))
    await asyncio.sleep(0)
    wf.confirm({"c1": True})
    wf.user_prompt("q2")
    await asyncio.sleep(0)
    wf.confirm({"c2": True})
    await task

    history = wf.get_conversation_history()
    assert [m for d in history for m in d.values()] == [
        "q1",
        "resp:q1",
        "q2",
        "resp:q2",
    ]
    assert wf.get_latest_tool_data() == {"c2": True}


@pytest.mark.asyncio
async def test_continue_as_new(monkeypatch):
    class ContinueSentinel(Exception):
        def __init__(self, args, kwargs):
            self.args_data = args
            self.kwargs_data = kwargs

    def fake_continue_as_new(*args, **kwargs):  # pragma: no cover - exercised
        raise ContinueSentinel(args, kwargs)

    proceed = asyncio.Event()

    async def fake_run_query(question, instructions="", tools=None, mcp_endpoints=None):
        await proceed.wait()
        return f"resp:{question}", None

    monkeypatch.setattr(workflow_stub, "continue_as_new", fake_continue_as_new)
    monkeypatch.setattr(tw, "run_query", fake_run_query)

    wf = tw.DeepAgentWorkflow()
    task = asyncio.create_task(wf.run("q1", remaining_turns=5, continue_after=1))
    await asyncio.sleep(0)  # allow run to start and block in fake_run_query
    wf.user_prompt("q2")
    proceed.set()

    with pytest.raises(ContinueSentinel) as exc:
        await task

    kwargs = exc.value.kwargs_data
    assert kwargs["conversation_history"][0]["user"] == "q1"
    assert kwargs["remaining_turns"] == 4
    assert kwargs["prompt_queue"] == ["q2"]

