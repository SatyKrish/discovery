from __future__ import annotations

import asyncio
import os
from pathlib import Path

from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin, ModelActivityParameters
from temporalio.contrib.pydantic import pydantic_data_converter

from src.config import settings, apply_openai_env_from_settings
from src.otel import setup_tracing
from src.workflows.agent_orchestrator import AgentOrchestratorWorkflow
from src.workflows.subagent import SubAgentWorkflow
from src.activities import (
    plan_activity,
    decision_agents_activity,
    tool_dispatch,
    discover_mcp_tools,
    summarize_activity,
    append_transcript,
    guardrail_check,
    vfs_put,
)


async def main():
    # Load environment overrides (dev)
    try:
        from dotenv import load_dotenv
        for f in (".env", ".env.local"):
            p = Path(f)
            if p.exists():
                load_dotenv(p)
    except Exception:
        pass

    setup_tracing(settings.otel_service_name_worker, settings.otel_endpoint)

    # Configure Agents plugin (keeps model calls as Activities)
    agents_plugin = OpenAIAgentsPlugin(model_params=ModelActivityParameters())

    # Project OpenAI/Azure params into env for Activities
    apply_openai_env_from_settings()

    client = await Client.connect(
        settings.temporal_target,
        namespace=settings.temporal_namespace,
        plugins=[agents_plugin],
        data_converter=pydantic_data_converter,
    )

    worker = Worker(
        client,
        task_queue=settings.task_queue,
        workflows=[AgentOrchestratorWorkflow, SubAgentWorkflow],
        activities=[
            plan_activity,
            decision_agents_activity,
            tool_dispatch,
            discover_mcp_tools,
            vfs_put,
            summarize_activity,
            append_transcript,
            guardrail_check,
        ],
        # build_id="v1",  # enable Worker Versioning in prod
    )

    print(f"Worker started on queue {settings.task_queue}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
