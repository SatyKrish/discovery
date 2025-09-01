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
import hashlib
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
    r = (response_data or {}).get("response") or {}
    t = r.get("type", "")
    status = r.get("status", "")
    hints = r.get("client_hints", {}) or {}

    if hints.get("completion_indicator") in {"conversation_complete", "workflow_completed", "error"}:
        return True

    # Treat only real assistant completions as final
    return t in ("completion", "assistant_message") and status in ("completed", "done", "success")


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


def _response_fingerprint(resp: Dict[str, Any]) -> str:
    """Create a fingerprint of the response to detect changes"""
    try:
        # Remove volatile fields that change on each status query
        sanitized = dict(resp or {})
        if "timestamp" in sanitized:
            sanitized = dict(sanitized)
            sanitized.pop("timestamp", None)
        return json.dumps(sanitized, sort_keys=True, ensure_ascii=False)
    except Exception:
        return str(resp)


def _looks_displayable(resp: Dict[str, Any]) -> bool:
    """Return True if this looks like something we should show to a user."""
    if not isinstance(resp, dict):
        return False
    t = (resp.get("type") or "").lower()

    # Hide known-noise types unless they contain real text to show
    if t in {"status", "tool_request", "tool_call"}:
        return False

    content = resp.get("content")
    textish = None
    if isinstance(content, dict):
        textish = content.get("formatted_display") or content.get("text") or content.get("message")
    elif isinstance(content, str):
        textish = content
    elif isinstance(content, list):
        textish = "\n".join([str(x) for x in content if x])

    # If there's actual text-ish content, show it
    if textish and str(textish).strip():
        return True

    # Otherwise only show classic assistant/completion types
    if t in {"completion", "assistant_message", "message"}:
        return True

    return False


def _extract_text_for_display(resp_data: Dict[str, Any]) -> str:
    """Extract text for display from response data"""
    resp = (resp_data or {}).get("response") or {}
    content = resp.get("content") or resp.get("text") or resp.get("message") or ""
    if isinstance(content, dict):
        return content.get("formatted_display") or content.get("text") or content.get("message") or pretty(content)
    if isinstance(content, list):
        return "\n".join(str(x) for x in content)
    if isinstance(content, str):
        return content
    return str(content)


def _is_workflow_done(resp_data: Dict[str, Any]) -> bool:
    """Check if the workflow/conversation is complete"""
    r = (resp_data or {}).get("response") or {}
    hints = r.get("client_hints") or {}
    if hints.get("completion_indicator") in {"conversation_complete", "workflow_completed", "error"}:
        return True
    t = (r.get("type") or "").lower()
    st = (r.get("status") or "").lower()
    return t in {"completion", "assistant_message"} and st in {"completed", "done", "success"}


def run_one_shot(api: str, message: str) -> None:
    """Send a single message and print the response, then exit"""
    wid = start_session(api)
    print(f"Session started: {wid}")

    send_prompt(api, wid, message)
    print("Agent: (generating response...)")

    response_start = time.time()
    last_seen_fp = None
    # Optional: if your backend is slow to populate, give it a short grace
    time.sleep(0.25)

    while True:
        status = get_status(api, wid)
        resp = (status or {}).get("response") or {}
        fp = _response_fingerprint(resp)

        # Debug output if requested
        if os.environ.get("CLI_DEBUG_STATUS") == "1":
            print(pretty({"turns": status.get("turns"),
                          "response_keys": list(((status.get("response") or {}).keys())),
                          "response_type": (status.get("response") or {}).get("type"),
                          "response_status": (status.get("response") or {}).get("status"),
                          "role": (status.get("response") or {}).get("role") or (status.get("response") or {}).get("author") or (status.get("response") or {}).get("speaker"),
                         }))

        # Show only if it looks like new AND displayable
        if fp and fp != last_seen_fp and _looks_displayable(resp):
            text = _extract_text_for_display(status).strip()
            if text:
                print(f"Agent: {text}")
                # If the workflow says it's done, stop waiting; otherwise stop after first displayable message
                # (If you expect multi-chunk streaming via status, remove the 'break' and keep polling until done)
                break
            last_seen_fp = fp

        # Timeout
        if time.time() - response_start > 30:
            print("Agent: (response timeout - no response available)")
            break

        time.sleep(0.5)

    end_conversation(api, wid)


def run_repl(api: str) -> None:
    """Run the interactive REPL"""
    wid = start_session(api)
    print(f"Session started: {wid}")

    try:
        # Keep a session-wide fingerprint of the last response we've shown
        # so we don't reprint the previous turn's answer after each prompt.
        session_last_seen_fp = None
        while True:
            prompt = input("You: ")
            if not prompt:
                continue

            # Check for quit command
            if prompt.strip().lower() in [":quit", ":q", "/quit", "/q"]:
                print("Goodbye!")
                break

            send_prompt(api, wid, prompt)

            print("Agent: (generating response...)")
            response_start = time.time()
            # Optional: if your backend is slow to populate, give it a short grace
            time.sleep(0.25)

            while True:
                status = get_status(api, wid)
                resp = (status or {}).get("response") or {}
                fp = _response_fingerprint(resp)

                # Show only if it looks like new AND displayable
                if fp and fp != session_last_seen_fp and _looks_displayable(resp):
                    text = _extract_text_for_display(status).strip()
                    if text:
                        print(f"Agent: {text}")
                        # Update session-wide fingerprint so we don't show this again
                        session_last_seen_fp = fp
                        # If the workflow says it's done, stop waiting; otherwise stop after first displayable message
                        # (If you expect multi-chunk streaming via status, remove the 'break' and keep polling until done)
                        break

                # Timeout
                if time.time() - response_start > 30:
                    print("Agent: (response timeout - no response available)")
                    break

                time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        # Send end conversation signal to terminate workflow
        end_conversation(api, wid)
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
