from __future__ import annotations
from temporalio import activity
from opentelemetry import trace
from agents import Agent, FunctionTool
from agents.run import Runner
from typing import Callable, Dict, Any, List
import json
from src.registry import list_tool_specs
from src.tool_chain_orchestrator import tool_chain_builder, tool_chain_executor, reflection_engine
from src.hierarchical_agents import agent_coordinator, strategy_manager

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

        # Get the current user message from state_view
        messages = state_view.get("messages", [])
        current_user_message = None

        # Find the most recent user message
        for msg in reversed(messages):
            if msg.get("role") == "user":
                current_user_message = msg.get("content", "")
                break

        if not current_user_message:
            # Fallback if no user message found
            current_user_message = "Please continue the conversation."

        # Get last response ID for multi-turn conversation
        last_response_id = state_view.get("last_response_id", "")

        # Collect tools for the agent
        tools = await _collect_agent_tools()

        # Convert tools to OpenAI Responses API format
        openai_tools = []
        for tool in tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.schema or {"type": "object", "properties": {}}
                }
            })

        # Use OpenAI Responses API with multi-turn state management
        from src.llm import _provider

        provider = _provider()
        if last_response_id:
            provider.last_response_id = last_response_id

        # Create system message for agent instructions
        system_message = (
            "You are a helpful conversational AI assistant.\n\n"

            "IMPORTANT: Always respond to the user's MOST RECENT message first.\n\n"

            "CONVERSATION:\n"
            "- Focus on answering the current user message\n"
            "- Use conversation history for context when relevant\n"
            "- Keep responses natural and conversational\n\n"

            "TOOLS:\n"
            "- Use tools when you need specific information\n"
            "- Explain briefly what you're doing\n\n"

            "RESPONSES:\n"
            "- Answer the current user message directly\n"
            "- Be helpful and friendly\n"
            "- Stay focused on the immediate request"
        )

        try:
            # Create response using OpenAI Responses API
            response = provider.create_response(
                user_message=current_user_message,
                model="gpt-4",  # Use appropriate model
                tools=openai_tools if openai_tools else None,
                system_message=system_message
            )

            # Check for tool calls in the response
            if hasattr(response, 'tool_calls') and response.tool_calls:
                # Handle tool calls
                tool_call = response.tool_calls[0]  # Take first tool call
                return {
                    "type": "tool_call",
                    "call": {
                        "id": f"tc-{info.activity_id}",
                        "name": tool_call.function.name,
                        "args": json.loads(tool_call.function.arguments),
                        "requires_approval": False,
                    },
                    "message": None,
                    "subagent_spec": None,
                    "plan_diff": None,
                }

            # Extract the response text
            content = getattr(response, "output_text", "")
            if not content and hasattr(response, 'content'):
                # Fallback for different response formats
                content = str(response.content)

            return {
                "type": "assistant_message",
                "message": {"role": "assistant", "content": content, "ts": 0},
                "last_response_id": provider.get_last_response_id(),
            }

        except Exception as e:
            # Fallback to simple response if API fails
            return {
                "type": "assistant_message",
                "message": {"role": "assistant", "content": f"I apologize, but I encountered an error: {str(e)}", "ts": 0},
            }
