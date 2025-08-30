# MCP (Model Context Protocol) Integration

This document describes the MCP integration in the discovery-agent, which provides a standardized way to connect to local and remote tools.

## Overview

The discovery-agent now uses MCP as the primary approach for managing and connecting to tools. This provides several benefits:

- **Standardization**: Follows MCP protocol specifications
- **Flexibility**: Support for both local (stdio) and remote (streamable-http) tools
- **Scalability**: Easy to add new tools without code changes
- **Configuration-driven**: Tool definitions managed through `mcp-config.json`

## Architecture

### Components

1. **MCP Servers** (`tools/` directory)
   - Individual tool implementations as MCP servers
   - Each server runs as a separate process
   - Communicate via stdio transport

2. **MCP Client** (`src/mcp_client.py`)
   - Manages connections to MCP servers
   - Supports both stdio and streamable-http transports
   - Handles tool discovery and execution

3. **Configuration** (`mcp-config.json`)
   - Declarative configuration of MCP servers
   - Environment variable expansion
   - Validation and error handling

4. **Registry** (`src/registry.py`)
   - Pure MCP-based tool registry
   - No static tool registration
   - Dynamic tool discovery and caching

## Configuration

### mcp-config.json

```json
{
  "mcpServers": {
    "echo": {
      "type": "stdio",
      "command": "python",
      "args": ["tools/echo_server.py"],
      "env": {},
      "description": "Simple echo tool for testing"
    },
    "calculator": {
      "type": "stdio",
      "command": "python",
      "args": ["tools/calculator_server.py"],
      "env": {},
      "description": "Mathematical calculations"
    },
    "web-search": {
      "type": "stdio",
      "command": "python",
      "args": ["tools/web_search_server.py"],
      "env": {
        "SEARCH_API_KEY": "${SEARCH_API_KEY:-}"
      },
      "description": "Web search functionality"
    }
  }
}
```

### Environment Variables

The configuration supports environment variable expansion:

- `${VAR}` - Required environment variable
- `${VAR:-default}` - Optional with default value

## Tool Development

### Creating a New MCP Server

1. **Create the server file** in `tools/` directory:

```python
#!/usr/bin/env python3
from base_server import BaseMCPServer

class MyToolServer(BaseMCPServer):
    def __init__(self):
        super().__init__("my-tool-server", "1.0.0")

    def _setup_tools(self):
        @self.server.tool()
        async def my_tool(param: str) -> str:
            """Description of my tool"""
            return f"Processed: {param}"

def main():
    server = MyToolServer()
    server.run()

if __name__ == "__main__":
    main()
```

2. **Add to mcp-config.json**:

```json
{
  "mcpServers": {
    "my-tool": {
      "type": "stdio",
      "command": "python",
      "args": ["tools/my_tool_server.py"],
      "env": {},
      "description": "My custom tool"
    }
  }
}
```

3. **Make executable**:

```bash
chmod +x tools/my_tool_server.py
```

## Transport Types

### Stdio Transport (Local Tools)

- **Use case**: Tools running on the same machine
- **Advantages**: No network overhead, process isolation
- **Configuration**: Requires `command` and `args`

### Streamable HTTP Transport (Remote Tools)

- **Use case**: Tools running on remote servers
- **Advantages**: Network-accessible, scalable
- **Configuration**: Requires `url` and optional authentication

## Testing

### Running the Test Suite

```bash
cd discovery-agent
python test_mcp_setup.py
```

This will:
- Load MCP configuration
- Create MCP clients
- Discover available tools
- Test tool execution
- Validate the registry

### Manual Testing

```python
import asyncio
from src.mcp_client import tool_orchestrator

async def test():
    # Discover tools
    tools = await tool_orchestrator.discover_dynamic_tools()
    print(f"Available tools: {tools}")

    # Execute a tool
    result = await tool_orchestrator.execute_tool("echo.echo", {"text": "Hello"})
    print(f"Result: {result}")

asyncio.run(test())
```

## Migration from Static Tools

### Before (Static Registration)

```python
from src.registry import registry

registry.register(
    "echo",
    lambda args: {"echo": args.get("text")},
    description="Echo back text"
)
```

### After (MCP-based)

1. Create `tools/echo_server.py` as MCP server
2. Add configuration to `mcp-config.json`
3. Remove static registration code

## Best Practices

### Tool Design

1. **Single Responsibility**: Each MCP server should provide one type of functionality
2. **Error Handling**: Implement proper error handling and validation
3. **Documentation**: Provide clear descriptions and parameter schemas
4. **Testing**: Test tools independently before integration

### Configuration

1. **Environment Variables**: Use environment variables for sensitive data
2. **Validation**: Validate configuration on startup
3. **Documentation**: Document all configuration options

### Performance

1. **Caching**: Implement appropriate caching for expensive operations
2. **Async Operations**: Use async/await for I/O operations
3. **Resource Management**: Properly manage process lifecycle

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `src/` is in Python path
2. **Configuration Errors**: Validate `mcp-config.json` syntax
3. **Process Failures**: Check server logs and error messages
4. **Tool Discovery**: Verify MCP server is running and accessible

### Debugging

```bash
# Enable debug logging
export PYTHONPATH=src
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"

# Test individual components
python -c "from src.mcp_config import config_loader; print(config_loader.get_servers())"
```

## Future Enhancements

1. **Remote MCP Servers**: Add support for streamable-http transport
2. **Tool Marketplace**: Dynamic tool discovery and installation
3. **Authentication**: OAuth and API key support for remote servers
4. **Monitoring**: Tool usage metrics and health monitoring
5. **Caching**: Intelligent response caching and invalidation

## References

- [MCP Specification](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Stdio Transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#stdio)
- [Streamable HTTP Transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)
