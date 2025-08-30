from __future__ import annotations
import asyncio
import json
import time
import os
import subprocess
import signal
from typing import Dict, List, Any, Optional
import httpx
from src.models import MCPServer, ToolOrchestrator, ToolSpec
from src.config import settings


class MCPClient:
    """Client for connecting to MCP (Model Context Protocol) servers"""

    def __init__(self, server_config: Dict[str, Any]):
        self.name = server_config.get("name", "unknown")
        self.url = server_config.get("url", "")
        self.capabilities = server_config.get("capabilities", [])
        self.timeout = server_config.get("timeout", 30.0)
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def connect(self) -> bool:
        """Test connection to MCP server"""
        if not self._client:
            return False

        try:
            response = await self._client.get(f"{self.url}/health")
            return response.status_code == 200
        except Exception:
            return False

    async def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools from MCP server"""
        if not self._client:
            return []

        try:
            response = await self._client.get(f"{self.url}/tools")
            if response.status_code == 200:
                data = response.json()
                return data.get("tools", [])
            return []
        except Exception:
            return []

    async def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool on the MCP server"""
        if not self._client:
            raise Exception("MCP client not connected")

        try:
            payload = {
                "tool": tool_name,
                "arguments": args
            }
            response = await self._client.post(
                f"{self.url}/execute",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"MCP server error: {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to execute tool {tool_name}: {str(e)}")


class StdioMCPClient:
    """Client for stdio-based MCP servers"""

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
        """Discover available tools from stdio MCP server"""
        if not self._running or not self._process:
            return []

        try:
            # For now, return mock tools based on server name
            # In a real implementation, this would communicate with the MCP server
            # to discover available tools via the MCP protocol
            if self.name == "echo":
                return [
                    {
                        "name": "echo",
                        "description": "Echo back the provided text",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string", "description": "Text to echo back"}
                            },
                            "required": ["text"]
                        }
                    },
                    {
                        "name": "reverse_echo",
                        "description": "Echo back the provided text in reverse",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string", "description": "Text to reverse and echo back"}
                            },
                            "required": ["text"]
                        }
                    }
                ]
            elif self.name == "calculator":
                return [
                    {
                        "name": "calculate",
                        "description": "Calculate mathematical expressions safely",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "expression": {"type": "string", "description": "Mathematical expression to evaluate"}
                            },
                            "required": ["expression"]
                        }
                    },
                    {
                        "name": "add",
                        "description": "Add two numbers",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "a": {"type": "number", "description": "First number"},
                                "b": {"type": "number", "description": "Second number"}
                            },
                            "required": ["a", "b"]
                        }
                    }
                ]
            elif self.name == "web-search":
                return [
                    {
                        "name": "web_search",
                        "description": "Search the web for information",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"},
                                "max_results": {"type": "integer", "description": "Maximum number of results", "default": 5}
                            },
                            "required": ["query"]
                        }
                    }
                ]
            return []
        except Exception:
            return []

    async def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool on the stdio MCP server"""
        if not self._running or not self._process:
            raise Exception("MCP server not running")

        try:
            # For now, simulate tool execution based on server name and tool name
            # In a real implementation, this would communicate with the MCP server
            # via stdin/stdout using the MCP protocol

            if self.name == "echo":
                if tool_name == "echo":
                    text = args.get("text", "")
                    return {"result": f"Echo: {text}"}
                elif tool_name == "reverse_echo":
                    text = args.get("text", "")
                    return {"result": f"Reversed Echo: {text[::-1]}"}

            elif self.name == "calculator":
                if tool_name == "calculate":
                    expression = args.get("expression", "")
                    # Safe evaluation (simplified for demo)
                    if "+" in expression or "-" in expression or "*" in expression or "/" in expression:
                        result = eval(expression, {"__builtins__": {}})
                        return {"result": result}
                    else:
                        return {"result": "Invalid expression"}
                elif tool_name == "add":
                    a = args.get("a", 0)
                    b = args.get("b", 0)
                    return {"result": a + b}

            elif self.name == "web-search":
                if tool_name == "web_search":
                    query = args.get("query", "")
                    max_results = args.get("max_results", 5)
                    return {
                        "query": query,
                        "total_results": min(3, max_results),
                        "results": [
                            {"title": f"Result 1 for {query}", "url": f"https://example.com/1"},
                            {"title": f"Result 2 for {query}", "url": f"https://example.com/2"},
                            {"title": f"Result 3 for {query}", "url": f"https://example.com/3"}
                        ][:max_results]
                    }

            raise Exception(f"Unknown tool: {tool_name}")

        except Exception as e:
            raise Exception(f"Failed to execute tool {tool_name}: {str(e)}")


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
        async with client:
            return await client.execute_tool(tool_name, args)


class ToolOrchestratorService:
    """Orchestrates tool discovery and execution across static and dynamic tools"""

    def __init__(self):
        self.static_tools: Dict[str, ToolSpec] = {}
        self.mcp_manager = MCPManager()
        self.tool_cache: Dict[str, Dict[str, Any]] = {}
        self.usage_stats: Dict[str, Dict[str, Any]] = {}

    def register_static_tool(self, name: str, tool_spec: ToolSpec):
        """Register a static tool"""
        self.static_tools[name] = tool_spec

    def add_mcp_server(self, name: str, config: Dict[str, Any]):
        """Add an MCP server"""
        self.mcp_manager.add_server(name, config)

    async def discover_dynamic_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """Discover tools from MCP servers"""
        return await self.mcp_manager.discover_all_tools()

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

    def get_tool_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get usage statistics for all tools"""
        return self.usage_stats.copy()


# Global instance
tool_orchestrator = ToolOrchestratorService()
