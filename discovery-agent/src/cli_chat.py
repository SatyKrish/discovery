from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, Optional, Tuple, List

import requests


def _mask(s: Optional[str]) -> str:
    if not s or len(s) < 12:
        return "<none>"
    return f"{s[:4]}…{s[-4:]}"


def _print(msg: str = "", end: str = "\n") -> None:
    sys.stdout.write(msg + end)
    sys.stdout.flush()


def _post_json(url: str, payload: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
    resp = requests.post(url, json=payload, timeout=timeout)
    resp.raise_for_status()
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Non-JSON response from {url}: {resp.text[:500]}")


def _get_json(url: str, timeout: float = 30.0) -> Dict[str, Any]:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Non-JSON response from {url}: {resp.text[:500]}")


# -----------------------------
# Result extraction helpers
# -----------------------------

DONE_STATES = {"completed", "succeeded", "done", "finished", "success"}
PENDING_STATES = {
    "queued",
    "running",
    "in_progress",
    "pending",
    "processing",
    "starting",
}


def _extract_status_url(api: str, first_reply: Dict[str, Any], session_id: Optional[str]) -> Optional[str]:
    """
    Try to find a status URL in the server's reply; if not present,
    fall back to commonly used patterns with session/workflow ids.
    """
    # 1) direct hint from server
    if "status_url" in first_reply and isinstance(first_reply["status_url"], str):
        return first_reply["status_url"]

    # 2) id-based hint provided by server
    rid = first_reply.get("response_id") or first_reply.get("run_id") or first_reply.get("id")
    if isinstance(rid, str):
        return f"{api.rstrip('/')}/status/{rid}"

    # 3) fall back to session status if exposed that way
    if session_id:
        return f"{api.rstrip('/')}/sessions/{session_id}/status"

    return None


def _extract_output_text(obj: Dict[str, Any]) -> Optional[str]:
    """
    Be generous with shapes:
      - { "output_text": "..." }
      - { "result": "..."} or nested: { "response": { "output_text": "..." } }
      - { "results": [ { "result": "..."} ] }
      - OpenAI-style choices/content
    """
    # direct
    for key in ("output_text", "final_text", "result", "message", "text"):
        v = obj.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()

    # nested last_message used by discovery-agent
    last = obj.get("last_message")
    if isinstance(last, dict):
        content = last.get("content")
        if isinstance(content, str) and content.strip():
            return content.strip()

    # nested response
    resp = obj.get("response")
    if isinstance(resp, dict):
        v = _extract_output_text(resp)
        if v:
            return v

    # list of results
    results = obj.get("results")
    if isinstance(results, list):
        for r in results:
            if isinstance(r, dict):
                v = _extract_output_text(r)
                if v:
                    return v

    # OpenAI-like
    choices = obj.get("choices")
    if isinstance(choices, list) and choices:
        ch0 = choices[0]
        if isinstance(ch0, dict):
            msg = ch0.get("message") or ch0.get("delta")
            if isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, str):
                    return content.strip()

    # Responses API style aggregated text
    output = obj.get("output")
    if isinstance(output, dict):
        # Sometimes `output_text` sits here
        if isinstance(output.get("output_text"), str):
            return output["output_text"].strip()
    return None


def _extract_state(obj: Dict[str, Any]) -> Optional[str]:
    for k in ("status", "state", "phase"):
        v = obj.get(k)
        if isinstance(v, str):
            return v.lower()
    return None


def _poll_until_done(status_url: str, poll_interval: float = 1.0, timeout: float = 120.0) -> Tuple[Optional[str], Dict[str, Any]]:
    start = time.time()
    last = {}
    while True:
        last = _get_json(status_url, timeout=30.0)
        out = _extract_output_text(last)
        state = _extract_state(last)

        if out and (state in DONE_STATES or state is None):
            return out, last

        if state in DONE_STATES:
            return out, last

        if (time.time() - start) > timeout:
            return out, last

        time.sleep(poll_interval)


# -----------------------------
# CLI
# -----------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description="Simple CLI chat client for Discovery Agent API")
    ap.add_argument("--api", required=True, help="Base URL of the API, e.g. http://localhost:8080")
    ap.add_argument("--session", default=None, help="Existing session id (optional)")
    ap.add_argument("--poll-timeout", type=float, default=180.0, help="Max seconds to poll a status endpoint")
    ap.add_argument("--poll-interval", type=float, default=1.0, help="Polling interval seconds")
    args = ap.parse_args()

    api = args.api.rstrip("/")
    session_id = args.session or f"session-{int(time.time() * 1000)}"
    _print(f"Session started: {session_id}")

    try:
        while True:
            _print("You: ", end="")
            user = sys.stdin.readline()
            if not user:
                break
            user = user.rstrip("\n")
            if not user:
                continue
            if user.lower() in {"exit", "quit", ":q"}:
                break

            payload = {"session_id": session_id, "input": user}
            try:
                reply = _post_json(f"{api}/chat", payload)
            except Exception as e:
                _print(f"Agent: [error sending message] {e}")
                continue

            text = _extract_output_text(reply)
            if text:
                _print(f"Agent: {text}")
                continue

            status_url = _extract_status_url(api, reply, session_id=session_id)
            if status_url:
                _print("Agent: (working… polling status)")
                out, last = _poll_until_done(
                    status_url,
                    poll_interval=args.poll_interval,
                    timeout=args.poll_timeout,
                )
                if out:
                    _print(f"Agent: {out}")
                else:
                    state = _extract_state(last) or "unknown"
                    _print(f"Agent: (no final text; state={state})")
                    _print(f"[debug] last status payload:\n{json.dumps(last, indent=2)[:2000]}")
            else:
                _print("Agent: (no output; server replied)")
                _print(json.dumps(reply, indent=2))

    except KeyboardInterrupt:
        _print("\nChat ended.")


if __name__ == "__main__":
    main()

