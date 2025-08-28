"""Temporal workflow managing an interactive DeepAgent session.

This module rewrites the previous minimal workflow to support a prompt queue,
conversation history, and a remaining-turn limit.  External callers can send
new prompts or confirm tool executions via workflow signals.  The workflow is
able to expose its current conversation transcript and the most recent tool
interaction through queries.

After a configurable number of turns the workflow will issue
``continue_as_new`` with the current state so that long chats can proceed
without growing execution history unbounded.
"""

from __future__ import annotations

from datetime import timedelta
from importlib import import_module
from typing import TYPE_CHECKING, Any, Dict, List, Sequence, Tuple
import logging

from temporalio import activity, workflow

if TYPE_CHECKING:  # pragma: no cover - hints only
    from langchain_core.tools import BaseTool


def create_deep_agent(*args, **kwargs):  # pragma: no cover - runtime import
    from deep_agent import create_deep_agent as _create
    return _create(*args, **kwargs)


def _load_tool(spec: str) -> "BaseTool":
    """Resolve a ``module:attr`` spec to a ``BaseTool`` instance."""

    from langchain_core.tools import BaseTool  # Imported lazily for sandboxing

    module_name, attr_name = spec.split(":", 1)
    module = import_module(module_name)
    obj = getattr(module, attr_name)
    if isinstance(obj, BaseTool):
        return obj
    if callable(obj):
        tool_obj = obj()
        if isinstance(tool_obj, BaseTool):
            return tool_obj
    raise TypeError(f"{spec} did not resolve to a BaseTool")


