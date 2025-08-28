from __future__ import annotations

"""Lightweight dataclasses for registry definitions.

These structures describe tools and agent goals in a serialisable format so
that registries can reference them as keys.  The dataclasses are frozen to
allow instances to be used as dictionary keys.
"""

from dataclasses import dataclass, asdict
from typing import Tuple


@dataclass(frozen=True)
class ToolArgument:
    """Description of a single tool argument."""

    name: str
    type: str
    description: str
    required: bool = True

    def to_dict(self) -> dict:
        """Return a serialisable representation of the argument."""
        return asdict(self)


@dataclass(frozen=True)
class ToolDefinition:
    """Definition for a callable tool."""

    name: str
    description: str
    arguments: Tuple[ToolArgument, ...] = ()

    def to_dict(self) -> dict:
        """Return a serialisable representation of the tool."""
        return {
            "name": self.name,
            "description": self.description,
            "arguments": [arg.to_dict() for arg in self.arguments],
        }


@dataclass(frozen=True)
class AgentGoal:
    """Represents a high level goal available to the agent."""

    name: str
    description: str

    def to_dict(self) -> dict:
        """Return a serialisable representation of the goal."""
        return asdict(self)
