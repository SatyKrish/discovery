# ──────────────────────────────────────────────────────────────────────────────
# File: src/workflows/agent_orchestrator.py
# Parent workflow with durable loop, approvals, subagent fan-out/fan-in
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import asyncio
import json
from collections import deque
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Deque, Dict, List, Optional
from pydantic import BaseModel
from temporalio import workflow
from temporalio.common import RetryPolicy
from src.models import (
    Message,
    PlanItem,
    FileRef,
    ToolCall,
    AssistantAction,
    ConversationMemory,
    PlanningContext,
    StructuredToolResult,
)
from src.models_subagent import SubAgentSpec, SubAgentResult
from src.workflows.subagent import SubAgentWorkflow

# ---- Helper: parse JSON tool directive if model emits raw JSON (fallback) ----
def _maybe_parse_tool_directive(raw: str) -> Optional[dict]:
    try:
        data = json.loads(raw)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    name = data.get("tool_call") or data.get("tool") or data.get("name")
    if not name or not isinstance(name, str):
        return None
    args = data.get("parameters") or data.get("args") or data.get("arguments") or data.get("input") or {}
    if not isinstance(args, dict):
        args = {"input": args}
    requires_approval = bool(data.get("requires_approval", False))
    return {"name": name, "args": args, "requires_approval": requires_approval}

# ---- Workflow state ----------------------------------------------------------
@dataclass
class State:
    conversation_id: str = ""
    turns: int = 0
    plan: List[PlanItem] = field(default_factory=list)
    planning_context: PlanningContext | None = None
    artifacts: List[FileRef] = field(default_factory=list)
    pending_tool_call: ToolCall | None = None
    gate_ok: bool = True
    done: bool = False
    prompt_queue: Deque[dict] = field(default_factory=deque)  # {turn_id, content}
    last_response_id: str = ""
    memory: ConversationMemory = field(default_factory=ConversationMemory)
    last_tool_approval: Optional[bool] = None
    next_turn_id: int = 1
    discovered_tools: List[dict] = field(default_factory=list)
    discovered_prompts: List[str] = field(default_factory=list)
    pending_tool_access: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # child_id -> {tools, rationale}

    def view_for_llm(self) -> dict:
        recent = self.memory.short_term[-20:] if len(self.memory.short_term) > 20 else self.memory.short_term
        return {
            "plan": [p.model_dump() for p in self.plan],
            "turns": self.turns,
            "pending_tool_call": self.pending_tool_call.model_dump() if self.pending_tool_call else None,
            "artifacts": [a.model_dump() for a in self.artifacts],
            "messages": [m.model_dump() for m in recent],
            "memory_summary": self.memory.summary,
            "user_patterns": self.memory.long_term_patterns,
            "gate_ok": self.gate_ok,
            "last_response_id": self.last_response_id,
            "available_tools": self.discovered_tools,
            "available_prompts": self.discovered_prompts,
        }

    def should_summarize(self) -> bool:
        return self.turns > 0 and self.turns % 5 == 0

    def should_continue_as_new(self) -> bool:
        return self.turns > 0 and self.turns % 25 == 0

# Returned by Updates
class TurnResult(BaseModel):
    assistant: Optional[Message] = None
    pending_tool: Optional[ToolCall] = None

