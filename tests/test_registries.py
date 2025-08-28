import sys
from pathlib import Path
from dataclasses import asdict

# Make registry modules importable
sys.path.append(str(Path(__file__).resolve().parents[1] / "discovery-agent/temporal"))

import registries
import tool_registry
import goal_registry


def _get_tool_def(name: str):
    for td in tool_registry.TOOL_REGISTRY:
        if td.name == name:
            return td
    raise KeyError(name)


def _get_goal(name: str):
    for goal in goal_registry.GOAL_REGISTRY:
        if goal.name == name:
            return goal
    raise KeyError(name)


def test_tool_registry_lookup_and_serialisation():
    add_def = _get_tool_def("add")
    handler = tool_registry.TOOL_REGISTRY[add_def]
    assert handler(2, 3) == 5

    data = asdict(add_def)
    assert data["name"] == "add"
    assert data["arguments"][0]["name"] == "a"
    assert data["arguments"][1]["name"] == "b"

    arg_data = asdict(add_def.arguments[0])
    assert arg_data == {
        "name": "a",
        "type": "int",
        "description": "First integer",
        "required": True,
    }


def test_goal_registry_lookup_and_serialisation():
    goal = _get_goal("write_docs")
    prompt = goal_registry.GOAL_REGISTRY[goal]
    assert "documentation" in prompt.lower()

    data = asdict(goal)
    assert data == {
        "name": "write_docs",
        "description": "Produce or update project documentation",
    }
