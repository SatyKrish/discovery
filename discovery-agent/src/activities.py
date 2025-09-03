# ──────────────────────────────────────────────────────────────────────────────
# File: src/activities.py
# Temporal Activities: planning/deciding/summarizing/guardrails/tool-dispatch
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import json
import hashlib
from datetime import timedelta
from typing import Any, Dict, List
from temporalio import activity
from src.config import settings, apply_openai_env_from_settings
from src.llm import LLMError, _provider
from src.models import PlanItem, ToolCall, StructuredToolResult
from src.tools.registry import TOOLS, TOOL_SCHEMAS

# Ensure env for activity process
apply_openai_env_from_settings()

@activity.defn
async def discover_mcp_tools() -> Dict[str, Any]:
    # In production, probe MCP servers. Here we expose the static registry.
    return {"success": True, "tools": list(TOOLS.keys())}

@activity.defn
async def guardrail_check(payload: Dict[str, Any]) -> bool:
    # Replace with real policy checks (PII, budget, allowed domains, etc.)
    goal = payload.get("goal", "")
    msg = payload.get("message", "")
    banned = ["delete all", "format drive", "wire money to"]
    return not any(b in msg.lower() for b in banned)

@activity.defn
async def append_transcript(conversation_id: str, role: str, content: str) -> None:
    # Idempotency: derive stable key from input (example; replace with DB upsert)
    key = hashlib.sha256(f"{conversation_id}:{role}:{content}".encode()).hexdigest()
    activity.logger.debug("append_transcript key=%s", key)
    return None

@activity.defn
async def plan_activity(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Simple seed plan based on goal; in prod call model with schema
    goal = payload.get("goal", "")
    items = [
        {"id": "plan-1", "title": f"Understand goal: {goal}"},
        {"id": "plan-2", "title": "Gather information via tools"},
        {"id": "plan-3", "title": "Synthesize results"},
    ]
    return items

@activity.defn
async def summarize_activity(view: Dict[str, Any]) -> str:
    # In prod, call model with strict schema for summary
    msgs = view.get("messages", [])
    last_user = next((m for m in reversed(msgs) if m.get("role") == "user"), None)
    return f"Summary up to {len(msgs)} msgs. Last user msg: {(last_user or {}).get('content','')}"

# Decision activity using Responses API tool calling where applicable
@activity.defn
async def decision_agents_activity(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stateless decider: build a minimal conversation window and expose selected tools
    to the model. Returns AssistantAction dict.
    """
    model = settings.default_model
    system = (
        "You are Discovery, a durable research/booking agent. "
        "Prefer calling tools when they help achieve the goal. "
        "Return JSON with fields: type, message?, plan_diff?, call?, subagents?, last_response_id?"
    )

    allowed_tools = context.get("allowed_tools") or context.get("tool_allowlist") or []
    tool_schemas = [TOOL_SCHEMAS[n] for n in allowed_tools if n in TOOL_SCHEMAS]

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(context, ensure_ascii=False)},
    ]

    # If no tools are allowed, ask for a friendly assistant message
    if not tool_schemas:
        out = _provider().json(
            system=system,
            user=(
                "Given the context, reply as an assistant_message object: "
                "{\"type\":\"assistant_message\",\"message\":{\"role\":\"assistant\",\"content\":\"<your reply>\"}}"
            ),
            model=model,
        )
        return out if isinstance(out, dict) else {"type": "assistant_message", "message": {"role": "assistant", "content": "OK"}}

    # Tools are available: let the model choose a function call
    resp = _provider().tools(messages=messages, tools=tool_schemas, model=model, tool_choice="auto")

    # Adapt OpenAI Responses tool-calls to AssistantAction
    tool_calls = []
    try:
        if getattr(resp, "output", None):
            # Iterate tool calls if present (shape depends on SDK version)
            for item in resp.output or []:
                tcalls = getattr(item, "tool_calls", None) or []
                for tc in tcalls:
                    tool_calls.append({
                        "id": getattr(tc, "id", "tc"),
                        "name": getattr(tc, "function", {}).get("name") if getattr(tc, "function", None) else getattr(tc, "name", None),
                        "args": getattr(tc, "function", {}).get("arguments", {}) if getattr(tc, "function", None) else getattr(tc, "arguments", {}),
                    })
    except Exception:
        activity.logger.exception("Failed to adapt tool calls; falling back")

    if tool_calls:
        tc = tool_calls[0]
        return {
            "type": "tool_call",
            "call": {"id": tc["id"], "name": tc["name"], "args": tc.get("args", {}), "requires_approval": False},
            "last_response_id": getattr(resp, "id", None),
        }

    # No tool selected → default to assistant message
    txt = getattr(resp, "output_text", "I can proceed.")
    return {
        "type": "assistant_message",
        "message": {"role": "assistant", "content": txt},
        "last_response_id": getattr(resp, "id", None),
    }

@activity.defn
async def tool_dispatch(call: ToolCall) -> Dict[str, Any]:
    # Idempotency key example (ensure tool handlers support it)
    _ = hashlib.sha256(f"{call.id}:{call.name}:{json.dumps(call.args, sort_keys=True)}".encode()).hexdigest()
    handler = TOOLS.get(call.name)
    if not handler:
        return {"success": False, "error": f"Unknown tool {call.name}"}
    try:
        data = handler(**call.args)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@activity.defn
async def vfs_put(bytes_data: bytes, filename: str, mime: str) -> FileRef:
    from pathlib import Path
    from src.models import FileRef
    Path(settings.vfs_root).mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(bytes_data).hexdigest()
    path = Path(settings.vfs_root) / f"{sha}_{filename}"
    with open(path, "wb") as f:
        f.write(bytes_data)
    return FileRef(uri=str(path), sha256=sha, size=len(bytes_data), mime=mime)