@activity.defn
async def run_query(
    question: str,
    instructions: str = "",
    tools: Sequence[str] | None = None,
    mcp_endpoints: Sequence[str] | None = None,
) -> Tuple[str, Dict[str, Any] | None]:
    """Execute the DeepAgent and return its response and any tool request."""
    _alog = getattr(activity, "logger", None) or logging.getLogger(__name__)
    _alog.info(
        "activity.run_query.start",
        extra={
            "question_len": len(question or ""),
            "instructions_len": len(instructions or ""),
            "tools_count": len(tools) if tools else 0,
            "mcp_endpoints_count": len(mcp_endpoints) if mcp_endpoints else 0,
        },
    )
    latest_tool: Dict[str, Any] | None = None

    async def _on_tool_call(name: str, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        nonlocal latest_tool
        latest_tool = {"name": name, "args": data}
        # Disallow execution; the workflow will confirm separately.
        _alog.info(
            "activity.run_query.tool_requested",
            extra={"tool_name": name, "arg_keys": list(data.keys())},
        )
        return False, data

    tool_objs = [_load_tool(t) for t in tools] if tools else None

    try:
        agent = create_deep_agent(
            tools=tool_objs,
            mcp_endpoints=mcp_endpoints,
            on_tool_call=_on_tool_call,
        )
        response = await agent(question, instructions)
        _alog.info(
            "activity.run_query.completed",
            extra={"tool_requested": bool(latest_tool)},
        )
        return response, latest_tool
    except Exception:
        _alog.exception("activity.run_query.error")
        raise


@workflow.defn
class DeepAgentWorkflow:
    """Workflow that orchestrates an interactive DeepAgent session."""

    def __init__(self) -> None:  # pragma: no cover - exercised in tests
        self.prompt_queue: List[str] = []
        self.conversation_history: List[Dict[str, str]] = []
        self.latest_tool_data: Dict[str, Any] | None = None
        self._awaiting_confirmation = False
        self._chat_ended = False

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------
    @workflow.signal
    def user_prompt(self, prompt: str) -> None:
        """Add a new user prompt to the queue."""
        workflow.logger.info(
            "signal.user_prompt",
            extra={"prompt_len": len(prompt or "")},
        )
        self.prompt_queue.append(prompt)

    @workflow.signal
    def confirm(self, data: Dict[str, Any] | None = None) -> None:
        """Confirm the last tool call and optionally supply result data."""
        workflow.logger.info(
            "signal.confirm",
            extra={"has_data": data is not None, "data_keys": list(data.keys()) if isinstance(data, dict) else None},
        )
        self.latest_tool_data = data
        self._awaiting_confirmation = False

    @workflow.signal
    def end_chat(self) -> None:
        """Terminate the chat loop."""
        workflow.logger.info("signal.end_chat")
        self._chat_ended = True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    @workflow.query
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Return the accumulated conversation messages."""

        return list(self.conversation_history)

    @workflow.query
    def get_latest_tool_data(self) -> Dict[str, Any] | None:
        """Return data associated with the most recent tool call."""

        return self.latest_tool_data

    # ------------------------------------------------------------------
    # Workflow run
    # ------------------------------------------------------------------
    @workflow.run
    async def run(
        self,
        question: str | None = None,
        instructions: str = "",
        tools: Sequence[str] | None = None,
        mcp_endpoints: Sequence[str] | None = None,
        *,
        conversation_history: List[Dict[str, str]] | None = None,
        remaining_turns: int = 20,
        continue_after: int = 50,
        prompt_queue: List[str] | None = None,
    ) -> List[Dict[str, str]]:  # pragma: no cover - workflow entrypoint
        """Run the chat loop until exhausted or ``end_chat`` is signalled."""
        info = workflow.info()
        workflow.logger.info(
            "workflow.run.start",
            extra={
                "workflow_id": info.workflow_id,
                "run_id": info.run_id,
                "initial_prompt_present": question is not None,
                "tools_count": len(tools) if tools else 0,
                "mcp_endpoints_count": len(mcp_endpoints) if mcp_endpoints else 0,
                "remaining_turns": remaining_turns,
                "continue_after": continue_after,
            },
        )
        self.prompt_queue = list(prompt_queue or [])
        if question:
            self.prompt_queue.append(question)
        self.conversation_history = conversation_history or []
        self.latest_tool_data = None
        self._awaiting_confirmation = False
        self._chat_ended = False

        turns = 0
        while remaining_turns > 0 and not self._chat_ended:
            # Wait for a prompt to be queued or chat to be ended
            await workflow.wait_condition(
                lambda: bool(self.prompt_queue) or self._chat_ended
            )
            if self._chat_ended or not self.prompt_queue:
                break

            prompt = self.prompt_queue.pop(0)
            self.conversation_history.append({"user": prompt})
            workflow.logger.info(
                "workflow.run.turn_begin",
                extra={"turn": turns + 1, "queue_len": len(self.prompt_queue)},
            )

            response, tool_data = await workflow.execute_activity(
                run_query,
                prompt,
                instructions,
                tools,
                mcp_endpoints,
                schedule_to_close_timeout=timedelta(minutes=1),
            )

            self.conversation_history.append({"assistant": response})
            self.latest_tool_data = tool_data
            workflow.logger.info(
                "workflow.run.turn_end",
                extra={"turn": turns + 1, "tool_requested": tool_data is not None},
            )

            if tool_data is not None:
                self._awaiting_confirmation = True
                workflow.logger.info("workflow.run.awaiting_confirmation")
                await workflow.wait_condition(lambda: not self._awaiting_confirmation)
                workflow.logger.info("workflow.run.confirmation_received")

            remaining_turns -= 1
            turns += 1

            if turns >= continue_after:
                workflow.logger.info(
                    "workflow.run.continue_as_new",
                    extra={"turns": turns, "remaining_turns": remaining_turns},
                )
                return workflow.continue_as_new(
                    None,
                    instructions,
                    tools,
                    mcp_endpoints,
                    conversation_history=self.conversation_history,
                    remaining_turns=remaining_turns,
                    continue_after=continue_after,
                    prompt_queue=list(self.prompt_queue),
                )
        workflow.logger.info(
            "workflow.run.completed",
            extra={"turns": turns, "remaining_turns": remaining_turns, "ended_by_signal": self._chat_ended},
        )
        return self.conversation_history

