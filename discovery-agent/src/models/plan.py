# src/models/plan.py (or wherever PlanItem lives)
from typing import Literal, Optional, Dict, List
from pydantic import BaseModel, Field, field_validator, ConfigDict

class PlanItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
    )

    id: str = Field(..., description="Stable string id")
    title: str
    status: Literal["pending", "running", "done", "failed"] = "pending"
    deps: List[str] = []
    tool: Optional[str] = None
    inputs: Dict[str, object] = {}
    result: Optional[str] = None
    error: Optional[str] = None

    @field_validator("id", mode="before")
    @classmethod
    def coerce_id(cls, v):
        # Accept ints or strings, always store as string
        return str(v)
