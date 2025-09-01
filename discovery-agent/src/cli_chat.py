#!/usr/bin/env python
import argparse
import json
import os
import time
from typing import Optional

import requests


class AgentAPI:
    def __init__(self, base_url: str, workflow_id: Optional[str] = None):
        self.base = base_url.rstrip("/")
        self.workflow_id = workflow_id

    def send_sync(self, text: str) -> dict:
        payload = {"text": text}
        if self.workflow_id:
            payload["workflow_id"] = self.workflow_id
        r = requests.post(f"{self.base}/chat/send-sync", json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        self.workflow_id = data.get("workflow_id", self.workflow_id)
        return data

    def confirm(self, tool_call_id: str, approved: bool = True, args: Optional[dict] = None) -> None:
        if not self.workflow_id:
            raise RuntimeError("No workflow_id")
        payload = {
            "workflow_id": self.workflow_id,
            "tool_call_id": tool_call_id,
            "approved": bool(approved),
            "args": args or None,
        }
        r = requests.post(f"{self.base}/chat/confirm", json=payload, timeout=60)
        r.raise_for_status()

    def wait_sync(self) -> dict:
        if not self.workflow_id:
            raise RuntimeError("No workflow_id")
        r = requests.post(f"{self.base}/chat/wait-sync", params={"workflow_id": self.workflow_id}, timeout=300)
        r.raise_for_status()
        return r.json()

    def history(self) -> list[dict]:
        if not self.workflow_id:
            return []
        r = requests.get(f"{self.base}/sessions/{self.workflow_id}/history", timeout=30)
        if r.status_code != 200:
            return []
        return r.json()

    def end(self):
        if not self.workflow_id:
            return
        try:
            requests.post(f"{self.base}/chat/end", json={"workflow_id": self.workflow_id}, timeout=10)
        except Exception:
            pass


def run_repl(api_base: str, workflow_id: Optional[str]):
    api = AgentAPI(api_base, workflow_id)
    print(f"Connected. workflow_id={workflow_id or '(created on first turn)'}")
    try:
        while True:
            user = input("You: ").strip()
            if not user:
                continue
            if user.lower() in {":q", "/q", ":quit", "/quit"}:
                print("Goodbye!"); break
            if user.lower().startswith(":approve"):
                # :approve <tool_call_id> [<json_args>]
                parts = user.split(" ", 2)
                if len(parts) < 2:
                    print("usage: :approve <tool_call_id> [<json_args>]")
                    continue
                tool_call_id = parts[1]
                args = None
                if len(parts) == 3:
                    try:
                        args = json.loads(parts[2])
                    except Exception as e:
                        print(f"Invalid JSON args: {e}")
                        continue
                try:
                    print("Agent: (approving...)")
                    api.confirm(tool_call_id, True, args)
                    print("Agent: (waiting for reply...)")
                    result = api.wait_sync()
                    print(f"Agent: {result.get('assistant',{}).get('content','')}")
                except Exception as e:
                    print(f"Agent: (error) {e}")
                continue

            print("Agent: (thinking...)")
            try:
                resp = api.send_sync(user)
            except Exception as e:
                print(f"Agent: (error) {e}")
                continue

            assistant = resp.get("assistant")
            pending = resp.get("pending_tool")

            if assistant:
                print(f"Agent: {assistant.get('content','').strip()}")
            elif pending:
                tool_call_id = pending.get("id")
                name = pending.get("name")
                print(f"Agent: Tool '{name}' requires approval.")
                print(f"        Run :approve {tool_call_id} [json_args]")
            else:
                print("Agent: (no reply)")

    except KeyboardInterrupt:
        pass
    finally:
        api.end()
        print("\nChat ended.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Chat CLI (sync Updates)")
    p.add_argument("--api", default=os.environ.get("DISCOVERY_API_URL", "http://localhost:8080"))
    p.add_argument("--workflow-id", default=None)
    args = p.parse_args()
    run_repl(args.api, args.workflow_id)
