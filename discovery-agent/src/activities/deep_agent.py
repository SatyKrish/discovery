# ──────────────────────────────────────────────────────────────────────────────
# File: src/activities/deep_agent.py
# Optimized deep agent with fast responses and dynamic tool integration
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from temporalio import activity
from opentelemetry import trace
from agents import Agent, FunctionTool, Model, ModelProvider, OpenAIChatCompletionsModel, RunConfig
from agents.run import Runner
from typing import Callable, Dict, Any, List
import json
import time
from src.registry import list_tool_specs
from src.config import settings
from openai import AsyncOpenAI

# Custom Azure OpenAI provider
client = AsyncOpenAI(
    base_url=settings.openai_base_url,
    api_key=settings.openai_api_key,
)

class CustomModelProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(
            model=model_name or settings.openai_model,
            openai_client=client
        )

CUSTOM_MODEL_PROVIDER = CustomModelProvider()

tracer = trace.get_tracer(__name__)

# Global cache for expensive operations
_cached_agent = None
_cached_tools = None
_cache_timestamp = None
CACHE_DURATION = 300  # 5 minutes

def _build_dynamic_instructions(available_tools: List[dict]) -> str:
    """Build instructions dynamically based on available tools"""

    # Format available tools for the prompt
    tool_list = []
    for tool in available_tools:
        if isinstance(tool, dict) and 'name' in tool:
            tool_list.append(tool['name'])
        elif hasattr(tool, 'name'):
            tool_list.append(tool.name)

    tools_str = ", ".join(tool_list) if tool_list else "echo.echo, calculator.calculate, web-search.web_search"

    return f"""
You are a DeepAgent, a conversational AI assistant with access to tools and sub-agents.

Your role is to decide when to respond directly, when to call a tool, and when to spawn sub-agents. 
Keep interactions fast, helpful, and predictable.

**FAST RESPONSES (no reasoning or tool calls needed):**
- Greetings (hi, hello, hey) → Respond warmly and ask how to help.
- Small talk (how are you, what's your name, are you there) → Short, friendly answer.
- Thanks / closing (thanks, bye) → Polite acknowledgement and offer further help.
- Status checks (ready?, working?) → Confirm you are available and ready.

**SIMPLE CLARIFICATIONS:**
- If the user asks what you can do, summarize briefly: 
  "I can chat, answer simple questions, and for complex tasks I can plan and use tools."

**COMPLEX TASKS (invoke agent loop):**
- Use tools only when external data, search, or computation is required.
- Spawn sub-agents only for multi-step workflows (e.g., planning a trip, validating data, generating a report).
- If input is ambiguous, ask 1 short clarifying question before proceeding.

**GUIDELINES:**
- Default to a direct conversational reply unless external action is explicitly needed.
- Keep trivial responses ≤ 2 sentences.
- For tool use, always output a JSON object:
  {{ "tool_call": {{ "tool": "<tool_name>", "parameters": {{ ... }} }} }}
- For sub-agent workflows, describe the sub-agent spec in JSON.
- Always be friendly, efficient, and safe.
""".strip()

def _get_cached_agent():
    """Get cached agent and tools with automatic refresh"""
    global _cached_agent, _cached_tools, _cache_timestamp

    now = time.time()
    if (_cached_agent is None or
        _cache_timestamp is None or
        (now - _cache_timestamp) > CACHE_DURATION):

        # Get fresh tool specs
        tool_specs = list_tool_specs()
        _cached_tools = _collect_agent_tools()

        # Build dynamic instructions
        instructions = _build_dynamic_instructions(tool_specs)

        # Create agent with optimized instructions
        _cached_agent = Agent(
            name="orchestrator",
            instructions=instructions,
            tools=_cached_tools
        )
        _cache_timestamp = now

    return _cached_agent, _cached_tools

# Build agent-visible tool shims with per-tool JSON schemas
def _make_agent_tool(name: str, schema: Dict[str, Any], description: str) -> FunctionTool:
    async def _on_invoke_tool(ctx, input: str):
        try:
            args = json.loads(input) if input else {}
        except Exception:
            args = {}
        # Provide a sentinel that deep_agent_activity will convert to a ToolCall action
        return {"_tool_request": {"name": name, "args": args}}

    return FunctionTool(
        name=name,
        description=description,
        params_json_schema=schema or {"type": "object", "properties": {}},
        on_invoke_tool=_on_invoke_tool,
    )

