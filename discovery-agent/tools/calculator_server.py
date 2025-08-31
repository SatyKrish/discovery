#!/usr/bin/env python3
"""
Calculator MCP Server - Safe mathematical calculations
"""

import asyncio
import sys
import os
import re
from typing import Union

# Add the parent directory to the path so we can import base_server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_server import BaseMCPServer

class CalculatorServer(BaseMCPServer):
    """MCP Server for calculator functionality"""

    def __init__(self):
        super().__init__("calculator-server", "1.0.0")

    def _setup_tools(self):
        """Setup the calculator tools"""

        @self.server.call_tool()
        async def calculate(name: str, arguments: dict = None) -> Union[float, int, str]:
            """Calculate mathematical expressions safely."""
            if arguments and "expression" in arguments:
                expression = arguments["expression"]
                try:
                    # Use safe evaluation
                    result = self._safe_eval_math(expression)
                    return result
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Error: No expression provided"

        @self.server.call_tool()
        async def add(name: str, arguments: dict = None) -> float:
            """Add two numbers."""
            if arguments and "a" in arguments and "b" in arguments:
                return arguments["a"] + arguments["b"]
            return "Error: Missing arguments 'a' and/or 'b'"

        @self.server.call_tool()
        async def subtract(name: str, arguments: dict = None) -> float:
            """Subtract second number from first."""
            if arguments and "a" in arguments and "b" in arguments:
                return arguments["a"] - arguments["b"]
            return "Error: Missing arguments 'a' and/or 'b'"

        @self.server.call_tool()
        async def multiply(name: str, arguments: dict = None) -> float:
            """Multiply two numbers."""
            if arguments and "a" in arguments and "b" in arguments:
                return arguments["a"] * arguments["b"]
            return "Error: Missing arguments 'a' and/or 'b'"

        @self.server.call_tool()
        async def divide(name: str, arguments: dict = None) -> Union[float, str]:
            """Divide first number by second."""
            if arguments and "a" in arguments and "b" in arguments:
                if arguments["b"] == 0:
                    return "Error: Division by zero"
                return arguments["a"] / arguments["b"]
            return "Error: Missing arguments 'a' and/or 'b'"

        @self.server.list_tools()
        async def list_tools() -> list:
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


def main():
    """Main entry point for the calculator server"""
    server = CalculatorServer()
    server.run()


if __name__ == "__main__":
    main()
