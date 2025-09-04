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
from src.models import PlanItem, ToolCall, StructuredToolResult, FileRef
from src.tools.registry import mcp_discover_tools, mcp_list_prompts, mcp_invoke_tool, mcp_get_prompt

# Ensure env for activity process
apply_openai_env_from_settings()

@activity.defn
async def discover_mcp_tools() -> Dict[str, Any]:
    return {"success": True, "tools": mcp_discover_tools(), "prompts": mcp_list_prompts()}

@activity.defn
async def get_prompt(prompt_id: str) -> Dict[str, Any]:
    return mcp_get_prompt(prompt_id)

@activity.defn
async def mcp_invoke(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    return mcp_invoke_tool(tool_name, args)

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

# Strict validation schemas for actions
TOOL_CALL_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["id", "name", "requires_approval"],  # args is optional
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "args": {"type": "object"},  # Allow any args structure
        "requires_approval": {"type": "boolean"}
    },
    "additionalProperties": False
}

SUBAGENT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["kind", "goal", "allowed_tools"],
    "properties": {
        "kind": {"type": "string"},
        "goal": {"type": "string"},
        "instructions": {"type": ["string", "null"]},
        "instructions_ref": {"type": ["string", "null"]},
        "allowed_tools": {"type": "array", "items": {"type": "string"}},
        "input_args": {"type": "object"},
        "requires_approval": {"type": "boolean"},
        "timeout_minutes": {"type": "integer", "minimum": 1, "maximum": 60}
    },
    "additionalProperties": False
}

