import json
from types import SimpleNamespace

import agents
import pytest
from temporalio import workflow
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from src.activities import decision_agents_activity
from src.models_subagent import SubAgentSpec
from src.workflows.subagent import SubAgentWorkflow


@pytest.mark.asyncio
async def test_decision_filters_allowed_tools(monkeypatch):
    def fake_llm(system, user, model, json_schema=None):
        return {
            "type": "spawn_subagents",
            "subagents": [
                {
                    "kind": "researcher",
                    "goal": "g",
                    "allowed_tools": ["prov/a", "prov/b"],
                    "instructions_ref": "prov/pack1",
                }
            ],
        }

    monkeypatch.setattr("src.activities.llm_json", fake_llm)
    context = {
        "available_tools": [{"name": "prov/a"}],
        "available_prompts": ["prov/pack1"],
    }
    out = await decision_agents_activity(context)
    assert out["subagents"][0]["allowed_tools"] == ["prov/a"]
    assert out["subagents"][0]["instructions_ref"] == "prov/pack1"
@workflow.defn
class ParentWorkflow:
    def __init__(self):
        self.req = None

    @workflow.signal
    async def request_tool_access(self, child_id, tools, rationale):
        self.req = (child_id, tools, rationale)

    @workflow.run
    async def run(self):
        spec = SubAgentSpec(
            kind="test",
            goal="g",
            allowed_tools=[],
            instructions_ref="pack",
        )
        child = workflow.start_child_workflow(
            SubAgentWorkflow.run,
            spec,
            id=f"{workflow.info().workflow_id}/child",
            task_queue=workflow.info().task_queue,
        )
        await workflow.wait_condition(lambda: self.req is not None)
        await child.signal("grant_tool_access", self.req[1])
        return await child


@pytest.mark.skip(reason="requires Temporal test server")
@pytest.mark.asyncio
async def test_subagent_requests_tool_access(monkeypatch):
    async def fake_get_prompt(prompt_id: str):
        return {"success": True, "text": "", "tools": ["prov/extra"]}

    async def fake_mcp_invoke(tool_name: str, args: dict):
        return {"success": True}

    monkeypatch.setattr(
        "src.workflows.subagent.GetPromptActivity", fake_get_prompt
    )
    monkeypatch.setattr(
        "src.workflows.subagent.MCPInvokeActivity", fake_mcp_invoke
    )

    outputs = [
        SimpleNamespace(
            final_output=json.dumps(
                {"request_tools": ["prov/extra"], "rationale": "need"}
            ),
            new_items=[],
        ),
        SimpleNamespace(final_output="DONE", new_items=[]),
    ]

    async def fake_run(agent, msgs, run_config=None, max_turns=None):
        return outputs.pop(0)

    monkeypatch.setattr(agents.Runner, "run", fake_run)

    env = await WorkflowEnvironment.start_time_skipping()
    async with env:
        worker = Worker(
            env.client,
            task_queue="test",
            workflows=[SubAgentWorkflow, ParentWorkflow],
            activities=[fake_get_prompt, fake_mcp_invoke],
        )
        async with worker:
            result = await env.client.execute_workflow(
                ParentWorkflow.run, id="parent", task_queue="test"
            )

    assert result.ok
    assert result.message == "DONE"

