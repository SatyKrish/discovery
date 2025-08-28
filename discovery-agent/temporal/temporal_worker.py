"""Worker to run the Temporal workflow for the custom DeepAgent.

This worker exposes the :class:`~temporal_workflow.DeepAgentWorkflow` along with
utility activities from :class:`~agent_activities.AgentActivities`.  It also
registers a dynamic activity dispatcher so that any tool present in
``TOOL_REGISTRY`` can be invoked directly as an activity.

The Temporal service address, task queue, and LLM settings are loaded from the
environment.  Blocking tool implementations run in a thread pool executor to
avoid stalling the worker's event loop.
"""

from __future__ import annotations

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Sequence

from dotenv import load_dotenv
from temporalio import activity
from temporalio.client import Client
from temporalio.common import RawValue
from temporalio.converter import DataConverter
from temporalio.worker import Worker

from agent_activities import AgentActivities
from tool_registry import TOOL_REGISTRY
from temporal_workflow import DeepAgentWorkflow, run_query

load_dotenv()


# Dynamic dispatcher ---------------------------------------------------------

DATA_CONVERTER = DataConverter.default


@activity.defn(dynamic=True)
def dynamic_tool_dispatcher(values: Sequence[RawValue]) -> object:
    """Dispatch dynamic tool activities based on the activity name.

    The activity name corresponds to a tool in ``TOOL_REGISTRY``.  Arguments are
    expected to be encoded as a single JSON object.
    """
    name = activity.info().activity_type
    try:
        decoded = (
            asyncio.run(DATA_CONVERTER.decode([v.payload for v in values]))
            if values
            else []
        )
    except Exception:
        activity.logger.exception("dynamic_tool_dispatcher.decode_failed", extra={
            "activity_type": name,
            "arg_count": len(values) if values else 0,
        })
        raise

    kwargs = decoded[0] if decoded else {}
    # Avoid logging potentially sensitive argument values. Log only keys.
    activity.logger.info(
        "dynamic_tool_dispatcher.received",
        extra={
            "activity_type": name,
            "arg_keys": list(kwargs.keys()) if isinstance(kwargs, dict) else None,
        },
    )
    for definition, handler in TOOL_REGISTRY.items():
        if definition.name == name:
            try:
                result = handler(**kwargs)
                activity.logger.info(
                    "dynamic_tool_dispatcher.completed",
                    extra={"activity_type": name},
                )
                return result
            except Exception:
                activity.logger.exception(
                    "dynamic_tool_dispatcher.handler_error",
                    extra={"activity_type": name},
                )
                raise
    activity.logger.error("dynamic_tool_dispatcher.unknown_tool", extra={"activity_type": name})
    raise KeyError(f"Unknown tool: {name}")


async def main() -> None:
    """Entry point for running the Temporal worker."""
    # Configure logging level from env; default INFO. Avoid logging secrets.
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO), format="%(asctime)s %(levelname)s %(name)s %(message)s")

    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    task_queue = os.getenv("TEMPORAL_TASK_QUEUE", "deep-agent-task-queue")

    # Access LLM settings so they are loaded from the environment.  The
    # ``openai_model`` module reads these values when imported by activities.
    os.getenv("OPENAI_API_KEY", "")
    os.getenv("OPENAI_MODEL", "")
    logging.getLogger(__name__).info(
        "worker.starting",
        extra={
            "temporal_address": temporal_address,
            "task_queue": task_queue,
            "openai_key_set": bool(os.getenv("OPENAI_API_KEY")),
            "openai_model_set": bool(os.getenv("OPENAI_MODEL")),
        },
    )

    client = await Client.connect(temporal_address)
    logging.getLogger(__name__).info("worker.client_connected", extra={"temporal_address": temporal_address})

    activities = AgentActivities()
    activity_funcs = [
        run_query,
        dynamic_tool_dispatcher,
        activities.agent_toolPlanner,
        activities.agent_validatePrompt,
        activities.get_wf_env_vars,
    ]

    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[DeepAgentWorkflow],
        activities=activity_funcs,
        activity_executor=ThreadPoolExecutor(),
    )
    logging.getLogger(__name__).info(
        "worker.running",
        extra={
            "task_queue": task_queue,
            "workflow_count": 1,
            "activity_count": len(activity_funcs),
        },
    )
    try:
        await worker.run()
    except Exception:
        logging.getLogger(__name__).exception("worker.error")
        raise


if __name__ == "__main__":  # pragma: no cover - manual execution only
    asyncio.run(main())
