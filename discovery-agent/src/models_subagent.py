# ──────────────────────────────────────────────────────────────────────────────
# File: src/models_subagent.py
# Models specific to sub-agent orchestration
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class SubAgentSpec(BaseModel):
    kind: str
    goal: str
    allowed_tools: List[str] = Field(default_factory=list)
    input_args: Dict[str, str] = Field(default_factory=dict)
    requires_approval: bool = False
    timeout_minutes: int = 10
    instructions: Optional[str] = None
    instructions_ref: Optional[str] = None
    parent_workflow_id: Optional[str] = None

class SubAgentResult(BaseModel):
    ok: bool
    artifact_refs: List[str] = Field(default_factory=list)
    message: Optional[str] = None
