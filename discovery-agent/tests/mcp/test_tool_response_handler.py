#!/usr/bin/env python3
"""
Test script for the enhanced tool response handler
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_tool_response_handler():
    """Test the tool response handler functionality"""
    print("🛠️ Testing Tool Response Handler")
    print("=" * 50)

    try:
        from src.activities.tool_response_handler import tool_response_handler

        # Test 1: Tool call detection
        print("🔍 Testing tool call detection...")

        # Test different formats
        test_cases = [
            '{"tool_call": "weather_api", "parameters": {"location": "New York City"}}',
            '{"tool_call": {"tool_name": "weather_forecast", "parameters": {"location": "New York City", "days": 3}}}',
            '{"_tool_request": {"name": "echo.echo", "args": {"text": "hello"}}}',
            'Not a tool call',  # Should return None
        ]

        for i, test_case in enumerate(test_cases, 1):
            result = tool_response_handler.detect_tool_call(test_case)
            print(f"   Test {i}: {'✅ Detected' if result else '❌ Not detected'} - {test_case[:50]}...")

        # Test 2: Tool execution
        print("\n⚡ Testing tool execution...")

        # Test echo tool
        result = await tool_response_handler.execute_tool_call(
            "test-1", "echo.echo", {"text": "Hello from test!"}
        )
        print(f"   Echo tool: {'✅ Success' if result.success else '❌ Failed'}")
        if result.success:
            print(f"   Result: {result.result}")

        # Test calculator tool
        result = await tool_response_handler.execute_tool_call(
            "test-2", "calculator.calculate", {"expression": "10 + 5"}
        )
        print(f"   Calculator tool: {'✅ Success' if result.success else '❌ Failed'}")
        if result.success:
            print(f"   Result: {result.result}")

        # Test non-existent tool
        result = await tool_response_handler.execute_tool_call(
            "test-3", "nonexistent.tool", {"param": "value"}
        )
        print(f"   Non-existent tool: {'✅ Handled gracefully' if not result.success else '❌ Should have failed'}")
        if not result.success:
            print(f"   Error: {result.error}")

        # Test 3: Response formatting
        print("\n📝 Testing response formatting...")

        success_result = await tool_response_handler.execute_tool_call(
            "test-4", "echo.echo", {"text": "Format test"}
        )
        formatted = tool_response_handler.format_result_for_agent(success_result)
        print(f"   Formatted success: {formatted}")

        print("\n🎉 Tool Response Handler Test Complete!")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"❌ Tool Response Handler Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    success = asyncio.run(test_tool_response_handler())
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