def _validate_action(action: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Simple JSON schema validation for actions."""
    try:
        import jsonschema
        jsonschema.validate(instance=action, schema=schema)
        return True
    except Exception:
        return False

async def _repair_invalid_action(action: Dict[str, Any], action_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Attempt to repair invalid action arguments."""
    try:
        repair_prompt = f"""
        The following {action_type} action is invalid. Please repair it to be valid:

        Invalid action: {json.dumps(action, indent=2)}

        Context: {json.dumps(context, indent=2)}

        Return a repaired version of the action that follows the correct schema.
        """

        repair_result = _provider().json(
            system="You are an action repair assistant. Fix invalid actions to make them valid.",
            user=repair_prompt,
            model=settings.default_model,
            json_schema={"type": "object", "properties": {"repaired_action": {"type": "object"}}, "required": ["repaired_action"]}
        )

        return repair_result.get("repaired_action", action)
    except Exception:
        # If repair fails, return original action
        return action

# Decision activity using Responses API tool calling where applicable
@activity.defn
async def decision_agents_activity(context: Dict[str, Any]) -> Dict[str, Any]:
    """Structured decider: assistant_message | tool_call | spawn_subagents | revise_plan."""
    model = settings.default_model
    ACTION_SCHEMA: Dict[str, Any] = {
        "type": "object", "additionalProperties": False, "required": ["type"],
        "properties": {
            "type": {"type": "string", "enum": ["assistant_message", "tool_call", "spawn_subagents", "revise_plan"]},
            "message": {"type": "object",
                        "properties": {"role": {"type": "string", "enum": ["assistant"]}, "content": {"type": "string"}},
                        "additionalProperties": False},
            "call": {"type": "object",
                     "properties": {"id": {"type": "string"}, "name": {"type": "string"},
                                    "args": {"type": "object"},
                                    "requires_approval": {"type": "boolean"}},
                     "additionalProperties": False},
            "plan_diff": {"type": "array", "items": {"type": "object",
                                                     "properties": {"id":{"type":"string"}, "title":{"type":"string"}, "details":{"type":["string","null"]}},
                                                     "additionalProperties": False}},
            "subagents": {"type": "array", "items": {"type": "object",
                         "properties": {
                             "kind": {"type": "string"},
                             "goal": {"type": "string"},
                             "instructions": {"type": ["string","null"]},
                             "instructions_ref": {"type": ["string","null"]},
                             "allowed_tools": {"type": "array", "items": {"type": "string"}},
                             "input_args": {"type":"object"},
                             "requires_approval": {"type":"boolean"},
                             "timeout_minutes": {"type":"integer","minimum":1,"maximum":60},
                         },
                         "additionalProperties": False}},
            "last_response_id": {"type": ["string","null"]},
        }
    }

    def _names(lst):
        out=[]
        for t in (lst or []):
            if isinstance(t, str): out.append(t)
            elif isinstance(t, dict) and "name" in t: out.append(t["name"])
        return out

    tool_names = _names(context.get("available_tools"))
    prompt_ids = context.get("available_prompts", []) or []

    user_payload = {
        "agent_view": {
            "plan": context.get("plan"),
            "messages": context.get("messages"),
            "memory_summary": context.get("memory_summary"),
            "goal": (context.get("planning_context") or {}).get("goal") or context.get("goal"),
        },
        "available_tools": tool_names,
        "available_prompts": prompt_ids,
        "hint": (
            "If the goal decomposes into independent specialist tasks, reply with type=spawn_subagents and subagents array. "
            "For each, set concise 'instructions' OR 'instructions_ref' (from available_prompts). "
            "Only include tools from available_tools; set requires_approval only when needed."
        ),
    }

    system = ("You are the Discovery decider. Choose the next best action. "
              "Prefer spawn_subagents when parallelizable; otherwise tool_call or assistant_message. "
              "Return ONLY the JSON object per the schema.")

    out = _provider().json(system=system, user=json.dumps(user_payload, ensure_ascii=False), model=model, json_schema=ACTION_SCHEMA)

    # Strict validation for actions that require execution
    if isinstance(out, dict):
        action_type = out.get("type")

        if action_type == "tool_call" and out.get("call"):
            # Validate tool call with strict schema
            if not _validate_action(out["call"], TOOL_CALL_SCHEMA):
                activity.logger.warning("Invalid tool call detected, attempting repair")
                repaired_call = await _repair_invalid_action(out["call"], "tool_call", context)
                if _validate_action(repaired_call, TOOL_CALL_SCHEMA):
                    out["call"] = repaired_call
                    activity.logger.info("Tool call repaired successfully")
                else:
                    activity.logger.error("Tool call repair failed, converting to assistant message")
                    out = {
                        "type": "assistant_message",
                        "message": {
                            "role": "assistant",
                            "content": "I tried to use a tool but the request was invalid. Could you please clarify what you'd like me to do?"
                        }
                    }

        elif action_type == "spawn_subagents" and out.get("subagents"):
            # Validate each subagent with strict schema
            valid_subagents = []
            for subagent in out["subagents"]:
                if _validate_action(subagent, SUBAGENT_SCHEMA):
                    valid_subagents.append(subagent)
                else:
                    activity.logger.warning("Invalid subagent detected, attempting repair")
                    repaired_subagent = await _repair_invalid_action(subagent, "subagent", context)
                    if _validate_action(repaired_subagent, SUBAGENT_SCHEMA):
                        valid_subagents.append(repaired_subagent)
                        activity.logger.info("Subagent repaired successfully")
                    else:
                        activity.logger.warning("Subagent repair failed, skipping invalid subagent")

            if not valid_subagents:
                activity.logger.error("All subagents invalid, converting to assistant message")
                out = {
                    "type": "assistant_message",
                    "message": {
                        "role": "assistant",
                        "content": "I tried to create specialized agents but the requests were invalid. Could you please clarify what tasks you'd like me to perform?"
                    }
                }
            else:
                out["subagents"] = valid_subagents

    # Post-processing for valid actions
    if isinstance(out, dict) and out.get("type") == "spawn_subagents":
        subs = out.get("subagents") or []
        for s in subs:
            s["allowed_tools"] = [t for t in s.get("allowed_tools", []) if t in tool_names]
            if s.get("instructions_ref") and s["instructions_ref"] not in prompt_ids:
                s["instructions_ref"] = None
            tmo = int(s.get("timeout_minutes", 10)); s["timeout_minutes"] = max(1, min(60, tmo))
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
async def vfs_put(bytes_data: bytes, filename: str, mime: str) -> FileRef:
    from pathlib import Path
    from src.models import FileRef
    Path(settings.vfs_root).mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(bytes_data).hexdigest()
    path = Path(settings.vfs_root) / f"{sha}_{filename}"
    with open(path, "wb") as f:
        f.write(bytes_data)
    return FileRef(uri=str(path), sha256=sha, size=len(bytes_data), mime=mime)
