from __future__ import annotations
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from discovery_agent.config import settings
from discovery_agent.otel import setup_tracing
from discovery_agent.workflows.agent_orchestrator import AgentOrchestratorWorkflow
from discovery_agent.workflows.subagent import SubAgentWorkflow
from discovery_agent.activities.plan import plan_activity
from discovery_agent.activities.decision_agents import decision_agents_activity
from discovery_agent.activities.tool_dispatch import tool_dispatch
from discovery_agent.activities.vfs import vfs_put
from discovery_agent.activities.summarize import summarize_activity
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin

async def main():
    setup_tracing(settings.otel_service_name_worker, settings.otel_endpoint)
    client = await Client.connect(settings.temporal_target, namespace=settings.temporal_namespace)

    agents_plugin = OpenAIAgentsPlugin(
        default_model=settings.llm_model_decision,
        enable_tracing=True,
    )

    worker = Worker(
        client,
        task_queue=settings.task_queue,
        workflows=[AgentOrchestratorWorkflow, SubAgentWorkflow],
        activities=[plan_activity, decision_agents_activity, tool_dispatch, vfs_put, summarize_activity],
        # build_id="v1",  # enable Worker Versioning when ready
        plugins=[agents_plugin],
    )
    print(f"Worker started on queue {settings.task_queue}")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
