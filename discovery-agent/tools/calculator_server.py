#!/usr/bin/env python3
"""
Calculator MCP Server - Safe mathematical calculations
"""

import asyncio
import sys
import os
import re
import json
from typing import List, Dict, Any, Union

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent
    MCP_AVAILABLE = True
except ImportError:
    print("MCP package not found. Please install with: pip install mcp")
    MCP_AVAILABLE = False


class CalculatorServer:
    """MCP Server for calculator functionality"""

    def __init__(self, server_name: str = "calculator-server", version: str = "1.0.0"):
        if not MCP_AVAILABLE:
            raise ImportError("MCP package is required for MCP servers")

        self.server_name = server_name
        self.version = version
        self.server = Server(server_name, version)
        self._setup_tools()

    def _setup_tools(self):
        """Setup the calculator tools"""

        @self.server.call_tool()
        async def calculate(arguments: Dict[str, Any] = None) -> List[TextContent]:
            """Calculate mathematical expressions safely."""
            if arguments and "expression" in arguments:
                expression = arguments["expression"]
                try:
                    # Use safe evaluation
                    result = self._safe_eval_math(expression)
                    return [TextContent(type="text", text=json.dumps({"result": result}))]
                except Exception as e:
                    return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
            return [TextContent(type="text", text=json.dumps({"error": "No expression provided"}))]

        @self.server.call_tool()
        async def add(arguments: Dict[str, Any] = None) -> List[TextContent]:
            """Add two numbers."""
            if arguments and "a" in arguments and "b" in arguments:
                result = arguments["a"] + arguments["b"]
                return [TextContent(type="text", text=json.dumps({"result": result}))]
            return [TextContent(type="text", text=json.dumps({"error": "Missing arguments 'a' and/or 'b'"}))]

        @self.server.call_tool()
        async def subtract(arguments: Dict[str, Any] = None) -> List[TextContent]:
            """Subtract second number from first."""
            if arguments and "a" in arguments and "b" in arguments:
                result = arguments["a"] - arguments["b"]
                return [TextContent(type="text", text=json.dumps({"result": result}))]
            return [TextContent(type="text", text=json.dumps({"error": "Missing arguments 'a' and/or 'b'"}))]

        @self.server.call_tool()
        async def multiply(arguments: Dict[str, Any] = None) -> List[TextContent]:
            """Multiply two numbers."""
            if arguments and "a" in arguments and "b" in arguments:
                result = arguments["a"] * arguments["b"]
                return [TextContent(type="text", text=json.dumps({"result": result}))]
            return [TextContent(type="text", text=json.dumps({"error": "Missing arguments 'a' and/or 'b'"}))]

        @self.server.call_tool()
        async def divide(arguments: Dict[str, Any] = None) -> List[TextContent]:
            """Divide first number by second."""
            if arguments and "a" in arguments and "b" in arguments:
                if arguments["b"] == 0:
                    return [TextContent(type="text", text=json.dumps({"error": "Division by zero"}))]
                result = arguments["a"] / arguments["b"]
                return [TextContent(type="text", text=json.dumps({"result": result}))]
            return [TextContent(type="text", text=json.dumps({"error": "Missing arguments 'a' and/or 'b'"}))]

        @self.server.list_tools()
        async def list_tools() -> List[Dict[str, Any]]:
            """List available tools"""
            return [
                {
                    "name": "calculate",
                    "description": "Calculate mathematical expressions safely",
                    "inputSchema": {
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
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "subtract",
                    "description": "Subtract second number from first",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "multiply",
                    "description": "Multiply two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "divide",
                    "description": "Divide first number by second",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    }
                }
            ]

    def _safe_eval_math(self, expression: str) -> Union[float, int]:
        """Safely evaluate mathematical expressions"""
        # Remove any dangerous characters/functions
        if not re.match(r'^[0-9+\-*/().\s^pieE]+$', expression):
            raise ValueError("Invalid characters in expression")

        # Replace common math constants
        expression = expression.replace('pi', '3.141592653589793')
        expression = expression.replace('e', '2.718281828459045')

        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')

        # Use eval with restricted globals
        allowed_names = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
        }

        try:
            result = eval(expression, allowed_names)
            return result
        except Exception as e:
            raise ValueError(f"Invalid mathematical expression: {str(e)}")

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
    """Main entry point for the calculator server"""
    server = CalculatorServer()
    server.run()


if __name__ == "__main__":
    main()
