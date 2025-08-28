"""Worker to run the Temporal workflow for the custom DeepAgent."""

import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from temporal_workflow import DeepAgentWorkflow, run_query


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="deep-agent-task-queue",
        workflows=[DeepAgentWorkflow],
        activities=[run_query],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
