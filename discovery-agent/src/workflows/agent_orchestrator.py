from __future__ import annotations
from dataclasses import dataclass, field
from datetime import timedelta
from typing import List, Dict, Any
import json
from temporalio import workflow
from temporalio.common import RetryPolicy
from src.models import Message, PlanItem, FileRef, ToolCall, ToolResult, AssistantAction, StatusView, ConversationMemory, PlanningContext, SubGoal, ResponseEnvelope, StructuredToolResult
from src.response_formatter import response_formatter


def format_tool_result_for_display(tool_name: str, result: Any) -> str:
    """Format tool results into human-readable text"""
    try:
        # Handle MCP tool results (already dict format)
        if isinstance(result, dict):
            # Check if this is our MCP result format (success/content structure)
            if "success" in result and "content" in result:
                return format_mcp_content_result(tool_name, result)
            # Check if this is an MCP tool result with content array at top level
            elif "content" in result and isinstance(result["content"], list):
                return format_mcp_content_result(tool_name, result)
            else:
                return format_json_result(tool_name, result)

        # Handle string results (try to parse as JSON)
        elif isinstance(result, str):
            try:
                parsed = json.loads(result)
                return format_json_result(tool_name, parsed)
            except json.JSONDecodeError:
                return result

        # Handle other types
        else:
            return str(result)
    except Exception as e:
        # Fallback to string representation with error info
        return f"Tool result formatting error: {str(e)}\nRaw result: {str(result)}"


def format_json_result(tool_name: str, data: Dict[str, Any]) -> str:
    """Format specific tool JSON results into readable text"""
    if tool_name == "web-search.web_search":
        return format_web_search_result(data)
    elif tool_name == "calculator.calculate":
        return format_calculator_result(data)
    elif tool_name == "echo.echo":
        return format_echo_result(data)
    # Add more tool-specific formatters as needed
    else:
        return json.dumps(data, indent=2)


def format_web_search_result(data: Dict[str, Any]) -> str:
    """Format web search results into readable text"""
    query = data.get("query", "Unknown query")
    total_results = data.get("total_results", 0)
    results = data.get("results", [])

    if not results:
        return f"No results found for '{query}'."

    response = f"Search results for '{query}':\n\n"
    for i, result in enumerate(results[:5], 1):  # Limit to top 5
        title = result.get("title", "No title")
        url = result.get("url", "")
        response += f"{i}. {title}\n"
        if url:
            response += f"   {url}\n"
        response += "\n"

    if total_results > 5:
        response += f"... and {total_results - 5} more results."

    return response


def format_calculator_result(data: Dict[str, Any]) -> str:
    """Format calculator results"""
    expression = data.get("expression", "")
    result = data.get("result", "")
    return f"Calculation result: {expression} = {result}"


def format_echo_result(data: Dict[str, Any]) -> str:
    """Format echo results"""
    # Handle our MCP result format
    if isinstance(data, dict) and "content" in data:
        content_list = data.get("content", [])
        if content_list and isinstance(content_list, list):
            for item in content_list:
                if isinstance(item, dict) and item.get("type") == "text":
                    return f"Echo: {item.get('text', '')}"
        return f"Echo result: {str(data)}"
    else:
        # Handle direct result format
        text = data.get("text", "")
        return f"Echo: {text}"


def format_mcp_content_result(tool_name: str, data: Dict[str, Any]) -> str:
    """Format MCP tool results with content array"""
    # Handle the case where data is the result dict itself
    if isinstance(data, dict) and "content" in data:
        content_list = data.get("content", [])
    elif isinstance(data, dict) and "success" in data:
        # This is our MCP result format
        if data.get("success"):
            content_data = data.get("content", [])
            if isinstance(content_data, list):
                content_list = content_data
            else:
                return f"Tool '{tool_name}' result: {str(content_data)}"
        else:
            return f"Tool '{tool_name}' failed: {data.get('error', 'Unknown error')}"
    else:
        # Fallback for other formats
        return f"Tool '{tool_name}' result: {str(data)}"

    if not content_list:
        return f"Tool '{tool_name}' completed but returned no content."

    # Extract text content from MCP result
    text_parts = []
    for item in content_list:
        if isinstance(item, dict) and item.get("type") == "text":
            text_parts.append(item.get("text", ""))
        elif isinstance(item, str):
            text_parts.append(item)

    if text_parts:
        combined_text = " ".join(text_parts)
        return f"Tool '{tool_name}' result: {combined_text}"
    else:
        # Fallback for non-text content
        return f"Tool '{tool_name}' completed with {len(content_list)} content items."

