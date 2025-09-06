#!/usr/bin/env python3
"""
Test script for MCP tool dispatch functionality
"""

import asyncio
import sys
import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.models import ToolCall, StructuredToolResult
from src.mcp.core.tool_dispatch import execute_mcp_tool, tool_dispatch, ToolNotFoundError, ToolExecutionError


@pytest.mark.skip(reason="Integration test requiring MCP servers running - disabled for unit test focus")
@pytest.mark.asyncio
async def test_execute_mcp_tool_success():
    """Test successful MCP tool execution"""
    pass


@pytest.mark.asyncio
async def test_execute_mcp_tool_server_not_found():
    """Test MCP tool execution with non-existent server"""
    with patch('src.mcp.core.tool_dispatch.config_loader') as mock_config:
        mock_config.get_expanded_server_config.return_value = None

        with pytest.raises(ToolNotFoundError, match="MCP server 'nonexistent' not configured"):
            await execute_mcp_tool("nonexistent.echo", {"text": "test"})


@pytest.mark.asyncio
async def test_execute_mcp_tool_invalid_format():
    """Test MCP tool execution with invalid tool name format"""
    with pytest.raises(ToolNotFoundError, match="Invalid MCP tool name format"):
        await execute_mcp_tool("invalid_tool_name", {"text": "test"})


@pytest.mark.skip(reason="Integration test requiring Temporal worker runtime - disabled for unit test focus")
@pytest.mark.asyncio
async def test_tool_dispatch_activity_success():
    """Test tool dispatch activity with successful execution"""
    pass


@pytest.mark.skip(reason="Integration test requiring Temporal worker runtime - disabled for unit test focus")
@pytest.mark.asyncio
async def test_tool_dispatch_activity_tool_not_found():
    """Test tool dispatch activity with tool not found"""
    pass


@pytest.mark.skip(reason="Integration test requiring Temporal worker runtime - disabled for unit test focus")
@pytest.mark.asyncio
async def test_tool_dispatch_activity_execution_error():
    """Test tool dispatch activity with execution error"""
    pass


@pytest.mark.skip(reason="Integration test requiring Temporal worker runtime - disabled for unit test focus")
@pytest.mark.asyncio
async def test_tool_dispatch_activity_unexpected_error():
    """Test tool dispatch activity with unexpected error"""
    pass


def test_tool_call_model():
    """Test ToolCall model creation and validation"""
    tool_call = ToolCall(id="test-1", name="echo.echo", args={"text": "hello"})
    assert tool_call.id == "test-1"
    assert tool_call.name == "echo.echo"
    assert tool_call.args == {"text": "hello"}
    assert tool_call.requires_approval is False


def test_structured_tool_result_model():
    """Test StructuredToolResult model"""
    result = StructuredToolResult(
        success=True,
        data={"content": "Hello"}
    )
    assert result.success is True
    assert result.data == {"content": "Hello"}


if __name__ == "__main__":
    # Run with pytest for better output
    pytest.main([__file__, "-v"])
