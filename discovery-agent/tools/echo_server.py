#!/usr/bin/env python3
"""
Echo MCP Server - Simple echo tool for testing MCP functionality
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import base_server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_server import BaseMCPServer

class EchoServer(BaseMCPServer):
    """MCP Server for echo functionality"""

    def __init__(self):
        super().__init__("echo-server", "1.0.0")

    def _setup_tools(self):
        """Setup the echo tool"""

        @self.server.call_tool()
        async def echo(name: str, arguments: dict = None) -> str:
            """Echo back the provided text."""
            if arguments and "text" in arguments:
                text = arguments["text"]
                return f"Echo: {text}"
            return "Echo: (no text provided)"

        @self.server.call_tool()
        async def reverse_echo(name: str, arguments: dict = None) -> str:
            """Echo back the provided text in reverse."""
            if arguments and "text" in arguments:
                text = arguments["text"]
                return f"Reversed Echo: {text[::-1]}"
            return "Reversed Echo: (no text provided)"

        @self.server.list_tools()
        async def list_tools() -> list:
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
                },
                {
                    "name": "reverse_echo",
                    "description": "Echo back the provided text in reverse",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Text to reverse and echo back"}
                        },
                        "required": ["text"]
                    }
                }
            ]


def main():
    """Main entry point for the echo server"""
    server = EchoServer()
    server.run()


if __name__ == "__main__":
    main()
