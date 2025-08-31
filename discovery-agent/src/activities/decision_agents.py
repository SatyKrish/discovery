from __future__ import annotations
from temporalio import activity
from opentelemetry import trace
from agents import Agent, FunctionTool
from agents.run import Runner
from typing import Callable, Dict, Any, List
import json
from src.registry import list_tool_specs

tracer = trace.get_tracer(__name__)

# Build agent-visible tool shims with per-tool JSON schemas

def _make_agent_tool(name: str, schema: Dict[str, Any], description: str) -> FunctionTool:
    async def _on_invoke_tool(ctx, input: str):
        try:
            args = json.loads(input) if input else {}
        except Exception:
            args = {}
        # Provide a sentinel that decision_agents_activity will convert to a ToolCall action
        return {"_tool_request": {"name": name, "args": args}}

    return FunctionTool(
        name=name,
        description=description,
        params_json_schema=schema or {"type": "object", "properties": {}},
        on_invoke_tool=_on_invoke_tool,
    )


def _collect_agent_tools() -> List[FunctionTool]:
    tools: List[FunctionTool] = []
    for spec in list_tool_specs():
        tools.append(_make_agent_tool(spec.name, spec.input_schema or {}, spec.description or spec.name))
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
                "You are a conversational AI assistant. Based on the user's message and current plan, "
                "decide your next action. You can either:\n"
                "1. Respond directly to the user with a helpful message (assistant_message)\n"
                "2. Call a tool to perform an action (tool_call)\n"
                "3. Revise the current plan (revise_plan)\n"
                "4. Spawn a subagent for complex tasks (spawn_subagent)\n\n"
                "For assistant_message: Provide a natural, conversational response to the user.\n"
                "For tool_call: Use the available tools and return JSON with tool details.\n"
                "For other actions: Return the appropriate JSON structure.\n\n"
                "Available tools: echo.echo, calculator.calculate, web-search.web_search\n"
                "Use proper tool names with server prefixes (e.g., 'web-search.web_search')\n"
                "If you need to call a tool, return a JSON object with 'tool_call' and 'parameters' fields.\n"
                "The tool will be executed immediately and results will be provided in the next response."
            ),
            tools=_collect_agent_tools(),
        )

        # Run the agent via the SDK Runner; pass state_view as a JSON string input
        import json as _json
        run_result = await Runner.run(agent, _json.dumps(state_view))

        # Look for our sentinel in tool call outputs produced by function tools
        for item in run_result.new_items:
            if getattr(item, "type", "") == "tool_call_output_item":
                out = getattr(item, "output", None)
                if isinstance(out, dict) and "_tool_request" in out:
                    tr = out["_tool_request"]
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

        # Check for tool calls in final output (enhanced detection)
        content = str(getattr(run_result, "final_output", ""))

        # Import handler here to avoid circular imports
        from .tool_response_handler import tool_response_handler

        tool_call = tool_response_handler.detect_tool_call(content)

        if tool_call:
            # Execute tool immediately
            call_id = f"tc-{info.activity_id}"
            result = await tool_response_handler.execute_tool_call(
                call_id, tool_call["name"], tool_call["args"]
            )

            # Return formatted result to agent
            formatted_result = tool_response_handler.format_result_for_agent(result)

            return {
                "type": "assistant_message",
                "message": {
                    "role": "assistant",
                    "content": formatted_result,
                    "ts": 0
                }
            }

        # Try to parse JSON output to extract the actual message
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict) and "message" in parsed:
                # Agent returned JSON with nested message
                if isinstance(parsed["message"], str):
                    content = parsed["message"]
                elif isinstance(parsed["message"], dict) and "content" in parsed["message"]:
                    content = parsed["message"]["content"]
        except (json.JSONDecodeError, KeyError, TypeError):
            # If JSON parsing fails, use the content as-is
            pass

        return {
            "type": "assistant_message",
            "message": {"role": "assistant", "content": content, "ts": 0},
        }
