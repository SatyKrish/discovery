#!/usr/bin/env python3
"""
Test activities functionality
"""

import sys
import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from src.models import PlanItem


@pytest.mark.asyncio
async def test_plan_activity_basic():
    """Test basic plan activity functionality"""
    from src.activities.plan import plan_activity

    mock_context = {"goal": "Create a simple web application"}

    # Mock LLM response for basic planning
    mock_response = [
        {
            "id": "1",
            "title": "Set up project structure",
            "status": "todo",
            "tool_hints": ["file_system"]
        },
        {
            "id": "2",
            "title": "Create HTML template",
            "status": "todo",
            "tool_hints": ["html", "css"]
        }
    ]

    # Mock Temporal activity context
    mock_activity_info = MagicMock()
    mock_activity_info.workflow_id = "test-wf-123"
    mock_activity_info.run_id = "test-run-456"
    mock_activity_info.attempt = 1

    with patch('src.activities.plan.llm_json', return_value=mock_response) as mock_llm, \
         patch('temporalio.activity.info', return_value=mock_activity_info), \
         patch('src.activities.plan.get_tracer') as mock_tracer:

        mock_span = MagicMock()
        mock_tracer.return_value.start_as_current_span.return_value.__enter__ = mock_span
        mock_tracer.return_value.start_as_current_span.return_value.__exit__ = MagicMock()

        result = await plan_activity(mock_context)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["title"] == "Set up project structure"
        assert result[1]["title"] == "Create HTML template"

        # Verify LLM was called with correct parameters
        mock_llm.assert_called_once()
        call_args = mock_llm.call_args
        # call_args[0] contains positional args, call_args[1] contains keyword args
        user_arg = call_args[1].get("user", call_args[0][1] if len(call_args[0]) > 1 else "")
        assert "Create a simple web application" in user_arg


@pytest.mark.asyncio
async def test_plan_activity_hierarchical():
    """Test plan activity with hierarchical planning response"""
    from src.activities.plan import plan_activity

    mock_context = {"goal": "Build a complex application"}

    # Mock hierarchical planning response
    mock_response = {
        "primary_goal": "Build a complex application",
        "subgoals": [
            {
                "id": "sg1",
                "title": "Design system architecture",
                "description": "Create detailed system design",
                "priority": 5,
                "estimated_effort": "complex",
                "dependencies": [],
                "success_criteria": "Architecture document completed",
                "tools_needed": ["design_tools", "documentation"]
            },
            {
                "id": "sg2",
                "title": "Implement core features",
                "description": "Build the main functionality",
                "priority": 4,
                "estimated_effort": "complex",
                "dependencies": ["sg1"],
                "success_criteria": "Core features working",
                "tools_needed": ["programming", "testing"]
            }
        ],
        "replan_triggers": ["user_feedback", "tool_failures"]
    }

    # Mock Temporal activity context
    mock_activity_info = MagicMock()
    mock_activity_info.workflow_id = "test-wf-123"
    mock_activity_info.run_id = "test-run-456"
    mock_activity_info.attempt = 1

    with patch('src.activities.plan.llm_json', return_value=mock_response) as mock_llm, \
         patch('temporalio.activity.info', return_value=mock_activity_info), \
         patch('src.activities.plan.get_tracer') as mock_tracer:

        mock_span = MagicMock()
        mock_tracer.return_value.start_as_current_span.return_value.__enter__ = mock_span
        mock_tracer.return_value.start_as_current_span.return_value.__exit__ = MagicMock()

        result = await plan_activity(mock_context)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "1"  # Converted from sg1
        assert result[0]["title"] == "Design system architecture"
        assert result[0]["tool_hints"] == ["design_tools", "documentation"]
        assert result[1]["id"] == "2"  # Converted from sg2
        assert result[1]["title"] == "Implement core features"


