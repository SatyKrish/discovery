#!/usr/bin/env python
"""Simple CLI to interact with the Discovery Agent API endpoints.

Usage:
    python -m src.cli_chat --api http://localhost:8080

The script starts a new workflow and lets the user chat with it from the
terminal. Press Ctrl+C to exit.
"""

import argparse
import os
import time
import warnings
from typing import Any, Dict

import requests


def start_session(api: str, goal: str = "Have a helpful conversation") -> str:
    res = requests.post(f"{api}/sessions", json={"goal": goal})
    res.raise_for_status()
    return res.json().get("workflow_id")


def get_status(api: str, wid: str) -> Dict[str, Any]:
    res = requests.get(f"{api}/sessions/{wid}/status")
    res.raise_for_status()
    return res.json()


def send_prompt(api: str, wid: str, prompt: str) -> None:
    res = requests.post(f"{api}/sessions/{wid}/messages", json={"text": prompt})
    res.raise_for_status()

def end_conversation(api: str, wid: str) -> None:
    """Send signal to end the conversation and terminate workflow"""
    try:
        res = requests.post(f"{api}/sessions/{wid}/end")
        res.raise_for_status()
    except Exception:
        # Ignore errors when ending conversation
        pass


def end_chat(api: str, wid: str) -> None:
    # Signal the workflow to end the conversation
    try:
        res = requests.post(f"{api}/sessions/{wid}/end")
        res.raise_for_status()
        print("Conversation ended.")
    except Exception as e:
        print(f"Warning: Could not end conversation properly: {e}")


def _is_final_response(response_data: Dict[str, Any]) -> bool:
    """Check if the response indicates completion"""
    if not response_data or "response" not in response_data:
        return False

    response = response_data["response"]
    if not response:
        return False

    # Check response type and status
    response_type = response.get("type", "")
    status = response.get("status", "")
    client_hints = response.get("client_hints", {})

    # Check for completion indicators in client hints
    completion_indicator = client_hints.get("completion_indicator", "")

    if completion_indicator in ["conversation_complete", "error"]:
        return True

    # Check for specific response types that indicate completion
    if response_type == "completion" and status == "completed":
        return True

    # Check for tool completion without next actions
    if response_type == "tool_result" and status == "success":
        next_actions = client_hints.get("next_actions", [])
        return len(next_actions) == 0

    return False


def _is_processing_response(response_data: Dict[str, Any]) -> bool:
    """Check if the response indicates processing is ongoing"""
    if not response_data or "response" not in response_data:
        return False

    response = response_data["response"]
    if not response:
        return False

    # Check response type and status
    response_type = response.get("type", "")
    status = response.get("status", "")
    client_hints = response.get("client_hints", {})

    # Check for processing indicators
    if status == "pending":
        return True

    if response_type == "status" and "waiting" in response.get("content", "").lower():
        return True

    # Tool results with next actions are still processing
    if response_type == "tool_result" and status == "success":
        next_actions = client_hints.get("next_actions", [])
        return len(next_actions) > 0

    return False


def _extract_response_content(response_data: Dict[str, Any]) -> str:
    """Extract the display content from the response envelope"""
    if not response_data or "response" not in response_data:
        return ""

    response = response_data["response"]
    if not response:
        return ""

    content = response.get("content", "")

    # For tool results, use the formatted display if available
    if response.get("type") == "tool_result" and isinstance(content, dict):
        return content.get("formatted_display", str(content))

    return str(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat CLI with Discovery Agent")
    parser.add_argument("--api", default=os.environ.get("DISCOVERY_API_URL", "http://localhost:8080"),
                        help="Base URL of FastAPI service")
    args = parser.parse_args()
    api = args.api.rstrip("/")

    wid = start_session(api)
    print(f"Session started: {wid}")
    last_turns = 0
    try:
        while True:
            prompt = input("You: ")
            if not prompt:
                continue
            send_prompt(api, wid, prompt)
            # Poll for turns increase, then wait for actual response
            while True:
                time.sleep(1)
                status = get_status(api, wid)
                turns = int(status.get("turns", 0))
                if turns > last_turns:
                    # Turns increased, now wait for the actual response
                    print("Agent: (generating response...)")
                    response_start = time.time()
                    while True:
                        response_content = _extract_response_content(status)
                        if response_content:
                            # Enhanced response detection using new format
                            if _is_final_response(status):
                                print(f"Agent: {response_content}")
                                break
                            elif _is_processing_response(status):
                                # Continue polling for actual result
                                pass
                            else:
                                # Normal response
                                print(f"Agent: {response_content}")
                                break

                        # Timeout after 30 seconds
                        if time.time() - response_start > 30:
                            print("Agent: (response timeout - no response available)")
                            break
                        time.sleep(0.5)
                        status = get_status(api, wid)
                    last_turns = turns
                    break
    except KeyboardInterrupt:
        pass
    finally:
        # Send end conversation signal to terminate workflow
        end_conversation(api, wid)
        end_chat(api, wid)
        print("\nChat ended.")


if __name__ == "__main__":
    main()
