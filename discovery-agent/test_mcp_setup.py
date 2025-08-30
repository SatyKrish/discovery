#!/usr/bin/env python3
"""
Test script for MCP setup validation
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_mcp_setup():
    """Test the MCP setup"""
    print("🔧 Testing MCP Setup")
    print("=" * 50)

    try:
        # Test config loading
        print("📄 Testing configuration loading...")
        from src.mcp_config import config_loader

        servers = config_loader.get_servers()
        print(f"✅ Found {len(servers)} MCP servers in config:")
        for name, config in servers.items():
            print(f"   - {name}: {config.get('type', 'streamable-http')}")

        # Test MCP client creation
        print("\n🔌 Testing MCP client creation...")
        from src.mcp_client import tool_orchestrator

        configs = config_loader.get_all_expanded_configs()
        for config in configs:
            server_name = config["name"]
            print(f"   - Creating client for {server_name}...")
            tool_orchestrator.add_mcp_server(server_name, config)

        print("✅ All MCP clients created successfully")

        # Test tool discovery
        print("\n🔍 Testing tool discovery...")
        all_tools = await tool_orchestrator.discover_dynamic_tools()

        total_tools = 0
        for server_name, tools in all_tools.items():
            print(f"   - {server_name}: {len(tools)} tools")
            total_tools += len(tools)
            for tool in tools:
                print(f"     • {tool['name']}: {tool.get('description', 'No description')}")

        print(f"✅ Total tools discovered: {total_tools}")

        # Test tool execution (if tools are available)
        if total_tools > 0:
            print("\n⚡ Testing tool execution...")

            # Test echo tool
            if "echo" in [config["name"] for config in configs]:
                try:
                    result = await tool_orchestrator.execute_tool("echo.echo", {"text": "Hello MCP!"})
                    print(f"✅ Echo tool result: {result}")
                except Exception as e:
                    print(f"❌ Echo tool failed: {e}")

            # Test calculator tool
            if "calculator" in [config["name"] for config in configs]:
                try:
                    result = await tool_orchestrator.execute_tool("calculator.calculate", {"expression": "2 + 3"})
                    print(f"✅ Calculator tool result: {result}")
                except Exception as e:
                    print(f"❌ Calculator tool failed: {e}")

        # Test registry
        print("\n📋 Testing tool registry...")
        from src.registry import registry, list_tool_specs

        specs = list_tool_specs()
        print(f"✅ Registry has {len(specs)} tool specs")

        print("\n🎉 MCP Setup Test Complete!")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"❌ MCP Setup Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    success = asyncio.run(test_mcp_setup())
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
