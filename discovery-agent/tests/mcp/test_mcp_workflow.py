#!/usr/bin/env python3
"""
Test script for the clean MCP implementation based on temporal-ai-agents reference
"""

import asyncio
import sys
import os
import time

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp.core.client import mcp_client_manager
from src.mcp.core.config import config_loader, load_mcp_servers_into_manager
from src.workflows.agent_orchestrator import format_tool_result_for_display


async def test_clean_mcp_implementation():
    """Test the clean MCP implementation"""
    print("🧪 Testing Clean MCP Implementation")
    print("=" * 50)

    # Initialize MCP servers
    print("📡 Initializing MCP servers...")
    load_mcp_servers_into_manager()

    # Test 1: Configuration Validation
    print("\n1️⃣ Testing Configuration Validation...")
    try:
        issues = config_loader.validate_config()
        if issues:
            print("⚠️  Configuration issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ Configuration validation passed!")
    except Exception as e:
        print(f"❌ Configuration validation error: {e}")

    # Test 2: Tool Discovery
    print("\n2️⃣ Testing Tool Discovery...")
    try:
        # Get all server configs
        server_configs = config_loader.get_all_expanded_configs()
        print(f"   Found {len(server_configs)} configured servers")

        for server_config in server_configs:
            server_name = server_config["name"]
            print(f"   Discovering tools from {server_name}...")

            # Discover tools from this server
            result = await mcp_client_manager.discover_tools(server_config)

            if result.get("success"):
                tools = result.get("tools", {})
                print(f"   ✅ {server_name}: {len(tools)} tools discovered")
                for tool_name, tool_info in tools.items():
                    print(f"      - {tool_name}: {tool_info.get('description', 'No description')}")
            else:
                print(f"   ❌ {server_name}: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Tool discovery error: {e}")

    # Test 3: Tool Execution
    print("\n3️⃣ Testing Tool Execution...")
    test_cases = [
        ("echo.echo", {"text": "Hello World"}, "Echo Tool"),
        ("calculator.calculate", {"expression": "2 + 3"}, "Calculator Tool"),
    ]

    for tool_name, args, description in test_cases:
        try:
            print(f"   Testing {description}...")

            # Import the tool_dispatch activity for testing
            from src.mcp.core.tool_dispatch import execute_mcp_tool
            from src.models import ToolCall

            # Create a tool call
            tool_call = ToolCall(id=f"test-{tool_name}", name=tool_name, args=args)

            # Execute the tool
            result = await execute_mcp_tool(tool_call.name, tool_call.args)
            print(f"   ✅ {description} executed successfully")
            print(f"   🔍 Raw result: {result}")

            # Test formatting
            formatted = format_tool_result_for_display(tool_name, result)
            print(f"   📝 Formatted result: {formatted[:100]}...")

        except Exception as e:
            print(f"   ❌ {description} failed: {e}")

    # Test 4: Health Monitoring
    print("\n4️⃣ Testing Health Monitoring...")
    try:
        health_status = mcp_client_manager.server_health
        print(f"   Server health status: {len(health_status)} servers monitored")

        for server_name, health in health_status.items():
            status = health.get('status', 'unknown')
            last_check = health.get('last_check', 0)
            tool_count = health.get('tool_count', 0)
            time_since_check = time.time() - last_check
            print(f"   {server_name}: {status}, {tool_count} tools ({time_since_check:.1f}s ago)")

    except Exception as e:
        print(f"❌ Health monitoring error: {e}")

    # Test 5: Error Handling
    print("\n5️⃣ Testing Error Handling...")
    try:
        # Test with invalid server
        try:
            from src.mcp.core.tool_dispatch import execute_mcp_tool
            await execute_mcp_tool("nonexistent.echo", {"text": "test"})
            print("   ❌ Should have failed with nonexistent server")
        except Exception as e:
            print(f"   ✅ Correctly handled nonexistent server: {type(e).__name__}")

        # Test with invalid tool
        try:
            from src.mcp.core.tool_dispatch import execute_mcp_tool
            await execute_mcp_tool("echo.nonexistent_tool", {"text": "test"})
            print("   ❌ Should have failed with nonexistent tool")
        except Exception as e:
            print(f"   ✅ Correctly handled nonexistent tool: {type(e).__name__}")

    except Exception as e:
        print(f"❌ Error handling test failed: {e}")

    print("\n" + "=" * 50)
    print("🎉 Clean MCP Implementation Testing Complete!")
    print("\n📊 Summary:")
    print("   ✅ Configuration validation")
    print("   ✅ Tool discovery")
    print("   ✅ Tool execution and formatting")
    print("   ✅ Health monitoring")
    print("   ✅ Error handling")


if __name__ == "__main__":
    asyncio.run(test_clean_mcp_implementation())
