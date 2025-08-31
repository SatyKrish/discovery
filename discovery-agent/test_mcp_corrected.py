#!/usr/bin/env python3
"""
Test script to verify the corrected MCP implementation
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_mcp_client():
    """Test the MCP client functionality"""
    print("Testing MCP Client...")

    try:
        from src.mcp_client import MCPClientManager
        from src.mcp_config import config_loader

        # Create client manager
        manager = MCPClientManager()

        # Load server configs
        configs = config_loader.get_all_expanded_configs()
        print(f"Found {len(configs)} MCP server configurations")

        for config in configs:
            print(f"  - {config['name']}: {config.get('description', 'No description')}")

        # Add servers to manager
        for config in configs:
            manager.add_server(config["name"], config)

        # Test tool discovery
        print("\nDiscovering tools...")
        tools = await manager.discover_all_tools()

        total_tools = 0
        for server_name, server_tools in tools.items():
            print(f"  Server '{server_name}': {len(server_tools)} tools")
            total_tools += len(server_tools)
            for tool in server_tools:
                print(f"    - {tool['name']}: {tool.get('description', 'No description')}")

        print(f"\nTotal tools discovered: {total_tools}")

        # Test tool execution if tools were found
        if total_tools > 0:
            print("\nTesting tool execution...")
            # Try to execute echo tool
            for server_name, server_tools in tools.items():
                for tool in server_tools:
                    if tool['name'] == 'echo':
                        print(f"Testing echo tool on server '{server_name}'...")
                        try:
                            client = await manager.get_client({"name": server_name})
                            async with client:
                                result = await client.execute_tool('echo', {"text": "Hello MCP!"})
                                print(f"Echo result: {result}")
                        except Exception as e:
                            print(f"Error executing echo tool: {e}")
                        break
                else:
                    continue
                break

        # Get health metrics
        health = manager.get_health_metrics()
        print("\nServer health:")
        for server_name, metrics in health.items():
            print(f"  {server_name}: {metrics.get('status', 'unknown')}")

        return True

    except Exception as e:
        print(f"MCP Client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_tool_dispatch():
    """Test the tool dispatch activity"""
    print("\nTesting Tool Dispatch Activity...")

    try:
        from src.activities.tool_dispatch import execute_tool_with_mcp
        from src.mcp_config import config_loader

        # Test with a simple echo tool call
        configs = config_loader.get_all_expanded_configs()
        if configs:
            server_name = configs[0]["name"]
            tool_name = f"{server_name}.echo"

            print(f"Testing tool dispatch for: {tool_name}")
            result = await execute_tool_with_mcp(tool_name, {"text": "Test from tool dispatch"})
            print(f"Tool dispatch result: {result}")
            return True
        else:
            print("No MCP servers configured for tool dispatch test")
            return False

    except Exception as e:
        print(f"Tool dispatch test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("=== MCP Implementation Test ===\n")

    # Test MCP client
    client_test = await test_mcp_client()

    # Test tool dispatch
    dispatch_test = await test_tool_dispatch()

    print("\n=== Test Results ===")
    print(f"MCP Client Test: {'PASS' if client_test else 'FAIL'}")
    print(f"Tool Dispatch Test: {'PASS' if dispatch_test else 'FAIL'}")

    if client_test and dispatch_test:
        print("\n✅ All tests passed! MCP implementation is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
