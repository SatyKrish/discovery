#!/usr/bin/env python3
"""
Base MCP Server implementation for discovery-agent tools.
Provides common functionality for all MCP servers in the tools directory.
"""

import asyncio
import sys
import json
import logging
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from mcp import Tool
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, PromptMessage
    MCP_AVAILABLE = True
except ImportError:
    logger.error("MCP package not found. Please install with: pip install mcp")
    MCP_AVAILABLE = False
    # Define dummy classes for type hints
    class Tool:
        def __init__(self, *args, **kwargs): pass
        def __call__(self, *args, **kwargs): pass

    class Server:
        def __init__(self, *args, **kwargs): pass
        def tool(self, *args, **kwargs): pass
        def run(self, *args, **kwargs): pass
        def create_initialization_options(self, *args, **kwargs): pass

    class stdio_server:
        def __init__(self, *args, **kwargs): pass
        def __aenter__(self): return self
        def __aexit__(self, *args, **kwargs): pass


class BaseMCPServer(ABC):
    """Base class for MCP servers in discovery-agent"""

    def __init__(self, server_name: str, version: str = "1.0.0"):
        if not MCP_AVAILABLE:
            raise ImportError("MCP package is required for MCP servers")

        self.server_name = server_name
        self.version = version
        self.server = Server(server_name, version)
        self.tools = {}
        self._setup_tools()

    @abstractmethod
    def _setup_tools(self):
        """Setup the tools for this MCP server. Must be implemented by subclasses."""
        pass

    def add_tool(self, name: str, handler, description: str = "", input_schema: Dict[str, Any] = None):
        """Add a tool to the server"""
        self.tools[name] = {
            "handler": handler,
            "description": description,
            "input_schema": input_schema or {}
        }

        # Register the tool with the MCP server using the correct API
        @self.server.call_tool()
        async def tool_call(name=name, arguments=None):
            if name in self.tools:
                handler = self.tools[name]["handler"]
                if asyncio.iscoroutinefunction(handler):
                    return await handler(arguments or {})
                else:
                    return handler(arguments or {})
            else:
                raise ValueError(f"Unknown tool: {name}")

        # Store the tool definition for list_tools
        self._tool_definitions = getattr(self, '_tool_definitions', [])
        self._tool_definitions.append({
            "name": name,
            "description": description,
            "inputSchema": input_schema or {}
        })

    @abstractmethod
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools - must be implemented by subclasses"""
        pass

    def _create_text_content(self, text: str) -> List[Dict[str, Any]]:
        """Helper to create MCP text content response"""
        return [TextContent(type="text", text=text)]

    async def run_stdio(self):
        """Run the MCP server using stdio transport"""
        try:
            logger.info(f"Starting MCP server: {self.server_name} v{self.version}")
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        except Exception as e:
            logger.error(f"Error running MCP server {self.server_name}: {e}")
            raise

    def run(self):
        """Entry point for running the server"""
        asyncio.run(self.run_stdio())


def create_tool_decorator(server: Server):
    """Create a tool decorator that works with the MCP server"""
    def tool(name: Optional[str] = None, description: str = ""):
        def decorator(func):
            tool_name = name or func.__name__

            # Create the MCP tool
            mcp_tool = Tool(
                name=tool_name,
                description=description or func.__doc__ or f"Tool: {tool_name}",
                inputSchema={
                    "type": "object",
                    "properties": getattr(func, "_input_schema", {}),
                    "required": getattr(func, "_required_params", [])
                }
            )

            # Register the tool with the server
            @server.tool()
            async def tool_wrapper(**kwargs):
                try:
                    result = await func(**kwargs) if asyncio.iscoroutinefunction(func) else func(**kwargs)
                    return result
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}")
                    raise

            return func
        return decorator
    return tool


def tool_parameter(name: str, type: str = "string", description: str = "", required: bool = True):
    """Decorator to define tool parameters"""
    def decorator(func):
        if not hasattr(func, "_input_schema"):
            func._input_schema = {}
            func._required_params = []

        func._input_schema[name] = {
            "type": type,
            "description": description
        }

        if required:
            func._required_params.append(name)

        return func
    return decorator
