"""
MCP Client Manager - Clean implementation based on temporal-ai-agents reference
"""

import os
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

# Import MCP client libraries (New API)
try:
    from mcp.client.stdio import stdio_client
    from mcp.types import TextContent
except ImportError:
    # Fallback if MCP not installed
    stdio_client = None
    TextContent = None


class MCPClientManager:
    """Manages MCP server connections with pooling"""

    def __init__(self):
        self.clients: Dict[str, Any] = {}
        self.server_health: Dict[str, Dict[str, Any]] = {}

    def add_server(self, name: str, config: Dict[str, Any]):
        """Add an MCP server configuration"""
        self.clients[name] = config
        self.server_health[name] = {
            "status": "unknown",
            "last_check": 0,
            "tool_count": 0
        }

    async def get_client(self, server_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Get a client configuration for the server"""
        server_name = server_definition.get("name", "unknown")
        if server_name not in self.clients:
            self.add_server(server_name, server_definition)
        return self.clients[server_name]

    async def execute_tool(self, server_config: Dict[str, Any], tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool on a specific MCP server"""
        server_name = server_config.get("name", "unknown")

        try:
            connection = self._build_connection(server_config)

            if connection["type"] == "stdio":
                async with self._stdio_connection(
                    command=connection.get("command", "python"),
                    args=connection.get("args", ["server.py"]),
                    env=connection.get("env", {}),
                ) as (read, write):
                    # Use the new MCP client session API
                    from mcp import ClientSession
                    async with ClientSession(read, write) as session:
                        # Initialize the session
                        await session.initialize()

                        # Call the tool
                        result = await session.call_tool(tool_name, arguments=args)

                        # Process result
                        if hasattr(result, "content"):
                            content = []
                            if hasattr(result.content, "__iter__") and not isinstance(result.content, str):
                                for item in result.content:
                                    if hasattr(item, "text"):
                                        content.append(item.text)
                                    else:
                                        content.append(str(item))
                            else:
                                content.append(str(result.content))

                            return {
                                "tool": tool_name,
                                "success": True,
                                "content": content,
                            }
                        else:
                            return {
                                "tool": tool_name,
                                "success": True,
                                "content": [str(result)],
                            }

        except Exception as e:
            return {
                "tool": tool_name,
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
            }

    async def discover_tools(self, server_config: Dict[str, Any]) -> Dict[str, Any]:
        """Discover tools from a specific MCP server"""
        server_name = server_config.get("name", "unknown")

        try:
            connection = self._build_connection(server_config)

            if connection["type"] == "stdio":
                async with self._stdio_connection(
                    command=connection.get("command", "python"),
                    args=connection.get("args", ["server.py"]),
                    env=connection.get("env", {}),
                ) as (read, write):
                    # Use the new MCP client session API
                    from mcp import ClientSession
                    async with ClientSession(read, write) as session:
                        # Initialize the session
                        await session.initialize()

                        # List available tools
                        tools_response = await session.list_tools()

                        # Process tools
                        tools_info = {}
                        for tool in tools_response.tools:
                            tools_info[tool.name] = {
                                "name": tool.name,
                                "description": tool.description,
                                "inputSchema": tool.inputSchema,
                            }

                        # Update health
                        self.server_health[server_name] = {
                            "status": "healthy",
                            "last_check": __import__("time").time(),
                            "tool_count": len(tools_info),
                        }

                        return {
                            "server_name": server_name,
                            "success": True,
                            "tools": tools_info,
                            "total_available": len(tools_response.tools),
                        }

        except Exception as e:
            # Update health on error
            self.server_health[server_name] = {
                "status": "error",
                "last_check": __import__("time").time(),
                "tool_count": 0,
                "error": str(e),
            }

            return {
                "server_name": server_name,
                "success": False,
                "error": str(e),
                "tools": {},
                "total_available": 0,
            }

    def _build_connection(self, server_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Build connection parameters from server definition"""
        return {
            "type": server_definition.get("type", "stdio"),
            "command": server_definition.get("command", "python"),
            "args": server_definition.get("args", ["server.py"]),
            "env": server_definition.get("env", {}) or {},
        }

    @asynccontextmanager
    async def _stdio_connection(self, command: str, args: list, env: dict):
        """Create stdio connection to MCP server"""
        if stdio_client is None:
            raise Exception("MCP client libraries not available")

        # Prepare environment variables
        full_env = os.environ.copy()
        full_env.update(env)

        # Create server parameters using new API
        from mcp.client.stdio import StdioServerParameters
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=full_env
        )

        async with stdio_client(server_params) as (read, write):
            yield read, write


# Global instance
mcp_client_manager = MCPClientManager()


class ToolOrchestrator:
    """Tool orchestrator that provides the interface expected by the registry"""

    def __init__(self):
        self.tool_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.server_configs: Dict[str, Dict[str, Any]] = {}

    def add_mcp_server(self, name: str, config: Dict[str, Any]):
        """Add an MCP server configuration"""
        self.server_configs[name] = config
        mcp_client_manager.add_server(name, config)

    async def execute_tool(self, name: str, args: dict):
        """Execute a tool by name"""
        # Parse server and tool name (format: "server.tool")
        if "." not in name:
            raise ValueError(f"Invalid tool name format: {name}. Expected 'server.tool'")

        server_name, tool_name = name.split(".", 1)

        if server_name not in self.server_configs:
            raise ValueError(f"Unknown server: {server_name}")

        # Get server config and execute tool
        server_config = self.server_configs[server_name]

        # Use the MCP client manager to execute
        result = await mcp_client_manager.execute_tool(server_config, tool_name, args)
        return result

    async def discover_tools(self, server_name: str):
        """Discover tools for a specific server"""
        if server_name not in self.server_configs:
            raise ValueError(f"Unknown server: {server_name}")

        server_config = self.server_configs[server_name]
        result = await mcp_client_manager.discover_tools(server_config)

        if result.get("success"):
            # Cache the tools
            self.tool_cache[server_name] = list(result.get("tools", {}).values())

        return result

    async def discover_all_tools(self):
        """Discover tools from all configured servers"""
        for server_name in self.server_configs:
            await self.discover_tools(server_name)


# Global tool orchestrator instance
tool_orchestrator = ToolOrchestrator()
