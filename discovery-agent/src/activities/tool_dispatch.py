from __future__ import annotations
from temporalio import activity
from src.models import ToolCall, ToolResult
from src.registry import execute_tool
from src.otel import get_tracer

tracer = get_tracer(__name__)

class ToolNotFoundError(Exception):
    """Raised when a requested tool is not found"""
    pass

class ToolExecutionError(Exception):
    """Raised when tool execution fails"""
    pass

@activity.defn
async def tool_dispatch(call: ToolCall) -> ToolResult:
    ai = activity.info()
    with tracer.start_as_current_span("tool_dispatch") as span:
        span.set_attribute("temporal.workflow_id", ai.workflow_id)
        span.set_attribute("temporal.run_id", ai.workflow_run_id)
        span.set_attribute("temporal.attempt", ai.attempt)
        span.set_attribute("tool.name", call.name)

        activity.logger.info(f"Starting tool dispatch for: {call.name} with args: {call.args}")

        try:
            # Enhanced tool execution with better error handling
            output = await execute_tool_with_fallback(call.name, call.args)

            activity.logger.info(f"Tool {call.name} executed successfully, output type: {type(output)}")
            if isinstance(output, dict):
                activity.logger.debug(f"Tool output keys: {list(output.keys())}")

            return ToolResult(id=call.id, ok=True, output=output)

        except ToolNotFoundError as e:
            activity.logger.error(f"Tool not found: {call.name}")
            span.record_exception(e)
            return ToolResult(
                id=call.id,
                ok=False,
                error=f"Tool '{call.name}' not found. Available tools: echo, calculator, web-search"
            )

        except ToolExecutionError as e:
            activity.logger.error(f"Tool execution error for {call.name}: {str(e)}")
            span.record_exception(e)
            return ToolResult(id=call.id, ok=False, error=f"Tool execution failed: {str(e)}")

        except Exception as e:
            activity.logger.error(f"Unexpected error in tool dispatch for {call.name}: {str(e)}")
            span.record_exception(e)
            return ToolResult(id=call.id, ok=False, error=f"Unexpected error: {str(e)}")

async def execute_tool_with_fallback(tool_name: str, args: dict) -> any:
    """Execute tool with fallback logic for better error handling"""
    try:
        from src.registry import execute_tool
        return await execute_tool(tool_name, args)

    except Exception as e:
        error_msg = str(e).lower()

        # Check for specific error types and provide helpful fallbacks
        if "not found" in error_msg or "unknown tool" in error_msg:
            raise ToolNotFoundError(f"Tool '{tool_name}' is not available")

        # Provide helpful fallback suggestions based on tool name
        if "weather" in tool_name.lower():
            return {
                "error": "Weather tool not available. Try using web-search for weather information.",
                "suggestion": "Use web-search.web_search with query like 'weather in New York City'"
            }
        elif "flight" in tool_name.lower() or "find_flights" in tool_name.lower():
            return {
                "error": "Flight search tool not available. Try using web-search for flight information.",
                "suggestion": "Use web-search.web_search with query like 'flights from Paris to NYC'"
            }
        elif "search" in tool_name.lower():
            # For search-related tools, suggest using web-search
            return {
                "error": f"Search tool '{tool_name}' failed. Try using web-search.web_search instead.",
                "suggestion": f"Use web-search.web_search with your search query"
            }
        else:
            # Generic fallback
            raise ToolExecutionError(f"Tool '{tool_name}' execution failed: {str(e)}")
