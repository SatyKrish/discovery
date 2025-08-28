import sys
import types
import pytest
from pathlib import Path

# Stub temporalio to avoid dependency in tests
activity_module = types.SimpleNamespace(defn=lambda f: f)
temporal_stub = types.ModuleType("temporalio")
temporal_stub.activity = activity_module
sys.modules["temporalio"] = temporal_stub

# Ensure the temporal modules are importable
sys.path.append(str(Path(__file__).resolve().parents[1] / "temporal"))

from agent_activities import AgentActivities


@pytest.mark.asyncio
async def test_agent_toolplanner_valid():
    activities = AgentActivities()
    prompt = '{"tool": "add", "args": {"a": 1, "b": 2}}'
    result = await activities.agent_toolPlanner(prompt)
    assert result == 3


@pytest.mark.asyncio
async def test_agent_toolplanner_unknown_tool():
    activities = AgentActivities()
    prompt = '{"tool": "missing", "args": {}}'
    with pytest.raises(KeyError):
        await activities.agent_toolPlanner(prompt)


@pytest.mark.asyncio
async def test_agent_validatePrompt_valid():
    activities = AgentActivities()
    prompt = '{"tool": "echo", "args": {"text": "hi"}}'
    parsed = await activities.agent_validatePrompt(prompt)
    assert parsed["tool"] == "echo"
    assert parsed["args"]["text"] == "hi"


@pytest.mark.asyncio
async def test_agent_validatePrompt_invalid_json():
    activities = AgentActivities()
    bad_prompt = '{tool:"nope"}'
    with pytest.raises(ValueError):
        await activities.agent_validatePrompt(bad_prompt)


@pytest.mark.asyncio
async def test_get_wf_env_vars(monkeypatch):
    activities = AgentActivities()
    monkeypatch.setenv("OPENAI_API_KEY", "openai")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic")
    result = await activities.get_wf_env_vars()
    assert result == {"OPENAI_API_KEY": "openai", "ANTHROPIC_API_KEY": "anthropic"}
