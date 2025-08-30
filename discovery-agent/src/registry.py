from __future__ import annotations
from typing import Callable, Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ToolSpec(BaseModel):
    name: str
    fn: Callable[[dict], Any]
    description: Optional[str] = None
    schema: Optional[Dict[str, Any]] = Field(default=None, description="JSON Schema for args")

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, name: str, fn: Callable[[dict], Any], *, description: str | None = None, schema: Dict[str, Any] | None = None):
        self._tools[name] = ToolSpec(name=name, fn=fn, description=description, schema=schema)

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

# MCP hook (stub)
class MCPClient:
    def execute(self, name: str, args: dict):
        raise NotImplementedError("MCP client not wired yet")

mcp = MCPClient()

def execute_tool(name: str, args: dict):
    if registry.has(name):
        return registry.execute(name, args)
    return mcp.execute(name, args)

# Helper for decision_agents to expose schemas to the Agent

def list_tool_specs() -> List[ToolSpec]:
    return registry.specs()
