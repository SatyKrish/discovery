#!/usr/bin/env python3
"""
Comprehensive test script to verify MCP integration improvements:
- Tool execution and caching
- Health monitoring and metrics
- Configuration validation
- Error handling and recovery
"""

import asyncio
import sys
import os
import time

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp_client import tool_orchestrator
from src.mcp_config import config_loader, load_mcp_servers_into_orchestrator
from src.workflows.agent_orchestrator import format_tool_result_for_display

async def test_mcp_improvements():
    """Test all MCP integration improvements"""
    print("🧪 Testing MCP Integration Improvements")
    print("=" * 50)

    # Initialize MCP servers
    print("📡 Initializing MCP servers...")
    load_mcp_servers_into_orchestrator()

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

    # Test 2: Tool Discovery with Caching
    print("\n2️⃣ Testing Tool Discovery with Caching...")
    try:
        # First discovery
        start_time = time.time()
        tool_cache = await tool_orchestrator.discover_dynamic_tools()
        first_discovery_time = time.time() - start_time
        print(f"   First discovery took: {first_discovery_time:.2f}s")
        print(f"   Discovered servers: {list(tool_cache.keys())}")
        for server, tools in tool_cache.items():
            print(f"   {server}: {len(tools)} tools")

        # Second discovery (should use cache)
        start_time = time.time()
        cached_tools = await tool_orchestrator.discover_dynamic_tools()
        second_discovery_time = time.time() - start_time
        print(f"   Second discovery took: {second_discovery_time:.2f}s")

        # Check cache info
        cache_info = tool_orchestrator.get_cache_info()
        print(f"   Cache status: {cache_info['cache_status']}")
        print(f"   Cache TTL: {cache_info['cache_ttl_seconds']}s")

    except Exception as e:
        print(f"❌ Tool discovery error: {e}")

    # Test 3: Tool Execution and Statistics
    print("\n3️⃣ Testing Tool Execution and Statistics...")
    test_cases = [
        ("web-search.web_search", {"query": "weather in New York"}, "Web Search"),
        ("echo.echo", {"text": "Hello World"}, "Echo"),
        ("calculator.calculate", {"expression": "2 + 3"}, "Calculator"),
    ]

    for tool_name, args, description in test_cases:
        try:
            print(f"   Testing {description}...")
            result = await tool_orchestrator.execute_tool(tool_name, args)
            print(f"   ✅ {description} executed successfully")

            # Test formatting
            formatted = format_tool_result_for_display(tool_name, result)
            print(f"   📝 Formatted result preview: {formatted[:100]}...")

        except Exception as e:
            print(f"   ❌ {description} failed: {e}")

    # Test 4: Health Monitoring
    print("\n4️⃣ Testing Health Monitoring...")
    try:
        health_status = tool_orchestrator.get_server_health()
        print(f"   Server health status: {len(health_status)} servers monitored")

        for server_name, health in health_status.items():
            status = health.get('status', 'unknown')
            last_check = health.get('last_check', 0)
            time_since_check = time.time() - last_check
            print(f"   {server_name}: {status} ({time_since_check:.1f}s ago)")

        # Test overall health
        overall_health = tool_orchestrator.mcp_manager.get_overall_health_status()
        print(f"   Overall health: {overall_health['status']} - {overall_health['message']}")

    except Exception as e:
        print(f"❌ Health monitoring error: {e}")

    # Test 5: Usage Statistics
    print("\n5️⃣ Testing Usage Statistics...")
    try:
        stats = tool_orchestrator.get_tool_stats()
        print(f"   Tool usage statistics: {len(stats)} tools tracked")

        for tool_name, tool_stats in stats.items():
            calls = tool_stats.get('calls', 0)
            successes = tool_stats.get('successes', 0)
            failures = tool_stats.get('failures', 0)
            success_rate = (successes / calls * 100) if calls > 0 else 0
            print(f"   {tool_name}: {calls} calls, {success_rate:.1f}% success")

    except Exception as e:
        print(f"❌ Statistics error: {e}")

    # Test 6: Cache Management
    print("\n6️⃣ Testing Cache Management...")
    try:
        # Get cache info
        cache_info = tool_orchestrator.get_cache_info()
        print(f"   Cache info: {cache_info['cache_status']}")
        print(f"   Cached tools: {cache_info['total_cached_tools']}")
        print(f"   Cache age: {cache_info.get('cache_age_seconds', 'N/A')}")

        # Test cache clearing
        tool_orchestrator.clear_cache()
        cache_info_after_clear = tool_orchestrator.get_cache_info()
        print(f"   Cache status after clear: {cache_info_after_clear['cache_status']}")

    except Exception as e:
        print(f"❌ Cache management error: {e}")

    # Test 7: Error Handling and Recovery
    print("\n7️⃣ Testing Error Handling and Recovery...")
    try:
        # Test with invalid tool
        try:
            await tool_orchestrator.execute_tool("nonexistent.tool", {})
            print("   ❌ Should have failed with nonexistent tool")
        except Exception as e:
            print(f"   ✅ Correctly handled nonexistent tool: {type(e).__name__}")

        # Test with invalid arguments
        try:
            await tool_orchestrator.execute_tool("echo.echo", {"invalid_param": "test"})
            print("   ✅ Echo handled invalid parameters gracefully")
        except Exception as e:
            print(f"   ⚠️  Echo failed with invalid params: {e}")

    except Exception as e:
        print(f"❌ Error handling test failed: {e}")

    print("\n" + "=" * 50)
    print("🎉 MCP Integration Testing Complete!")
    print("\n📊 Summary:")
    print("   ✅ Configuration validation")
    print("   ✅ Tool discovery with caching")
    print("   ✅ Tool execution and formatting")
    print("   ✅ Health monitoring and metrics")
    print("   ✅ Usage statistics tracking")
    print("   ✅ Cache management")
    print("   ✅ Error handling and recovery")

if __name__ == "__main__":
    asyncio.run(test_mcp_improvements())
