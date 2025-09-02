#!/usr/bin/env python3
"""
Test MCP result processing functionality
"""

import sys
import os
import json
import pytest

# Add src to path for robust imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)


def test_mcp_result_processing_basic():
    """Test basic MCP result processing"""
    from tests.test_utils import format_tool_result_for_display

    # Mock MCP result similar to what the servers return
    mock_mcp_result = {
        "content": [
            {"type": "text", "text": "Echo: Hello World"},
            {"type": "text", "text": "This is a test"}
        ],
        "tool": "echo.echo",
        "success": True
    }

    # Test the workflow formatting function
    formatted_result = format_tool_result_for_display("echo.echo", mock_mcp_result)
    assert "Echo: Hello World" in formatted_result
    assert "This is a test" in formatted_result


def test_mcp_result_processing_empty_content():
    """Test MCP result processing with empty content"""
    from tests.test_utils import format_tool_result_for_display

    mock_mcp_result = {
        "content": [],
        "tool": "echo.echo",
        "success": True
    }

    formatted_result = format_tool_result_for_display("echo.echo", mock_mcp_result)
    assert "completed but returned no content" in formatted_result


def test_mcp_result_processing_mixed_content():
    """Test MCP result processing with mixed content types"""
    from tests.test_utils import format_tool_result_for_display

    mock_mcp_result = {
        "content": [
            {"type": "text", "text": "Hello World"},
            {"type": "image", "data": "base64data"},
            "plain string content"
        ],
        "tool": "mixed.tool",
        "success": True
    }

    formatted_result = format_tool_result_for_display("mixed.tool", mock_mcp_result)
    assert "Hello World" in formatted_result
    assert "plain string content" in formatted_result


def test_format_tool_result_for_display_json_string():
    """Test formatting when result is a JSON string"""
    from tests.test_utils import format_tool_result_for_display

    json_result = '{"text": "Hello from JSON", "status": "success"}'
    formatted = format_tool_result_for_display("echo.echo", json_result)
    assert "Hello from JSON" in formatted


def test_format_tool_result_for_display_plain_string():
    """Test formatting when result is a plain string"""
    from tests.test_utils import format_tool_result_for_display

    plain_result = "Plain text result"
    formatted = format_tool_result_for_display("test.tool", plain_result)
    assert formatted == "Plain text result"


def test_format_tool_result_for_display_other_types():
    """Test formatting when result is other types"""
    from tests.test_utils import format_tool_result_for_display

    # Test with integer
    int_result = 42
    formatted = format_tool_result_for_display("test.tool", int_result)
    assert formatted == "42"

    # Test with list
    list_result = [1, 2, 3]
    formatted = format_tool_result_for_display("test.tool", list_result)
    assert "1" in formatted and "2" in formatted


def test_error_handling_malformed_content():
    """Test error handling with malformed content"""
    from tests.test_utils import format_tool_result_for_display

    # Test with malformed content
    malformed_result = {
        "content": [
            {"type": "text"},  # Missing text field
            "string content",  # String instead of dict
            {"invalid": "structure"}
        ],
        "tool": "test.tool",
        "success": True
    }

    # Should not raise exception, should handle gracefully
    formatted = format_tool_result_for_display("test.tool", malformed_result)
    assert isinstance(formatted, str)
    assert len(formatted) > 0


def test_format_mcp_content_result_various_types():
    """Test MCP content formatting with various content types"""
    from tests.test_utils import format_tool_result_for_display

    # Test with only text content
    text_only = {
        "content": [
            {"type": "text", "text": "First message"},
            {"type": "text", "text": "Second message"}
        ],
        "tool": "echo.echo",
        "success": True
    }

    formatted = format_tool_result_for_display("echo.echo", text_only)
    assert "First message" in formatted
    assert "Second message" in formatted

    # Test with no text content
    no_text = {
        "content": [
            {"type": "image", "data": "image_data"},
            {"type": "file", "path": "/tmp/file.txt"}
        ],
        "tool": "file.tool",
        "success": True
    }

    formatted = format_tool_result_for_display("file.tool", no_text)
    assert "completed with 2 content items" in formatted


def test_format_json_result_different_tools():
    """Test JSON result formatting for different tools"""
    from tests.test_utils import format_tool_result_for_display

    # Test echo tool
    echo_data = {"text": "Hello World"}
    formatted = format_tool_result_for_display("echo.echo", echo_data)
    assert formatted == "Echo: Hello World"

    # Test other tool (should return JSON)
    other_data = {"result": "some data", "status": "ok"}
    formatted = format_tool_result_for_display("other.tool", other_data)
    # Should contain the JSON data
    assert "result" in formatted
    assert "some data" in formatted
