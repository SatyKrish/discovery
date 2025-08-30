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

        @self.server.tool()
        async def echo(text: str) -> str:
            """Echo back the provided text.

            Args:
                text: The text to echo back

            Returns:
                The echoed text
            """
            return f"Echo: {text}"

        @self.server.tool()
        async def reverse_echo(text: str) -> str:
            """Echo back the provided text in reverse.

            Args:
                text: The text to reverse and echo back

            Returns:
                The reversed echoed text
            """
            return f"Reversed Echo: {text[::-1]}"


def main():
    """Main entry point for the echo server"""
    server = EchoServer()
    server.run()


if __name__ == "__main__":
    main()
