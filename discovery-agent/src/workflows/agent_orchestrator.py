from __future__ import annotations

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
    ToolResult,
    AssistantAction,
    ConversationMemory,
    PlanningContext,
    StructuredToolResult,
)

# ---------- Formatting helpers (pure/deterministic) ----------

def _format_web_search_result(data: Dict[str, Any]) -> str:
    query = data.get("query", "Unknown query")
    total_results = data.get("total_results", 0)
    results = data.get("results", [])
    if not results:
        return f"No results found for '{query}'."
    out = [f"Search results for '{query}':", ""]
    for i, r in enumerate(results[:5], 1):
        title = r.get("title", "No title")
        url = r.get("url", "")
        out.append(f"{i}. {title}")
        if url:
            out.append(f"   {url}")
        out.append("")
    if total_results > 5:
        out.append(f"... and {total_results - 5} more results.")
    return "\n".join(out)

def _format_calculator_result(data: Dict[str, Any]) -> str:
    return f"Calculation result: {data.get('expression','')} = {data.get('result','')}"

def _format_echo_result(data: Dict[str, Any]) -> str:
    if isinstance(data, dict) and "content" in data:
        for item in data.get("content", []) or []:
            if isinstance(item, dict) and item.get("type") == "text":
                return f"Echo: {item.get('text','')}"
        return f"Echo result: {str(data)}"
    return f"Echo: {data.get('text','')}"

def _format_mcp_content_result(tool_name: str, data: Dict[str, Any]) -> str:
    if "content" in data:
        content_list = data.get("content") or []
    elif "success" in data:
        if data.get("success"):
            content_list = data.get("content") or []
        else:
            return f"Tool '{tool_name}' failed: {data.get('error', 'Unknown error')}"
    else:
        return f"Tool '{tool_name}' result: {str(data)}"

    if not content_list:
        return f"Tool '{tool_name}' completed but returned no content."

    texts: List[str] = []
    for item in content_list:
        if isinstance(item, dict) and item.get("type") == "text":
            texts.append(item.get("text", ""))
        elif isinstance(item, str):
            texts.append(item)
    return f"Tool '{tool_name}' result: {' '.join(texts) if texts else f'{len(content_list)} content items.'}"

def _format_json_result(tool_name: str, data: Dict[str, Any]) -> str:
    if tool_name == "web-search.web_search":
        return _format_web_search_result(data)
    if tool_name == "calculator.calculate":
        return _format_calculator_result(data)
    if tool_name == "echo.echo":
        return _format_echo_result(data)
    return json.dumps(data, indent=2)

def _format_tool_result_for_display(tool_name: str, result: Any) -> str:
    """Format tool results into user-friendly messages."""
    try:
        if isinstance(result, dict):
            # Handle MCP tool results
            if "success" in result and "content" in result:
                if result["success"]:
                    return _format_mcp_content_result(tool_name, result)
                else:
                    return f"Sorry, the {tool_name} tool failed: {result.get('error', 'Unknown error')}"

            # Handle structured results
            if "result" in result:
                # Calculator result
                if tool_name == "calculator.calculate":
                    return f"The calculation result is: {result['result']}"

            # Handle content arrays
            if "content" in result and isinstance(result["content"], list):
                return _format_mcp_content_result(tool_name, result)

            # Fallback to JSON formatting
            return _format_json_result(tool_name, result)

        if isinstance(result, str):
            try:
                parsed = json.loads(result)
                return _format_tool_result_for_display(tool_name, parsed)
            except json.JSONDecodeError:
                return result

        return str(result)
    except Exception as e:
        return f"I encountered an error processing the tool result: {e}"

