# ──────────────────────────────────────────────────────────────────────────────
# File: src/models.py
# Core data models shared across workflows and activities
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from typing import Any, Dict, List, Optional, Deque
from dataclasses import dataclass, field
from collections import deque
from pydantic import BaseModel, Field

# ----- Chat primitives --------------------------------------------------------
class Message(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str
    ts: float | None = None
    meta: Dict[str, Any] = Field(default_factory=dict)  # e.g., {"turn_id": 7}

class PlanItem(BaseModel):
    id: str
    title: str
    details: str | None = None

class FileRef(BaseModel):
    uri: str
    kind: str | None = None

class ToolCall(BaseModel):
    id: str
    name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    requires_approval: bool = False

class ToolResult(BaseModel):
    call_id: str
    success: bool
    data: Any | None = None
    error: str | None = None

class StructuredToolResult(BaseModel):
    success: bool
    data: Any | None = None
    error: str | None = None

class ConversationMemory(BaseModel):
    short_term: List[Message] = Field(default_factory=list)
    summary: str = ""
    last_summarized_turn: int = 0
    long_term_patterns: Dict[str, Any] = Field(default_factory=dict)

class PlanningContext(BaseModel):
    goal: str

class ToolSpec(BaseModel):
    name: str
    description: str = ""
    input_schema: Dict[str, Any] = Field(default_factory=dict)

# ----- Assistant decision contract -------------------------------------------
class AssistantAction(BaseModel):
    # type: "assistant_message" | "revise_plan" | "tool_call" | "spawn_subagents"
    type: str
    message: Optional[Message] = None
    plan_diff: Optional[List[PlanItem]] = None
    call: Optional[ToolCall] = None
    subagents: Optional[List[dict]] = None  # serialized SubAgentSpec
    last_response_id: Optional[str] = None
