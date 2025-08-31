from __future__ import annotations
import asyncio
import os
from pathlib import Path
from temporalio.client import Client
from temporalio.worker import Worker
from src.config import settings, apply_openai_env_from_settings
from src.otel import setup_tracing
from src.workflows.agent_orchestrator import AgentOrchestratorWorkflow
from src.workflows.subagent import SubAgentWorkflow
from src.activities.plan import plan_activity
from src.activities.decision_agents import decision_agents_activity
from src.activities.tool_dispatch import tool_dispatch, discover_mcp_tools
from src.activities.vfs import vfs_put
from src.activities.summarize import summarize_activity
from src.activities.transcript import append_transcript
from src.activities.guardrail import guardrail_check
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin, ModelActivityParameters
from temporalio.contrib.pydantic import pydantic_data_converter

async def main():
    # Load .env files at process start (outside workflow sandbox)
    try:
        from dotenv import load_dotenv
        for f in (".env", ".env.local"):
            p = Path(f)
            if p.exists():
                load_dotenv(p)
    except Exception:
        pass
    setup_tracing(settings.otel_service_name_worker, settings.otel_endpoint)
    # Disable OpenAI Agents SDK tracing when using Azure keys for models to avoid 401s,
    # unless an explicit OpenAI tracing key is provided.
    try:
        from agents import set_tracing_disabled, set_tracing_export_api_key  # type: ignore
        # Default: disable Agents SDK tracing to avoid 401s when using Azure keys for models.
        tracing_flag = (os.getenv("OPENAI_AGENTS_DISABLE_TRACING", "1") or "1").strip().lower()
        if tracing_flag in ("1", "true", "yes", "on"):
            set_tracing_disabled(True)
        else:
            # Only enable tracing if an explicit OpenAI tracing key is provided.
            tracing_key = os.getenv("OPENAI_AGENTS_EXPORT_API_KEY")
            if tracing_key:
                set_tracing_export_api_key(tracing_key)
            else:
                set_tracing_disabled(True)
    except Exception:
        # If agents SDK isn't available for any reason, continue without changing tracing
        pass

    # Configure OpenAI Agents plugin. Default ModelActivityParameters will set a 60s
    # start_to_close timeout for model calls if none is provided.
    agents_plugin = OpenAIAgentsPlugin(
        model_params=ModelActivityParameters()
    )

    # Project configured Azure/OpenAI settings into env for plugins/clients
    apply_openai_env_from_settings()

    # Attach the plugin to the client so data conversion and tracing are configured.
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
    # build_id="v1",  # enable Worker Versioning when ready
    )
    print(f"Worker started on queue {settings.task_queue}")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
