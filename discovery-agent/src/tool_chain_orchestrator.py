from __future__ import annotations
import asyncio
import time
import uuid
from typing import Dict, List, Any, Optional
from src.models import ToolChain, ToolChainStep, ToolChainExecution, ToolSpec
from src.mcp.core.client import tool_orchestrator
from src.config import settings


class ToolChainBuilder:
    """Builds tool chains for complex multi-step tasks"""

    def __init__(self):
        self.available_tools = tool_orchestrator.get_all_available_tools()

    def create_chain_from_task(self, task_description: str, available_tools: List[str]) -> ToolChain:
        """Create a tool chain from a task description"""
        chain_id = f"chain_{int(time.time())}_{uuid.uuid4().hex[:8]}"

        # Analyze task and create appropriate steps
        steps = self._analyze_task_and_create_steps(task_description, available_tools)

        # Create input/output schemas
        input_schema = self._infer_input_schema(steps)
        output_schema = self._infer_output_schema(steps)

        chain = ToolChain(
            chain_id=chain_id,
            name=f"Chain for: {task_description[:50]}...",
            description=f"Automated tool chain for: {task_description}",
            steps=steps,
            input_schema=input_schema,
            output_schema=output_schema,
            success_criteria="All steps completed successfully",
            estimated_duration=len(steps) * 30,  # Rough estimate
            created_at=time.time()
        )

        return chain

    def _analyze_task_and_create_steps(self, task: str, available_tools: List[str]) -> List[ToolChainStep]:
        """Analyze task and create appropriate tool chain steps"""
        steps = []
        task_lower = task.lower()

        # Research tasks
        if any(keyword in task_lower for keyword in ["research", "find", "search", "lookup"]):
            if "web_search" in available_tools:
                steps.append(ToolChainStep(
                    tool_name="web_search",
                    step_id="research_1",
                    description="Search for relevant information",
                    input_mapping={"query": "task_description"},
                    output_mapping={"results": "search_results"},
                    dependencies=[],
                    timeout=60
                ))

        # Analysis tasks
        if any(keyword in task_lower for keyword in ["analyze", "review", "evaluate"]):
            if "web_search" in available_tools and len(steps) == 0:
                steps.append(ToolChainStep(
                    tool_name="web_search",
                    step_id="gather_data",
                    description="Gather data for analysis",
                    input_mapping={"query": "task_description"},
                    output_mapping={"results": "analysis_data"},
                    dependencies=[],
                    timeout=60
                ))

        # Calculation tasks
        if any(keyword in task_lower for keyword in ["calculate", "compute", "math"]):
            if "calculate" in available_tools:
                steps.append(ToolChainStep(
                    tool_name="calculate",
                    step_id="computation_1",
                    description="Perform mathematical calculations",
                    input_mapping={"expression": "calculation_expression"},
                    output_mapping={"result": "calculation_result"},
                    dependencies=[],
                    timeout=30
                ))

        # If no specific tools match, create a generic chain
        if not steps:
            if "echo" in available_tools:
                steps.append(ToolChainStep(
                    tool_name="echo",
                    step_id="echo_1",
                    description="Process the request",
                    input_mapping={"text": "task_description"},
                    output_mapping={"echo": "response"},
                    dependencies=[],
                    timeout=30
                ))

        return steps

    def _infer_input_schema(self, steps: List[ToolChainStep]) -> Dict[str, Any]:
        """Infer input schema from chain steps"""
        properties = {}
        required = []

        for step in steps:
            for input_param in step.input_mapping.keys():
                if input_param not in properties:
                    properties[input_param] = {
                        "type": "string",
                        "description": f"Input for {input_param}"
                    }
                    required.append(input_param)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    def _infer_output_schema(self, steps: List[ToolChainStep]) -> Dict[str, Any]:
        """Infer output schema from chain steps"""
        properties = {}

        for step in steps:
            for output_var in step.output_mapping.values():
                properties[output_var] = {
                    "type": "string",
                    "description": f"Output from {step.tool_name}"
                }

        return {
            "type": "object",
            "properties": properties
        }


