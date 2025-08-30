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
    goal = context.get('goal', '')

    # Enhanced planning with hierarchical decomposition
    system = (
        "You are an expert planning assistant for complex task decomposition. "
        "Create a detailed, hierarchical plan with the following structure:\n\n"
        "PRIMARY GOAL: Break down the user's goal into 3-5 major sub-goals\n\n"
        "For each sub-goal, provide:\n"
        "- id: Unique identifier (sg1, sg2, etc.)\n"
        "- title: Clear, actionable title\n"
        "- description: Detailed explanation of what this sub-goal achieves\n"
        "- priority: 1-5 (5 being highest priority)\n"
        "- estimated_effort: 'quick', 'medium', or 'complex'\n"
        "- dependencies: List of sub-goal IDs that must be completed first\n"
        "- success_criteria: How to measure completion\n"
        "- tools_needed: List of tools or capabilities required\n\n"
        "Return ONLY a JSON object with this structure:\n"
        "{\n"
        "  \"primary_goal\": \"[restated goal]\",\n"
        "  \"subgoals\": [\n"
        "    {\n"
        "      \"id\": \"sg1\",\n"
        "      \"title\": \"...\",\n"
        "      \"description\": \"...\",\n"
        "      \"priority\": 3,\n"
        "      \"estimated_effort\": \"medium\",\n"
        "      \"dependencies\": [],\n"
        "      \"success_criteria\": \"...\",\n"
        "      \"tools_needed\": [\"tool1\", \"tool2\"]\n"
        "    }\n"
        "  ],\n"
        "  \"replan_triggers\": [\"user_feedback\", \"tool_failures\", \"new_requirements\"]\n"
        "}\n\n"
        "Focus on creating logical dependencies and realistic effort estimates."
    )

    user = f"Goal: {goal}\n\nCreate a detailed hierarchical plan breaking this down into manageable sub-goals with dependencies and success criteria."

    with tracer.start_as_current_span("plan_activity") as span:
        span.set_attribute("temporal.workflow_id", ai.workflow_id)
        span.set_attribute("temporal.run_id", ai.workflow_run_id)
        span.set_attribute("temporal.attempt", ai.attempt)
        try:
            data = llm_json(system, user, settings.llm_model_plan)

            # Handle the new hierarchical planning format
            if isinstance(data, dict) and "subgoals" in data:
                # Convert hierarchical plan to simple PlanItem format for backward compatibility
                items = []
                for i, subgoal in enumerate(data["subgoals"]):
                    # Create a PlanItem from each sub-goal
                    plan_item = PlanItem(
                        id=str(i + 1),
                        title=subgoal["title"],
                        status="todo",
                        tool_hints=subgoal.get("tools_needed", [])
                    )
                    items.append(plan_item)

                # Store the full hierarchical context for future use
                # This would be enhanced in future versions to use the full PlanningContext

                return [pi.model_dump() for pi in items]
            else:
                # Fallback to original format
                items = data if isinstance(data, list) else data.get("plan", [])
                normalized: List[PlanItem] = []
                for it in items:
                    if isinstance(it, PlanItem):
                        normalized.append(it)
                    else:
                        normalized.append(PlanItem(**it))
                return [pi.model_dump() for pi in normalized]

        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise
