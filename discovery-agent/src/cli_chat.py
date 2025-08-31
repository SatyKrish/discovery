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

# Suppress MCP pydantic warnings
warnings.filterwarnings("ignore", message="Field name \"schema\" in \"ToolSpec\" shadows an attribute")


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


def _is_final_response(output_text: str) -> bool:
    """Check if the response indicates completion"""
    if not output_text:
        return False
    # Check for completion indicators
    completion_indicators = [
        "conversation ended",
        "chat ended",
        "goodbye",
        "farewell",
        "completed successfully",
        "tool completed",
        "search results for",
        "calculation result",
        "echo:"
    ]
    return any(indicator in output_text.lower() for indicator in completion_indicators)


def _is_processing_response(output_text: str) -> bool:
    """Check if the response indicates processing is ongoing"""
    if not output_text:
        return False
    # Check for processing indicators
    processing_indicators = [
        "generating",
        "processing",
        "thinking",
        "working",
        "calling a",
        "calling tool",
        "executing",
        "running",
        "tool '",
        "completed successfully"  # This might be part of a processing message
    ]

    # Don't treat tool completion messages as processing
    if "completed successfully" in output_text.lower() and any(indicator in output_text.lower() for indicator in [
        "search results for",
        "calculation result",
        "echo:",
        "no results found"
    ]):
        return False

    return any(indicator in output_text.lower() for indicator in processing_indicators)


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
                        output_text = status.get("output_text")
                        if output_text:
                            # Enhanced response detection
                            if _is_final_response(output_text):
                                print(f"Agent: {output_text}")
                                break
                            elif _is_processing_response(output_text):
                                # Continue polling for actual result
                                pass
                            else:
                                # Normal response
                                print(f"Agent: {output_text}")
                                break

                        # Timeout after 30 seconds
                        if time.time() - response_start > 30:
                            print("Agent: (response timeout - no text available)")
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
