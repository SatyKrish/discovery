#!/usr/bin/env python3
"""
Test utilities for unit tests
"""

import json
from typing import Any


def format_tool_result_for_display(tool_name: str, result: Any) -> str:
    """
    Test utility function for formatting tool results for display.
    This is a test-only utility, not part of the main application.
    """
    try:
        # Handle MCP tool results (already dict format)
        if isinstance(result, dict):
            # Check if this is an MCP tool result with content array
            if "content" in result and isinstance(result["content"], list):
                return _format_mcp_content_result(tool_name, result)
            else:
                return _format_json_result(tool_name, result)

        # Handle string results (try to parse as JSON)
        elif isinstance(result, str):
            try:
                parsed = json.loads(result)
                return _format_json_result(tool_name, parsed)
            except json.JSONDecodeError:
                return result

        # Handle other types
        else:
            return str(result)
    except Exception as e:
        # Fallback to string representation
        return f"Tool result: {str(result)}"


def _format_mcp_content_result(tool_name: str, data: dict) -> str:
    """Format MCP content result for display"""
    content_list = data.get("content", [])

    if not content_list:
        return f"Tool '{tool_name}' completed but returned no content."

    # Extract text content from MCP result
    text_parts = []
    for item in content_list:
        if isinstance(item, dict) and item.get("type") == "text":
            text_parts.append(item.get("text", ""))
        elif isinstance(item, str):
            text_parts.append(item)

    if text_parts:
        combined_text = " ".join(text_parts)
        return f"Tool '{tool_name}' result: {combined_text}"
    else:
        # Fallback for non-text content
        return f"Tool '{tool_name}' completed with {len(content_list)} content items."


def _format_json_result(tool_name: str, data: dict) -> str:
    """Format JSON result for display"""
    if tool_name == "echo.echo":
        text = data.get("text", "")
        return f"Echo: {text}"
    else:
        return json.dumps(data, indent=2)