@workflow.defn
class AgentOrchestratorWorkflow:
    def __init__(self):
        self.state = State()

    # ---------- Signals ----------
    @workflow.signal
    async def approve_tool(self, tool_call_id: str, approved: bool, edited_args: dict | None = None):
        if self.state.pending_tool_call and self.state.pending_tool_call.id == tool_call_id:
            if approved and edited_args:
                self.state.pending_tool_call.args = edited_args
            self.state.last_tool_approval = approved
            self.state.pending_tool_call = None

    # child → parent: request additional tools
    @workflow.signal
    async def request_tool_access(self, child_id: str, tools: List[str], rationale: str):
        self.state.pending_tool_access[child_id] = {"tools": tools, "rationale": rationale}

    # external (HITL) → parent: approve; parent → child: grant
    @workflow.signal
    async def approve_tool_access(self, child_id: str, approved_tools: List[str]):
        handle = workflow.get_external_workflow_handle(child_id)
        await handle.signal("grant_tool_access", approved_tools)
        self.state.pending_tool_access.pop(child_id, None)

    @workflow.signal
    async def end_conversation(self):
        self.state.done = True

    # ---------- Queries ----------
    @workflow.query
    def get_conversation_history(self) -> List[Message]:
        return list(self.state.memory.short_term)

    @workflow.query
    def get_pending_tool_access(self) -> Dict[str, Dict[str, Any]]:
        return self.state.pending_tool_access

    # ---------- Updates ----------
    @workflow.update
    async def user_turn(self, msg: Message) -> TurnResult:
        turn_id = self.state.next_turn_id
        self.state.next_turn_id += 1
        # Append user message with turn_id tag
        msg.meta = {**(msg.meta or {}), "turn_id": turn_id}
        self.state.memory.short_term.append(msg)
        if len(self.state.memory.short_term) > 50:
            self.state.memory.short_term = self.state.memory.short_term[-50:]

        await workflow.execute_activity(
            "append_transcript",
            args=[self.state.conversation_id or workflow.info().workflow_id, msg.role, msg.content],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        self.state.gate_ok = await workflow.execute_activity(
            "guardrail_check",
            args=[{"goal": self.state.plan[0].title if self.state.plan else "", "message": msg.content}],
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )

        self.state.prompt_queue.append({"turn_id": turn_id, "content": msg.content})
        self.state.turns += 1

        base_len = len(self.state.memory.short_term)

        def _ready() -> bool:
            if self.state.done or self.state.pending_tool_call is not None:
                return True
            # release when an assistant message tagged for this turn arrives
            for m in self.state.memory.short_term[base_len:]:
                if m.role == "assistant" and (m.meta or {}).get("turn_id") == turn_id:
                    return True
            return False

        await workflow.wait_condition(_ready)

        if self.state.pending_tool_call is not None:
            return TurnResult(pending_tool=self.state.pending_tool_call)

        for m in self.state.memory.short_term[base_len:]:
            if m.role == "assistant" and (m.meta or {}).get("turn_id") == turn_id:
                return TurnResult(assistant=m)

        return TurnResult(assistant=Message(role="assistant", content="(conversation ended)", ts=workflow.now().timestamp(), meta={"turn_id": turn_id}))

    @workflow.update
    async def wait_for_assistant(self) -> Message:
        base_idx = len(self.state.memory.short_term)

        def _assistant_ready() -> bool:
            if self.state.done:
                return True
            return any(m.role == "assistant" for m in self.state.memory.short_term[base_idx:])

        await workflow.wait_condition(_assistant_ready)
        for m in self.state.memory.short_term[base_idx:]:
            if m.role == "assistant":
                return m
        return Message(role="assistant", content="(no reply found)", ts=workflow.now().timestamp())

    # ---------- Helpers ----------
    def _append_assistant(self, msg: Message, *, turn_id: Optional[int] = None) -> None:
        if turn_id is not None:
            msg.meta = {**(msg.meta or {}), "turn_id": turn_id}
        self.state.memory.short_term.append(msg)
        if len(self.state.memory.short_term) > 50:
            self.state.memory.short_term = self.state.memory.short_term[-50:]

    async def _run_tool_and_summarize(self, call: ToolCall, *, turn_id: Optional[int] = None) -> None:
        # Approval gating
        if call.requires_approval:
            self.state.pending_tool_call = call
            self.state.last_tool_approval = None
            await workflow.wait_condition(lambda: self.state.pending_tool_call is None or self.state.done)
            if self.state.done:
                return
            if self.state.last_tool_approval is not True:
                self._append_assistant(Message(role="assistant", content=f"Cancelled **{call.name}** as requested.", ts=workflow.now().timestamp()), turn_id=turn_id)
                return

        # Execute tool
        raw = await workflow.execute_activity(
            "tool_dispatch",
            args=[call],
            heartbeat_timeout=timedelta(seconds=30),
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        tool_result = StructuredToolResult(**raw) if isinstance(raw, dict) else raw

        # Let decider craft a natural-language reply given the tool observation
        response_action_dict: dict = await workflow.execute_activity(
            "decision_agents_activity",
            args=[{
                **self.state.view_for_llm(),
                "tool_observation": {
                    "tool": call.name,
                    "result": getattr(tool_result, "data", None),
                    "error": getattr(tool_result, "error", None),
                },
            }],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        response_action = AssistantAction(**response_action_dict)

        if response_action.type == "assistant_message" and response_action.message:
            self._append_assistant(response_action.message, turn_id=turn_id)
        else:
            self._append_assistant(
                Message(role="assistant", content="I ran the tool and updated context. What next?", ts=workflow.now().timestamp()),
                turn_id=turn_id,
            )

    async def _spawn_subagents(self, specs: List[SubAgentSpec]) -> List[SubAgentResult]:
        children = []
        for i, spec in enumerate(specs):
            # attach parent workflow id for signaling
            if not spec.parent_workflow_id:
                spec.parent_workflow_id = workflow.info().workflow_id
            child = workflow.start_child_workflow(
                SubAgentWorkflow.run,
                spec,
                id=f"{workflow.info().workflow_id}/sub/{spec.kind}/{i}",
                task_queue=workflow.info().task_queue,
                retry_policy=RetryPolicy(maximum_attempts=2),
            )
            children.append(child)
        results = await asyncio.gather(*[child.result() for child in children])
        workflow.upsert_search_attributes({
            "ChildCount": [len(results)],
            "ChildKinds": [s.kind for s in specs],
        })
        return results

    # ---------- Main run loop ----------
    @workflow.run
    async def run(self, goal: str, bootstrap: dict | None = None):
        self.state.conversation_id = workflow.info().workflow_id
        if bootstrap:
            # restore selected fields deterministically
            self.state.plan = [PlanItem(**p) for p in bootstrap.get("plan", [])]
            self.state.artifacts = [FileRef(**a) for a in bootstrap.get("artifacts", [])]
            self.state.memory.summary = bootstrap.get("summary", "")
            self.state.turns = bootstrap.get("turns", 0)
            self.state.last_response_id = bootstrap.get("last_response_id", "")

        # MCP/tool discovery
        discovery = await workflow.execute_activity(
            "discover_mcp_tools",
            args=[],
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )
        if discovery.get("success"):
            self.state.discovered_tools = discovery.get("tools", [])
            self.state.discovered_prompts = discovery.get("prompts", [])
        else:
            workflow.logger.warning(f"Tool discovery failed: {discovery.get('error','unknown')}")

        # Initial plan
        plan_data = await workflow.execute_activity(
            "plan_activity",
            args=[{"goal": goal}],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        self.state.plan = [PlanItem(**it) if isinstance(it, dict) else it for it in plan_data]

        while not self.state.done:
            await workflow.wait_condition(lambda: bool(self.state.prompt_queue) or self.state.done)
            if self.state.done:
                break

            prompt_item = self.state.prompt_queue.popleft()
            turn_id = prompt_item["turn_id"]
            prompt = prompt_item["content"]
            workflow.logger.info(f"Processing turn {turn_id}: {prompt[:120]}")

            # Decide next action (tools enabled path)
            action_dict: dict = await workflow.execute_activity(
                "decision_agents_activity",
                args=[self.state.view_for_llm()],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            action = AssistantAction(**action_dict)

            if "last_response_id" in action_dict:
                self.state.last_response_id = action_dict["last_response_id"]

            if action.type == "assistant_message":
                if action.message:
                    directive = _maybe_parse_tool_directive(action.message.content)
                    if directive:
                        await self._run_tool_and_summarize(ToolCall(id=f"tc-{self.state.turns}-{int(workflow.now().timestamp())}", name=directive["name"], args=directive["args"], requires_approval=directive["requires_approval"]), turn_id=turn_id)
                    else:
                        self._append_assistant(action.message, turn_id=turn_id)

            elif action.type == "revise_plan" and action.plan_diff:
                self.state.plan = action.plan_diff

            elif action.type == "tool_call" and action.call:
                await self._run_tool_and_summarize(action.call, turn_id=turn_id)

            elif action.type == "spawn_subagents" and action.subagents:
                specs = [SubAgentSpec(**s) if not isinstance(s, SubAgentSpec) else s for s in action.subagents]
                results = await self._spawn_subagents(specs)
                # Share artifacts as system note and let LLM craft summary
                system_note = Message(role="system", content=json.dumps({"subagent_results": [r.model_dump() for r in results]}), ts=workflow.now().timestamp())
                self.state.memory.short_term.append(system_note)
                action_dict = await workflow.execute_activity(
                    "decision_agents_activity",
                    args=[self.state.view_for_llm()],
                    start_to_close_timeout=timedelta(minutes=2),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )
                action2 = AssistantAction(**action_dict)
                if action2.type == "assistant_message" and action2.message:
                    self._append_assistant(action2.message, turn_id=turn_id)

            # Summarize / rotate history
            if self.state.should_summarize():
                summary = await workflow.execute_activity(
                    "summarize_activity",
                    args=[self.state.view_for_llm()],
                    start_to_close_timeout=timedelta(minutes=1),
                    retry_policy=RetryPolicy(maximum_attempts=2),
                )
                self.state.memory.summary = summary
                self.state.memory.last_summarized_turn = self.state.turns

            if self.state.should_continue_as_new():
                snapshot = {
                    "plan": [p.model_dump() for p in self.state.plan],
                    "artifacts": [a.model_dump() for a in self.state.artifacts],
                    "summary": self.state.memory.summary,
                    "turns": self.state.turns,
                    "last_response_id": self.state.last_response_id,
                }
                workflow.continue_as_new(goal, snapshot)

        if self.state.done:
            workflow.logger.info("Conversation ended, completing workflow")
            return {
                "status": "completed",
                "conversation_id": self.state.conversation_id,
                "total_turns": self.state.turns,
                "final_plan": [p.model_dump() for p in self.state.plan],
                "artifacts": [a.model_dump() for a in self.state.artifacts],
                "conversation_history": [msg.model_dump() for msg in self.state.memory.short_term],
                "memory_summary": self.state.memory.summary,
                "last_response_id": self.state.last_response_id,
            }
