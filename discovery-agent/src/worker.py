from __future__ import annotations
import asyncio
import os
from pathlib import Path
from temporalio.client import Client
from temporalio.worker import Worker
from src.config import settings
from src.otel import setup_tracing
from src.workflows.agent_orchestrator import AgentOrchestratorWorkflow
from src.workflows.subagent import SubAgentWorkflow
from src.activities.plan import plan_activity
from src.activities.decision_agents import decision_agents_activity
from src.activities.tool_dispatch import tool_dispatch
from src.activities.vfs import vfs_put
from src.activities.summarize import summarize_activity
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin, ModelActivityParameters

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
    # Configure OpenAI Agents plugin. Default ModelActivityParameters will set a 60s
    # start_to_close timeout for model calls if none is provided.
    agents_plugin = OpenAIAgentsPlugin(
        model_params=ModelActivityParameters()
    )

    # Ensure OpenAI client env vars are present for the Agents plugin (supports Ollama)
    if settings.openai_base_url and not os.environ.get("OPENAI_BASE_URL"):
        os.environ["OPENAI_BASE_URL"] = settings.openai_base_url
    if not os.environ.get("OPENAI_API_KEY"):
        # Use configured key or a dummy value for local providers like Ollama
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key or "ollama"

    # Attach the plugin to the client so data conversion and tracing are configured.
    client = await Client.connect(
        settings.temporal_target,
        namespace=settings.temporal_namespace,
        plugins=[agents_plugin],
    )

    worker = Worker(
        client,
        task_queue=settings.task_queue,
        workflows=[AgentOrchestratorWorkflow, SubAgentWorkflow],
    activities=[plan_activity, decision_agents_activity, tool_dispatch, vfs_put, summarize_activity],
    # build_id="v1",  # enable Worker Versioning when ready
    )
    print(f"Worker started on queue {settings.task_queue}")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
