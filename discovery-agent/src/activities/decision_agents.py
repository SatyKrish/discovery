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


async def _collect_agent_tools() -> List[FunctionTool]:
    """Collect all available tools (static + dynamic) for the agent"""
    tools: List[FunctionTool] = []

    # Get all available tool specs
    tool_specs = list_tool_specs()

    for spec in tool_specs:
        tools.append(_make_agent_tool(spec.name, spec.schema or {}, spec.description or spec.name))

    return tools

@activity.defn
async def decision_agents_activity(state_view: dict) -> dict:
    info = activity.info()
    with tracer.start_as_current_span("decision_agents_activity") as span:
        span.set_attribute("temporal.workflow_id", info.workflow_id)
        span.set_attribute("temporal.run_id", info.workflow_run_id)
        span.set_attribute("temporal.attempt", info.attempt)

        # Collect tools synchronously for the agent
        tools = await _collect_agent_tools()

        agent = Agent(
            name="conversational_deep_agent",
            instructions=(
                "You are a helpful, conversational AI assistant engaged in a multi-turn dialogue. "
                "Your goal is to have natural conversations while helping users accomplish their objectives.\n\n"

                "CONVERSATION STYLE:\n"
                "- Acknowledge user messages naturally (e.g., 'Got it', 'I understand', 'That makes sense')\n"
                "- Ask clarifying questions when needed\n"
                "- Provide contextually relevant information\n"
                "- Maintain conversational flow while working toward goals\n\n"

                "HIERARCHICAL PLANNING:\n"
                "- Work through the plan systematically, focusing on one sub-goal at a time\n"
                "- Explain what you're working on and why\n"
                "- Update progress as you complete tasks\n"
                "- Be flexible - adapt the plan based on user feedback\n"
                "- Consider dependencies between tasks\n\n"

                "AVAILABLE ACTIONS:\n"
                "1. assistant_message: Respond conversationally to user input\n"
                "2. tool_call: Use tools to gather information or perform tasks\n"
                "3. revise_plan: Update the current plan based on new information\n"
                "4. spawn_subagent: Delegate complex tasks to specialized agents\n\n"

                "RESPONSE GUIDELINES:\n"
                "- For assistant_message: Write natural, engaging responses that acknowledge the user's input\n"
                "- For tool_call: Use tools when you need specific information or to perform actions\n"
                "- Consider conversation history and user preferences\n"
                "- Balance being helpful with being conversational\n"
                "- Explain your planning and progress clearly\n\n"

                "CONTEXT AWARENESS:\n"
                "- Review the conversation history to understand the user's intent\n"
                "- Remember user preferences and previous interactions\n"
                "- Adapt your communication style to the user's responses\n"
                "- Use the current plan as a flexible guide, not a rigid script\n"
                "- Track progress and celebrate completed tasks\n\n"

                "TOOL USAGE:\n"
                "- Only call tools when necessary for the conversation\n"
                "- Explain why you're using a tool if it might not be obvious\n"
                "- Use both default tools and any MCP server tools available\n"
                "- Consider tool capabilities when planning tasks\n\n"

                "PROGRESS TRACKING:\n"
                "- Keep the user informed about what you're working on\n"
                "- Mark tasks as completed when finished\n"
                "- Ask for feedback on completed work\n"
                "- Suggest next steps clearly"
            ),
            tools=tools,
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

        # Otherwise, treat the final output as an assistant message
        content = str(getattr(run_result, "final_output", ""))

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
