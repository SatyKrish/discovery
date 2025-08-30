from __future__ import annotations
import asyncio
import json
import time
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


class MCPManager:
    """Manages multiple MCP server connections"""

    def __init__(self):
        self.servers: Dict[str, MCPClient] = {}
        self.server_health: Dict[str, Dict[str, Any]] = {}

    def add_server(self, name: str, config: Dict[str, Any]):
        """Add an MCP server configuration"""
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
