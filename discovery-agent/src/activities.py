# ──────────────────────────────────────────────────────────────────────────────
# File: src/activities.py
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List

from temporalio import activity

from src.config import apply_openai_env_from_settings, settings
from src.llm import llm_json
from src.models import ToolCall
from src.tools.registry import (
    mcp_discover_tools,
    mcp_get_prompt,
    mcp_invoke_tool,
    mcp_list_prompts,
)


apply_openai_env_from_settings()


@activity.defn
async def discover_mcp_tools() -> Dict[str, Any]:
    return {"success": True, "tools": mcp_discover_tools(), "prompts": mcp_list_prompts()}


@activity.defn
async def get_prompt(prompt_id: str) -> Dict[str, Any]:
    return mcp_get_prompt(prompt_id)


@activity.defn
async def guardrail_check(payload: Dict[str, Any]) -> bool:
    msg = payload.get("message", "")
    banned = ["delete all", "format drive", "wire money to"]
    return not any(b in (msg or "").lower() for b in banned)


@activity.defn
async def append_transcript(conversation_id: str, role: str, content: str) -> None:
    _ = hashlib.sha256(f"{conversation_id}:{role}:{content}".encode()).hexdigest()
    return None


@activity.defn
async def plan_activity(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    goal = payload.get("goal", "")
    return [
        {"id": "plan-1", "title": f"Understand goal: {goal}"},
        {"id": "plan-2", "title": "Gather information via tools"},
        {"id": "plan-3", "title": "Synthesize results"},
    ]


@activity.defn
async def summarize_activity(view: Dict[str, Any]) -> str:
    msgs = view.get("messages", [])
    last_user = next((m for m in reversed(msgs) if m.get("role") == "user"), None)
    return f"Summary up to {len(msgs)} msgs. Last user msg: {(last_user or {}).get('content','')}"


@activity.defn
async def decision_agents_activity(context: Dict[str, Any]) -> Dict[str, Any]:
    """Structured decider: assistant_message | tool_call | spawn_subagents | revise_plan."""

    model = settings.default_model

    ACTION_SCHEMA: Dict[str, Any] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["type"],
        "properties": {
            "type": {
                "type": "string",
                "enum": [
                    "assistant_message",
                    "tool_call",
                    "spawn_subagents",
                    "revise_plan",
                ],
            },
            "message": {
                "type": "object",
                "required": ["role", "content"],
                "properties": {
                    "role": {"type": "string", "enum": ["assistant"]},
                    "content": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "call": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "args": {
                        "type": "object",
                        "additionalProperties": True,
                    },
                    "requires_approval": {"type": "boolean"},
                },
                "additionalProperties": False,
            },
            "plan_diff": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "title"],
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "details": {"type": ["string", "null"]},
                    },
                    "additionalProperties": False,
                },
            },
            "subagents": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["kind", "goal", "allowed_tools"],
                    "properties": {
                        "kind": {"type": "string"},
                        "goal": {"type": "string"},
                        "instructions": {"type": ["string", "null"]},
                        "instructions_ref": {"type": ["string", "null"]},
                        "allowed_tools": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "input_args": {
                            "type": "object",
                            "additionalProperties": True,
                        },
                        "requires_approval": {"type": "boolean"},
                        "timeout_minutes": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 60,
                        },
                    },
                    "additionalProperties": False,
                },
            },
            "last_response_id": {"type": ["string", "null"]},
        },
    }

    def _names(lst):
        out = []
        for t in (lst or []):
            if isinstance(t, str):
                out.append(t)
            elif isinstance(t, dict) and "name" in t:
                out.append(t["name"])
        return out

    tool_names = _names(context.get("available_tools"))
    prompt_ids = context.get("available_prompts", []) or []

    user_payload = {
        "agent_view": {
            "plan": context.get("plan"),
            "messages": context.get("messages"),
            "memory_summary": context.get("memory_summary"),
            "goal": (context.get("planning_context") or {}).get("goal")
            or context.get("goal"),
        },
        "available_tools": tool_names,
        "available_prompts": prompt_ids,
        "hint": (
            "If the goal decomposes into independent specialist tasks, reply with type=spawn_subagents and subagents array. "
            "For each, set concise 'instructions' OR 'instructions_ref' (from available_prompts). "
            "Only include tools from available_tools; set requires_approval only when needed."
        ),
    }

    system = (
        "You are the Discovery decider. Choose the next best action. "
        "Prefer spawn_subagents when parallelizable; otherwise tool_call or assistant_message. "
        "Return ONLY the JSON object per the schema."
    )

    out = llm_json(
        system=system,
        user=json.dumps(user_payload, ensure_ascii=False),
        model=model,
        json_schema=ACTION_SCHEMA,
    )

    if isinstance(out, dict) and out.get("type") == "spawn_subagents":
        subs = out.get("subagents") or []
        for s in subs:
            s["allowed_tools"] = [t for t in s.get("allowed_tools", []) if t in tool_names]
            if s.get("instructions_ref") and s["instructions_ref"] not in prompt_ids:
                s["instructions_ref"] = None
            tmo = int(s.get("timeout_minutes", 10))
            s["timeout_minutes"] = max(1, min(60, tmo))
        out["subagents"] = subs

    if isinstance(out, dict) and out.get("type") == "tool_call":
        c = out.get("call") or {}
        if "id" not in c:
            c["id"] = f"tc-{hashlib.sha256(json.dumps(c, sort_keys=True).encode()).hexdigest()[:8]}"
        out["call"] = c

    return out


@activity.defn
async def tool_dispatch(call: ToolCall) -> Dict[str, Any]:
    return mcp_invoke_tool(call.name, call.args)


@activity.defn
async def mcp_invoke(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    return mcp_invoke_tool(tool_name, args)