@pytest.mark.asyncio
async def test_plan_activity_fallback():
    """Test plan activity fallback to original format"""
    from src.activities.plan import plan_activity

    mock_context = {"goal": "Simple task"}

    # Mock response in original format
    mock_response = {
        "plan": [
            PlanItem(id="1", title="Step 1", status="todo", tool_hints=["tool1"]),
            PlanItem(id="2", title="Step 2", status="todo", tool_hints=["tool2"])
        ]
    }

    # Mock Temporal activity context
    mock_activity_info = MagicMock()
    mock_activity_info.workflow_id = "test-wf-123"
    mock_activity_info.run_id = "test-run-456"
    mock_activity_info.attempt = 1

    with patch('src.activities.plan.llm_json', return_value=mock_response) as mock_llm, \
         patch('temporalio.activity.info', return_value=mock_activity_info), \
         patch('src.activities.plan.get_tracer') as mock_tracer:

        mock_span = MagicMock()
        mock_tracer.return_value.start_as_current_span.return_value.__enter__ = mock_span
        mock_tracer.return_value.start_as_current_span.return_value.__exit__ = MagicMock()

        result = await plan_activity(mock_context)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["title"] == "Step 1"
        assert result[1]["title"] == "Step 2"


@pytest.mark.asyncio
async def test_plan_activity_error_handling():
    """Test plan activity error handling"""
    from src.activities.plan import plan_activity

    mock_context = {"goal": "Test goal"}

    # Mock Temporal activity context
    mock_activity_info = MagicMock()
    mock_activity_info.workflow_id = "test-wf-123"
    mock_activity_info.run_id = "test-run-456"
    mock_activity_info.attempt = 1

    with patch('src.activities.plan.llm_json', side_effect=Exception("LLM Error")) as mock_llm, \
         patch('temporalio.activity.info', return_value=mock_activity_info), \
         patch('src.activities.plan.get_tracer') as mock_tracer:

        mock_span = MagicMock()
        mock_tracer.return_value.start_as_current_span.return_value.__enter__ = mock_span
        mock_tracer.return_value.start_as_current_span.return_value.__exit__ = MagicMock()

        with pytest.raises(Exception, match="LLM Error"):
            await plan_activity(mock_context)


@pytest.mark.asyncio
async def test_plan_activity_empty_goal():
    """Test plan activity with empty goal"""
    from src.activities.plan import plan_activity

    mock_context = {"goal": ""}

    mock_response = [
        {
            "id": "1",
            "title": "Clarify requirements",
            "status": "todo",
            "tool_hints": []
        }
    ]

    # Mock Temporal activity context
    mock_activity_info = MagicMock()
    mock_activity_info.workflow_id = "test-wf-123"
    mock_activity_info.run_id = "test-run-456"
    mock_activity_info.attempt = 1

    with patch('src.activities.plan.llm_json', return_value=mock_response) as mock_llm, \
         patch('temporalio.activity.info', return_value=mock_activity_info), \
         patch('src.activities.plan.get_tracer') as mock_tracer:

        mock_span = MagicMock()
        mock_tracer.return_value.start_as_current_span.return_value.__enter__ = mock_span
        mock_tracer.return_value.start_as_current_span.return_value.__exit__ = MagicMock()

        result = await plan_activity(mock_context)

        assert isinstance(result, list)
        assert len(result) >= 0  # May return empty or default plan


def test_plan_item_model():
    """Test PlanItem model creation and validation"""
    plan_item = PlanItem(
        id="test-1",
        title="Test task",
        status="todo",
        tool_hints=["tool1", "tool2"]
    )

    assert plan_item.id == "test-1"
    assert plan_item.title == "Test task"
    assert plan_item.status == "todo"
    assert plan_item.tool_hints == ["tool1", "tool2"]


def test_plan_item_id_coercion():
    """Test PlanItem ID coercion from int to string"""
    plan_item = PlanItem(id=123, title="Test", status="todo")
    assert plan_item.id == "123"
    assert isinstance(plan_item.id, str)
