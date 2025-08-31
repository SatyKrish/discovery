"""
MCP Configuration Loader - Clean implementation based on temporal-ai-agents reference
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class MCPConfigLoader:
    """Loads and manages MCP server configurations"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Default to mcp-config.json in the project root
            self.config_path = Path(__file__).parent.parent.parent.parent / "mcp-config.json"
        else:
            self.config_path = Path(config_path)

        self.config = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from file"""
        if not self.config_path.exists():
            print(f"Warning: MCP config file not found at {self.config_path}")
            self.config = {"mcpServers": {}}
            return

        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)

            # Validate basic structure
            if "mcpServers" not in self.config:
                print("Warning: 'mcpServers' key not found in config, creating empty config")
                self.config["mcpServers"] = {}

        except json.JSONDecodeError as e:
            print(f"Error parsing MCP config file: {e}")
            self.config = {"mcpServers": {}}
        except Exception as e:
            print(f"Error loading MCP config file: {e}")
            self.config = {"mcpServers": {}}

    def get_servers(self) -> Dict[str, Dict[str, Any]]:
        """Get all MCP server configurations"""
        return self.config.get("mcpServers", {})

    def get_server_config(self, server_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific server"""
        servers = self.get_servers()
        return servers.get(server_name)

    def get_all_server_configs(self) -> List[Dict[str, Any]]:
        """Get all server configurations as a list"""
        servers = self.get_servers()
        configs = []

        for server_name, server_config in servers.items():
            # Add server name to config
            config_copy = server_config.copy()
            config_copy["name"] = server_name
            configs.append(config_copy)

        return configs

    def _expand_env_vars(self, value: Any) -> Any:
        """Recursively expand environment variables in configuration values"""
        if isinstance(value, str):
            # Handle ${VAR} and ${VAR:-default} syntax
            import re

            def replace_var(match):
                var_expr = match.group(1)
                if ':-' in var_expr:
                    var_name, default_value = var_expr.split(':-', 1)
                    return os.environ.get(var_name, default_value)
                else:
                    return os.environ.get(var_expr, "")

            return re.sub(r'\$\{([^}]+)\}', replace_var, value)

        elif isinstance(value, dict):
            return {k: self._expand_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._expand_env_vars(item) for item in value]
        else:
            return value

    def get_expanded_server_config(self, server_name: str) -> Optional[Dict[str, Any]]:
        """Get server config with environment variables expanded"""
        config = self.get_server_config(server_name)
        if config:
            expanded_config = self._expand_env_vars(config)
            # Ensure name is included
            expanded_config["name"] = server_name
            return expanded_config
        return None

    def get_all_expanded_configs(self) -> List[Dict[str, Any]]:
        """Get all server configs with environment variables expanded"""
        configs = self.get_all_server_configs()
        return [self._expand_env_vars(config) for config in configs]

    def reload_config(self):
        """Reload configuration from file"""
        self._load_config()

    def validate_config(self) -> List[str]:
        """Validate the configuration and return any issues"""
        issues = []

        servers = self.get_servers()

        for server_name, server_config in servers.items():
            # Check required fields based on type
            server_type = server_config.get("type", "stdio")

            if server_type == "stdio":
                required_fields = ["command", "args"]
                for field in required_fields:
                    if field not in server_config:
                        issues.append(f"Server '{server_name}': missing required field '{field}' for stdio type")

                # Validate command exists and is executable
                command = server_config.get("command")
                if command:
                    if not isinstance(command, str):
                        issues.append(f"Server '{server_name}': command must be a string")
                    elif not command.strip():
                        issues.append(f"Server '{server_name}': command cannot be empty")

                # Validate args is a list
                args = server_config.get("args", [])
                if not isinstance(args, list):
                    issues.append(f"Server '{server_name}': args must be a list")
                else:
                    # Check each arg is a string
                    for i, arg in enumerate(args):
                        if not isinstance(arg, str):
                            issues.append(f"Server '{server_name}': arg[{i}] must be a string")

            else:
                issues.append(f"Server '{server_name}': unknown server type '{server_type}'. Supported types: stdio")

            # Validate timeout
            timeout = server_config.get("timeout")
            if timeout is not None:
                if not isinstance(timeout, (int, float)):
                    issues.append(f"Server '{server_name}': timeout must be a number")
                elif timeout <= 0:
                    issues.append(f"Server '{server_name}': timeout must be positive")

        return issues


# Global instance
config_loader = MCPConfigLoader()


def load_mcp_servers_into_manager():
    """Load all MCP servers from config into the global MCP client manager"""
    try:
        from .mcp_client import mcp_client_manager

        # Clear existing servers
        mcp_client_manager.clients.clear()
        mcp_client_manager.server_health.clear()

        # Load servers from config
        configs = config_loader.get_all_expanded_configs()

        for config in configs:
            server_name = config["name"]
            mcp_client_manager.add_server(server_name, config)
            print(f"Loaded MCP server: {server_name} ({config.get('type', 'stdio')})")

    except ImportError:
        # Skip loading if running as standalone script
        pass


# Auto-load servers when module is imported (but not when run as script)
if __name__ != "__main__":
    load_mcp_servers_into_manager()