def _collect_agent_tools() -> List[FunctionTool]:
    """Collect tools from registry"""
    tools: List[FunctionTool] = []
    for spec in list_tool_specs():
        tools.append(_make_agent_tool(spec.name, spec.input_schema or {}, spec.description or spec.name))
    return tools

def _detect_json_tool_call(content: str) -> Dict[str, Any] | None:
    """Detect tool calls in JSON format from agent output"""
    try:
        parsed = json.loads(content.strip())
    except json.JSONDecodeError:
        return None

    # Format 1: Direct tool call structure
    if isinstance(parsed, dict) and "tool_call" in parsed:
        tc = parsed["tool_call"]
        if isinstance(tc, dict):
            # Handle nested tool structure
            if "tool" in tc and "parameters" in tc:
                tool_name = tc["tool"]
                # Ensure proper server prefix
                if "." not in tool_name:
                    tool_name = _infer_server_prefix(tool_name)
                return {
                    "name": tool_name,
                    "args": tc["parameters"]
                }
            # Handle direct tool name
            elif "tool_name" in tc and "parameters" in tc:
                tool_name = tc["tool_name"]
                if "." not in tool_name:
                    tool_name = _infer_server_prefix(tool_name)
                return {
                    "name": tool_name,
                    "args": tc["parameters"]
                }

    # Format 2: Simple tool call with parameters
    if isinstance(parsed, dict) and "tool" in parsed and "parameters" in parsed:
        tool_name = parsed["tool"]
        if "." not in tool_name:
            tool_name = _infer_server_prefix(tool_name)
        return {
            "name": tool_name,
            "args": parsed["parameters"]
        }

    return None

def _infer_server_prefix(tool_name: str) -> str:
    """Infer MCP server prefix based on tool name"""
    tool_mappings = {
        "weather": "weather",
        "weather_api": "weather",
        "get_current_weather": "weather",
        "find_flights": "flights",
        "flight": "flights",
        "search": "web-search",
        "calculate": "calculator",
        "echo": "echo"
    }

    for keyword, server in tool_mappings.items():
        if keyword in tool_name.lower():
            return f"{server}.{tool_name}"

    return f"web-search.{tool_name}"  # Default fallback

@activity.defn
async def deep_agent_activity(state_view: dict) -> dict:
    """Optimized deep agent activity with fast responses and caching"""
    info = activity.info()

    with tracer.start_as_current_span("deep_agent_activity") as span:
        span.set_attribute("temporal.workflow_id", info.workflow_id)
        span.set_attribute("temporal.run_id", info.workflow_run_id)
        span.set_attribute("temporal.attempt", info.attempt)

        # Use cached agent and tools for performance
        agent, tools = _get_cached_agent()

        # Run agent decision with optimized settings
        run_result = await Runner.run(
            agent,
            json.dumps(state_view),
            run_config=RunConfig(
                model_provider=CUSTOM_MODEL_PROVIDER
            ),
        )

        # Check for tool calls in function outputs (fastest path)
        for item in run_result.new_items:
            if getattr(item, "type", "") == "tool_call_output_item":
                out = getattr(item, "output", None)
                if isinstance(out, dict) and "_tool_request" in out:
                    tr = out["_tool_request"]
                    return {
                        "type": "tool_call",
                        "call": {
                            "id": f"tc-{info.activity_id}",
                            "name": tr.get("name"),
                            "args": tr.get("args", {}),
                            "requires_approval": False,
                        },
                        "message": None,
                        "subagent_spec": None,
                        "plan_diff": None,
                    }

        # Check for tool calls in final output
        content = str(getattr(run_result, "final_output", ""))
        tool_call = _detect_json_tool_call(content)

        if tool_call:
            return {
                "type": "tool_call",
                "call": {
                    "id": f"tc-{info.activity_id}",
                    "name": tool_call["name"],
                    "args": tool_call["args"],
                    "requires_approval": False,
                },
                "message": None,
                "subagent_spec": None,
                "plan_diff": None,
            }

        # Extract message content
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict) and "message" in parsed:
                if isinstance(parsed["message"], str):
                    content = parsed["message"]
                elif isinstance(parsed["message"], dict) and "content" in parsed["message"]:
                    content = parsed["message"]["content"]
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

        return {
            "type": "assistant_message",
            "message": {"role": "assistant", "content": content, "ts": 0},
        }
