"""Client to start the Temporal workflow that runs the custom DeepAgent."""

import asyncio
from temporalio.client import Client

from temporal_workflow import DeepAgentWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        DeepAgentWorkflow.run,
        "List available banking tables",
        id="deep-agent-workflow-001",
        task_queue="deep-agent-task-queue",
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
