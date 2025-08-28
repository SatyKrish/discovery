from __future__ import annotations

"""Registry mapping ``ToolDefinition`` objects to their handlers."""

from typing import Callable, Dict

from registries import ToolArgument, ToolDefinition


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def echo(text: str) -> str:
    """Return the provided text verbatim."""
    return text


TOOL_REGISTRY: Dict[ToolDefinition, Callable] = {
    ToolDefinition(
        name="add",
        description="Add two integers",
        arguments=(
            ToolArgument("a", "int", "First integer"),
            ToolArgument("b", "int", "Second integer"),
        ),
    ): add,
    ToolDefinition(
        name="echo",
        description="Echo back the supplied text",
        arguments=(ToolArgument("text", "str", "Text to echo"),),
    ): echo,
}
