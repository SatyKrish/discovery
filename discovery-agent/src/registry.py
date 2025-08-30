from __future__ import annotations
from typing import Callable, Dict, Any, List, Optional
from pydantic import BaseModel, Field
from src.mcp_client import tool_orchestrator

class ToolSpec(BaseModel):
    name: str
    fn: Callable[[dict], Any]
    description: Optional[str] = None
    schema: Optional[Dict[str, Any]] = Field(default=None, description="JSON Schema for args")

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, name: str, fn: Callable[[dict], Any], *, description: str | None = None, schema: Dict[str, Any] | None = None):
        tool_spec = ToolSpec(name=name, fn=fn, description=description, schema=schema)
        self._tools[name] = tool_spec
        # Also register with the orchestrator
        tool_orchestrator.register_static_tool(name, tool_spec)

    def has(self, name: str) -> bool:
        return name in self._tools

    def execute(self, name: str, args: dict):
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name].fn(args)

    def specs(self) -> List[ToolSpec]:
        return list(self._tools.values())

registry = ToolRegistry()

# Example native tool: echo
registry.register(
    "echo",
    lambda args: {"echo": args.get("text")},
    description="Echo back the provided text.",
    schema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Text to echo back"}
        },
        "required": ["text"],
        "additionalProperties": False,
    },
)

# Add a web search tool example
registry.register(
    "web_search",
    lambda args: {"results": f"Mock search results for: {args.get('query', '')}"},
    description="Search the web for information.",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"],
        "additionalProperties": False,
    },
)

# Add a calculator tool
registry.register(
    "calculate",
    lambda args: {"result": eval(args.get("expression", "0"))},
    description="Calculate mathematical expressions.",
    schema={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Mathematical expression to evaluate"}
        },
        "required": ["expression"],
        "additionalProperties": False,
    },
)

async def execute_tool(name: str, args: dict):
    """Execute a tool using the orchestrator (handles both static and dynamic tools)"""
    return await tool_orchestrator.execute_tool(name, args)

# Helper for decision_agents to expose schemas to the Agent
def list_tool_specs() -> List[ToolSpec]:
    """Get all available tool specs (static + dynamic)"""
    return list(tool_orchestrator.get_all_available_tools().values())

# MCP server configuration examples
def configure_mcp_servers():
    """Configure MCP servers for dynamic tool discovery"""
    # Example: GitHub tools server
    tool_orchestrator.add_mcp_server("github", {
        "name": "GitHub Tools",
        "url": "http://localhost:3001",  # Example MCP server URL
        "capabilities": ["repository", "issues", "pull_requests"],
        "timeout": 30.0
    })

    # Example: Database tools server
    tool_orchestrator.add_mcp_server("database", {
        "name": "Database Tools",
        "url": "http://localhost:3002",
        "capabilities": ["query", "analytics", "export"],
        "timeout": 30.0
    })

# Initialize MCP servers on import
configure_mcp_servers()
