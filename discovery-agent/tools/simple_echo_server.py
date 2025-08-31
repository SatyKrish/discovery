#!/usr/bin/env python3
"""
Simple Echo MCP Server - Minimal working example
"""

import asyncio
from typing import Dict, List, Any

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent
    MCP_AVAILABLE = True
except ImportError:
    print("MCP package not found. Please install with: pip install mcp")
    MCP_AVAILABLE = False


def main():
    """Main entry point for the simple echo server"""
    if not MCP_AVAILABLE:
        print("MCP package not found. Please install with: pip install mcp")
        return

    server = Server("simple-echo-server", "1.0.0")

    @server.call_tool()
    async def echo(arguments: Dict[str, Any] = None) -> List[TextContent]:
        """Echo back the provided text."""
        if arguments and "text" in arguments:
            text = arguments["text"]
            return [TextContent(type="text", text=f"Echo: {text}")]
        return [TextContent(type="text", text="Echo: (no text provided)")]

    @server.list_tools()
    async def list_tools() -> List[Dict[str, Any]]:
        """List available tools"""
        return [
            {
                "name": "echo",
                "description": "Echo back the provided text",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to echo back"}
                    },
                    "required": ["text"]
                }
            }
        ]

    async def run_server():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run_server())


if __name__ == "__main__":
    main()
