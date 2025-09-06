from __future__ import annotations
from typing import Dict, Any, List, Optional
from src.models import ToolSpec
from src.mcp.core.client import tool_orchestrator
from src.mcp.core.config import config_loader

class ToolRegistry:
    """Pure MCP-based tool registry - no static tool registration"""

    def __init__(self):
        self._tool_cache: Dict[str, ToolSpec] = {}

    def has(self, name: str) -> bool:
        """Check if a tool is available"""
        return name in self._get_all_tools()

    def execute(self, name: str, args: dict):
        """Execute a tool - this method is deprecated, use execute_tool_async instead"""
        raise DeprecationWarning("Use execute_tool_async for async execution")

    def specs(self) -> List[ToolSpec]:
        """Get all available tool specs"""
        return list(self._get_all_tools().values())

    def _get_all_tools(self) -> Dict[str, ToolSpec]:
        """Get all available tools from MCP servers"""
        # Update cache if needed
        self._update_tool_cache()
        return self._tool_cache

    def _update_tool_cache(self):
        """Update the tool cache from MCP servers"""
        import asyncio

        # This is a simplified version - in production you'd want proper async handling
        try:
            # Get tools from all configured MCP servers
            all_tools = {}

            # Add tools from MCP servers
            for server_name, tools in tool_orchestrator.tool_cache.items():
                for tool in tools:
                    tool_name = f"{server_name}.{tool['name']}"
                    # Convert MCP tool to ToolSpec format
                    tool_spec = ToolSpec(
                        name=tool_name,
                        description=tool.get('description', ''),
                        input_schema=tool.get('input_schema', {})
                    )
                    all_tools[tool_name] = tool_spec

            self._tool_cache = all_tools
        except Exception as e:
            # If there's an error, keep the existing cache
            print(f"Warning: Could not update tool cache: {e}")
            pass

    def refresh_tools(self):
        """Force refresh of tool cache"""
        import asyncio
        # This would trigger rediscovery of tools from MCP servers
        # For now, just clear the cache so it gets refreshed on next access
        self._tool_cache.clear()

registry = ToolRegistry()

async def execute_tool(name: str, args: dict):
    """Execute a tool using the orchestrator (handles MCP tools only)"""
    return await tool_orchestrator.execute_tool(name, args)

# Helper for deep_agent to expose schemas to the Agent
def list_tool_specs() -> List[ToolSpec]:
    """Get all available tool specs from MCP servers"""
    return registry.specs()

# MCP server configuration from mcp-config.json
def configure_mcp_servers():
    """Configure MCP servers from mcp-config.json"""
    try:
        # Validate config
        issues = config_loader.validate_config()
        if issues:
            print("MCP Configuration Issues:")
            for issue in issues:
                print(f"  - {issue}")

        # Load servers from config
        configs = config_loader.get_all_expanded_configs()

        for config in configs:
            server_name = config["name"]
            tool_orchestrator.add_mcp_server(server_name, config)
            print(f"Configured MCP server: {server_name} ({config.get('type', 'streamable-http')})")
    except Exception as e:
        print(f"Warning: Could not configure MCP servers: {e}")

# Initialize MCP servers on import
configure_mcp_servers()
