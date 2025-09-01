#!/usr/bin/env python3
"""
Echo MCP Server - Simple echo tool for testing MCP functionality
"""

import asyncio
import sys
import os
import json
from typing import Dict, List, Any

# Add the parent directory to the path so we can import base_server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
    MCP_AVAILABLE = True
except ImportError:
    print("MCP package not found. Please install with: pip install mcp")
    MCP_AVAILABLE = False


def check_mcp_availability():
    """Check if MCP is available at runtime"""
    # For now, assume MCP is available since we know it's installed
    return True


class EchoServer:
    """MCP Server for echo functionality"""

    def __init__(self, server_name: str = "echo-server", version: str = "1.0.0"):
        if not check_mcp_availability():
            raise ImportError("MCP package is required for MCP servers")

        self.server_name = server_name
        self.version = version
        self.server = Server(server_name, version)
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup the MCP handlers"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="echo",
                    description="Echo back the provided text",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Text to echo back"}
                        },
                        "required": ["text"]
                    }
                ),
                Tool(
                    name="reverse_echo",
                    description="Echo back the provided text in reverse",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Text to reverse and echo back"}
                        },
                        "required": ["text"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any] = None) -> List[TextContent]:
            """Handle tool calls"""
            try:
                if name == "echo":
                    if arguments and "text" in arguments:
                        text = str(arguments["text"])
                        return [TextContent(type="text", text=json.dumps({
                            "tool": "echo.echo",
                            "success": True,
                            "content": {"text": text}
                        }))]
                    return [TextContent(type="text", text=json.dumps({
                        "tool": "echo.echo",
                        "success": False,
                        "error": "No text provided"
                    }))]

                elif name == "reverse_echo":
                    if arguments and "text" in arguments:
                        text = str(arguments["text"])
                        return [TextContent(type="text", text=json.dumps({
                            "tool": "echo.reverse_echo",
                            "success": True,
                            "content": {"text": text[::-1]}
                        }))]
                    return [TextContent(type="text", text=json.dumps({
                        "tool": "echo.reverse_echo",
                        "success": False,
                        "error": "No text provided"
                    }))]

                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]

            except Exception as e:
                return [TextContent(type="text", text=f"Tool error: {str(e)}")]

    async def run_stdio(self):
        """Run the MCP server using stdio transport"""
        try:
            print(f"Starting MCP server: {self.server_name} v{self.version}")
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        except Exception as e:
            print(f"Error running MCP server {self.server_name}: {e}")
            raise

    def run(self):
        """Entry point for running the server"""
        asyncio.run(self.run_stdio())


def main():
    """Main entry point for the echo server"""
    server = EchoServer()
    server.run()


if __name__ == "__main__":
    main()