@dataclass
class State:
    conversation_id: str = ""
    turns: int = 0
    plan: List[PlanItem] = field(default_factory=list)
    planning_context: PlanningContext | None = None
    artifacts: List[FileRef] = field(default_factory=list)
    pending_tool_call: ToolCall | None = None
    gate_ok: bool = True
    done: bool = False
    last_processed_turn: int = 0
    last_response_id: str = ""  # OpenAI Responses API state management
    memory: ConversationMemory = field(default_factory=ConversationMemory)

    def view_for_llm(self) -> dict:
        # Provide recent messages for context (limit to last 20 for efficiency)
        recent_messages = self.memory.short_term[-20:] if len(self.memory.short_term) > 20 else self.memory.short_term

        return {
            "plan": [p.model_dump() for p in self.plan],
            "turns": self.turns,
            "pending_tool_call": self.pending_tool_call.model_dump() if self.pending_tool_call else None,
            "artifacts": [a.model_dump() for a in self.artifacts],
            "messages": [m.model_dump() for m in recent_messages],
            "memory_summary": self.memory.summary,
            "user_patterns": self.memory.long_term_patterns,
            "gate_ok": self.gate_ok,
            "last_response_id": self.last_response_id,  # OpenAI Responses API state
        }

    def should_summarize(self) -> bool:
        return self.turns > 0 and self.turns % 5 == 0

    def should_continue_as_new(self) -> bool:
        return self.turns > 0 and self.turns % 25 == 0

