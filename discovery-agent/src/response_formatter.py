"""
Response Formatter - Client-agnostic formatting for structured responses
"""

import json
from typing import Any, Dict, List, Union
from datetime import datetime

from src.models import ResponseEnvelope, StructuredToolResult


class ResponseFormatter:
    """Formats responses for different client types and output formats"""

    @staticmethod
    def format_tool_result(result: StructuredToolResult) -> str:
        """Format a tool result into human-readable text"""
        if not result.success:
            return f"Tool '{result.tool_name}' failed: {result.error}"

        # Use formatted display if available
        if result.formatted_display:
            return result.formatted_display

        # Fallback to generic formatting based on tool type
        return ResponseFormatter._format_tool_data(result.tool_name, result.data)

    @staticmethod
    def _format_tool_data(tool_name: str, data: Any) -> str:
        """Format tool data based on tool type"""
        if tool_name == "calculator.calculate":
            return ResponseFormatter._format_calculator_result(data)
        elif tool_name == "web-search.web_search":
            return ResponseFormatter._format_web_search_result(data)
        elif tool_name == "echo.echo":
            return ResponseFormatter._format_echo_result(data)
        else:
            # Generic formatting
            return ResponseFormatter._format_generic_result(tool_name, data)

    @staticmethod
    def _format_calculator_result(data: Any) -> str:
        """Format calculator results"""
        if isinstance(data, dict):
            if "result" in data:
                return f"Calculation result: {data['result']}"
            elif "error" in data:
                return f"Calculation error: {data['error']}"
        return f"Calculator result: {str(data)}"

    @staticmethod
    def _format_web_search_result(data: Any) -> str:
        """Format web search results"""
        if isinstance(data, dict):
            query = data.get("query", "Unknown query")
            results = data.get("results", [])

            if not results:
                return f"No results found for '{query}'."

            response = f"Search results for '{query}':\n\n"
            for i, result in enumerate(results[:5], 1):  # Limit to top 5
                title = result.get("title", "No title")
                url = result.get("url", "")
                response += f"{i}. {title}\n"
                if url:
                    response += f"   {url}\n"
                response += "\n"

            if len(results) > 5:
                response += f"... and {len(results) - 5} more results."

            return response

        return f"Search result: {str(data)}"

    @staticmethod
    def _format_echo_result(data: Any) -> str:
        """Format echo results"""
        if isinstance(data, dict):
            text = data.get("text", "")
            return f"Echo: {text}"
        return f"Echo result: {str(data)}"

    @staticmethod
    def _format_generic_result(tool_name: str, data: Any) -> str:
        """Generic formatting for unknown tool types"""
        if isinstance(data, dict):
            return f"Tool '{tool_name}' completed with result: {json.dumps(data, indent=2)}"
        elif isinstance(data, list):
            return f"Tool '{tool_name}' returned {len(data)} items: {json.dumps(data, indent=2)}"
        else:
            return f"Tool '{tool_name}' result: {str(data)}"

    @staticmethod
    def create_response_envelope(
        response_type: str,
        status: str,
        content: Any,
        metadata: Dict[str, Any] = None,
        client_hints: Dict[str, Any] = None,
        timestamp: float = None
    ) -> ResponseEnvelope:
        """Create a standardized response envelope"""
        return ResponseEnvelope(
            type=response_type,
            status=status,
            content=content,
            metadata=metadata or {},
            client_hints=client_hints or {},
            timestamp=timestamp
        )

    @staticmethod
    def create_tool_response(
        tool_result: StructuredToolResult,
        include_raw_data: bool = False
    ) -> ResponseEnvelope:
        """Create a response envelope for tool execution"""
        # Format the display text
        formatted_display = ResponseFormatter.format_tool_result(tool_result)

        # Prepare content based on whether to include raw data
        if include_raw_data:
            content = {
                "formatted_display": formatted_display,
                "raw_data": tool_result.data,
                "execution_time": tool_result.execution_time,
                "next_actions": tool_result.next_actions
            }
        else:
            content = formatted_display

        # Create metadata
        metadata = {
            "tool_name": tool_result.tool_name,
            "execution_time": tool_result.execution_time,
            "has_next_actions": len(tool_result.next_actions) > 0
        }

        # Create client hints
        client_hints = {
            "completion_indicator": "tool_completed",
            "next_actions": tool_result.next_actions,
            "requires_user_input": len(tool_result.next_actions) > 0
        }

        return ResponseFormatter.create_response_envelope(
            response_type="tool_result",
            status="success" if tool_result.success else "error",
            content=content,
            metadata=metadata,
            client_hints=client_hints
        )

    @staticmethod
    def create_assistant_response(
        message: str,
        metadata: Dict[str, Any] = None
    ) -> ResponseEnvelope:
        """Create a response envelope for assistant messages"""
        client_hints = {
            "completion_indicator": "assistant_message",
            "requires_user_input": True
        }

        return ResponseFormatter.create_response_envelope(
            response_type="assistant_message",
            status="completed",
            content=message,
            metadata=metadata or {},
            client_hints=client_hints
        )

    @staticmethod
    def create_error_response(
        error_message: str,
        error_type: str = "general_error",
        metadata: Dict[str, Any] = None
    ) -> ResponseEnvelope:
        """Create a response envelope for errors"""
        client_hints = {
            "completion_indicator": "error",
            "error_type": error_type,
            "requires_user_input": True
        }

        return ResponseFormatter.create_response_envelope(
            response_type="error",
            status="error",
            content=error_message,
            metadata=metadata or {},
            client_hints=client_hints
        )

    @staticmethod
    def create_completion_response(
        summary: str = None,
        metadata: Dict[str, Any] = None
    ) -> ResponseEnvelope:
        """Create a response envelope for conversation completion"""
        content = summary or "Conversation completed successfully."

        client_hints = {
            "completion_indicator": "conversation_complete",
            "requires_user_input": False,
            "can_restart": True
        }

        return ResponseFormatter.create_response_envelope(
            response_type="completion",
            status="completed",
            content=content,
            metadata=metadata or {},
            client_hints=client_hints
        )


# Global formatter instance
response_formatter = ResponseFormatter()
