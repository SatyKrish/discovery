from __future__ import annotations
import time
import uuid
from typing import Dict, List, Any, Optional
from src.models import HierarchicalAgent, SelfReflectionEntry
from src.tool_chain_orchestrator import reflection_engine


class AgentCoordinator:
    """Coordinates multiple specialized agents for complex tasks"""

    def __init__(self):
        self.agents: Dict[str, HierarchicalAgent] = {}
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize the core agent team"""
        # Planning Agent - Strategic goal decomposition
        self.agents["planning"] = HierarchicalAgent(
            agent_id="planning_agent",
            name="Strategic Planner",
            role="planning",
            capabilities=["goal_analysis", "task_decomposition", "priority_assessment", "dependency_mapping"],
            specialization="Breaking down complex objectives into actionable plans",
            performance_score=0.8,
            experience_level=3,
            active=True
        )

        # Execution Agent - Tool orchestration and task completion
        self.agents["execution"] = HierarchicalAgent(
            agent_id="execution_agent",
            name="Task Executor",
            role="execution",
            capabilities=["tool_orchestration", "workflow_execution", "error_handling", "progress_tracking"],
            specialization="Executing plans using available tools and resources",
            performance_score=0.7,
            experience_level=2,
            active=True
        )

        # Reflection Agent - Performance analysis and improvement
        self.agents["reflection"] = HierarchicalAgent(
            agent_id="reflection_agent",
            name="Performance Analyst",
            role="reflection",
            capabilities=["performance_analysis", "pattern_recognition", "strategy_optimization", "learning"],
            specialization="Analyzing performance and suggesting improvements",
            performance_score=0.9,
            experience_level=4,
            active=True
        )

        # Communication Agent - Natural conversation handling
        self.agents["communication"] = HierarchicalAgent(
            agent_id="communication_agent",
            name="Conversation Specialist",
            role="communication",
            capabilities=["natural_language", "user_engagement", "clarification", "progress_reporting"],
            specialization="Managing natural conversations and user interactions",
            performance_score=0.85,
            experience_level=3,
            active=True
        )

    def assign_task(self, task_description: str, task_type: str = "general") -> Dict[str, Any]:
        """Assign a task to the most suitable agent"""
        task_id = f"task_{int(time.time())}_{uuid.uuid4().hex[:8]}"

        # Determine primary agent based on task type
        primary_agent = self._select_primary_agent(task_description, task_type)

        task_info = {
            "task_id": task_id,
            "description": task_description,
            "type": task_type,
            "primary_agent": primary_agent,
            "supporting_agents": self._select_supporting_agents(task_description, primary_agent),
            "status": "assigned",
            "created_at": time.time(),
            "progress": 0.0,
            "subtasks": []
        }

        self.active_tasks[task_id] = task_info
        return task_info

    def _select_primary_agent(self, task_description: str, task_type: str) -> str:
        """Select the primary agent for a task"""
        task_lower = task_description.lower()

        # Planning-heavy tasks
        if any(keyword in task_lower for keyword in ["plan", "strategy", "organize", "structure"]):
            return "planning"

        # Execution-heavy tasks
        if any(keyword in task_lower for keyword in ["execute", "run", "perform", "implement"]):
            return "execution"

        # Analysis/reflection tasks
        if any(keyword in task_lower for keyword in ["analyze", "review", "evaluate", "improve"]):
            return "reflection"

        # Communication tasks
        if any(keyword in task_lower for keyword in ["explain", "discuss", "chat", "help"]):
            return "communication"

        # Default to planning for complex tasks
        if len(task_description.split()) > 20:
            return "planning"

        return "execution"  # Default fallback

    def _select_supporting_agents(self, task_description: str, primary_agent: str) -> List[str]:
        """Select supporting agents for complex tasks"""
        supporting = []

        # Most tasks benefit from communication support
        if primary_agent != "communication":
            supporting.append("communication")

        # Complex tasks may need reflection
        if len(task_description.split()) > 30:
            if primary_agent != "reflection":
                supporting.append("reflection")

        # Multi-step tasks may need execution support
        if any(keyword in task_description.lower() for keyword in ["multiple", "several", "various", "complex"]):
            if primary_agent != "execution":
                supporting.append("execution")

        return supporting

    def update_task_progress(self, task_id: str, progress: float, status: str = None) -> bool:
        """Update task progress and status"""
        if task_id not in self.active_tasks:
            return False

        task = self.active_tasks[task_id]
        task["progress"] = progress

        if status:
            task["status"] = status

        # Update agent performance based on task completion
        if progress >= 1.0:
            primary_agent = task["primary_agent"]
            if primary_agent in self.agents:
                agent = self.agents[primary_agent]
                # Reward successful completion
                agent.performance_score = min(1.0, agent.performance_score + 0.05)
                agent.experience_level += 1

        return True

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent"""
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "role": agent.role,
            "performance_score": agent.performance_score,
            "experience_level": agent.experience_level,
            "active": agent.active,
            "capabilities": agent.capabilities,
            "specialization": agent.specialization
        }

    def get_team_status(self) -> Dict[str, Any]:
        """Get overall team status"""
        active_agents = [aid for aid, agent in self.agents.items() if agent.active]
        avg_performance = sum(self.agents[aid].performance_score for aid in active_agents) / len(active_agents) if active_agents else 0.0

        return {
            "total_agents": len(self.agents),
            "active_agents": len(active_agents),
            "average_performance": avg_performance,
            "active_tasks": len(self.active_tasks),
            "agents": {aid: self.get_agent_status(aid) for aid in self.agents.keys()}
        }

    def reflect_on_performance(self, task_id: str, success: bool, feedback: str = "") -> Dict[str, Any]:
        """Have agents reflect on task performance"""
        if task_id not in self.active_tasks:
            return {"error": "Task not found"}

        task = self.active_tasks[task_id]
        primary_agent = task["primary_agent"]

        # Create reflection entry
        reflection_data = {
            "type": "task_completion",
            "success": success,
            "duration": time.time() - task["created_at"],
            "tools_used": [],  # Would be populated from actual execution
            "feedback": feedback
        }

        reflection = reflection_engine.analyze_interaction(reflection_data)

        # Update agent performance based on reflection
        if primary_agent in self.agents:
            agent = self.agents[primary_agent]
            if success:
                agent.performance_score = min(1.0, agent.performance_score + 0.02)
            else:
                agent.performance_score = max(0.0, agent.performance_score - 0.05)

        return reflection

    def optimize_team(self) -> Dict[str, Any]:
        """Optimize team composition and performance"""
        optimizations = []

        # Identify underperforming agents
        underperformers = [
            aid for aid, agent in self.agents.items()
            if agent.performance_score < 0.6 and agent.active
        ]

        if underperformers:
            optimizations.append(f"Consider retraining agents: {', '.join(underperformers)}")

        # Suggest specialization improvements
        for aid, agent in self.agents.items():
            if agent.experience_level > 5 and len(agent.capabilities) < 3:
                optimizations.append(f"Expand capabilities for experienced agent: {aid}")

        # Balance workload
        active_tasks_per_agent = {}
        for task in self.active_tasks.values():
            primary = task["primary_agent"]
            active_tasks_per_agent[primary] = active_tasks_per_agent.get(primary, 0) + 1

        overloaded = [aid for aid, count in active_tasks_per_agent.items() if count > 5]
        if overloaded:
            optimizations.append(f"Redistribute workload from overloaded agents: {', '.join(overloaded)}")

        return {
            "optimizations": optimizations,
            "team_metrics": self.get_team_status(),
            "performance_insights": reflection_engine.get_performance_insights()
        }