@workflow.defn
class AgentOrchestratorWorkflow:
    def __init__(self):
        self.state = State()

    @workflow.signal
    async def user_message(self, msg: Message):
        # Store the user message in memory
        self.state.memory.short_term.append(msg)

        # Maintain memory size limit (keep last 50 messages)
        if len(self.state.memory.short_term) > 50:
            # Move older messages to summary if needed
            self.state.memory.short_term = self.state.memory.short_term[-50:]

        await workflow.execute_activity(
            "append_transcript",
            args=[
                self.state.conversation_id or workflow.info().workflow_id,
                msg.role,
                msg.content,
            ],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        self.state.gate_ok = await workflow.execute_activity(
            "guardrail_check",
            args=[{"goal": self.state.plan[0].title if self.state.plan else "", "message": msg.content}],
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )
        # Always increment turns - guardrail is advisory, not blocking
        self.state.turns += 1

    @workflow.signal
    async def approve_tool(self, tool_call_id: str, approved: bool, edited_args: dict | None = None):
        if self.state.pending_tool_call and self.state.pending_tool_call.id == tool_call_id and approved:
            if edited_args:
                self.state.pending_tool_call.args = edited_args
        self.state.pending_tool_call = None

    @workflow.signal
    async def end_conversation(self):
        """Signal to end the conversation and terminate the workflow"""
        self.state.done = True
        # Force exit from any wait conditions by ensuring turns are processed
        self.state.last_processed_turn = max(self.state.last_processed_turn, self.state.turns)

    @workflow.query
    def get_status(self) -> StatusView:
        # Create response envelope based on current state
        response = self._create_current_response()

        return StatusView(
            conversation_id=self.state.conversation_id,
            plan=self.state.plan,
            pending_tool_call=self.state.pending_tool_call,
            turns=self.state.turns,
            artifacts=self.state.artifacts,
            state="done" if self.state.done else "running",
            response=response,
            memory_summary=self.state.memory.summary,
        )

    def _create_current_response(self) -> ResponseEnvelope | None:
        """Create the current response envelope based on workflow state"""
        # Find the most recent assistant message
        for msg in reversed(self.state.memory.short_term):
            if msg.role == "assistant":
                # Check if this is a tool result message
                if "Tool '" in msg.content and "' completed successfully" in msg.content:
                    response = response_formatter.create_tool_response(
                        StructuredToolResult(
                            tool_name=self._extract_tool_name_from_message(msg.content),
                            success=True,
                            data=self._extract_tool_data_from_message(msg.content),
                            formatted_display=msg.content
                        )
                    )
                    response.timestamp = workflow.now().timestamp()
                    return response
                else:
                    # Regular assistant message
                    response = response_formatter.create_assistant_response(msg.content)
                    response.timestamp = workflow.now().timestamp()
                    return response

        # If no assistant message found, check for pending tool call
        if self.state.pending_tool_call:
            response = response_formatter.create_response_envelope(
                response_type="status",
                status="pending",
                content="Waiting for tool approval",
                metadata={"pending_tool": self.state.pending_tool_call.name}
            )
            response.timestamp = workflow.now().timestamp()
            return response

        # If conversation is done
        if self.state.done:
            response = response_formatter.create_completion_response()
            response.timestamp = workflow.now().timestamp()
            return response

        # No active response
        return None

    def _extract_tool_name_from_message(self, content: str) -> str:
        """Extract tool name from tool result message"""
        try:
            # Message format: "Tool 'tool.name' completed successfully.\n\nformatted_result"
            if "Tool '" in content:
                start = content.find("Tool '") + 6
                end = content.find("'", start)
                if end > start:
                    return content[start:end]
        except:
            pass
        return "unknown_tool"

    def _extract_tool_data_from_message(self, content: str) -> Any:
        """Extract tool data from tool result message"""
        try:
            # Try to extract structured data from the message
            lines = content.split('\n')
            for line in lines:
                if line.startswith("Calculation result:"):
                    # Calculator result
                    return {"result": line.split(": ", 1)[1]}
                elif line.startswith("Echo:"):
                    # Echo result
                    return {"text": line.split(": ", 1)[1]}
        except:
            pass
        return None

    @workflow.run
    async def run(self, goal: str):
        self.state.conversation_id = workflow.info().workflow_id

        # Discover MCP tools at workflow start
        tool_discovery_result = await workflow.execute_activity(
            "discover_mcp_tools",
            args=[],
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )

        if tool_discovery_result.get("success"):
            workflow.logger.info(f"Discovered {tool_discovery_result['total_tools']} tools from {tool_discovery_result['server_count']} MCP servers")
        else:
            workflow.logger.warning(f"MCP tool discovery failed: {tool_discovery_result.get('error', 'Unknown error')}")

        plan_data = await workflow.execute_activity(
            "plan_activity",
            args=[{"goal": goal}],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        # Convert JSON-serializable dicts back into PlanItem objects
        self.state.plan = [PlanItem(**it) if isinstance(it, dict) else it for it in plan_data]

        while not self.state.done:
            # Wait for new messages to process, but also check if we should exit due to end signal
            # Add timeout to prevent indefinite waiting (Temporal best practice)
            try:
                await workflow.wait_condition(
                    lambda: (self.state.last_processed_turn < self.state.turns) and not self.state.done,
                    timeout=timedelta(minutes=5)  # Timeout after 5 minutes of inactivity
                )
            except TimeoutError:
                # If we timeout due to inactivity, terminate the workflow
                if not self.state.done:
                    self.state.done = True
                    break

            action_dict: dict = await workflow.execute_activity(
                "decision_agents_activity",
                args=[self.state.view_for_llm()],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            action: AssistantAction = AssistantAction(**action_dict)

            # Update last_response_id from OpenAI Responses API
            if "last_response_id" in action_dict:
                self.state.last_response_id = action_dict["last_response_id"]

            if action.type == "assistant_message":
                if action.message:
                    self.state.memory.short_term.append(action.message)
                    # Maintain memory size limit
                    if len(self.state.memory.short_term) > 50:
                        self.state.memory.short_term = self.state.memory.short_term[-50:]
                self.state.last_processed_turn = self.state.turns
            elif action.type == "revise_plan" and action.plan_diff:
                self.state.plan = action.plan_diff
                self.state.last_processed_turn = self.state.turns
            elif action.type == "tool_call" and action.call:
                call = action.call
                if call.requires_approval:
                    self.state.pending_tool_call = call
                    await workflow.wait_condition(lambda: self.state.pending_tool_call is None or self.state.done)

                tool_result: StructuredToolResult = await workflow.execute_activity(
                    "tool_dispatch",
                    args=[call],
                    heartbeat_timeout=timedelta(seconds=30),
                    start_to_close_timeout=timedelta(minutes=10),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )

                # Create response envelope for the tool result
                response_envelope = response_formatter.create_tool_response(tool_result)
                response_envelope.timestamp = workflow.now().timestamp()

                # Store tool result in conversation for context
                if tool_result.success:
                    # Format the result for human-readable display
                    formatted_result = response_formatter.format_tool_result(tool_result)

                    tool_result_message = Message(
                        role="assistant",
                        content=formatted_result,
                        ts=workflow.now().timestamp()
                    )
                    self.state.memory.short_term.append(tool_result_message)
                else:
                    # Handle tool failure
                    error_message = Message(
                        role="assistant",
                        content=f"Tool '{call.name}' failed: {tool_result.error}",
                        ts=workflow.now().timestamp()
                    )
                    self.state.memory.short_term.append(error_message)

                # Generate response based on tool results
                response_action_dict: dict = await workflow.execute_activity(
                    "decision_agents_activity",
                    args=[self.state.view_for_llm()],
                    start_to_close_timeout=timedelta(minutes=2),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )
                response_action: AssistantAction = AssistantAction(**response_action_dict)

                # Process the response action
                if response_action.type == "assistant_message" and response_action.message:
                    self.state.memory.short_term.append(response_action.message)
                    # Maintain memory size limit
                    if len(self.state.memory.short_term) > 50:
                        self.state.memory.short_term = self.state.memory_short_term[-50:]

                    # Update processing state so status query returns output_text
                    self.state.last_processed_turn = self.state.turns
                    workflow.logger.info(f"Tool result processed, updated last_processed_turn to: {self.state.last_processed_turn}")
                else:
                    # If no assistant message was generated, still update the turn
                    self.state.last_processed_turn = self.state.turns
                    workflow.logger.info(f"No assistant message generated, still updated last_processed_turn to: {self.state.last_processed_turn}")
            elif action.type == "spawn_subagent":
                self.state.last_processed_turn = self.state.turns

            if self.state.should_summarize():
                summary_result = await workflow.execute_activity(
                    "summarize_activity",
                    args=[self.state.view_for_llm()],
                    start_to_close_timeout=timedelta(minutes=1),
                    retry_policy=RetryPolicy(maximum_attempts=2),
                )
                # Update memory summary
                self.state.memory.summary = summary_result
                self.state.memory.last_summarized_turn = self.state.turns

            if self.state.should_continue_as_new():
                workflow.continue_as_new(goal)
