from __future__ import annotations
from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator

Role = Literal["user", "assistant", "system"]

class Message(BaseModel):
    role: Role
    content: str
    ts: float

class PlanItem(BaseModel):
    id: str
    title: str
    status: Literal["todo","doing","done"] = "todo"
    tool_hints: list[str] | None = None

    # Accept ints or strings for id; always store as a string for consistency
    @field_validator("id", mode="before")
    @classmethod
    def _coerce_id(cls, v):
        return str(v)

class FileRef(BaseModel):
    uri: str
    sha256: str
    size: int
    mime: str

class ToolCall(BaseModel):
    id: str
    name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    requires_approval: bool = False

class ToolResult(BaseModel):
    id: str
    ok: bool
    output: Any | None = None
    error: str | None = None

class AssistantAction(BaseModel):
    type: Literal["assistant_message","tool_call","spawn_subagent","revise_plan"]
    message: Optional[Message] = None
    call: Optional[ToolCall] = None
    subagent_spec: Optional[Dict[str, Any]] = None
    plan_diff: Optional[List[PlanItem]] = None

class StatusView(BaseModel):
    conversation_id: str
    plan: List[PlanItem]
    pending_tool_call: ToolCall | None = None
    turns: int
    artifacts: List[FileRef] = []
    state: str = "running"
    output_text: str | None = None
