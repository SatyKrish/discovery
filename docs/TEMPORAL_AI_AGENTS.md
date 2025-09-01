# Temporal AI Agent

This demo shows a multi-turn conversation with an AI agent running inside a Temporal workflow. The purpose of the agent is to collect information towards a goal, running tools along the way. The agent supports both native tools and Model Context Protocol (MCP) tools, allowing it to interact with external services.

The agent operates in single-agent mode by default, focusing on one specific goal. It also supports experimental multi-agent/multi-goal mode where users can choose between different agent types and switch between them during conversations.

Goals are organized in the `/goals/` directory by category (finance, HR, travel, ecommerce, etc.) and can leverage both native and MCP tools.

The AI will respond with clarifications and ask for any missing information to that goal. You can configure it to use any LLM supported by [LiteLLM](https://docs.litellm.ai/docs/providers), including:
- OpenAI models (GPT-4, GPT-3.5)
- Anthropic Claude models
- Google Gemini models
- Deepseek models
- Ollama models (local)
- And many more!

It's really helpful to [watch the demo (5 minute YouTube video)](https://www.youtube.com/watch?v=GEXllEH2XiQ) to understand how interaction works.

[![Watch the demo](./assets/agent-youtube-screenshot.jpeg)](https://www.youtube.com/watch?v=GEXllEH2XiQ)

### Multi-Agent Demo Video
See multi-agent execution in action [here](https://www.youtube.com/watch?v=8Dc_0dC14yY).

## Why Temporal?
There are a lot of AI and Agentic AI tools out there, and more on the way. But why Temporal? Temporal gives this system reliability, state management, a code-first approach that we really like, built-in observability and easy error handling.
For more, check out [architecture-decisions](docs/architecture-decisions.md).

## What is "Agentic AI"?
These are the key elements of an agentic framework:
1. Goals that a system can accomplish, made up of tools that can execute individual steps
2. Agent loops - executing an LLM, executing tools, and eliciting input from an external source such as a human: repeat until goal(s) are done
3. Support for tool calls that require input and approval
4. Use of an LLM to check human input for relevance before calling the 'real' LLM
5. Use of an LLM to summarize and compact the conversation history
6. Prompt construction made of system prompts, conversation history, and tool metadata - sent to the LLM to create user questions and confirmations
7. Ideally high durability (done in this system with Temporal Workflow and Activities)

For a deeper dive into this, check out the [architecture guide](docs/architecture.md).

## 🔧 MCP Tool Calling Support

This agent acts as an **MCP (Model Context Protocol) client**, enabling seamless integration with external services and tools. The system supports two types of tools:
- **Native Tools**: Custom tools implemented directly in the codebase (in `/tools/`)
 - **MCP Tools**: External tools accessed via Model Context Protocol (MCP) servers like Stripe, databases, or APIs. Configuration is covered in [the Setup guide](docs/setup.md)
- Set `AGENT_GOAL=goal_food_ordering` with `SHOW_CONFIRM=False` in `.env` for an example of a goal that calls MCP Tools (Stripe).

## Setup and Configuration
See [the Setup guide](docs/setup.md) for detailed instructions. The basic configuration requires just two environment variables:
```bash
LLM_MODEL=openai/gpt-4o  # or any other model supported by LiteLLM
LLM_KEY=your-api-key-here
```

## Customizing Interaction & Tools
See [the guide to adding goals and tools](docs/adding-goals-and-tools.md).

The system supports MCP (Model Context Protocol) for easy integration with external services. MCP server configurations are managed in `shared/mcp_config.py`, and goals are organized by category in the `/goals/` directory.

## Architecture
See [the architecture guide](docs/architecture.md).

## Testing

The project includes comprehensive tests for workflows and activities using Temporal's testing framework:

```bash
# Install dependencies including test dependencies
uv sync

# Run all tests
uv run pytest

# Run with time-skipping for faster execution
uv run pytest --workflow-environment=time-skipping
```

**Test Coverage:**
- ✅ **Workflow Tests**: AgentGoalWorkflow signals, queries, state management
- ✅ **Activity Tests**: ToolActivities, LLM integration (mocked), environment configuration
- ✅ **Integration Tests**: End-to-end workflow and activity execution

- **Quick Start**: [testing.md](docs/testing.md) - Simple commands to run tests
- **Comprehensive Guide**: [tests/README.md](tests/README.md) - Detailed testing documentation, patterns, and best practices

## Development

To contribute to this project, see [contributing.md](docs/contributing.md).

Start the Temporal Server and API server, see [setup](docs/setup.md)

## Productionalization & Adding Features
- In a prod setting, I would need to ensure that payload data is stored separately (e.g. in S3 or a noSQL db - the claim-check pattern), or otherwise 'garbage collected'. Without these techniques, long conversations will fill up the workflow's conversation history, and start to breach Temporal event history payload limits.
- A single worker can easily support many agent workflows (chats) running at the same time. Currently the workflow ID is the same each time, so it will only run one agent at a time. To run multiple agents, you can use a different workflow ID each time (e.g. by using a UUID or timestamp).
- Perhaps the UI should show when the LLM response is being retried (i.e. activity retry attempt because the LLM provided bad output)
- The project now includes comprehensive tests for workflows and activities! [See testing guide](docs/testing.md).

See [the todo](docs/todo.md) for more details on things we want to do (or that you could contribute!).

See [the guide to adding goals and tools](docs/adding-goals-and-tools.md) for more ways you can add features.

## Enablement Guide (internal resource for Temporal employees)
Check out the [slides](https://docs.google.com/presentation/d/1wUFY4v17vrtv8llreKEBDPLRtZte3FixxBUn0uWy5NU/edit#slide=id.g3333e5deaa9_0_0) here and the [enablement guide](https://docs.google.com/document/d/14E0cEOibUAgHPBqConbWXgPUBY0Oxrnt6_AImdiheW4/edit?tab=t.0#heading=h.ajnq2v3xqbu1).





================================================
FILE: __init__.py
================================================
[Empty file]


================================================
FILE: AGENTS.md
================================================
# Temporal AI Agent Contribution Guide

## Repository Layout
- `workflows/` - Temporal workflows including the main AgentGoalWorkflow for multi-turn AI conversations
- `activities/` - Temporal activities for tool execution and LLM interactions  
- `tools/` - Native AI agent tool implementations organized by category (finance, HR, ecommerce, travel, etc.)
- `goals/` - Agent goal definitions organized by category, supporting both native and MCP tools
- `shared/` - Shared configuration including MCP server definitions
- `models/` - Data types and tool definitions used throughout the system
- `prompts/` - Agent prompt generators and templates
- `api/` - FastAPI server that exposes REST endpoints to interact with workflows
- `frontend/` - React-based web UI for chatting with the AI agent
- `tests/` - Comprehensive test suite for workflows and activities using Temporal's testing framework
- `enterprise/` - .NET worker implementation for enterprise activities (train booking)
- `scripts/` - Utility scripts for running workers and testing tools

## Running the Application

### Quick Start with Docker
```bash
# Start all services with development hot-reload
docker compose up -d

# Quick rebuild without infrastructure
docker compose up -d --no-deps --build api worker frontend
```

Default URLs:
- Temporal UI: http://localhost:8080
- API: http://localhost:8000  
- Frontend: http://localhost:5173

### Local Development Setup

1. **Prerequisites:**
   ```bash
   # Install uv and Temporal server (MacOS)
   brew install uv
   brew install temporal

   temporal server start-dev
   ```

2. **Backend (Python):**
   ```bash
   # Quick setup using Makefile
   make setup              # Creates venv and installs dependencies
   make run-worker         # Starts the Temporal worker
   make run-api            # Starts the API server
   
   # Or manually:
   uv sync
   uv run scripts/run_worker.py    # In one terminal
   uv run uvicorn api.main:app --reload   # In another terminal
   ```

3. **Frontend (React):**
   ```bash
   make run-frontend       # Using Makefile
   
   # Or manually:
   cd frontend
   npm install
   npx vite
   ```

4. **Enterprise .NET Worker (optional):**
   ```bash
   make run-enterprise     # Using Makefile
   
   # Or manually:
   cd enterprise
   dotnet build
   dotnet run
   ```

### Environment Configuration
Copy `.env.example` to `.env` and configure:
```bash
# Required: LLM Configuration
LLM_MODEL=openai/gpt-4o
LLM_KEY=your-api-key-here
# LLM_MODEL=anthropic/claude-3-5-sonnet-20240620
# LLM_KEY=${ANTHROPIC_API_KEY}
# LLM_MODEL=gemini/gemini-2.5-flash-preview-04-17
# LLM_KEY=${GOOGLE_API_KEY}

# Optional: Agent Goals and Categories  
AGENT_GOAL=goal_choose_agent_type
GOAL_CATEGORIES=hr,travel-flights,travel-trains,fin,ecommerce,mcp-integrations,food

# Optional: Tool-specific APIs
STRIPE_API_KEY=sk_test_...       # For invoice creation
# `goal_event_flight_invoice` works without this key – it falls back to a mock invoice if unset
FOOTBALL_DATA_API_KEY=...        # For real football fixtures
```

## Testing

The project includes comprehensive tests using Temporal's testing framework:

```bash
# Install test dependencies
uv sync

# Run all tests
uv run pytest

# Run with time-skipping for faster execution  
uv run pytest --workflow-environment=time-skipping

# Run specific test categories
uv run pytest tests/test_tool_activities.py -v     # Activity tests
uv run pytest tests/test_agent_goal_workflow.py -v # Workflow tests

# Run with coverage
uv run pytest --cov=workflows --cov=activities
```

**Test Coverage:**
- ✅ **Workflow Tests**: AgentGoalWorkflow signals, queries, state management
- ✅ **Activity Tests**: ToolActivities, LLM integration (mocked), environment configuration  
- ✅ **Integration Tests**: End-to-end workflow and activity execution

**Documentation:**
- **Quick Start**: [testing.md](docs/testing.md) - Simple commands to run tests
- **Comprehensive Guide**: [tests/README.md](tests/README.md) - Detailed testing patterns and best practices

## Linting and Code Quality

```bash
# Using poe tasks
uv run poe format    # Format code with black and isort
uv run poe lint      # Check code style and types
uv run poe test      # Run test suite

# Manual commands
uv run black .
uv run isort .
uv run mypy --check-untyped-defs --namespace-packages .
```

## Agent Customization

### Adding New Goals and Tools

#### For Native Tools:
1. Create tool implementation in `tools/` directory
2. Add tool function mapping in `tools/__init__.py`  
3. Register tool definition in `tools/tool_registry.py`
4. Add tool names to static tools list in `workflows/workflow_helpers.py`
5. Create or update goal definition in appropriate file in `goals/` directory

#### For MCP Tools:
1. Configure MCP server definition in `shared/mcp_config.py` (for reusable servers)
2. Create or update goal definition in appropriate file in `goals/` directory with `mcp_server_definition`
3. Set required environment variables (API keys, etc.)

#### For Goals:
1. Create goal file in `goals/` directory (e.g., `goals/my_category.py`)
2. Import and extend the goal list in `goals/__init__.py`

### Configuring Goals
The agent supports multiple goal categories organized in `goals/`:
- **Financial**: Money transfers, loan applications (`goals/finance.py`)
- **HR**: PTO booking, payroll status (`goals/hr.py`)  
- **Travel**: Flight/train booking, event finding (`goals/travel.py`)
- **Ecommerce**: Order tracking, package management (`goals/ecommerce.py`)
- **Food**: Restaurant ordering and cart management (`goals/food.py`)
- **MCP Integrations**: External service integrations like Stripe (`goals/stripe_mcp.py`)

Goals can use:
- **Native Tools**: Custom implementations in `/tools/` directory
- **MCP Tools**: External tools via Model Context Protocol servers (configured in `shared/mcp_config.py`)

See [adding-goals-and-tools.md](docs/adding-goals-and-tools.md) for detailed customization guide.

## Architecture

This system implements agentic AI—autonomous systems that pursue goals through iterative tool use and human feedback—with these key components:
1. **Goals** - High-level objectives accomplished through tool sequences (organized in `/goals/` by category)
2. **Native & MCP Tools** - Custom implementations and external service integrations
3. **Agent Loops** - LLM execution → tool calls → human input → repeat until goal completion
4. **Tool Approval** - Human confirmation for sensitive operations
5. **Conversation Management** - LLM-powered input validation and history summarization
6. **Durability** - Temporal workflows ensure reliable execution across failures

For detailed architecture information, see [architecture.md](docs/architecture.md).

## Commit Messages and Pull Requests
- Use clear commit messages describing the change purpose
- Reference specific files and line numbers when relevant (e.g., `workflows/agent_goal_workflow.py:125`)
- Open PRs describing **what changed** and **why**
- Ensure tests pass before submitting: `uv run pytest --workflow-environment=time-skipping`

## Additional Resources
- **Setup Guide**: [setup.md](docs/setup.md) - Detailed configuration instructions
- **Architecture Decisions**: [architecture-decisions.md](docs/architecture-decisions.md) - Why Temporal for AI agents
- **Demo Video**: [5-minute YouTube overview](https://www.youtube.com/watch?v=GEXllEH2XiQ)
- **Multi-Agent Demo**: [Advanced multi-agent execution](https://www.youtube.com/watch?v=8Dc_0dC14yY)


================================================
FILE: docker-compose.override.yml
================================================
services:
  api:
    volumes:
      - ./:/app:cached
    command: uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

  worker:
    volumes:
      - ./:/app:cached
    command: uv run scripts/run_worker.py

  train-api:
    volumes:
      - ./:/app:cached
    command: uv run thirdparty/train_api.py

  frontend:
    volumes:
      - ./frontend:/app:cached
    command: sh -c "apk update && apk add --no-cache xdg-utils && npm install && npx vite --host 0.0.0.0 --port 5173"



================================================
FILE: docker-compose.yml
================================================
services:
  # Database service
  postgresql:
    image: postgres:14
    container_name: temporal-postgresql
    environment:
      POSTGRES_USER: temporal
      POSTGRES_PASSWORD: temporal
      POSTGRES_DB: temporal
    volumes:
      - postgresql:/var/lib/postgresql/data
    networks:
      - temporal-network

  # Temporal services
  temporal:
    image: temporalio/auto-setup:1.27.2
    container_name: temporal
    ports:
      - "7233:7233"
    environment:
      - DB=postgres12
      - DB_PORT=5432
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=temporal
      - POSTGRES_SEEDS=postgresql
    depends_on:
      - postgresql
    networks:
      - temporal-network

  temporal-admin-tools:
    image: temporalio/admin-tools:1.27
    container_name: temporal-admin-tools
    depends_on:
      - temporal
    environment:
      - TEMPORAL_CLI_ADDRESS=temporal:7233
    networks:
      - temporal-network

  temporal-ui:
    image: temporalio/ui:2.37.2
    container_name: temporal-ui
    ports:
      - "8080:8080"
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
      - TEMPORAL_CORS_ORIGINS=http://localhost:8080
    depends_on:
      - temporal
    networks:
      - temporal-network

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: temporal-ai-agent-api
    ports:
      - "8000:8000"
    depends_on:
      - temporal
    networks:
      - temporal-network
    env_file:
      - .env
    environment:
      - TEMPORAL_ADDRESS=temporal:7233

  worker:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: temporal-ai-agent-worker
    depends_on:
      - temporal
    env_file:
      - .env
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    command: uv run scripts/run_worker.py
    networks:
      - temporal-network

  train-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: temporal-ai-agent-train-api
    depends_on:
      - temporal
    env_file:
      - .env
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    command: uv run thirdparty/train_api.py
    networks:
      - temporal-network

  frontend:
    image: node:18-alpine
    container_name: temporal-ai-agent-frontend
    working_dir: /app
    volumes:
      - ./frontend:/app
    command: sh -c "apk update && apk add --no-cache xdg-utils && npm install && npx vite --host 0.0.0.0"
    ports:
      - "5173:5173"
    depends_on:
      - api
    networks:
      - temporal-network

networks:
  temporal-network:
    driver: bridge

volumes:
  postgresql:



================================================
FILE: Dockerfile
================================================
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="$PATH:/root/.local/bin"

# Copy dependency files and README (needed for package build)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies and create virtual environment
RUN uv sync --frozen

# Copy application code
COPY . .

# Set Python to run in unbuffered mode (recommended for Docker)
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose the port the app will run on
EXPOSE 8000

# Default to running only the API server; worker and train-api are separate Compose services
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]



================================================
FILE: LICENSE
================================================
MIT License

Copyright (c) 2025 Steve Androulakis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



================================================
FILE: Makefile
================================================
.PHONY: setup install run-worker run-api run-frontend run-train-api run-legacy-worker run-enterprise setup-venv check-python run-dev

setup:
	uv sync
	cd frontend && npm install

# Run commands
run-worker:
	uv run scripts/run_worker.py

run-api:
	uv run uvicorn api.main:app --reload

run-frontend:
	cd frontend && npx vite

run-train-api:
	uv run thirdparty/train_api.py

run-legacy-worker:
	uv run scripts/run_legacy_worker.py

run-enterprise:
	cd enterprise && dotnet build && dotnet run

# Development environment setup
setup-temporal-mac:
	brew install temporal
	temporal server start-dev

# Run all development services
run-dev:
	@echo "Starting all development services..."
	@make run-worker & \
	make run-api & \
	make run-frontend & \
	wait

# Help command
help:
	@echo "Available commands:"
	@echo "  make setup              - Install all dependencies"
	@echo "  make run-worker         - Start the Temporal worker"
	@echo "  make run-api            - Start the API server"
	@echo "  make run-frontend       - Start the frontend development server"
	@echo "  make run-train-api      - Start the train API server"
	@echo "  make run-legacy-worker  - Start the legacy worker"
	@echo "  make run-enterprise     - Build and run the enterprise .NET worker"
	@echo "  make setup-temporal-mac - Install and start Temporal server on Mac"
	@echo "  make run-dev            - Start all development services (worker, API, frontend) in parallel"


================================================
FILE: pyproject.toml
================================================
[project]
name = "temporal_AI_agent"
version = "0.2.0"
description = "Temporal AI Agent"
authors = [
    { name = "Steve Androulakis", email = "steve.androulakis@temporal.io" },
    { name = "Laine Smith", email = "lainecaseysmith@gmail.com" },
    { name = "Joshua Smith", email = "josh.smith@temporal.io" },
]
requires-python = ">=3.10,<4.0"
readme = "README.md"
license = "MIT"
dependencies = [
    "temporalio>=1.8.0,<2",
    "litellm>=1.70.0,<2",
    "pyyaml>=6.0.2,<7",
    "fastapi>=0.115.6,<0.116",
    "uvicorn>=0.34.0,<0.35",
    "python-dotenv>=1.0.1,<2",
    "requests>=2.32.3,<3",
    "pandas>=2.2.3,<3",
    "stripe>=11.4.1,<12",
    "gtfs-kit>=10.1.1,<11",
    "fastmcp>=2.7.0,<3",
]

[project.urls]
"Bug Tracker" = "https://github.com/temporal-community/temporal-ai-agent/issues"

[dependency-groups]
dev = [
    "pytest>=8.2",
    "pytest-asyncio>=0.26.0,<0.27",
    "black~=23.7",
    "isort~=5.12",
    "mypy>=1.16.0,<2",
]

[tool.poe.tasks]
format = [{cmd = "black ."}, {cmd = "isort ."}]
lint = [{cmd = "black --check ."}, {cmd = "isort --check-only ."}, {ref = "lint-types" }]
lint-types = "mypy --check-untyped-defs --namespace-packages ."
test = "pytest"

[tool.hatch.metadata]
allow-direct-references = true

[tool.hatch.build]
packages = ["activities", "api", "goals", "models", "prompts", "shared", "tools", "workflows"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
asyncio_default_fixture_loop_scope = "function"
norecursedirs = ["vibe"]

[tool.mypy]
python_version = "3.10"
ignore_missing_imports = true
check_untyped_defs = true
namespace_packages = true
explicit_package_bases = true
ignore_errors = true

[tool.isort]
profile = "black"



================================================
FILE: temporal-ai-agent.sln
================================================
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.5.2.0
MinimumVisualStudioVersion = 10.0.40219.1
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "TrainSearchWorker", "enterprise\TrainSearchWorker.csproj", "{E415E5FE-0362-B204-B4B1-A5E60F3A436D}"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|Any CPU = Debug|Any CPU
		Release|Any CPU = Release|Any CPU
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		{E415E5FE-0362-B204-B4B1-A5E60F3A436D}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{E415E5FE-0362-B204-B4B1-A5E60F3A436D}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{E415E5FE-0362-B204-B4B1-A5E60F3A436D}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{E415E5FE-0362-B204-B4B1-A5E60F3A436D}.Release|Any CPU.Build.0 = Release|Any CPU
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
	GlobalSection(ExtensibilityGlobals) = postSolution
		SolutionGuid = {463FDBB3-0167-4747-8007-C25ADDC83630}
	EndGlobalSection
EndGlobal



================================================
FILE: .env.example
================================================
# Example environment configuration

### LLM configuration
LLM_MODEL=openai/gpt-4o
LLM_KEY=sk-proj-...
# LLM_MODEL=anthropic/claude-3-5-sonnet-20240620
# LLM_KEY=${ANTHROPIC_API_KEY}
# LLM_MODEL=gemini/gemini-2.5-flash-preview-04-17
# LLM_KEY=${GOOGLE_API_KEY}

### Tool API keys
# RAPIDAPI_KEY=9df2cb5...                         # Optional - if unset flight search generates realistic mock data
# RAPIDAPI_HOST_FLIGHTS=sky-scrapper.p.rapidapi.com # For real travel flight information (optional)
RAPIDAPI_HOST_PACKAGE=trackingpackage.p.rapidapi.com # For eCommerce order status package tracking tool
FOOTBALL_DATA_API_KEY=
# Leave blank to use the built-in mock fixtures generator

STRIPE_API_KEY=sk_test_51J...
# Optional for `goal_event_flight_invoice` – if unset a mock invoice is created.
# Sign up for a free Stripe account and get a test key at https://dashboard.stripe.com/test/apikeys

### Temporal connection (optional)
# Uncomment and update these values to connect to a non-default Temporal server
# TEMPORAL_ADDRESS=namespace.acct.tmprl.cloud:7233
# TEMPORAL_NAMESPACE=default
# TEMPORAL_TASK_QUEUE=agent-task-queue
# TEMPORAL_TLS_CERT='path/to/cert.pem'
# TEMPORAL_TLS_KEY='path/to/key.pem'
# TEMPORAL_API_KEY=abcdef1234567890

### Agent goal configuration
# Set starting goal of agent - if unset default is goal_event_flight_invoice (single agent mode)
#AGENT_GOAL=goal_choose_agent_type  # for multi-goal mode (experimental)
AGENT_GOAL=goal_event_flight_invoice
#AGENT_GOAL=goal_match_train_invoice # for replay goal

# Choose which goal categories are listed by the Agent Goal picker if enabled above
# Options: system (always included), hr, travel-flights, travel-trains, fin, ecommerce, mcp-integrations, food, all
GOAL_CATEGORIES=all
#GOAL_CATEGORIES=travel-flights

### Other settings
SHOW_CONFIRM=True

# Money Scenarios:
# Set if you want it to really start workflows - otherwise it'll fake it
# if you want it to be real you'll need moneytransfer and early return workers running
FIN_START_REAL_WORKFLOW=FALSE



================================================
FILE: activities/__init__.py
================================================
[Empty file]


================================================
FILE: activities/tool_activities.py
================================================
import inspect
import json
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence

from dotenv import load_dotenv
from litellm import completion
from temporalio import activity
from temporalio.common import RawValue
from temporalio.exceptions import ApplicationError

from models.data_types import (
    EnvLookupInput,
    EnvLookupOutput,
    ToolPromptInput,
    ValidationInput,
    ValidationResult,
)
from models.tool_definitions import MCPServerDefinition
from shared.mcp_client_manager import MCPClientManager

# Import MCP client libraries
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    # Fallback if MCP not installed
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None

load_dotenv(override=True)


class ToolActivities:
    def __init__(self, mcp_client_manager: MCPClientManager = None):
        """Initialize LLM client using LiteLLM and optional MCP client manager"""
        self.llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4")
        self.llm_key = os.environ.get("LLM_KEY")
        self.llm_base_url = os.environ.get("LLM_BASE_URL")
        self.mcp_client_manager = mcp_client_manager
        print(f"Initializing ToolActivities with LLM model: {self.llm_model}")
        if self.llm_base_url:
            print(f"Using custom base URL: {self.llm_base_url}")
        if self.mcp_client_manager:
            print("MCP client manager enabled for connection pooling")

    @activity.defn
    async def agent_validatePrompt(
        self, validation_input: ValidationInput
    ) -> ValidationResult:
        """
        Validates the prompt in the context of the conversation history and agent goal.
        Returns a ValidationResult indicating if the prompt makes sense given the context.
        """
        # Create simple context string describing tools and goals
        tools_description = []
        for tool in validation_input.agent_goal.tools:
            tool_str = f"Tool: {tool.name}\n"
            tool_str += f"Description: {tool.description}\n"
            tool_str += "Arguments: " + ", ".join(
                [f"{arg.name} ({arg.type})" for arg in tool.arguments]
            )
            tools_description.append(tool_str)
        tools_str = "\n".join(tools_description)

        # Convert conversation history to string
        history_str = json.dumps(validation_input.conversation_history, indent=2)

        # Create context instructions
        context_instructions = f"""The agent goal and tools are as follows:
            Description: {validation_input.agent_goal.description}
            Available Tools:
            {tools_str}
            The conversation history to date is:
            {history_str}"""

        # Create validation prompt
        validation_prompt = f"""The user's prompt is: "{validation_input.prompt}"
            Please validate if this prompt makes sense given the agent goal and conversation history.
            If the prompt makes sense toward the goal then validationResult should be true.
            If the prompt is wildly nonsensical or makes no sense toward the goal and current conversation history then validationResult should be false.
            If the response is low content such as "yes" or "that's right" then the user is probably responding to a previous prompt.  
             Therefore examine it in the context of the conversation history to determine if it makes sense and return true if it makes sense.
            Return ONLY a JSON object with the following structure:
                "validationResult": true/false,
                "validationFailedReason": "If validationResult is false, provide a clear explanation to the user in the response field 
                about why their request doesn't make sense in the context and what information they should provide instead.
                validationFailedReason should contain JSON in the format
                {{
                    "next": "question",
                    "response": "[your reason here and a response to get the user back on track with the agent goal]"
                }}
                If validationResult is true (the prompt makes sense), return an empty dict as its value {{}}"
            """

        # Call the LLM with the validation prompt
        prompt_input = ToolPromptInput(
            prompt=validation_prompt, context_instructions=context_instructions
        )

        result = await self.agent_toolPlanner(prompt_input)

        return ValidationResult(
            validationResult=result.get("validationResult", False),
            validationFailedReason=result.get("validationFailedReason", {}),
        )

    @activity.defn
    async def agent_toolPlanner(self, input: ToolPromptInput) -> dict:
        messages = [
            {
                "role": "system",
                "content": input.context_instructions
                + ". The current date is "
                + datetime.now().strftime("%B %d, %Y"),
            },
            {
                "role": "user",
                "content": input.prompt,
            },
        ]

        try:
            completion_kwargs = {
                "model": self.llm_model,
                "messages": messages,
                "api_key": self.llm_key,
            }

            # Add base_url if configured
            if self.llm_base_url:
                completion_kwargs["base_url"] = self.llm_base_url

            response = completion(**completion_kwargs)

            response_content = response.choices[0].message.content
            activity.logger.info(f"Raw LLM response: {repr(response_content)}")
            activity.logger.info(f"LLM response content: {response_content}")
            activity.logger.info(f"LLM response type: {type(response_content)}")
            activity.logger.info(
                f"LLM response length: {len(response_content) if response_content else 'None'}"
            )

            # Use the new sanitize function
            response_content = self.sanitize_json_response(response_content)
            activity.logger.info(f"Sanitized response: {repr(response_content)}")

            return self.parse_json_response(response_content)
        except Exception as e:
            print(f"Error in LLM completion: {str(e)}")
            raise

    def parse_json_response(self, response_content: str) -> dict:
        """
        Parses the JSON response content and returns it as a dictionary.
        """
        try:
            data = json.loads(response_content)
            return data
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            raise

    def sanitize_json_response(self, response_content: str) -> str:
        """
        Sanitizes the response content to ensure it's valid JSON.
        """
        # Remove any markdown code block markers
        response_content = response_content.replace("```json", "").replace("```", "")

        # Remove any leading/trailing whitespace
        response_content = response_content.strip()

        return response_content

    @activity.defn
    async def get_wf_env_vars(self, input: EnvLookupInput) -> EnvLookupOutput:
        """gets env vars for workflow as an activity result so it's deterministic
        handles default/None
        """
        output: EnvLookupOutput = EnvLookupOutput(
            show_confirm=input.show_confirm_default, multi_goal_mode=False
        )
        show_confirm_value = os.getenv(input.show_confirm_env_var_name)
        if show_confirm_value is None:
            output.show_confirm = input.show_confirm_default
        elif show_confirm_value is not None and show_confirm_value.lower() == "false":
            output.show_confirm = False
        else:
            output.show_confirm = True

        first_goal_value = os.getenv("AGENT_GOAL")
        if first_goal_value is None:
            output.multi_goal_mode = False  # default to single agent mode if unset
        elif (
            first_goal_value is not None
            and first_goal_value.lower() == "goal_choose_agent_type"
        ):
            output.multi_goal_mode = True
        else:
            output.multi_goal_mode = False

        return output

    @activity.defn
    async def mcp_tool_activity(
        self, tool_name: str, tool_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """MCP Tool - now using pooled connections"""
        activity.logger.info(f"Executing MCP tool: {tool_name} with args: {tool_args}")

        # Extract server definition
        server_definition = tool_args.pop("server_definition", None)

        if self.mcp_client_manager:
            # Use pooled connection
            return await self._execute_mcp_tool_pooled(
                tool_name, tool_args, server_definition
            )
        else:
            # Fallback to original implementation
            return await _execute_mcp_tool(tool_name, tool_args, server_definition)

    async def _execute_mcp_tool_pooled(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        server_definition: MCPServerDefinition | Dict[str, Any] | None,
    ) -> Dict[str, Any]:
        """Execute MCP tool using pooled client connection"""
        activity.logger.info(f"Executing MCP tool with pooled connection: {tool_name}")

        # Convert argument types for MCP tools
        converted_args = _convert_args_types(tool_args)

        try:
            # Get pooled client
            client = await self.mcp_client_manager.get_client(server_definition)

            # Call the tool using existing client session
            result = await client.call_tool(tool_name, arguments=converted_args)
            normalized_result = _normalize_result(result)

            return {
                "tool": tool_name,
                "success": True,
                "content": normalized_result,
            }
        except Exception as e:
            activity.logger.error(f"MCP tool {tool_name} failed: {str(e)}")
            return {
                "tool": tool_name,
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
            }


@activity.defn(dynamic=True)
async def dynamic_tool_activity(args: Sequence[RawValue]) -> dict:
    from tools import get_handler

    tool_name = activity.info().activity_type  # e.g. "FindEvents"
    tool_args = activity.payload_converter().from_payload(args[0].payload, dict)
    activity.logger.info(f"Running dynamic tool '{tool_name}' with args: {tool_args}")

    # Check if this is an MCP tool call by looking for server_definition in args
    server_definition = tool_args.pop("server_definition", None)

    if server_definition:
        # This is an MCP tool call - handle it directly
        activity.logger.info(f"Executing MCP tool: {tool_name}")
        return await _execute_mcp_tool(tool_name, tool_args, server_definition)
    else:
        # This is a regular tool - delegate to the relevant function
        handler = get_handler(tool_name)
        if inspect.iscoroutinefunction(handler):
            result = await handler(tool_args)
        else:
            result = handler(tool_args)

        # Optionally log or augment the result
        activity.logger.info(f"Tool '{tool_name}' result: {result}")
        return result


# MCP Client Activities


def _build_connection(
    server_definition: MCPServerDefinition | Dict[str, Any] | None,
) -> Dict[str, Any]:
    """Build connection parameters from MCPServerDefinition or dict"""
    if server_definition is None:
        # Default to stdio connection with the main server
        return {"type": "stdio", "command": "python", "args": ["server.py"], "env": {}}

    # Handle both MCPServerDefinition objects and dicts (from Temporal serialization)
    if isinstance(server_definition, dict):
        return {
            "type": server_definition.get("connection_type", "stdio"),
            "command": server_definition.get("command", "python"),
            "args": server_definition.get("args", ["server.py"]),
            "env": server_definition.get("env", {}) or {},
        }

    return {
        "type": server_definition.connection_type,
        "command": server_definition.command,
        "args": server_definition.args,
        "env": server_definition.env or {},
    }


def _normalize_result(result: Any) -> Any:
    """Normalize MCP tool result for serialization"""
    if hasattr(result, "content"):
        # Handle MCP result objects
        if hasattr(result.content, "__iter__") and not isinstance(result.content, str):
            return [
                item.text if hasattr(item, "text") else str(item)
                for item in result.content
            ]
        return str(result.content)
    return result


def _convert_args_types(tool_args: Dict[str, Any]) -> Dict[str, Any]:
    """Convert string arguments to appropriate types for MCP tools"""
    converted_args = {}

    for key, value in tool_args.items():
        if key == "server_definition":
            # Skip server_definition - it's metadata
            continue

        if isinstance(value, str):
            # Try to convert string values to appropriate types
            if value.isdigit():
                # Convert numeric strings to integers
                converted_args[key] = int(value)
            elif value.replace(".", "").isdigit() and value.count(".") == 1:
                # Convert decimal strings to floats
                converted_args[key] = float(value)
            elif value.lower() in ("true", "false"):
                # Convert boolean strings
                converted_args[key] = value.lower() == "true"
            else:
                # Keep as string
                converted_args[key] = value
        else:
            # Keep non-string values as-is
            converted_args[key] = value

    return converted_args


async def _execute_mcp_tool(
    tool_name: str,
    tool_args: Dict[str, Any],
    server_definition: MCPServerDefinition | Dict[str, Any] | None,
) -> Dict[str, Any]:
    """Execute an MCP tool with the given arguments and server definition"""
    activity.logger.info(f"Executing MCP tool: {tool_name}")

    # Convert argument types for MCP tools
    converted_args = _convert_args_types(tool_args)
    connection = _build_connection(server_definition)

    try:
        if connection["type"] == "stdio":
            # Handle stdio connection
            async with _stdio_connection(
                command=connection.get("command", "python"),
                args=connection.get("args", ["server.py"]),
                env=connection.get("env", {}),
            ) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    activity.logger.info(f"Initializing MCP session for {tool_name}")
                    await session.initialize()
                    activity.logger.info(f"MCP session initialized for {tool_name}")

                    # Call the tool
                    activity.logger.info(
                        f"Calling MCP tool {tool_name} with args: {converted_args}"
                    )
                    try:
                        result = await session.call_tool(
                            tool_name, arguments=converted_args
                        )
                        activity.logger.info(
                            f"MCP tool {tool_name} returned result: {result}"
                        )
                    except Exception as tool_exc:
                        activity.logger.error(
                            f"MCP tool {tool_name} call failed: {type(tool_exc).__name__}: {tool_exc}"
                        )
                        raise

                    normalized_result = _normalize_result(result)
                    activity.logger.info(f"MCP tool {tool_name} completed successfully")

                    return {
                        "tool": tool_name,
                        "success": True,
                        "content": normalized_result,
                    }

        elif connection["type"] == "tcp":
            # Handle TCP connection (placeholder for future implementation)
            raise ApplicationError("TCP connections not yet implemented")

        else:
            raise ApplicationError(f"Unsupported connection type: {connection['type']}")

    except Exception as e:
        activity.logger.error(f"MCP tool {tool_name} failed: {str(e)}")

        # Return error information
        return {
            "tool": tool_name,
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


@asynccontextmanager
async def _stdio_connection(command: str, args: list, env: dict):
    """Create stdio connection to MCP server"""
    if stdio_client is None:
        raise ApplicationError("MCP client libraries not available")

    # Create server parameters
    server_params = StdioServerParameters(command=command, args=args, env=env)

    async with stdio_client(server_params) as (read, write):
        yield read, write


@activity.defn
async def mcp_list_tools(
    server_definition: MCPServerDefinition, include_tools: Optional[List[str]] = None
) -> Dict[str, Any]:
    """List available MCP tools from the specified server"""

    activity.logger.info(f"Listing MCP tools for server: {server_definition.name}")

    connection = _build_connection(server_definition)

    try:
        if connection["type"] == "stdio":
            async with _stdio_connection(
                command=connection.get("command", "python"),
                args=connection.get("args", ["server.py"]),
                env=connection.get("env", {}),
            ) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    await session.initialize()

                    # List available tools
                    tools_response = await session.list_tools()

                    # Process tools based on include_tools filter
                    tools_info = {}
                    for tool in tools_response.tools:
                        # If include_tools is specified, only include those tools
                        if include_tools is None or tool.name in include_tools:
                            tools_info[tool.name] = {
                                "name": tool.name,
                                "description": tool.description,
                                "inputSchema": (
                                    tool.inputSchema.model_dump()
                                    if hasattr(tool.inputSchema, "model_dump")
                                    else str(tool.inputSchema)
                                ),
                            }

                    activity.logger.info(
                        f"Found {len(tools_info)} tools for server {server_definition.name}"
                    )

                    return {
                        "server_name": server_definition.name,
                        "success": True,
                        "tools": tools_info,
                        "total_available": len(tools_response.tools),
                        "filtered_count": len(tools_info),
                    }

        elif connection["type"] == "tcp":
            raise ApplicationError("TCP connections not yet implemented")

        else:
            raise ApplicationError(f"Unsupported connection type: {connection['type']}")

    except Exception as e:
        activity.logger.error(
            f"Failed to list tools for server {server_definition.name}: {str(e)}"
        )

        return {
            "server_name": server_definition.name,
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }



================================================
FILE: api/main.py
================================================
import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from temporalio.api.enums.v1 import WorkflowExecutionStatus
from temporalio.client import Client
from temporalio.exceptions import TemporalError

from goals import goal_list
from models.data_types import AgentGoalWorkflowParams, CombinedInput
from shared.config import TEMPORAL_TASK_QUEUE, get_temporal_client
from workflows.agent_goal_workflow import AgentGoalWorkflow

app = FastAPI()
temporal_client: Optional[Client] = None

# Load environment variables
load_dotenv()


def get_initial_agent_goal():
    """Get the agent goal from environment variables."""
    env_goal = os.getenv(
        "AGENT_GOAL", "goal_event_flight_invoice"
    )  # if no goal is set in the env file, default to single agent mode
    for listed_goal in goal_list:
        if listed_goal.id == env_goal:
            return listed_goal


@app.on_event("startup")
async def startup_event():
    global temporal_client
    temporal_client = await get_temporal_client()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Temporal AI Agent!"}


@app.get("/tool-data")
async def get_tool_data():
    """Calls the workflow's 'get_tool_data' query."""
    try:
        # Get workflow handle
        handle = temporal_client.get_workflow_handle("agent-workflow")

        # Check if the workflow is completed
        workflow_status = await handle.describe()
        if workflow_status.status == 2:
            # Workflow is completed; return an empty response
            return {}

        # Query the workflow
        tool_data = await handle.query("get_latest_tool_data")
        return tool_data
    except TemporalError as e:
        # Workflow not found; return an empty response
        print(e)
        return {}


@app.get("/get-conversation-history")
async def get_conversation_history():
    """Calls the workflow's 'get_conversation_history' query."""
    try:
        handle = temporal_client.get_workflow_handle("agent-workflow")

        failed_states = [
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_TERMINATED,
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_CANCELED,
            WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_FAILED,
        ]

        description = await handle.describe()
        if description.status in failed_states:
            print("Workflow is in a failed state. Returning empty history.")
            return []

        # Set a timeout for the query
        try:
            conversation_history = await asyncio.wait_for(
                handle.query("get_conversation_history"),
                timeout=5,  # Timeout after 5 seconds
            )
            return conversation_history
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=404,
                detail="Temporal query timed out (worker may be unavailable).",
            )

    except TemporalError as e:
        error_message = str(e)
        print(f"Temporal error: {error_message}")

        # If worker is down or no poller is available, return a 404
        if "no poller seen for task queue recently" in error_message:
            raise HTTPException(
                status_code=404, detail="Workflow worker unavailable or not found."
            )

        if "workflow not found" in error_message:
            await start_workflow()
            return []
        else:
            # For other Temporal errors, return a 500
            raise HTTPException(
                status_code=500, detail="Internal server error while querying workflow."
            )


@app.get("/agent-goal")
async def get_agent_goal():
    """Calls the workflow's 'get_agent_goal' query."""
    try:
        # Get workflow handle
        handle = temporal_client.get_workflow_handle("agent-workflow")

        # Check if the workflow is completed
        workflow_status = await handle.describe()
        if workflow_status.status == 2:
            # Workflow is completed; return an empty response
            return {}

        # Query the workflow
        agent_goal = await handle.query("get_agent_goal")
        return agent_goal
    except TemporalError as e:
        # Workflow not found; return an empty response
        print(e)
        return {}


@app.post("/send-prompt")
async def send_prompt(prompt: str):
    # Create combined input with goal from environment
    combined_input = CombinedInput(
        tool_params=AgentGoalWorkflowParams(None, None),
        agent_goal=get_initial_agent_goal(),
        # change to get from workflow query
    )

    workflow_id = "agent-workflow"

    # Start (or signal) the workflow
    await temporal_client.start_workflow(
        AgentGoalWorkflow.run,
        combined_input,
        id=workflow_id,
        task_queue=TEMPORAL_TASK_QUEUE,
        start_signal="user_prompt",
        start_signal_args=[prompt],
    )

    return {"message": f"Prompt '{prompt}' sent to workflow {workflow_id}."}


@app.post("/confirm")
async def send_confirm():
    """Sends a 'confirm' signal to the workflow."""
    workflow_id = "agent-workflow"
    handle = temporal_client.get_workflow_handle(workflow_id)
    await handle.signal("confirm")
    return {"message": "Confirm signal sent."}


@app.post("/end-chat")
async def end_chat():
    """Sends a 'end_chat' signal to the workflow."""
    workflow_id = "agent-workflow"

    try:
        handle = temporal_client.get_workflow_handle(workflow_id)
        await handle.signal("end_chat")
        return {"message": "End chat signal sent."}
    except TemporalError as e:
        print(e)
        # Workflow not found; return an empty response
        return {}


@app.post("/start-workflow")
async def start_workflow():
    initial_agent_goal = get_initial_agent_goal()

    # Create combined input
    combined_input = CombinedInput(
        tool_params=AgentGoalWorkflowParams(None, None),
        agent_goal=initial_agent_goal,
    )

    workflow_id = "agent-workflow"

    # Start the workflow with the starter prompt from the goal
    await temporal_client.start_workflow(
        AgentGoalWorkflow.run,
        combined_input,
        id=workflow_id,
        task_queue=TEMPORAL_TASK_QUEUE,
        start_signal="user_prompt",
        start_signal_args=["### " + initial_agent_goal.starter_prompt],
    )

    return {
        "message": f"Workflow started with goal's starter prompt: {initial_agent_goal.starter_prompt}."
    }



================================================
FILE: docs/README.md
================================================
# Documentation Index

- **architecture.md** - Overview of system components and how they interact.
- **architecture-decisions.md** - Rationale behind key design choices.
- **changelog.md** - Project history and notable changes.
- **contributing.md** - How to contribute and run tests.
- **setup.md** - Installation and configuration instructions.
- **testing.md** - Commands for running the test suite.
- **adding-goals-and-tools.md** - Guide to extending the agent with new goals and tools.
- **todo.md** - Planned enhancements and future work.



================================================
FILE: docs/adding-goals-and-tools.md
================================================
# Customizing the Agent
The agent operates in single-agent mode by default, focusing on one specific goal. It also supports an experimental multi-agent mode where users can have multiple agents, each with their own goal, and supports switching back to choosing a new goal at the end of every successful goal (or even mid-goal). 

A goal can use two types of tools:
- **Native Tools**: Custom tools implemented directly in the codebase (in `/tools/`)
- **MCP Tools**: External tools accessed via Model Context Protocol (MCP) servers

It may be helpful to review the [architecture](./architecture.md) for a guide and definition of goals, tools, etc.

## Adding a New Goal Category
Goal Categories lets you pick which groups of goals to show in multi-agent mode. Set via an .env setting, `GOAL_CATEGORIES`. 
Even if you don't intend to use the goal in a multi-agent scenario, goal categories are useful for organization and discovery.
1. Pick a unique one that has some business meaning
2. Use it in your [.env](./.env) file
3. Add to [.env.example](./.env.example)
4. Use it in your Goal definition, see below.

## Adding a Goal
1. Create a new Python file in the `/goals/` directory (e.g., `goals/my_category.py`) - these files contain descriptions of goals and the tools used to achieve them
2. Pick a name for your goal! (such as "goal_hr_schedule_pto")
3. Fill out the required elements:
-  `id`: needs to be the same as the name
- `agent_name`: user-facing name for the agent/chatbot
- `category_tag`: category for the goal
- `agent_friendly_description`: user-facing description of what the agent/chatbot does
- `tools`: the list of **native tools** the goal uses. These are defined in [tools/tool_registry.py](tools/tool_registry.py) as `tool_registry.[name_of_tool]`

Example:
```python
tools=[
    tool_registry.current_pto_tool,
    tool_registry.future_pto_calc_tool,
    tool_registry.book_pto_tool,
]
```
- `mcp_server_definition`: (Optional) MCP server configuration for external tools. Can use predefined configurations from `shared/mcp_config.py` or define custom ones. See [MCP Tools section](#adding-mcp-tools) below.
- `description`: LLM-facing description of the goal that lists all tools (native and MCP) by name and purpose.
- `starter_prompt`: LLM-facing first prompt given to begin the scenario. This field can contain instructions that are different from other goals, like "begin by providing the output of the first tool" rather than waiting on user confirmation. (See [goal_choose_agent_type](tools/goal_registry.py) for an example.)
- `example_conversation_history`: LLM-facing sample conversation/interaction regarding the goal. See the existing goals for how to structure this.
4. Add your new goal to a list variable (e.g., `my_category_goals: List[AgentGoal] = [your_super_sweet_new_goal]`)
5. Import and extend the goal list in `goals/__init__.py` by adding:
   - Import: `from goals.my_category import my_category_goals`
   - Extend: `goal_list.extend(my_category_goals)`

## Adding Native Tools

Native tools are custom implementations that run directly in your codebase. Use these for business logic specific to your application.

### Note on Optional Tools
Tools can be optional - you can indicate this in the tool listing of goal description (see above section re: goal registry) by adding something like, "This step is optional and can be skipped by moving to the next tool." Here is an example from an older iteration of the `goal_hr_schedule_pto` goal, when it was going to have an optional step to check for existing calendar conflicts:

```
description="Help the user gather args for these tools in order: "
    "1. CurrentPTO: Tell the user how much PTO they currently have "
    "2. FuturePTO: Tell the user how much PTO they will have as of the prospective date "
    "3. CalendarConflict: Tell the user what conflicts if any exist around the prospective date on a list of calendars. This step is optional and can be skipped by moving to the next tool. "
    "4. BookPTO: Book PTO "
```

Tools should generally return meaningful information and be generally ‘failsafe’ in returning a useful result based on input.
(If you're doing a local data approach like those in [.tools/data/](./tools/data/)) it's good to document how they can be setup to get a good result in tool specific [setup](./setup.md).

### Add to Tool Registry
1.  Open [/tools/tool_registry.py](tools/tool_registry.py) - this file contains mapping of tool names to tool definitions (so the AI understands how to use them)
2. Define the tool
- `name`: name of the tool - this is the name as defined in the goal description list of tools. The name should be (sort of) the same as the tool name given in the goal description. So, if the description lists "CurrentPTO" as a tool, the name here should be `current_pto_tool`.
- `description`: LLM-facing description of tool
- `arguments`: These are the _input_ arguments to the tool. Each input argument should be defined as a [ToolArgument](./models/tool_definitions.py). Tools don't have to have arguments but the arguments list has to be declared. If the tool you're creating doesn't have inputs, define arguments as `arguments=[]`

### Create Each Native Tool Implementation
- The tools themselves are defined in their own files in `/tools` - you can add a subfolder to organize them, see the hr tools for an example.
- The file name and function name will be the same as each other and should also be the same as the name of the tool, without "tool" - so `current_pto_tool` would be `current_pto.py` with a function named `current_pto` within it.
- The function should have `args: dict` as the input and also return a `dict`
- The return dict should match the output format you specified in the goal's `example_conversation_history`
- tools are where the user input+model output becomes deterministic. Add validation here to make sure what the system is doing is valid and acceptable

### Add to `tools/__init__.py` and the tool get_handler()
- In [tools/__init__.py](./tools/__init__.py), add an import statement for each new native tool as well as an applicable return statement in `get_handler`. The tool name here should match the tool name as described in the goal's `description` field.
Example:
```python
if tool_name == "CurrentPTO":
    return current_pto
```

### Update workflow_helpers.py
- Add your new native tool to the static tools list in [workflows/workflow_helpers.py](workflows/workflow_helpers.py) so it's correctly identified as a native tool rather than an MCP tool.

## Adding MCP Tools

MCP (Model Context Protocol) tools are external tools provided by MCP servers. They're useful for integrating with third-party services like Stripe, databases, or APIs without implementing custom code.

### Configure MCP Server Definition
You can either use predefined MCP server configurations from `shared/mcp_config.py` or define custom ones. 

#### Using Predefined Configurations
```python
from shared.mcp_config import get_stripe_mcp_server_definition

# In your goal definition:
mcp_server_definition=get_stripe_mcp_server_definition(included_tools=["list_products", "create_customer"])
```

#### Custom MCP Server Definition
Add an `mcp_server_definition` to your goal:

```python
mcp_server_definition=MCPServerDefinition(
    name="stripe-mcp",
    command="npx",
    args=[
        "-y",
        "@stripe/mcp",
        "--tools=all",
        f"--api-key={os.getenv('STRIPE_API_KEY')}",
    ],
    env=None,
    included_tools=[
        "list_products",
        "list_prices", 
        "create_customer",
        "create_invoice",
        "create_payment_link",
    ],
)
```

### MCP Tool Configuration
- `name`: Identifier for the MCP server
- `command`: Command to start the MCP server (e.g., "npx", "python")
- `args`: Arguments to pass to the command
- `env`: Environment variables for the server (optional)
- `included_tools`: List of specific tools to use from the server (optional - if omitted, all tools are included)

### How MCP Tools Work
- MCP tools are automatically loaded when the workflow starts
- They're dynamically converted to `ToolDefinition` objects
- The system automatically routes MCP tool calls to the appropriate MCP server
- No additional code implementation needed - just configuration

## Tool Confirmation
There are three ways to manage confirmation of tool runs:
1. Arguments confirmation box - confirm tool arguments and execution with a button click
   -  Can be disabled by env setting: `SHOW_CONFIRM=FALSE`
2. Soft prompt confirmation via asking the model to prompt for confirmation: “Are you ready to be invoiced for the total cost of the train tickets?” in the [goal_registry](./tools/goal_registry.py).
3. Hard confirmation requirement as a tool argument. See for example the PTO Scheduling Tool:
```Python
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of user's desire to book PTO",
        ),
```
If you really want to wait for user confirmation, record it on the workflow (as a Signal) and not rely on the LLM to probably get it, use option #3. 
I recommend exploring all three. For a demo, I would decide if you want the Arguments confirmation in the UI, and if not I'd generally go with option #2 but use #3 for tools that make business sense to confirm, e.g. those tools that take action/write data.

## Add a Goal & Tools Checklist

### For All Goals:
- [ ] Create goal file in `/goals/` directory (e.g., `goals/my_category.py`)
- [ ] Add goal to the category's goal list in the file
- [ ] Import and extend the goal list in `goals/__init__.py`
- [ ] If a new category, add Goal Category to [.env](./.env) and [.env.example](./.env.example)

### For Native Tools:
- [ ] Add native tools to [tool_registry.py](tools/tool_registry.py)
- [ ] Implement tool functions in `/tools/` directory
- [ ] Add tools to [tools/__init__.py](tools/__init__.py) in the `get_handler()` function
- [ ] Add tool names to static tools list in [workflows/workflow_helpers.py](workflows/workflow_helpers.py)

### For MCP Tools:
- [ ] Add `mcp_server_definition` to your goal configuration (use `shared/mcp_config.py` for common servers)
- [ ] Ensure MCP server is available and properly configured
- [ ] Set required environment variables (API keys, etc.)
- [ ] Test MCP server connectivity before running the agent
- [ ] If creating new MCP server configs, add them to `shared/mcp_config.py` for reuse

And that's it! Happy AI Agent building!



================================================
FILE: docs/architecture-decisions.md
================================================
# Architecture Decisions
This documents some of the "why" behind the [architecture](./architecture.md). 

## AI Models
We wanted to have flexibility to use different models, because this space is changing rapidly and models get better regularly.
Also, for you, we wanted to let you pick your model of choice. The system is designed to make changing models out simple. For how to do that, checkout the [setup guide](./setup.md).

## Temporal
We asked one of the AI models used in this demo to answer this question (edited minorly):

### Reliability and State Management:
 Temporal ensures durability and fault tolerance, which are critical for agentic AI systems that involve long-running, complex workflows. For example, it preserves application state across failures, allowing AI agents to resume from where they left off without losing progress. Major AI companies use this for research experiments and agentic flows, where reliability is essential for continuous exploration.
### Handling Complex, Dynamic Workflows: 
Agentic AI often involves unpredictable, multi-step processes like web crawling or data searching. Temporal’s workflow orchestration simplifies managing these tasks by abstracting complexity, providing features like retries, timeouts, and signals/queries. Temporal makes observability and resuming failed complex experiments and deep searches simple.
### Scalability and Speed: 
Temporal enables rapid development and scaling, crucial for AI systems handling large-scale experiments or production workloads. AI model deployment and SRE teams use it to get code to production quickly with scale as a focus, while research teams can (and do!) run hundreds of experiments daily. Temporal customers report a significant reduction in development time (e.g., 20 weeks to 2 weeks for a feature).
### Observability and Debugging: 
Agentic AI systems need insight into where processes succeed or fail. Temporal provides end-to-end visibility and durable workflow history, which Temporal customers are using to track agentic flows and understand failure points.
### Simplified Error Handling: 
Temporal abstracts failure management (e.g., retries, rollbacks) so developers can focus on AI logic rather than "plumbing" code. This is vital for agentic AI, where external interactions (e.g., APIs, data sources) are prone to failure.
### Flexibility for Experimentation: 
For research-heavy agentic AI, Temporal supports dynamic, code-first workflows and easy integration of new signals/queries, aligning with researchers needs to iterate quickly on experimental paths.

In essence, Temporal’s value lies in its ability to make agentic AI systems more reliable, scalable, and easier to develop by handling the underlying complexity of distributed workflows for both research and applied AI tasks.

Temporal was built to solve the problems of distributed computing, including scalability, reliability, security, visibility, and complexity. Agentic AI systems are complex distributed systems, so Temporal should fit well. Scaling, security, and productionalization are major pain points in March 2025 for building agentic systems.

In this system Temporal lets you:
- Orchestrate interactions across distributed data stores and tools <br />
- Hold state, potentially over long periods of time <br />
- Ability to ‘self-heal’ and retry until the (probabilistic) LLM returns valid data <br />
- Support for human intervention such as approvals <br />
- Parallel processing for efficiency of data retrieval and tool use <br />


================================================
FILE: docs/architecture.md
================================================
# Elements
These are the main elements of this system. See [architecture decisions](./architecture-decisions.md) for information beind these choices.
In this document we will explain each element and their interactions, and then connect them all at the end.
<img src="./assets/Architecture_elements.png" width="50%" alt="Architecture Elements">

## Workflow 
This is a [Temporal Workflow](https://docs.temporal.io/workflows) - a durable straightforward description of the process to be executed. See [agent_goal_workflow.py](./workflows/agent_goal_workflow.py).
Temporal is used to make the process scalable, durable, reliable, secure, and visible.

### Workflow Responsibilities:
- Orchestrates interactive loops:
    - LLM Loop: Prompts LLM, durably executes LLM, stores responses
    - Interactive Loop: Elicits responses from input (in our case a human) and validates input responses
    - Tool Execution Loop: Durably executes Tools
- Keeps record of all interactions ([Signals, Queries, Updates](https://docs.temporal.io/develop/python/message-passing))
- Handles failures gracefully
- Input, LLM and Tool interaction history stored for debugging and analysis

## Activities
These are [Temporal Activities](https://docs.temporal.io/activities). Defined as simple functions, they are auto-retried async/event driven behind the scenes. Activities durably execute Tools and the LLM. See [a sample activity](./activities/tool_activities.py).

## Tools 
Tools define the capabilities of the system. They are simple Python functions (could be in any language as Temporal supports multiple languages).
They are executed by Temporal Activities. They are “just code” - can connect to any API or system. They also are where the deterministic business logic is: you can validate and retry actions using code you write.
Failures are handled gracefully by Temporal.

Activities + Tools turn the probabalistic input from the user and LLM into deterministic action.

## Prompts
Prompts are where the instructions to the LLM are. Prompts are made up of initial instructions, goal instructions, and tool instructions. 
See [agent prompts](./prompts/agent_prompt_generators.py) and [goal & tool prompts](./tools/goal_registry.py). 

This is where you can add probabalistic business logic to
- to control process flow
- describe what to do
- give examples of interactions
- give instruction and validation for the LLM

## LLM
Probabalistic execution: it will _probably_ do what you tell it to do.
Turns the guidance from the prompts (see [agent prompts](./prompts/agent_prompt_generators.py) and [goal prompts](./tools/goal_registry.py)) into 
You have a choice of providers - see [setup](./setup.md). 
The LLM:
- Drives toward the initial Goal and any subsequent Goals selected by user
- Decides what to do based on input, such as:
    - Validates user input for Tools
    - Decides when to execute Tools
    - Decides on next step for Goal
- Formats input and interprets output for Tools
- is executed by Temporal Activities
    - API failures and logical failures are handled transparently

## Interaction
Interaction is managed with Temporal Signals and Queries. These are durably stored in Workflow History. 
History can be used for analysis and debugging. It's all “just code” so it's easy to add new Signals and Queries. 
Input can be very dynamic, just needs to be serializable.

The Workflow executes the Interaction Loop: gathering input, validating input, and providing a response:

![Interaction Loop](./assets/interaction_loop.png)

Here's a more detailed example for gathering inputs for Tools:

![Tool Gathering](./assets/argument_gathering_cycle.png)

# Architecture Model
Now that we have the pieces and what they do, here is a more complete diagram of how the pieces work together: 


![Architecture](./assets/ai_agent_architecture_model.png "Architecture Model")


# Adding features
Want to add more Goals and Tools? See [adding goals and tools](./adding-goals-and-tools.md). Have fun!


================================================
FILE: docs/changelog.md
================================================
# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-04-24

![0.2.0 Changes Screenshot](./assets/0.2.0_changes.jpeg)

### Added
- **Multi‑goal agent architecture** with dynamic goal switching (`goal_choose_agent_type`, `ListAgents`, `ChangeGoal`).
    - See [the architecture guide](./architecture.md) and [setup guide](./setup.md).
- **New goal categories & agents**: HR PTO scheduling/checking, paycheck integration, Financial (balances, money movement, loan application), E‑commerce order tracking.
    - See [the guide for adding goals and tools](./adding-goals-and-tools.md).
- **Force Confirmation**: `SHOW_CONFIRM` will show a confirmation box before allowing the agent to run a tool.
- **Grok (`x.ai`) LLM provider** support via `GROK_API_KEY`.
- Extensive **docs**: `setup.md`, `architecture.md`, `architecture-decisions.md`, `adding-goals-and-tools.md`, plus new diagrams & assets.

### Changed
- **UI Confirmation Box** is less 'debug' looking and prettier.
- Package renamed to **`temporal_AI_agent`** and version bumped to **0.2.0** in `pyproject.toml`.
- Environment variables changed (see `.env_example`): (`RAPIDAPI_HOST_*`, `AGENT_GOAL` defaults, `GOAL_CATEGORIES`, `SHOW_CONFIRM`, `FIN_START_REAL_WORKFLOW`).

## [0.1.0] - 2025-01-04

### Added
- **Initial release** of the Temporal AI Agent demo.
- **Single goal agent** architecture with a single goal and agent type.
    - This is the agent demoed in the [YouTube video](https://www.youtube.com/watch?v=GEXllEH2XiQ).

[0.2.0]: https://github.com/temporal-community/temporal-ai-agent/pull/29


================================================
FILE: docs/contributing.md
================================================
# Contributing to the Temporal AI Agent Project

This document provides guidelines for contributing to `temporal-ai-agent`. All setup and installation instructions can be found in [setup.md](./setup.md).

## Getting Started

### Code Style & Formatting
We use `black` for code formatting and `isort` for import sorting to maintain a consistent codebase.
-   **Format code:**
    ```bash
    uv run poe format
    ```
    Or manually
    ```
    uv run black .
    uv run isort .
    ```
    Please format your code before committing.

### Linting & Type Checking
We use `mypy` for static type checking and other linters configured via `poe`.
-   **Run linters and type checks:**
    ```bash
    uv run poe lint
    ```
    Or manually for type checking:
    ```bash
    uv run mypy --check-untyped-defs --namespace-packages .
    ```
    Ensure all linting and type checks pass before submitting a pull request.

## Testing
Comprehensive testing is crucial for this project. We use `pytest` and Temporal's testing framework.
-   **Install test dependencies:**
    ```bash
    uv sync
    ```
-   **Run all tests:**
    ```bash
    uv run pytest
    ```
-   **Run tests with time-skipping (recommended for faster execution, especially in CI):**
    ```bash
    uv run pytest --workflow-environment=time-skipping
    ```

For detailed information on test categories, running specific tests, test environments, coverage, and troubleshooting, please refer to:
-   [testing.md](./testing.md) (Quick Start and overview)
-   [tests/README.md](../tests/README.md) (Comprehensive guide, patterns, and best practices)

**Ensure all tests pass before submitting a pull request.**

## Making Changes

### Adding New Tools or Goals
If you're looking to extend the agent's capabilities:
1.  Create your tool implementation in the `tools/` directory.
2.  Register your tool and associate it with relevant goals.
For detailed instructions, please see:
-   [Agent Customization in AGENTS.md](../AGENTS.md#agent-customization)
-   [Adding Goals and Tools Guide](./adding-goals-and-tools.md)

### General Code Changes
-   Follow the existing code style and patterns.
-   Ensure any new code is well-documented with comments.
-   Write new tests for new functionality or bug fixes.
-   Update existing tests if necessary.

## Submitting Contributions

### Pull Requests
When you're ready to submit your changes:
1.  Push your branch to the remote repository.
2.  Open a Pull Request (PR) against the `main` branch.
3.  **Describe your changes:** Clearly explain what you changed and why. Reference any related issues.
4.  **Ensure tests pass:** All CI checks, including tests and linters, must pass. The command `uv run pytest --workflow-environment=time-skipping` is a good one to run locally.
5.  **Request review:** Request a review from one or more maintainers.

## Reporting Bugs
If you encounter a bug, please:
1.  **Search existing issues:** Check if the bug has already been reported.
2.  **Open a new issue:** If not, create a new issue.
    -   Provide a clear and descriptive title.
    -   Include steps to reproduce the bug.
    -   Describe the expected behavior and what actually happened.
    -   Provide details about your environment (OS, Python version, Temporal server version, etc.).
    -   Include any relevant logs or screenshots.

## Suggesting Enhancements
We welcome suggestions for new features or improvements!
1.  **Search existing issues/discussions:** See if your idea has already been discussed.
2.  **Open a new issue:**
    -   Use a clear and descriptive title.
    -   Provide a detailed explanation of the enhancement and its benefits.
    -   Explain the use case or problem it solves.
    -   Include any potential implementation ideas if you have them.

## Key Resources
-   **Project Overview**: [README.md](../README.md)
-   **Detailed Contribution & Development Guide**: [AGENTS.md](../AGENTS.md)
-   **Setup Instructions**: [setup.md](./setup.md)
-   **Comprehensive Testing Guide**: [testing.md](./testing.md) and [tests/README.md](../tests/README.md)
-   **System Architecture**: [architecture.md](./architecture.md)
-   **Architecture Decisions**: [architecture-decisions.md](./architecture-decisions.md)
-   **Customizing Agent Tools and Goals**: [adding-goals-and-tools.md](./adding-goals-and-tools.md)
-   **To-Do List / Future Enhancements**: [todo.md](./todo.md)


================================================
FILE: docs/setup.md
================================================
# Setup Guide
## Initial Configuration

This application uses `.env` files for configuration. Copy the [.env.example](.env.example) file to `.env` and update the values:

```bash
cp .env.example .env
```

Then add API keys, configuration, as desired.

If you want to show confirmations/enable the debugging UI that shows tool args, set
```bash
SHOW_CONFIRM=True
```
We recommend setting this to `False` in most cases, as it can clutter the conversation with confirmation messages.

### Quick Start with Makefile

We've provided a Makefile to simplify the setup and running of the application. Here are the main commands:

```bash
# Initial setup
make setup              # Creates virtual environment and installs dependencies

# Running the application
make run-worker         # Starts the Temporal worker
make run-api            # Starts the API server
make run-frontend       # Starts the frontend development server

# Additional services
make run-train-api      # Starts the train API server
make run-legacy-worker  # Starts the legacy worker
make run-enterprise     # Builds and runs the enterprise .NET worker

# Development environment setup
make setup-temporal-mac # Installs and starts Temporal server on Mac

# View all available commands
make help
```

### Manual Setup (Alternative to Makefile)

If you prefer to run commands manually, see the sections below for detailed instructions on setting up the backend, frontend, and other components.

### Agent Goal Configuration

The agent can be configured to pursue different goals using the `AGENT_GOAL` environment variable in your `.env` file. 

**Single Agent Mode (Default)**
By default, the agent operates in single-agent mode using a specific goal. If unset, the default is `goal_event_flight_invoice`.

To set a specific single goal:
```bash
AGENT_GOAL=goal_event_flight_invoice
```

**Multi-Agent Mode (Experimental)**
The agent also supports an experimental multi-agent mode where users can choose between different agent types during the conversation. To enable this mode:

```bash
AGENT_GOAL=goal_choose_agent_type
```

When using multi-agent mode, you can control which agent categories are available using `GOAL_CATEGORIES` in your `.env` file. If unset, all categories are shown. Available categories include `hr`, `travel-flights`, `travel-trains`, `fin`, `ecommerce`, `mcp-integrations`, and `food`.
We recommend starting with `fin`:
```bash
GOAL_CATEGORIES=hr,travel-flights,travel-trains,fin
```

**Note:** Multi-agent mode is experimental and allows switching between different agents mid-conversation, but single-agent mode provides a more focused experience.

MCP (Model Context Protocol) tools are available for enhanced integration with external services. See the [MCP Tools Configuration](#mcp-tools-configuration) section for setup details.

See the section Goal-Specific Tool Configuration below for tool configuration for specific goals.

### LLM Configuration

Note: We recommend using OpenAI's GPT-4o or Claude 3.5 Sonnet for the best results. There can be significant differences in performance and capabilities between models, especially for complex tasks.

The agent uses LiteLLM to interact with various LLM providers. Configure the following environment variables in your `.env` file:

- `LLM_MODEL`: The model to use (e.g., "openai/gpt-4o", "anthropic/claude-3-sonnet", "google/gemini-pro", etc.)
- `LLM_KEY`: Your API key for the selected provider
- `LLM_BASE_URL`: (Optional) Custom base URL for the LLM provider. Useful for:
  - Using Ollama with a custom endpoint
  - Using a proxy or custom API gateway
  - Testing with different API versions

LiteLLM will automatically detect the provider based on the model name. For example:
- For OpenAI models: `openai/gpt-4o` or `openai/gpt-3.5-turbo`
- For Anthropic models: `anthropic/claude-3-sonnet`
- For Google models: `google/gemini-pro`
- For Ollama models: `ollama/mistral` (requires `LLM_BASE_URL` set to your Ollama server)

Example configurations:
```bash
# For OpenAI
LLM_MODEL=openai/gpt-4o
LLM_KEY=your-api-key-here

# For Anthropic
LLM_MODEL=anthropic/claude-3-sonnet
LLM_KEY=your-api-key-here

# For Ollama with custom URL
LLM_MODEL=ollama/mistral
LLM_BASE_URL=http://localhost:11434
```

For a complete list of supported models and providers, visit the [LiteLLM documentation](https://docs.litellm.ai/docs/providers).

## Configuring Temporal Connection

By default, this application will connect to a local Temporal server (`localhost:7233`) in the default namespace, using the `agent-task-queue` task queue. You can override these settings in your `.env` file.

### Use Temporal Cloud

See [.env.example](.env.example) for details on connecting to Temporal Cloud using mTLS or API key authentication.

[Sign up for Temporal Cloud](https://temporal.io/get-cloud)

### Use a local Temporal Dev Server

On a Mac
```bash
brew install temporal
temporal server start-dev
```
See the [Temporal documentation](https://learn.temporal.io/getting_started/python/dev_environment/) for other platforms.

You can also run a local Temporal server using Docker Compose. See the `Development with Docker` section below.

## Running the Application

### Docker
- All services are defined in `docker-compose.yml` (includes a Temporal server).
- **Dev overrides** (mounted code, live‑reload commands) live in `docker-compose.override.yml` and are **auto‑merged** on `docker compose up`.
- To start **development** mode (with hot‑reload):
  ```bash
  docker compose up -d
  # quick rebuild without infra:
  docker compose up -d --no-deps --build api train-api worker frontend
  ```
- To run **production** mode (ignore dev overrides):
  ```bash
  docker compose -f docker-compose.yml up -d
  ```

Default urls:
* Temporal UI: [http://localhost:8080](http://localhost:8080)
* API: [http://localhost:8000](http://localhost:8000)
* Frontend: [http://localhost:5173](http://localhost:5173)

### Local Machine (no docker)

**Python Backend**

Requires [`uv`](https://docs.astral.sh/uv/) to manage dependencies.

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. `uv sync`

Run the following commands in separate terminal windows:

1. Start the Temporal worker:
```bash
uv run scripts/run_worker.py
```

2. Start the API server:
```bash
uv run uvicorn api.main:app --reload
```
Access the API at `/docs` to see the available endpoints.

**React UI**
Start the frontend:
```bash
cd frontend
npm install
npx vite
```
Access the UI at `http://localhost:5173`


## MCP Tools Configuration

MCP (Model Context Protocol) tools enable integration with external services without custom implementation. The system automatically handles MCP server lifecycle and tool discovery.

### Adding MCP Tools to Goals
Configure MCP servers in your goal definitions using either:
1. Predefined configurations from `shared/mcp_config.py`
2. Custom `MCPServerDefinition` objects

Example using Stripe MCP Server:
```python
from shared.mcp_config import get_stripe_mcp_server_definition

mcp_server_definition=get_stripe_mcp_server_definition(
    included_tools=["list_products", "create_customer", "create_invoice"]
)
```

See the file `goals/stripe_mcp.py` for an example of how to use MCP tools in a an `AgentGoal`.

### MCP Environment Variables
Set required API keys and configuration in your `.env` file:
```bash
# For Stripe MCP Server
STRIPE_API_KEY=sk_test_your_stripe_key_here
```
`goal_event_flight_invoice` does not require a Stripe key. If `STRIPE_API_KEY` is unset, that scenario falls back to a mock invoice.

#### Accessing Your Test API Keys
It's free to sign up for a Stripe account and generate test keys (no real money is involved). Use the Developers Dashboard to create, reveal, delete, and rotate API keys. Navigate to the API Keys tab in your dashboard or visit [https://dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys) directly.

For detailed guidance on adding MCP tools, see [adding-goals-and-tools.md](./adding-goals-and-tools.md).

## Goal-Specific Tool Configuration
Here is configuration guidance for specific goals. Travel and financial goals have configuration & setup as below.
### Goal: Find an event in Australia / New Zealand, book flights to it and invoice the user for the cost
- `AGENT_GOAL=goal_event_flight_invoice` - Helps users find events, book flights, and arrange train travel with invoice generation
    - This is the scenario in the [original video](https://www.youtube.com/watch?v=GEXllEH2XiQ)

#### Configuring Agent Goal: goal_event_flight_invoice
* The agent uses a mock function to search for events. This has zero configuration.
* **Flight Search**: The agent intelligently handles flight searches:
    * **Default behavior**: If no `RAPIDAPI_KEY` is set, the agent generates realistic flight data with smart pricing based on route type (domestic, international, trans-Pacific)
    * **Real API (optional)**: To use live flight data, set `RAPIDAPI_KEY` in your `.env` file
        * It's free to sign up at [RapidAPI](https://rapidapi.com/apiheya/api/sky-scrapper)
        * This API might be slow to respond, so you may want to increase the start to close timeout, `TOOL_ACTIVITY_START_TO_CLOSE_TIMEOUT` in `workflows/workflow_helpers.py`
    * The smart generation creates realistic pricing (e.g., US-Australia routes $1200-1800, domestic flights $200-800) with appropriate airlines for each region
* Requires a Stripe key for the `create_invoice` tool. Set this in the `STRIPE_API_KEY` environment variable in `.env`
* It's free to sign up and get a key at [Stripe](https://stripe.com/) (test mode only, no real money)
        * Set permissions for read-write on: `Credit Notes, Invoices, Customers and Customer Sessions`
* If you don't have a Stripe key, comment out the `STRIPE_API_KEY` in the `.env` file, and a dummy invoice will be created rather than a Stripe invoice. The function can be found in `tools/create_invoice.py` – this is the default behavior for `goal_event_flight_invoice`.

### Goal: Find a Premier League match, book train tickets to it and invoice the user for the cost (Replay 2025 Keynote)
- `AGENT_GOAL=goal_match_train_invoice` - Focuses on Premier League match attendance with train booking and invoice generation
    - This goal was part of [Temporal's Replay 2025 conference keynote demo](https://www.youtube.com/watch?v=YDxAWrIBQNE)
    - Note, there is failure built in to this demo (the train booking step) to show how the agent can handle failures and retry. See Tool Configuration below for details.
#### Configuring Agent Goal: goal_match_train_invoice
NOTE: This goal was developed for an on-stage demo and has failure (and its resolution) built in to show how the agent can handle failures and retry.
* Omit `FOOTBALL_DATA_API_KEY` from .env for the `SearchFixtures` tool to automatically return mock Premier League fixtures. Finding a real match requires a key from [Football Data](https://www.football-data.org). Sign up for a free account, then see the 'My Account' page to get your API token.
* We use a mock function to search for trains. Start the train API server to use the real API: `python thirdparty/train_api.py`
* * The train activity is 'enterprise' so it's written in C# and requires a .NET runtime. See the [.NET backend](#net-(enterprise)-backend) section for details on running it.
* Requires a Stripe key for the `create_invoice` tool. Set this in the `STRIPE_API_KEY` environment variable in `.env`
    * It's free to sign up and get a key at [Stripe](https://stripe.com/) (test mode only)
    * If the key is missing this goal won't generate a real invoice – only `goal_event_flight_invoice` falls back to a mock invoice
    * If you're lazy go to `tools/create_invoice.py` and replace the `create_invoice` function with the mock `create_invoice_example` that exists in the same file.

##### Python Search Trains API
> Agent Goal: goal_match_train_invoice only

Required to search and book trains!
```bash
uv run thirdparty/train_api.py

# example url
# http://localhost:8080/api/search?from=london&to=liverpool&outbound_time=2025-04-18T09:00:00&inbound_time=2025-04-20T09:00:00
```

 ##### Python Train Legacy Worker
 > Agent Goal: goal_match_train_invoice only

 These are Python activities that fail (raise NotImplemented) to show how Temporal handles a failure. You can run these activities with.

 ```bash
 uv run scripts/run_legacy_worker.py
 ```

 The activity will fail and be retried infinitely. To rescue the activity (and its corresponding workflows), kill the worker and run the .NET one in the section below.

 ##### .NET (enterprise) Worker ;)
We have activities written in C# to call the train APIs.
```bash
cd enterprise
dotnet build # ensure you brew install dotnet@8 first!
dotnet run
```
If you're running your train API above on a different host/port then change the API URL in `Program.cs`. Otherwise, be sure to run it using `python thirdparty/train_api.py`.

#### Goals: FIN - Money Movement and Loan Application
Make sure you have the mock users you want (such as yourself) in [the account mock data file](./tools/data/customer_account_data.json).

- `AGENT_GOAL=goal_fin_move_money` - This scenario _can_ initiate a secondary workflow to move money. Check out [this repo](https://github.com/temporal-sa/temporal-money-transfer-java) - you'll need to get the worker running and connected to the same account as the agentic worker.
By default it will _not_ make a real workflow, it'll just fake it. If you get the worker running and want to start a workflow, in your [.env](./.env):
```bash
FIN_START_REAL_WORKFLOW=FALSE #set this to true to start a real workflow
```
- `AGENT_GOAL=goal_fin_loan_application` - This scenario _can_ initiate a secondary workflow to apply for a loan. Check out [this repo](https://github.com/temporal-sa/temporal-latency-optimization-scenarios) - you'll need to get the worker running and connected to the same account as the agentic worker.
By default it will _not_ make a real workflow, it'll just fake it. If you get the worker running and want to start a workflow, in your [.env](./.env):
```bash
FIN_START_REAL_WORKFLOW=FALSE #set this to true to start a real workflow
```

#### Goals: HR/PTO
Make sure you have the mock users you want in (such as yourself) in [the PTO mock data file](./tools/data/employee_pto_data.json).

#### Goals: Ecommerce
Make sure you have the mock orders you want in (such as those with real tracking numbers) in [the mock orders file](./tools/data/customer_order_data.json).

### Goal: Food Ordering with MCP Integration (Stripe Payment Processing)
- `AGENT_GOAL=goal_food_ordering` - Demonstrates food ordering with Stripe payment processing via MCP
    - Uses Stripe's MCP Server ([Agent Toolkit](https://github.com/stripe/agent-toolkit/tree/main/modelcontextprotocol)) for payment operations
    - Requires `STRIPE_API_KEY` in your `.env` file
    - Requires products in Stripe with metadata key `use_case=food_ordering_demo`. Run `tools/food/setup/create_stripe_products.py` to set up pizza menu items
    - Example of MCP tool integration without custom implementation
    - This is an excellent demonstration of MCP (Model Context Protocol) capabilities


## Customizing the Agent Further
- `tool_registry.py` contains the mapping of tool names to tool definitions (so the AI understands how to use them)
- `goals/` contains descriptions of goals and the tools used to achieve them
- The tools themselves are defined in their own files in `/tools`

For more details, check out [adding goals and tools guide](./adding-goals-and-tools.md).

## Setup Checklist
[  ] copy `.env.example` to `.env` <br />
[  ] Select an LLM and add your API key to `.env` <br />
[  ] (Optional) set your starting goal and goal category in  `.env` <br />
[  ] (Optional) configure your Temporal Cloud settings in  `.env` <br />
[  ] `uv run scripts/run_worker.py` <br />
[  ] `uv run uvicorn api.main:app --reload` <br />
[  ] `cd frontend`, `npm install`, `npx vite` <br />
[ ] Access the UI at `http://localhost:5173` <br />

And that's it! Happy AI Agent Exploring!



================================================
FILE: docs/testing.md
================================================
# Testing the Temporal AI Agent

This guide provides instructions for running the comprehensive test suite for the Temporal AI Agent project.

## Quick Start

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run all tests**:
   ```bash
   uv run pytest
   ```

3. **Run with time-skipping for faster execution**:
   ```bash
   uv run pytest --workflow-environment=time-skipping
   ```

## Test Categories

### Unit Tests
- **Activity Tests**: `tests/test_tool_activities.py`
  - LLM integration (mocked)
  - Environment configuration
  - JSON processing
  - Dynamic tool execution

### Integration Tests  
- **Workflow Tests**: `tests/test_agent_goal_workflow.py`
  - Full workflow execution
  - Signal and query handling
  - State management
  - Error scenarios

## Running Specific Tests

```bash
# Run only activity tests
uv run pytest tests/test_tool_activities.py -v

# Run only workflow tests  
uv run pytest tests/test_agent_goal_workflow.py -v

# Run a specific test
uv run pytest tests/test_tool_activities.py::TestToolActivities::test_sanitize_json_response -v

# Run tests matching a pattern
uv run pytest -k "validation" -v
```

## Test Environment Options

### Local Environment (Default)
```bash
uv run pytest --workflow-environment=local
```

### Time-Skipping Environment (Recommended for CI)
```bash
uv run pytest --workflow-environment=time-skipping
```

### External Temporal Server
```bash
uv run pytest --workflow-environment=localhost:7233
```

## Environment Variables

Tests can be configured with these environment variables:

- `LLM_MODEL`: Model for LLM testing (default: "openai/gpt-4")
- `LLM_KEY`: API key for LLM service (mocked in tests)
- `LLM_BASE_URL`: Custom LLM endpoint (optional)

## Test Coverage

The test suite covers:

✅ **Workflows**
- AgentGoalWorkflow initialization and execution
- Signal handling (user_prompt, confirm, end_chat)
- Query methods (conversation history, agent goal, tool data)
- State management and conversation flow
- Validation and error handling

✅ **Activities**  
- ToolActivities class methods
- LLM integration (mocked)
- Environment variable handling
- JSON response processing
- Dynamic tool activity execution

✅ **Integration**
- End-to-end workflow execution
- Activity registration in workers
- Temporal client interactions

## Test Output

Successful test run example:
```
============================== test session starts ==============================
platform darwin -- Python 3.11.3, pytest-8.3.5, pluggy-1.5.0
rootdir: /Users/steveandroulakis/Documents/Code/agentic/temporal-demo/temporal-ai-agent
configfile: pyproject.toml
plugins: anyio-4.5.2, asyncio-0.26.0
collected 21 items

tests/test_tool_activities.py::TestToolActivities::test_sanitize_json_response PASSED
tests/test_tool_activities.py::TestToolActivities::test_parse_json_response_success PASSED
tests/test_tool_activities.py::TestToolActivities::test_get_wf_env_vars_default_values PASSED
...

============================== 21 passed in 12.5s ==============================
```

## Troubleshooting

### Common Issues

1. **Module not found errors**: Run `uv sync`
2. **Async warnings**: These are expected with pytest-asyncio and can be ignored  
3. **Test timeouts**: Use `--workflow-environment=time-skipping` for faster execution
4. **Import errors**: Check that you're running tests from the project root directory

### Debugging Tests

Enable verbose logging:
```bash
uv run pytest --log-cli-level=DEBUG -s
```

Run with coverage:
```bash
uv run pytest --cov=workflows --cov=activities
```

## Continuous Integration

For CI environments, use:
```bash
uv run pytest --workflow-environment=time-skipping --tb=short
```

## Additional Resources

- See `tests/README.md` for detailed testing documentation
- Review `tests/conftest.py` for available test fixtures
- Check individual test files for specific test scenarios

## Test Architecture

The tests use:
- **Temporal Testing Framework**: For workflow and activity testing
- **pytest-asyncio**: For async test support  
- **unittest.mock**: For mocking external dependencies
- **Test Fixtures**: For consistent test data and setup

All external dependencies (LLM calls, file I/O) are mocked to ensure fast, reliable tests.


================================================
FILE: docs/todo.md
================================================
# todo list

## General Agent Enhancements

[ ] Google's A2A is emerging as the standard way to hand off agents to other agents. We should examine implementing this soon.

[ ] Custom metrics/tracing is important for AI specific aspects such as number of LLM calls, number of bad LLM responses that require retrying, number of bad chat outcomes. We should add this.

[ ] Evals are very important in agents. We want to be able to 'judge' the agent's performance both in dev and production (AIOps). This will help us improve our agent's performance over time in a targeted fashion.

[ ] Dynamically switch LLMs on persistent failures: <br />
    - detect failure in the activity using failurecount <br />
    - activity switches to secondary LLM defined in .env
    - activity reports switch to workflow

[ ] Collapse history/summarize chat after goal finished <br />

[ ] Write tests<br />

[ ] non-retry the api key error - "Invalid API Key provided: sk_test_**J..." and "AuthenticationError" <br />

[ ] add visual feedback when workflow starting <br />

[ ] enable user to list agents at any time - like end conversation - probably with a next step<br />

[ ] get this on the Model Context Protocol site's list of MCP clients https://modelcontextprotocol.io/clients

## Ideas for more goals and tools

[ ] Add fintech goals <br />
- Fraud Detection and Prevention - The AI monitors transactions across accounts, flagging suspicious activities (e.g., unusual spending patterns or login attempts) and autonomously freezing accounts or notifying customers and compliance teams.<br />
- Personalized Financial Advice - An AI agent analyzes a customer’s financial data (e.g., income, spending habits, savings, investments) and provides tailored advice, such as budgeting tips, investment options, or debt repayment strategies.<br />
- Portfolio Management and Rebalancing - The AI monitors a customer’s investment portfolio, rebalancing it automatically based on market trends, risk tolerance, and financial goals (e.g., shifting assets between stocks, bonds, or crypto).<br />

[ ] new loan/fraud check/update with start <br />
[ ] financial advise - args being freeform customer input about their financial situation, goals
    [ ] tool is maybe a new tool asking the LLM to advise

[ ] for demo simulate failure  - add utilities/simulated failures from pipeline demo <br />



================================================
FILE: enterprise/Program.cs
================================================
using Microsoft.Extensions.DependencyInjection;
using Temporalio.Client;
using Temporalio.Worker;
using TrainSearchWorker.Activities;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Console;

// Set up dependency injection
var services = new ServiceCollection();

var loggerFactory = LoggerFactory.Create(builder =>
{
    builder
        .AddSimpleConsole(options => options.TimestampFormat = "[HH:mm:ss] ")
        .SetMinimumLevel(LogLevel.Information);
});

// Add HTTP client
services.AddHttpClient("TrainApi", client =>
{
    client.BaseAddress = new Uri("http://localhost:8080/");
    client.DefaultRequestHeaders.Add("Accept", "application/json");
});

// Add activities
services.AddScoped<TrainActivities>();

var serviceProvider = services.BuildServiceProvider();

// Create client using the helper, which supports Temporal Cloud if environment variables are set
var client = await TemporalClientHelper.CreateClientAsync();

// Read connection details from environment or use defaults
var address = Environment.GetEnvironmentVariable("TEMPORAL_ADDRESS") ?? "localhost:7233";
var ns = Environment.GetEnvironmentVariable("TEMPORAL_NAMESPACE") ?? "default";

// Log connection details
Console.WriteLine("Starting worker...");
Console.WriteLine($"Connecting to Temporal at address: {address}");
Console.WriteLine($"Using namespace: {ns}");

// Create worker options
var options = new TemporalWorkerOptions("agent-task-queue-legacy")
{
    LoggerFactory = loggerFactory
};

// Register activities
var activities = serviceProvider.GetRequiredService<TrainActivities>();
options.AddActivity(activities.SearchTrains);
options.AddActivity(activities.BookTrains);

// Create and run worker
var worker = new TemporalWorker(client, options);

using var tokenSource = new CancellationTokenSource();
Console.CancelKeyPress += (_, eventArgs) =>
{
    eventArgs.Cancel = true;
    tokenSource.Cancel();
};

try 
{
    await worker.ExecuteAsync(tokenSource.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Worker shutting down...");
}



================================================
FILE: enterprise/TemporalClientHelper.cs
================================================
using System;
using System.IO;
using System.Collections.Generic;
using Temporalio.Client;

public static class TemporalClientHelper
{
    public static async Task<ITemporalClient> CreateClientAsync()
    {
        var address = Environment.GetEnvironmentVariable("TEMPORAL_ADDRESS") ?? "localhost:7233";
        var ns = Environment.GetEnvironmentVariable("TEMPORAL_NAMESPACE") ?? "default";
        var clientCertPath = Environment.GetEnvironmentVariable("TEMPORAL_TLS_CERT");
        var clientKeyPath = Environment.GetEnvironmentVariable("TEMPORAL_TLS_KEY");
        var apiKey = Environment.GetEnvironmentVariable("TEMPORAL_API_KEY");

        var options = new TemporalClientConnectOptions(address)
        {
            Namespace = ns
        };

        if (!string.IsNullOrEmpty(clientCertPath) && !string.IsNullOrEmpty(clientKeyPath))
        {
            // mTLS authentication
            options.Tls = new()
            {
                ClientCert = await File.ReadAllBytesAsync(clientCertPath),
                ClientPrivateKey = await File.ReadAllBytesAsync(clientKeyPath),
            };
        }
        else if (!string.IsNullOrEmpty(apiKey))
        {
            // API Key authentication
            // TODO test
            options.RpcMetadata = new Dictionary<string, string>()
            {
                ["authorization"] = $"Bearer {apiKey}",
                ["temporal-namespace"] = ns
            };
            options.RpcMetadata = new Dictionary<string, string>()
            {
                ["temporal-namespace"] = ns
            };
            options.Tls = new();
        }

        return await TemporalClient.ConnectAsync(options);
    }
}


================================================
FILE: enterprise/TrainSearchWorker.csproj
================================================
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Logging.Console" Version="9.0.4" />
    <PackageReference Include="Temporalio" Version="1.0.0" />
    <PackageReference Include="Microsoft.Extensions.Http" Version="8.0.0" />
  </ItemGroup>
</Project>



================================================
FILE: enterprise/Activities/TrainActivities.cs
================================================
using System.Net.Http.Json;
using System.Text.Json;
using Temporalio.Activities;
using TrainSearchWorker.Models;
using Microsoft.Extensions.Logging;

namespace TrainSearchWorker.Activities;

public class TrainActivities
{
    private readonly HttpClient _client;
    private readonly JsonSerializerOptions _jsonOptions;

    public TrainActivities(IHttpClientFactory clientFactory)
    {
        _client = clientFactory.CreateClient("TrainApi");
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
    }


    [Activity]
    public async Task<JourneyResponse> SearchTrains(SearchTrainsRequest request)
    {
        ActivityExecutionContext.Current.Logger.LogInformation($"SearchTrains from {request.From} to {request.To}");
        var response = await _client.GetAsync(
            $"api/search?from={Uri.EscapeDataString(request.From)}" +
            $"&to={Uri.EscapeDataString(request.To)}" +
            $"&outbound_time={Uri.EscapeDataString(request.OutboundTime)}" +
            $"&return_time={Uri.EscapeDataString(request.ReturnTime)}");

        response.EnsureSuccessStatusCode();
      
        // Deserialize into JourneyResponse rather than List<Journey>
        var journeyResponse = await response.Content.ReadFromJsonAsync<JourneyResponse>(_jsonOptions)
                              ?? throw new InvalidOperationException("Received null response from API");

        ActivityExecutionContext.Current.Logger.LogInformation("SearchTrains completed");

        return journeyResponse;
    }

    [Activity]
    public async Task<BookTrainsResponse> BookTrains(BookTrainsRequest request)
    {
        ActivityExecutionContext.Current.Logger.LogInformation($"Booking trains with IDs: {request.TrainIds}");

        // Build the URL using the train IDs from the request
        var url = $"api/book/{Uri.EscapeDataString(request.TrainIds)}";

        // POST with no JSON body, matching the Python version
        var response = await _client.PostAsync(url, null);
        response.EnsureSuccessStatusCode();

        // Deserialize into a BookTrainsResponse (a single object)
        var bookingResponse = await response.Content.ReadFromJsonAsync<BookTrainsResponse>(_jsonOptions)
                              ?? throw new InvalidOperationException("Received null response from API");

        ActivityExecutionContext.Current.Logger.LogInformation("BookTrains completed");

        return bookingResponse;
    }

}



================================================
FILE: enterprise/Models/BookTrainRequest.cs
================================================
using System.Text.Json.Serialization;

namespace TrainSearchWorker.Models;

public record BookTrainsRequest
{
    [JsonPropertyName("train_ids")]
    public required string TrainIds { get; init; }
}



================================================
FILE: enterprise/Models/BookTrainsResponse.cs
================================================
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace TrainSearchWorker.Models;

public record BookTrainsResponse
{
    [JsonPropertyName("booking_reference")]
    public required string BookingReference { get; init; }
    
    // If the API now returns train_ids as an array, use List<string>
    [JsonPropertyName("train_ids")]
    public required List<string> TrainIds { get; init; }
    
    [JsonPropertyName("status")]
    public required string Status { get; init; }
}



================================================
FILE: enterprise/Models/Journey.cs
================================================
using System.Text.Json.Serialization;

namespace TrainSearchWorker.Models;

public record Journey
{
    [JsonPropertyName("id")]
    public required string Id { get; init; }

    [JsonPropertyName("type")]
    public required string Type { get; init; }

    [JsonPropertyName("departure")]
    public required string Departure { get; init; }

    [JsonPropertyName("arrival")]
    public required string Arrival { get; init; }

    [JsonPropertyName("departure_time")]
    public required string DepartureTime { get; init; }

    [JsonPropertyName("arrival_time")]
    public required string ArrivalTime { get; init; }

    [JsonPropertyName("price")]
    public required decimal Price { get; init; }
}


================================================
FILE: enterprise/Models/JourneyResponse.cs
================================================
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace TrainSearchWorker.Models;

public record JourneyResponse
{
    [JsonPropertyName("journeys")]
    public List<Journey>? Journeys { get; init; }
}



================================================
FILE: enterprise/Models/SearchTrainsRequest.cs
================================================
using System.Text.Json.Serialization;

namespace TrainSearchWorker.Models;

public record SearchTrainsRequest
{
    [JsonPropertyName("origin")]
    public required string From { get; init; }

    [JsonPropertyName("destination")]
    public required string To { get; init; }

    [JsonPropertyName("outbound_time")]
    public required string OutboundTime { get; init; }

    [JsonPropertyName("return_time")]
    public required string ReturnTime { get; init; }
}



================================================
FILE: frontend/index.html
================================================
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Temporal AI Agent</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script type="module" src="/src/main.jsx"></script>
  </head>
  <body class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100">
    <div id="root"></div>
  </body>
</html>



================================================
FILE: frontend/package.json
================================================
{
  "name": "temporal-ai-agent-frontend",
  "version": "1.0.0",
  "description": "React and Tailwind",
  "license": "ISC",
  "author": "",
  "type": "commonjs",
  "main": "index.js",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "vite": "^6.0.7"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.17"
  }
}



================================================
FILE: frontend/postcss.config.js
================================================
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};



================================================
FILE: frontend/tailwind.config.js
================================================
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: "class", // enable dark mode by toggling a .dark class
  theme: {
    extend: {},
  },
  plugins: [],
};


================================================
FILE: frontend/vite.config.js
================================================
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    open: true,
    host: process.env.VITE_HOST ?? 'localhost',
  },
});


================================================
FILE: frontend/src/index.css
================================================
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

*,
html,
body {
    box-sizing: border-box;
}

html {
    height: 100vh;
    width: 100vw;
}

body {
    font-family: Inter, sans-serif;
    position: relative;
    height: 100%;
    width: 100%;
}

h1,
h2,
h3,
h4,
h5,
h6,
titles,
labels {
    font-family: Poppins, sans-serif;
}

/* example if you want it in index.css or a separate .css */
.corner {
    width: 3em;
    height: 3em;
}
.corner a {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}
.corner img {
    width: 2em;
    height: 2em;
    object-fit: contain;
}



================================================
FILE: frontend/src/main.jsx
================================================
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./pages/App";
import "./index.css"; // Tailwind imports

const container = document.getElementById("root");
const root = createRoot(container);

root.render(<App />);



================================================
FILE: frontend/src/components/ChatWindow.jsx
================================================
import React, { memo, useCallback } from "react";
import LLMResponse from "./LLMResponse";
import MessageBubble from "./MessageBubble";
import LoadingIndicator from "./LoadingIndicator";

class ChatErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error("ChatWindow error:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="text-red-500 p-4 text-center">
                    Something went wrong. Please Terminate the workflow and try again.
                </div>
            );
        }
        return this.props.children;
    }
}

const safeParse = (str) => {
    try {
        return typeof str === 'string' ? JSON.parse(str) : str;
    } catch (err) {
        console.error("safeParse error:", err, "Original string:", str);
        return str;
    }
};

const Message = memo(({ msg, idx, isLastMessage, onConfirm, onContentChange }) => {
    const { actor, response } = msg;
    
    if (actor === "user") {
        return <MessageBubble message={{ response }} isUser />;
    }
    
    if (actor === "agent") {
        const data = safeParse(response);
        return (
            <LLMResponse
                data={data}
                onConfirm={onConfirm}
                isLastMessage={isLastMessage}
                onHeightChange={onContentChange}
            />
        );
    }
    
    return null;
});

Message.displayName = 'Message';

const ChatWindow = memo(({ conversation, loading, onConfirm, onContentChange }) => {
    const validateConversation = useCallback((conv) => {
        if (!Array.isArray(conv)) {
            console.error("ChatWindow expected conversation to be an array, got:", conv);
            return [];
        }
        return conv;
    }, []);

    const filtered = validateConversation(conversation).filter((msg) => {
        const { actor } = msg;
        return actor === "user" || actor === "agent";
    });

    return (
        <ChatErrorBoundary>
            <div className="flex-grow flex flex-col">
                <div className="flex-grow flex flex-col justify-end overflow-y-auto space-y-3">
                    {filtered.map((msg, idx) => (
                        <Message
                            key={`${msg.actor}-${idx}-${typeof msg.response === 'string' ? msg.response : msg.response?.response}`}
                            msg={msg}
                            idx={idx}
                            isLastMessage={idx === filtered.length - 1}
                            onConfirm={onConfirm}
                            onContentChange={onContentChange}
                        />
                    ))}
                    {loading && (
                        <div className="pt-2 flex justify-center">
                            <LoadingIndicator />
                        </div>
                    )}
                </div>
            </div>
        </ChatErrorBoundary>
    );
});

ChatWindow.displayName = 'ChatWindow';

export default ChatWindow;



================================================
FILE: frontend/src/components/ConfirmInline.jsx
================================================
import React, { memo, useState } from "react";

/** Inline SVG icons so we don’t need an extra library */
const PlayIcon = ({ className }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    className={className}
    aria-hidden="true"
  >
    <path d="M5 3.868v16.264c0 1.04 1.12 1.675 2.025 1.16l13.11-8.132a1.33 1.33 0 000-2.256L7.025 2.773C6.12 2.259 5 2.894 5 3.934z" />
  </svg>
);

const SpinnerIcon = ({ className }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={`animate-spin ${className}`}
    aria-hidden="true"
  >
    <circle cx="12" cy="12" r="10" strokeOpacity="0.25" />
    <path d="M22 12a10 10 0 00-10-10" />
  </svg>
);

/**
 * User‑friendly confirmation card that surfaces tool invocation details
 * without developer jargon.  Tweaks include:
 *  • Left green accent‑border + compact heading (visual hierarchy)
 *  • Collapsible arg list & array support (argument‑list UX)
 *  • Mobile‑first, pulsing confirm button (button affordance)
 */
const ConfirmInline = memo(({ data, confirmed, onConfirm }) => {
  const { args = {}, tool } = data || {};

  // Collapsible argument list if we have more than 4 root keys
  const [showAll, setShowAll] = useState(false);
  const argEntries = Object.entries(args);
  const shouldCollapse = argEntries.length > 4 && !showAll;

  /** Recursively pretty‑print argument values (objects & arrays). */
  const RenderValue = ({ value }) => {
    if (value === null || value === undefined) return <span className="italic">‑</span>;

    if (Array.isArray(value)) {
      return (
        <ol className="pl-4 list-decimal space-y-0.5">
          {value.map((v, i) => (
            <li key={i} className="flex gap-1">
              <RenderValue value={v} />
            </li>
          ))}
        </ol>
      );
    }

    if (typeof value === "object") {
      return (
        <ul className="pl-4 space-y-0.5 list-disc marker:text-green-500 dark:marker:text-green-400">
          {Object.entries(value).map(([k, v]) => (
            <li key={k} className="flex gap-1">
              <span className="capitalize text-gray-600 dark:text-gray-300">{k}:&nbsp;</span>
              <RenderValue value={v} />
            </li>
          ))}
        </ul>
      );
    }

    return <span className="font-medium text-gray-800 dark:text-gray-100">{String(value)}</span>;
  };

  const cardBase =
    "mt-2 p-3 rounded-lg border-l-4 border-green-500 bg-gray-100/60 dark:bg-gray-800/60 shadow-sm";

  // ===== Running state =====
  if (confirmed) {
    return (
      <div className={`${cardBase} flex items-center gap-3`} role="status">
        <SpinnerIcon className="text-green-600 dark:text-green-400 w-4 h-4" />
        <span className="text-sm text-gray-700 dark:text-gray-200">
          Running <strong className="font-semibold">{tool ?? "Unknown"}</strong> …
        </span>
      </div>
    );
  }

  // ===== Confirmation state =====
  return (
    <div className={`${cardBase} space-y-2`} role="group">
      {/* Heading */}
      <div className="flex items-center gap-2">
        <PlayIcon className="text-green-600 dark:text-green-400 w-5 h-5 shrink-0" />
        <p className="text-sm font-medium text-gray-700 dark:text-gray-200">
          Ready to run <strong>{tool ?? "Unknown"}</strong>
        </p>
      </div>

      {/* Dynamic argument list */}
      {argEntries.length > 0 && (
        <div className="text-sm text-gray-700 dark:text-gray-300">
          {argEntries
            .slice(0, shouldCollapse ? 4 : argEntries.length)
            .map(([k, v]) => (
              <div key={k} className="flex gap-1">
                <span className="capitalize">{k}:&nbsp;</span>
                <RenderValue value={v} />
              </div>
            ))}
          {shouldCollapse && (
            <button
              onClick={() => setShowAll(true)}
              className="mt-1 text-green-600 dark:text-green-400 text-xs underline hover:no-underline"
            >
              …show all
            </button>
          )}
          {showAll && argEntries.length > 4 && (
            <button
              onClick={() => setShowAll(false)}
              className="mt-1 block text-green-600 dark:text-green-400 text-xs underline hover:no-underline"
            >
              show less
            </button>
          )}
        </div>
      )}

      {/* Confirm button */}
      <div className="text-right">
        <button
          onClick={onConfirm}
          onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && onConfirm()}
          className="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white text-sm px-3 py-1.5 rounded-md shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-1 animate-pulse sm:animate-none"
          aria-label={`Confirm running ${tool}`}
        >
          Confirm
        </button>
      </div>
    </div>
  );
});

ConfirmInline.displayName = "ConfirmInline";

export default ConfirmInline;


================================================
FILE: frontend/src/components/LLMResponse.jsx
================================================
import React, { memo, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import ConfirmInline from "./ConfirmInline";

const LLMResponse = memo(({ data, onConfirm, isLastMessage, onHeightChange }) => {
    const [isConfirmed, setIsConfirmed] = React.useState(false);
    const responseRef = React.useRef(null);

    // Notify parent of height changes when confirm UI appears/changes
    useEffect(() => {
        if (isLastMessage && responseRef.current && onHeightChange) {
            onHeightChange();
        }
    }, [isLastMessage, isConfirmed, onHeightChange]);

    const handleConfirm = async () => {
        try {
            if (onConfirm) await onConfirm();
            setIsConfirmed(true);
        } catch (error) {
            console.error('Error confirming action:', error);
        }
    };

    const response = typeof data?.response === 'object' 
        ? data.response.response 
        : data?.response;

    const displayText = (response || '').trim();
    const requiresConfirm = data.force_confirm && data.next === "confirm" && isLastMessage;
    const defaultText = requiresConfirm 
        ? `Agent is ready to run "${data.tool}". Please confirm.` 
        : '';

    return (
        <div ref={responseRef} className="space-y-2" style={{ whiteSpace: 'pre-line' }}>
            <MessageBubble 
                message={{ response: displayText || defaultText }} 
            />
            {requiresConfirm && (
                <ConfirmInline
                    data={data}
                    confirmed={isConfirmed}
                    onConfirm={handleConfirm}
                />
            )}
            {!requiresConfirm && data.tool && data.next === "confirm" && (
                <div className="text-sm text-center text-green-600 dark:text-green-400">
                    <div>
                        Agent chose tool: <strong>{data.tool ?? "Unknown"}</strong>
                    </div>
                </div>
            )}
        </div>
    );
});

LLMResponse.displayName = 'LLMResponse';

export default LLMResponse;



================================================
FILE: frontend/src/components/LoadingIndicator.jsx
================================================
import React, { memo } from "react";

const LoadingIndicator = memo(() => {
    return (
        <div 
            className="flex items-center justify-center space-x-2 pb-4"
            role="status"
            aria-label="Loading"
        >
            {[0, 1, 2].map((i) => (
                <div
                    key={i}
                    className={`w-2 h-2 rounded-full bg-blue-600 animate-ping
                        ${i > 0 ? `delay-${i}00` : ''}`}
                />
            ))}
            <span className="sr-only">Loading...</span>
        </div>
    );
});

LoadingIndicator.displayName = 'LoadingIndicator';

export default LoadingIndicator;



================================================
FILE: frontend/src/components/MessageBubble.jsx
================================================
import React, { memo } from "react";

const MessageBubble = memo(({ message, fallback = "", isUser = false }) => {
    const displayText = message.response?.trim() ? message.response : fallback;

    if (displayText.startsWith("###")) {
        return null;
    }

    const renderTextWithLinks = (text) => {
        // First handle image markdown: ![alt text](url)
        const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        
        // Split by image markdown first
        const imageParts = text.split(imageRegex);
        
        return imageParts.map((part, index) => {
            // Every third element (starting from index 2) is an image URL
            if (index > 0 && (index - 2) % 3 === 0) {
                const altText = imageParts[index - 1];
                const imageUrl = part;
                return (
                    <img
                        key={index}
                        src={imageUrl}
                        alt={altText}
                        className="max-w-full h-auto rounded mt-2 mb-2 mx-auto block border border-gray-300 dark:border-gray-600"
                        style={{ maxHeight: '200px' }}
                        loading="lazy"
                    />
                );
            }
            // Skip alt text parts (every second element after first)
            if (index > 0 && (index - 1) % 3 === 0) {
                return null;
            }
            
            // Handle regular text and links
            const linkParts = part.split(urlRegex);
            return linkParts.map((linkPart, linkIndex) => {
                if (urlRegex.test(linkPart)) {
                    return (
                        <a
                            key={`${index}-${linkIndex}`}
                            href={linkPart}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 hover:text-blue-600 underline"
                            aria-label={`External link to ${linkPart}`}
                        >
                            {linkPart}
                        </a>
                    );
                }
                return linkPart;
            });
        }).filter(Boolean);
    };

    return (
        <div
            className={`
                inline-block px-4 py-2 mb-1 rounded-lg
                ${isUser 
                    ? "ml-auto bg-blue-100 dark:bg-blue-900 dark:text-white" 
                    : "mr-auto bg-gray-200 dark:bg-gray-700 dark:text-white"
                }
                break-words max-w-[75%] transition-colors duration-200
            `}
            role="article"
            aria-label={`${isUser ? 'User' : 'Agent'} message`}
        >
            {renderTextWithLinks(displayText)}
        </div>
    );
});

MessageBubble.displayName = 'MessageBubble';

export default MessageBubble;



================================================
FILE: frontend/src/components/NavBar.jsx
================================================
import React, { memo } from "react";

const NavBar = memo(({ title }) => {
    return (
        <header 
            className="fixed top-0 left-0 w-full p-4 bg-white/70 dark:bg-gray-800/70 
                backdrop-blur-md shadow-md z-10 flex justify-center items-center
                transition-colors duration-200"
            role="banner"
        >
            <h1 className="text-xl font-bold font-poppins">
                {title}
            </h1>
        </header>
    );
});

NavBar.displayName = 'NavBar';

export default NavBar;



================================================
FILE: frontend/src/hooks/useLocalChatHistory.js
================================================
import { useState, useEffect } from "react";

export default function useLocalChatHistory(key, initialValue) {
  const [state, setState] = useState(() => {
    try {
      const stored = window.localStorage.getItem(key);
      return stored ? JSON.parse(stored) : initialValue;
    } catch (err) {
      console.error("Error parsing localStorage:", err);
      return initialValue;
    }
  });

  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(state));
  }, [key, state]);

  return [state, setState];
}



================================================
FILE: frontend/src/pages/App.jsx
================================================
import React, { useEffect, useState, useRef, useCallback } from "react";
import NavBar from "../components/NavBar";
import ChatWindow from "../components/ChatWindow";
import { apiService } from "../services/api";

const POLL_INTERVAL = 600; // 0.6 seconds
const INITIAL_ERROR_STATE = { visible: false, message: '' };
const DEBOUNCE_DELAY = 300; // 300ms debounce for user input

function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);

    return debouncedValue;
}

export default function App() {
    const containerRef = useRef(null);
    const inputRef = useRef(null);
    const pollingRef = useRef(null);
    const scrollTimeoutRef = useRef(null);
    
    const [conversation, setConversation] = useState([]);
    const [lastMessage, setLastMessage] = useState(null);
    const [userInput, setUserInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(INITIAL_ERROR_STATE);
    const [done, setDone] = useState(true);

    const debouncedUserInput = useDebounce(userInput, DEBOUNCE_DELAY);

    const errorTimerRef = useRef(null);

    const handleError = useCallback((error, context) => {
        console.error(`${context}:`, error);
        
        const isConversationFetchError = error.status === 404;
        const errorMessage = isConversationFetchError 
            ? "Error fetching conversation. Retrying..."  // Updated message
            : `Error ${context.toLowerCase()}. Please try again.`;
    
        setError(prevError => {
            // If the same 404 error is already being displayed, don't reset state (prevents flickering)
            if (prevError.visible && prevError.message === errorMessage) {
                return prevError;
            }
            return { visible: true, message: errorMessage };
        });
    
        // Clear any existing timeout
        if (errorTimerRef.current) {
            clearTimeout(errorTimerRef.current);
        }
    
        // Only auto-dismiss non-404 errors after 3 seconds
        if (!isConversationFetchError) {
            errorTimerRef.current = setTimeout(() => setError(INITIAL_ERROR_STATE), 3000);
        }
    }, []);
    
    
    const clearErrorOnSuccess = useCallback(() => {
        if (errorTimerRef.current) {
            clearTimeout(errorTimerRef.current);
        }
        setError(INITIAL_ERROR_STATE);
    }, []);
    
    const fetchConversationHistory = useCallback(async () => {
        try {
            const data = await apiService.getConversationHistory();
            const newConversation = data.messages || [];
            
            setConversation(prevConversation => 
                JSON.stringify(prevConversation) !== JSON.stringify(newConversation) ? newConversation : prevConversation
            );
    
            if (newConversation.length > 0) {
                const lastMsg = newConversation[newConversation.length - 1];
                const isAgentMessage = lastMsg.actor === "agent";
                
                setLoading(!isAgentMessage);
                setDone(lastMsg.response.next === "done");
    
                setLastMessage(prevLastMessage =>
                    !prevLastMessage || lastMsg.response.response !== prevLastMessage.response.response
                        ? lastMsg
                        : prevLastMessage
                );
            } else {
                setLoading(false);
                setDone(true);
                setLastMessage(null);
            }
    
            // Successfully fetched data, clear any persistent errors
            clearErrorOnSuccess();
        } catch (err) {
            handleError(err, "fetching conversation");
        }
    }, [handleError, clearErrorOnSuccess]);
    
    // Setup polling with cleanup
    useEffect(() => {
        pollingRef.current = setInterval(fetchConversationHistory, POLL_INTERVAL);
        
        return () => clearInterval(pollingRef.current);
    }, [fetchConversationHistory]);
    

    const scrollToBottom = useCallback(() => {
        if (containerRef.current) {
            if (scrollTimeoutRef.current) {
                clearTimeout(scrollTimeoutRef.current);
            }
            
            scrollTimeoutRef.current = setTimeout(() => {
                const element = containerRef.current;
                element.scrollTop = element.scrollHeight;
                scrollTimeoutRef.current = null;
            }, 100);
        }
    }, []);

    const handleContentChange = useCallback(() => {
        scrollToBottom();
    }, [scrollToBottom]);

    useEffect(() => {
        if (lastMessage) {
            scrollToBottom();
        }
    }, [lastMessage, scrollToBottom]);

    useEffect(() => {
        if (inputRef.current && !loading && !done) {
            inputRef.current.focus();
        }
        
        return () => {
            if (scrollTimeoutRef.current) {
                clearTimeout(scrollTimeoutRef.current);
            }
        };
    }, [loading, done]);

    const handleSendMessage = async () => {
        const trimmedInput = userInput.trim();
        if (!trimmedInput) return;
        
        try {
            setLoading(true);
            setError(INITIAL_ERROR_STATE);
            await apiService.sendMessage(trimmedInput);
            setUserInput("");
        } catch (err) {
            handleError(err, "sending message");
            setLoading(false);
        }
    };

    const handleConfirm = async () => {
        try {
            setLoading(true);
            setError(INITIAL_ERROR_STATE);
            await apiService.confirm();
        } catch (err) {
            handleError(err, "confirming action");
            setLoading(false);
        }
    };

    const handleStartNewChat = async () => {
        try {
            setError(INITIAL_ERROR_STATE);
            setLoading(true);
            await apiService.startWorkflow();
            setConversation([]);
            setLastMessage(null);
        } catch (err) {
            handleError(err, "starting new chat");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen">
            <NavBar title="Temporal AI Agent 🤖" />

            {error.visible && (
                <div className="fixed top-16 left-1/2 transform -translate-x-1/2 
                    bg-red-500 text-white px-4 py-2 rounded shadow-lg z-50 
                    transition-opacity duration-300">
                    {error.message}
                </div>
            )}

            <div className="flex-grow flex justify-center px-4 py-2 overflow-hidden">
                <div className="w-full max-w-lg bg-white dark:bg-gray-900 p-8 px-3 rounded shadow-md 
                    flex flex-col overflow-hidden">
                    <div ref={containerRef} 
                        className="flex-grow overflow-y-auto pb-20 pt-10 scroll-smooth">
                        <ChatWindow
                            conversation={conversation}
                            loading={loading}
                            onConfirm={handleConfirm}
                            onContentChange={handleContentChange}
                        />
                        {done && (
                            <div className="text-center text-sm text-gray-500 dark:text-gray-400 mt-4 
                                animate-fade-in">
                                Chat ended
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 
                w-full max-w-lg bg-white dark:bg-gray-900 p-4
                border-t border-gray-300 dark:border-gray-700 shadow-lg
                transition-all duration-200"
                style={{ zIndex: 10 }}>
                <form onSubmit={(e) => {
                    e.preventDefault();
                    handleSendMessage();
                }} className="flex items-center">
                    <input
                        ref={inputRef}
                        type="text"
                        className={`flex-grow rounded-l px-3 py-2 border border-gray-300
                            dark:bg-gray-700 dark:border-gray-600 focus:outline-none
                            transition-opacity duration-200
                            ${loading || done ? "opacity-50 cursor-not-allowed" : ""}`}
                        placeholder="Type your message..."
                        value={userInput}
                        onChange={(e) => setUserInput(e.target.value)}
                        disabled={loading || done}
                        aria-label="Type your message"
                    />
                    <button
                        type="submit"
                        className={`bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-r 
                            transition-all duration-200
                            ${loading || done ? "opacity-50 cursor-not-allowed" : ""}`}
                        disabled={loading || done}
                        aria-label="Send message"
                    >
                        Send
                    </button>
                </form>
                
                <div className="text-right mt-3">
                    <button
                        onClick={handleStartNewChat}
                        className={`text-sm underline text-gray-600 dark:text-gray-400 
                            hover:text-gray-800 dark:hover:text-gray-200 
                            transition-all duration-200
                            ${!done ? "opacity-0 cursor-not-allowed" : ""}`}
                        disabled={!done}
                        aria-label="Start new chat"
                    >
                        Start New Chat
                    </button>
                </div>
            </div>
        </div>
    );
}



================================================
FILE: frontend/src/services/api.js
================================================
const API_BASE_URL = 'http://127.0.0.1:8000';

class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
        this.name = 'ApiError';
    }
}

async function handleResponse(response) {
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
            errorData.message || 'An error occurred',
            response.status
        );
    }
    return response.json();
}

export const apiService = {
    async getConversationHistory() {
        try {
            const res = await fetch(`${API_BASE_URL}/get-conversation-history`);
            return handleResponse(res);
        } catch (error) {
            throw new ApiError(
                'Failed to fetch conversation history',
                error.status || 500
            );
        }
    },

    async sendMessage(message) {
        if (!message?.trim()) {
            throw new ApiError('Message cannot be empty', 400);
        }

        try {
            const res = await fetch(
                `${API_BASE_URL}/send-prompt?prompt=${encodeURIComponent(message)}`,
                { 
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            );
            return handleResponse(res);
        } catch (error) {
            throw new ApiError(
                'Failed to send message',
                error.status || 500
            );
        }
    },

    async startWorkflow() {
        try {
            const res = await fetch(
                `${API_BASE_URL}/start-workflow`,
                { 
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            );
            return handleResponse(res);
        } catch (error) {
            throw new ApiError(
                'Failed to start workflow',
                error.status || 500
            );
        }
    },

    async confirm() {
        try {
            const res = await fetch(`${API_BASE_URL}/confirm`, { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            return handleResponse(res);
        } catch (error) {
            throw new ApiError(
                'Failed to confirm action',
                error.status || 500
            );
        }
    }
}; 


================================================
FILE: goals/__init__.py
================================================
import os
from typing import List

import tools.tool_registry as tool_registry
from goals.agent_selection import agent_selection_goals
from goals.ecommerce import ecommerce_goals
from goals.finance import finance_goals
from goals.food import food_goals
from goals.hr import hr_goals
from goals.stripe_mcp import mcp_goals
from goals.travel import travel_goals
from models.tool_definitions import AgentGoal

goal_list: List[AgentGoal] = []
goal_list.extend(agent_selection_goals)
goal_list.extend(travel_goals)
goal_list.extend(hr_goals)
goal_list.extend(finance_goals)
goal_list.extend(ecommerce_goals)
goal_list.extend(mcp_goals)
goal_list.extend(food_goals)

# for multi-goal, just set list agents as the last tool
first_goal_value = os.getenv("AGENT_GOAL")
if first_goal_value is None:
    multi_goal_mode = False  # default to single agent mode if unset
elif (
    first_goal_value is not None
    and first_goal_value.lower() == "goal_choose_agent_type"
):
    multi_goal_mode = True
else:
    multi_goal_mode = False

if multi_goal_mode:
    for goal in goal_list:
        list_agents_found: bool = False
        for tool in goal.tools:
            if tool.name == "ListAgents":
                list_agents_found = True
                continue
        if list_agents_found is False:
            goal.tools.append(tool_registry.list_agents_tool)
            continue



================================================
FILE: goals/agent_selection.py
================================================
from typing import List

import tools.tool_registry as tool_registry
from models.tool_definitions import AgentGoal

# Turn on Silly Mode - this should be a description of the persona you'd like the bot to have and can be a single word or a phrase.
# Example if you want the bot to be a specific person, like Mario or Christopher Walken, or to describe a specific tone:
# SILLY_MODE="Christopher Walken"
# SILLY_MODE="belligerent"
#
# Example if you want it to take on a persona (include 'a'):
# SILLY_MODE="a pirate"
# Note - this only works with certain LLMs. Grok for sure will stay in character, while OpenAI will not.
SILLY_MODE = "off"
if SILLY_MODE is not None and SILLY_MODE != "off":
    silly_prompt = "You are " + SILLY_MODE + ", stay in character at all times. "
    print("Silly mode is on: " + SILLY_MODE)
else:
    silly_prompt = ""

starter_prompt_generic = (
    silly_prompt
    + "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job."
)

goal_choose_agent_type = AgentGoal(
    id="goal_choose_agent_type",
    category_tag="agent_selection",
    agent_name="Choose Agent",
    agent_friendly_description="Choose the type of agent to assist you today. You can always interrupt an existing agent to pick a new one.",
    tools=[
        tool_registry.list_agents_tool,
        tool_registry.change_goal_tool,
    ],
    description="The user wants to choose which type of agent they will interact with. "
    "Help the user select an agent by gathering args for the Changegoal tool, in order: "
    "1. ListAgents: List agents available to interact with. Do not ask for user confirmation for this tool. "
    "2. ChangeGoal: Change goal of agent "
    "After these tools are complete, change your goal to the new goal as chosen by the user. ",
    starter_prompt=silly_prompt
    + "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job. List all details of all agents as provided by the output of the first tool included in this goal. ",
    example_conversation_history="\n ".join(
        [
            "agent: Here are the currently available agents.",
            "tool_result: { agents: 'agent_name': 'Event Flight Finder', 'goal_id': 'goal_event_flight_invoice', 'agent_description': 'Helps users find interesting events and arrange travel to them',"
            "'agent_name': 'Schedule PTO', 'goal_id': 'goal_hr_schedule_pto', 'agent_description': 'Schedule PTO based on your available PTO.' }",
            "agent: The available agents are: Event Flight Finder and Schedule PTO. \n Which agent would you like to work with? ",
            "user: I'd like to find an event and book flights using the Event Flight Finder",
            "user_confirmed_tool_run: <user clicks confirm on ChangeGoal tool>",
            "tool_result: { 'new_goal': 'goal_event_flight_invoice' }",
        ]
    ),
)

# Easter egg - if silly mode = a pirate, include goal_pirate_treasure as a "system" goal so it always shows up.
# Can also turn make this goal available by setting the GOAL_CATEGORIES in the env file to include 'pirate', but if SILLY_MODE
#   is not 'a pirate', the interaction as a whole will be less pirate-y.
pirate_category_tag = "pirate"
if SILLY_MODE == "a pirate":
    pirate_category_tag = "system"
goal_pirate_treasure = AgentGoal(
    id="goal_pirate_treasure",
    category_tag=pirate_category_tag,
    agent_name="Arrr, Find Me Treasure!",
    agent_friendly_description="Sail the high seas and find me pirate treasure, ye land lubber!",
    tools=[
        tool_registry.give_hint_tool,
        tool_registry.guess_location_tool,
    ],
    description="The user wants to find a pirate treasure. "
    "Help the user gather args for these tools, in a loop, until treasure_found is True or the user requests to be done: "
    "1. GiveHint: If the user wants a hint regarding the location of the treasure, give them a hint. If they do not want a hint, this tool is optional."
    "2. GuessLocation: The user guesses where the treasure is, by giving an address. ",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to try to find the treasure",
            "agent: Sure! Do you want a hint?",
            "user: yes",
            "agent: Here is hint number 1!",
            "user_confirmed_tool_run: <user clicks confirm on GiveHint tool>",
            "tool_result: { 'hint_number': 1, 'hint': 'The treasure is in the state of Arizona.' }",
            "agent: The treasure is in the state of Arizona. Would you like to guess the address of the treasure? ",
            "user: Yes, address is 123 Main St Phoenix, AZ",
            "agent: Let's see if you found the treasure...",
            "user_confirmed_tool_run: <user clicks confirm on GuessLocation tool>"
            "tool_result: {'treasure_found':False}",
            "agent: Nope, that's not the right location! Do you want another hint?",
            "user: yes",
            "agent: Here is hint number 2.",
            "user_confirmed_tool_run: <user clicks confirm on GiveHint tool>",
            "tool_result: { 'hint_number': 2, 'hint': 'The treasure is in the city of Tucson, AZ.' }",
            "agent: The treasure is in the city of Tucson, AZ. Would you like to guess the address of the treasure? ",
            "user: Yes, address is 456 Main St Tucson, AZ",
            "agent: Let's see if you found the treasure...",
            "user_confirmed_tool_run: <user clicks confirm on GuessLocation tool>",
            "tool_result: {'treasure_found':True}",
            "agent: Congratulations, Land Lubber, you've found the pirate treasure!",
        ]
    ),
)

agent_selection_goals: List[AgentGoal] = [
    goal_choose_agent_type,
    goal_pirate_treasure,
]



================================================
FILE: goals/ecommerce.py
================================================
from typing import List

import tools.tool_registry as tool_registry
from models.tool_definitions import AgentGoal

starter_prompt_generic = "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job."

goal_ecomm_order_status = AgentGoal(
    id="goal_ecomm_order_status",
    category_tag="ecommerce",
    agent_name="Check Order Status",
    agent_friendly_description="Check the status of your order.",
    tools=[
        tool_registry.ecomm_get_order,
        tool_registry.ecomm_track_package,
    ],
    description="The user wants to learn the status of a specific order. If the status is 'shipped' or 'delivered', they might want to get the package tracking information. To assist with that goal, help the user gather args for these tools in order: "
    "1. GetOrder: get information about an order"
    "2. TrackPackage: provide tracking information for the package. This tool is optional and should only be offered if the status is 'shipped' OR 'delivered' - otherwise, skip this tool and do not mention it to the user.",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to know the status of my order",
            "agent: Sure! I can help you out with that. May I have your order number?",
            "user: 102 ",
            "user_confirmed_tool_run: <user clicks confirm on GetOrderStatus tool>",
            "tool_result: { 'id': '102', 'summary': 'Red Sunglasses', 'email': 'matt.murdock@nelsonmurdock.com', 'status': 'shipped', 'order_date': '2025-04-01', 'last_order_update': '2025-04-06', 'tracking_id': '039813852990618' }",
            "agent: Your order 'Red Sunglasses,' placed April 1, 2025, was shipped on April 6, 2025. Would you like to see the tracking inforation?",
            "user: Yes",
            "user_confirmed_tool_run: <user clicks confirm on TrackPackage tool>",
            "tool_result: { 'scheduled_delivery_date': 'April 30, 2025', 'carrier': 'USPS', 'status_summary': 'Your item has left our acceptance facility and is in transit to a sorting facility on April 10, 2025 at 7:06 am in IRON RIDGE, WI 53035.', 'tracking_link': 'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=12345','last_tracking_update': '2025-03-22T16:14:48'}",
            "agent: Your package is scheduled to be delivered on April 30, 2025 via USPS. Here is the most recent status from them regarding your package, updated as of March 22: \\n"
            "Your item has left our acceptance facility and is in transit to a sorting facility on April 10, 2025 at 7:06 am in IRON RIDGE, WI 53035. \\n"
            "You can find the full tracking details here: tracking_link !",
        ]
    ),
)

goal_ecomm_list_orders = AgentGoal(
    id="goal_ecomm_list_orders",
    category_tag="ecommerce",
    agent_name="List All Orders",
    agent_friendly_description="List all orders for a user.",
    tools=[
        tool_registry.ecomm_list_orders,
        tool_registry.ecomm_get_order,
        tool_registry.ecomm_track_package,
    ],
    description="The user wants to see all of their orders. They may want more details about specific orders, and if the status of an order is 'shipped' or 'delivered', they might want to get the package tracking information. To assist with that goal, help the user gather args for this tool: "
    "1. ListOrders: list orders for a user"
    " and then offer the following tools, in a loop, until the user indicates they are done:"
    "2. GetOrder: get information about an order. This tool is optional."
    "3. TrackPackage: provide tracking information for the package. This tool is optional and should only be offered if the status is 'shipped' OR 'delivered' - otherwise, skip this tool and do not mention it to the user.",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to see all of my orders.",
            "agent: Sure! I can help you out with that. May I have your email address?",
            "user: email is bob.johnson@emailzzz.com ",
            "user_confirmed_tool_run: <user clicks confirm on ListOrders tool>",
            "tool_result: a list of orders including [{'id': '102', 'summary': 'Red Sunglasses', 'email': 'matt.murdock@nelsonmurdock.com', 'status': 'shipped', 'order_date': '2025-04-01', 'last_order_update': '2025-04-06', 'tracking_id': '039813852990618' }, { 'id': '103', 'summary': 'Blue Sunglasses', 'email': 'matt.murdock@nelsonmurdock.com', 'status': 'paid', 'order_date': '2025-04-03', 'last_order_update': '2025-04-07' }]",
            "agent: Your orders are as follows: \\n",
            "1. Red Sunglasses, ordered 4/1/2025 \\n",
            "2. Blue Sunglasses, ordered 4/3/2025 \\n",
            "Would you like more information about any of your orders?"
            "user: Yes, the Red Sunglasses",
            "agent: Your order 'Red Sunglasses,' placed April 1, 2025, was shipped on April 6, 2025. Would you like to see the tracking inforation?",
            "user: Yes",
            "user_confirmed_tool_run: <user clicks confirm on TrackPackage tool>",
            "tool_result: { 'scheduled_delivery_date': 'April 30, 2025', 'carrier': 'USPS', 'status_summary': 'Your item has left our acceptance facility and is in transit to a sorting facility on April 10, 2025 at 7:06 am in IRON RIDGE, WI 53035.', 'tracking_link': 'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=12345','last_tracking_update': '2025-03-22T16:14:48'}",
            "agent: Your package is scheduled to be delivered on April 30, 2025 via USPS. Here is the most recent status from them regarding your package \\n, updated as of March 22: \\n"
            "Your item has left our acceptance facility and is in transit to a sorting facility on April 10, 2025 at 7:06 am in IRON RIDGE, WI 53035. \\n"
            "You can find the full tracking details here: tracking_link ! \\n"
            "Would you like more information about any of your other orders?",
            "user: No" "agent: Thanks, and have a great day!",
        ]
    ),
)

ecommerce_goals: List[AgentGoal] = [
    goal_ecomm_order_status,
    goal_ecomm_list_orders,
]



================================================
FILE: goals/finance.py
================================================
from typing import List

import tools.tool_registry as tool_registry
from models.tool_definitions import AgentGoal

starter_prompt_generic = "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job."

goal_fin_check_account_balances = AgentGoal(
    id="goal_fin_check_account_balances",
    category_tag="fin",
    agent_name="Account Balances",
    agent_friendly_description="Check your account balances in Checking, Savings, etc.",
    tools=[
        tool_registry.financial_check_account_is_valid,
        tool_registry.financial_get_account_balances,
    ],
    description="The user wants to check their account balances at the bank or financial institution. To assist with that goal, help the user gather args for these tools in order: "
    "1. FinCheckAccountIsValid: validate the user's account is valid"
    "2. FinCheckAccountBalance: Tell the user their account balance at the bank or financial institution",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to check my account balances",
            "agent: Sure! I can help you out with that. May I have your email address and account number?",
            "user: email is bob.johnson@emailzzz.com ",
            "user_confirmed_tool_run: <user clicks confirm on FincheckAccountIsValid tool>",
            "tool_result: { 'status': account valid }",
            "agent: Great! I can tell you what the your account balances are.",
            "user_confirmed_tool_run: <user clicks confirm on FinCheckAccountBalance tool>",
            "tool_result: { 'name': Matt Murdock, 'email': matt.murdock@nelsonmurdock.com, 'account_id': 11235, 'checking_balance': 875.40, 'savings_balance': 3200.15, 'bitcoin_balance': 0.1378, 'account_creation_date': 2014-03-10 }",
            "agent: Your account balances are as follows: \\n "
            "Checking: $875.40. \\n "
            "Savings: $3200.15. \\n "
            "Bitcoin: 0.1378 \\n "
            "Thanks for being a customer since 2014!",
        ]
    ),
)

goal_fin_move_money = AgentGoal(
    id="goal_fin_move_money",
    category_tag="fin",
    agent_name="Money Movement",
    agent_friendly_description="Initiate money movement.",
    tools=[
        tool_registry.financial_check_account_is_valid,
        tool_registry.financial_get_account_balances,
        tool_registry.financial_move_money,
    ],
    description="The user wants to transfer money in their account at the bank or financial institution. To assist with that goal, help the user gather args for these tools in order: "
    "1. FinCheckAccountIsValid: validate the user's account is valid"
    "2. FinCheckAccountBalance: Tell the user their account balance at the bank or financial institution"
    "3. FinMoveMoney: Initiate money movement (transfer)",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to transfer some money",
            "agent: Sure! I can help you out with that. May I have account number and email address?",
            "user: my account number is 11235 and my email address is matt.murdock@nelsonmurdock.com",
            "user_confirmed_tool_run: <user clicks confirm on FincheckAccountIsValid tool>",
            "tool_result: { 'status': account valid }",
            "agent: Great! Here are your account balances:",
            "user_confirmed_tool_run: <user clicks confirm on FinCheckAccountBalance tool>",
            "tool_result: { 'name': Matt Murdock, 'email': matt.murdock@nelsonmurdock.com, 'account_id': 11235, 'checking_balance': 875.40, 'savings_balance': 3200.15, 'bitcoin_balance': 0.1378, 'account_creation_date': 2014-03-10 }",
            "agent: Your account balances are as follows: \\n "
            "Checking: $875.40. \\n "
            "Savings: $3200.15. \\n "
            "Bitcoint: 0.1378 \\n "
            "agent: how much would you like to move, from which account type, and to which account number?",
            "user: I'd like to move $500 from savings to account number #56789",
            "user_confirmed_tool_run: <user clicks confirm on FinMoveMoney tool>",
            "tool_result: { 'status': money movement complete, 'confirmation id': 333421, 'new_balance': $2700.15 }",
            "agent: Money movement completed! New account balance: $2700.15. Your confirmation id is 333421. ",
        ]
    ),
)

goal_fin_loan_application = AgentGoal(
    id="goal_fin_loan_application",
    category_tag="fin",
    agent_name="Easy Loan",
    agent_friendly_description="Initiate a simple loan application.",
    tools=[
        tool_registry.financial_check_account_is_valid,
        tool_registry.financial_submit_loan_approval,
    ],
    description="The user wants to apply for a loan at the financial institution. To assist with that goal, help the user gather args for these tools in order: "
    "1. FinCheckAccountIsValid: validate the user's account is valid"
    "2. FinCheckAccountSubmitLoanApproval: submit the loan for approval",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to apply for a loan",
            "agent: Sure! I can help you out with that. May I have account number and email address to validate your account?",
            "user: account number is 11235813",
            "user_confirmed_tool_run: <user clicks confirm on FincheckAccountIsValid tool>",
            "tool_result: { 'status': account valid }",
            "agent: Great! We've validated your account. What will the loan amount be?",
            "user: I'd like a loan for $500",
            "user_confirmed_tool_run: <user clicks confirm on FinCheckAccountSubmitLoanApproval tool>",
            "tool_result: { 'status': submitted, 'detailed_status': loan application is submitted and initial validation is complete, 'confirmation id': 333421, 'next_step': You'll receive a confirmation for final approval in three business days }",
            "agent: I have submitted your loan application process and the initial validation is successful. Your application ID is 333421. You'll receive a notification for final approval from us in three business days. ",
        ]
    ),
)

finance_goals: List[AgentGoal] = [
    goal_fin_check_account_balances,
    goal_fin_move_money,
    goal_fin_loan_application,
]



================================================
FILE: goals/food.py
================================================
from typing import List

import tools.tool_registry as tool_registry
from models.tool_definitions import AgentGoal
from shared.mcp_config import get_stripe_mcp_server_definition

starter_prompt_generic = "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job."

goal_food_ordering = AgentGoal(
    id="goal_food_ordering",
    category_tag="food",
    agent_name="Food Ordering Assistant",
    agent_friendly_description="Order food from Tony's Pizza Palace using Stripe for payment processing. Browse menu, add items to your order, and check out securely. Please ensure context carries over between tool runs.",
    tools=[tool_registry.food_add_to_cart_tool],
    mcp_server_definition=get_stripe_mcp_server_definition(
        included_tools=[
            "list_products",
            "list_prices",
            "create_customer",
            "create_invoice",
            "create_invoice_item",
            "finalize_invoice",
        ]
    ),
    description="The user wants to order food from Tony's Pizza Palace. "
    "First, help the user browse the menu by calling list_products. You can refer to this data throughout the conversation to answer questions (without re-calling this tool). If menu items contain links to images, you can use markdown to display them e.g. ![Pepperoni Pizza](https://...)"
    "When they express interest in items, get pricing using list_prices. "
    "Add items to their cart using AddToCart as they decide - the order doesn't matter, multiple items can be added. "
    "After they're done selecting items, get their customer details and create a Stripe customer. "
    "For checkout: 1) create_invoice, 2) create_invoice_item for each individual item (IMPORTANT: create_invoice_item does NOT accept quantity parameter - call it once per item, so if user wants 2 pizzas, call create_invoice_item twice with the same price), "
    "3) finalize_invoice. The finalized invoice will contain a hosted_invoice_url for payment.",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I want to order food.",
            "agent: Welcome to Tony's Pizza Palace! I can help you browse our menu, add items to your cart, and process payment. Let me show you what we have available.",
            "user_confirmed_tool_run: <user clicks confirm on list_products tool with limit=100 and product.metadata.use_case == 'food_ordering_demo'>",
            'tool_result: {"products": [{"id": "prod_pepperoni", "name": "Pepperoni Pizza", "description": "A timeless classic featuring pepperoni", "images": ["https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfcGRHc0c4cEZYWmR2bm0zOHBOa0FWMk5t008QmCJoWr"]}, {"id": "prod_margherita", "name": "Margherita Pizza", "description": "Fresh mozzarella and basil", "images": ["https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfamdmTXBFbzY0TW9rS2N0c2g0Tml2SERL00Evl60Ttq"]}, {"id": "prod_garlic_bread", "name": "Garlic Bread", "description": "Warm crusty bread with garlic butter", "images": ["https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfWTdIZTBkUjNZNFQ1ZEhSVG9nRnduY1pS00XVgLRRZD"]}, {"id": "prod_soda", "name": "Soda", "description": "A large bottle of cola", "images": ["https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfbDJxckJKMDRnT1dDc243OHlZNWNkZkY5006Xg07kHT"]}]}',
            "agent: Welcome to our menu! Here's what we have available:\\n\\n**Pepperoni Pizza** - A timeless classic featuring pepperoni\\n![Pepperoni Pizza](https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfcGRHc0c4cEZYWmR2bm0zOHBOa0FWMk5t008QmCJoWr)\\n\\n**Margherita Pizza** - Fresh mozzarella and basil\\n![Margherita Pizza](https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfamdmTXBFbzY0TW9rS2N0c2g0Tml2SERL00Evl60Ttq)\\n\\n**Garlic Bread** - Warm crusty bread with garlic butter\\n![Garlic Bread](https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfWTdIZTBkUjNZNFQ1ZEhSVG9nRnduY1pS00XVgLRRZD)\\n\\n**Soda** - A large bottle of cola\\n![Soda](https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfbDJxckJKMDRnT1dDc243OHlZNWNkZkY5006Xg07kHT)\\n\\nWhat would you like to order?",
            "user: I'd like 2 pepperoni pizzas and a soda.",
            "agent: Excellent! Let me get the pricing for the pepperoni pizzas first so you know the cost.",
            "user_confirmed_tool_run: <user clicks confirm on list_prices tool with product='prod_pepperoni'>",
            'tool_result: {"prices": [{"id": "price_pepperoni_large", "product": "prod_pepperoni", "unit_amount": 2299, "currency": "usd"}]}',
            "agent: Pepperoni Pizza is $22.99 each. Now let me check the soda pricing:",
            "user_confirmed_tool_run: <user clicks confirm on list_prices tool with product='prod_soda'>",
            'tool_result: {"prices": [{"id": "price_soda", "product": "prod_soda", "unit_amount": 250, "currency": "usd"}]}',
            "agent: And Soda is $2.50. So 2 Pepperoni Pizzas ($22.99 each) plus 1 Soda ($2.50) = $48.48 total. What's your email address to add these items to your cart?",
            "user: jane.smith@example.com",
            "agent: Perfect! Adding 2 Pepperoni Pizzas to your cart for jane.smith@example.com. Note: I'm using quantity=2 since you want 2 pizzas.",
            "user_confirmed_tool_run: <user clicks confirm on AddToCart tool with customer_email='jane.smith@example.com', item_name='Pepperoni Pizza', item_price=22.99, quantity=2, stripe_product_id='prod_pepperoni'>",
            'tool_result: {"status": "success", "message": "Added 2 x Pepperoni Pizza ($22.99) to cart for jane.smith@example.com", "item_added": {"quantity": 2, "name": "Pepperoni Pizza"}}',
            "agent: Great! Added 2 Pepperoni Pizzas to your cart. Now adding the Soda (quantity=1):",
            "user_confirmed_tool_run: <user clicks confirm on AddToCart tool with customer_email='jane.smith@example.com', item_name='Soda', item_price=2.50, quantity=1, stripe_product_id='prod_soda'>",
            'tool_result: {"status": "success", "message": "Added 1 x Soda ($2.50) to cart for jane.smith@example.com", "item_added": {"quantity": 1, "name": "Soda"}}',
            "agent: Perfect! Added 1 Soda to your cart. Your cart now contains: 2 Pepperoni Pizzas ($22.99 each) and 1 Soda ($2.50). What else would you like to order?",
            "user: Nothing, that's all.",
            "agent: Great! Your order is complete with 2 Pepperoni Pizzas and 1 Soda for a total of $48.48. Now let's proceed to checkout. I'll need your full name to create your customer profile.",
            "user: My name is Jane Smith.",
            "agent: Thank you Jane! Creating your Stripe customer profile with name and email.",
            "user_confirmed_tool_run: <user clicks confirm on create_customer tool with name='Jane Smith' and email='jane.smith@example.com'>",
            'tool_result: {"customer": {"id": "cus_ExAmPlE12345", "name": "Jane Smith", "email": "jane.smith@example.com"}}',
            "agent: Customer profile created! Now I'll create a draft invoice for your order.",
            "user_confirmed_tool_run: <user clicks confirm on create_invoice tool with customer='cus_ExAmPlE12345'>",
            'tool_result: {"invoice": {"id": "in_InvOicE54321", "status": "draft", "customer": "cus_ExAmPlE12345"}}',
            "agent: Invoice created! Now adding your first Pepperoni Pizza to the invoice.",
            "user_confirmed_tool_run: <user clicks confirm on create_invoice_item tool with customer='cus_ExAmPlE12345', invoice='in_InvOicE54321', price='price_pepperoni_large'>",
            'tool_result: {"status": "success", "invoice_item": {"id": "ii_pizza1"}}',
            "agent: First pizza added! Now adding your second Pepperoni Pizza to the invoice.",
            "user_confirmed_tool_run: <user clicks confirm on create_invoice_item tool with customer='cus_ExAmPlE12345', invoice='in_InvOicE54321', price='price_pepperoni_large'>",
            'tool_result: {"status": "success", "invoice_item": {"id": "ii_pizza2"}}',
            "agent: Both pizzas added! Now adding your Soda to the invoice.",
            "user_confirmed_tool_run: <user clicks confirm on create_invoice_item tool with customer='cus_ExAmPlE12345', invoice='in_InvOicE54321', price='price_soda'>",
            'tool_result: {"status": "success", "invoice_item": {"id": "ii_soda"}}',
            "agent: All items added to invoice! Now finalizing to generate the payment link.",
            "user_confirmed_tool_run: <user clicks confirm on finalize_invoice tool with invoice='in_InvOicE54321'>",
            'tool_result: {"invoice": {"id": "in_InvOicE54321", "status": "open", "hosted_invoice_url": "https://invoice.stripe.com/i/acct_1NBOLuKVZbzw7QA5/test_YWNjdF8xTkJPTHVLVlpienc3UUE1LF9SbGJlZ2xLMjhlc3lxNzFkVVBXbkswOUlFa2Rna1RxLDEzMDAwMTY4Nw0200RKeJRMlw?s=ap", "amount_due": 4848}}',
            "agent: Perfect! Your order is complete with 2 Pepperoni Pizzas and 1 Soda. Total: $48.48. Pay securely here: https://invoice.stripe.com/i/acct_1NBOLuKVZbzw7QA5/test_YWNjdF8xTkJPTHVLVlpienc3UUE1LF9SbGJlZ2xLMjhlc3lxNzFkVVBXbkswOUlFa2Rna1RxLDEzMDAwMTY4Nw0200RKeJRMlw?s=ap\\\\n\\\\nThank you for ordering from Tony's Pizza Palace!",
        ]
    ),
)

food_goals: List[AgentGoal] = [
    goal_food_ordering,
]



================================================
FILE: goals/hr.py
================================================
from typing import List

import tools.tool_registry as tool_registry
from models.tool_definitions import AgentGoal

starter_prompt_generic = "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job."

goal_hr_schedule_pto = AgentGoal(
    id="goal_hr_schedule_pto",
    category_tag="hr",
    agent_name="Schedule PTO",
    agent_friendly_description="Schedule PTO based on your available PTO.",
    tools=[
        tool_registry.current_pto_tool,
        tool_registry.future_pto_calc_tool,
        tool_registry.book_pto_tool,
    ],
    description="The user wants to schedule paid time off (PTO) after today's date. To assist with that goal, help the user gather args for these tools in order: "
    "1. CurrentPTO: Tell the user how much PTO they currently have "
    "2. FuturePTOCalc: Tell the user how much PTO they will have as of the prospective future date "
    "3. BookPTO: Book PTO after user types 'yes'",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to schedule some time off",
            "agent: Sure! Let's start by determining how much PTO you currently have. May I have your email address?",
            "user: bob.johnson@emailzzz.com",
            "agent: Great! I can tell you how much PTO you currently have accrued.",
            "user_confirmed_tool_run: <user clicks confirm on CurrentPTO tool>",
            "tool_result: { 'num_hours': 400, 'num_days': 50 }",
            "agent: You have 400 hours, or 50 days, of PTO available. What dates would you like to take your time off? ",
            "user: Dec 1 through Dec 5",
            "agent: Let's check if you'll have enough PTO accrued by Dec 1 of this year to accomodate that.",
            "user_confirmed_tool_run: <user clicks confirm on FuturePTO tool>"
            'tool_result: {"enough_pto": True, "pto_hrs_remaining_after": 410}',
            "agent: You do in fact have enough PTO to accommodate that, and will have 410 hours remaining after you come back. Do you want to book the PTO? ",
            "user: yes ",
            "user_confirmed_tool_run: <user clicks confirm on BookPTO tool>",
            'tool_result: { "status": "success" }',
            "agent: PTO successfully booked! ",
        ]
    ),
)

goal_hr_check_pto = AgentGoal(
    id="goal_hr_check_pto",
    category_tag="hr",
    agent_name="Check PTO Amount",
    agent_friendly_description="Check your available PTO.",
    tools=[
        tool_registry.current_pto_tool,
    ],
    description="The user wants to check their paid time off (PTO) after today's date. To assist with that goal, help the user gather args for these tools in order: "
    "1. CurrentPTO: Tell the user how much PTO they currently have ",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to check my time off amounts at the current time",
            "agent: Sure! I can help you out with that. May I have your email address?",
            "user: bob.johnson@emailzzz.com",
            "agent: Great! I can tell you how much PTO you currently have accrued.",
            "user_confirmed_tool_run: <user clicks confirm on CurrentPTO tool>",
            "tool_result: { 'num_hours': 400, 'num_days': 50 }",
            "agent: You have 400 hours, or 50 days, of PTO available.",
        ]
    ),
)

goal_hr_check_paycheck_bank_integration_status = AgentGoal(
    id="goal_hr_check_paycheck_bank_integration_status",
    category_tag="hr",
    agent_name="Check paycheck deposit status",
    agent_friendly_description="Check your integration between your employer and your financial institution.",
    tools=[
        tool_registry.paycheck_bank_integration_status_check,
    ],
    description="The user wants to check their bank integration used to deposit their paycheck. To assist with that goal, help the user gather args for these tools in order: "
    "1. CheckPayBankStatus: Tell the user the status of their paycheck bank integration ",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to check paycheck bank integration",
            "agent: Sure! I can help you out with that. May I have your email address?",
            "user: bob.johnson@emailzzz.com",
            "agent: Great! I can tell you what the status is for your paycheck bank integration.",
            "user_confirmed_tool_run: <user clicks confirm on CheckPayBankStatus tool>",
            "tool_result: { 'status': connected }",
            "agent: Your paycheck bank deposit integration is properly connected.",
        ]
    ),
)

hr_goals: List[AgentGoal] = [
    goal_hr_schedule_pto,
    goal_hr_check_pto,
    goal_hr_check_paycheck_bank_integration_status,
]



================================================
FILE: goals/stripe_mcp.py
================================================
from typing import List

from models.tool_definitions import AgentGoal
from shared.mcp_config import get_stripe_mcp_server_definition

starter_prompt_generic = "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job."

goal_mcp_stripe = AgentGoal(
    id="goal_mcp_stripe",
    category_tag="mcp-integrations",
    agent_name="Stripe MCP Agent",
    agent_friendly_description="Manage Stripe operations via MCP",
    tools=[],  # Will be populated dynamically
    mcp_server_definition=get_stripe_mcp_server_definition(included_tools=[]),
    description="Help manage Stripe operations for customer and product data by using the customers.read and products.read tools.",
    starter_prompt="Welcome! I can help you read Stripe customer and product information.",
    example_conversation_history="\n ".join(
        [
            "agent: Welcome! I can help you read Stripe customer and product information. What would you like to do first?",
            "user: what customers are there?",
            "agent: I'll check for customers now.",
            "user_confirmed_tool_run: <user clicks confirm on customers.read tool>",
            'tool_result: { "customers": [{"id": "cus_abc", "name": "Customer A"}, {"id": "cus_xyz", "name": "Customer B"}] }',
            "agent: I found two customers: Customer A and Customer B. Can I help with anything else?",
            "user: what products exist?",
            "agent: Let me get the list of products for you.",
            "user_confirmed_tool_run: <user clicks confirm on products.read tool>",
            'tool_result: { "products": [{"id": "prod_123", "name": "Gold Plan"}, {"id": "prod_456", "name": "Silver Plan"}] }',
            "agent: I found two products: Gold Plan and Silver Plan.",
        ]
    ),
)


mcp_goals: List[AgentGoal] = [
    goal_mcp_stripe,
]



================================================
FILE: goals/travel.py
================================================
from typing import List

import tools.tool_registry as tool_registry
from models.tool_definitions import AgentGoal

starter_prompt_generic = "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job."

goal_match_train_invoice = AgentGoal(
    id="goal_match_train_invoice",
    category_tag="travel-trains",
    agent_name="UK Premier League Match Trip Booking",
    agent_friendly_description="Book a trip to a city in the UK around the dates of a premier league match.",
    tools=[
        tool_registry.search_fixtures_tool,
        tool_registry.search_trains_tool,
        tool_registry.book_trains_tool,
        tool_registry.create_invoice_tool,
    ],
    description="The user wants to book a trip to a city in the UK around the dates of a premier league match. "
    "Help the user find a premier league match to attend, search and book trains for that match and offers to invoice them for the cost of train tickets. "
    "The user lives in London. Premier league fixtures may be mocked data, so don't worry about valid season dates and teams. "
    "Gather args for these tools in order, ensuring you move the user from one tool to the next: "
    "1. SearchFixtures: Search for fixtures for a team within a specified date range. The user might ask questions about the matches dates and locations to decide on where to go. "
    "2. SearchTrains: Search for trains to the city of the match. Ensure you list them for the customer to choose from "
    "3. BookTrains: Book the train tickets, used to invoice the user for the cost of the train tickets "
    "4. CreateInvoice: Invoices the user for the cost of train tickets, with total and details inferred from the conversation history ",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to travel to a premier league match",
            "agent: Sure! Let's start by finding a match you'd like to attend. I know about Premier League fixtures in the UK. Could you tell me which team and what date range you're interested in?"
            "user: Wolves between mid-April and the first week of May, please."
            "agent: Great! Let's find fixtures for Wolverhampton Wanderers FC between 2025-04-15 and 2025-05-05."
            "user_confirmed_tool_run: <user clicks confirm on SearchFixtures tool, passing the full team name as an input>",
            'tool_result: SearchFixtures responds in this JSON format and the results are parsed by the agent below {"fixtures": [{"awayTeam": "West Ham United FC","date": "2025-04-01","homeTeam": "Wolverhampton Wanderers FC"},...,',
            "agent: I found 4 Wolves matches in May 2025: 1. Man City vs Wolves (Away) - May 3 2. Wolves vs Brighton (Home) - May 10 3. Crystal Palace vs Wolves (Away) - May 18 4. Wolves vs Brentford (Home) - May 25 Which match would you like to attend? I'll help you find trains from London.",
            "user: How about the Man City match",
            "agent: Great! Let's find trains to Manchester and back for the match.",
            "user_confirmed_tool_run: <user clicks confirm on SearchTrains tool>",
            'tool_result: SearchTrains responds in this JSON format and the results are parsed by the agent below: {"journeys": [{"arrival": "Manchester","arrival_time": "2025-04-18T12:11","departure": "London","departure_time": "2025-04-18T11:00","id": "T8049","platform": "1","price": 73.5,"type": "outbound"},',
            "agent: I found several train options for your journey to Manchester including outbound options on May 9 at 11am, 3:30pm and 4:30pm and return options on May 11 at 9am, 11am and 1pm. Which trains would you like to book?",
            "user: I'd like the 11am outbound and 3:30pm return",
            "agent: Sounds good, let's book train tickets for the 11am outbound and 3:30pm return trains on May 9 and May 11, one day before and after the match.",
            "user_confirmed_tool_run: <user clicks confirm on BookTrains tool>",
            'tool_result: BookTrains responds in this JSON format and the results are parsed by the agent belowg [{"booking_reference": "BR10879","journey_id": "T9532,T1027","status": "confirmed"}]',
            "agent: Your train tickets have been booked with the reference ABCD1234. Are you ready to be invoiced for the total cost of the train tickets?",
            "user: Yes, pelase invoice me.",
            "user_confirmed_tool_run: <user clicks confirm on CreateInvoice tool which includes details of the train journey, the match, and the total cost>",
            'tool_result: CreateInvoice responds in this JSON format and the results are parsed by the agent below (including a link to the invoice): {"invoiceStatus": "open","invoiceURL": "https://invoice.stripe.com/i/acct_1NBOLuKVZbzw7QA5/test_YWNjdF8xTkJPTHVLVlpienc3UUE1LF9SbGJlZ2xLMjhlc3lxNzFkVVBXbkswOUlFa2Rna1RxLDEzMDAwMTY4Nw0200RLeJRMlw?s=ap","reference": "F9B01CD7-0001"}',
            "agent: Great! I've generated your invoice for your trains to the Manchester City match on the 10th of May. You can view and pay your invoice at this link: https://invoice.stripe.com/i/acct_1NBOLuKVZbzw7QA5/test_YWNjdF8xTkJPTHVLVlpienc3UUE1LF9SbGJlZ2xLMjhlc3lxNzFkVVBXbkswOUlFa2Rna1RxLDEzMDAwMTY4Nw0200RLeJRMlw?s=ap <this is the end of the chat>",
        ]
    ),
)

goal_event_flight_invoice = AgentGoal(
    id="goal_event_flight_invoice",
    category_tag="travel-flights",
    agent_name="Australia and New Zealand Event Flight Booking",
    agent_friendly_description="Book a trip to a city in Australia or New Zealand around the dates of events in that city.",
    tools=[
        tool_registry.find_events_tool,
        tool_registry.search_flights_tool,
        tool_registry.create_invoice_tool,
    ],
    description="Help the user gather args for these tools in order: "
    "1. FindEvents: Find an event in Australia or New Zealand to travel to "
    "2. SearchFlights: search for a flight around the event dates "
    "3. CreateInvoice: Create a simple invoice for the cost of that flight ",
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I'd like to travel to an event",
            "agent: Sure! Let's start by finding an event you'd like to attend. I know about events in Australia and New Zealand cities. Could you tell me which city and month you're interested in?",
            "user: sydney in may please",
            "agent: Great! Let's find an events in Sydney in May.",
            "user_confirmed_tool_run: <user clicks confirm on FindEvents tool>",
            "tool_result: { 'event_name': 'Vivid Sydney', 'event_date': '2023-05-01' }",
            "agent: Found an event! There's Vivid Sydney on May 1 2025, ending on May 14 2025. Would you like to search for flights around these dates?",
            "user: Yes, please",
            "agent: Let's search for flights around these dates. Could you provide your departure city?",
            "user: San Francisco",
            "agent: Thanks, searching for flights from San Francisco to Sydney around 2023-02-25 to 2023-02-28.",
            "user_confirmed_tool_run: <user clicks confirm on SearchFlights tool>"
            'tool_result: results including {"flight_number": "CX101", "return_flight_number": "CX102", "price": 850.0}',
            "agent: Found some flights! The cheapest is CX101 for $850. Would you like to generate an invoice for this flight?",
            "user_confirmed_tool_run: <user clicks confirm on CreateInvoice tool>",
            'tool_result: { "status": "success", "invoice": { "flight_number": "CX101", "amount": 850.0 }, invoiceURL: "https://example.com/invoice" }',
            "agent: Invoice generated! Here's the link: https://example.com/invoice",
        ]
    ),
)

travel_goals: List[AgentGoal] = [
    goal_match_train_invoice,
    goal_event_flight_invoice,
]



================================================
FILE: models/__init__.py
================================================
[Empty file]


================================================
FILE: models/data_types.py
================================================
from dataclasses import dataclass
from typing import Any, Deque, Dict, List, Literal, Optional, Union

from models.tool_definitions import AgentGoal


@dataclass
class AgentGoalWorkflowParams:
    conversation_summary: Optional[str] = None
    prompt_queue: Optional[Deque[str]] = None


@dataclass
class CombinedInput:
    tool_params: AgentGoalWorkflowParams
    agent_goal: AgentGoal


Message = Dict[str, Union[str, Dict[str, Any]]]
ConversationHistory = Dict[str, List[Message]]
NextStep = Literal["confirm", "question", "pick-new-goal", "done"]


@dataclass
class ToolPromptInput:
    prompt: str
    context_instructions: str


@dataclass
class ValidationInput:
    prompt: str
    conversation_history: ConversationHistory
    agent_goal: AgentGoal


@dataclass
class ValidationResult:
    validationResult: bool
    validationFailedReason: dict = None

    def __post_init__(self):
        # Initialize empty dict if None
        if self.validationFailedReason is None:
            self.validationFailedReason = {}


@dataclass
class EnvLookupInput:
    show_confirm_env_var_name: str
    show_confirm_default: bool


@dataclass
class EnvLookupOutput:
    show_confirm: bool
    multi_goal_mode: bool



================================================
FILE: models/tool_definitions.py
================================================
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MCPServerDefinition:
    """Definition for an MCP (Model Context Protocol) server connection"""

    name: str
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None
    connection_type: str = "stdio"
    included_tools: Optional[List[str]] = None


@dataclass
class ToolArgument:
    name: str
    type: str
    description: str


@dataclass
class ToolDefinition:
    name: str
    description: str
    arguments: List[ToolArgument]


@dataclass
class AgentGoal:
    id: str
    category_tag: str
    agent_name: str
    agent_friendly_description: str
    tools: List[ToolDefinition]
    description: str = "Description of the tools purpose and overall goal"
    starter_prompt: str = "Initial prompt to start the conversation"
    example_conversation_history: str = "Example conversation history to help the AI agent understand the context of the conversation"
    mcp_server_definition: Optional[MCPServerDefinition] = None



================================================
FILE: prompts/__init__.py
================================================
[Empty file]


================================================
FILE: prompts/agent_prompt_generators.py
================================================
import json
from typing import Optional

from models.tool_definitions import AgentGoal

MULTI_GOAL_MODE: bool = None


def generate_genai_prompt(
    agent_goal: AgentGoal,
    conversation_history: str,
    multi_goal_mode: bool,
    raw_json: Optional[str] = None,
    mcp_tools_info: Optional[dict] = None,
) -> str:
    """
    Generates a concise prompt for producing or validating JSON instructions
    with the provided tools and conversation history.
    """
    prompt_lines = []
    set_multi_goal_mode_if_unset(multi_goal_mode)

    # Intro / Role
    prompt_lines.append(
        "You are an AI agent that helps fill required arguments for the tools described below. "
        "CRITICAL: You must respond with ONLY valid JSON using the exact schema provided. "
        "DO NOT include any text before or after the JSON. Your entire response must be parseable JSON."
    )

    # Main Conversation History
    prompt_lines.append("=== Conversation History ===")
    prompt_lines.append(
        "This is the ongoing history to determine which tool and arguments to gather:"
    )
    prompt_lines.append("*BEGIN CONVERSATION HISTORY*")
    prompt_lines.append(json.dumps(conversation_history, indent=2))
    prompt_lines.append("*END CONVERSATION HISTORY*")
    prompt_lines.append(
        "REMINDER: You can use the conversation history to infer arguments for the tools."
    )

    # Example Conversation History (from agent_goal)
    if agent_goal.example_conversation_history:
        prompt_lines.append("=== Example Conversation With These Tools ===")
        prompt_lines.append(
            "Use this example to understand how tools are invoked and arguments are gathered."
        )
        prompt_lines.append("BEGIN EXAMPLE")
        prompt_lines.append(agent_goal.example_conversation_history)
        prompt_lines.append("END EXAMPLE")
        prompt_lines.append("")

    # Add MCP server context if present
    if agent_goal.mcp_server_definition:
        prompt_lines.append("=== MCP Server Information ===")
        prompt_lines.append(
            f"Connected to MCP Server: {agent_goal.mcp_server_definition.name}"
        )
        if mcp_tools_info and mcp_tools_info.get("success", False):
            tools = mcp_tools_info.get("tools", {})
            server_name = mcp_tools_info.get("server_name", "Unknown")
            prompt_lines.append(
                f"MCP Tools loaded from {server_name} ({len(tools)} tools):"
            )
            for tool_name, tool_info in tools.items():
                prompt_lines.append(
                    f"  - {tool_name}: {tool_info.get('description', 'No description')}"
                )
        else:
            prompt_lines.append("Additional tools available via MCP integration:")
        prompt_lines.append("")

    # Tools Definitions
    prompt_lines.append("=== Tools Definitions ===")
    prompt_lines.append(f"There are {len(agent_goal.tools)} available tools:")
    prompt_lines.append(", ".join([t.name for t in agent_goal.tools]))
    prompt_lines.append(f"Goal: {agent_goal.description}")
    prompt_lines.append(
        "CRITICAL: You MUST follow the complete sequence described in the Goal above. "
        "Do NOT skip steps or assume the goal is complete until ALL steps are done."
    )
    prompt_lines.append(
        "Gather the necessary information for each tool in the sequence described above."
    )
    prompt_lines.append(
        "Only ask for arguments listed below. Do not add extra arguments."
    )
    prompt_lines.append("")
    for tool in agent_goal.tools:
        prompt_lines.append(f"Tool name: {tool.name}")
        prompt_lines.append(f"  Description: {tool.description}")
        prompt_lines.append("  Required args:")
        for arg in tool.arguments:
            prompt_lines.append(f"    - {arg.name} ({arg.type}): {arg.description}")
        prompt_lines.append("")
    prompt_lines.append(
        "When all required args for a tool are known, you can propose next='confirm' to run it."
    )

    # JSON Format Instructions
    prompt_lines.append("=== CRITICAL: JSON-ONLY RESPONSE FORMAT ===")
    prompt_lines.append(
        "MANDATORY: Your response must be ONLY valid JSON with NO additional text.\n"
        "NO explanations, NO comments, NO text before or after the JSON.\n"
        "Your entire response must start with '{' and end with '}'.\n\n"
        "Required JSON format:\n"
        "{\n"
        '  "response": "<plain text>",\n'
        '  "next": "<question|confirm|pick-new-goal|done>",\n'
        '  "tool": "<tool_name or null>",\n'
        '  "args": {\n'
        '    "<arg1>": "<value1 or null>",\n'
        '    "<arg2>": "<value2 or null>",\n'
        "    ...\n"
        "  }\n"
        "}\n\n"
        "INVALID EXAMPLE: 'Thank you for providing... {\"response\": ...}'\n"
        'VALID EXAMPLE: \'{"response": "Thank you for providing...", "next": ...}\''
    )
    prompt_lines.append(
        "DECISION LOGIC (follow this exact order):\n"
        "1) Do I need to run a tool next?\n"
        "   - If your response says 'let's get/proceed/check/add/create/finalize...' -> YES, you need a tool\n"
        "   - If you're announcing what you're about to do -> YES, you need a tool\n"
        "   - If no more steps needed for current goal -> NO, go to step 3\n\n"
        "2) If YES to step 1: Do I have all required arguments?\n"
        "   - Check tool definition for required args\n"
        "   - Can I fill missing args from conversation history?\n"
        "   - Can I use sensible defaults (limit=100, etc.)?\n"
        "   - If ALL args available/inferrable -> set next='confirm', specify tool and args\n"
        "   - If missing required args -> set next='question', ask for missing args, tool=null\n\n"
        "3) If NO to step 1: Is the entire goal complete?\n"
        "   - Check Goal description in system prompt - are ALL steps done?\n"
        "   - Check recent conversation for completion indicators ('finalized', 'complete', etc.)\n"
        f"   - If complete -> {generate_toolchain_complete_guidance()}\n"
        "   - If not complete -> identify next needed tool, go to step 2\n\n"
        "CRITICAL RULES:\n"
        "• RESPOND WITH JSON ONLY - NO TEXT BEFORE OR AFTER THE JSON OBJECT\n"
        "• Your response must start with '{' and end with '}' - nothing else\n"
        "• NEVER set next='question' without asking an actual question in your response\n"
        "• NEVER set tool=null when you're announcing you'll run a specific tool\n"
        "• If response contains 'let's proceed to get pricing' -> next='confirm', tool='list_prices'\n"
        "• If response contains 'Now adding X' -> next='confirm', tool='create_invoice_item'\n"
        "• Use conversation history to infer arguments (customer IDs, product IDs, etc.)\n"
        "• Use sensible defaults rather than asking users for technical parameters\n"
        "• Carry forward arguments between tools (same customer, same invoice, etc.)\n"
        "• If force_confirm='False' in history, be declarative, don't ask permission\n\n"
        "EXAMPLES:\n"
        "WRONG: response='let\\'s get pricing', next='question', tool=null\n"
        "RIGHT: response='let\\'s get pricing', next='confirm', tool='list_prices'\n"
        "WRONG: response='adding pizza', next='question', tool='create_invoice_item'\n"
        "RIGHT: response='adding pizza', next='confirm', tool='create_invoice_item'\n"
    )

    # Validation Task (If raw_json is provided)
    if raw_json is not None:
        prompt_lines.append("")
        prompt_lines.append("=== Validation Task ===")
        prompt_lines.append("Validate and correct the following JSON if needed:")
        prompt_lines.append(json.dumps(raw_json, indent=2))
        prompt_lines.append("")
        prompt_lines.append(
            "Check syntax, 'tool' validity, 'args' completeness, "
            "and set 'next' appropriately. Return ONLY corrected JSON."
        )

    # Prompt Start
    prompt_lines.append("")
    prompt_lines.append("=== FINAL REMINDER ===")
    prompt_lines.append("RESPOND WITH VALID JSON ONLY. NO ADDITIONAL TEXT.")
    prompt_lines.append("")
    if raw_json is not None:
        prompt_lines.append(
            "Validate the provided JSON and return ONLY corrected JSON."
        )
    else:
        prompt_lines.append(
            "Return ONLY a valid JSON response. Start with '{' and end with '}'."
        )

    return "\n".join(prompt_lines)


def generate_tool_completion_prompt(current_tool: str, dynamic_result: dict) -> str:
    """
    Generates a prompt for handling tool completion and determining next steps.

    Args:
        current_tool: The name of the tool that just completed
        dynamic_result: The result data from the tool execution

    Returns:
        str: A formatted prompt string for the agent to process the tool completion
    """
    return (
        f"### The '{current_tool}' tool completed successfully with {dynamic_result}. "
        "INSTRUCTIONS: Parse this tool result as plain text, and use the system prompt containing the list of tools in sequence and the conversation history (and previous tool_results) to figure out next steps, if any. "
        "You will need to use the tool_results to auto-fill arguments for subsequent tools and also to figure out if all tools have been run. "
        '{"next": "<question|confirm|pick-new-goal|done>", "tool": "<tool_name or null>", "args": {"<arg1>": "<value1 or null>", "<arg2>": "<value2 or null>}, "response": "<plain text (can include \\n line breaks)>"}'
        "ONLY return those json keys (next, tool, args, response), nothing else. "
        'Next should be "question" if the tool is not the last one in the sequence. '
        'Next should be "done" if the user is asking to be done with the chat. '
        f"{generate_pick_new_goal_guidance()}"
    )


def generate_missing_args_prompt(
    current_tool: str, tool_data: dict, missing_args: list[str]
) -> str:
    """
    Generates a prompt for handling missing arguments for a tool.

    Args:
        current_tool: The name of the tool that needs arguments
        tool_data: The current tool data containing the response
        missing_args: List of argument names that are missing

    Returns:
        str: A formatted prompt string for requesting missing arguments
    """
    return (
        f"### INSTRUCTIONS set next='question', combine this response response='{tool_data.get('response')}' "
        f"and following missing arguments for tool {current_tool}: {missing_args}. "
        "Only provide a valid JSON response without any comments or metadata."
    )


def set_multi_goal_mode_if_unset(mode: bool) -> None:
    """
    Set multi-mode (used to pass workflow)

    Args:
        None

    Returns:
        bool: True if in multi-goal mode, false if not
    """
    global MULTI_GOAL_MODE
    if MULTI_GOAL_MODE is None:
        MULTI_GOAL_MODE = mode


def is_multi_goal_mode() -> bool:
    """
    Centralized logic for if we're in multi-goal mode.

    Args:
        None

    Returns:
        bool: True if in multi-goal mode, false if not
    """
    return MULTI_GOAL_MODE


def generate_pick_new_goal_guidance() -> str:
    """
    Generates a prompt for guiding the LLM to pick a new goal or be done depending on multi-goal mode.

    Args:
        None

    Returns:
        str: A prompt string prompting the LLM to when to go to pick-new-goal
    """
    if is_multi_goal_mode():
        return 'Next should only be "pick-new-goal" if EVERY SINGLE STEP in the Goal description has been completed (check the system prompt Goal section carefully), or the user explicitly requested to pick a new goal. If any step is missing (like customer creation, invoice creation, or payment processing), continue with the next required tool.'
    else:
        return 'Next should never be "pick-new-goal".'


def generate_toolchain_complete_guidance() -> str:
    """
    Generates a prompt for guiding the LLM to handle the end of the toolchain.

    Args:
        None

    Returns:
        str: A prompt string prompting the LLM to prompt for a new goal, or be done
    """
    if is_multi_goal_mode():
        return "If no more tools are needed for the current goal (EVERY step in the Goal description has been completed AND user_confirmed_tool_run has been run for all required tools), set next='pick-new-goal' and tool=null to allow the user to choose their next action."
    else:
        return "If no more tools are needed (EVERY step in the Goal description has been completed AND user_confirmed_tool_run has been run for all), set next='done' and tool=null."



================================================
FILE: scripts/create_invoice_test.py
================================================
from tools.create_invoice import create_invoice

if __name__ == "__main__":
    # Example usage:
    args_create = {
        "email": "jenny.rosen@example.com",
        "amount": 150.00,
        "description": "Flight to Seattle",
        "days_until_due": 7,
    }
    invoice_details = create_invoice(args_create)
    print(invoice_details)



================================================
FILE: scripts/end_chat.py
================================================
import asyncio

from shared.config import get_temporal_client
from workflows.agent_goal_workflow import AgentGoalWorkflow


async def main():
    # Create client connected to server at the given address
    client = await get_temporal_client()

    workflow_id = "agent-workflow"

    handle = client.get_workflow_handle_for(AgentGoalWorkflow.run, workflow_id)

    # Sends a signal to the workflow
    await handle.signal(AgentGoalWorkflow.end_chat)


if __name__ == "__main__":
    print("Sending signal to end chat.")
    asyncio.run(main())



================================================
FILE: scripts/find_events_test.py
================================================
import json

from tools.search_flights import search_flights

# Example usage
if __name__ == "__main__":
    search_args = {"city": "Sydney", "month": "July"}
    results = search_flights(search_args)
    print(json.dumps(results, indent=2))



================================================
FILE: scripts/flight_api_test.py
================================================
import json

from tools.search_flights import search_flights

if __name__ == "__main__":
    # Suppose user typed "new" for New York, "lon" for London
    flights = search_flights("London", "JFK", "2025-01-15", "2025-01-23")
    print(json.dumps(flights, indent=2))



================================================
FILE: scripts/get_history.py
================================================
import asyncio

from shared.config import get_temporal_client
from workflows.agent_goal_workflow import AgentGoalWorkflow


async def main():
    # Create client connected to server at the given address
    client = await get_temporal_client()
    workflow_id = "agent-workflow"

    handle = client.get_workflow_handle(workflow_id)

    # Queries the workflow for the conversation history
    history = await handle.query(AgentGoalWorkflow.get_conversation_history)

    print("Conversation History")
    print(history)


if __name__ == "__main__":
    asyncio.run(main())



================================================
FILE: scripts/run_legacy_worker.py
================================================
import asyncio
import concurrent.futures

from temporalio.worker import Worker

from activities.tool_activities import dynamic_tool_activity
from shared.config import TEMPORAL_LEGACY_TASK_QUEUE, get_temporal_client


async def main():
    # Create the client
    client = await get_temporal_client()

    # Run the worker
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue=TEMPORAL_LEGACY_TASK_QUEUE,
            activities=[
                dynamic_tool_activity,
            ],
            activity_executor=activity_executor,
        )

        print(
            f"Starting legacy worker, connecting to task queue: {TEMPORAL_LEGACY_TASK_QUEUE}"
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())



================================================
FILE: scripts/run_worker.py
================================================
import asyncio
import concurrent.futures
import logging
import os

from dotenv import load_dotenv
from temporalio.worker import Worker

from activities.tool_activities import (
    ToolActivities,
    dynamic_tool_activity,
    mcp_list_tools,
)
from shared.config import TEMPORAL_TASK_QUEUE, get_temporal_client
from shared.mcp_client_manager import MCPClientManager
from workflows.agent_goal_workflow import AgentGoalWorkflow


async def main():
    # Load environment variables
    load_dotenv(override=True)

    # Print LLM configuration info
    llm_model = os.environ.get("LLM_MODEL", "openai/gpt-4")
    print(f"Worker will use LLM model: {llm_model}")

    # Create shared MCP client manager
    mcp_client_manager = MCPClientManager()

    # Create the client
    client = await get_temporal_client()

    # Initialize the activities class with injected manager
    activities = ToolActivities(mcp_client_manager)
    print(f"ToolActivities initialized with LLM model: {llm_model}")

    # If using Ollama, pre-load the model to avoid cold start latency
    if llm_model.startswith("ollama"):
        print("\n======== OLLAMA MODEL INITIALIZATION ========")
        print("Ollama models need to be loaded into memory on first use.")
        print("This may take 30+ seconds depending on your hardware and model size.")
        print("Please wait while the model is being loaded...")

        # This call will load the model and measure initialization time
        success = activities.warm_up_ollama()

        if success:
            print("===========================================================")
            print("✅ Ollama model successfully pre-loaded and ready for requests!")
            print("===========================================================\n")
        else:
            print("===========================================================")
            print("⚠️ Ollama model pre-loading failed. The worker will continue,")
            print("but the first actual request may experience a delay while")
            print("the model is loaded on-demand.")
            print("===========================================================\n")

    print("Worker ready to process tasks!")
    logging.basicConfig(level=logging.INFO)

    # Run the worker with proper cleanup
    try:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=100
        ) as activity_executor:
            worker = Worker(
                client,
                task_queue=TEMPORAL_TASK_QUEUE,
                workflows=[AgentGoalWorkflow],
                activities=[
                    activities.agent_validatePrompt,
                    activities.agent_toolPlanner,
                    activities.get_wf_env_vars,
                    activities.mcp_tool_activity,
                    dynamic_tool_activity,
                    mcp_list_tools,
                ],
                activity_executor=activity_executor,
            )

            print(f"Starting worker, connecting to task queue: {TEMPORAL_TASK_QUEUE}")
            await worker.run()
    finally:
        # Cleanup MCP connections when worker shuts down
        await mcp_client_manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())



================================================
FILE: scripts/send_confirm.py
================================================
import asyncio
import sys

from shared.config import get_temporal_client


async def main():
    # Connect to Temporal and signal the workflow
    client = await get_temporal_client()

    workflow_id = "agent-workflow"

    await client.get_workflow_handle(workflow_id).signal("confirm")


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: python send_confirm.py'")
    else:
        asyncio.run(main())



================================================
FILE: shared/config.py
================================================
import os

from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.service import TLSConfig

load_dotenv(override=True)

# Temporal connection settings
TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")
TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "agent-task-queue")
TEMPORAL_LEGACY_TASK_QUEUE = os.getenv(
    "TEMPORAL_LEGACY_TASK_QUEUE", "agent-task-queue-legacy"
)

# Authentication settings
TEMPORAL_TLS_CERT = os.getenv("TEMPORAL_TLS_CERT", "")
TEMPORAL_TLS_KEY = os.getenv("TEMPORAL_TLS_KEY", "")
TEMPORAL_API_KEY = os.getenv("TEMPORAL_API_KEY", "")


async def get_temporal_client() -> Client:
    """
    Creates a Temporal client based on environment configuration.
    Supports local server, mTLS, and API key authentication methods.
    """
    # Default to no TLS for local development
    tls_config = False
    print(f"Address: {TEMPORAL_ADDRESS}, Namespace {TEMPORAL_NAMESPACE}")
    print("(If unset, then will try to connect to local server)")

    # Configure mTLS if certificate and key are provided
    if TEMPORAL_TLS_CERT and TEMPORAL_TLS_KEY:
        print(f"TLS cert: {TEMPORAL_TLS_CERT}")
        print(f"TLS key: {TEMPORAL_TLS_KEY}")
        with open(TEMPORAL_TLS_CERT, "rb") as f:
            client_cert = f.read()
        with open(TEMPORAL_TLS_KEY, "rb") as f:
            client_key = f.read()
        tls_config = TLSConfig(
            client_cert=client_cert,
            client_private_key=client_key,
        )

    # Use API key authentication if provided
    if TEMPORAL_API_KEY:
        print(f"API key: {TEMPORAL_API_KEY}")
        return await Client.connect(
            TEMPORAL_ADDRESS,
            namespace=TEMPORAL_NAMESPACE,
            api_key=TEMPORAL_API_KEY,
            tls=True,  # Always use TLS with API key
        )

    # Use mTLS or local connection
    return await Client.connect(
        TEMPORAL_ADDRESS,
        namespace=TEMPORAL_NAMESPACE,
        tls=tls_config,
    )



================================================
FILE: shared/mcp_client_manager.py
================================================
import asyncio
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Dict, Tuple

from temporalio import activity

from models.tool_definitions import MCPServerDefinition

# Import MCP client libraries
if TYPE_CHECKING:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
else:
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError:
        # Fallback if MCP not installed
        ClientSession = None
        StdioServerParameters = None
        stdio_client = None


class MCPClientManager:
    """Manages pooled MCP client connections for reuse across tool calls"""

    def __init__(self):
        self._clients: Dict[str, Any] = {}
        self._connections: Dict[str, Tuple[Any, Any]] = {}
        self._lock = asyncio.Lock()

    async def get_client(
        self, server_def: MCPServerDefinition | Dict[str, Any] | None
    ) -> Any:
        """Return existing client or create new one, keyed by server definition hash"""
        async with self._lock:
            key = self._get_server_key(server_def)
            if key not in self._clients:
                await self._create_client(server_def, key)
                activity.logger.info(
                    f"Created new MCP client for {self._get_server_name(server_def)}"
                )
            else:
                activity.logger.info(
                    f"Reusing existing MCP client for {self._get_server_name(server_def)}"
                )
            return self._clients[key]

    def _get_server_key(
        self, server_def: MCPServerDefinition | Dict[str, Any] | None
    ) -> str:
        """Generate unique key for server definition"""
        if server_def is None:
            return "default:python:server.py"

        # Handle both MCPServerDefinition objects and dicts (from Temporal serialization)
        if isinstance(server_def, dict):
            name = server_def.get("name", "default")
            command = server_def.get("command", "python")
            args = server_def.get("args", ["server.py"])
        else:
            name = server_def.name
            command = server_def.command
            args = server_def.args

        return f"{name}:{command}:{':'.join(args)}"

    def _get_server_name(
        self, server_def: MCPServerDefinition | Dict[str, Any] | None
    ) -> str:
        """Get server name for logging"""
        if server_def is None:
            return "default"

        if isinstance(server_def, dict):
            return server_def.get("name", "default")
        else:
            return server_def.name

    def _build_connection(
        self, server_def: MCPServerDefinition | Dict[str, Any] | None
    ) -> Dict[str, Any]:
        """Build connection parameters from MCPServerDefinition or dict"""
        if server_def is None:
            # Default to stdio connection with the main server
            return {
                "type": "stdio",
                "command": "python",
                "args": ["server.py"],
                "env": {},
            }

        # Handle both MCPServerDefinition objects and dicts (from Temporal serialization)
        if isinstance(server_def, dict):
            return {
                "type": server_def.get("connection_type", "stdio"),
                "command": server_def.get("command", "python"),
                "args": server_def.get("args", ["server.py"]),
                "env": server_def.get("env", {}) or {},
            }

        return {
            "type": server_def.connection_type,
            "command": server_def.command,
            "args": server_def.args,
            "env": server_def.env or {},
        }

    @asynccontextmanager
    async def _stdio_connection(self, command: str, args: list, env: dict):
        """Create stdio connection to MCP server"""
        if stdio_client is None:
            raise Exception("MCP client libraries not available")

        # Create server parameters
        server_params = StdioServerParameters(command=command, args=args, env=env)

        async with stdio_client(server_params) as (read, write):
            yield read, write

    async def _create_client(
        self, server_def: MCPServerDefinition | Dict[str, Any] | None, key: str
    ):
        """Create and store new client connection"""
        connection = self._build_connection(server_def)

        if connection["type"] == "stdio":
            # Create stdio connection
            connection_manager = self._stdio_connection(
                command=connection.get("command", "python"),
                args=connection.get("args", ["server.py"]),
                env=connection.get("env", {}),
            )

            # Enter the connection context
            read, write = await connection_manager.__aenter__()

            # Create and initialize client session
            session = ClientSession(read, write)
            await session.initialize()

            # Store both the session and connection manager for cleanup
            self._clients[key] = session
            self._connections[key] = (connection_manager, read, write)
        else:
            raise Exception(f"Unsupported connection type: {connection['type']}")

    async def cleanup(self):
        """Close all connections gracefully"""
        async with self._lock:
            # Close all client sessions
            for session in self._clients.values():
                try:
                    await session.close()
                except Exception as e:
                    activity.logger.warning(f"Error closing MCP session: {e}")

            # Exit all connection contexts
            for connection_manager, read, write in self._connections.values():
                try:
                    await connection_manager.__aexit__(None, None, None)
                except Exception as e:
                    activity.logger.warning(f"Error closing MCP connection: {e}")

            self._clients.clear()
            self._connections.clear()
            activity.logger.info("All MCP connections closed")



================================================
FILE: shared/mcp_config.py
================================================
import os

from models.tool_definitions import MCPServerDefinition


def get_stripe_mcp_server_definition(included_tools: list[str]) -> MCPServerDefinition:
    """
    Returns a Stripe MCP server definition with customizable included tools.

    Args:
        included_tools: List of tool names to include from the Stripe MCP server

    Returns:
        MCPServerDefinition configured for Stripe
    """
    return MCPServerDefinition(
        name="stripe-mcp",
        command="npx",
        args=[
            "-y",
            "@stripe/mcp",
            "--tools=all",
            f"--api-key={os.getenv('STRIPE_API_KEY')}",
        ],
        env=None,
        included_tools=included_tools,
    )



================================================
FILE: tests/README.md
================================================
# Temporal AI Agent - Testing Guide

This directory contains comprehensive tests for the Temporal AI Agent project. The tests cover workflows, activities, and integration scenarios using Temporal's testing framework.

## Test Structure

```
tests/
├── README.md                      # This file - testing documentation
├── conftest.py                    # Test configuration and fixtures
├── test_agent_goal_workflow.py    # Workflow tests
├── test_tool_activities.py        # Activity tests
└── workflowtests/                 # Legacy workflow tests
    └── agent_goal_workflow_test.py
```

## Test Types

### 1. Workflow Tests (`test_agent_goal_workflow.py`)

Tests the main `AgentGoalWorkflow` class covering:

- **Workflow Initialization**: Basic workflow startup and state management
- **Signal Handling**: Testing user_prompt, confirm, end_chat signals
- **Query Methods**: Testing all workflow query endpoints
- **State Management**: Conversation history, goal changes, tool data
- **Validation Flow**: Prompt validation and error handling
- **Tool Execution Flow**: Confirmation and tool execution cycles

### 2. Activity Tests (`test_tool_activities.py`)

Tests the `ToolActivities` class and `dynamic_tool_activity` function:

- **LLM Integration**: Testing agent_toolPlanner with mocked LLM responses
- **Validation Logic**: Testing agent_validatePrompt with various scenarios
- **Environment Configuration**: Testing get_wf_env_vars with different env setups
- **JSON Processing**: Testing response parsing and sanitization
- **Dynamic Tool Execution**: Testing the dynamic activity dispatcher
- **Integration**: End-to-end activity execution in Temporal workers

### 3. Configuration Tests (`conftest.py`)

Provides shared test fixtures and configuration:

- **Temporal Environment**: Local and time-skipping test environments
- **Sample Data**: Pre-configured agent goals, conversation history, inputs
- **Test Client**: Configured Temporal client for testing

## Running Tests

### Prerequisites

Ensure you have the required dependencies installed:

```bash
uv sync
```

### Basic Test Execution

Run all tests:
```bash
uv run pytest
```

Run specific test files:
```bash
# Workflow tests only
uv run pytest tests/test_agent_goal_workflow.py

# Activity tests only
uv run pytest tests/test_tool_activities.py

# Legacy tests
uv run pytest tests/workflowtests/
```

Run with verbose output:
```bash
uv run pytest -v
```

### Test Environment Options

The tests support different Temporal environments via the `--workflow-environment` flag:

#### Local Environment (Default)
Uses a local Temporal test server:
```bash
uv run pytest --workflow-environment=local
```

#### Time-Skipping Environment
Uses Temporal's time-skipping test environment for faster execution:
```bash
uv run pytest --workflow-environment=time-skipping
```

#### External Server
Connect to an existing Temporal server:
```bash
uv run pytest --workflow-environment=localhost:7233
```

#### Setup Script for AI Agent environments such as OpenAI Codex
```bash
export SHELL=/bin/bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
ls
uv sync
cd frontend
npm install
cd ..

# Pre-download the temporal test server binary
uv run python -c "
import asyncio
import sys
from temporalio.testing import WorkflowEnvironment

async def predownload():
    try:
        print('Starting test server download...')
        env = await WorkflowEnvironment.start_time_skipping()
        print('Test server downloaded and started successfully')
        await env.shutdown()
        print('Test server shut down successfully')
    except Exception as e:
        print(f'Error during download: {e}')
        sys.exit(1)

asyncio.run(predownload())
"
```

### Filtering Tests

Run tests by pattern:
```bash
# Run only validation tests
uv run pytest -k "validation"

# Run only workflow tests
uv run pytest -k "workflow"

# Run only activity tests
uv run pytest -k "activity"
```

Run tests by marker (if you add custom markers):
```bash
# Run only integration tests
uv run pytest -m integration

# Skip slow tests
uv run pytest -m "not slow"
```

## Test Configuration

### Test Discovery

The `vibe/` directory is excluded from test collection to avoid conflicts with sample tests. This is configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
norecursedirs = ["vibe"]
```

### Environment Variables

Tests respect the following environment variables:

- `LLM_MODEL`: Model to use for LLM testing (defaults to "openai/gpt-4")
- `LLM_KEY`: API key for LLM service
- `LLM_BASE_URL`: Custom base URL for LLM service
- `SHOW_CONFIRM`: Whether to show confirmation dialogs
- `AGENT_GOAL`: Default agent goal setting

### Mocking Strategy

The tests use extensive mocking to avoid external dependencies:

- **LLM Calls**: Mocked using `unittest.mock` to avoid actual API calls
- **Tool Handlers**: Mocked to test workflow logic without tool execution
- **Environment Variables**: Patched for consistent test environments

## Writing New Tests

### Test Naming Convention

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<functionality>_<scenario>`

Example:
```python
class TestAgentGoalWorkflow:
    async def test_user_prompt_signal_valid_input(self, client, sample_combined_input):
        # Test implementation
        pass
```

### Using Fixtures

Leverage the provided fixtures for consistent test data:

```python
async def test_my_workflow(self, client, sample_agent_goal, sample_conversation_history):
    # client: Temporal test client
    # sample_agent_goal: Pre-configured AgentGoal
    # sample_conversation_history: Sample conversation data
    pass
```

### Mocking External Dependencies

Always mock external services:

```python
@patch('activities.tool_activities.completion')
async def test_llm_integration(self, mock_completion):
    mock_completion.return_value.choices[0].message.content = '{"test": "response"}'
    # Test implementation
```

### Testing Workflow Signals and Queries

```python
async def test_workflow_signal(self, client, sample_combined_input):
    # Start workflow
    handle = await client.start_workflow(
        AgentGoalWorkflow.run,
        sample_combined_input,
        id=str(uuid.uuid4()),
        task_queue=task_queue_name,
    )
    
    # Send signal
    await handle.signal(AgentGoalWorkflow.user_prompt, "test message")
    
    # Query state
    conversation = await handle.query(AgentGoalWorkflow.get_conversation_history)
    
    # End workflow
    await handle.signal(AgentGoalWorkflow.end_chat)
    result = await handle.result()
```

## Test Data and Fixtures

### Sample Agent Goal

The `sample_agent_goal` fixture provides a basic agent goal with:
- Goal ID: "test_goal"
- One test tool with a required string argument
- Suitable for most workflow testing scenarios

### Sample Conversation History

The `sample_conversation_history` fixture provides:
- Basic user and agent message exchange
- Proper message format for testing

### Sample Combined Input

The `sample_combined_input` fixture provides:
- Complete workflow input with agent goal and tool params
- Conversation summary and prompt queue
- Ready for workflow execution

## Debugging Tests

### Verbose Logging

Enable detailed logging:
```bash
uv run pytest --log-cli-level=DEBUG -s
```

### Temporal Web UI

When using local environment, access Temporal Web UI at http://localhost:8233 to inspect workflow executions during tests.

### Test Isolation

Each test uses unique task queue names to prevent interference:
```python
task_queue_name = str(uuid.uuid4())
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - run: uv run pytest --workflow-environment=time-skipping
```

### Test Coverage

Generate coverage reports:
```bash
uv add --group dev pytest-cov
uv run pytest --cov=workflows --cov=activities --cov-report=html
```

## Best Practices

1. **Mock External Dependencies**: Always mock LLM calls, file I/O, and network requests
2. **Use Time-Skipping**: For CI/CD, prefer time-skipping environment for speed
3. **Unique Identifiers**: Use UUIDs for workflow IDs and task queues
4. **Clean Shutdown**: Always end workflows properly in tests
5. **Descriptive Names**: Use clear, descriptive test names
6. **Test Edge Cases**: Include error scenarios and validation failures
7. **Keep Tests Fast**: Use mocks to avoid slow external calls
8. **Isolate Tests**: Ensure tests don't depend on each other

## Troubleshooting

### Common Issues

1. **Workflow Timeout**: Increase timeouts or use time-skipping environment
2. **Mock Not Working**: Check patch decorators and import paths
3. **Test Hanging**: Ensure workflows are properly ended with signals
4. **Environment Issues**: Check environment variable settings

### Getting Help

- Check Temporal Python SDK documentation
- Review existing test patterns in the codebase
- Use `uv run pytest --collect-only` to verify test discovery
- Run with `-v` flag for detailed output

## Legacy Tests

The `workflowtests/` directory contains legacy tests. New tests should be added to the main `tests/` directory following the patterns established in this guide.


================================================
FILE: tests/__init__.py
================================================
[Empty file]


================================================
FILE: tests/conftest.py
================================================
import asyncio
import multiprocessing
import sys
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from temporalio.client import Client
from temporalio.testing import WorkflowEnvironment

# Due to https://github.com/python/cpython/issues/77906, multiprocessing on
# macOS starting with Python 3.8 has changed from "fork" to "spawn". For
# pre-3.8, we are changing it for them.
if sys.version_info < (3, 8) and sys.platform.startswith("darwin"):
    multiprocessing.set_start_method("spawn", True)


def pytest_addoption(parser):
    parser.addoption(
        "--workflow-environment",
        default="local",
        help="Which workflow environment to use ('local', 'time-skipping', or target to existing server)",
    )


@pytest.fixture(scope="session")
def event_loop():
    # See https://github.com/pytest-dev/pytest-asyncio/issues/68
    # See https://github.com/pytest-dev/pytest-asyncio/issues/257
    # Also need ProactorEventLoop on older versions of Python with Windows so
    # that asyncio subprocess works properly
    if sys.version_info < (3, 8) and sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
    else:
        loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def env(request) -> AsyncGenerator[WorkflowEnvironment, None]:
    env_type = request.config.getoption("--workflow-environment")
    if env_type == "local":
        env = await WorkflowEnvironment.start_local(
            dev_server_extra_args=[
                "--dynamic-config-value",
                "frontend.enableExecuteMultiOperation=true",
            ]
        )
    elif env_type == "time-skipping":
        env = await WorkflowEnvironment.start_time_skipping()
    else:
        env = WorkflowEnvironment.from_client(await Client.connect(env_type))
    yield env
    await env.shutdown()


@pytest_asyncio.fixture
async def client(env: WorkflowEnvironment) -> Client:
    return env.client


@pytest.fixture
def sample_agent_goal():
    """Sample agent goal for testing."""
    from models.tool_definitions import AgentGoal, ToolArgument, ToolDefinition

    return AgentGoal(
        id="test_goal",
        category_tag="test",
        agent_name="TestAgent",
        agent_friendly_description="A test agent for testing purposes",
        description="Test goal for agent testing",
        tools=[
            ToolDefinition(
                name="TestTool",
                description="A test tool for testing purposes",
                arguments=[
                    ToolArgument(
                        name="test_arg", type="string", description="A test argument"
                    )
                ],
            )
        ],
    )


@pytest.fixture
def sample_conversation_history():
    """Sample conversation history for testing."""
    return {
        "messages": [
            {"actor": "user", "response": "Hello, I need help with testing"},
            {"actor": "agent", "response": "I can help you with that"},
        ]
    }


@pytest.fixture
def sample_combined_input(sample_agent_goal):
    """Sample combined input for workflow testing."""
    from collections import deque

    from models.data_types import AgentGoalWorkflowParams, CombinedInput

    tool_params = AgentGoalWorkflowParams(
        conversation_summary="Test conversation summary",
        prompt_queue=deque(),  # Start with empty queue for most tests
    )

    return CombinedInput(agent_goal=sample_agent_goal, tool_params=tool_params)



================================================
FILE: tests/test_agent_goal_workflow.py
================================================
import uuid

from temporalio import activity
from temporalio.client import Client
from temporalio.worker import Worker

from models.data_types import (
    AgentGoalWorkflowParams,
    CombinedInput,
    EnvLookupInput,
    EnvLookupOutput,
    ToolPromptInput,
    ValidationInput,
    ValidationResult,
)
from workflows.agent_goal_workflow import AgentGoalWorkflow


class TestAgentGoalWorkflow:
    """Test cases for AgentGoalWorkflow."""

    async def test_workflow_initialization(
        self, client: Client, sample_combined_input: CombinedInput
    ):
        """Test workflow can be initialized and started."""
        task_queue_name = str(uuid.uuid4())

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[mock_get_wf_env_vars],
        ):
            # Start workflow but don't wait for completion since it runs indefinitely
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                sample_combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Verify workflow is running
            assert handle is not None

            # Query the workflow to check initial state
            conversation_history = await handle.query(
                AgentGoalWorkflow.get_conversation_history
            )
            assert isinstance(conversation_history, dict)
            assert "messages" in conversation_history

            # Test goal query
            agent_goal = await handle.query(AgentGoalWorkflow.get_agent_goal)
            assert agent_goal == sample_combined_input.agent_goal

            # End the workflow
            await handle.signal(AgentGoalWorkflow.end_chat)
            result = await handle.result()
            assert isinstance(result, str)

    async def test_user_prompt_signal(
        self, client: Client, sample_combined_input: CombinedInput
    ):
        """Test user_prompt signal handling."""
        task_queue_name = str(uuid.uuid4())

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        @activity.defn(name="agent_validatePrompt")
        async def mock_agent_validatePrompt(
            validation_input: ValidationInput,
        ) -> ValidationResult:
            return ValidationResult(validationResult=True, validationFailedReason={})

        @activity.defn(name="agent_toolPlanner")
        async def mock_agent_toolPlanner(input: ToolPromptInput) -> dict:
            return {"next": "done", "response": "Test response from LLM"}

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[
                mock_get_wf_env_vars,
                mock_agent_validatePrompt,
                mock_agent_toolPlanner,
            ],
        ):
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                sample_combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Send user prompt
            await handle.signal(
                AgentGoalWorkflow.user_prompt, "Hello, this is a test message"
            )

            # Wait for workflow to complete (it should end due to "done" next step)
            result = await handle.result()
            assert isinstance(result, str)

            # Verify the conversation includes our message
            import json

            try:
                conversation_history = json.loads(result.replace("'", '"'))
            except Exception:
                # Fallback to eval if json fails
                conversation_history = eval(result)
            messages = conversation_history["messages"]

            # Should have our user message and agent response
            user_messages = [msg for msg in messages if msg["actor"] == "user"]
            assert len(user_messages) > 0
            assert any(
                "Hello, this is a test message" in str(msg["response"])
                for msg in user_messages
            )

    async def test_confirm_signal(
        self, client: Client, sample_combined_input: CombinedInput
    ):
        """Test confirm signal handling for tool execution."""
        task_queue_name = str(uuid.uuid4())

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        @activity.defn(name="agent_validatePrompt")
        async def mock_agent_validatePrompt(
            validation_input: ValidationInput,
        ) -> ValidationResult:
            return ValidationResult(validationResult=True, validationFailedReason={})

        @activity.defn(name="agent_toolPlanner")
        async def mock_agent_toolPlanner(input: ToolPromptInput) -> dict:
            return {
                "next": "confirm",
                "tool": "TestTool",
                "args": {"test_arg": "test_value"},
                "response": "Ready to execute tool",
            }

        @activity.defn(name="TestTool")
        async def mock_test_tool(args: dict) -> dict:
            return {"result": "Test tool executed successfully"}

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[
                mock_get_wf_env_vars,
                mock_agent_validatePrompt,
                mock_agent_toolPlanner,
                mock_test_tool,
            ],
        ):
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                sample_combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Send user prompt that will require confirmation
            await handle.signal(AgentGoalWorkflow.user_prompt, "Execute the test tool")

            # Query to check tool data is set
            import asyncio

            await asyncio.sleep(0.1)  # Give workflow time to process

            tool_data = await handle.query(AgentGoalWorkflow.get_latest_tool_data)
            if tool_data:
                assert tool_data.get("tool") == "TestTool"
                assert tool_data.get("next") == "confirm"

            # Send confirmation and end chat
            await handle.signal(AgentGoalWorkflow.confirm)
            await handle.signal(AgentGoalWorkflow.end_chat)

            result = await handle.result()
            assert isinstance(result, str)

    async def test_validation_failure(
        self, client: Client, sample_combined_input: CombinedInput
    ):
        """Test workflow handles validation failures correctly."""
        task_queue_name = str(uuid.uuid4())

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        @activity.defn(name="agent_validatePrompt")
        async def mock_agent_validatePrompt(
            validation_input: ValidationInput,
        ) -> ValidationResult:
            return ValidationResult(
                validationResult=False,
                validationFailedReason={
                    "next": "question",
                    "response": "Your request doesn't make sense in this context",
                },
            )

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[mock_get_wf_env_vars, mock_agent_validatePrompt],
        ):
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                sample_combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Send invalid prompt
            await handle.signal(
                AgentGoalWorkflow.user_prompt, "Invalid nonsensical prompt"
            )

            # Give workflow time to process the prompt
            import asyncio

            await asyncio.sleep(0.2)

            # End workflow to check conversation
            await handle.signal(AgentGoalWorkflow.end_chat)
            result = await handle.result()

            # Verify validation failure message was added
            import json

            try:
                conversation_history = json.loads(result.replace("'", '"'))
            except Exception:
                # Fallback to eval if json fails
                conversation_history = eval(result)
            messages = conversation_history["messages"]

            # Should have validation failure response
            agent_messages = [msg for msg in messages if msg["actor"] == "agent"]
            assert len(agent_messages) > 0
            assert any(
                "doesn't make sense" in str(msg["response"]) for msg in agent_messages
            )

    async def test_conversation_summary_initialization(
        self, client: Client, sample_agent_goal
    ):
        """Test workflow initializes with conversation summary."""
        task_queue_name = str(uuid.uuid4())

        # Create input with conversation summary
        from collections import deque

        tool_params = AgentGoalWorkflowParams(
            conversation_summary="Previous conversation summary", prompt_queue=deque()
        )
        combined_input = CombinedInput(
            agent_goal=sample_agent_goal, tool_params=tool_params
        )

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[mock_get_wf_env_vars],
        ):
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Give workflow time to initialize
            import asyncio

            await asyncio.sleep(0.1)

            # Query conversation summary
            summary = await handle.query(AgentGoalWorkflow.get_summary_from_history)
            assert summary == "Previous conversation summary"

            # Query conversation history - should include summary message
            conversation_history = await handle.query(
                AgentGoalWorkflow.get_conversation_history
            )
            messages = conversation_history["messages"]

            # Should have conversation_summary message
            summary_messages = [
                msg for msg in messages if msg["actor"] == "conversation_summary"
            ]
            assert len(summary_messages) == 1
            assert summary_messages[0]["response"] == "Previous conversation summary"

            # End workflow
            await handle.signal(AgentGoalWorkflow.end_chat)
            await handle.result()

    async def test_workflow_queries(
        self, client: Client, sample_combined_input: CombinedInput
    ):
        """Test all workflow query methods."""
        task_queue_name = str(uuid.uuid4())

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[mock_get_wf_env_vars],
        ):
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                sample_combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Give workflow time to initialize
            import asyncio

            await asyncio.sleep(0.1)

            # Test get_conversation_history query
            conversation_history = await handle.query(
                AgentGoalWorkflow.get_conversation_history
            )
            assert isinstance(conversation_history, dict)
            assert "messages" in conversation_history

            # Test get_agent_goal query
            agent_goal = await handle.query(AgentGoalWorkflow.get_agent_goal)
            assert agent_goal.id == sample_combined_input.agent_goal.id

            # Test get_summary_from_history query
            summary = await handle.query(AgentGoalWorkflow.get_summary_from_history)
            # Summary might be None if not set, so check for that
            if sample_combined_input.tool_params.conversation_summary:
                assert summary == sample_combined_input.tool_params.conversation_summary
            else:
                assert summary is None

            # Test get_latest_tool_data query (should be None initially)
            tool_data = await handle.query(AgentGoalWorkflow.get_latest_tool_data)
            assert tool_data is None

            # End workflow
            await handle.signal(AgentGoalWorkflow.end_chat)
            await handle.result()

    async def test_enable_disable_debugging_confirm_signals(
        self, client: Client, sample_combined_input: CombinedInput
    ):
        """Test debugging confirm enable/disable signals."""
        task_queue_name = str(uuid.uuid4())

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[mock_get_wf_env_vars],
        ):
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                sample_combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Test enable debugging confirm signal
            await handle.signal(AgentGoalWorkflow.enable_debugging_confirm)

            # Test disable debugging confirm signal
            await handle.signal(AgentGoalWorkflow.disable_debugging_confirm)

            # End workflow
            await handle.signal(AgentGoalWorkflow.end_chat)
            result = await handle.result()
            assert isinstance(result, str)

    async def test_workflow_with_empty_prompt_queue(
        self, client: Client, sample_agent_goal
    ):
        """Test workflow behavior with empty prompt queue."""
        task_queue_name = str(uuid.uuid4())

        # Create input with empty prompt queue
        from collections import deque

        tool_params = AgentGoalWorkflowParams(
            conversation_summary=None, prompt_queue=deque()
        )
        combined_input = CombinedInput(
            agent_goal=sample_agent_goal, tool_params=tool_params
        )

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[mock_get_wf_env_vars],
        ):
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Give workflow time to initialize
            import asyncio

            await asyncio.sleep(0.1)

            # Query initial state
            conversation_history = await handle.query(
                AgentGoalWorkflow.get_conversation_history
            )
            assert isinstance(conversation_history, dict)
            assert "messages" in conversation_history

            # Should have no messages initially (empty prompt queue, no summary)
            messages = conversation_history["messages"]
            assert len(messages) == 0

            # End workflow
            await handle.signal(AgentGoalWorkflow.end_chat)
            result = await handle.result()
            assert isinstance(result, str)

    async def test_multiple_user_prompts(
        self, client: Client, sample_combined_input: CombinedInput
    ):
        """Test workflow handling multiple user prompts in sequence."""
        task_queue_name = str(uuid.uuid4())

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        @activity.defn(name="agent_validatePrompt")
        async def mock_agent_validatePrompt(
            validation_input: ValidationInput,
        ) -> ValidationResult:
            return ValidationResult(validationResult=True, validationFailedReason={})

        @activity.defn(name="agent_toolPlanner")
        async def mock_agent_toolPlanner(input: ToolPromptInput) -> dict:
            # Keep workflow running for multiple prompts
            return {"next": "question", "response": f"Processed: {input.prompt}"}

        async with Worker(
            client,
            task_queue=task_queue_name,
            workflows=[AgentGoalWorkflow],
            activities=[
                mock_get_wf_env_vars,
                mock_agent_validatePrompt,
                mock_agent_toolPlanner,
            ],
        ):
            handle = await client.start_workflow(
                AgentGoalWorkflow.run,
                sample_combined_input,
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )

            # Send multiple prompts
            await handle.signal(AgentGoalWorkflow.user_prompt, "First message")
            import asyncio

            await asyncio.sleep(0.1)

            await handle.signal(AgentGoalWorkflow.user_prompt, "Second message")
            await asyncio.sleep(0.1)

            await handle.signal(AgentGoalWorkflow.user_prompt, "Third message")
            await asyncio.sleep(0.1)

            # End workflow
            await handle.signal(AgentGoalWorkflow.end_chat)
            result = await handle.result()
            assert isinstance(result, str)

            # Parse result and verify multiple messages
            import json

            try:
                conversation_history = json.loads(result.replace("'", '"'))
            except Exception:
                conversation_history = eval(result)
            messages = conversation_history["messages"]

            # Should have at least one user message (timing dependent)
            user_messages = [msg for msg in messages if msg["actor"] == "user"]
            assert len(user_messages) >= 1

            # Verify at least the first message was processed
            message_texts = [str(msg["response"]) for msg in user_messages]
            assert any("First message" in text for text in message_texts)



================================================
FILE: tests/test_mcp_integration.py
================================================
import asyncio
import uuid
from collections import deque
from typing import Sequence
from unittest.mock import patch

import pytest
from temporalio import activity
from temporalio.client import Client
from temporalio.common import RawValue
from temporalio.testing import ActivityEnvironment
from temporalio.worker import Worker

from activities.tool_activities import _convert_args_types, mcp_list_tools
from models.data_types import (
    AgentGoalWorkflowParams,
    CombinedInput,
    EnvLookupInput,
    EnvLookupOutput,
    ToolPromptInput,
    ValidationInput,
    ValidationResult,
)
from models.tool_definitions import AgentGoal, MCPServerDefinition, ToolDefinition
from workflows.agent_goal_workflow import AgentGoalWorkflow
from workflows.workflow_helpers import is_mcp_tool


class DummySession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def initialize(self):
        pass

    async def list_tools(self):
        class Tool:
            def __init__(self, name):
                self.name = name
                self.description = f"desc {name}"
                self.inputSchema = {}

        return type(
            "Resp", (), {"tools": [Tool("list_products"), Tool("create_customer")]}
        )()


def test_convert_args_types_basic():
    args = {
        "count": "5",
        "price": "12.5",
        "flag_true": "true",
        "flag_false": "false",
        "name": "pizza",
        "already_int": 2,
    }
    result = _convert_args_types(args)
    assert result["count"] == 5 and isinstance(result["count"], int)
    assert result["price"] == 12.5 and isinstance(result["price"], float)
    assert result["flag_true"] is True
    assert result["flag_false"] is False
    assert result["name"] == "pizza"
    assert result["already_int"] == 2


def test_is_mcp_tool_identification():
    server_def = MCPServerDefinition(name="test", command="python", args=["server.py"])
    goal = AgentGoal(
        id="g",
        category_tag="food",
        agent_name="agent",
        agent_friendly_description="",
        description="",
        tools=[ToolDefinition(name="AddToCart", description="", arguments=[])],
        starter_prompt="",
        example_conversation_history="",
        mcp_server_definition=server_def,
    )

    assert is_mcp_tool("list_products", goal) is True
    assert is_mcp_tool("AddToCart", goal) is False
    no_mcp_goal = AgentGoal(
        id="g2",
        category_tag="food",
        agent_name="agent",
        agent_friendly_description="",
        description="",
        tools=[],
        starter_prompt="",
        example_conversation_history="",
        mcp_server_definition=None,
    )
    assert is_mcp_tool("list_products", no_mcp_goal) is False


@pytest.mark.asyncio
async def test_mcp_list_tools_success():
    server_def = MCPServerDefinition(name="test", command="python", args=["server.py"])

    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def dummy_connection(command, args, env):
        yield None, None

    with patch(
        "activities.tool_activities._build_connection", return_value={"type": "stdio"}
    ), patch("activities.tool_activities._stdio_connection", dummy_connection), patch(
        "activities.tool_activities.ClientSession", lambda r, w: DummySession()
    ):
        activity_env = ActivityEnvironment()
        result = await activity_env.run(mcp_list_tools, server_def, ["list_products"])
        assert result["success"] is True
        assert result["filtered_count"] == 1
        assert "list_products" in result["tools"]


@pytest.mark.asyncio
async def test_mcp_list_tools_failure():
    server_def = MCPServerDefinition(name="test", command="python", args=["server.py"])

    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def failing_connection(*args, **kwargs):
        raise RuntimeError("conn fail")
        yield None, None

    with patch(
        "activities.tool_activities._build_connection", return_value={"type": "stdio"}
    ), patch("activities.tool_activities._stdio_connection", failing_connection):
        activity_env = ActivityEnvironment()
        result = await activity_env.run(mcp_list_tools, server_def)
        assert result["success"] is False
        assert "conn fail" in result["error"]


@pytest.mark.asyncio
async def test_workflow_loads_mcp_tools_dynamically(client: Client):
    """Workflow should load MCP tools and add them to the goal."""
    task_queue_name = str(uuid.uuid4())
    server_def = MCPServerDefinition(name="test", command="python", args=["srv.py"])
    goal = AgentGoal(
        id="g_mcp",
        category_tag="food",
        agent_name="agent",
        agent_friendly_description="",
        description="",
        tools=[],
        starter_prompt="",
        example_conversation_history="",
        mcp_server_definition=server_def,
    )
    combined_input = CombinedInput(
        agent_goal=goal,
        tool_params=AgentGoalWorkflowParams(
            conversation_summary=None, prompt_queue=deque()
        ),
    )

    @activity.defn(name="get_wf_env_vars")
    async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
        return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

    @activity.defn(name="mcp_list_tools")
    async def mock_mcp_list_tools(
        server_definition: MCPServerDefinition, include_tools=None
    ):
        return {
            "server_name": server_definition.name,
            "success": True,
            "tools": {
                "list_products": {
                    "name": "list_products",
                    "description": "",
                    "inputSchema": {},
                },
            },
            "total_available": 1,
            "filtered_count": 1,
        }

    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[AgentGoalWorkflow],
        activities=[mock_get_wf_env_vars, mock_mcp_list_tools],
    ):
        handle = await client.start_workflow(
            AgentGoalWorkflow.run,
            combined_input,
            id=str(uuid.uuid4()),
            task_queue=task_queue_name,
        )

        # Wait until the MCP tools have been added
        for _ in range(10):
            updated_goal = await handle.query(AgentGoalWorkflow.get_agent_goal)
            if any(t.name == "list_products" for t in updated_goal.tools):
                break
            await asyncio.sleep(0.1)
        else:
            updated_goal = await handle.query(AgentGoalWorkflow.get_agent_goal)

        assert any(t.name == "list_products" for t in updated_goal.tools)

        await handle.signal(AgentGoalWorkflow.end_chat)
        await handle.result()


@pytest.mark.asyncio
async def test_mcp_tool_execution_flow(client: Client):
    """MCP tool execution should pass server_definition to activity."""
    task_queue_name = str(uuid.uuid4())
    server_def = MCPServerDefinition(name="test", command="python", args=["srv.py"])
    goal = AgentGoal(
        id="g_mcp_exec",
        category_tag="food",
        agent_name="agent",
        agent_friendly_description="",
        description="",
        tools=[],
        starter_prompt="",
        example_conversation_history="",
        mcp_server_definition=server_def,
    )
    combined_input = CombinedInput(
        agent_goal=goal,
        tool_params=AgentGoalWorkflowParams(
            conversation_summary=None, prompt_queue=deque()
        ),
    )

    captured: dict = {}

    @activity.defn(name="get_wf_env_vars")
    async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
        return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

    @activity.defn(name="agent_validatePrompt")
    async def mock_validate(prompt: ValidationInput) -> ValidationResult:
        return ValidationResult(validationResult=True, validationFailedReason={})

    @activity.defn(name="agent_toolPlanner")
    async def mock_planner(input: ToolPromptInput) -> dict:
        if "planner_called" not in captured:
            captured["planner_called"] = True
            return {
                "next": "confirm",
                "tool": "list_products",
                "args": {"limit": "5"},
                "response": "Listing products",
            }
        return {"next": "done", "response": "done"}

    @activity.defn(name="mcp_list_tools")
    async def mock_mcp_list_tools(
        server_definition: MCPServerDefinition, include_tools=None
    ):
        return {
            "server_name": server_definition.name,
            "success": True,
            "tools": {
                "list_products": {
                    "name": "list_products",
                    "description": "",
                    "inputSchema": {},
                },
            },
            "total_available": 1,
            "filtered_count": 1,
        }

    @activity.defn(name="dynamic_tool_activity", dynamic=True)
    async def mock_dynamic_tool_activity(args: Sequence[RawValue]) -> dict:
        payload = activity.payload_converter().from_payload(args[0].payload, dict)
        captured["dynamic_args"] = payload
        return {"tool": "list_products", "success": True, "content": {"ok": True}}

    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[AgentGoalWorkflow],
        activities=[
            mock_get_wf_env_vars,
            mock_validate,
            mock_planner,
            mock_mcp_list_tools,
            mock_dynamic_tool_activity,
        ],
    ):
        handle = await client.start_workflow(
            AgentGoalWorkflow.run,
            combined_input,
            id=str(uuid.uuid4()),
            task_queue=task_queue_name,
        )

        await handle.signal(AgentGoalWorkflow.user_prompt, "show menu")
        await asyncio.sleep(0.5)
        await handle.signal(AgentGoalWorkflow.confirm)
        # Give workflow time to execute the MCP tool and finish
        await asyncio.sleep(0.5)
        result = await handle.result()
        print(result)

    assert "dynamic_args" in captured
    assert "server_definition" in captured["dynamic_args"]
    assert captured["dynamic_args"]["server_definition"]["name"] == server_def.name


@pytest.mark.asyncio
async def test_mcp_tool_failure_recorded(client: Client):
    """Failure of an MCP tool should be recorded in conversation history."""
    task_queue_name = str(uuid.uuid4())
    server_def = MCPServerDefinition(name="test", command="python", args=["srv.py"])
    goal = AgentGoal(
        id="g_mcp_fail",
        category_tag="food",
        agent_name="agent",
        agent_friendly_description="",
        description="",
        tools=[],
        starter_prompt="",
        example_conversation_history="",
        mcp_server_definition=server_def,
    )
    combined_input = CombinedInput(
        agent_goal=goal,
        tool_params=AgentGoalWorkflowParams(
            conversation_summary=None, prompt_queue=deque()
        ),
    )

    @activity.defn(name="get_wf_env_vars")
    async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
        return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

    @activity.defn(name="agent_validatePrompt")
    async def mock_validate(prompt: ValidationInput) -> ValidationResult:
        return ValidationResult(validationResult=True, validationFailedReason={})

    @activity.defn(name="agent_toolPlanner")
    async def mock_planner(input: ToolPromptInput) -> dict:
        return {
            "next": "confirm",
            "tool": "list_products",
            "args": {},
            "response": "Listing products",
        }

    @activity.defn(name="mcp_list_tools")
    async def mock_mcp_list_tools(
        server_definition: MCPServerDefinition, include_tools=None
    ):
        return {
            "server_name": server_definition.name,
            "success": True,
            "tools": {
                "list_products": {
                    "name": "list_products",
                    "description": "",
                    "inputSchema": {},
                },
            },
            "total_available": 1,
            "filtered_count": 1,
        }

    @activity.defn(name="dynamic_tool_activity", dynamic=True)
    async def failing_dynamic_tool(args: Sequence[RawValue]) -> dict:
        return {
            "tool": "list_products",
            "success": False,
            "error": "Connection timed out",
        }

    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[AgentGoalWorkflow],
        activities=[
            mock_get_wf_env_vars,
            mock_validate,
            mock_planner,
            mock_mcp_list_tools,
            failing_dynamic_tool,
        ],
    ):
        handle = await client.start_workflow(
            AgentGoalWorkflow.run,
            combined_input,
            id=str(uuid.uuid4()),
            task_queue=task_queue_name,
        )

        await handle.signal(AgentGoalWorkflow.user_prompt, "show menu")
        await asyncio.sleep(0.5)
        await handle.signal(AgentGoalWorkflow.confirm)
        # Give workflow time to record the failure result
        await asyncio.sleep(0.5)
        await handle.signal(AgentGoalWorkflow.end_chat)
        result = await handle.result()

    import json

    try:
        history = json.loads(result.replace("'", '"'))
    except Exception:
        history = eval(result)

    assert any(
        msg["actor"] == "tool_result" and not msg["response"].get("success", True)
        for msg in history["messages"]
    )



================================================
FILE: tests/test_tool_activities.py
================================================
import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from temporalio.client import Client
from temporalio.testing import ActivityEnvironment

from activities.tool_activities import (
    MCPServerDefinition,
    ToolActivities,
    dynamic_tool_activity,
)
from models.data_types import (
    EnvLookupInput,
    EnvLookupOutput,
    ToolPromptInput,
    ValidationInput,
    ValidationResult,
)


class TestToolActivities:
    """Test cases for ToolActivities."""

    def setup_method(self):
        """Set up test environment for each test."""
        self.tool_activities = ToolActivities()

    @pytest.mark.asyncio
    async def test_agent_validatePrompt_valid_prompt(
        self, sample_agent_goal, sample_conversation_history
    ):
        """Test agent_validatePrompt with a valid prompt."""
        validation_input = ValidationInput(
            prompt="I need help with the test tool",
            conversation_history=sample_conversation_history,
            agent_goal=sample_agent_goal,
        )

        # Mock the agent_toolPlanner to return a valid response
        mock_response = {"validationResult": True, "validationFailedReason": {}}

        with patch.object(
            self.tool_activities, "agent_toolPlanner", new_callable=AsyncMock
        ) as mock_planner:
            mock_planner.return_value = mock_response

            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.agent_validatePrompt, validation_input
            )

            assert isinstance(result, ValidationResult)
            assert result.validationResult is True
            assert result.validationFailedReason == {}

            # Verify the mock was called with correct parameters
            mock_planner.assert_called_once()

    @pytest.mark.asyncio
    async def test_agent_validatePrompt_invalid_prompt(
        self, sample_agent_goal, sample_conversation_history
    ):
        """Test agent_validatePrompt with an invalid prompt."""
        validation_input = ValidationInput(
            prompt="asdfghjkl nonsense",
            conversation_history=sample_conversation_history,
            agent_goal=sample_agent_goal,
        )

        # Mock the agent_toolPlanner to return an invalid response
        mock_response = {
            "validationResult": False,
            "validationFailedReason": {
                "next": "question",
                "response": "Your request doesn't make sense in this context",
            },
        }

        with patch.object(
            self.tool_activities, "agent_toolPlanner", new_callable=AsyncMock
        ) as mock_planner:
            mock_planner.return_value = mock_response

            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.agent_validatePrompt, validation_input
            )

            assert isinstance(result, ValidationResult)
            assert result.validationResult is False
            assert "doesn't make sense" in str(result.validationFailedReason)

    @pytest.mark.asyncio
    async def test_agent_toolPlanner_success(self):
        """Test agent_toolPlanner with successful LLM response."""
        prompt_input = ToolPromptInput(
            prompt="Test prompt", context_instructions="Test context instructions"
        )

        # Mock the completion function
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = (
            '{"next": "confirm", "tool": "TestTool", "response": "Test response"}'
        )

        with patch("activities.tool_activities.completion") as mock_completion:
            mock_completion.return_value = mock_response

            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.agent_toolPlanner, prompt_input
            )

            assert isinstance(result, dict)
            assert result["next"] == "confirm"
            assert result["tool"] == "TestTool"
            assert result["response"] == "Test response"

            # Verify completion was called with correct parameters
            mock_completion.assert_called_once()
            call_args = mock_completion.call_args[1]
            assert call_args["model"] == self.tool_activities.llm_model
            assert len(call_args["messages"]) == 2
            assert call_args["messages"][0]["role"] == "system"
            assert call_args["messages"][1]["role"] == "user"

    @pytest.mark.asyncio
    async def test_agent_toolPlanner_with_custom_base_url(self):
        """Test agent_toolPlanner with custom base URL configuration."""
        # Set up tool activities with custom base URL
        with patch.dict(os.environ, {"LLM_BASE_URL": "https://custom.endpoint.com"}):
            tool_activities = ToolActivities()

            prompt_input = ToolPromptInput(
                prompt="Test prompt", context_instructions="Test context instructions"
            )

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[
                0
            ].message.content = '{"next": "done", "response": "Test"}'

            with patch("activities.tool_activities.completion") as mock_completion:
                mock_completion.return_value = mock_response

                activity_env = ActivityEnvironment()
                await activity_env.run(tool_activities.agent_toolPlanner, prompt_input)

                # Verify base_url was included in the call
                call_args = mock_completion.call_args[1]
                assert "base_url" in call_args
                assert call_args["base_url"] == "https://custom.endpoint.com"

    @pytest.mark.asyncio
    async def test_agent_toolPlanner_json_parsing_error(self):
        """Test agent_toolPlanner handles JSON parsing errors."""
        prompt_input = ToolPromptInput(
            prompt="Test prompt", context_instructions="Test context instructions"
        )

        # Mock the completion function to return invalid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Invalid JSON response"

        with patch("activities.tool_activities.completion") as mock_completion:
            mock_completion.return_value = mock_response

            activity_env = ActivityEnvironment()
            with pytest.raises(Exception):  # Should raise JSON parsing error
                await activity_env.run(
                    self.tool_activities.agent_toolPlanner, prompt_input
                )

    @pytest.mark.asyncio
    async def test_get_wf_env_vars_default_values(self):
        """Test get_wf_env_vars with default values."""
        env_input = EnvLookupInput(
            show_confirm_env_var_name="SHOW_CONFIRM", show_confirm_default=True
        )

        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.get_wf_env_vars, env_input
            )

            assert isinstance(result, EnvLookupOutput)
            assert result.show_confirm is True  # default value
            assert result.multi_goal_mode is False  # default value (single agent mode)

    @pytest.mark.asyncio
    async def test_get_wf_env_vars_custom_values(self):
        """Test get_wf_env_vars with custom environment values."""
        env_input = EnvLookupInput(
            show_confirm_env_var_name="SHOW_CONFIRM", show_confirm_default=True
        )

        # Set environment variables
        with patch.dict(
            os.environ, {"SHOW_CONFIRM": "false", "AGENT_GOAL": "specific_goal"}
        ):
            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.get_wf_env_vars, env_input
            )

            assert isinstance(result, EnvLookupOutput)
            assert result.show_confirm is False  # from env var
            assert result.multi_goal_mode is False  # from env var

    def test_sanitize_json_response(self):
        """Test JSON response sanitization."""
        # Test with markdown code blocks
        response_with_markdown = '```json\n{"test": "value"}\n```'
        sanitized = self.tool_activities.sanitize_json_response(response_with_markdown)
        assert sanitized == '{"test": "value"}'

        # Test with extra whitespace
        response_with_whitespace = '  \n{"test": "value"}  \n'
        sanitized = self.tool_activities.sanitize_json_response(
            response_with_whitespace
        )
        assert sanitized == '{"test": "value"}'

    def test_parse_json_response_success(self):
        """Test successful JSON parsing."""
        json_string = '{"next": "confirm", "tool": "TestTool"}'
        result = self.tool_activities.parse_json_response(json_string)

        assert isinstance(result, dict)
        assert result["next"] == "confirm"
        assert result["tool"] == "TestTool"

    def test_parse_json_response_failure(self):
        """Test JSON parsing with invalid JSON."""
        invalid_json = "Not valid JSON"

        with pytest.raises(Exception):  # Should raise JSON parsing error
            self.tool_activities.parse_json_response(invalid_json)


class TestDynamicToolActivity:
    """Test cases for dynamic_tool_activity."""

    @pytest.mark.asyncio
    async def test_dynamic_tool_activity_sync_handler(self):
        """Test dynamic tool activity with synchronous handler."""
        # Mock the activity info and payload converter
        mock_info = MagicMock()
        mock_info.activity_type = "TestTool"

        mock_payload_converter = MagicMock()
        mock_payload = MagicMock()
        mock_payload.payload = b'{"test_arg": "test_value"}'
        mock_payload_converter.from_payload.return_value = {"test_arg": "test_value"}

        # Mock the handler function
        def mock_handler(args):
            return {"result": f"Handled {args['test_arg']}"}

        with patch("temporalio.activity.info", return_value=mock_info), patch(
            "temporalio.activity.payload_converter", return_value=mock_payload_converter
        ), patch("tools.get_handler", return_value=mock_handler):
            activity_env = ActivityEnvironment()
            result = await activity_env.run(dynamic_tool_activity, [mock_payload])

            assert isinstance(result, dict)
            assert result["result"] == "Handled test_value"

    @pytest.mark.asyncio
    async def test_dynamic_tool_activity_async_handler(self):
        """Test dynamic tool activity with asynchronous handler."""
        # Mock the activity info and payload converter
        mock_info = MagicMock()
        mock_info.activity_type = "AsyncTestTool"

        mock_payload_converter = MagicMock()
        mock_payload = MagicMock()
        mock_payload.payload = b'{"test_arg": "async_test"}'
        mock_payload_converter.from_payload.return_value = {"test_arg": "async_test"}

        # Mock the async handler function
        async def mock_async_handler(args):
            return {"async_result": f"Async handled {args['test_arg']}"}

        with patch("temporalio.activity.info", return_value=mock_info), patch(
            "temporalio.activity.payload_converter", return_value=mock_payload_converter
        ), patch("tools.get_handler", return_value=mock_async_handler):
            activity_env = ActivityEnvironment()
            result = await activity_env.run(dynamic_tool_activity, [mock_payload])

            assert isinstance(result, dict)
            assert result["async_result"] == "Async handled async_test"


class TestToolActivitiesIntegration:
    """Integration tests for ToolActivities in a real Temporal environment."""

    @pytest.mark.asyncio
    async def test_activities_in_worker(self, client: Client):
        """Test activities can be registered and executed in a worker."""
        # task_queue_name = str(uuid.uuid4())
        tool_activities = ToolActivities()

        # Test get_wf_env_vars activity using ActivityEnvironment
        env_input = EnvLookupInput(
            show_confirm_env_var_name="TEST_CONFIRM", show_confirm_default=False
        )

        activity_env = ActivityEnvironment()
        result = await activity_env.run(tool_activities.get_wf_env_vars, env_input)

        assert isinstance(result, EnvLookupOutput)
        assert isinstance(result.show_confirm, bool)
        assert isinstance(result.multi_goal_mode, bool)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def setup_method(self):
        """Set up test environment for each test."""
        self.tool_activities = ToolActivities()

    @pytest.mark.asyncio
    async def test_agent_validatePrompt_with_empty_conversation_history(
        self, sample_agent_goal
    ):
        """Test validation with empty conversation history."""
        validation_input = ValidationInput(
            prompt="Test prompt",
            conversation_history={"messages": []},
            agent_goal=sample_agent_goal,
        )

        mock_response = {"validationResult": True, "validationFailedReason": {}}

        with patch.object(
            self.tool_activities, "agent_toolPlanner", new_callable=AsyncMock
        ) as mock_planner:
            mock_planner.return_value = mock_response

            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.agent_validatePrompt, validation_input
            )

            assert isinstance(result, ValidationResult)
            assert result.validationResult
            assert result.validationFailedReason == {}

    @pytest.mark.asyncio
    async def test_agent_toolPlanner_with_long_prompt(self):
        """Test toolPlanner with very long prompt."""
        long_prompt = "This is a very long prompt " * 100
        tool_prompt_input = ToolPromptInput(
            prompt=long_prompt, context_instructions="Test context instructions"
        )

        # Mock the completion response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = '{"next": "done", "response": "Processed long prompt"}'

        with patch("activities.tool_activities.completion", return_value=mock_response):
            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.agent_toolPlanner, tool_prompt_input
            )

            assert isinstance(result, dict)
            assert result["next"] == "done"
            assert "Processed long prompt" in result["response"]

    @pytest.mark.asyncio
    async def test_sanitize_json_with_various_formats(self):
        """Test JSON sanitization with various input formats."""
        # Test markdown code blocks
        markdown_json = '```json\n{"test": "value"}\n```'
        result = self.tool_activities.sanitize_json_response(markdown_json)
        assert result == '{"test": "value"}'

        # Test with extra whitespace
        whitespace_json = '   \n  {"test": "value"}  \n  '
        result = self.tool_activities.sanitize_json_response(whitespace_json)
        assert result == '{"test": "value"}'

        # Test already clean JSON
        clean_json = '{"test": "value"}'
        result = self.tool_activities.sanitize_json_response(clean_json)
        assert result == '{"test": "value"}'

    @pytest.mark.asyncio
    async def test_parse_json_response_with_invalid_json(self):
        """Test JSON parsing with invalid JSON."""
        with pytest.raises(json.JSONDecodeError):
            self.tool_activities.parse_json_response("Invalid JSON {test: value")

    @pytest.mark.asyncio
    async def test_get_wf_env_vars_with_various_env_values(self):
        """Test environment variable parsing with different values."""
        # Test with "true" string
        with patch.dict(os.environ, {"TEST_CONFIRM": "true"}):
            env_input = EnvLookupInput(
                show_confirm_env_var_name="TEST_CONFIRM", show_confirm_default=False
            )

            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.get_wf_env_vars, env_input
            )

            assert result.show_confirm

        # Test with "false" string
        with patch.dict(os.environ, {"TEST_CONFIRM": "false"}):
            env_input = EnvLookupInput(
                show_confirm_env_var_name="TEST_CONFIRM", show_confirm_default=True
            )

            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.get_wf_env_vars, env_input
            )

            assert not result.show_confirm

        # Test with missing env var (should use default)
        with patch.dict(os.environ, {}, clear=True):
            env_input = EnvLookupInput(
                show_confirm_env_var_name="MISSING_VAR", show_confirm_default=True
            )

            activity_env = ActivityEnvironment()
            result = await activity_env.run(
                self.tool_activities.get_wf_env_vars, env_input
            )

            assert result.show_confirm


class TestMCPIntegration:
    @pytest.mark.asyncio
    async def test_convert_args_types(self):
        from activities.tool_activities import _convert_args_types

        args = {
            "int_val": "123",
            "float_val": "123.45",
            "bool_true": "true",
            "bool_false": "False",
            "string": "text",
            "other": 5,
        }
        converted = _convert_args_types(args)
        assert converted["int_val"] == 123
        assert converted["float_val"] == 123.45
        assert converted["bool_true"] is True
        assert converted["bool_false"] is False
        assert converted["string"] == "text"
        assert converted["other"] == 5

    @pytest.mark.asyncio
    async def test_dynamic_tool_activity_mcp_call(self):
        mcp_def = MCPServerDefinition(
            name="stripe", command="python", args=["server.py"]
        )
        payload = MagicMock()
        payload.payload = b'{"server_definition": null, "amount": "10", "flag": "true"}'
        mock_info = MagicMock()
        mock_info.activity_type = "list_products"

        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def dummy_conn(*args, **kwargs):
            yield (None, None)

        class DummySession:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                pass

            async def initialize(self):
                pass

            async def call_tool(self, tool_name, arguments=None):
                self.called_tool = tool_name
                self.called_args = arguments
                return MagicMock(content="ok")

        mock_payload_converter = MagicMock()
        mock_payload_converter.from_payload.return_value = {
            "server_definition": mcp_def,
            "amount": "10",
            "flag": "true",
        }

        with patch("activities.tool_activities._stdio_connection", dummy_conn), patch(
            "activities.tool_activities.ClientSession", return_value=DummySession()
        ), patch(
            "activities.tool_activities._build_connection",
            return_value={
                "type": "stdio",
                "command": "python",
                "args": ["server.py"],
                "env": {},
            },
        ), patch(
            "temporalio.activity.info", return_value=mock_info
        ), patch(
            "temporalio.activity.payload_converter", return_value=mock_payload_converter
        ):
            result = await ActivityEnvironment().run(dynamic_tool_activity, [payload])

        assert result["success"] is True
        assert result["tool"] == "list_products"

    @pytest.mark.asyncio
    async def test_mcp_tool_activity_failure(self):
        tool_activities = ToolActivities()
        mcp_def = MCPServerDefinition(
            name="stripe", command="python", args=["server.py"]
        )

        async def dummy_conn(*args, **kwargs):
            from contextlib import asynccontextmanager

            @asynccontextmanager
            async def cm():
                yield (None, None)

            return cm()

        class DummySession:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                pass

            async def initialize(self):
                pass

            async def call_tool(self, tool_name, arguments=None):
                raise TypeError("boom")

        with patch("activities.tool_activities._stdio_connection", dummy_conn), patch(
            "activities.tool_activities.ClientSession", return_value=DummySession()
        ), patch(
            "activities.tool_activities._build_connection",
            return_value={
                "type": "stdio",
                "command": "python",
                "args": ["server.py"],
                "env": {},
            },
        ):
            result = await ActivityEnvironment().run(
                tool_activities.mcp_tool_activity,
                "list_products",
                {"server_definition": mcp_def, "amount": "10"},
            )

        assert result["success"] is False
        assert result["error_type"] == "TypeError"



================================================
FILE: tests/test_workflow_helpers.py
================================================
import pytest

from models.tool_definitions import (
    AgentGoal,
    MCPServerDefinition,
    ToolArgument,
    ToolDefinition,
)
from workflows.workflow_helpers import is_mcp_tool


def make_goal(with_mcp: bool) -> AgentGoal:
    tools = [ToolDefinition(name="AddToCart", description="", arguments=[])]
    mcp_def = None
    if with_mcp:
        mcp_def = MCPServerDefinition(
            name="stripe", command="python", args=["server.py"]
        )
    return AgentGoal(
        id="g",
        category_tag="test",
        agent_name="Test",
        agent_friendly_description="",
        tools=tools,
        mcp_server_definition=mcp_def,
    )


def test_is_mcp_tool_recognizes_native():
    goal = make_goal(True)
    assert not is_mcp_tool("AddToCart", goal)


def test_is_mcp_tool_recognizes_mcp():
    goal = make_goal(True)
    assert is_mcp_tool("list_products", goal)



================================================
FILE: tests/workflowtests/agent_goal_workflow_test.py
================================================
import concurrent.futures
import uuid
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Sequence

from temporalio import activity
from temporalio.client import Client, WorkflowExecutionStatus
from temporalio.common import RawValue
from temporalio.worker import Worker

from api.main import get_initial_agent_goal
from models.data_types import (
    AgentGoalWorkflowParams,
    CombinedInput,
    EnvLookupInput,
    EnvLookupOutput,
    ToolPromptInput,
    ValidationInput,
    ValidationResult,
)
from models.tool_definitions import MCPServerDefinition
from workflows.agent_goal_workflow import AgentGoalWorkflow


@contextmanager
def my_context():
    print("Setup")
    yield "some_value"  # Value assigned to 'as' variable
    print("Cleanup")


async def test_flight_booking(client: Client):
    # load_dotenv("test_flights_single.env")

    with my_context() as value:
        print(f"Working with {value}")

        # Create the test environment
        # env = await WorkflowEnvironment.start_local()
        # client = env.client
        task_queue_name = str(uuid.uuid4())
        workflow_id = str(uuid.uuid4())

        # Create mock activity functions with proper signatures
        @activity.defn(name="get_wf_env_vars")
        async def mock_get_wf_env_vars(input: EnvLookupInput) -> EnvLookupOutput:
            return EnvLookupOutput(show_confirm=True, multi_goal_mode=True)

        @activity.defn(name="agent_validatePrompt")
        async def mock_agent_validatePrompt(
            validation_input: ValidationInput,
        ) -> ValidationResult:
            return ValidationResult(validationResult=True, validationFailedReason={})

        @activity.defn(name="agent_toolPlanner")
        async def mock_agent_toolPlanner(input: ToolPromptInput) -> dict:
            return {"next": "done", "response": "Test response from LLM"}

        @activity.defn(name="mcp_list_tools")
        async def mock_mcp_list_tools(
            server_definition: MCPServerDefinition,
            include_tools: Optional[List[str]] = None,
        ) -> Dict[str, Any]:
            return {"success": True, "tools": {}, "server_name": "test"}

        @activity.defn(name="mcp_tool_activity")
        async def mock_mcp_tool_activity(
            tool_name: str, tool_args: Dict[str, Any]
        ) -> Dict[str, Any]:
            return {"success": True, "result": "Mock MCP tool result"}

        @activity.defn(name="dynamic_tool_activity", dynamic=True)
        async def mock_dynamic_tool_activity(args: Sequence[RawValue]) -> dict:
            return {"success": True, "result": "Mock dynamic tool result"}

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=100
        ) as activity_executor:
            worker = Worker(
                client,
                task_queue=task_queue_name,
                workflows=[AgentGoalWorkflow],
                activities=[
                    mock_get_wf_env_vars,
                    mock_agent_validatePrompt,
                    mock_agent_toolPlanner,
                    mock_mcp_list_tools,
                    mock_mcp_tool_activity,
                    mock_dynamic_tool_activity,
                ],
                activity_executor=activity_executor,
            )

            async with worker:
                initial_agent_goal = get_initial_agent_goal()
                # Create combined input
                combined_input = CombinedInput(
                    tool_params=AgentGoalWorkflowParams(None, None),
                    agent_goal=initial_agent_goal,
                )

                prompt = "Hello!"

                # async with Worker(client, task_queue=task_queue_name, workflows=[AgentGoalWorkflow], activities=[ToolActivities.agent_validatePrompt, ToolActivities.agent_toolPlanner, dynamic_tool_activity]):

                # todo set goal categories for scenarios
                handle = await client.start_workflow(
                    AgentGoalWorkflow.run,
                    combined_input,
                    id=workflow_id,
                    task_queue=task_queue_name,
                    start_signal="user_prompt",
                    start_signal_args=[prompt],
                )
                # todo send signals to simulate user input
                # await handle.signal(AgentGoalWorkflow.user_prompt, "book flights") # for multi-goal
                await handle.signal(
                    AgentGoalWorkflow.user_prompt, "sydney in september"
                )
                assert (
                    WorkflowExecutionStatus.RUNNING == (await handle.describe()).status
                )

                # assert ["Hello, user1", "Hello, user2"] == await handle.result()
                await handle.signal(
                    AgentGoalWorkflow.user_prompt, "I'm all set, end conversation"
                )

                # assert WorkflowExecutionStatus.COMPLETED == (await handle.describe()).status

                result = await handle.result()
                print(f"Workflow result: {result}")
                # todo dump workflow history for analysis optional
                # todo assert result is good



================================================
FILE: thirdparty/train_api.py
================================================
import json
import random
import string
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def parse_datetime(datetime_str):
    # Remove trailing 'Z' if present
    if datetime_str.endswith("Z"):
        datetime_str = datetime_str[:-1]

    formats = [
        "%Y-%m-%dT%H:%M",  # e.g. "2025-04-18T09:00"
        "%Y-%m-%dT%H:%M:%S",  # e.g. "2025-04-18T09:00:00"
        "%Y-%m-%d %H:%M:%S",  # e.g. "2025-04-18 09:00:00"
        "%Y-%m-%d",  # e.g. "2025-04-11"
    ]

    for fmt in formats:
        try:
            parsed = time.strptime(datetime_str, fmt)
            if fmt == "%Y-%m-%d":
                # Default to 9am if no time provided
                hour, minute = 9, 0
            else:
                hour, minute = parsed.tm_hour, parsed.tm_min
            return (
                parsed.tm_year,
                parsed.tm_mon,
                parsed.tm_mday,
                hour,
                minute,
            )
        except ValueError:
            continue
    return None, None, None, None, None


class TrainServer(BaseHTTPRequestHandler):
    def generate_journeys(self, origin, destination, out_datetime, ret_datetime):
        journeys = []

        # Helper to format datetime
        def format_datetime(year, month, day, hour, minute):
            return "{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}".format(
                year=year, month=month, day=day, hour=hour, minute=minute
            )

        # Generate outbound journeys
        year, month, day, hour, minute = out_datetime
        for offset in [-30, 0, 30]:
            # Calculate journey times
            adj_minutes = minute + offset
            adj_hour = hour + (adj_minutes // 60)
            adj_minute = adj_minutes % 60

            # Simple handling of day rollover
            adj_day = day + (adj_hour // 24)
            adj_hour = adj_hour % 24

            # Journey takes 2h15m-2h45m (135-165 minutes)
            duration = 135 + random.randint(0, 30)
            arr_hour = adj_hour + (duration // 60)
            arr_minute = (adj_minute + (duration % 60)) % 60
            arr_day = adj_day + (arr_hour // 24)
            arr_hour = arr_hour % 24

            journey = {
                "id": "T{}".format(random.randint(1000, 9999)),
                "type": "outbound",
                "departure": origin,
                "arrival": destination,
                "departure_time": format_datetime(
                    year, month, adj_day, adj_hour, adj_minute
                ),
                "arrival_time": format_datetime(
                    year, month, arr_day, arr_hour, arr_minute
                ),
                "price": round(30 + random.random() * 50, 2),
            }
            journeys.append(journey)

        # Generate return journeys if return datetime provided
        if ret_datetime[0] is not None:
            year, month, day, hour, minute = ret_datetime
            for offset in [-30, 0, 30]:
                adj_minutes = minute + offset
                adj_hour = hour + (adj_minutes // 60)
                adj_minute = adj_minutes % 60

                adj_day = day + (adj_hour // 24)
                adj_hour = adj_hour % 24

                # Journey takes 2h15m-2h45m (135-165 minutes)
                duration = 135 + random.randint(0, 30)
                arr_hour = adj_hour + (duration // 60)
                arr_minute = (adj_minute + (duration % 60)) % 60
                arr_day = adj_day + (arr_hour // 24)
                arr_hour = arr_hour % 24

                journey = {
                    "id": "T{}".format(random.randint(1000, 9999)),
                    "type": "return",
                    "departure": destination,
                    "arrival": origin,
                    "departure_time": format_datetime(
                        year, month, adj_day, adj_hour, adj_minute
                    ),
                    "arrival_time": format_datetime(
                        year, month, arr_day, arr_hour, arr_minute
                    ),
                    "price": round(30 + random.random() * 50, 2),
                }
                journeys.append(journey)

        return journeys

    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/api/search":
            try:
                params = parse_qs(parsed_url.query)
                origin = params.get("from", [""])[0]
                destination = params.get("to", [""])[0]
                outbound_datetime = params.get("outbound_time", [""])[0]
                return_datetime = params.get("return_time", [""])[0]

                if not origin or not destination or not outbound_datetime:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps(
                            {
                                "error": "Required parameters: 'from', 'to', and 'outbound_time'"
                            }
                        ).encode("utf-8")
                    )
                    return

                # Parse datetimes
                out_dt = parse_datetime(outbound_datetime)
                ret_dt = (
                    parse_datetime(return_datetime)
                    if return_datetime
                    else (None, None, None, None, None)
                )

                if out_dt[0] is None:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps(
                            {"error": "Invalid datetime format. Use YYYY-MM-DDTHH:MM"}
                        ).encode("utf-8")
                    )
                    return

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                journeys = self.generate_journeys(origin, destination, out_dt, ret_dt)
                response = json.dumps({"journeys": journeys})

                self.wfile.write(response.encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path.startswith("/api/book/"):
            train_ids = parsed_url.path.split("/")[-1].split(",")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            booking_ref = "BR" + "".join(
                [random.choice(string.digits) for _ in range(5)]
            )

            response = json.dumps(
                {
                    "booking_reference": booking_ref,
                    "train_ids": train_ids,
                    "status": "confirmed",
                }
            )

            self.wfile.write(response.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()


def run_server():
    server = HTTPServer(("", 8080), TrainServer)
    print("Train booking server starting on port 8080...")
    server.serve_forever()


if __name__ == "__main__":
    run_server()



================================================
FILE: tools/__init__.py
================================================
from .change_goal import change_goal
from .create_invoice import create_invoice
from .ecommerce.get_order import get_order
from .ecommerce.list_orders import list_orders
from .ecommerce.track_package import track_package
from .fin.check_account_valid import check_account_valid
from .fin.get_account_balances import get_account_balance
from .fin.move_money import move_money
from .fin.submit_loan_application import submit_loan_application
from .find_events import find_events
from .food.add_to_cart import add_to_cart
from .give_hint import give_hint
from .guess_location import guess_location
from .hr.book_pto import book_pto
from .hr.checkpaybankstatus import checkpaybankstatus
from .hr.current_pto import current_pto
from .hr.future_pto_calc import future_pto_calc
from .list_agents import list_agents
from .search_fixtures import search_fixtures
from .search_flights import search_flights
from .search_trains import book_trains, search_trains
from .transfer_control import transfer_control


def get_handler(tool_name: str):
    if tool_name == "SearchFixtures":
        return search_fixtures
    if tool_name == "SearchFlights":
        return search_flights
    if tool_name == "SearchTrains":
        return search_trains
    if tool_name == "BookTrains":
        return book_trains
    if tool_name == "CreateInvoice":
        return create_invoice
    if tool_name == "FindEvents":
        return find_events
    if tool_name == "ListAgents":
        return list_agents
    if tool_name == "ChangeGoal":
        return change_goal
    if tool_name == "TransferControl":
        return transfer_control
    if tool_name == "CurrentPTO":
        return current_pto
    if tool_name == "BookPTO":
        return book_pto
    if tool_name == "FuturePTOCalc":
        return future_pto_calc
    if tool_name == "CheckPayBankStatus":
        return checkpaybankstatus
    if tool_name == "FinCheckAccountIsValid":
        return check_account_valid
    if tool_name == "FinCheckAccountBalance":
        return get_account_balance
    if tool_name == "FinMoveMoney":
        return move_money
    if tool_name == "FinCheckAccountSubmitLoanApproval":
        return submit_loan_application
    if tool_name == "GetOrder":
        return get_order
    if tool_name == "TrackPackage":
        return track_package
    if tool_name == "ListOrders":
        return list_orders
    if tool_name == "GiveHint":
        return give_hint
    if tool_name == "GuessLocation":
        return guess_location
    if tool_name == "AddToCart":
        return add_to_cart

    raise ValueError(f"Unknown tool: {tool_name}")



================================================
FILE: tools/change_goal.py
================================================
def change_goal(args: dict) -> dict:
    new_goal = args.get("goalID")
    if new_goal is None:
        new_goal = "goal_choose_agent_type"

    return {
        "new_goal": new_goal,
    }



================================================
FILE: tools/create_invoice.py
================================================
import os

from dotenv import load_dotenv


def ensure_customer_exists(
    customer_id: str = None, email: str = "default@example.com"
) -> str:
    """Ensure a Stripe customer exists; create one if not."""
    import stripe

    if customer_id:
        try:
            stripe.Customer.retrieve(customer_id)
            return customer_id
        except stripe.error.InvalidRequestError:
            # Customer ID is invalid or doesn't exist
            pass

    # Create a new customer if no valid customer_id
    customer = stripe.Customer.create(email=email)
    return customer.id


def create_invoice(args: dict) -> dict:
    """Create and finalize a Stripe invoice."""
    import stripe

    # Load environment variables and configure stripe
    load_dotenv(override=True)
    stripe.api_key = os.getenv("STRIPE_API_KEY")

    # If an API key exists in the env file, find or create customer
    if stripe.api_key is not None and stripe.api_key != "":
        customer_id = ensure_customer_exists(
            args.get("customer_id"), args.get("email", "default@example.com")
        )

        # Get amount and convert to cents
        amount = args.get("amount", 200.00)  # Default to $200.00
        try:
            amount_cents = int(float(amount) * 100)
        except (TypeError, ValueError):
            return {"error": "Invalid amount provided. Please confirm the amount."}

        # Create an invoice item
        stripe.InvoiceItem.create(
            customer=customer_id,
            amount=amount_cents,
            currency="gbp",
            description=args.get("tripDetails", "Service Invoice"),
        )

        # Create and finalize the invoice
        invoice = stripe.Invoice.create(
            customer=customer_id,
            collection_method="send_invoice",  # Invoice is sent to the customer
            days_until_due=args.get("days_until_due", 7),  # Default due date: 7 days
            pending_invoice_items_behavior="include",  # No pending invoice items
        )
        finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)

        return {
            "invoiceStatus": finalized_invoice.status,
            "invoiceURL": finalized_invoice.hosted_invoice_url,
            "reference": finalized_invoice.number,
        }
    # if no API key is in the env file, return dummy info
    else:
        print("[CreateInvoice] Creating invoice with:", args)
        return {
            "invoiceStatus": "generated",
            "invoiceURL": "https://pay.example.com/invoice/12345",
            "reference": "INV-12345",
        }



================================================
FILE: tools/find_events.py
================================================
import json
from datetime import datetime
from pathlib import Path


def find_events(args: dict) -> dict:
    search_city = args.get("city", "").lower()
    search_month = args.get("month", "").capitalize()

    file_path = Path(__file__).resolve().parent / "data" / "find_events_data.json"
    if not file_path.exists():
        return {"error": "Data file not found."}

    try:
        month_number = datetime.strptime(search_month, "%B").month
    except ValueError:
        return {"error": "Invalid month provided."}

    # Helper to wrap months into [1..12]
    def get_adjacent_months(m):
        prev_m = 12 if m == 1 else (m - 1)
        next_m = 1 if m == 12 else (m + 1)
        return [prev_m, m, next_m]

    valid_months = get_adjacent_months(month_number)

    matching_events = []
    for city_name, events in json.load(open(file_path)).items():
        if search_city and search_city not in city_name.lower():
            continue

        for event in events:
            date_from = datetime.strptime(event["dateFrom"], "%Y-%m-%d")
            date_to = datetime.strptime(event["dateTo"], "%Y-%m-%d")

            # If the event's start or end month is in our valid months
            if date_from.month in valid_months or date_to.month in valid_months:
                # Add metadata explaining how it matches
                if date_from.month == month_number or date_to.month == month_number:
                    month_context = "requested month"
                elif (
                    date_from.month == valid_months[0]
                    or date_to.month == valid_months[0]
                ):
                    month_context = "previous month"
                else:
                    month_context = "next month"

                matching_events.append(
                    {
                        "city": city_name,
                        "eventName": event["eventName"],
                        "dateFrom": event["dateFrom"],
                        "dateTo": event["dateTo"],
                        "description": event["description"],
                        "month": month_context,
                    }
                )

    # Add top-level metadata if you wish
    return {
        "note": f"Returning events from {search_month} plus one month either side (i.e., {', '.join(datetime(2025, m, 1).strftime('%B') for m in valid_months)}).",
        "events": matching_events,
    }



================================================
FILE: tools/give_hint.py
================================================
TREASURE_LOCATION = {
    "address": "300 Lenora",
    "city": "Seattle",
    "state_full": "Washington",
    "state_abbrev": "WA",
    "zip": "98121",
    "country": "USA",
}

HINTS = [
    "country of " + TREASURE_LOCATION["country"],
    "state of " + TREASURE_LOCATION["state_full"],
    "city of " + TREASURE_LOCATION["city"],
    "at a company HQ",
    "The company's tech traces its roots to a project called Cadence",  # thanks, Grok
    "The company offers a tool that lets developers write code as if it's running forever, no matter what crashes",  # thanks, Grok
]
''' Additional Grok provided hints about Temporal:
"This company was founded by two engineers who previously worked on a system named after a South American river at Uber."
"Their platform is all about orchestrating workflows that can survive failures—like a conductor keeping the music going."
"They offer a tool that lets developers write code as if it’s running forever, no matter what crashes."
"Their mission is tied to making distributed systems feel as simple as writing a single app."
"They’ve got a knack for ‘durability’—both in their software and their growing reputation."
"This outfit spun out of experiences at AWS and Uber, blending cloud and ride-sharing know-how."
"Their open-source framework has a community that’s ticking along, fixing bugs and adding features daily."
"They’re backed by big venture capital names like Sequoia, betting on their vision for reliable software."
"The company’s name might remind you of a word for something fleeting, yet their tech is built to last."'''


def give_hint(args: dict) -> dict:
    hint_total = args.get("hint_total")
    if hint_total is None:
        hint_total = 0

    index = hint_total % len(HINTS)
    hint_text = HINTS[index]

    hint_total = hint_total + 1
    return {"hint_number": hint_total, "hint": hint_text}



================================================
FILE: tools/guess_location.py
================================================
from .give_hint import TREASURE_LOCATION


def guess_location(args: dict) -> dict:
    guess_address = args.get("address").lower()
    guess_city = args.get("city").lower()
    guess_state = args.get("state").lower()

    if len(guess_state) == 2:
        compare_state = TREASURE_LOCATION.get("state_abbrev").lower()
    else:
        compare_state = TREASURE_LOCATION.get("state_full").lower()

    # Check for the street address to be included in the guess to account for "st" vs "street" or leaving Street off entirely
    if (
        TREASURE_LOCATION.get("address").lower() in guess_address
        and TREASURE_LOCATION.get("city").lower() == guess_city
        and compare_state == guess_state
    ):
        return {"treasure_found": "True"}
    else:
        return {"treasure_found": "False"}



================================================
FILE: tools/list_agents.py
================================================
import os

import goals


def list_agents(args: dict) -> dict:
    goal_categories_start = os.getenv("GOAL_CATEGORIES")
    if goal_categories_start is None:
        goal_categories = ["all"]  # default to 'all' categories
    else:
        goal_categories_start.strip().lower()  # handle extra spaces or non-lowercase
        goal_categories = goal_categories_start.split(",")

    # if multi-goal-mode, add agent_selection as a goal (defaults to True)
    if "agent_selection" not in goal_categories:
        first_goal_value = os.getenv("AGENT_GOAL")
        if (
            first_goal_value is None
            or first_goal_value.lower() == "goal_choose_agent_type"
        ):
            goal_categories.append("agent_selection")

    # always show goals labeled as "system," like the goal chooser
    if "system" not in goal_categories:
        goal_categories.append("system")

    agents = []
    if goals.goal_list is not None:
        for goal in goals.goal_list:
            # add to list if either
            #   - all
            #   - current goal's tag is in goal_categories
            if "all" in goal_categories or goal.category_tag in goal_categories:
                agents.append(
                    {
                        "agent_name": goal.agent_name,
                        "goal_id": goal.id,
                        "agent_description": goal.agent_friendly_description,
                    }
                )
    return {
        "agents": agents,
    }



================================================
FILE: tools/search_fixtures.py
================================================
import os
import random
from datetime import date, datetime, timedelta

import requests
from dotenv import load_dotenv

PREMIER_LEAGUE_CLUBS_DATA = [
    {"name": "Arsenal FC", "stadium": "Emirates Stadium"},
    {"name": "Aston Villa FC", "stadium": "Villa Park"},
    {"name": "AFC Bournemouth", "stadium": "Vitality Stadium"},
    {"name": "Brentford FC", "stadium": "Gtech Community Stadium"},
    {"name": "Brighton & Hove Albion FC", "stadium": "American Express Stadium"},
    {"name": "Chelsea FC", "stadium": "Stamford Bridge"},
    {"name": "Crystal Palace FC", "stadium": "Selhurst Park"},
    {"name": "Everton FC", "stadium": "Goodison Park"},
    {"name": "Fulham FC", "stadium": "Craven Cottage"},
    {"name": "Ipswich Town FC", "stadium": "Portman Road"},
    {"name": "Leicester City FC", "stadium": "King Power Stadium"},
    {"name": "Liverpool FC", "stadium": "Anfield"},
    {"name": "Manchester City FC", "stadium": "Etihad Stadium"},
    {"name": "Manchester United FC", "stadium": "Old Trafford"},
    {"name": "Newcastle United FC", "stadium": "St James' Park"},
    {"name": "Nottingham Forest FC", "stadium": "City Ground"},
    {"name": "Southampton FC", "stadium": "St Mary's Stadium"},
    {"name": "Tottenham Hotspur FC", "stadium": "Tottenham Hotspur Stadium"},
    {"name": "West Ham United FC", "stadium": "London Stadium"},
    {"name": "Wolverhampton Wanderers FC", "stadium": "Molineux Stadium"},
]


def get_future_matches(
    team_name: str,
    all_clubs_data: list,
    num_matches: int = 12,
    date_from: date = None,
    date_to: date = None,
) -> list:
    """Generate a set of future Premier League matches for ``team_name``.

    This is a purely mocked schedule. It returns up to ``num_matches``
    fixtures, respecting the ``date_from`` and ``date_to`` constraints.
    Matches are typically on Saturdays or Sundays.
    """
    matches = []

    team_details = next((c for c in all_clubs_data if c["name"] == team_name), None)
    if not team_details:
        return []

    opponents_pool = [c for c in all_clubs_data if c["name"] != team_name]
    if not opponents_pool:
        return []

    # Determine the maximum number of matches we can generate based on opponents
    # and the requested num_matches
    num_actual_matches_to_generate = min(num_matches, len(opponents_pool))
    if num_actual_matches_to_generate == 0:
        return []

    # Shuffle opponents once and pick them sequentially
    random.shuffle(opponents_pool)  # Shuffle in place

    # Determine the initial Saturday for match week consideration
    today_date = date.today()
    # Default to next Saturday
    current_match_week_saturday = today_date + timedelta(
        days=(5 - today_date.weekday() + 7) % 7
    )

    # If today is Saturday and it's late evening, or if today is Sunday,
    # advance to the following Saturday.
    now_time = datetime.now().time()
    if (
        today_date.weekday() == 5
        and now_time > datetime.strptime("20:00", "%H:%M").time()
    ) or (today_date.weekday() == 6):
        current_match_week_saturday += timedelta(days=7)

    # If date_from is specified, ensure our starting Saturday is not before it.
    if date_from:
        if current_match_week_saturday < date_from:
            current_match_week_saturday = date_from
        # Align current_match_week_saturday to be a Saturday on or after the potentially adjusted date
        current_match_week_saturday += timedelta(
            days=(5 - current_match_week_saturday.weekday() + 7) % 7
        )

    opponent_idx = 0
    while len(matches) < num_actual_matches_to_generate and opponent_idx < len(
        opponents_pool
    ):
        # If the current week's Saturday is already past date_to, stop.
        if date_to and current_match_week_saturday > date_to:
            break

        opponent_details = opponents_pool[opponent_idx]
        is_saturday_game = random.choice([True, True, False])
        actual_match_date = None
        kick_off_time = ""

        if is_saturday_game:
            actual_match_date = current_match_week_saturday
            kick_off_time = random.choice(["12:30", "15:00", "17:30"])
        else:  # Sunday game
            actual_match_date = current_match_week_saturday + timedelta(days=1)
            kick_off_time = random.choice(["14:00", "16:30"])

        # Check if this specific match date is within the date_to constraint
        if date_to and actual_match_date > date_to:
            # If this game is too late, try the next week if possible.
            # (This mainly affects Sunday games if Saturday was the last valid day)
            current_match_week_saturday += timedelta(days=7)
            continue  # Skip adding this match, try next week.

        match_datetime_gmt = (
            f"{actual_match_date.strftime('%Y-%m-%d')} {kick_off_time} GMT"
        )
        is_home_match = random.choice([True, False])

        if is_home_match:
            team1_name = team_details["name"]
            team2_name = opponent_details["name"]
            stadium_name = team_details["stadium"]
        else:
            team1_name = opponent_details["name"]
            team2_name = team_details["name"]
            stadium_name = opponent_details["stadium"]

        matches.append(
            {
                "team1": team1_name,
                "team2": team2_name,
                "stadium": stadium_name,
                "datetime_gmt": match_datetime_gmt,
            }
        )
        opponent_idx += 1
        current_match_week_saturday += timedelta(
            days=7
        )  # Advance to next week's Saturday

    return matches


BASE_URL = "https://api.football-data.org/v4"


def search_fixtures(args: dict) -> dict:
    load_dotenv(override=True)
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")

    team_name = args.get("team")
    date_from_str = args.get("date_from")
    date_to_str = args.get("date_to")

    if not team_name:
        return {"error": "Team name is required."}

    parsed_date_from = None
    if date_from_str:
        try:
            parsed_date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
        except ValueError:
            return {
                "error": f"Invalid date_from: '{date_from_str}'. Expected format YYYY-MM-DD."
            }

    parsed_date_to = None
    if date_to_str:
        try:
            parsed_date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
        except ValueError:
            return {
                "error": f"Invalid date_to: '{date_to_str}'. Expected format YYYY-MM-DD."
            }

    if parsed_date_from and parsed_date_to and parsed_date_from > parsed_date_to:
        return {"error": "date_from cannot be after date_to."}

    # If no API key, fall back to mocked data
    if not api_key:
        # Use the parsed date objects (which can be None)
        fixtures = get_future_matches(
            team_name,
            PREMIER_LEAGUE_CLUBS_DATA,
            date_from=parsed_date_from,
            date_to=parsed_date_to,
            # num_matches can be passed explicitly if needed, otherwise defaults to 12
        )
        if not fixtures:
            # Check if the team name itself was invalid, as get_future_matches returns [] for that too
            team_details_check = next(
                (c for c in PREMIER_LEAGUE_CLUBS_DATA if c["name"] == team_name), None
            )
            if not team_details_check:
                return {"error": f"Team '{team_name}' not found in mocked data."}
            # If team is valid, an empty fixtures list means no matches fit the criteria (e.g., date range)
        return {"fixtures": fixtures}

    # API Key is present, proceed with API logic
    # The API requires both date_from and date_to
    if not parsed_date_from or not parsed_date_to:
        return {
            "error": "Both date_from and date_to (YYYY-MM-DD) are required for API search."
        }

    headers = {"X-Auth-Token": api_key}
    # For API calls, team name matching might be case-insensitive or require specific handling
    # The existing logic uses team_name.lower() for the API search path later.

    # Fetch team ID
    teams_response = requests.get(f"{BASE_URL}/competitions/PL/teams", headers=headers)
    if teams_response.status_code != 200:
        return {
            "error": f"Failed to fetch teams data from API (status {teams_response.status_code})."
        }

    teams_data = teams_response.json()
    team_id = None
    # Using lower() for comparison, assuming API team names might have varied casing
    # or the input team_name might not be exact.
    # The `ToolDefinition` lists exact names, so direct match might also be an option.
    for team_api_data in teams_data.get("teams", []):
        if team_name.lower() in team_api_data.get("name", "").lower():
            team_id = team_api_data["id"]
            break

    if not team_id:
        return {"error": f"Team '{team_name}' not found via API."}

    date_from_formatted = parsed_date_from.strftime("%Y-%m-%d")
    date_to_formatted = parsed_date_to.strftime("%Y-%m-%d")
    fixtures_url = f"{BASE_URL}/teams/{team_id}/matches?dateFrom={date_from_formatted}&dateTo={date_to_formatted}"
    # print(fixtures_url) # Keep for debugging if necessary

    fixtures_response = requests.get(fixtures_url, headers=headers)
    if fixtures_response.status_code != 200:
        return {
            "error": f"Failed to fetch fixtures data from API (status {fixtures_response.status_code})."
        }

    fixtures_data = fixtures_response.json()
    matching_fixtures = []

    for match in fixtures_data.get("matches", []):
        # Ensure match datetime parsing is robust
        try:
            match_datetime_utc = datetime.strptime(
                match["utcDate"], "%Y-%m-%dT%H:%M:%SZ"
            )
        except (ValueError, TypeError):
            # Skip malformed match entries or log an error
            continue

        if match.get("competition", {}).get("code") == "PL":
            matching_fixtures.append(
                {
                    "date": match_datetime_utc.strftime("%Y-%m-%d"),
                    "homeTeam": match.get("homeTeam", {}).get("name", "N/A"),
                    "awayTeam": match.get("awayTeam", {}).get("name", "N/A"),
                }
            )

    return {"fixtures": matching_fixtures}


def search_fixtures_example(args: dict) -> dict:
    """
    Example version of search_fixtures that returns hardcoded data without making API calls.
    The function respects the team name provided and generates fixture dates within the specified range.

    Args:
        args: Dictionary containing 'team', 'date_from', and 'date_to'

    Returns:
        Dictionary with 'fixtures' key containing a list of fixture objects
    """
    team_name = args.get("team", "Default Team FC")
    date_from_str = args.get("date_from")
    date_to_str = args.get("date_to")

    # Validate dates
    try:
        # Ensure date strings are not None before parsing
        if date_from_str is None or date_to_str is None:
            raise ValueError("Date strings cannot be None")
        date_from_obj = datetime.strptime(date_from_str, "%Y-%m-%d")
        date_to_obj = datetime.strptime(date_to_str, "%Y-%m-%d")
    except ValueError:
        return {
            "error": "Invalid date provided. Expected format YYYY-MM-DD for both date_from and date_to."
        }

    # Calculate 3 reasonable fixture dates within the given range
    date_range = (date_to_obj - date_from_obj).days
    if date_range < 0:  # date_from is after date_to
        return {"fixtures": []}  # No fixtures possible

    fixture_dates_timestamps = []
    if date_range < 21:
        # If range is less than 3 weeks, use evenly spaced fixtures if possible
        if date_range >= 2:  # Need at least some gap for 3 fixtures
            fixture_dates_timestamps = [
                date_from_obj
                + timedelta(days=max(0, date_range // 4)),  # Closer to start
                date_from_obj + timedelta(days=max(1, date_range // 2)),  # Middle
                date_to_obj - timedelta(days=max(0, date_range // 4)),  # Closer to end
            ]
        elif date_range == 1:  # Only two days
            fixture_dates_timestamps = [date_from_obj, date_to_obj]
        elif date_range == 0:  # Only one day
            fixture_dates_timestamps = [date_from_obj]
        else:  # date_range is negative, handled above, or 0 (single day)
            fixture_dates_timestamps = [date_from_obj] if date_range == 0 else []

    else:
        # Otherwise space them out by weeks, ensuring they are within the bounds
        d1 = date_from_obj + timedelta(days=7)
        d2 = date_from_obj + timedelta(days=14)
        d3 = date_to_obj - timedelta(days=7)  # Potential third game from the end

        fixture_dates_timestamps.append(d1)
        if d2 <= date_to_obj and d2 > d1:  # ensure d2 is valid and distinct
            fixture_dates_timestamps.append(d2)
        if (
            d3 >= date_from_obj and d3 > d2 and d3 <= date_to_obj
        ):  # ensure d3 is valid and distinct
            fixture_dates_timestamps.append(d3)
        elif (
            d3 < date_from_obj and len(fixture_dates_timestamps) < 3
        ):  # if d3 is too early, try using date_to_obj itself if distinct
            if date_to_obj not in fixture_dates_timestamps:
                fixture_dates_timestamps.append(date_to_obj)

    # Ensure unique dates and sort, then take up to 3.
    fixture_dates_timestamps = sorted(
        list(
            set(
                f_date
                for f_date in fixture_dates_timestamps
                if date_from_obj <= f_date <= date_to_obj
            )
        )
    )
    fixture_dates_final = fixture_dates_timestamps[:3]

    all_opponents = [
        "Manchester United FC",
        "Leicester City FC",
        "Manchester City FC",
        "Liverpool FC",
        "Chelsea FC",
        "Arsenal FC",
        "Tottenham Hotspur FC",
        "West Ham United FC",
        "Everton FC",
        "Generic Opponent A",
        "Generic Opponent B",
        "Generic Opponent C",  # Fallbacks
    ]

    available_opponents = [
        team for team in all_opponents if team.lower() != team_name.lower()
    ]

    # Ensure we have enough opponents for the number of fixtures we'll generate
    if len(available_opponents) < len(fixture_dates_final):
        needed = len(fixture_dates_final) - len(available_opponents)
        for i in range(needed):
            available_opponents.append(f"Placeholder Opponent {i+1}")

    opponents = available_opponents[: len(fixture_dates_final)]

    fixtures = []
    for i, fixture_date_obj in enumerate(fixture_dates_final):
        if i >= len(opponents):  # Should not happen with the logic above
            break
        date_str = fixture_date_obj.strftime("%Y-%m-%d")
        if i % 2 == 0:  # Home game
            fixtures.append(
                {"date": date_str, "homeTeam": team_name, "awayTeam": opponents[i]}
            )
        else:  # Away game
            fixtures.append(
                {"date": date_str, "homeTeam": opponents[i], "awayTeam": team_name}
            )

    return {"fixtures": fixtures}



================================================
FILE: tools/search_flights.py
================================================
import http.client
import json
import os
import random
import urllib.parse

from dotenv import load_dotenv


def search_airport(query: str) -> list:
    """
    Returns a list of matching airports/cities from sky-scrapper's searchAirport endpoint.
    """
    load_dotenv(override=True)
    api_key = os.getenv("RAPIDAPI_KEY", "YOUR_DEFAULT_KEY")
    api_host = os.getenv("RAPIDAPI_HOST_FLIGHTS", "sky-scrapper.p.rapidapi.com")

    conn = http.client.HTTPSConnection(api_host)
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host,
    }

    # Sanitize the query to ensure it is URL-safe
    print(f"Searching for: {query}")
    encoded_query = urllib.parse.quote(query)
    path = f"/api/v1/flights/searchAirport?query={encoded_query}&locale=en-US"

    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    if res.status != 200:
        print(f"Error: API responded with status code {res.status}")
        print(f"Response: {res.read().decode('utf-8')}")
        return []

    data = res.read()
    conn.close()

    try:
        return json.loads(data).get("data", [])
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response")
        print(f"Response: {data.decode('utf-8')}")
        return []


def search_flights_real_api(
    args: dict,
) -> dict:  # rename to search_flights to use the real API
    """
    1) Looks up airport/city codes via search_airport.
    2) Finds the first matching skyId/entityId for both origin & destination.
    3) Calls the flight search endpoint with those codes.
    """
    date_depart = args.get("dateDepart")
    date_return = args.get("dateReturn")
    origin_query = args.get("origin")
    dest_query = args.get("destination")

    # Step 1: Resolve skyIds
    origin_candidates = search_airport(origin_query)
    destination_candidates = search_airport(dest_query)

    if not origin_candidates or not destination_candidates:
        return {"error": "No matches found for origin/destination"}

    origin_params = origin_candidates[0]["navigation"]["relevantFlightParams"]
    dest_params = destination_candidates[0]["navigation"]["relevantFlightParams"]

    origin_sky_id = origin_params["skyId"]  # e.g. "LOND"
    origin_entity_id = origin_params["entityId"]  # e.g. "27544008"
    dest_sky_id = dest_params["skyId"]  # e.g. "NYCA"
    dest_entity_id = dest_params["entityId"]  # e.g. "27537542"

    # Step 2: Call flight search with resolved codes
    load_dotenv(override=True)
    api_key = os.getenv("RAPIDAPI_KEY", "YOUR_DEFAULT_KEY")
    api_host = os.getenv("RAPIDAPI_HOST_FLIGHTS", "sky-scrapper.p.rapidapi.com")

    conn = http.client.HTTPSConnection(api_host)
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host,
    }

    path = (
        "/api/v2/flights/searchFlights?"
        f"originSkyId={origin_sky_id}"
        f"&destinationSkyId={dest_sky_id}"
        f"&originEntityId={origin_entity_id}"
        f"&destinationEntityId={dest_entity_id}"
        f"&date={date_depart}"
        f"&returnDate={date_return}"
        f"&cabinClass=economy&adults=1&sortBy=best&currency=USD"
        f"&market=en-US&countryCode=US"
    )

    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    try:
        json_data = json.loads(data)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}

    itineraries = json_data.get("data", {}).get("itineraries", [])
    if not itineraries:
        return json_data  # Return raw response for debugging if itineraries are empty

    formatted_results = []
    seen_carriers = set()

    for itinerary in itineraries:
        legs = itinerary.get("legs", [])
        if len(legs) >= 2:
            # Extract outbound and return flight details
            outbound_leg = legs[0]
            return_leg = legs[1]

            # Get the first segment for flight details
            outbound_flight = outbound_leg.get("segments", [{}])[0]
            return_flight = return_leg.get("segments", [{}])[0]

            # Extract flight details
            outbound_carrier = outbound_flight.get("operatingCarrier", {}).get(
                "name", "N/A"
            )
            outbound_carrier_code = outbound_flight.get("operatingCarrier", {}).get(
                "alternateId", ""
            )
            outbound_flight_number = outbound_flight.get("flightNumber", "N/A")
            outbound_flight_code = (
                f"{outbound_carrier_code}{outbound_flight_number}"
                if outbound_carrier_code
                else outbound_flight_number
            )

            return_carrier = return_flight.get("operatingCarrier", {}).get(
                "name", "N/A"
            )
            return_carrier_code = return_flight.get("operatingCarrier", {}).get(
                "alternateId", ""
            )
            return_flight_number = return_flight.get("flightNumber", "N/A")
            return_flight_code = (
                f"{return_carrier_code}{return_flight_number}"
                if return_carrier_code
                else return_flight_number
            )

            # Check if carrier is unique
            if outbound_carrier not in seen_carriers:
                seen_carriers.add(outbound_carrier)  # Add to seen carriers
                formatted_results.append(
                    {
                        "outbound_flight_code": outbound_flight_code,
                        "operating_carrier": outbound_carrier,
                        "return_flight_code": return_flight_code,
                        "return_operating_carrier": return_carrier,
                        "price": itinerary.get("price", {}).get("raw", 0.0),
                    }
                )

            # Stop after finding 3 unique carriers
            if len(formatted_results) >= 3:
                break

    return {
        "origin": origin_query,
        "destination": dest_query,
        "currency": "USD",
        "results": formatted_results,
    }


def generate_smart_flights(origin: str, destination: str) -> list:
    """
    Generate realistic flight options with smart pricing based on origin and destination.
    """
    # Common airlines for different regions
    airlines_by_region = {
        "domestic_us": [
            {"name": "American Airlines", "code": "AA"},
            {"name": "United Airlines", "code": "UA"},
            {"name": "Delta Airlines", "code": "DL"},
            {"name": "Southwest Airlines", "code": "WN"},
        ],
        "us_international": [
            {"name": "American Airlines", "code": "AA"},
            {"name": "United Airlines", "code": "UA"},
            {"name": "Delta Airlines", "code": "DL"},
            {"name": "Virgin Atlantic", "code": "VS"},
        ],
        "australia_nz": [
            {"name": "Qantas", "code": "QF"},
            {"name": "Jetstar", "code": "JQ"},
            {"name": "Virgin Australia", "code": "VA"},
            {"name": "Air New Zealand", "code": "NZ"},
        ],
        "international": [
            {"name": "American Airlines", "code": "AA"},
            {"name": "United Airlines", "code": "UA"},
            {"name": "Delta Airlines", "code": "DL"},
            {"name": "Air New Zealand", "code": "NZ"},
            {"name": "Qantas", "code": "QF"},
            {"name": "Singapore Airlines", "code": "SQ"},
        ],
    }

    # Determine route type and base pricing
    origin_lower = origin.lower()
    dest_lower = destination.lower()

    # Australia/NZ cities
    anz_cities = [
        "sydney",
        "melbourne",
        "syd",
        "mel",
        "auckland",
        "akl",
        "wellington",
        "wlg",
        "brisbane",
        "bne",
        "perth",
        "per",
    ]
    # US cities
    us_cities = [
        "los angeles",
        "lax",
        "san francisco",
        "sfo",
        "new york",
        "nyc",
        "jfk",
        "chicago",
        "ord",
        "miami",
        "mia",
    ]

    is_origin_anz = any(city in origin_lower for city in anz_cities)
    is_dest_anz = any(city in dest_lower for city in anz_cities)
    is_origin_us = any(city in origin_lower for city in us_cities)
    is_dest_us = any(city in dest_lower for city in us_cities)

    # Determine airline pool and base price
    if (is_origin_us and is_dest_anz) or (is_origin_anz and is_dest_us):
        # Trans-Pacific routes
        airline_pool = airlines_by_region["international"]
        base_price = random.randint(1200, 1800)
    elif is_origin_anz and is_dest_anz:
        # Australia/NZ domestic
        airline_pool = airlines_by_region["australia_nz"]
        base_price = random.randint(300, 600)
    elif is_origin_us and is_dest_us:
        # US domestic
        airline_pool = airlines_by_region["domestic_us"]
        base_price = random.randint(200, 800)
    else:
        # General international
        airline_pool = airlines_by_region["international"]
        base_price = random.randint(800, 1500)

    # Generate 3-4 flight options
    num_flights = random.randint(3, 4)
    results = []
    used_airlines = set()

    for i in range(num_flights):
        # Pick unique airline
        available_airlines = [a for a in airline_pool if a["name"] not in used_airlines]
        if not available_airlines:
            available_airlines = airline_pool  # Reset if we run out

        airline = random.choice(available_airlines)
        used_airlines.add(airline["name"])

        # Generate flight numbers
        outbound_num = random.randint(100, 999)
        return_num = random.randint(100, 999)

        # Price variation (cheaper airlines get lower prices)
        price_multiplier = 1.0
        if "Southwest" in airline["name"] or "Jetstar" in airline["name"]:
            price_multiplier = 0.7
        elif "Virgin" in airline["name"]:
            price_multiplier = 0.85
        elif "Singapore" in airline["name"]:
            price_multiplier = 1.2

        # Add some random variation
        price_variation = random.uniform(0.9, 1.1)
        final_price = round(base_price * price_multiplier * price_variation, 2)

        results.append(
            {
                "operating_carrier": airline["name"],
                "outbound_flight_code": f"{airline['code']}{outbound_num}",
                "price": final_price,
                "return_flight_code": f"{airline['code']}{return_num}",
                "return_operating_carrier": airline["name"],
            }
        )

    # Sort by price
    results.sort(key=lambda x: x["price"])
    return results


def search_flights(args: dict) -> dict:
    """
    Search for flights. Uses real API if RAPIDAPI_KEY is available, otherwise generates smart mock data.
    """
    load_dotenv(override=True)
    api_key = os.getenv("RAPIDAPI_KEY")

    origin = args.get("origin")
    destination = args.get("destination")

    if not origin or not destination:
        return {"error": "Both origin and destination are required"}

    # If API key is available, use the real API
    if api_key and api_key != "YOUR_DEFAULT_KEY":
        return search_flights_real_api(args)

    # Otherwise, generate smart mock data
    results = generate_smart_flights(origin, destination)

    return {
        "currency": "USD",
        "destination": destination,
        "origin": origin,
        "results": results,
    }



================================================
FILE: tools/search_trains.py
================================================
def search_trains(args: dict) -> dict:
    raise NotImplementedError("TODO implement :)")


def book_trains(args: dict) -> dict:
    raise NotImplementedError("TODO implement :)")



================================================
FILE: tools/tool_registry.py
================================================
from typing import Dict, List

from models.tool_definitions import ToolArgument, ToolDefinition

# ----- System tools -----
list_agents_tool = ToolDefinition(
    name="ListAgents",
    description="List available agents to interact with, pulled from goal_registry. ",
    arguments=[],
)

change_goal_tool = ToolDefinition(
    name="ChangeGoal",
    description="Change the goal of the active agent. ",
    arguments=[
        ToolArgument(
            name="goalID",
            type="string",
            description="Which goal to change to",
        ),
    ],
)

give_hint_tool = ToolDefinition(
    name="GiveHint",
    description="Give a hint to the user regarding the location of the pirate treasure. Use previous conversation to determine the hint_total, it should initially be 0 ",
    arguments=[
        ToolArgument(
            name="hint_total",
            type="number",
            description="How many hints have been given",
        ),
    ],
)

guess_location_tool = ToolDefinition(
    name="GuessLocation",
    description="Allow the user to guess the location (in the form of an address) of the pirate treasure. ",
    arguments=[
        ToolArgument(
            name="address",
            type="string",
            description="Address at which the user is guessing the treasure is located",
        ),
        ToolArgument(
            name="city",
            type="string",
            description="City at which the user is guessing the treasure is located",
        ),
        ToolArgument(
            name="state",
            type="string",
            description="State at which the user is guessing the treasure is located",
        ),
    ],
)

# ----- Travel use cases tools -----
search_flights_tool = ToolDefinition(
    name="SearchFlights",
    description="Search for return flights from an origin to a destination within a date range (dateDepart, dateReturn). "
    "You are allowed to suggest dates from the conversation history, but ALWAYS ask the user if ok.",
    arguments=[
        ToolArgument(
            name="origin",
            type="string",
            description="Airport or city (infer airport code from city and store)",
        ),
        ToolArgument(
            name="destination",
            type="string",
            description="Airport or city code for arrival (infer airport code from city and store)",
        ),
        ToolArgument(
            name="dateDepart",
            type="ISO8601",
            description="Start of date range in human readable format, when you want to depart",
        ),
        ToolArgument(
            name="dateReturn",
            type="ISO8601",
            description="End of date range in human readable format, when you want to return",
        ),
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of the user's desire to search flights, and to confirm the details "
            + "before moving on to the next step",
        ),
    ],
)

search_trains_tool = ToolDefinition(
    name="SearchTrains",
    description="Search for trains between two English cities. Returns a list of train information for the user to choose from. Present the list to the user.",
    arguments=[
        ToolArgument(
            name="origin",
            type="string",
            description="The city or place to depart from",
        ),
        ToolArgument(
            name="destination",
            type="string",
            description="The city or place to arrive at",
        ),
        ToolArgument(
            name="outbound_time",
            type="ISO8601",
            description="The date and time to search for outbound trains. If time of day isn't asked for, assume a decent time of day/evening for the outbound journey",
        ),
        ToolArgument(
            name="return_time",
            type="ISO8601",
            description="The date and time to search for return trains. If time of day isn't asked for, assume a decent time of day/evening for the inbound journey",
        ),
    ],
)

book_trains_tool = ToolDefinition(
    name="BookTrains",
    description="Books train tickets. Returns a booking reference.",
    arguments=[
        ToolArgument(
            name="train_ids",
            type="string",
            description="The IDs of the trains to book, comma separated",
        ),
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of user's desire to book train tickets",
        ),
    ],
)

create_invoice_tool = ToolDefinition(
    name="CreateInvoice",
    description="Generate an invoice for the items described for the total inferred by the conversation history so far. Returns URL to invoice.",
    arguments=[
        ToolArgument(
            name="amount",
            type="float",
            description="The total cost to be invoiced. Infer this from the conversation history.",
        ),
        ToolArgument(
            name="tripDetails",
            type="string",
            description="A description of the item details to be invoiced, inferred from the conversation history.",
        ),
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of user's desire to create an invoice",
        ),
    ],
)

search_fixtures_tool = ToolDefinition(
    name="SearchFixtures",
    description="Search for upcoming fixtures for a given team within a date range inferred from the user's description. Ignore valid premier league dates. Valid teams this season are Arsenal FC, Aston Villa FC, AFC Bournemouth, Brentford FC, Brighton & Hove Albion FC, Chelsea FC, Crystal Palace FC, Everton FC, Fulham FC, Ipswich Town FC, Leicester City FC, Liverpool FC, Manchester City FC, Manchester United FC, Newcastle United FC, Nottingham Forest FC, Southampton FC, Tottenham Hotspur FC, West Ham United FC, Wolverhampton Wanderers FC",
    arguments=[
        ToolArgument(
            name="team",
            type="string",
            description="The full name of the team to search for.",
        ),
        ToolArgument(
            name="date_from",
            type="string",
            description="The start date in format (YYYY-MM-DD) for the fixture search inferred from the user's request (e.g. mid-March).",
        ),
        ToolArgument(
            name="date_to",
            type="string",
            description="The end date in format (YYYY-MM-DD) for the fixture search (e.g. 'the last week of May').",
        ),
    ],
)

find_events_tool = ToolDefinition(
    name="FindEvents",
    description="Find upcoming events to travel to a given city (e.g., 'Melbourne') and a date or month. "
    "It knows about events in Oceania only (e.g. major Australian and New Zealand cities). "
    "It will search 1 month either side of the month provided. "
    "Returns a list of events. ",
    arguments=[
        ToolArgument(
            name="city",
            type="string",
            description="Which city to search for events",
        ),
        ToolArgument(
            name="month",
            type="string",
            description="The month to search for events (will search 1 month either side of the month provided)",
        ),
    ],
)

# ----- HR use cases tools -----
current_pto_tool = ToolDefinition(
    name="CurrentPTO",
    description="Find how much PTO a user currently has accrued. "
    "Returns the number of hours and (calculated) number of days of PTO. ",
    arguments=[
        ToolArgument(
            name="email",
            type="string",
            description="email address of user",
        ),
    ],
)

future_pto_calc_tool = ToolDefinition(
    name="FuturePTOCalc",
    description="Calculate if the user will have enough PTO as of their proposed date to accommodate the request. The proposed start and end dates should be in the future. "
    "Returns a boolean enough_pto and how many hours of PTO they will have remaining if they take the proposed dates. ",
    arguments=[
        ToolArgument(
            name="start_date",
            type="string",
            description="Start date of proposed PTO, sent in the form yyyy-mm-dd",
        ),
        ToolArgument(
            name="end_date",
            type="string",
            description="End date of proposed PTO, sent in the form yyyy-mm-dd",
        ),
        ToolArgument(
            name="email",
            type="string",
            description="email address of user",
        ),
    ],
)

book_pto_tool = ToolDefinition(
    name="BookPTO",
    description="Book PTO start and end date. Either 1) makes calendar item, or 2) sends calendar invite to self and boss? "
    "Returns a success indicator. ",
    arguments=[
        ToolArgument(
            name="start_date",
            type="string",
            description="Start date of proposed PTO, sent in the form yyyy-mm-dd",
        ),
        ToolArgument(
            name="end_date",
            type="string",
            description="End date of proposed PTO, sent in the form yyyy-mm-dd",
        ),
        ToolArgument(
            name="email",
            type="string",
            description="Email address of user, used to look up current PTO",
        ),
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of user's desire to book PTO",
        ),
    ],
)

paycheck_bank_integration_status_check = ToolDefinition(
    name="CheckPayBankStatus",
    description="Check status of Bank Integration for Paychecks. "
    "Returns the status of the bank integration, connected or disconnected. ",
    arguments=[
        ToolArgument(
            name="email",
            type="string",
            description="email address of user",
        ),
    ],
)

# ----- Financial use cases tools -----
financial_check_account_is_valid = ToolDefinition(
    name="FinCheckAccountIsValid",
    description="Check if an account is valid by email address or account ID. "
    "Returns the account status, valid or invalid. ",
    arguments=[
        ToolArgument(
            name="email",
            type="string",
            description="email address of user",
        ),
        ToolArgument(
            name="account_id",
            type="string",
            description="account ID of user",
        ),
    ],
)

financial_get_account_balances = ToolDefinition(
    name="FinCheckAccountBalance",
    description="Get account balance for your accounts. "
    "Returns the account balances of your accounts. ",
    arguments=[
        ToolArgument(
            name="email_address_or_account_ID",
            type="string",
            description="email address or account ID of user",
        ),
    ],
)

financial_move_money = ToolDefinition(
    name="FinMoveMoney",
    description="Send money from one account to another under the same acount ID (e.g. checking to savings). "
    "Returns the status of the order and the new balances in each account. ",
    arguments=[
        ToolArgument(
            name="email_address_or_account_ID",
            type="string",
            description="email address or account ID of user (you will need both to find the account)",
        ),
        ToolArgument(
            name="accounttype",
            type="string",
            description="account type, such as checking or savings",
        ),
        ToolArgument(
            name="amount",
            type="string",
            description="amount to move in the order (e.g. checking or savings)",
        ),
        ToolArgument(
            name="destinationaccount",
            type="string",
            description="account to move the money to (e.g. checking or savings)",
        ),
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of user's desire to move money",
        ),
    ],
)

financial_submit_loan_approval = ToolDefinition(
    name="FinCheckAccountSubmitLoanApproval",
    description="Submit a loan application. " "Returns the loan status. ",
    arguments=[
        ToolArgument(
            name="email_address_or_account_ID",
            type="string",
            description="email address or account ID of user",
        ),
        ToolArgument(
            name="amount",
            type="string",
            description="amount requested for the loan",
        ),
    ],
)

# ----- ECommerce Use Case Tools -----
ecomm_list_orders = ToolDefinition(
    name="ListOrders",
    description="Get all orders for a certain email address.",
    arguments=[
        ToolArgument(
            name="email_address",
            type="string",
            description="Email address of user by which to find orders",
        ),
    ],
)

ecomm_get_order = ToolDefinition(
    name="GetOrder",
    description="Get infromation about an order by order ID.",
    arguments=[
        ToolArgument(
            name="order_id",
            type="string",
            description="ID of order to determine status of",
        ),
    ],
)

ecomm_track_package = ToolDefinition(
    name="TrackPackage",
    description="Get tracking information for a package by shipping provider and tracking ID",
    arguments=[
        ToolArgument(
            name="tracking_id",
            type="string",
            description="ID of package to track",
        ),
        ToolArgument(
            name="userConfirmation",
            type="string",
            description="Indication of user's desire to get package tracking information",
        ),
    ],
)


# ----- Food Ordering Use Case Tools -----
food_add_to_cart_tool = ToolDefinition(
    name="AddToCart",
    description="Add a menu item to the customer's cart using item details from Stripe.",
    arguments=[
        ToolArgument(
            name="customer_email",
            type="string",
            description="Email address of the customer",
        ),
        ToolArgument(
            name="item_name",
            type="string",
            description="Name of the menu item (e.g., 'Margherita Pizza', 'Caesar Salad')",
        ),
        ToolArgument(
            name="item_price",
            type="number",
            description="Price of the item in dollars (e.g., 14.99)",
        ),
        ToolArgument(
            name="quantity",
            type="number",
            description="Quantity of the item to add (defaults to 1)",
        ),
        ToolArgument(
            name="stripe_product_id",
            type="string",
            description="Stripe product ID for reference (optional)",
        ),
    ],
)

# MCP Integration Functions


def create_mcp_tool_definitions(
    mcp_tools_info: Dict[str, Dict],
) -> List[ToolDefinition]:
    """Convert MCP tool info to ToolDefinition objects"""
    tool_definitions = []

    for tool_name, tool_info in mcp_tools_info.items():
        # Extract input schema properties
        input_schema = tool_info.get("inputSchema", {})
        properties = (
            input_schema.get("properties", {}) if isinstance(input_schema, dict) else {}
        )

        # Convert properties to ToolArgument objects
        arguments = []
        for param_name, param_info in properties.items():
            if isinstance(param_info, dict):
                arguments.append(
                    ToolArgument(
                        name=param_name,
                        type=param_info.get("type", "string"),
                        description=param_info.get("description", ""),
                    )
                )

        # Create ToolDefinition
        tool_def = ToolDefinition(
            name=tool_info["name"],
            description=tool_info.get("description", ""),
            arguments=arguments,
        )
        tool_definitions.append(tool_def)

    return tool_definitions



================================================
FILE: tools/transfer_control.py
================================================
import shared.config


def transfer_control(args: dict) -> dict:
    return {
        "new_goal": shared.config.AGENT_GOAL,
    }



================================================
FILE: tools/data/customer_account_data.json
================================================
{
    "accounts": [
        {
            "name": "Matt Murdock",
            "email": "matt.murdock@nelsonmurdock.com",
            "account_id": "11235",
            "checking_balance": "1275.4",
            "savings_balance": "2800.15",
            "bitcoin_balance": 0.1378,
            "account_creation_date": "2014-03-10"
        },
        {
            "name": "Foggy Nelson",
            "email": "foggy.nelson@nelsonmurdock.com",
            "account_id": "112358",
            "checking_balance": "1523.66",
            "savings_balance": "4875.89",
            "bitcoin_balance": 0.0923,
            "account_creation_date": "2014-03-10"
        },
        {
            "name": "Karen Page",
            "email": "karen.page@nelsonmurdock.com",
            "account_id": "112",
            "checking_balance": 645.25,
            "savings_balance": "830.5",
            "bitcoin_balance": 0.0456,
            "account_creation_date": "2015-01-15"
        },
        {
            "name": "Wilson Fisk",
            "email": "wilson.fisk@fiskcorp.com",
            "account_id": "11",
            "checking_balance": 25000.0,
            "savings_balance": 150000.75,
            "bitcoin_balance": 5987.6721,
            "account_creation_date": "2013-09-20"
        },
        {
            "name": "Frank Castle",
            "email": "frank.castle@vigilante.net",
            "account_id": "1",
            "checking_balance": 320.1,
            "savings_balance": 0.3,
            "bitcoin_balance": 15.2189,
            "account_creation_date": "2016-02-05"
        },
        {
            "name": "Joshua Smith",
            "email": "joshmsmith@gmail.com",
            "account_id": "11235813",
            "checking_balance": 3021.9,
            "savings_balance": 500.5,
            "bitcoin_balance": 0.001,
            "account_creation_date": "2020-03-19"
        }
    ]
}


================================================
FILE: tools/data/customer_order_data.json
================================================
{ 
    "orders": [
        {
            "id": "100",
            "summary": "Lawyer Books",
            "email": "matt.murdock@nelsonmurdock.com",
            "status": "cancelled",
            "order_date": "2025-03-30",
            "last_update": "2025-04-01"
        },
        {
            "id": "101",
            "summary": "Bonking Sticks",
            "email": "matt.murdock@nelsonmurdock.com",
            "status": "paid",
            "order_date": "2025-04-01",
            "last_order_update": "2025-04-01"
        },
        {
            "id": "102",
            "summary": "Red Sunglasses",
            "email": "matt.murdock@nelsonmurdock.com",
            "status": "shipped",
            "order_date": "2025-04-01",
            "last_order_update": "2025-04-01",
            "tracking_id": "UPS67890"
        },
        {
            "id": "200",
            "summary": "Paper",
            "email": "foggy.nelson@nelsonmurdock.com",
            "status": "shipped",
            "order_date": "2025-04-03",
            "last_update": "2025-04-06",
            "tracking_id": "USPS12345" 
        },
        {
            "id": "300",
            "summary": "Chemistry Books",
            "email": "heisenberg@blue-meth.com",
            "status": "shipped",
            "order_date": "2025-03-30",
            "last_update": "2025-04-06",
            "tracking_id": "USPS12345" 
        },
        {
            "id": "301",
            "summary": "Book: Being a Cool Bro",
            "email": "heisenberg@blue-meth.com",
            "status": "cancelled",
            "order_date": "2025-04-01",
            "last_update": "2025-04-02" 
        },
        {
            "id": "302",
            "summary": "Black Hat",
            "email": "heisenberg@blue-meth.com",
            "status": "delivered",
            "order_date": "2025-04-01",
            "last_update": "2025-04-06",
            "tracking_id": "UPS67890" 
        },
        {
            "id": "400",
            "summary": "Giant Graphic Hoodie",
            "email": "jessenotpinkman@blue-meth.com",
            "status": "shipped",
            "order_date": "2025-04-03",
            "last_update": "2025-04-09",
            "tracking_id": "UPS67890" 
        },
        {
            "id": "401",
            "summary": "Giant Pants",
            "email": "jessenotpinkman@blue-meth.com",
            "status": "processing",
            "order_date": "2025-04-03",
            "last_update": "2025-04-09" 
        }
    ]
}


================================================
FILE: tools/data/dummy_tracking_data.json
================================================
{ 
    "packages": [
        {
            "TrackingNumber": "USPS12345",
            "Delivered": false,
            "Carrier": "USPS",
            "ServiceType": "USPS Ground Advantage<SUP>&#153;</SUP>",
            "PickupDate": "",
            "ScheduledDeliveryDate": "April 14, 2025",
            "ScheduledDeliveryDateInDateTimeFromat": "2025-04-14T00:00:00",
            "StatusCode": "In Transit from Origin Processing",
            "Status": "Departed Post Office",
            "StatusSummary": "Your item has left our acceptance facility and is in transit to a sorting facility on April 10, 2025 at 7:06 am in IRON RIDGE, WI 53035.",
            "Message": "",
            "DeliveredDateTime": "",
            "DeliveredDateTimeInDateTimeFormat": null,
            "SignatureName": "",
            "DestinationCity": "CITY",
            "DestinationState": "ST",
            "DestinationZip": "12345",
            "DestinationCountry": null,
            "EventDate": "2025-04-10T07:06:00",
            "TrackingDetails": [
                {
                    "EventDateTime": "April 10, 2025 7:06 am",
                    "Event": "Departed Post Office",
                    "EventAddress": "IRON RIDGE WI 53035",
                    "State": "WI",
                    "City": "IRON RIDGE",
                    "Zip": "53035",
                    "EventDateTimeInDateTimeFormat": "2025-04-10T07:06:00"
                },
                {
                    "EventDateTime": "April 9, 2025 11:29 am",
                    "Event": "USPS picked up item",
                    "EventAddress": "IRON RIDGE WI 53035",
                    "State": "WI",
                    "City": "IRON RIDGE",
                    "Zip": "53035",
                    "EventDateTimeInDateTimeFormat": "2025-04-09T11:29:00"
                },
                {
                    "EventDateTime": "April 7, 2025 6:29 am",
                    "Event": "Shipping Label Created, USPS Awaiting Item",
                    "EventAddress": "IRON RIDGE WI 53035",
                    "State": "WI",
                    "City": "IRON RIDGE",
                    "Zip": "53035",
                    "EventDateTimeInDateTimeFormat": "2025-04-07T06:29:00"
                }
            ]
        },
        {
            "TrackingNumber": "UPS67890",
            "Delivered": true,
            "Carrier": "UPS",
            "ServiceType": "UPS Ground Saver®",
            "PickupDate": "",
            "ScheduledDeliveryDate": "",
            "ScheduledDeliveryDateInDateTimeFromat": null,
            "StatusCode": "D",
            "Status": "DELIVERED",
            "StatusSummary": "DELIVERED",
            "Message": "",
            "DeliveredDateTime": "20250415 154315",
            "DeliveredDateTimeInDateTimeFormat": "2025-04-15T15:43:15",
            "SignatureName": "",
            "DestinationCity": "CHICAGO",
            "DestinationState": "IL",
            "DestinationZip": "",
            "DestinationCountry": "US",
            "EventDate": "2025-04-15T15:43:15",
            "TrackingDetails": [
                {
                    "EventDateTime": "20250415 154315",
                    "Event": "DELIVERED ",
                    "EventAddress": "CHICAGO IL US",
                    "State": "IL",
                    "City": "CHICAGO",
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-15T15:43:15"
                },
                {
                    "EventDateTime": "20250415 090938",
                    "Event": "Out For Delivery Today",
                    "EventAddress": "Chicago IL US",
                    "State": "IL",
                    "City": "Chicago",
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-15T09:09:38"
                },
                {
                    "EventDateTime": "20250415 074141",
                    "Event": "Loaded on Delivery Vehicle ",
                    "EventAddress": "Chicago IL US",
                    "State": "IL",
                    "City": "Chicago",
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-15T07:41:41"
                },
                {
                    "EventDateTime": "20250415 032200",
                    "Event": "Arrived at Facility",
                    "EventAddress": "Chicago IL US",
                    "State": "IL",
                    "City": "Chicago",
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-15T03:22:00"
                },
                {
                    "EventDateTime": "20250414 223000",
                    "Event": "Departed from Facility",
                    "EventAddress": "Hodgkins IL US",
                    "State": "IL",
                    "City": "Hodgkins",
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-14T22:30:00"
                },
                {
                    "EventDateTime": "20250414 002700",
                    "Event": "Arrived at Facility",
                    "EventAddress": "Hodgkins IL US",
                    "State": "IL",
                    "City": "Hodgkins",
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-14T00:27:00"
                },
                {
                    "EventDateTime": "20250410 211700",
                    "Event": "Departed from Facility",
                    "EventAddress": "Las Vegas NV US",
                    "State": "NV",
                    "City": "Las Vegas",
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-10T21:17:00"
                },
                {
                    "EventDateTime": "20250410 132625",
                    "Event": "Arrived at Facility",
                    "EventAddress": "Las Vegas NV US",
                    "State": "NV",
                    "City": "Las Vegas",
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-10T13:26:25"
                },
                {
                    "EventDateTime": "20250409 100659",
                    "Event": "Shipper created a label, UPS has not received the package yet. ",
                    "EventAddress": "  US",
                    "State": null,
                    "City": null,
                    "Zip": null,
                    "EventDateTimeInDateTimeFormat": "2025-04-09T10:06:59"
                }
            ]
        }
    ]
}


================================================
FILE: tools/data/employee_pto_data.json
================================================
{
  "theCompany": {
    "weLove": "theCompany", 
    "employees": [
      {
        "email": "josh.smith@temporal.io",
        "currentPTOHrs": 400,
        "hrsAddedPerMonth": 8
      },
      {
        "email": "laine@awesome.com",
        "currentPTOHrs": 40,
        "hrsAddedPerMonth": 12
      },
      {
        "email": "steve.this.is.for.you@gmail.com",
        "currentPTOHrs": 4000,
        "hrsAddedPerMonth": 20
      },
      {
        "email": "your_email_here@yourcompany.com",
        "currentPTOHrs": 150,
        "hrsAddedPerMonth": 19
      } 
    ]
  }
}


================================================
FILE: tools/data/find_events_data.json
================================================
{
    "Melbourne": [
      {
        "eventName": "Australian Open",
        "dateFrom": "2025-01-13",
        "dateTo": "2025-01-26",
        "description": "A two-week Grand Slam tennis tournament featuring the world's top players, accompanied by various entertainment options including live music and family-friendly activities."
      },
      {
        "eventName": "Melbourne International Comedy Festival",
        "dateFrom": "2025-03-26",
        "dateTo": "2025-04-20",
        "description": "One of the world's largest comedy festivals, showcasing stand-up, cabaret, theatre, and street performances across numerous city venues."
      },
      {
        "eventName": "Melbourne International Film Festival (MIFF)",
        "dateFrom": "2025-08-07",
        "dateTo": "2025-08-23",
        "description": "Established in 1952, MIFF presents a diverse selection of Australian and international films, including features, documentaries, and shorts."
      },
      {
        "eventName": "Melbourne Fringe Festival",
        "dateFrom": "2025-09-17",
        "dateTo": "2025-10-04",
        "description": "An open-access arts festival featuring a wide array of art forms such as theatre, comedy, music, and digital art across various venues."
      },
      {
        "eventName": "Moomba Festival",
        "dateFrom": "2025-03-07",
        "dateTo": "2025-03-10",
        "description": "Australia's largest free community festival, celebrated over four days during the Labour Day long weekend, including a parade, live music, fireworks, and the famous Birdman Rally along the Yarra River."
      },
      {
        "eventName": "White Night Melbourne",
        "dateFrom": "2025-08-22",
        "dateTo": "2025-08-24",
        "description": "A dusk-to-dawn arts and cultural festival transforming the city with light installations, projections, music, and performances."
      },
      {
        "eventName": "Melbourne Food and Wine Festival",
        "dateFrom": "2025-03-19",
        "dateTo": "2025-03-29",
        "description": "A celebration of Victoria's culinary scene, featuring food and wine events, masterclasses, and dining experiences."
      }
    ],
    "Sydney": [
      {
        "eventName": "Sydney Gay and Lesbian Mardi Gras",
        "dateFrom": "2025-02-14",
        "dateTo": "2025-03-01",
        "description": "One of the largest LGBTQ+ festivals globally, featuring a vibrant parade, parties, and cultural events celebrating diversity and inclusion."
      },
      {
        "eventName": "Vivid Sydney",
        "dateFrom": "2025-05-22",
        "dateTo": "2025-06-13",
        "description": "An annual festival of light, music, and ideas, transforming the city with mesmerizing light installations and projections."
      },
      {
        "eventName": "Sydney Festival",
        "dateFrom": "2025-01-08",
        "dateTo": "2025-01-26",
        "description": "A major arts festival presenting a diverse program of theatre, dance, music, and visual arts across the city."
      },
      {
        "eventName": "Sculpture by the Sea, Bondi",
        "dateFrom": "2025-10-23",
        "dateTo": "2025-11-09",
        "description": "An outdoor sculpture exhibition along the Bondi to Tamarama coastal walk, showcasing works by Australian and international artists."
      },
      {
        "eventName": "Sydney Writers' Festival",
        "dateFrom": "2025-04-27",
        "dateTo": "2025-05-03",
        "description": "An annual literary festival featuring talks, panel discussions, and workshops with acclaimed authors and thinkers."
      },
      {
        "eventName": "Sydney Film Festival",
        "dateFrom": "2025-06-04",
        "dateTo": "2025-06-15",
        "description": "One of the longest-running film festivals in the world, showcasing a diverse selection of local and international films."
      }
    ],
    "Auckland": [
      {
        "eventName": "Pasifika Festival",
        "dateFrom": "2025-03-08",
        "dateTo": "2025-03-09",
        "description": "The largest Pacific Islands-themed festival globally, celebrating the diverse cultures of the Pacific with traditional cuisine, performances, and arts."
      },
      {
        "eventName": "Auckland Arts Festival",
        "dateFrom": "2025-03-11",
        "dateTo": "2025-03-29",
        "description": "A biennial multi-arts festival showcasing local and international artists in theatre, dance, music, and visual arts."
      },
      {
        "eventName": "Auckland Writers Festival",
        "dateFrom": "2025-05-13",
        "dateTo": "2025-05-18",
        "description": "An annual event bringing together international and local writers for discussions, readings, and workshops."
      },
      {
        "eventName": "Auckland Diwali Festival",
        "dateFrom": "2025-10-26",
        "dateTo": "2025-10-27",
        "description": "A vibrant celebration of Indian culture and the Hindu festival of Diwali, featuring performances, food stalls, and traditional activities."
      }
    ],
    "Brisbane": [
      {
        "eventName": "Brisbane Festival",
        "dateFrom": "2025-09-05",
        "dateTo": "2025-09-26",
        "description": "A major international arts festival featuring theatre, music, dance, and visual arts, culminating in the Riverfire fireworks display."
      },
      {
        "eventName": "NRL Magic Round",
        "dateFrom": "2025-05-02",
        "dateTo": "2025-05-04",
        "description": "A rugby league extravaganza where all NRL matches for the round are played at Suncorp Stadium, attracting fans nationwide."
      },
      {
        "eventName": "Brisbane International Film Festival",
        "dateFrom": "2025-10-01",
        "dateTo": "2025-10-11",
        "description": "Showcasing a curated selection of films from around the world, including premieres and special events."
      },
      {
        "eventName": "Brisbane Comedy Festival",
        "dateFrom": "2025-02-22",
        "dateTo": "2025-03-24",
        "description": "A month-long comedy festival featuring local and international comedians in stand-up, sketch, and improv performances."
      },
      {
        "eventName": "Brisbane Writers Festival",
        "dateFrom": "2025-09-05",
        "dateTo": "2025-09-08",
        "description": "An annual literary festival celebrating books, writing, and ideas with author talks, panel discussions, and workshops."
      },
      {
        "eventName": "Brisbane Asia Pacific Film Festival",
        "dateFrom": "2025-11-29",
        "dateTo": "2025-12-08",
        "description": "Showcasing the best cinema from the Asia Pacific region, including features, documentaries, and short films."
      }
    ],
    "Perth": [
      {
        "eventName": "Perth Festival",
        "dateFrom": "2025-02-07",
        "dateTo": "2025-03-01",
        "description": "Australia's longest-running cultural festival, offering a diverse program of music, theatre, dance, literature, and visual arts."
      },
      {
        "eventName": "Fringe World Festival",
        "dateFrom": "2025-01-16",
        "dateTo": "2025-02-15",
        "description": "One of the largest fringe festivals globally, featuring a vast array of performances including comedy, cabaret, theatre, and street arts."
      },
      {
        "eventName": "Sculpture by the Sea",
        "dateFrom": "2025-03-06",
        "dateTo": "2025-03-23",
        "description": "An annual outdoor sculpture exhibition along Cottesloe Beach, showcasing works from Australian and international artists."
      },
      {
        "eventName": "Revelation Perth International Film Festival",
        "dateFrom": "2025-07-03",
        "dateTo": "2025-07-13",
        "description": "A showcase of independent cinema, featuring a diverse selection of films, documentaries, and short films."
      },
      {
        "eventName": "Perth Comedy Festival",
        "dateFrom": "2025-04-22",
        "dateTo": "2025-05-19",
        "description": "A month-long comedy festival featuring local and international comedians in stand-up, sketch, and improv performances."
      }
    ],
    "Adelaide": [
      {
        "eventName": "Adelaide Festival",
        "dateFrom": "2025-02-28",
        "dateTo": "2025-03-15",
        "description": "A premier arts festival offering a rich program of theatre, music, dance, and visual arts from renowned international and local artists."
      },
      {
        "eventName": "Adelaide Fringe",
        "dateFrom": "2025-02-14",
        "dateTo": "2025-03-15",
        "description": "The largest open-access arts festival in the Southern Hemisphere, featuring thousands of performances across various genres and venues."
      },
      {
        "eventName": "SALA Festival",
        "dateFrom": "2025-08-01",
        "dateTo": "2025-08-31",
        "description": "South Australia's largest visual arts festival, showcasing the work of local artists in exhibitions, workshops, and events."
      },
      {
        "eventName": "OzAsia Festival",
        "dateFrom": "2025-09-25",
        "dateTo": "2025-10-11",
        "description": "A celebration of Asian arts and culture, featuring performances, exhibitions, and events from across the region."
      },
      {
        "eventName": "Adelaide Film Festival",
        "dateFrom": "2025-10-16",
        "dateTo": "2025-10-26",
        "description": "Showcasing a diverse selection of Australian and international films, including features, documentaries, and shorts."
      },
      {
        "eventName": "Adelaide Writers' Week",
        "dateFrom": "2025-03-01",
        "dateTo": "2025-03-06",
        "description": "An annual literary festival featuring talks, panel discussions, and readings by acclaimed authors and thinkers."
      }
    ],
    "Wellington": [
      {
        "eventName": "New Zealand Festival of the Arts",
        "dateFrom": "2025-02-21",
        "dateTo": "2025-03-15",
        "description": "The nation's largest celebration of contemporary arts and culture, featuring a diverse range of performances and exhibitions across various venues in Wellington.",
        "url": "https://www.festival.nz/"
      },
      {
        "eventName": "Wellington Jazz Festival",
        "dateFrom": "2025-06-05",
        "dateTo": "2025-06-09",
        "description": "A five-day festival showcasing local and international jazz musicians in concerts, workshops, and community events.",
        "url": "https://www.jazzfestival.co.nz/"
      },
      {
        "eventName": "Wellington on a Plate",
        "dateFrom": "2025-08-01",
        "dateTo": "2025-08-16",
        "description": "A culinary festival celebrating the city's food and beverage industry with special menus, events, and culinary experiences."
      },
      {
        "eventName": "CubaDupa",
        "dateFrom": "2025-03-28",
        "dateTo": "2025-03-29",
        "description": "A vibrant street festival in Wellington's Cuba Street, featuring music, dance, street performers, and food stalls."
      },
      {
        "eventName": "Wellington Pasifika Festival",
        "dateFrom": "2025-01-18",
        "dateTo": "2025-01-19",
        "description": "A celebration of Pacific Island culture with traditional performances, food stalls, and arts and crafts."
      }
    ]
  }


================================================
FILE: tools/ecommerce/get_order.py
================================================
import json
from pathlib import Path


# this is made to demonstrate functionality but it could just as durably be an API call
# called as part of a temporal activity with automatic retries
def get_order(args: dict) -> dict:
    order_id = args.get("order_id")

    file_path = (
        Path(__file__).resolve().parent.parent / "data" / "customer_order_data.json"
    )
    if not file_path.exists():
        return {"error": "Data file not found."}

    with open(file_path, "r") as file:
        data = json.load(file)
    order_list = data["orders"]

    for order in order_list:
        if order["id"] == order_id:
            return order

    return_msg = "Order " + order_id + " not found."
    return {"error": return_msg}



================================================
FILE: tools/ecommerce/list_orders.py
================================================
import json
from pathlib import Path


def sorting(e):
    return e["order_date"]


def list_orders(args: dict) -> dict:
    email_address = args.get("email_address")

    file_path = (
        Path(__file__).resolve().parent.parent / "data" / "customer_order_data.json"
    )
    if not file_path.exists():
        return {"error": "Data file not found."}

    with open(file_path, "r") as file:
        data = json.load(file)
    order_list = data["orders"]

    rtn_order_list = []
    for order in order_list:
        if order["email"] == email_address:
            rtn_order_list.append(order)

    if len(rtn_order_list) > 0:
        rtn_order_list.sort(key=sorting)
        return {"orders": rtn_order_list}
    else:
        return_msg = "No orders for customer " + email_address + " found."
        return {"error": return_msg}



================================================
FILE: tools/ecommerce/track_package.py
================================================
import http
import json
import os
from pathlib import Path


# Send back dummy data in the correct format - to use the real API, 1) change this to be track_package_fake and 2) change the below track_package_real to be track_package
def track_package(args: dict) -> dict:
    tracking_id = args.get("tracking_id")
    file_path = (
        Path(__file__).resolve().parent.parent / "data" / "dummy_tracking_data.json"
    )
    if not file_path.exists():
        return {"error": "Data file not found."}

    with open(file_path, "r") as file:
        data = json.load(file)
    package_list = data["packages"]

    for package in package_list:
        if package["TrackingNumber"] == tracking_id:
            scheduled_delivery_date = package["ScheduledDeliveryDate"]
            carrier = package["Carrier"]
            status_summary = package["StatusSummary"]
            tracking_details = package.get("TrackingDetails", [])
            last_tracking_update = ""
            if (
                tracking_details
                and tracking_details is not None
                and tracking_details[0] is not None
            ):
                last_tracking_update = tracking_details[0][
                    "EventDateTimeInDateTimeFormat"
                ]

            tracking_link = ""
            if carrier == "USPS":
                tracking_link = f"https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1={tracking_id}"
            elif carrier == "UPS":
                tracking_link = (
                    f"https://www.ups.com/track?track=yes&trackNums={tracking_id}"
                )

            return {
                "scheduled_delivery_date": scheduled_delivery_date,
                "carrier": carrier,
                "status_summary": status_summary,
                "tracking_link": tracking_link,
                "last_tracking_update": last_tracking_update,
            }

    return_msg = "Package not found with tracking info " + tracking_id
    return {"error": return_msg}


"""Format of response:
{
    "TrackingNumber": "",
    "Delivered": false,
    "Carrier": "USPS",
    "ServiceType": "USPS Ground Advantage<SUP>&#153;</SUP>",
    "PickupDate": "",
    "ScheduledDeliveryDate": "April 14, 2025",
    "ScheduledDeliveryDateInDateTimeFromat": "2025-04-14T00:00:00",
    "StatusCode": "In Transit from Origin Processing",
    "Status": "Departed Post Office",
    "StatusSummary": "Your item has left our acceptance facility and is in transit to a sorting facility on April 10, 2025 at 7:06 am in IRON RIDGE, WI 53035.",
    "Message": "",
    "DeliveredDateTime": "",
    "DeliveredDateTimeInDateTimeFormat": null,
    "SignatureName": "",
    "DestinationCity": "CITY",
    "DestinationState": "ST",
    "DestinationZip": "12345",
    "DestinationCountry": null,
    "EventDate": "2025-04-10T07:06:00",
    "TrackingDetails": [
        {
            "EventDateTime": "April 10, 2025 7:06 am",
            "Event": "Departed Post Office",
            "EventAddress": "IRON RIDGE WI 53035",
            "State": "WI",
            "City": "IRON RIDGE",
            "Zip": "53035",
            "EventDateTimeInDateTimeFormat": "2025-04-10T07:06:00"
        },
        {
            "EventDateTime": "April 9, 2025 11:29 am",
            "Event": "USPS picked up item",
            "EventAddress": "IRON RIDGE WI 53035",
            "State": "WI",
            "City": "IRON RIDGE",
            "Zip": "53035",
            "EventDateTimeInDateTimeFormat": "2025-04-09T11:29:00"
        },
        {
            "EventDateTime": "April 7, 2025 6:29 am",
            "Event": "Shipping Label Created, USPS Awaiting Item",
            "EventAddress": "IRON RIDGE WI 53035",
            "State": "WI",
            "City": "IRON RIDGE",
            "Zip": "53035",
            "EventDateTimeInDateTimeFormat": "2025-04-07T06:29:00"
        }
    ]
}
"""


def track_package_real(args: dict) -> dict:
    tracking_id = args.get("tracking_id")

    api_key = os.getenv("RAPIDAPI_KEY")
    api_host = os.getenv("RAPIDAPI_HOST_PACKAGE", "trackingpackage.p.rapidapi.com")

    conn = http.client.HTTPSConnection(api_host)
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host,
        "Authorization": "Basic Ym9sZGNoYXQ6TGZYfm0zY2d1QzkuKz9SLw==",
    }

    path = f"/TrackingPackage?trackingNumber={tracking_id}"

    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    data = res.read()
    data_decoded = data.decode("utf-8")
    conn.close()

    try:
        json_data = json.loads(data_decoded)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}

    scheduled_delivery_date = json_data["ScheduledDeliveryDate"]
    carrier = json_data["Carrier"]
    status_summary = json_data["StatusSummary"]
    tracking_details = json_data.get("TrackingDetails", [])
    last_tracking_update = ""
    if (
        tracking_details
        and tracking_details is not None
        and tracking_details[0] is not None
    ):
        last_tracking_update = tracking_details[0]["EventDateTimeInDateTimeFormat"]
    tracking_link = ""
    if carrier == "USPS":
        tracking_link = (
            f"https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1={tracking_id}"
        )
    elif carrier == "UPS":
        tracking_link = f"https://www.ups.com/track?track=yes&trackNums={tracking_id}"

    return {
        "scheduled_delivery_date": scheduled_delivery_date,
        "carrier": carrier,
        "status_summary": status_summary,
        "tracking_link": tracking_link,
        "last_tracking_update": last_tracking_update,
    }



================================================
FILE: tools/fin/check_account_valid.py
================================================
import json
from pathlib import Path


# this is made to demonstrate functionality but it could just as durably be an API call
# called as part of a temporal activity with automatic retries
def check_account_valid(args: dict) -> dict:
    email = args.get("email")
    account_id = args.get("account_id")

    file_path = (
        Path(__file__).resolve().parent.parent / "data" / "customer_account_data.json"
    )
    if not file_path.exists():
        return {"error": "Data file not found."}

    with open(file_path, "r") as file:
        data = json.load(file)
    account_list = data["accounts"]

    for account in account_list:
        if account["email"] == email or account["account_id"] == account_id:
            return {"status": "account valid"}

    return_msg = (
        "Account not found with email address "
        + email
        + " or account ID: "
        + account_id
    )
    return {"error": return_msg}



================================================
FILE: tools/fin/get_account_balances.py
================================================
import json
from pathlib import Path


# this is made to demonstrate functionality but it could just as durably be an API call
# this assumes it's a valid account - use check_account_valid() to verify that first
def get_account_balance(args: dict) -> dict:
    account_key = args.get("email_address_or_account_ID")

    file_path = (
        Path(__file__).resolve().parent.parent / "data" / "customer_account_data.json"
    )
    if not file_path.exists():
        return {"error": "Data file not found."}

    with open(file_path, "r") as file:
        data = json.load(file)
    account_list = data["accounts"]

    for account in account_list:
        if account["email"] == account_key or account["account_id"] == account_key:
            return {
                "name": account["name"],
                "email": account["email"],
                "account_id": account["account_id"],
                "checking_balance": account["checking_balance"],
                "savings_balance": account["savings_balance"],
                "bitcoin_balance": account["bitcoin_balance"],
                "account_creation_date": account["account_creation_date"],
            }

    return_msg = "Account not found with for " + account_key
    return {"error": return_msg}



================================================
FILE: tools/fin/move_money.py
================================================
import json
import os
from dataclasses import dataclass
from pathlib import Path

from temporalio.exceptions import WorkflowAlreadyStartedError

from shared.config import get_temporal_client

# enums for the java enum
# class ExecutionScenarios(Enum):
#     HAPPY_PATH = 0
#     ADVANCED_VISIBILITY = auto() # 1
#     HUMAN_IN_LOOP = auto()       # 2
#     API_DOWNTIME = auto()        # 3
#     BUG_IN_WORKFLOW = auto()     # 4
#     INVALID_ACCOUNT = auto()     # 5


# these dataclasses are for calling the Temporal Workflow
# Python equivalent of the workflow we're calling's Java WorkflowParameterObj
@dataclass
class MoneyMovementWorkflowParameterObj:
    amount: int  # Using snake_case as per Python conventions
    scenario: str


# this is made to demonstrate functionality but it could just as durably be an API call
# this assumes it's a valid account - use check_account_valid() to verify that first
async def move_money(args: dict) -> dict:
    account_key = args.get("email_address_or_account_ID")
    account_type: str = args.get("accounttype")
    amount = args.get("amount")
    destinationaccount = args.get("destinationaccount")

    file_path = (
        Path(__file__).resolve().parent.parent / "data" / "customer_account_data.json"
    )
    if not file_path.exists():
        return {"error": "Data file not found."}

    with open(file_path, "r") as file:
        data = json.load(file)
    account_list = data["accounts"]

    for account in account_list:
        if account["email"] == account_key or account["account_id"] == account_key:
            amount_str: str = str(amount)
            from_account_combo = account_key + account_type

            transfer_workflow_id = await start_workflow(
                amount_cents=str_dollars_to_cents(amount_str),
                from_account_name=from_account_combo,
                to_account_name=destinationaccount,
            )

            if account_type.casefold() == "checking":
                from_key = "checking_balance"
            elif account_type.casefold() == "savings":
                from_key = "savings_balance"
            else:
                return_msg = "Money order for account types other than checking or savings is not implemented."
                return {"error": return_msg}

            to_key = (
                "savings_balance"
                if destinationaccount.casefold() == "savings"
                else "checking_balance"
            )

            # Update from-account balance
            from_balance = float(str_dollars_to_cents(str(account[from_key])))
            from_balance -= float(str_dollars_to_cents(amount_str))
            account[from_key] = str(from_balance / 100)

            # Update destination-account balance
            to_balance = float(str_dollars_to_cents(str(account[to_key])))
            to_balance += float(str_dollars_to_cents(amount_str))
            account[to_key] = str(to_balance / 100)

            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            return {
                "status": "money movement complete",
                "confirmation id": transfer_workflow_id,
                "new_balance": account[from_key],
                "destination_balance": account[to_key],
            }

    return_msg = "Account not found with for " + account_key
    return {"error": return_msg}


# Async function to start workflow
async def start_workflow(
    amount_cents: int, from_account_name: str, to_account_name: str
) -> str:
    start_real_workflow = os.getenv("FIN_START_REAL_WORKFLOW")
    if start_real_workflow is not None and start_real_workflow.lower() == "false":
        START_REAL_WORKFLOW = False
    else:
        START_REAL_WORKFLOW = True

    if START_REAL_WORKFLOW:
        # Connect to Temporal
        client = await get_temporal_client()
        # Create the parameter object
        params = MoneyMovementWorkflowParameterObj(
            amount=amount_cents, scenario="HAPPY_PATH"
        )

        workflow_id = (
            "TRANSFER-ACCT-" + from_account_name + "-TO-" + to_account_name
        )  # business-relevant workflow ID

        try:
            handle = await client.start_workflow(
                "moneyTransferWorkflow",  # Workflow name
                params,  # Workflow parameters
                id=workflow_id,
                task_queue="MoneyTransferJava",  # Task queue name
            )
            return handle.id
        except WorkflowAlreadyStartedError:
            existing_handle = client.get_workflow_handle(workflow_id=workflow_id)
            return existing_handle.id
    else:
        return (
            "TRANSFER-ACCT-" + from_account_name + "-TO-" + to_account_name + "not-real"
        )


# cleans a string dollar amount description to cents value
def str_dollars_to_cents(dollar_str: str) -> int:
    try:
        # Remove '$' and any whitespace
        cleaned_str = dollar_str.replace("$", "").strip()

        # Handle empty string or invalid input
        if not cleaned_str:
            raise ValueError("Empty amount provided")

        # Convert to float and then to cents
        amount = float(cleaned_str)
        if amount < 0:
            raise ValueError("Negative amounts not allowed")

        return int(amount * 100)
    except ValueError as e:
        raise ValueError(f"Invalid dollar amount format: {dollar_str}") from e



================================================
FILE: tools/fin/submit_loan_application.py
================================================
import os
from dataclasses import dataclass
from datetime import date

from temporalio import common
from temporalio.client import WithStartWorkflowOperation, WorkflowUpdateFailedError

from shared.config import get_temporal_client


# Define data structures to match the Java workflow's expected input/output
# see https://github.com/temporal-sa/temporal-latency-optimization-scenarios for more details
@dataclass
class TransactionRequest:
    amount: float
    sourceAccount: str
    targetAccount: str


@dataclass
class TxResult:
    transactionId: str
    status: str


# demonstrate starting a workflow and early return pattern while the workflow continues
async def submit_loan_application(args: dict) -> dict:
    account_key = args.get("email_address_or_account_ID")
    amount = args.get("amount")

    loan_status: dict = await start_workflow(amount=amount, account_name=account_key)

    if loan_status.get("error") is None:
        return {
            "status": loan_status.get("loan_application_status"),
            "detailed_status": loan_status.get("application_details"),
            "next_step": loan_status.get("advisement"),
            "confirmation_id": loan_status.get("transaction_id"),
        }
    else:
        print(loan_status)
        return loan_status


# Async function to start workflow
async def start_workflow(
    amount: str,
    account_name: str,
) -> dict:
    start_real_workflow = os.getenv("FIN_START_REAL_WORKFLOW")
    if start_real_workflow is not None and start_real_workflow.lower() == "false":
        # START_REAL_WORKFLOW = False
        return {
            "loan_application_status": "applied",
            "application_details": "loan application is submitted and initial validation is complete",
            "transaction_id": "APPLICATION" + account_name,
            "advisement": "You'll receive a confirmation for final approval in three business days",
        }
    else:
        # START_REAL_WORKFLOW = True
        # Connect to Temporal
        client = await get_temporal_client()

        # Define the workflow ID and task queue
        workflow_id = (
            "LOAN_APPLICATION-" + account_name + "-" + date.today().strftime("%Y-%m-%d")
        )
        task_queue = "LatencyOptimizationTEST"

        # Create a TransactionRequest (matching the Java workflow's expected input)
        tx_request = TransactionRequest(
            amount=float(amount),
            targetAccount=account_name,
            sourceAccount=account_name,
        )

        start_op = WithStartWorkflowOperation(
            "TransactionWorkflowLocalBeforeUpdate",
            tx_request,
            id=workflow_id,
            id_conflict_policy=common.WorkflowIDConflictPolicy.USE_EXISTING,
            task_queue=task_queue,
        )

        try:
            print("trying update-with-start")
            tx_result = TxResult(
                await client.execute_update_with_start_workflow(
                    "returnInitResult",
                    start_workflow_operation=start_op,
                )
            )
        except WorkflowUpdateFailedError:
            print("aww man got exception WorkflowUpdateFailedError")
            tx_result = None
            return_msg = "Loan could not be processed for " + account_name
            return {"error": return_msg}

        workflow_handle = await start_op.workflow_handle()
        print(f"Workflow started with ID: {workflow_handle.id}")
        print(tx_result)

        print(
            f"Update result: Transaction ID = {tx_result.transactionId}, Message = {tx_result.status}"
        )

        # Optionally, wait for the workflow to complete and get the final result
        # final_result = await handle.result()
        # print(f"Workflow completed with result: {final_result}")

        # return {'status': loan_status.get("loan_status"), 'detailed_status': loan_status.get("results"), 'next_step': loan_status.get("advisement"), 'confirmation_id': loan_status.get("workflowID")}
        return {
            "loan_application_status": "applied",
            "application_details": "loan application is submitted and initial validation is complete",
            "transaction_id": tx_result.transactionId,
            "advisement": "You'll receive a confirmation for final approval in three business days",
        }



================================================
FILE: tools/food/add_to_cart.py
================================================
def add_to_cart(args: dict) -> dict:
    """
    Simple stateless cart tool for demo purposes.
    In production, this would use proper session storage or database.
    """
    customer_email = args.get("customer_email")
    item_name = args.get("item_name")
    item_price = float(args.get("item_price", 0))
    quantity = int(args.get("quantity", 1))
    stripe_product_id = args.get("stripe_product_id")

    # Basic validation
    if not customer_email:
        return {"error": "Customer email is required"}
    if not item_name:
        return {"error": "Item name is required"}
    if item_price <= 0:
        return {"error": "Item price must be greater than 0"}
    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}

    # For demo purposes, just acknowledge the addition
    # In a real system, this would store to session/database
    return {
        "status": "success",
        "message": f"Added {quantity} x {item_name} (${item_price}) to cart for {customer_email}",
        "item_added": {
            "name": item_name,
            "price": item_price,
            "quantity": quantity,
            "stripe_product_id": stripe_product_id,
        },
    }



================================================
FILE: tools/food/setup/archive_food_products.py
================================================
import os

from dotenv import load_dotenv


def delete_food_ordering_products():
    """Archive all Stripe products with metadata use_case = food_ordering_demo (since products with prices cannot be deleted)."""
    import stripe

    # Load environment variables and configure stripe
    load_dotenv(override=True)
    stripe.api_key = os.getenv("STRIPE_API_KEY")

    if not stripe.api_key:
        print("Error: STRIPE_API_KEY not found in environment variables")
        return

    try:
        # Search for products with food_ordering_demo use_case
        products = stripe.Product.search(
            query="metadata['use_case']:'food_ordering_demo'", limit=100
        )

        if not products.data:
            print("No products found with use_case = food_ordering_demo")
            return

        archived_count = 0

        for product in products.data:
            try:
                # Archive the product (set active=False)
                stripe.Product.modify(product.id, active=False)
                print(f"Archived product: {product.name} (ID: {product.id})")
                archived_count += 1

            except Exception as e:
                print(
                    f"Error archiving product {product.name} (ID: {product.id}): {str(e)}"
                )

        print(f"\nSuccessfully archived {archived_count} products")

    except Exception as e:
        print(f"Error searching for products: {str(e)}")


if __name__ == "__main__":
    delete_food_ordering_products()



================================================
FILE: tools/food/setup/create_stripe_products.py
================================================
import json
import os

from dotenv import load_dotenv


def create_stripe_products():
    """Create Stripe products and prices from the stripe_pizza_products.json file."""
    import stripe

    # Load environment variables and configure stripe
    load_dotenv(override=True)
    stripe.api_key = os.getenv("STRIPE_API_KEY")

    if not stripe.api_key:
        print("Error: STRIPE_API_KEY not found in environment variables")
        return

    # Load the products data
    current_dir = os.path.dirname(__file__)
    products_file = os.path.join(current_dir, "stripe_pizza_products.json")

    with open(products_file, "r") as f:
        products_data = json.load(f)

    # Filter for food ordering demo products only
    food_products = [
        p
        for p in products_data
        if p.get("metadata", {}).get("use_case") == "food_ordering_demo"
    ]

    created_products = []

    for product_data in food_products:
        try:
            # Create the product with relevant fields
            product = stripe.Product.create(
                name=product_data["name"],
                description=product_data.get("description"),
                images=product_data.get("images", []),
                metadata=product_data.get("metadata", {}),
                type=product_data.get("type", "service"),
                active=product_data.get("active", True),
            )

            # Create price for the product if price_info exists
            price_info = product_data.get("price_info")
            if price_info:
                price_amount = price_info.get("amount")
                currency = price_info.get("currency", "usd")

                price = stripe.Price.create(
                    currency=currency, unit_amount=price_amount, product=product.id
                )

                # Set this price as the default price for the product
                stripe.Product.modify(product.id, default_price=price.id)

                print(
                    f"Created product: {product.name} (ID: {product.id}) with default price ${price_amount/100:.2f}"
                )

                created_products.append(
                    {
                        "name": product.name,
                        "id": product.id,
                        "price_id": price.id,
                        "price_amount": price_amount,
                        "original_id": product_data["id"],
                    }
                )
            else:
                print(
                    f"Created product: {product.name} (ID: {product.id}) - No price defined"
                )
                created_products.append(
                    {
                        "name": product.name,
                        "id": product.id,
                        "original_id": product_data["id"],
                    }
                )

        except Exception as e:
            print(f"Error creating product {product_data['name']}: {str(e)}")

    print(f"\nSuccessfully created {len(created_products)} products with prices")
    return created_products


if __name__ == "__main__":
    create_stripe_products()



================================================
FILE: tools/food/setup/stripe_pizza_products.json
================================================
[
    {
        "id": "prod_SSWirxxS5A8gcT",
        "object": "product",
        "active": true,
        "attributes": [],
        "created": 1749360061,
        "default_price": "price_1RXbfGKVZbzw7QA57Mj1akGI",
        "description": "A large size bottle of cola.",
        "images": [
            "https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfbDJxckJKMDRnT1dDc253OHlZNWNkZkY5006Xg07kHT"
        ],
        "livemode": false,
        "marketing_features": [],
        "metadata": {
            "use_case": "food_ordering_demo"
        },
        "name": "Soda",
        "price_info": {
            "amount": 349,
            "currency": "usd"
        },
        "package_dimensions": null,
        "shippable": null,
        "statement_descriptor": null,
        "tax_code": null,
        "type": "service",
        "unit_label": null,
        "updated": 1749360062,
        "url": null
    },
    {
        "id": "prod_SSWhxv3tUy1YOG",
        "object": "product",
        "active": true,
        "attributes": [],
        "created": 1749359978,
        "default_price": "price_1RXbdvKVZbzw7QA5ARomQvaf",
        "description": "Our warm, crusty bread is generously spread with a savory garlic butter and toasted to golden perfection. It's the ideal aromatic and flavorful side to accompany your main course.",
        "images": [
            "https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfWTdIZTBkUjNZNFQ1ZEhSVG9nRnduY1pS00XVgLRRZD"
        ],
        "livemode": false,
        "marketing_features": [],
        "metadata": {
            "use_case": "food_ordering_demo"
        },
        "name": "Garlic Bread",
        "price_info": {
            "amount": 799,
            "currency": "usd"
        },
        "package_dimensions": null,
        "shippable": null,
        "statement_descriptor": null,
        "tax_code": null,
        "type": "service",
        "unit_label": null,
        "updated": 1749360084,
        "url": null
    },
    {
        "id": "prod_SSWgXa5bwUFCJs",
        "object": "product",
        "active": true,
        "attributes": [],
        "created": 1749359922,
        "default_price": "price_1RXbd0KVZbzw7QA5Nq36vdLW",
        "description": "A tribute to Italian simplicity, this pizza is topped with fresh mozzarella, a vibrant tomato sauce, and fragrant basil leaves. Each bite delivers a clean and authentic taste of Italy's most famous flavors.",
        "images": [
            "https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfamdmTXBFbzY0TW9rS2N0c2g0Tml2SERL00Evl60Ttq"
        ],
        "livemode": false,
        "marketing_features": [],
        "metadata": {
            "use_case": "food_ordering_demo"
        },
        "name": "Margherita Pizza",
        "price_info": {
            "amount": 1699,
            "currency": "usd"
        },
        "package_dimensions": null,
        "shippable": null,
        "statement_descriptor": null,
        "tax_code": null,
        "type": "service",
        "unit_label": null,
        "updated": 1749359998,
        "url": null
    },
    {
        "id": "prod_SSWf738UqIJzzi",
        "object": "product",
        "active": true,
        "attributes": [],
        "created": 1749359845,
        "default_price": "price_1RXbbmKVZbzw7QA53EkjV2nB",
        "description": "A timeless classic featuring a generous layer of savory pepperoni over rich tomato sauce and melted mozzarella cheese. It's the perfect choice for those who love a bold, meaty flavor on a perfectly baked crust.",
        "images": [
            "https://files.stripe.com/links/MDB8YWNjdF8xTkJPTHVLVlpienc3UUE1fGZsX3Rlc3RfcGRHc0c4cEZYWmR2bm0zOHBOa0FWMk5t008QmCJoWr"
        ],
        "livemode": false,
        "marketing_features": [],
        "metadata": {
            "use_case": "food_ordering_demo"
        },
        "name": "Pepperoni Pizza",
        "price_info": {
            "amount": 2299,
            "currency": "usd"
        },
        "package_dimensions": null,
        "shippable": null,
        "statement_descriptor": null,
        "tax_code": null,
        "type": "service",
        "unit_label": null,
        "updated": 1749359846,
        "url": null
    },
    {
        "id": "prod_SGMXBnatLlkJ4d",
        "object": "product",
        "active": true,
        "attributes": [],
        "created": 1746554502,
        "default_price": "price_1RLpoJKVZbzw7QA5ra76Fk6g",
        "description": null,
        "images": [],
        "livemode": false,
        "marketing_features": [],
        "metadata": {},
        "name": "ACME Scooter Token",
        "package_dimensions": null,
        "shippable": null,
        "statement_descriptor": null,
        "tax_code": null,
        "type": "service",
        "unit_label": null,
        "updated": 1746554503,
        "url": null
    },
    {
        "id": "prod_NxJPcqTWzXk45K",
        "object": "product",
        "active": true,
        "attributes": [],
        "created": 1684961969,
        "default_price": null,
        "description": "$12/Month subscription",
        "images": [],
        "livemode": false,
        "marketing_features": [],
        "metadata": {},
        "name": "Starter Subscription",
        "package_dimensions": null,
        "shippable": null,
        "statement_descriptor": null,
        "tax_code": null,
        "type": "service",
        "unit_label": null,
        "updated": 1684961969,
        "url": null
    },
    {
        "id": "prod_NxJ4KvyENd0uUu",
        "object": "product",
        "active": true,
        "attributes": [],
        "created": 1684960731,
        "default_price": null,
        "description": "Created with the Stripe CLI",
        "images": [],
        "livemode": false,
        "marketing_features": [],
        "metadata": {},
        "name": "Temporal Money Transfer",
        "package_dimensions": null,
        "shippable": null,
        "statement_descriptor": null,
        "tax_code": null,
        "type": "service",
        "unit_label": null,
        "updated": 1684960731,
        "url": null
    }
]


================================================
FILE: tools/hr/book_pto.py
================================================
def book_pto(args: dict) -> dict:
    email = args.get("email")
    start_date = args.get("start_date")
    end_date = args.get("end_date")

    print(
        f"[BookPTO] Totally would send an email confirmation of PTO from {start_date} to {end_date} to {email} here!"
    )

    return {"status": "success"}



================================================
FILE: tools/hr/checkpaybankstatus.py
================================================
def checkpaybankstatus(args: dict) -> dict:
    email = args.get("email")

    if email == "grinch@grinch.com":
        print("THE GRINCH IS FOUND!")
        return {"status": "no money for the grinch"}

    # could do logic here or look up data but for now everyone but the grinch is getting paid
    return_msg = "connected"
    return {"status": return_msg}



================================================
FILE: tools/hr/current_pto.py
================================================
import json
from pathlib import Path


def current_pto(args: dict) -> dict:
    email = args.get("email")

    file_path = (
        Path(__file__).resolve().parent.parent / "data" / "employee_pto_data.json"
    )
    if not file_path.exists():
        return {"error": "Data file not found."}

    data = json.load(open(file_path))
    employee_list = data["theCompany"]["employees"]

    for employee in employee_list:
        if employee["email"] == email:
            num_hours = int(employee["currentPTOHrs"])
            num_days = float(num_hours / 8)
            return {
                "num_hours": num_hours,
                "num_days": num_days,
            }

    return_msg = "Employee not found with email address " + email
    return {"error": return_msg}



================================================
FILE: tools/hr/future_pto_calc.py
================================================
import json
from datetime import date, datetime
from pathlib import Path

import pandas
from dateutil.relativedelta import relativedelta


def future_pto_calc(args: dict) -> dict:
    file_path = (
        Path(__file__).resolve().parent.parent / "data" / "employee_pto_data.json"
    )
    if not file_path.exists():
        return {"error": "Data file not found."}

    start_date = datetime.strptime(args.get("start_date"), "%Y-%m-%d").date()
    end_date = datetime.strptime(args.get("end_date"), "%Y-%m-%d").date()
    email = args.get("email")

    # Next, set up the ability to calculate how much PTO will be added to the user's total by the start of the PTO request
    today = date.today()

    if today > start_date:
        return_msg = (
            "PTO start date " + args.get("start_date") + "cannot be in the past"
        )
        return {"error": return_msg}

    if end_date < start_date:
        return_msg = (
            "PTO end date "
            + args.get("end_date")
            + " must be after PTO start date "
            + args.get("start_date")
        )
        return {"error": return_msg}

    # Get the number of business days, and then business hours (assume 8 hr biz day), included in the PTO request
    biz_days_of_request = len(
        pandas.bdate_range(start=start_date, end=end_date, inclusive="both")
    )
    if biz_days_of_request == 0:
        return_msg = (
            "There are no business days between "
            + args.get("start_date")
            + " and "
            + args.get("end_date")
        )
        return {"error": return_msg}
    biz_hours_of_request = biz_days_of_request * 8

    # Assume PTO is added on the first of every month - month math compares rolling dates, so compare the PTO request with the first day of the current month.
    today_first_of_month = date(today.year, today.month, 1)
    time_difference = relativedelta(start_date, today_first_of_month)
    months_to_accrue = time_difference.years * 12 + time_difference.months

    data = json.load(open(file_path))
    employee_list = data["theCompany"]["employees"]

    enough_pto = False

    for employee in employee_list:
        if employee["email"] == email:
            current_pto_hours = int(employee["currentPTOHrs"])
            hrs_added_per_month = int(employee["hrsAddedPerMonth"])
            pto_available_at_start = current_pto_hours + (
                months_to_accrue * hrs_added_per_month
            )
            pto_hrs_remaining_after = pto_available_at_start - biz_hours_of_request
            if pto_hrs_remaining_after >= 0:
                enough_pto = True
            return {
                "enough_pto": enough_pto,
                "pto_hrs_remaining_after": str(pto_hrs_remaining_after),
            }

    return_msg = "Employee not found with email address " + email
    return {"error": return_msg}



================================================
FILE: workflows/__init__.py
================================================
[Empty file]


================================================
FILE: workflows/agent_goal_workflow.py
================================================
from collections import deque
from datetime import timedelta
from typing import Any, Deque, Dict, List, Optional, TypedDict, Union

from temporalio import workflow
from temporalio.common import RetryPolicy

from models.data_types import (
    ConversationHistory,
    EnvLookupInput,
    EnvLookupOutput,
    NextStep,
    ValidationInput,
)
from models.tool_definitions import AgentGoal
from workflows import workflow_helpers as helpers
from workflows.workflow_helpers import (
    LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
    LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,
)

with workflow.unsafe.imports_passed_through():
    from activities.tool_activities import ToolActivities, mcp_list_tools
    from goals import goal_list
    from models.data_types import CombinedInput, ToolPromptInput
    from prompts.agent_prompt_generators import generate_genai_prompt
    from tools.tool_registry import create_mcp_tool_definitions

# Constants
MAX_TURNS_BEFORE_CONTINUE = 250


# ToolData as part of the workflow is what's accessible to the UI - see LLMResponse.jsx for example
class ToolData(TypedDict, total=False):
    next: NextStep
    tool: str
    args: Dict[str, Any]
    response: str
    force_confirm: bool = True


@workflow.defn
class AgentGoalWorkflow:
    """Workflow that manages tool execution with user confirmation and conversation history."""

    def __init__(self) -> None:
        self.conversation_history: ConversationHistory = {"messages": []}
        self.prompt_queue: Deque[str] = deque()
        self.conversation_summary: Optional[str] = None
        self.chat_ended: bool = False
        self.tool_data: Optional[ToolData] = None
        self.confirmed: bool = (
            False  # indicates that we have confirmation to proceed to run tool
        )
        self.tool_results: List[Dict[str, Any]] = []
        self.goal: AgentGoal = {"tools": []}
        self.show_tool_args_confirmation: bool = (
            True  # set from env file in activity lookup_wf_env_settings
        )
        self.multi_goal_mode: bool = (
            False  # set from env file in activity lookup_wf_env_settings
        )
        self.mcp_tools_info: Optional[dict] = None  # stores complete MCP tools result

    # see ../api/main.py#temporal_client.start_workflow() for how the input parameters are set
    @workflow.run
    async def run(self, combined_input: CombinedInput) -> str:
        """Main workflow execution method."""
        # setup phase, starts with blank tool_params and agent_goal prompt as defined in tools/goal_registry.py
        params = combined_input.tool_params
        self.goal = combined_input.agent_goal

        await self.lookup_wf_env_settings(combined_input)

        # If the goal has an MCP server definition, dynamically load MCP tools
        if self.goal.mcp_server_definition:
            await self.load_mcp_tools()

        # add message from sample conversation provided in tools/goal_registry.py, if it exists
        if params and params.conversation_summary:
            self.add_message("conversation_summary", params.conversation_summary)
            self.conversation_summary = params.conversation_summary

        if params and params.prompt_queue:
            self.prompt_queue.extend(params.prompt_queue)

        waiting_for_confirm = False
        current_tool = None

        # This is the main interactive loop. Main responsibilities:
        #   - Selecting and changing goals as directed by the user
        #   - reacting to user input (from signals)
        #   - validating user input to make sure it makes sense with the current goal and tools
        #   - calling the LLM through activities to determine next steps and prompts
        #   - executing the selected tools via activities
        while True:
            # wait indefinitely for input from signals - user_prompt, end_chat, or confirm as defined below
            await workflow.wait_condition(
                lambda: bool(self.prompt_queue) or self.chat_ended or self.confirmed
            )

            # handle chat should end. When chat ends, push conversation history to workflow results.
            if self.chat_should_end():
                return f"{self.conversation_history}"

            # Execute the tool
            if self.ready_for_tool_execution(waiting_for_confirm, current_tool):
                waiting_for_confirm = await self.execute_tool(current_tool)
                continue

            # process forward on the prompt queue if any
            if self.prompt_queue:
                # get most recent prompt
                prompt = self.prompt_queue.popleft()
                workflow.logger.info(
                    f"workflow step: processing message on the prompt queue, message is {prompt}"
                )

                # Validate user-provided prompts
                if self.is_user_prompt(prompt):
                    self.add_message("user", prompt)

                    # Validate the prompt before proceeding
                    validation_input = ValidationInput(
                        prompt=prompt,
                        conversation_history=self.conversation_history,
                        agent_goal=self.goal,
                    )
                    validation_result = await workflow.execute_activity_method(
                        ToolActivities.agent_validatePrompt,
                        args=[validation_input],
                        schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                        start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                        retry_policy=RetryPolicy(
                            initial_interval=timedelta(seconds=5), backoff_coefficient=1
                        ),
                    )

                    # If validation fails, provide that feedback to the user - i.e., "your words make no sense, puny human" end this iteration of processing
                    if not validation_result.validationResult:
                        workflow.logger.warning(
                            f"Prompt validation failed: {validation_result.validationFailedReason}"
                        )
                        self.add_message(
                            "agent", validation_result.validationFailedReason
                        )
                        continue

                # If valid, proceed with generating the context and prompt
                context_instructions = generate_genai_prompt(
                    agent_goal=self.goal,
                    conversation_history=self.conversation_history,
                    multi_goal_mode=self.multi_goal_mode,
                    raw_json=self.tool_data,
                    mcp_tools_info=self.mcp_tools_info,
                )

                prompt_input = ToolPromptInput(
                    prompt=prompt, context_instructions=context_instructions
                )

                # connect to LLM and execute to get next steps
                tool_data = await workflow.execute_activity_method(
                    ToolActivities.agent_toolPlanner,
                    prompt_input,
                    schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                    start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                    retry_policy=RetryPolicy(
                        initial_interval=timedelta(seconds=5), backoff_coefficient=1
                    ),
                )

                tool_data["force_confirm"] = self.show_tool_args_confirmation
                self.tool_data = tool_data

                # process the tool as dictated by the prompt response - what to do next, and with which tool
                next_step = tool_data.get("next")
                current_tool = tool_data.get("tool")

                workflow.logger.info(
                    f"next_step: {next_step}, current tool is {current_tool}"
                )

                # make sure we're ready to run the tool & have everything we need
                if next_step == "confirm" and current_tool:
                    args = tool_data.get("args", {})
                    # if we're missing arguments, ask for them
                    if await helpers.handle_missing_args(
                        current_tool, args, tool_data, self.prompt_queue
                    ):
                        continue

                    waiting_for_confirm = True

                    # We have needed arguments, if we want to force the user to confirm, set that up
                    if self.show_tool_args_confirmation:
                        self.confirmed = False  # set that we're not confirmed
                        workflow.logger.info("Waiting for user confirm signal...")
                    # if we have all needed arguments (handled above) and not holding for a debugging confirm, proceed:
                    else:
                        self.confirmed = True
                # else if the next step is to pick a new goal, set that to be the goal
                elif next_step == "pick-new-goal":
                    workflow.logger.info("All steps completed. Resetting goal.")
                    self.change_goal("goal_choose_agent_type")

                # else if the next step is to be done with the conversation such as if the user requests it via asking to "end conversation"
                elif next_step == "done":
                    self.add_message("agent", tool_data)

                    # here we could send conversation to AI for analysis

                    # end the workflow
                    return str(self.conversation_history)

                self.add_message("agent", tool_data)
                await helpers.continue_as_new_if_needed(
                    self.conversation_history,
                    self.prompt_queue,
                    self.goal,
                    MAX_TURNS_BEFORE_CONTINUE,
                    self.add_message,
                )

    # Signal that comes from api/main.py via a post to /send-prompt
    @workflow.signal
    async def user_prompt(self, prompt: str) -> None:
        """Signal handler for receiving user prompts."""
        workflow.logger.info(f"signal received: user_prompt, prompt is {prompt}")
        if self.chat_ended:
            workflow.logger.info(f"Message dropped due to chat closed: {prompt}")
            return
        self.prompt_queue.append(prompt)

    # Signal that comes from api/main.py via a post to /confirm
    @workflow.signal
    async def confirm(self) -> None:
        """Signal handler for user confirmation of tool execution."""
        workflow.logger.info("Received user signal: confirmation")
        self.confirmed = True

    # Signal that comes from api/main.py via a post to /end-chat
    @workflow.signal
    async def end_chat(self) -> None:
        """Signal handler for ending the chat session."""
        workflow.logger.info("signal received: end_chat")
        self.chat_ended = True

    # Signal that can be sent from Temporal Workflow UI to enable debugging confirm and override .env setting
    @workflow.signal
    async def enable_debugging_confirm(self) -> None:
        """Signal handler for enabling debugging confirm UI & associated logic."""
        workflow.logger.info("signal received: enable_debugging_confirm")
        self.enable_debugging_confirm = True

    # Signal that can be sent from Temporal Workflow UI to disable debugging confirm and override .env setting
    @workflow.signal
    async def disable_debugging_confirm(self) -> None:
        """Signal handler for disabling debugging confirm UI & associated logic."""
        workflow.logger.info("signal received: disable_debugging_confirm")
        self.enable_debugging_confirm = False

    @workflow.query
    def get_conversation_history(self) -> ConversationHistory:
        """Query handler to retrieve the full conversation history."""
        return self.conversation_history

    @workflow.query
    def get_agent_goal(self) -> AgentGoal:
        """Query handler to retrieve the current goal of the agent."""
        return self.goal

    @workflow.query
    def get_summary_from_history(self) -> Optional[str]:
        """Query handler to retrieve the conversation summary if available.
        Used only for continue as new of the workflow."""
        return self.conversation_summary

    @workflow.query
    def get_latest_tool_data(self) -> Optional[ToolData]:
        """Query handler to retrieve the latest tool data response if available."""
        return self.tool_data

    def add_message(self, actor: str, response: Union[str, Dict[str, Any]]) -> None:
        """Add a message to the conversation history.

        Args:
            actor: The entity that generated the message (e.g., "user", "agent")
            response: The message content, either as a string or structured data
        """
        if isinstance(response, dict):
            response_str = str(response)
            workflow.logger.debug(f"Adding {actor} message: {response_str[:100]}...")
        else:
            workflow.logger.debug(f"Adding {actor} message: {response[:100]}...")

        self.conversation_history["messages"].append(
            {"actor": actor, "response": response}
        )

    def change_goal(self, goal: str) -> None:
        """Change the goal (usually on request of the user).

        Args:
            goal: goal to change to)
        """
        if goal is not None:
            for listed_goal in goal_list:
                if listed_goal.id == goal:
                    self.goal = listed_goal
                    workflow.logger.info("Changed goal to " + goal)
            if goal is None:
                workflow.logger.warning(
                    "Goal not set after goal reset, probably bad."
                )  # if this happens, there's probably a problem with the goal list

    # workflow function that defines if chat should end
    def chat_should_end(self) -> bool:
        if self.chat_ended:
            workflow.logger.info("Chat-end signal received. Chat ending.")
            return True
        else:
            return False

    # define if we're ready for tool execution
    def ready_for_tool_execution(
        self, waiting_for_confirm: bool, current_tool: Any
    ) -> bool:
        if self.confirmed and waiting_for_confirm and current_tool and self.tool_data:
            return True
        else:
            return False

    # LLM-tagged prompts start with "###"
    # all others are from the user
    def is_user_prompt(self, prompt) -> bool:
        if prompt.startswith("###"):
            return False
        else:
            return True

    # look up env settings in an activity so they're part of history
    async def lookup_wf_env_settings(self, combined_input: CombinedInput) -> None:
        env_lookup_input = EnvLookupInput(
            show_confirm_env_var_name="SHOW_CONFIRM",
            show_confirm_default=True,
        )
        env_output: EnvLookupOutput = await workflow.execute_activity_method(
            ToolActivities.get_wf_env_vars,
            env_lookup_input,
            start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5), backoff_coefficient=1
            ),
        )
        self.show_tool_args_confirmation = env_output.show_confirm
        self.multi_goal_mode = env_output.multi_goal_mode

    # execute the tool - return False if we're not waiting for confirm anymore (always the case if it works successfully)
    #
    async def execute_tool(self, current_tool: str) -> bool:
        workflow.logger.info(
            f"workflow step: user has confirmed, executing the tool {current_tool}"
        )
        self.confirmed = False
        waiting_for_confirm = False
        confirmed_tool_data = self.tool_data.copy()
        confirmed_tool_data["next"] = "user_confirmed_tool_run"
        self.add_message("user_confirmed_tool_run", confirmed_tool_data)

        # execute the tool by key as defined in tools/__init__.py
        await helpers.handle_tool_execution(
            current_tool,
            self.tool_data,
            self.tool_results,
            self.add_message,
            self.prompt_queue,
            self.goal,
        )

        # set new goal if we should
        if len(self.tool_results) > 0:
            if (
                "ChangeGoal" in self.tool_results[-1].values()
                and "new_goal" in self.tool_results[-1].keys()
            ):
                new_goal = self.tool_results[-1].get("new_goal")
                self.change_goal(new_goal)
            elif (
                "ListAgents" in self.tool_results[-1].values()
                and self.goal.id != "goal_choose_agent_type"
            ):
                self.change_goal("goal_choose_agent_type")
        return waiting_for_confirm

    # debugging helper - drop this in various places in the workflow to get status
    # also don't forget you can look at the workflow itself and do queries if you want
    def print_useful_workflow_vars(self, status_or_step: str) -> None:
        print(f"***{status_or_step}:***")
        if self.goal:
            print(f"current goal: {self.goal.id}")
        if self.tool_data:
            print(f"force confirm? {self.tool_data['force_confirm']}")
            print(f"next step: {self.tool_data.get('next')}")
            print(f"current_tool: {self.tool_data.get('tool')}")
        else:
            print("no tool data initialized yet")
        print(f"self.confirmed: {self.confirmed}")

    async def load_mcp_tools(self) -> None:
        """Load MCP tools dynamically from the server definition"""
        if not self.goal.mcp_server_definition:
            return

        workflow.logger.info(
            f"Loading MCP tools from server: {self.goal.mcp_server_definition.name}"
        )

        # Get the list of tools to include (if specified)
        include_tools = self.goal.mcp_server_definition.included_tools

        # Call the MCP list tools activity
        mcp_tools_result = await workflow.execute_activity(
            mcp_list_tools,
            args=[self.goal.mcp_server_definition, include_tools],
            start_to_close_timeout=LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT,
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5), backoff_coefficient=1
            ),
            summary=f"{self.goal.mcp_server_definition.name}",
        )

        if mcp_tools_result.get("success", False):
            tools_info = mcp_tools_result.get("tools", {})
            workflow.logger.info(f"Successfully loaded {len(tools_info)} MCP tools")

            # Store complete MCP tools result for use in prompt generation
            self.mcp_tools_info = mcp_tools_result

            # Convert MCP tools to ToolDefinition objects and add to goal
            mcp_tool_definitions = create_mcp_tool_definitions(tools_info)
            self.goal.tools.extend(mcp_tool_definitions)

            workflow.logger.info(f"Added {len(mcp_tool_definitions)} MCP tools to goal")
        else:
            error_msg = mcp_tools_result.get("error", "Unknown error")
            workflow.logger.error(f"Failed to load MCP tools: {error_msg}")
            # Continue execution without MCP tools



================================================
FILE: workflows/workflow_helpers.py
================================================
from datetime import timedelta
from typing import Any, Deque, Dict

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

from models.data_types import ConversationHistory, ToolPromptInput
from models.tool_definitions import AgentGoal
from prompts.agent_prompt_generators import (
    generate_missing_args_prompt,
    generate_tool_completion_prompt,
)
from shared.config import TEMPORAL_LEGACY_TASK_QUEUE

# Constants from original file
TOOL_ACTIVITY_START_TO_CLOSE_TIMEOUT = timedelta(seconds=12)
TOOL_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT = timedelta(minutes=30)
LLM_ACTIVITY_START_TO_CLOSE_TIMEOUT = timedelta(seconds=20)
LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT = timedelta(minutes=30)


def is_mcp_tool(tool_name: str, goal: AgentGoal) -> bool:
    """Check if a tool is an MCP tool based on the goal's MCP server definition"""
    if not goal.mcp_server_definition:
        return False

    # Check if the tool name matches any MCP tools that were loaded
    # We can identify MCP tools by checking if they're not in the original static tools
    from tools.tool_registry import (
        book_pto_tool,
        book_trains_tool,
        change_goal_tool,
        create_invoice_tool,
        current_pto_tool,
        ecomm_get_order,
        ecomm_list_orders,
        ecomm_track_package,
        financial_check_account_is_valid,
        financial_get_account_balances,
        financial_move_money,
        financial_submit_loan_approval,
        find_events_tool,
        food_add_to_cart_tool,
        future_pto_calc_tool,
        give_hint_tool,
        guess_location_tool,
        list_agents_tool,
        paycheck_bank_integration_status_check,
        search_fixtures_tool,
        search_flights_tool,
        search_trains_tool,
    )

    static_tool_names = {
        list_agents_tool.name,
        change_goal_tool.name,
        give_hint_tool.name,
        guess_location_tool.name,
        search_flights_tool.name,
        search_trains_tool.name,
        book_trains_tool.name,
        create_invoice_tool.name,
        search_fixtures_tool.name,
        find_events_tool.name,
        current_pto_tool.name,
        future_pto_calc_tool.name,
        book_pto_tool.name,
        paycheck_bank_integration_status_check.name,
        financial_check_account_is_valid.name,
        financial_get_account_balances.name,
        financial_move_money.name,
        financial_submit_loan_approval.name,
        ecomm_list_orders.name,
        ecomm_get_order.name,
        ecomm_track_package.name,
        food_add_to_cart_tool.name,
    }

    return tool_name not in static_tool_names


async def handle_tool_execution(
    current_tool: str,
    tool_data: Dict[str, Any],
    tool_results: list,
    add_message_callback: callable,
    prompt_queue: Deque[str],
    goal: AgentGoal = None,
) -> None:
    """Execute a tool after confirmation and handle its result."""
    workflow.logger.info(f"Confirmed. Proceeding with tool: {current_tool}")

    try:
        # Check if this is an MCP tool
        if goal and is_mcp_tool(current_tool, goal):
            workflow.logger.info(f"Executing MCP tool: {current_tool}")

            # Add server definition to args for MCP tools
            mcp_args = tool_data["args"].copy()
            mcp_args["server_definition"] = goal.mcp_server_definition

            dynamic_result = await workflow.execute_activity(
                current_tool,
                mcp_args,
                schedule_to_close_timeout=TOOL_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                start_to_close_timeout=TOOL_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=5), backoff_coefficient=1
                ),
                summary=f"{goal.mcp_server_definition.name} (MCP Tool)",
            )
        else:
            # Handle regular tools
            task_queue = (
                TEMPORAL_LEGACY_TASK_QUEUE
                if current_tool in ["SearchTrains", "BookTrains"]
                else None
            )

            dynamic_result = await workflow.execute_activity(
                current_tool,
                tool_data["args"],
                task_queue=task_queue,
                schedule_to_close_timeout=TOOL_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                start_to_close_timeout=TOOL_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=5), backoff_coefficient=1
                ),
            )

        dynamic_result["tool"] = current_tool
        tool_results.append(dynamic_result)

    except ActivityError as e:
        workflow.logger.error(f"Tool execution failed: {str(e)}")
        dynamic_result = {"error": str(e), "tool": current_tool}

    add_message_callback("tool_result", dynamic_result)
    prompt_queue.append(generate_tool_completion_prompt(current_tool, dynamic_result))


async def handle_missing_args(
    current_tool: str,
    args: Dict[str, Any],
    tool_data: Dict[str, Any],
    prompt_queue: Deque[str],
) -> bool:
    """Check for missing arguments and handle them if found."""
    missing_args = [key for key, value in args.items() if value is None]

    if missing_args:
        prompt_queue.append(
            generate_missing_args_prompt(current_tool, tool_data, missing_args)
        )
        workflow.logger.info(
            f"Missing arguments for tool: {current_tool}: {' '.join(missing_args)}"
        )
        return True
    return False


def format_history(conversation_history: ConversationHistory) -> str:
    """Format the conversation history into a single string."""
    return " ".join(str(msg["response"]) for msg in conversation_history["messages"])


def prompt_with_history(
    conversation_history: ConversationHistory, prompt: str
) -> tuple[str, str]:
    """Generate a context-aware prompt with conversation history."""
    history_string = format_history(conversation_history)
    context_instructions = (
        f"Here is the conversation history: {history_string} "
        "Please add a few sentence response in plain text sentences. "
        "Don't editorialize or add metadata. "
        "Keep the text a plain explanation based on the history."
    )
    return (context_instructions, prompt)


async def continue_as_new_if_needed(
    conversation_history: ConversationHistory,
    prompt_queue: Deque[str],
    agent_goal: Any,
    max_turns: int,
    add_message_callback: callable,
) -> None:
    """Handle workflow continuation if message limit is reached."""
    if len(conversation_history["messages"]) >= max_turns:
        summary_context, summary_prompt = prompt_summary_with_history(
            conversation_history
        )
        summary_input = ToolPromptInput(
            prompt=summary_prompt, context_instructions=summary_context
        )
        conversation_summary = await workflow.start_activity_method(
            "ToolActivities.agent_toolPlanner",
            summary_input,
            schedule_to_close_timeout=LLM_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
        )
        workflow.logger.info(f"Continuing as new after {max_turns} turns.")
        add_message_callback("conversation_summary", conversation_summary)
        workflow.continue_as_new(
            args=[
                {
                    "tool_params": {
                        "conversation_summary": conversation_summary,
                        "prompt_queue": prompt_queue,
                    },
                    "agent_goal": agent_goal,
                }
            ]
        )


def prompt_summary_with_history(
    conversation_history: ConversationHistory,
) -> tuple[str, str]:
    """Generate a prompt for summarizing the conversation.
    Used only for continue as new of the workflow."""
    history_string = format_history(conversation_history)
    context_instructions = f"Here is the conversation history between a user and a chatbot: {history_string}"
    actual_prompt = (
        "Please produce a two sentence summary of this conversation. "
        'Put the summary in the format { "summary": "<plain text>" }'
    )
    return (context_instructions, actual_prompt)



================================================
FILE: .devcontainer/devcontainer.json
================================================
{
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "name": "Temporal AI Agentic Demo",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {},
    "ghcr.io/va-h/devcontainers-features/uv:1": {},
    "ghcr.io/devcontainers/features/python:1": {},
    "ghcr.io/devcontainers-extra/features/temporal-cli:1": {},
    "ghcr.io/mrsimonemms/devcontainers/tcld:1": {}
  },
  "forwardPorts": [
    5173,
	  7233,
    8000,
	  8233
  ],
  "containerEnv": {
    "VITE_HOST": "0.0.0.0"
  }
}