from __future__ import annotations
from temporalio import activity
from src.models import ToolCall, ToolResult
from src.mcp_client import MCPClientManager
from src.mcp_config import config_loader
from src.otel import get_tracer
from typing import Dict, Any

tracer = get_tracer(__name__)

class ToolNotFoundError(Exception):
    """Raised when a requested tool is not found"""
    pass

class ToolExecutionError(Exception):
    """Raised when tool execution fails"""
    pass

# Global MCP client manager instance
mcp_client_manager = MCPClientManager()

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
            # Execute tool using MCP client manager
            output = await execute_tool_with_mcp(call.name, call.args)

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

async def execute_tool_with_mcp(tool_name: str, args: Dict[str, Any]) -> Any:
    """Execute tool using MCP client manager"""
    try:
        # Check if it's an MCP tool (server.tool format)
        if "." in tool_name:
            server_name, actual_tool_name = tool_name.split(".", 1)

            # Get server config
            server_config = config_loader.get_server_config(server_name)
            if not server_config:
                raise ToolNotFoundError(f"MCP server '{server_name}' not configured")

            # Add server name to config for client manager
            server_config_with_name = server_config.copy()
            server_config_with_name["name"] = server_name

            # Get client and execute tool
            client = await mcp_client_manager.get_client(server_config_with_name)
            async with client:
                result = await client.execute_tool(actual_tool_name, args)
                return result
        else:
            # Handle non-MCP tools (fallback for backward compatibility)
            raise ToolNotFoundError(f"Tool '{tool_name}' is not an MCP tool")

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

@activity.defn
async def discover_mcp_tools() -> Dict[str, Any]:
    """Activity to discover tools from all configured MCP servers"""
    try:
        # Load all server configs
        server_configs = config_loader.get_all_expanded_configs()

        # Add servers to client manager
        for config in server_configs:
            mcp_client_manager.add_server(config["name"], config)

        # Discover tools from all servers
        tools = await mcp_client_manager.discover_all_tools()

        return {
            "success": True,
            "tools": tools,
            "server_count": len(tools),
            "total_tools": sum(len(server_tools) for server_tools in tools.values())
        }

    except Exception as e:
        activity.logger.error(f"Error discovering MCP tools: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "tools": {},
            "server_count": 0,
            "total_tools": 0
        }
