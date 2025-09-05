# ──────────────────────────────────────────────────────────────────────────────
# File: src/workflows/agent_orchestrator.py
# Clean, simplified agent orchestrator - maintainable and readable
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from temporalio import workflow
from temporalio.common import RetryPolicy
from src.models import Message, ToolCall, AssistantAction, StructuredToolResult
from src.models_subagent import SubAgentSpec, SubAgentResult
from src.workflows.subagent import SubAgentWorkflow

# ---- Clean State (only essential fields) ----
@dataclass
class State:
    messages: List[Message] = field(default_factory=list)
    pending_tool_call: ToolCall | None = None
    done: bool = False
    current_request_id: Optional[str] = None

    def view_for_llm(self) -> dict:
        recent = self.messages[-20:] if len(self.messages) > 20 else self.messages
        return {
            "pending_tool_call": self.pending_tool_call.model_dump() if self.pending_tool_call else None,
            "messages": [m.model_dump() for m in recent],
        }

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
            self.state.pending_tool_call = None

    @workflow.signal
    async def end_conversation(self):
        self.state.done = True

    # ---------- Queries ----------
    @workflow.query
    def get_conversation_history(self) -> List[Message]:
        return self.state.messages

    @workflow.query
    def get_health_status(self) -> Dict[str, Any]:
        return {
            "status": "healthy" if not self.state.done else "completed",
            "active_tools": 1 if self.state.pending_tool_call else 0,
            "memory_usage": len(self.state.messages),
            "last_activity": workflow.now().timestamp(),
        }

    # ---------- Updates ----------
    @workflow.update
    async def wait_for_assistant(self) -> Message:
        """Wait for the next assistant message after user input"""
        # Get current count of assistant messages
        initial_count = len([m for m in self.state.messages if m.role == "assistant"])

        # Wait for a new assistant message
        await workflow.wait_condition(
            lambda: len([m for m in self.state.messages if m.role == "assistant"]) > initial_count
        )

        # Return the latest assistant message
        for msg in reversed(self.state.messages):
            if msg.role == "assistant":
                return msg

        return None

    @workflow.update
    async def user_turn(self, msg: Message) -> TurnResult:
        # Add message to conversation with deterministic request tracking
        request_id = f"req-{workflow.info().workflow_id}-{len(self.state.messages)}"
        msg.meta["request_id"] = request_id
        self.state.messages.append(msg)
        self.state.current_request_id = request_id

        if len(self.state.messages) > 50:
            self.state.messages = self.state.messages[-50:]

        # Log transcript
        await workflow.execute_activity(
            "append_transcript",
            args=[workflow.info().workflow_id, msg.role, msg.content],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=3, initial_interval=timedelta(seconds=1)),
        )

        # Gate check
        gate_ok = await workflow.execute_activity(
            "guardrail_check",
            args=[{"message": msg.content}],
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(maximum_attempts=2, initial_interval=timedelta(seconds=1)),
        )

        # Check for pending tool calls first
        if self.state.pending_tool_call:
            return TurnResult(pending_tool=self.state.pending_tool_call)

        # Generate response synchronously (restore original behavior)
        action_dict = await workflow.execute_activity(
            "deep_agent_activity",
            args=[self.state.view_for_llm()],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        action = AssistantAction(**action_dict)

        if action.type == "assistant_message" and action.message:
            # Add response to conversation
            self.state.messages.append(action.message)
            return TurnResult(assistant=action.message)
        elif action.type == "tool_call" and action.call:
            # Handle tool calls
            self.state.pending_tool_call = action.call
            return TurnResult(pending_tool=action.call)

        return TurnResult()

    # ---------- Main workflow ----------
    @workflow.run
    async def run(self, goal: str):
        conversation_id = workflow.info().workflow_id

        # Tool discovery (removed from state - can be handled differently if needed)
        discovery = await workflow.execute_activity(
            "discover_mcp_tools",
            args=[],
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )

        # Main conversation loop
        while not self.state.done:
            # Wait for user input
            await workflow.wait_condition(lambda: any(m.role == "user" for m in self.state.messages[-1:]) or self.state.done)
            if self.state.done:
                break

            # Get latest user message
            user_msg = next((m for m in reversed(self.state.messages) if m.role == "user"), None)
            if not user_msg:
                continue

            # Decide next action
            action_dict = await workflow.execute_activity(
                "deep_agent_activity",
                args=[self.state.view_for_llm()],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            action = AssistantAction(**action_dict)

            if action.type == "assistant_message" and action.message:
                self.state.messages.append(action.message)

            elif action.type == "tool_call" and action.call:
                await self._execute_tool(action.call)

            elif action.type == "spawn_subagents" and action.subagents:
                await self._spawn_subagents(action.subagents)

        return {
            "status": "completed",
            "conversation_id": conversation_id,
            "total_messages": len(self.state.messages),
            "conversation_history": [msg.model_dump() for msg in self.state.messages],
        }

    # ---------- Helper methods ----------
    async def _execute_tool(self, call: ToolCall):
        # Approval gating
        if call.requires_approval:
            self.state.pending_tool_call = call
            await workflow.wait_condition(lambda: self.state.pending_tool_call is None or self.state.done)
            if self.state.done or not self.state.pending_tool_call:
                return

        # Execute tool
        raw = await workflow.execute_activity(
            "tool_dispatch",
            args=[call],
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(maximum_attempts=3, initial_interval=timedelta(seconds=2)),
        )
        tool_result = StructuredToolResult(**raw) if isinstance(raw, dict) else raw

        # Get response from LLM
        response_action_dict = await workflow.execute_activity(
            "deep_agent_activity",
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
            self.state.messages.append(response_action.message)

    async def _spawn_subagents(self, subagents: List[dict]):
        # Convert to SubAgentSpec objects
        specs = [SubAgentSpec(**s) if not isinstance(s, SubAgentSpec) else s for s in subagents]

        # Spawn subagent workflows
        children = []
        for i, spec in enumerate(specs):
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

        # Wait for all subagents to complete
        results = await asyncio.gather(*[child.result() for child in children])

        # Process results and get LLM summary
        result_summary = await workflow.execute_activity(
            "deep_agent_activity",
            args=[{
                **self.state.view_for_llm(),
                "subagent_results": [r.model_dump() for r in results],
            }],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        summary_action = AssistantAction(**result_summary)

        if summary_action.type == "assistant_message" and summary_action.message:
            self.state.messages.append(summary_action.message)
