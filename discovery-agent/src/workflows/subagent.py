from __future__ import annotations
from temporalio import workflow

@workflow.defn
class SubAgentWorkflow:
    @workflow.run
    async def run(self, spec: dict) -> dict:
        # Placeholder for specialized child workflows
        return {"ok": True, "artifact_ref": None}
