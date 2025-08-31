#!/usr/bin/env python3
"""
Enhanced MCP Tool Response Handler
Handles tool call detection, execution, and response formatting
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ToolCallResult:
    call_id: str
    tool_name: str
    success: bool
    result: Any = None
    error: str = None
    execution_time: float = 0.0

class MCPToolResponseHandler:
    def __init__(self, timeout_seconds: int = 30):
        self.timeout_seconds = timeout_seconds
        self.pending_calls: Dict[str, ToolCallResult] = {}

    def detect_tool_call(self, content: str) -> Optional[Dict[str, Any]]:
        """Detect tool calls in various formats the agent might return"""
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            return None

        # Format 1: Simple tool call
        if isinstance(parsed, dict) and "tool_call" in parsed and "parameters" in parsed:
            tool_name = parsed["tool_call"]
            if "." not in tool_name:  # Add server prefix if missing
                tool_name = self._infer_server_prefix(tool_name)
            return {
                "name": tool_name,
                "args": parsed["parameters"]
            }

        # Format 2: Nested tool call
        if isinstance(parsed, dict) and "tool_call" in parsed:
            tc = parsed["tool_call"]
            if isinstance(tc, dict) and "tool_name" in tc and "parameters" in tc:
                tool_name = tc["tool_name"]
                if "." not in tool_name:
                    tool_name = self._infer_server_prefix(tool_name)
                return {
                    "name": tool_name,
                    "args": tc["parameters"]
                }

        # Format 3: Sentinel format (existing system)
        if isinstance(parsed, dict) and "_tool_request" in parsed:
            return parsed["_tool_request"]

        return None

    def _infer_server_prefix(self, tool_name: str) -> str:
        """Infer MCP server prefix based on tool name"""
        tool_mappings = {
            "weather": "weather",
            "weather_api": "weather",
            "get_current_weather": "weather",
            "find_flights": "flights",
            "flight": "flights",
            "search": "web-search",
            "calculate": "calculator",
            "echo": "echo"
        }

        for keyword, server in tool_mappings.items():
            if keyword in tool_name.lower():
                return f"{server}.{tool_name}"

        return f"web-search.{tool_name}"  # Default fallback

    async def execute_tool_call(self, call_id: str, tool_name: str, args: Dict[str, Any]) -> ToolCallResult:
        """Execute a tool call with proper error handling and timeout"""
        start_time = time.time()

        # Record pending call
        self.pending_calls[call_id] = ToolCallResult(
            call_id=call_id,
            tool_name=tool_name,
            success=False
        )

        try:
            # Import here to avoid circular imports
            from src.registry import execute_tool

            # Execute with timeout
            result = await asyncio.wait_for(
                execute_tool(tool_name, args),
                timeout=self.timeout_seconds
            )

            execution_time = time.time() - start_time

            # Update pending call
            self.pending_calls[call_id] = ToolCallResult(
                call_id=call_id,
                tool_name=tool_name,
                success=True,
                result=result,
                execution_time=execution_time
            )

            return self.pending_calls[call_id]

        except asyncio.TimeoutError:
            error_msg = f"Tool {tool_name} timed out after {self.timeout_seconds}s"
            self.pending_calls[call_id] = ToolCallResult(
                call_id=call_id,
                tool_name=tool_name,
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
            return self.pending_calls[call_id]

        except Exception as e:
            error_msg = f"Tool {tool_name} failed: {str(e)}"
            self.pending_calls[call_id] = ToolCallResult(
                call_id=call_id,
                tool_name=tool_name,
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
            return self.pending_calls[call_id]

    def get_call_result(self, call_id: str) -> Optional[ToolCallResult]:
        """Get result of a tool call"""
        return self.pending_calls.get(call_id)

    def format_result_for_agent(self, result: ToolCallResult) -> str:
        """Format tool result for agent consumption"""
        if result.success:
            return f"Tool {result.tool_name} completed successfully. Result: {json.dumps(result.result)}"
        else:
            return f"Tool {result.tool_name} failed. Error: {result.error}"

    def cleanup_old_calls(self, max_age: int = 300):
        """Clean up old completed/failed calls"""
        cutoff_time = time.time() - max_age
        to_remove = []

        for call_id, call_info in self.pending_calls.items():
            if call_info.execution_time > 0 and (time.time() - call_info.execution_time) > max_age:
                to_remove.append(call_id)

        for call_id in to_remove:
            del self.pending_calls[call_id]

# Global instance
tool_response_handler = MCPToolResponseHandler()