class ToolChainExecutor:
    """Executes tool chains with proper error handling and flow control"""

    def __init__(self):
        self.active_executions: Dict[str, ToolChainExecution] = {}

    async def execute_chain(self, chain: ToolChain, inputs: Dict[str, Any]) -> ToolChainExecution:
        """Execute a tool chain with given inputs"""
        execution_id = f"exec_{int(time.time())}_{uuid.uuid4().hex[:8]}"

        execution = ToolChainExecution(
            execution_id=execution_id,
            chain_id=chain.chain_id,
            status="running",
            variables=inputs.copy(),
            started_at=time.time()
        )

        self.active_executions[execution_id] = execution

        try:
            # Execute steps in dependency order
            completed_steps = set()
            step_results = {}

            while len(completed_steps) < len(chain.steps):
                # Find next executable step
                next_step = self._find_next_executable_step(chain.steps, completed_steps)

                if not next_step:
                    # Check if we're stuck due to failed dependencies
                    if any(step.step_id not in completed_steps and
                           all(dep in completed_steps for dep in step.dependencies)
                           for step in chain.steps):
                        raise Exception("Tool chain execution stuck - circular dependencies or failed steps")
                    break

                # Execute the step
                execution.current_step = next_step.step_id
                step_result = await self._execute_step(next_step, execution.variables)

                step_results[next_step.step_id] = step_result
                completed_steps.add(next_step.step_id)

                # Update variables with step outputs
                if step_result.get("ok", False):
                    for output_var, output_key in next_step.output_mapping.items():
                        if output_key in step_result.get("output", {}):
                            execution.variables[output_var] = step_result["output"][output_key]

            # Mark execution as completed
            execution.status = "completed"
            execution.completed_at = time.time()
            execution.step_results = step_results

        except Exception as e:
            execution.status = "failed"
            execution.error_message = str(e)
            execution.completed_at = time.time()

        return execution

    def _find_next_executable_step(self, steps: List[ToolChainStep], completed_steps: set) -> Optional[ToolChainStep]:
        """Find the next step that can be executed"""
        for step in steps:
            if step.step_id in completed_steps:
                continue

            # Check if all dependencies are satisfied
            if all(dep in completed_steps for dep in step.dependencies):
                return step

        return None

    async def _execute_step(self, step: ToolChainStep, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step in the tool chain"""
        try:
            # Prepare inputs for the tool
            tool_inputs = {}
            for input_param, var_name in step.input_mapping.items():
                if var_name in variables:
                    tool_inputs[input_param] = variables[var_name]
                else:
                    # Try to use the variable name directly if it's a literal
                    tool_inputs[input_param] = var_name

            # Execute the tool
            result = await tool_orchestrator.execute_tool(step.tool_name, tool_inputs)

            return {
                "ok": True,
                "output": result,
                "execution_time": time.time()
            }

        except Exception as e:
            return {
                "ok": False,
                "error": str(e),
                "execution_time": time.time()
            }

    def get_execution_status(self, execution_id: str) -> Optional[ToolChainExecution]:
        """Get the status of a tool chain execution"""
        return self.active_executions.get(execution_id)


class SelfReflectionEngine:
    """Analyzes performance and learns from interactions"""

    def __init__(self):
        self.reflection_history: List[Dict[str, Any]] = []
        self.performance_patterns: Dict[str, Any] = {}

    def analyze_interaction(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a completed interaction and extract insights"""
        interaction_type = interaction_data.get("type", "unknown")
        success = interaction_data.get("success", False)
        duration = interaction_data.get("duration", 0)
        tools_used = interaction_data.get("tools_used", [])

        # Calculate success rating
        success_rating = 1.0 if success else 0.0

        # Adjust for duration (prefer faster successful interactions)
        if success and duration > 0:
            if duration < 10:  # Very fast
                success_rating = min(1.0, success_rating + 0.1)
            elif duration > 60:  # Slow
                success_rating = max(0.0, success_rating - 0.1)

        # Analyze tool usage patterns
        tool_insights = self._analyze_tool_usage(tools_used, success)

        reflection = {
            "timestamp": time.time(),
            "interaction_type": interaction_type,
            "success_rating": success_rating,
            "performance_metrics": {
                "duration": duration,
                "tools_used": len(tools_used),
                "success": success
            },
            "tool_insights": tool_insights,
            "lessons_learned": self._extract_lessons(interaction_data),
            "strategy_adjustments": self._suggest_improvements(interaction_data)
        }

        self.reflection_history.append(reflection)
        self._update_patterns(reflection)

        return reflection

    def _analyze_tool_usage(self, tools_used: List[str], success: bool) -> Dict[str, Any]:
        """Analyze tool usage patterns"""
        insights = {
            "tool_combinations": {},
            "success_rates": {},
            "recommendations": []
        }

        if len(tools_used) > 1:
            # Analyze tool combinations
            combo_key = "+".join(sorted(tools_used))
            if combo_key not in insights["tool_combinations"]:
                insights["tool_combinations"][combo_key] = {"successes": 0, "total": 0}
            insights["tool_combinations"][combo_key]["total"] += 1
            if success:
                insights["tool_combinations"][combo_key]["successes"] += 1

        # Individual tool success rates
        for tool in tools_used:
            if tool not in insights["success_rates"]:
                insights["success_rates"][tool] = {"successes": 0, "total": 0}
            insights["success_rates"][tool]["total"] += 1
            if success:
                insights["success_rates"][tool]["successes"] += 1

        return insights

    def _extract_lessons(self, interaction_data: Dict[str, Any]) -> List[str]:
        """Extract lessons from the interaction"""
        lessons = []

        success = interaction_data.get("success", False)
        duration = interaction_data.get("duration", 0)
        tools_used = interaction_data.get("tools_used", [])

        if success:
            if duration < 10:
                lessons.append("Fast execution with good results - maintain this efficiency")
            if len(tools_used) > 2:
                lessons.append("Complex tool combinations can be effective for sophisticated tasks")
        else:
            if duration > 120:
                lessons.append("Long execution times may indicate need for optimization")
            if len(tools_used) == 0:
                lessons.append("Consider using tools for tasks that might benefit from external capabilities")

        return lessons

    def _suggest_improvements(self, interaction_data: Dict[str, Any]) -> List[str]:
        """Suggest strategy improvements"""
        suggestions = []

        success = interaction_data.get("success", False)
        tools_used = interaction_data.get("tools_used", [])

        if not success:
            suggestions.append("Consider alternative tool combinations for failed tasks")
            suggestions.append("Review error patterns to identify common failure modes")

        if len(tools_used) > 3:
            suggestions.append("Complex tool chains may benefit from parallel execution")

        return suggestions

    def _update_patterns(self, reflection: Dict[str, Any]):
        """Update performance patterns based on new reflection"""
        interaction_type = reflection["interaction_type"]

        if interaction_type not in self.performance_patterns:
            self.performance_patterns[interaction_type] = {
                "total_interactions": 0,
                "success_rate": 0.0,
                "average_duration": 0.0,
                "common_tools": {},
                "improvement_trends": []
            }

        pattern = self.performance_patterns[interaction_type]
        pattern["total_interactions"] += 1

        # Update success rate
        current_success_rate = pattern["success_rate"]
        new_success_rate = reflection["success_rating"]
        pattern["success_rate"] = (current_success_rate * (pattern["total_interactions"] - 1) + new_success_rate) / pattern["total_interactions"]

        # Update average duration
        current_avg_duration = pattern["average_duration"]
        new_duration = reflection["performance_metrics"]["duration"]
        pattern["average_duration"] = (current_avg_duration * (pattern["total_interactions"] - 1) + new_duration) / pattern["total_interactions"]

    def get_performance_insights(self) -> Dict[str, Any]:
        """Get overall performance insights"""
        return {
            "patterns": self.performance_patterns,
            "recent_reflections": self.reflection_history[-10:],  # Last 10 reflections
            "overall_success_rate": self._calculate_overall_success_rate(),
            "top_performing_tools": self._identify_top_tools(),
            "improvement_suggestions": self._aggregate_suggestions()
        }

    def _calculate_overall_success_rate(self) -> float:
        """Calculate overall success rate across all interactions"""
        if not self.reflection_history:
            return 0.0

        total_success = sum(r["success_rating"] for r in self.reflection_history)
        return total_success / len(self.reflection_history)

    def _identify_top_tools(self) -> List[str]:
        """Identify highest performing tools"""
        tool_performance = {}

        for reflection in self.reflection_history:
            for tool, stats in reflection.get("tool_insights", {}).get("success_rates", {}).items():
                if tool not in tool_performance:
                    tool_performance[tool] = {"successes": 0, "total": 0}

                tool_performance[tool]["successes"] += stats["successes"]
                tool_performance[tool]["total"] += stats["total"]

        # Calculate success rates and sort
        tool_rates = []
        for tool, stats in tool_performance.items():
            if stats["total"] > 0:
                rate = stats["successes"] / stats["total"]
                tool_rates.append((tool, rate))

        tool_rates.sort(key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in tool_rates[:5]]  # Top 5

    def _aggregate_suggestions(self) -> List[str]:
        """Aggregate improvement suggestions from recent reflections"""
        suggestions = []
        recent_reflections = self.reflection_history[-20:]  # Last 20 reflections

        for reflection in recent_reflections:
            suggestions.extend(reflection.get("strategy_adjustments", []))

        # Remove duplicates and return top suggestions
        unique_suggestions = list(set(suggestions))
        return unique_suggestions[:10]  # Top 10 unique suggestions


# Global instances
tool_chain_builder = ToolChainBuilder()
tool_chain_executor = ToolChainExecutor()
reflection_engine = SelfReflectionEngine()
