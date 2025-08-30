from __future__ import annotations
from temporalio import activity
from src.models import ToolCall, ToolResult
from src.registry import execute_tool
from src.otel import get_tracer

tracer = get_tracer(__name__)

@activity.defn
async def tool_dispatch(call: ToolCall) -> ToolResult:
    ai = activity.info()
    with tracer.start_as_current_span("tool_dispatch") as span:
        span.set_attribute("temporal.workflow_id", ai.workflow_id)
        span.set_attribute("temporal.run_id", ai.workflow_run_id)
        span.set_attribute("temporal.attempt", ai.attempt)
        span.set_attribute("tool.name", call.name)
        try:
            # All tools are now MCP-based and executed asynchronously
            output = await execute_tool(call.name, call.args)

            return ToolResult(id=call.id, ok=True, output=output)
        except Exception as e:
            span.record_exception(e)
            return ToolResult(id=call.id, ok=False, error=str(e))
