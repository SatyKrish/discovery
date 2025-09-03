# ──────────────────────────────────────────────────────────────────────────────
# File: src/workflows/subagent.py
# Dynamic child workflow for domain-specific tasks (flight/hotel/cab/event)
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from datetime import timedelta
from typing import List
from temporalio import workflow
from temporalio.common import RetryPolicy
from src.models_subagent import SubAgentSpec, SubAgentResult
from src.models import AssistantAction, ToolCall, Message, StructuredToolResult

@workflow.defn
class SubAgentWorkflow:
    @workflow.run
    async def run(self, spec: SubAgentSpec) -> SubAgentResult:
        artifacts: List[str] = []
        turns = 0
        deadline = workflow.now() + timedelta(minutes=spec.timeout_minutes)

        while workflow.now() < deadline:
            action_dict = await workflow.execute_activity(
                "decision_agents_activity",
                args=[{
                    "subagent": spec.kind,
                    "goal": spec.goal,
                    "allowed_tools": spec.allowed_tools,
                    "input_args": spec.input_args,
                }],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            action = AssistantAction(**action_dict)

            if action.type == "tool_call" and action.call:
                call: ToolCall = action.call
                if spec.allowed_tools and call.name not in spec.allowed_tools:
                    await workflow.execute_activity(
                        "append_transcript",
                        args=[workflow.info().workflow_id, "system", f"Denied {call.name}: not allowed"],
                        start_to_close_timeout=timedelta(seconds=10),
                    )
                    continue

                if spec.requires_approval:
                    # hook: parent can signal child-specific approval if you add a signal
                    pass

                raw = await workflow.execute_activity(
                    "tool_dispatch",
                    args=[call],
                    heartbeat_timeout=timedelta(seconds=30),
                    start_to_close_timeout=timedelta(minutes=10),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )
                result = StructuredToolResult(**raw) if isinstance(raw, dict) else raw
                if result.success and isinstance(result.data, dict) and "artifact_ref" in result.data:
                    artifacts.append(result.data["artifact_ref"])

                # Ask decider to produce next step / completion message
                action_dict = await workflow.execute_activity(
                    "decision_agents_activity",
                    args=[{
                        "subagent": spec.kind,
                        "goal": spec.goal,
                        "allowed_tools": spec.allowed_tools,
                        "tool_observation": {"tool": call.name, "result": getattr(result, "data", None), "error": getattr(result, "error", None)},
                    }],
                    start_to_close_timeout=timedelta(minutes=2),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )
                action = AssistantAction(**action_dict)

            if action.type == "assistant_message" and action.message:
                msg: Message = action.message
                if "DONE" in (msg.content or "").upper():
                    return SubAgentResult(ok=True, artifact_refs=artifacts, message=msg.content)

            turns += 1
            if turns % 15 == 0:
                workflow.continue_as_new(spec)

        return SubAgentResult(ok=bool(artifacts), artifact_refs=artifacts, message="timeout")
