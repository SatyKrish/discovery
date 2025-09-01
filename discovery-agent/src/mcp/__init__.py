"""
MCP (Model Context Protocol) module for discovery-agent
"""

# Import key components for easy access
from .core.client import mcp_client_manager
from .core.config import config_loader

__all__ = ['mcp_client_manager', 'config_loader']
