# ──────────────────────────────────────────────────────────────────────────────
# File: src/tools/registry.py
# Tool registry + dispatcher (Activities call these)
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from typing import Any, Dict, Callable

# Example tool implementations (replace with real MCP/OpenAPI clients)

def tool_search_flights(**kwargs) -> Dict[str, Any]:
    # pretend to call a flight API and return an artifact reference
    return {"artifact_ref": f"flight:{kwargs.get('from','')}->{kwargs.get('to','')}:{kwargs.get('date','')}"}

def tool_search_hotels(**kwargs) -> Dict[str, Any]:
    return {"artifact_ref": f"hotel:{kwargs.get('city','')}:{kwargs.get('checkin','')}"}

def tool_book_cab(**kwargs) -> Dict[str, Any]:
    return {"artifact_ref": f"cab:{kwargs.get('city','')}:{kwargs.get('time','')}"}

def tool_find_events(**kwargs) -> Dict[str, Any]:
    return {"artifact_ref": f"event:{kwargs.get('city','')}:{kwargs.get('date','')}"}

TOOLS: Dict[str, Callable[..., Dict[str, Any]]] = {
    "SearchFlights": tool_search_flights,
    "SearchHotels": tool_search_hotels,
    "RideShareReserve": tool_book_cab,
    "FindEvents": tool_find_events,
}

# A JSON-schema suitable for exposing to the model (simplified)
TOOL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    name: {
        "type": "function",
        "name": name,
        "description": f"Invoke {name}",
        "parameters": {"type": "object", "properties": {}, "additionalProperties": True},
    }
    for name in TOOLS.keys()
}
