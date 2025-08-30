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
from typing import Any, Dict

import requests


def start_session(api: str, goal: str = "Chat via CLI") -> str:
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


def end_chat(_: str, __: str) -> None:
    # No explicit end endpoint; ignore
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI chat with Discovery Agent")
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
        end_chat(api, wid)
        print("\nChat ended.")


if __name__ == "__main__":
    main()
