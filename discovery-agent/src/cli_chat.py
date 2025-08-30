#!/usr/bin/env python
"""Simple CLI to interact with the FastAPI DeepAgent endpoints.

Usage:
    python cli_chat.py --api http://localhost:8000

The script starts a new workflow and lets the user chat with it from the
terminal. Press Ctrl+C to exit.
"""

import argparse
import os
import time
from typing import List

import requests


def start_workflow(api: str) -> str:
    res = requests.post(f"{api}/workflow/start", json={})
    res.raise_for_status()
    return res.json()["workflow_id"]


def fetch_history(api: str, wid: str) -> List[dict]:
    res = requests.get(f"{api}/workflow/{wid}/history")
    res.raise_for_status()
    return res.json().get("history", [])


def send_prompt(api: str, wid: str, prompt: str) -> None:
    res = requests.post(f"{api}/workflow/{wid}/prompt", json={"prompt": prompt})
    res.raise_for_status()


def end_chat(api: str, wid: str) -> None:
    try:
        requests.post(f"{api}/workflow/{wid}/end", timeout=2)
    except Exception:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI chat with DeepAgent")
    parser.add_argument("--api", default=os.environ.get("DISCOVERY_API_URL", "http://localhost:8000"),
                        help="Base URL of FastAPI service")
    args = parser.parse_args()
    api = args.api.rstrip("/")

    wid = start_workflow(api)
    print(f"Workflow started: {wid}")
    history_len = 0
    try:
        while True:
            prompt = input("You: ")
            if not prompt:
                continue
            send_prompt(api, wid, prompt)
            # Poll for a new assistant message
            while True:
                time.sleep(1)
                hist = fetch_history(api, wid)
                if len(hist) > history_len + 1:
                    # Expect a pair of messages: user and assistant
                    msg = hist[-1].get("assistant")
                    if msg:
                        print(f"Agent: {msg}")
                    history_len = len(hist)
                    break
    except KeyboardInterrupt:
        pass
    finally:
        end_chat(api, wid)
        print("\nChat ended.")


if __name__ == "__main__":
    main()