class AdaptiveStrategyManager:
    """Manages adaptive strategies based on performance and user patterns"""

    def __init__(self):
        self.strategies: Dict[str, Dict[str, Any]] = {}
        self.user_patterns: Dict[str, Any] = {}
        self.performance_history: List[Dict[str, Any]] = []

    def adapt_strategy(self, user_id: str, interaction_context: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt strategy based on user and interaction context"""
        # Analyze user patterns
        user_pattern = self._analyze_user_pattern(user_id, interaction_context)

        # Determine optimal strategy
        strategy = self._select_optimal_strategy(user_pattern, interaction_context)

        # Apply adaptations
        adaptations = self._apply_adaptations(strategy, interaction_context)

        return {
            "strategy": strategy,
            "adaptations": adaptations,
            "user_pattern": user_pattern,
            "confidence": self._calculate_confidence(strategy, user_pattern)
        }

    def _analyze_user_pattern(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user interaction patterns"""
        if user_id not in self.user_patterns:
            self.user_patterns[user_id] = {
                "interaction_count": 0,
                "preferred_complexity": "medium",
                "response_time_preference": "balanced",
                "tool_usage_patterns": {},
                "communication_style": "standard"
            }

        pattern = self.user_patterns[user_id]
        pattern["interaction_count"] += 1

        # Update patterns based on context
        task_complexity = context.get("task_complexity", "medium")
        response_time = context.get("response_time", 30)

        # Adapt complexity preference
        if task_complexity == "simple" and pattern["preferred_complexity"] == "complex":
            pattern["preferred_complexity"] = "medium"
        elif task_complexity == "complex" and pattern["preferred_complexity"] == "simple":
            pattern["preferred_complexity"] = "medium"

        # Adapt response time preference
        if response_time < 10:
            pattern["response_time_preference"] = "fast"
        elif response_time > 60:
            pattern["response_time_preference"] = "thorough"

        return pattern

    def _select_optimal_strategy(self, user_pattern: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Select the optimal strategy for the current context"""
        task_type = context.get("task_type", "general")
        urgency = context.get("urgency", "normal")

        # High urgency tasks
        if urgency == "high":
            return "fast_execution"

        # Complex tasks for experienced users
        if (task_type == "complex" and
            user_pattern.get("preferred_complexity") == "complex"):
            return "detailed_planning"

        # Simple tasks for efficiency-focused users
        if (task_type == "simple" and
            user_pattern.get("response_time_preference") == "fast"):
            return "streamlined_execution"

        # Default balanced approach
        return "balanced_approach"

    def _apply_adaptations(self, strategy: str, context: Dict[str, Any]) -> List[str]:
        """Apply strategy-specific adaptations"""
        adaptations = []

        if strategy == "fast_execution":
            adaptations.extend([
                "Prioritize speed over detailed explanations",
                "Use pre-optimized tool chains",
                "Minimize user interaction points"
            ])

        elif strategy == "detailed_planning":
            adaptations.extend([
                "Provide comprehensive planning breakdown",
                "Include detailed progress updates",
                "Offer multiple approach options"
            ])

        elif strategy == "streamlined_execution":
            adaptations.extend([
                "Use simplified communication",
                "Minimize non-essential steps",
                "Focus on core functionality"
            ])

        elif strategy == "balanced_approach":
            adaptations.extend([
                "Maintain clear communication",
                "Balance speed and thoroughness",
                "Provide essential context"
            ])

        return adaptations

    def _calculate_confidence(self, strategy: str, user_pattern: Dict[str, Any]) -> float:
        """Calculate confidence in the selected strategy"""
        base_confidence = 0.7  # Default confidence

        # Increase confidence based on interaction history
        interaction_count = user_pattern.get("interaction_count", 0)
        if interaction_count > 10:
            base_confidence += 0.1
        elif interaction_count > 50:
            base_confidence += 0.2

        # Adjust based on strategy familiarity
        if strategy in ["balanced_approach"]:
            base_confidence += 0.1  # Well-tested strategies

        return min(1.0, base_confidence)

    def learn_from_outcome(self, strategy: str, success: bool, feedback: str = "") -> None:
        """Learn from strategy outcomes to improve future selections"""
        outcome = {
            "strategy": strategy,
            "success": success,
            "feedback": feedback,
            "timestamp": time.time()
        }

        self.performance_history.append(outcome)

        # Update strategy performance metrics
        if strategy not in self.strategies:
            self.strategies[strategy] = {
                "total_uses": 0,
                "successes": 0,
                "average_performance": 0.0,
                "feedback_themes": []
            }

        strat_data = self.strategies[strategy]
        strat_data["total_uses"] += 1

        if success:
            strat_data["successes"] += 1

        # Update average performance
        success_rate = strat_data["successes"] / strat_data["total_uses"]
        strat_data["average_performance"] = success_rate

        # Extract feedback themes
        if feedback:
            themes = self._extract_feedback_themes(feedback)
            strat_data["feedback_themes"].extend(themes)

    def _extract_feedback_themes(self, feedback: str) -> List[str]:
        """Extract key themes from feedback"""
        themes = []
        feedback_lower = feedback.lower()

        if any(word in feedback_lower for word in ["fast", "quick", "speed"]):
            themes.append("speed")
        if any(word in feedback_lower for word in ["detailed", "thorough", "comprehensive"]):
            themes.append("detail")
        if any(word in feedback_lower for word in ["simple", "clear", "easy"]):
            themes.append("simplicity")
        if any(word in feedback_lower for word in ["helpful", "useful", "effective"]):
            themes.append("effectiveness")

        return themes

    def get_strategy_insights(self) -> Dict[str, Any]:
        """Get insights about strategy performance"""
        return {
            "strategy_performance": self.strategies,
            "user_patterns": self.user_patterns,
            "recent_outcomes": self.performance_history[-10:],
            "recommendations": self._generate_recommendations()
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate strategy improvement recommendations"""
        recommendations = []

        # Find underperforming strategies
        underperformers = [
            strategy for strategy, data in self.strategies.items()
            if data["total_uses"] > 5 and data["average_performance"] < 0.6
        ]

        if underperformers:
            recommendations.append(f"Review underperforming strategies: {', '.join(underperformers)}")

        # Identify successful patterns
        top_performers = sorted(
            self.strategies.items(),
            key=lambda x: x[1]["average_performance"],
            reverse=True
        )[:3]

        if top_performers:
            top_names = [name for name, _ in top_performers]
            recommendations.append(f"Emphasize successful strategies: {', '.join(top_names)}")

        return recommendations


# Global instances
agent_coordinator = AgentCoordinator()
strategy_manager = AdaptiveStrategyManager()
