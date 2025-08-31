"""
Tool Dispatch Activity - Clean implementation based on temporal-ai-agents reference
"""

import json
from typing import Any, Dict, List, Optional, Sequence

from temporalio import activity
from temporalio.common import RetryPolicy

from src.models import ToolCall, ToolResult, StructuredToolResult
from src.mcp.core.client import mcp_client_manager
from src.mcp.core.config import config_loader


class ToolNotFoundError(Exception):
    """Raised when a requested tool is not found"""
    pass


class ToolExecutionError(Exception):
    """Raised when tool execution fails"""
    pass


@activity.defn
async def tool_dispatch(call: ToolCall) -> StructuredToolResult:
    """Execute a tool call using MCP or other mechanisms"""
    ai = activity.info()
    activity.logger.info(f"Starting tool dispatch for: {call.name} with args: {call.args}")

    import time
    start_time = time.time()

    try:
        # Check if this is an MCP tool (server.tool format)
        if "." in call.name:
            result = await execute_mcp_tool(call.name, call.args)
        else:
            # For now, non-MCP tools are not supported in this clean implementation
            raise ToolNotFoundError(f"Tool '{call.name}' is not an MCP tool")

        execution_time = time.time() - start_time
        activity.logger.info(f"Tool {call.name} executed successfully")

        return StructuredToolResult(
            tool_name=call.name,
            success=True,
            data=result,
            execution_time=execution_time
        )

    except ToolNotFoundError as e:
        execution_time = time.time() - start_time
        activity.logger.error(f"Tool not found: {call.name}")
        return StructuredToolResult(
            tool_name=call.name,
            success=False,
            error=f"Tool '{call.name}' not found. Available MCP servers: {list(config_loader.get_servers().keys())}",
            execution_time=execution_time
        )

    except ToolExecutionError as e:
        execution_time = time.time() - start_time
        activity.logger.error(f"Tool execution error for {call.name}: {str(e)}")
        return StructuredToolResult(
            tool_name=call.name,
            success=False,
            error=f"Tool execution failed: {str(e)}",
            execution_time=execution_time
        )

    except Exception as e:
        execution_time = time.time() - start_time
        activity.logger.error(f"Unexpected error in tool dispatch for {call.name}: {str(e)}")
        return StructuredToolResult(
            tool_name=call.name,
            success=False,
            error=f"Unexpected error: {str(e)}",
            execution_time=execution_time
        )


async def execute_mcp_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute an MCP tool with proper session management"""
    if "." not in tool_name:
        raise ToolNotFoundError(f"Invalid MCP tool name format: {tool_name}")

    server_name, actual_tool_name = tool_name.split(".", 1)

    # Get server config
    server_config = config_loader.get_expanded_server_config(server_name)
    if not server_config:
        raise ToolNotFoundError(f"MCP server '{server_name}' not configured")

    # Add server name to config for client manager
    server_config_with_name = server_config.copy()
    server_config_with_name["name"] = server_name

    try:
        # Get client and execute tool
        client_config = await mcp_client_manager.get_client(server_config_with_name)

        # Execute the tool using proper MCP session
        result = await _execute_tool_with_session(server_config_with_name, actual_tool_name, args)

        return result

    except Exception as e:
        error_msg = str(e).lower()
        activity.logger.error(f"MCP tool execution error for {tool_name}: {str(e)}")

        # Provide helpful fallback suggestions based on tool name
        if "search" in tool_name.lower():
            return {
                "tool": tool_name,
                "success": False,
                "error": f"Search tool '{tool_name}' failed. Check server configuration.",
                "suggestion": f"Verify MCP server '{server_name}' is running and accessible"
            }
        else:
            raise ToolExecutionError(f"Tool '{tool_name}' execution failed: {str(e)}")


async def _execute_tool_with_session(
    server_config: Dict[str, Any],
    tool_name: str,
    args: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute tool using proper MCP session management"""
    connection = _build_connection(server_config)

    if connection["type"] == "stdio":
        async with mcp_client_manager._stdio_connection(
            command=connection.get("command", "python"),
            args=connection.get("args", ["server.py"]),
            env=connection.get("env", {}),
        ) as (read, write):
            from mcp import ClientSession

            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()

                # Convert argument types for MCP tools
                converted_args = _convert_args_types(args)

                # Call the tool
                result = await session.call_tool(tool_name, arguments=converted_args)

                # Normalize the result
                normalized_result = _normalize_result(result)

                return {
                    "tool": tool_name,
                    "success": True,
                    "content": normalized_result,
                }

    else:
        raise ToolExecutionError(f"Unsupported connection type: {connection['type']}")


def _build_connection(server_definition: Dict[str, Any]) -> Dict[str, Any]:
    """Build connection parameters from server definition"""
    return {
        "type": server_definition.get("type", "stdio"),
        "command": server_definition.get("command", "python"),
        "args": server_definition.get("args", ["server.py"]),
        "env": server_definition.get("env", {}) or {},
    }


def _normalize_result(result: Any) -> Any:
    """Normalize MCP tool result for serialization"""
    if hasattr(result, "content"):
        # Handle MCP result objects
        content = result.content
        if hasattr(content, "__iter__") and not isinstance(content, str):
            try:
                # Convert to list if it's iterable
                content_list = list(content)
                return [
                    item.text if hasattr(item, "text") else str(item)
                    for item in content_list
                ]
            except (TypeError, AttributeError):
                # If conversion fails, return as string
                return str(content)
        return str(content)
    return result


def _convert_args_types(tool_args: Dict[str, Any]) -> Dict[str, Any]:
    """Convert string arguments to appropriate types for MCP tools"""
    converted_args = {}

    for key, value in tool_args.items():
        if isinstance(value, str):
            # Try to convert string values to appropriate types
            if value.isdigit():
                # Convert numeric strings to integers
                converted_args[key] = int(value)
            elif value.replace(".", "").isdigit() and value.count(".") == 1:
                # Convert decimal strings to floats
                converted_args[key] = float(value)
            elif value.lower() in ("true", "false"):
                # Convert boolean strings
                converted_args[key] = value.lower() == "true"
            else:
                # Keep as string
                converted_args[key] = value
        else:
            # Keep non-string values as-is
            converted_args[key] = value

    return converted_args


@activity.defn
async def discover_mcp_tools() -> Dict[str, Any]:
    """Activity to discover tools from all configured MCP servers"""
    try:
        # Get all server configs
        server_configs = config_loader.get_all_expanded_configs()

        all_tools = {}
        total_servers = 0
        total_tools = 0

        for server_config in server_configs:
            server_name = server_config["name"]
            activity.logger.info(f"Discovering tools from MCP server: {server_name}")

            # Discover tools from this server
            result = await mcp_client_manager.discover_tools(server_config)

            if result.get("success"):
                all_tools[server_name] = result.get("tools", {})
                total_servers += 1
                total_tools += result.get("total_available", 0)
                activity.logger.info(f"Found {result.get('total_available', 0)} tools from {server_name}")
            else:
                activity.logger.warning(f"Failed to discover tools from {server_name}: {result.get('error')}")

        return {
            "success": True,
            "tools": all_tools,
            "server_count": total_servers,
            "total_tools": total_tools
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
