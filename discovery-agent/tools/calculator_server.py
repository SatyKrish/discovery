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

        @self.server.tool()
        async def calculate(expression: str) -> Union[float, int, str]:
            """Calculate mathematical expressions safely.

            Supports basic arithmetic operations: +, -, *, /, **
            Also supports parentheses and mathematical constants like pi, e

            Args:
                expression: Mathematical expression to evaluate

            Returns:
                The result of the calculation or error message
            """
            try:
                # Use safe evaluation
                result = self._safe_eval_math(expression)
                return result
            except Exception as e:
                return f"Error: {str(e)}"

        @self.server.tool()
        async def add(a: float, b: float) -> float:
            """Add two numbers.

            Args:
                a: First number
                b: Second number

            Returns:
                Sum of the two numbers
            """
            return a + b

        @self.server.tool()
        async def subtract(a: float, b: float) -> float:
            """Subtract second number from first.

            Args:
                a: First number
                b: Second number

            Returns:
                Difference of the two numbers
            """
            return a - b

        @self.server.tool()
        async def multiply(a: float, b: float) -> float:
            """Multiply two numbers.

            Args:
                a: First number
                b: Second number

            Returns:
                Product of the two numbers
            """
            return a * b

        @self.server.tool()
        async def divide(a: float, b: float) -> Union[float, str]:
            """Divide first number by second.

            Args:
                a: First number
                b: Second number

            Returns:
                Quotient of the division or error if dividing by zero
            """
            if b == 0:
                return "Error: Division by zero"
            return a / b

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
