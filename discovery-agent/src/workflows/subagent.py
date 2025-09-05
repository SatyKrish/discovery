# ──────────────────────────────────────────────────────────────────────────────
# File: src/workflows/subagent.py
# Dynamic child workflow using Temporal OpenAI Agents SDK + MCP
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
import json
from datetime import timedelta
from typing import List
from temporalio import workflow
from temporalio.common import RetryPolicy

from agents import Agent, Runner

from src.config import settings
from src.models_subagent import SubAgentSpec, SubAgentResult

@workflow.defn
class SubAgentWorkflow:
    def __init__(self):
        self._extra_tools: List[str] = []

    # Parent → child: grant more tools
    @workflow.signal
    async def grant_tool_access(self, tools: List[str]):
        for t in tools:
            if t not in self._extra_tools:
                self._extra_tools.append(t)

    @workflow.run
    async def run(self, spec: SubAgentSpec) -> SubAgentResult:
        artifacts: List[str] = []
        deadline = workflow.now() + timedelta(minutes=spec.timeout_minutes)

        # Resolve instructions: prefer prompt pack if provided
        instructions = (spec.instructions or "").strip()
        if not instructions and spec.instructions_ref:
            got = await workflow.execute_activity(
                "get_prompt",
                spec.instructions_ref,
                start_to_close_timeout=timedelta(seconds=20),
                retry_policy=RetryPolicy(maximum_attempts=2),
            )
            if isinstance(got, dict) and got.get("success"):
                pack = got
                instructions = (pack.get("text") or "").strip()
                # If the pack suggests additional tools, request approval from parent
                suggested = [t for t in (pack.get("tools") or []) if t not in (spec.allowed_tools or [])]
                if suggested and (spec.parent_workflow_id or workflow.info().parent_workflow_id):
                    handle = workflow.get_external_workflow_handle(spec.parent_workflow_id or workflow.info().parent_workflow_id)
                    await handle.signal("request_tool_access", workflow.info().workflow_id, suggested, "Prompt-pack suggested tools")

        allowed = list(spec.allowed_tools)

        # System prompt explains: only allowed tools; request new tools via JSON
        sys = (instructions or
               "You are a specialist subagent. Use only tools listed in allowed_tools. "
               "If you need additional tools, reply with a single JSON object: "
               "{\"request_tools\":[\"provider/tool\",...],\"rationale\":\"...\"}. "
               "When complete, reply with the word DONE in your assistant message.")

        msgs = [
            {"role": "system", "content": json.dumps({"instructions": sys, "allowed_tools": allowed}, ensure_ascii=False)},
            {"role": "user", "content": json.dumps({"args": spec.input_args}, ensure_ascii=False)},
        ]

        # Let the OpenAI Agents SDK + Temporal integration handle tool activities automatically
        agent = Agent(
            name=f"{spec.kind} subagent",
            instructions="Follow the JSON provided in system content exactly.",
            tools=[],  # Tools will be handled automatically by the integration
        )

        while workflow.now() < deadline:
            result = await Runner.run(agent, msgs, max_turns=4)

            txt = (result.final_output or "").strip() if hasattr(result, "final_output") else ""
            if txt:
                # Check for an in-band tool request JSON
                try:
                    maybe = json.loads(txt)
                    if isinstance(maybe, dict) and "request_tools" in maybe:
                        needed = [t for t in maybe["request_tools"] if t not in allowed]
                        if needed and (spec.parent_workflow_id or workflow.info().parent_workflow_id):
                            handle = workflow.get_external_workflow_handle(spec.parent_workflow_id or workflow.info().parent_workflow_id)
                            await handle.signal("request_tool_access", workflow.info().workflow_id, needed, maybe.get("rationale",""))
                            # Wait for approval
                            await workflow.wait_condition(lambda: any(t in self._extra_tools for t in needed), timeout=timedelta(minutes=spec.timeout_minutes))
                            for t in self._extra_tools:
                                if t not in allowed:
                                    allowed.append(t)
                            msgs.append({"role":"system","content":json.dumps({"granted_tools": self._extra_tools})})
                            continue
                except Exception:
                    pass

                msgs.append({"role": "assistant", "content": txt})
                if "DONE" in txt.upper():
                    return SubAgentResult(ok=True, artifact_refs=artifacts, message=txt)

            # Collect artifacts if your MCP tools return {"artifact_ref": "..."}
            for item in getattr(result, "new_items", []) or []:
                out = getattr(item, "tool_output", None)
                if isinstance(out, dict) and out.get("artifact_ref"):
                    artifacts.append(out["artifact_ref"])

            # Keep the model informed of the latest allowed tools
            msgs.append({"role": "system", "content": json.dumps({"allowed_tools": allowed})})

        return SubAgentResult(ok=bool(artifacts), artifact_refs=artifacts, message="timeout")
