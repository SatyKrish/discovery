from __future__ import annotations
from typing import List, Dict, Any
from temporalio import activity
from src.models import PlanItem
from src.llm import llm_json
from src.config import settings
from src.otel import get_tracer
from opentelemetry.trace import Status, StatusCode

tracer = get_tracer(__name__)

@activity.defn
async def plan_activity(context: dict) -> List[Dict[str, Any]]:
    ai = activity.info()
    system = (
        "You are a planning assistant. Return ONLY a JSON list of PlanItem with fields: "
        "id,title,status (todo|doing|done),tool_hints[]."
    )
    user = f"Goal: {context.get('goal','')}. Produce 3-5 actionable steps."
    with tracer.start_as_current_span("plan_activity") as span:
        span.set_attribute("temporal.workflow_id", ai.workflow_id)
        span.set_attribute("temporal.run_id", ai.workflow_run_id)
        span.set_attribute("temporal.attempt", ai.attempt)
        try:
            data = llm_json(system, user, settings.llm_model_plan)
            items = data if isinstance(data, list) else data.get("plan", [])
            # Ensure PlanItem instances
            normalized: List[PlanItem] = []
            for it in items:
                if isinstance(it, PlanItem):
                    normalized.append(it)
                else:
                    normalized.append(PlanItem(**it))
            # Return JSON-serializable payload to the workflow
            return [pi.model_dump() for pi in normalized]
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise
