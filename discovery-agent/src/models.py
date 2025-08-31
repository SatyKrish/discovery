from __future__ import annotations
from typing import Literal, Optional, List, Dict, Any, Callable
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

class ConversationMemory(BaseModel):
    short_term: List[Message] = []  # Recent messages (last 20-50)
    long_term_patterns: Dict[str, Any] = {}  # User patterns and preferences
    summary: str = ""  # Rolling summary of conversation
    last_summarized_turn: int = 0

class SubGoal(BaseModel):
    id: str
    title: str
    description: str = ""
    status: Literal["pending", "in_progress", "completed", "failed"] = "pending"
    priority: int = 1  # 1-5 scale
    estimated_effort: str = ""  # "quick", "medium", "complex"
    dependencies: List[str] = []  # IDs of prerequisite sub-goals
    success_criteria: str = ""
    progress: float = 0.0  # 0.0 to 1.0
    tools_needed: List[str] = []
    notes: str = ""

class PlanningContext(BaseModel):
    primary_goal: str
    subgoals: List[SubGoal] = []
    dependencies: Dict[str, List[str]] = {}  # Maps goal ID to list of dependent goal IDs
    progress: Dict[str, float] = {}  # Maps goal ID to progress (0.0-1.0)
    replan_triggers: List[str] = []  # Conditions that should trigger replanning
    created_at: float = 0.0
    last_updated: float = 0.0
    version: int = 1

class MCPServer(BaseModel):
    name: str
    url: str
    capabilities: List[str] = []
    tools: List[Dict[str, Any]] = []
    last_connected: float = 0.0
    health_status: str = "unknown"  # "healthy", "unhealthy", "unknown"

class ToolOrchestrator(BaseModel):
    static_tools: Dict[str, ToolSpec] = {}
    mcp_servers: Dict[str, MCPServer] = {}
    tool_usage_stats: Dict[str, Dict[str, Any]] = {}
    last_discovery: float = 0.0

class ToolSpec(BaseModel):
    name: str
    fn: Callable[[dict], Any]
    description: Optional[str] = None
    schema: Optional[Dict[str, Any]] = Field(default=None, description="JSON Schema for args")

class ToolChainStep(BaseModel):
    tool_name: str
    step_id: str
    description: str
    input_mapping: Dict[str, str]  # Maps input params to previous step outputs
    output_mapping: Dict[str, str]  # Maps outputs to variable names
    dependencies: List[str] = []  # Step IDs this step depends on
    retry_count: int = 0
    timeout: int = 30

class ToolChain(BaseModel):
    chain_id: str
    name: str
    description: str
    steps: List[ToolChainStep]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    success_criteria: str = ""
    estimated_duration: int = 60  # seconds
    created_at: float = 0.0

class ToolChainExecution(BaseModel):
    execution_id: str
    chain_id: str
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    current_step: str = ""
    step_results: Dict[str, Any] = {}
    variables: Dict[str, Any] = {}
    started_at: float = 0.0
    completed_at: float = 0.0
    error_message: str = ""

class SelfReflectionEntry(BaseModel):
    reflection_id: str
    timestamp: float
    interaction_type: str  # "tool_use", "conversation", "planning"
    success_rating: float  # 0.0 to 1.0
    performance_metrics: Dict[str, Any]
    lessons_learned: List[str]
    strategy_adjustments: List[str]
    user_feedback: str = ""

class HierarchicalAgent(BaseModel):
    agent_id: str
    name: str
    role: str  # "planning", "execution", "reflection", "communication"
    capabilities: List[str]
    specialization: str
    performance_score: float = 0.5
    experience_level: int = 1
    active: bool = True

class PerformanceAnalytics(BaseModel):
    time_range: str  # "hour", "day", "week", "month"
    total_interactions: int = 0
    successful_interactions: int = 0
    average_response_time: float = 0.0
    tool_usage_stats: Dict[str, Dict[str, Any]] = {}
    user_satisfaction_score: float = 0.0
    common_patterns: List[str] = []
    improvement_suggestions: List[str] = []

class ResponseEnvelope(BaseModel):
    """Standardized response envelope for all agent responses"""
    type: Literal["assistant_message", "tool_result", "error", "completion", "status"]
    status: Literal["success", "error", "pending", "completed"]
    content: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)
    client_hints: Dict[str, Any] = Field(default_factory=dict)
    timestamp: Optional[float] = None

class StructuredToolResult(BaseModel):
    """Structured result from tool execution"""
    tool_name: str
    success: bool
    data: Any = None
    error: str = None
    formatted_display: str = None
    execution_time: float = None
    next_actions: List[str] = Field(default_factory=list)

class StatusView(BaseModel):
    conversation_id: str
    plan: List[PlanItem]
    pending_tool_call: ToolCall | None = None
    turns: int
    artifacts: List[FileRef] = []
    state: str = "running"
    response: ResponseEnvelope | None = None
    memory_summary: str | None = None
