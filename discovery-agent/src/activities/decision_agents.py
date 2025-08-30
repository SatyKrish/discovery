from __future__ import annotations
from temporalio import activity
from opentelemetry import trace
from agents import Agent, tool
from typing import Callable, Dict, Any, List
from src.registry import list_tool_specs

tracer = trace.get_tracer(__name__)

# Build agent-visible tool shims with per-tool JSON schemas

def _make_agent_tool(name: str, schema: Dict[str, Any], description: str) -> Callable[..., Dict[str, Any]]:
    param_names = list((schema.get("properties") or {}).keys())

    @tool(name=name, description=description, schema=schema)
    def _shim(**kwargs) -> Dict[str, Any]:
        for k in kwargs.keys():
            if k not in param_names:
                raise ValueError(f"Unexpected arg '{k}' for tool {name}")
        return {"_tool_request": {"name": name, "args": kwargs}}

    return _shim


def _collect_agent_tools() -> List[Callable[..., Dict[str, Any]]]:
    tools: List[Callable[..., Dict[str, Any]]] = []
    for spec in list_tool_specs():
        tools.append(_make_agent_tool(spec.name, spec.schema or {}, spec.description or spec.name))
    return tools

@activity.defn
async def decision_agents_activity(state_view: dict) -> dict:
    info = activity.info()
    with tracer.start_as_current_span("decision_agents_activity") as span:
        span.set_attribute("temporal.workflow_id", info.workflow_id)
        span.set_attribute("temporal.run_id", info.workflow_run_id)
        span.set_attribute("temporal.attempt", info.attempt)

        agent = Agent(
            name="orchestrator",
            instructions=(
                "Decide the single next action for a Temporal durable agent. "
                "Allowed types: assistant_message | tool_call | spawn_subagent | revise_plan. "
                "If you call a tool, the tool shim returns _tool_request; include it in your JSON output."
            ),
            tools=_collect_agent_tools(),
        )

        result = agent.run(input=state_view)

        if isinstance(result, dict) and "_tool_request" in result:
            tr = result["_tool_request"]
            return {
                "type": "tool_call",
                "call": {
                    "id": "tc-" + info.activity_id,
                    "name": tr.get("name"),
                    "args": tr.get("args", {}),
                    "requires_approval": False,
                },
                "message": None,
                "subagent_spec": None,
                "plan_diff": None,
            }

        if isinstance(result, dict):
            return result

        return {"type": "assistant_message", "message": {"role": "assistant", "content": str(result), "ts": 0}}