# ---------- Workflow state ----------

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
    prompt_queue: Deque[str] = field(default_factory=deque)
    last_response_id: str = ""
    memory: ConversationMemory = field(default_factory=ConversationMemory)

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
        if self.state.pending_tool_call and self.state.pending_tool_call.id == tool_call_id and approved:
            if edited_args:
                self.state.pending_tool_call.args = edited_args
        # Clear the gate whether approved or rejected; activities decide behavior
        self.state.pending_tool_call = None

    @workflow.signal
    async def end_conversation(self):
        self.state.done = True

    # ---------- Queries ----------
    @workflow.query
    def get_conversation_history(self) -> List[Message]:
        return list(self.state.memory.short_term)

    # ---------- Updates ----------
    @workflow.update
    async def user_turn(self, msg: Message) -> TurnResult:
        """
        Append user message, drive orchestration until either:
        - assistant message produced → return it
        - tool approval requested → return pending_tool
        """
        # Append user message + record turn
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

        self.state.prompt_queue.append(msg.content)
        self.state.turns += 1

        # Baseline index for assistant detection
        base_idx = len(self.state.memory.short_term)

        # Wait until assistant appears or a new pending tool is requested or done
        def _ready() -> bool:
            if self.state.done:
                return True
            if self.state.pending_tool_call is not None:
                return True
            # assistant after base_idx-1 (since we appended user already)
            return any(m.role == "assistant" for m in self.state.memory.short_term[base_idx:])

        await workflow.wait_condition(_ready)

        if self.state.pending_tool_call is not None:
            return TurnResult(pending_tool=self.state.pending_tool_call)

        # Return the first assistant message after base_idx
        for m in self.state.memory.short_term[base_idx:]:
            if m.role == "assistant":
                return TurnResult(assistant=m)

        # If ended without producing a reply
        return TurnResult(assistant=Message(role="assistant", content="(conversation ended)", ts=workflow.now().timestamp()))

    @workflow.update
    async def wait_for_assistant(self) -> Message:
        """
        Wait for the next assistant message after the call is made.
        Useful immediately after sending a tool approval.
        """
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

    # ---------- Main orchestration loop ----------
    @workflow.run
    async def run(self, goal: str):
        self.state.conversation_id = workflow.info().workflow_id

        # Discover tools once
        discovery = await workflow.execute_activity(
            "discover_mcp_tools",
            args=[],
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )
        if not discovery.get("success"):
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
            # Wait until there's a user prompt to process (or end)
            await workflow.wait_condition(lambda: bool(self.state.prompt_queue) or self.state.done)
            if self.state.done:
                break

            prompt = self.state.prompt_queue.popleft()
            workflow.logger.info(f"Processing user prompt: {prompt[:80]}")

            # Decide next action
            action_dict: dict = await workflow.execute_activity(
                "decision_agents_activity",
                args=[self.state.view_for_llm()],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            action = AssistantAction(**action_dict)

            # Optional: track last_response_id if provided
            if "last_response_id" in action_dict:
                self.state.last_response_id = action_dict["last_response_id"]

            if action.type == "assistant_message":
                if action.message:
                    self._append_assistant(action.message)

            elif action.type == "revise_plan" and action.plan_diff:
                self.state.plan = action.plan_diff

            elif action.type == "tool_call" and action.call:
                call = action.call

                # Approval gating
                if call.requires_approval:
                    self.state.pending_tool_call = call
                    await workflow.wait_condition(lambda: self.state.pending_tool_call is None or self.state.done)
                    if self.state.done:
                        break
                    # call may have updated args via approve signal

                # Execute tool
                raw = await workflow.execute_activity(
                    "tool_dispatch",
                    args=[call],
                    heartbeat_timeout=timedelta(seconds=30),
                    start_to_close_timeout=timedelta(minutes=10),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )
                tool_result = StructuredToolResult(**raw) if isinstance(raw, dict) else raw

                # Store a readable tool result as an assistant message
                if tool_result.success:
                    formatted = _format_tool_result_for_display(call.name, tool_result.data)
                    self._append_assistant(Message(role="assistant", content=formatted, ts=workflow.now().timestamp()))
                else:
                    self._append_assistant(
                        Message(
                            role="assistant",
                            content=f"Tool '{call.name}' failed: {tool_result.error}",
                            ts=workflow.now().timestamp(),
                        )
                    )

                # Follow-up response after tool
                response_action_dict: dict = await workflow.execute_activity(
                    "decision_agents_activity",
                    args=[self.state.view_for_llm()],
                    start_to_close_timeout=timedelta(minutes=2),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )
                response_action = AssistantAction(**response_action_dict)
                if response_action.type == "assistant_message" and response_action.message:
                    self._append_assistant(response_action.message)

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
                workflow.continue_as_new(goal)

    # ---------- Helpers ----------
    def _append_assistant(self, msg: Message) -> None:
        self.state.memory.short_term.append(msg)
        if len(self.state.memory.short_term) > 50:
            self.state.memory.short_term = self.state.memory.short_term[-50:]
