from __future__ import annotations

"""Registry of predefined :class:`AgentGoal` objects and their starter prompts."""

from typing import Dict

from registries import AgentGoal

GOAL_REGISTRY: Dict[AgentGoal, str] = {
    AgentGoal(
        name="write_docs",
        description="Produce or update project documentation",
    ): "You are a technical writer tasked with creating clear project documentation.",
    AgentGoal(
        name="fix_bug",
        description="Investigate and resolve issues in the codebase",
    ): "You are a debugging assistant focused on identifying and fixing code bugs.",
}
