#!/usr/bin/env python3
"""
Test MCP core components
"""

import sys
import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio

from src.mcp.core.client import MCPClientManager, ToolOrchestrator


@pytest.fixture
def mcp_manager():
    """Fixture for MCPClientManager instance"""
    return MCPClientManager()


@pytest.fixture
def tool_orchestrator():
    """Fixture for ToolOrchestrator instance"""
    return ToolOrchestrator()


def test_mcp_client_manager_init(mcp_manager):
    """Test MCPClientManager initialization"""
    assert isinstance(mcp_manager.clients, dict)
    assert isinstance(mcp_manager.server_health, dict)
    assert len(mcp_manager.clients) == 0
    assert len(mcp_manager.server_health) == 0


def test_add_server(mcp_manager):
    """Test adding a server to MCPClientManager"""
    server_config = {
        "name": "test_server",
        "type": "stdio",
        "command": "python",
        "args": ["server.py"]
    }

    mcp_manager.add_server("test_server", server_config)

    assert "test_server" in mcp_manager.clients
    assert mcp_manager.clients["test_server"] == server_config
    assert "test_server" in mcp_manager.server_health
    assert mcp_manager.server_health["test_server"]["status"] == "unknown"
    assert mcp_manager.server_health["test_server"]["tool_count"] == 0


@pytest.mark.asyncio
async def test_get_client_existing(mcp_manager):
    """Test getting an existing client"""
    server_config = {"name": "existing_server", "type": "stdio"}
    mcp_manager.add_server("existing_server", server_config)

    result = await mcp_manager.get_client(server_config)
    assert result == server_config


@pytest.mark.asyncio
async def test_get_client_new(mcp_manager):
    """Test getting a new client (auto-adds server)"""
    server_config = {"name": "new_server", "type": "stdio"}

    result = await mcp_manager.get_client(server_config)
    assert result == server_config
    assert "new_server" in mcp_manager.clients


@pytest.mark.skip(reason="Integration test requiring MCP client libraries and servers - disabled for unit test focus")
@pytest.mark.asyncio
async def test_execute_tool_success(mcp_manager):
    """Test successful tool execution"""
    pass


@pytest.mark.skip(reason="Integration test requiring MCP client libraries - disabled for unit test focus")
@pytest.mark.asyncio
async def test_execute_tool_error(mcp_manager):
    """Test tool execution with error"""
    pass


@pytest.mark.skip(reason="Integration test requiring MCP client libraries and servers - disabled for unit test focus")
@pytest.mark.asyncio
async def test_discover_tools_success(mcp_manager):
    """Test successful tool discovery"""
    pass


@pytest.mark.skip(reason="Integration test requiring MCP client libraries - disabled for unit test focus")
@pytest.mark.asyncio
async def test_discover_tools_error(mcp_manager):
    """Test tool discovery with error"""
    pass


def test_build_connection_stdio(mcp_manager):
    """Test building stdio connection parameters"""
    server_definition = {
        "type": "stdio",
        "command": "python",
        "args": ["server.py"],
        "env": {"TEST": "value"}
    }

    result = mcp_manager._build_connection(server_definition)

    assert result["type"] == "stdio"
    assert result["command"] == "python"
    assert result["args"] == ["server.py"]
    assert result["env"] == {"TEST": "value"}


def test_build_connection_defaults(mcp_manager):
    """Test building connection with defaults"""
    server_definition = {}

    result = mcp_manager._build_connection(server_definition)

    assert result["type"] == "stdio"
    assert result["command"] == "python"
    assert result["args"] == ["server.py"]
    assert result["env"] == {}


def test_tool_orchestrator_init(tool_orchestrator):
    """Test ToolOrchestrator initialization"""
    assert isinstance(tool_orchestrator.tool_cache, dict)
    assert isinstance(tool_orchestrator.server_configs, dict)


def test_add_mcp_server(tool_orchestrator):
    """Test adding MCP server to orchestrator"""
    server_config = {
        "name": "test_server",
        "type": "stdio",
        "command": "python"
    }

    tool_orchestrator.add_mcp_server("test_server", server_config)

    assert "test_server" in tool_orchestrator.server_configs
    assert tool_orchestrator.server_configs["test_server"] == server_config


@pytest.mark.asyncio
async def test_execute_tool_orchestrator_success(tool_orchestrator):
    """Test successful tool execution via orchestrator"""
    server_config = {
        "name": "test_server",
        "type": "stdio"
    }
    tool_orchestrator.add_mcp_server("test_server", server_config)

    mock_result = {"success": True, "content": ["Result"]}

    with patch('src.mcp.core.client.mcp_client_manager') as mock_manager:
        mock_manager.execute_tool = AsyncMock(return_value=mock_result)

        result = await tool_orchestrator.execute_tool("test_server.echo", {"text": "test"})

        assert result == mock_result
        mock_manager.execute_tool.assert_called_once_with(server_config, "echo", {"text": "test"})


@pytest.mark.asyncio
async def test_execute_tool_orchestrator_invalid_format(tool_orchestrator):
    """Test tool execution with invalid name format"""
    with pytest.raises(ValueError, match="Invalid tool name format"):
        await tool_orchestrator.execute_tool("invalid_name", {})


@pytest.mark.asyncio
async def test_execute_tool_orchestrator_unknown_server(tool_orchestrator):
    """Test tool execution with unknown server"""
    with pytest.raises(ValueError, match="Unknown server"):
        await tool_orchestrator.execute_tool("unknown.echo", {})


@pytest.mark.asyncio
async def test_discover_tools_orchestrator(tool_orchestrator):
    """Test tool discovery via orchestrator"""
    server_config = {
        "name": "test_server",
        "type": "stdio"
    }
    tool_orchestrator.add_mcp_server("test_server", server_config)

    mock_result = {
        "success": True,
        "tools": {"echo": {"name": "echo", "description": "Echo tool"}}
    }

    with patch('src.mcp.core.client.mcp_client_manager') as mock_manager:
        mock_manager.discover_tools = AsyncMock(return_value=mock_result)

        result = await tool_orchestrator.discover_tools("test_server")

        assert result == mock_result
        assert "test_server" in tool_orchestrator.tool_cache
        mock_manager.discover_tools.assert_called_once_with(server_config)


@pytest.mark.asyncio
async def test_discover_tools_orchestrator_unknown_server(tool_orchestrator):
    """Test tool discovery with unknown server"""
    with pytest.raises(ValueError, match="Unknown server"):
        await tool_orchestrator.discover_tools("unknown_server")


@pytest.mark.asyncio
async def test_discover_all_tools(tool_orchestrator):
    """Test discovering tools from all servers"""
    server_config1 = {"name": "server1", "type": "stdio"}
    server_config2 = {"name": "server2", "type": "stdio"}

    tool_orchestrator.add_mcp_server("server1", server_config1)
    tool_orchestrator.add_mcp_server("server2", server_config2)

    mock_result = {"success": True, "tools": {}}

    with patch('src.mcp.core.client.mcp_client_manager') as mock_manager:
        mock_manager.discover_tools = AsyncMock(return_value=mock_result)

        await tool_orchestrator.discover_all_tools()

        assert mock_manager.discover_tools.call_count == 2


@pytest.mark.asyncio
async def test_stdio_connection_missing_mcp():
    """Test stdio connection when MCP libraries are not available"""
    manager = MCPClientManager()

    # Mock missing MCP libraries
    with patch('src.mcp.core.client.stdio_client', None):
        server_config = {
            "name": "test_server",
            "type": "stdio",
            "command": "python",
            "args": ["server.py"]
        }

        with pytest.raises(Exception, match="MCP client libraries not available"):
            async with manager._stdio_connection("python", ["server.py"], {}):
                pass
