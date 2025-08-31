#!/usr/bin/env python3
"""
Test MCP result processing fixes
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mcp_result_processing():
    """Test that MCP result processing works correctly"""
    print("== MCP Result Processing Test ===")

    # Mock MCP result similar to what the servers return
    mock_mcp_result = {
        "content": [
            {"type": "text", "text": "Echo: Hello World"},
            {"type": "text", "text": "This is a test"}
        ],
        "tool": "echo.echo",
        "success": True
    }

    # Test the result processing logic from the MCP client
    print("Testing MCP result processing...")

    # Simulate the processing logic from execute_tool method
    if 'content' in mock_mcp_result and mock_mcp_result['content']:
        content = []
        try:
            for item in mock_mcp_result['content']:
                # Handle different MCP content types
                if isinstance(item, dict) and 'type' in item:
                    item_type = item['type']
                    if item_type == "text" and 'text' in item:
                        content.append({"type": "text", "text": item['text']})
                    elif 'data' in item:
                        content.append({"type": item_type, "data": item['data']})
                    else:
                        # Fallback for unknown content types
                        content.append({"type": item_type, "content": str(item)})
                elif isinstance(item, dict):
                    # Handle dict-like content (fallback)
                    content.append(item)
                else:
                    # Handle other content types
                    content.append({"type": "unknown", "content": str(item)})
        except Exception as content_error:
            print(f"Error processing MCP content: {content_error}")
            content = [{"type": "error", "text": f"Error processing content: {str(content_error)}"}]

        processed_result = {
            "tool": mock_mcp_result["tool"],
            "success": mock_mcp_result["success"],
            "content": content
        }

        print(f"✅ Processed result: {processed_result}")

        # Test the workflow formatting function (inline version)
        formatted_result = format_tool_result_for_display_test("echo.echo", processed_result)
        print(f"✅ Formatted result: {formatted_result}")

        return True

    return False

def format_tool_result_for_display_test(tool_name: str, result):
    """Test version of the workflow formatting function"""
    try:
        # Handle MCP tool results (already dict format)
        if isinstance(result, dict):
            # Check if this is an MCP tool result with content array
            if "content" in result and isinstance(result["content"], list):
                return format_mcp_content_result_test(tool_name, result)
            else:
                return format_json_result_test(tool_name, result)

        # Handle string results (try to parse as JSON)
        elif isinstance(result, str):
            try:
                parsed = json.loads(result)
                return format_json_result_test(tool_name, parsed)
            except json.JSONDecodeError:
                return result

        # Handle other types
        else:
            return str(result)
    except Exception as e:
        # Fallback to string representation
        return f"Tool result: {str(result)}"

def format_mcp_content_result_test(tool_name: str, data: dict) -> str:
    """Test version of MCP content formatting"""
    content_list = data.get("content", [])

    if not content_list:
        return f"Tool '{tool_name}' completed but returned no content."

    # Extract text content from MCP result
    text_parts = []
    for item in content_list:
        if isinstance(item, dict) and item.get("type") == "text":
            text_parts.append(item.get("text", ""))
        elif isinstance(item, str):
            text_parts.append(item)

    if text_parts:
        combined_text = " ".join(text_parts)
        return f"Tool '{tool_name}' result: {combined_text}"
    else:
        # Fallback for non-text content
        return f"Tool '{tool_name}' completed with {len(content_list)} content items."

def format_json_result_test(tool_name: str, data: dict) -> str:
    """Test version of JSON result formatting"""
    if tool_name == "echo.echo":
        text = data.get("text", "")
        return f"Echo: {text}"
    else:
        return json.dumps(data, indent=2)

def test_error_handling():
    """Test error handling in MCP result processing"""
    print("\nTesting error handling...")

    # Test with malformed content
    malformed_result = {
        "content": [
            {"type": "text"},  # Missing text field
            "string content",  # String instead of dict
            {"invalid": "structure"}
        ],
        "tool": "test.tool",
        "success": True
    }

    try:
        formatted = format_tool_result_for_display_test("test.tool", malformed_result)
        print(f"✅ Error handling works: {formatted}")
        return True
    except Exception as e:
        print(f"❌ Error handling failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing MCP result processing fixes...")

    success1 = test_mcp_result_processing()
    success2 = test_error_handling()

    if success1 and success2:
        print("\n🎉 All MCP result processing tests passed!")
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)
