from __future__ import annotations
import asyncio
import json
import time
import os
import subprocess
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

# Import MCP client libraries
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    # Fallback if MCP not installed
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None
    MCP_AVAILABLE = False


class MCPClientManager:
    """Manages MCP server connections with pooling"""

    def __init__(self):
        self.clients: Dict[str, 'StdioMCPClient'] = {}
        self.server_health: Dict[str, Dict[str, Any]] = {}

    def add_server(self, name: str, config: Dict[str, Any]):
        """Add an MCP server configuration"""
        self.clients[name] = StdioMCPClient(config)
        self.server_health[name] = {
            "status": "unknown",
            "last_check": 0,
            "tool_count": 0
        }

    async def get_client(self, server_definition: Dict[str, Any]) -> 'StdioMCPClient':
        """Get a pooled client for the server"""
        server_name = server_definition.get("name", "unknown")
        if server_name not in self.clients:
            self.add_server(server_name, server_definition)
        return self.clients[server_name]

    async def discover_all_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """Discover tools from all connected MCP servers"""
        all_tools = {}

        for server_name, client in self.clients.items():
            try:
                tools = await client.discover_tools()
                if tools:
                    all_tools[server_name] = tools
                    self.server_health[server_name] = {
                        "status": "healthy",
                        "last_check": time.time(),
                        "tool_count": len(tools)
                    }
                else:
                    self.server_health[server_name] = {
                        "status": "unhealthy",
                        "last_check": time.time(),
                        "tool_count": 0,
                        "error": "No tools discovered"
                    }
            except Exception as e:
                self.server_health[server_name] = {
                    "status": "error",
                    "last_check": time.time(),
                    "tool_count": 0,
                    "error": str(e)
                }

        return all_tools

    def get_health_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get health metrics for all servers"""
        return self.server_health.copy()


class StdioMCPClient:
    """Client for stdio-based MCP servers with connection pooling"""

    def __init__(self, server_config: Dict[str, Any]):
        self.name = server_config.get("name", "unknown")
        self.command = server_config.get("command", "")
        self.args = server_config.get("args", [])
        self.env = server_config.get("env", {})
        self.timeout = server_config.get("timeout", 30.0)
        self._process: Optional[subprocess.Popen] = None
        self._running = False

    async def __aenter__(self):
        await self.start_server()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop_server()

    async def start_server(self):
        """Start the stdio MCP server process"""
        if self._running:
            return

        try:
            # Prepare environment variables
            env = os.environ.copy()
            env.update(self.env)

            # Start the process
            self._process = subprocess.Popen(
                [self.command] + self.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
                bufsize=1
            )

            self._running = True
            # Give the server a moment to start
            await asyncio.sleep(0.1)

        except Exception as e:
            raise Exception(f"Failed to start MCP server {self.name}: {str(e)}")

    async def stop_server(self):
        """Stop the stdio MCP server process"""
        if self._process and self._running:
            try:
                self._process.terminate()
                try:
                    self._process.wait(timeout=5.0)
                except subprocess.TimeoutExpired:
                    self._process.kill()
                    self._process.wait()
            except Exception:
                pass  # Best effort cleanup
            finally:
                self._running = False
                self._process = None

    async def connect(self) -> bool:
        """Test connection to stdio MCP server"""
        return self._running and self._process and self._process.poll() is None

    async def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools from stdio MCP server using proper MCP protocol"""
        if not MCP_AVAILABLE:
            print(f"MCP library not available for server {self.name}")
            return []

        if not self._running or not self._process:
            return []

        try:
            # Use MCP stdio client to communicate with the server
            async with stdio_client(
                StdioServerParameters(
                    command=self.command,
                    args=self.args,
                    env={**os.environ, **self.env}
                )
            ) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    # Initialize the MCP session
                    await session.initialize()

                    # List available tools
                    tools_response = await session.list_tools()
                    tools = []

                    for tool in tools_response.tools:
                        tool_info = {
                            "name": tool.name,
                            "description": tool.description,
                            "inputSchema": tool.inputSchema
                        }
                        tools.append(tool_info)

                    return tools

        except Exception as e:
            print(f"Error discovering tools from {self.name}: {e}")
            return []

    async def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool on the stdio MCP server using proper MCP protocol"""
        if not MCP_AVAILABLE:
            raise Exception(f"MCP library not available for server {self.name}")

        if not self._running or not self._process:
            raise Exception("MCP server not running")

        try:
            # Use MCP stdio client to communicate with the server
            async with stdio_client(
                StdioServerParameters(
                    command=self.command,
                    args=self.args,
                    env={**os.environ, **self.env}
                )
            ) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    # Initialize the MCP session
                    await session.initialize()

                    # Call the tool
                    result = await session.call_tool(tool_name, arguments=args)

                    # Convert the result to a dictionary format
                    if hasattr(result, 'content'):
                        # Handle MCP result format
                        content = []
                        for item in result.content:
                            if hasattr(item, 'text'):
                                content.append({"type": "text", "text": item.text})
                            elif hasattr(item, 'data'):
                                content.append({"type": "data", "data": item.data})

                        return {
                            "tool": tool_name,
                            "success": True,
                            "content": content
                        }
                    else:
                        # Fallback for other result formats
                        return {
                            "tool": tool_name,
                            "success": True,
                            "result": str(result)
                        }

        except Exception as e:
            error_msg = f"Failed to execute tool {tool_name}: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)


class MCPManager:
    """Manages multiple MCP server connections"""

    def __init__(self):
        self.servers: Dict[str, Any] = {}  # Can be MCPClient or StdioMCPClient
        self.server_health: Dict[str, Dict[str, Any]] = {}

    def add_server(self, name: str, config: Dict[str, Any]):
        """Add an MCP server configuration"""
        server_type = config.get("type", "streamable-http")

        if server_type == "stdio":
            self.servers[name] = StdioMCPClient(config)
        else:
            # Default to HTTP-based client for backward compatibility
            self.servers[name] = MCPClient(config)

    async def discover_all_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """Discover tools from all connected MCP servers"""
        all_tools = {}

        for server_name, client in self.servers.items():
            try:
                async with client:
                    if await client.connect():
                        tools = await client.discover_tools()
                        if tools:
                            all_tools[server_name] = tools
                        self.server_health[server_name] = {
                            "status": "healthy",
                            "last_check": time.time(),
                            "tool_count": len(tools)
                        }
                    else:
                        self.server_health[server_name] = {
                            "status": "unhealthy",
                            "last_check": time.time(),
                            "error": "Connection failed"
                        }
            except Exception as e:
                self.server_health[server_name] = {
                    "status": "error",
                    "last_check": time.time(),
                    "error": str(e)
                }

        return all_tools

    async def execute_remote_tool(self, server_name: str, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool on a specific MCP server"""
        if server_name not in self.servers:
            raise Exception(f"Unknown MCP server: {server_name}")

        client = self.servers[server_name]

        # Update health metrics before execution
        if server_name in self.server_health:
            self.server_health[server_name]["last_tool_execution"] = time.time()
            self.server_health[server_name]["total_tool_calls"] = self.server_health[server_name].get("total_tool_calls", 0) + 1

        try:
            async with client:
                result = await client.execute_tool(tool_name, args)

            # Update success metrics
            if server_name in self.server_health:
                self.server_health[server_name]["successful_tool_calls"] = self.server_health[server_name].get("successful_tool_calls", 0) + 1
                self.server_health[server_name]["last_success"] = time.time()
                self.server_health[server_name]["status"] = "healthy"

            return result

        except Exception as e:
            # Update failure metrics
            if server_name in self.server_health:
                self.server_health[server_name]["failed_tool_calls"] = self.server_health[server_name].get("failed_tool_calls", 0) + 1
                self.server_health[server_name]["last_failure"] = time.time()
                self.server_health[server_name]["last_error"] = str(e)
                self.server_health[server_name]["status"] = "error"

            raise e

    def get_health_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get comprehensive health metrics for all servers"""
        current_time = time.time()
        metrics = {}

        for server_name, health_info in self.server_health.items():
            last_check = health_info.get("last_check", 0)
            time_since_check = current_time - last_check

            # Calculate uptime percentage (simplified)
            total_calls = health_info.get("total_tool_calls", 0)
            successful_calls = health_info.get("successful_tool_calls", 0)

            success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0

            metrics[server_name] = {
                **health_info,
                "time_since_last_check": time_since_check,
                "success_rate": success_rate,
                "is_stale": time_since_check > 300,  # Consider stale after 5 minutes
            }

        return metrics

    def get_overall_health_status(self) -> Dict[str, Any]:
        """Get overall health status across all servers"""
        if not self.server_health:
            return {"status": "unknown", "message": "No servers configured"}

        metrics = self.get_health_metrics()
        healthy_servers = sum(1 for m in metrics.values() if m.get("status") == "healthy")
        total_servers = len(metrics)

        if healthy_servers == total_servers:
            status = "healthy"
            message = f"All {total_servers} servers are healthy"
        elif healthy_servers > 0:
            status = "degraded"
            message = f"{healthy_servers}/{total_servers} servers are healthy"
        else:
            status = "unhealthy"
            message = f"All {total_servers} servers are unhealthy"

        return {
            "status": status,
            "message": message,
            "healthy_servers": healthy_servers,
            "total_servers": total_servers,
            "server_details": metrics
        }


class ToolOrchestratorService:
    """Orchestrates tool discovery and execution across static and dynamic tools"""

    def __init__(self, cache_ttl_seconds: int = 300):  # 5 minutes default TTL
        self.static_tools: Dict[str, ToolSpec] = {}
        self.mcp_manager = MCPManager()
        self.tool_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, float] = {}
        self.cache_ttl_seconds = cache_ttl_seconds
        self.usage_stats: Dict[str, Dict[str, Any]] = {}

    def register_static_tool(self, name: str, tool_spec: ToolSpec):
        """Register a static tool"""
        self.static_tools[name] = tool_spec

    def add_mcp_server(self, name: str, config: Dict[str, Any]):
        """Add an MCP server"""
        self.mcp_manager.add_server(name, config)

    async def discover_dynamic_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """Discover tools from MCP servers with caching"""
        current_time = time.time()

        # Check if cache is still valid
        if self._is_cache_valid(current_time):
            print(f"Using cached tool discovery results (age: {current_time - self.cache_timestamps.get('tools', 0):.1f}s)")
            return self.tool_cache

        # Cache is stale or empty, refresh it
        print("Refreshing tool discovery cache...")
        try:
            tools = await self.mcp_manager.discover_all_tools()
            self.tool_cache = tools
            self.cache_timestamps['tools'] = current_time
            print(f"Cached {sum(len(server_tools) for server_tools in tools.values())} tools from {len(tools)} servers")
            return tools
        except Exception as e:
            print(f"Error refreshing tool cache: {e}")
            # Return cached data if available, even if stale
            if self.tool_cache:
                print("Returning stale cache due to refresh error")
                return self.tool_cache
            raise

    def get_all_available_tools(self) -> Dict[str, ToolSpec]:
        """Get all available tools (static + dynamic)"""
        all_tools = self.static_tools.copy()

        # Add dynamic tools from cache
        for server_name, tools in self.tool_cache.items():
            for tool in tools:
                tool_name = f"{server_name}.{tool['name']}"
                # Convert MCP tool to ToolSpec format
                tool_spec = ToolSpec(
                    name=tool_name,
                    description=tool.get('description', ''),
                    schema=tool.get('schema', {})
                )
                all_tools[tool_name] = tool_spec

        return all_tools

    def find_tools_for_task(self, task_description: str, required_capabilities: List[str] = None) -> List[str]:
        """Find suitable tools for a given task"""
        suitable_tools = []

        # Check static tools
        for name, tool_spec in self.static_tools.items():
            if self._tool_matches_task(tool_spec, task_description, required_capabilities):
                suitable_tools.append(name)

        # Check dynamic tools
        for server_name, tools in self.tool_cache.items():
            for tool in tools:
                if self._dynamic_tool_matches_task(tool, task_description, required_capabilities):
                    suitable_tools.append(f"{server_name}.{tool['name']}")

        return suitable_tools

    def _tool_matches_task(self, tool_spec: ToolSpec, task: str, capabilities: List[str] = None) -> bool:
        """Check if a static tool matches the task requirements"""
        # Simple matching based on description and tool hints
        task_lower = task.lower()
        desc_lower = (tool_spec.description or "").lower()

        # Check for keyword matches
        keywords = ["search", "find", "lookup", "query", "calculate", "compute", "analyze"]
        if any(keyword in task_lower and keyword in desc_lower for keyword in keywords):
            return True

        return False

    def _dynamic_tool_matches_task(self, tool: Dict[str, Any], task: str, capabilities: List[str] = None) -> bool:
        """Check if a dynamic tool matches the task requirements"""
        task_lower = task.lower()
        desc_lower = tool.get('description', '').lower()

        # Check for keyword matches
        keywords = ["search", "find", "lookup", "query", "calculate", "compute", "analyze"]
        if any(keyword in task_lower and keyword in desc_lower for keyword in keywords):
            return True

        return False

    async def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Execute a tool (static or dynamic)"""
        # Track usage
        if tool_name not in self.usage_stats:
            self.usage_stats[tool_name] = {"calls": 0, "successes": 0, "failures": 0}
        self.usage_stats[tool_name]["calls"] += 1

        try:
            # Check if it's a static tool
            if tool_name in self.static_tools:
                result = self.static_tools[tool_name].fn(args)
                self.usage_stats[tool_name]["successes"] += 1
                return result

            # Check if it's a dynamic tool
            if "." in tool_name:
                server_name, actual_tool_name = tool_name.split(".", 1)
                result = await self.mcp_manager.execute_remote_tool(server_name, actual_tool_name, args)
                self.usage_stats[tool_name]["successes"] += 1
                return result

            raise Exception(f"Unknown tool: {tool_name}")

        except Exception as e:
            self.usage_stats[tool_name]["failures"] += 1
            raise e

    def _is_cache_valid(self, current_time: float) -> bool:
        """Check if the tool cache is still valid"""
        cache_timestamp = self.cache_timestamps.get('tools')
        if cache_timestamp is None:
            return False  # No cache available

        age_seconds = current_time - cache_timestamp
        return age_seconds < self.cache_ttl_seconds

    def clear_cache(self):
        """Clear the tool cache"""
        self.tool_cache.clear()
        self.cache_timestamps.clear()
        print("Tool cache cleared")

    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the current cache state"""
        current_time = time.time()
        cache_timestamp = self.cache_timestamps.get('tools')

        if cache_timestamp is None:
            return {
                "cache_status": "empty",
                "cached_servers": 0,
                "total_cached_tools": 0,
                "cache_age_seconds": None,
                "cache_ttl_seconds": self.cache_ttl_seconds
            }

        age_seconds = current_time - cache_timestamp
        total_tools = sum(len(tools) for tools in self.tool_cache.values())

        return {
            "cache_status": "valid" if self._is_cache_valid(current_time) else "stale",
            "cached_servers": len(self.tool_cache),
            "total_cached_tools": total_tools,
            "cache_age_seconds": age_seconds,
            "cache_ttl_seconds": self.cache_ttl_seconds,
            "time_until_expiry": max(0, self.cache_ttl_seconds - age_seconds)
        }

    def get_server_health(self) -> Dict[str, Dict[str, Any]]:
        """Get health status of all MCP servers"""
        return self.mcp_manager.server_health.copy()

    def get_tool_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get usage statistics for all tools"""
        return self.usage_stats.copy()


# Global instance
tool_orchestrator = ToolOrchestratorService()
