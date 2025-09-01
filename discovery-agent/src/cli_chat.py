#!/usr/bin/env python
"""Simple CLI to interact with the Discovery Agent API endpoints.

Usage:
    python -m src.cli_chat --api http://localhost:8080

Interactive REPL (default):
    python -m src.cli_chat --api http://localhost:8080

One-shot message:
    python -m src.cli_chat --api http://localhost:8080 -m "Hello world!"

Commands in REPL:
    :quit, :q, /quit, /q  - Exit gracefully

The script starts a new session and lets the user chat with it from the
terminal. Press Ctrl+C to exit or use :quit command.
"""

import argparse
import json
import os
import time
import warnings
from typing import Any, Dict

import requests


def pretty(obj: Any) -> str:
    """Pretty-print an object as JSON"""
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except Exception:
        return str(obj)


class DiscoveryAgentClient:
    """Client for interacting with the Discovery Agent API"""

    def __init__(self, base_url: str) -> None:
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url

    def start_session(self, goal: str = "Have a helpful conversation") -> str:
        res = requests.post(f"{self.base_url}/sessions", json={"goal": goal})
        res.raise_for_status()
        return res.json().get("workflow_id")

    def get_status(self, workflow_id: str) -> Dict[str, Any]:
        res = requests.get(f"{self.base_url}/sessions/{workflow_id}/status")
        if res.status_code == 404:
            # Worker unavailable or workflow not found; return empty status
            return {}
        res.raise_for_status()
        try:
            return res.json() or {}
        except Exception:
            return {}

    def send_prompt(self, workflow_id: str, prompt: str) -> None:
        res = requests.post(f"{self.base_url}/sessions/{workflow_id}/messages", json={"text": prompt})
        res.raise_for_status()

    def end_conversation(self, workflow_id: str) -> None:
        """Send signal to end the conversation and terminate workflow"""
        try:
            res = requests.post(f"{self.base_url}/sessions/{workflow_id}/end")
            res.raise_for_status()
        except Exception:
            # Ignore errors when ending conversation
            pass

    def end_chat(self, workflow_id: str) -> None:
        # Signal the workflow to end the conversation
        try:
            res = requests.post(f"{self.base_url}/sessions/{workflow_id}/end")
            res.raise_for_status()
            print("Conversation ended.")
        except Exception as e:
            print(f"Warning: Could not end conversation properly: {e}")


# Backward compatibility functions
def start_session(api: str, goal: str = "Have a helpful conversation") -> str:
    client = DiscoveryAgentClient(api)
    return client.start_session(goal)


def get_status(api: str, wid: str) -> Dict[str, Any]:
    client = DiscoveryAgentClient(api)
    return client.get_status(wid)


def send_prompt(api: str, wid: str, prompt: str) -> None:
    client = DiscoveryAgentClient(api)
    return client.send_prompt(wid, prompt)


def end_conversation(api: str, wid: str) -> None:
    client = DiscoveryAgentClient(api)
    return client.end_conversation(wid)


def end_chat(api: str, wid: str) -> None:
    client = DiscoveryAgentClient(api)
    return client.end_chat(wid)


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
    """Extract the display content from the response envelope with robust fallbacks"""
    if not isinstance(response_data, dict):
        return str(response_data)

    if "response" not in response_data:
        return str(response_data)

    response = response_data["response"]
    if not response:
        return ""

    # Try multiple possible content keys with fallbacks
    content = (response.get("content") or
               response.get("text") or
               response.get("message") or
               "")

    # Handle different content types
    if content is None:
        return ""
    elif isinstance(content, dict):
        # For dict content, try formatted_display first, then pretty print
        if response.get("type") == "tool_result":
            return content.get("formatted_display", content.get("text", pretty(content)))
        else:
            return content.get("text", content.get("message", pretty(content)))
    elif isinstance(content, list):
        # For list content, join items
        return "\n".join(str(item) for item in content)
    elif isinstance(content, str):
        return content
    else:
        return str(content)


def run_one_shot(api: str, message: str) -> None:
    """Send a single message and print the response, then exit"""
    wid = start_session(api)
    print(f"Session started: {wid}")

    send_prompt(api, wid, message)
    print("Agent: (generating response...)")

    # Poll for response
    response_start = time.time()
    last_turns = 0

    while True:
        time.sleep(0.5)
        status = get_status(api, wid)
        turns = int(status.get("turns", 0))

        if turns > last_turns:
            # Turns increased, wait for actual response
            while True:
                response_content = _extract_response_content(status)
                if response_content:
                    if _is_final_response(status):
                        print(f"Agent: {response_content}")
                        end_conversation(api, wid)
                        return
                    elif not _is_processing_response(status):
                        print(f"Agent: {response_content}")
                        end_conversation(api, wid)
                        return

                # Timeout after 30 seconds
                if time.time() - response_start > 30:
                    print("Agent: (response timeout - no response available)")
                    end_conversation(api, wid)
                    return

                time.sleep(0.5)
                status = get_status(api, wid)
            last_turns = turns

        # Timeout for initial response
        if time.time() - response_start > 30:
            print("Agent: (no response received)")
            end_conversation(api, wid)
            return


def run_repl(api: str) -> None:
    """Run the interactive REPL"""
    wid = start_session(api)
    print(f"Session started: {wid}")
    last_turns = 0

    try:
        while True:
            prompt = input("You: ")
            if not prompt:
                continue

            # Check for quit command
            if prompt.strip().lower() in [":quit", ":q", "/quit", "/q"]:
                print("Goodbye!")
                break

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat CLI with Discovery Agent")
    parser.add_argument("--api", default=os.environ.get("DISCOVERY_API_URL", "http://localhost:8080"),
                        help="Base URL of FastAPI service")
    parser.add_argument("-m", "--message",
                        help="Send a single message and exit (one-shot mode)")
    args = parser.parse_args()
    api = args.api.rstrip("/")

    if args.message:
        run_one_shot(api, args.message)
    else:
        run_repl(api)


if __name__ == "__main__":
    main()
