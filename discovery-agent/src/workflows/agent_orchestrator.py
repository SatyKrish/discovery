from __future__ import annotations
from dataclasses import dataclass, field
from datetime import timedelta
from typing import List
from temporalio import workflow
from temporalio.common import RetryPolicy
from src.models import Message, PlanItem, FileRef, ToolCall, ToolResult, AssistantAction, StatusView

@dataclass
class State:
    conversation_id: str = ""
    turns: int = 0
    plan: List[PlanItem] = field(default_factory=list)
    messages_digest: str = ""
    artifacts: List[FileRef] = field(default_factory=list)
    pending_tool_call: ToolCall | None = None
    gate_ok: bool = True
    done: bool = False
    last_message: Message | None = None

    def view_for_llm(self) -> dict:
        return {
            "plan": [p.model_dump() for p in self.plan],
            "turns": self.turns,
            "pending_tool_call": self.pending_tool_call.model_dump() if self.pending_tool_call else None,
            "artifacts": [a.model_dump() for a in self.artifacts],
            "messages_digest": self.messages_digest,
            "gate_ok": self.gate_ok,
        }

    def should_summarize(self) -> bool:
        return self.turns > 0 and self.turns % 5 == 0

    def should_continue_as_new(self) -> bool:
        return self.turns > 0 and self.turns % 25 == 0

@workflow.defn
class AgentOrchestratorWorkflow:
    def __init__(self):
        self.state = State()

    @workflow.signal
    async def user_message(self, msg: Message):
        await workflow.execute_activity(
            "append_transcript",
            args=[
                self.state.conversation_id or workflow.info().workflow_id,
                msg.role,
                msg.content,
            ],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        self.state.gate_ok = await workflow.execute_activity(
            "guardrail_check",
            args=[{"goal": self.state.plan[0].title if self.state.plan else "", "message": msg.content}],
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )
        if self.state.gate_ok:
            self.state.turns += 1

    @workflow.signal
    async def approve_tool(self, tool_call_id: str, approved: bool, edited_args: dict | None = None):
        if self.state.pending_tool_call and self.state.pending_tool_call.id == tool_call_id and approved:
            if edited_args:
                self.state.pending_tool_call.args = edited_args
        self.state.pending_tool_call = None

    @workflow.query
    def get_status(self) -> StatusView:
        return StatusView(
            conversation_id=self.state.conversation_id,
            plan=self.state.plan,
            pending_tool_call=self.state.pending_tool_call,
            turns=self.state.turns,
            artifacts=self.state.artifacts,
            state="done" if self.state.done else "running",
            last_message=self.state.last_message,
        )

    @workflow.run
    async def run(self, goal: str):
        self.state.conversation_id = workflow.info().workflow_id
        plan_data = await workflow.execute_activity(
            "plan_activity",
            args=[{"goal": goal}],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        # Convert JSON-serializable dicts back into PlanItem objects
        self.state.plan = [PlanItem(**it) if isinstance(it, dict) else it for it in plan_data]

        while not self.state.done:
            action_dict: dict = await workflow.execute_activity(
                "decision_agents_activity",
                args=[self.state.view_for_llm()],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            action: AssistantAction = AssistantAction(**action_dict)

            if action.type == "assistant_message":
                if action.message:
                    await workflow.execute_activity(
                        "append_transcript",
                        args=[
                            self.state.conversation_id or workflow.info().workflow_id,
                            action.message.role,
                            action.message.content,
                        ],
                        start_to_close_timeout=timedelta(seconds=10),
                        retry_policy=RetryPolicy(maximum_attempts=3),
                    )
                    self.state.last_message = action.message
                self.state.turns += 1
            elif action.type == "revise_plan" and action.plan_diff:
                self.state.plan = action.plan_diff
            elif action.type == "tool_call" and action.call:
                call = action.call
                if call.requires_approval:
                    self.state.pending_tool_call = call
                    await workflow.wait_condition(lambda: self.state.pending_tool_call is None)
                result: ToolResult = await workflow.execute_activity(
                    "tool_dispatch",
                    args=[call],
                    heartbeat_timeout=timedelta(seconds=30),
                    start_to_close_timeout=timedelta(minutes=10),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )
                self.state.turns += 1
            elif action.type == "spawn_subagent":
                self.state.turns += 1

            if self.state.should_summarize():
                self.state.messages_digest = await workflow.execute_activity(
                    "summarize_activity",
                    args=[self.state.view_for_llm()],
                    start_to_close_timeout=timedelta(minutes=1),
                    retry_policy=RetryPolicy(maximum_attempts=2),
                )

            if self.state.should_continue_as_new():
                workflow.continue_as_new(goal)
