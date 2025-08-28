# Discovery Agent

The `temporal.deep_agent` module provides a minimal autonomous agent used by the
Temporal workflow examples.  The new `create_deep_agent` factory makes it easy
to build a pre-configured agent with a base prompt, model, subagent registry,
extra tools, and step limit.

```python
from temporal.deep_agent import create_deep_agent
from langchain_community.tools import RequestsGetTool

agent = create_deep_agent(tools=[RequestsGetTool()])
result = await agent("2 + 2?")
```

The returned callable mirrors `run_agent` but applies the configuration above on
every invocation, letting callers focus on the question and optional
instructions.

## Command line chat

For environments without a browser the repository provides a small CLI that
talks to the FastAPI service exposing the Temporal workflow:

```bash
python cli_chat.py --api http://localhost:8000
```

The script starts a new workflow and allows chatting from the terminal. Use
`Ctrl+C` to end the session.

## Run with Temporal Server

This service uses Temporal for orchestration. You need a Temporal server running, a worker connected to a task queue, and the FastAPI API.

1) Start Temporal Server (pick one):

- Temporal CLI (Docker-internal server):
	- Install: https://docs.temporal.io/cli
	- Run server:
		- `temporal server start-dev` (defaults to 7233)

- Docker Compose (standard Temporal stack):
	- `docker run --name temporal -p 7233:7233 temporalio/auto-setup:latest`

2) Configure environment:

- Copy `.env.example` to `.env` and edit as needed. Key vars:
	- `TEMPORAL_ADDRESS` (default `localhost:7233`)
	- `TEMPORAL_TASK_QUEUE` (default `deep-agent-task-queue`)
	- `OPENAI_API_KEY` (optional, required if your tools use OpenAI)
	- Azure OpenAI (optional): set `AZURE_OPENAI_ENDPOINT` to switch to Azure
	  - Required: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`
	  - Optional: `AZURE_OPENAI_API_KEY` (if not using AAD), `AZURE_OPENAI_API_VERSION`
	  - When Azure vars are set, the app uses AzureChatOpenAI under the hood

3) Install deps and run services (in discovery-agent/):

- Install:
	- `pip install -r requirements.txt`

- Start the worker (Terminal A):
	- `python -m temporal.temporal_worker`

- Start the API (Terminal B):
	- `uvicorn api:app --reload --host 0.0.0.0 --port 8000`

Alternatively, with Makefile:

- `make install`
- `make worker` (Terminal A)
- `make api` (Terminal B)

4) Quick check:

- Start a chat from CLI:
	- `python cli_chat.py --api http://localhost:8000`

If the worker is connected and the server is running, new workflows will be created on `deep-agent-task-queue` and the API endpoints will respond.

### API endpoints

- `POST /workflow/start` -> `{ workflow_id }`
- `POST /workflow/{id}/prompt` -> `{ status: "ok" }`
- `POST /workflow/{id}/confirm` -> `{ status: "ok" }`
- `POST /workflow/{id}/end` -> `{ status: "ok" }`
- `GET  /workflow/{id}/history` -> `{ history: [...] }`

The API connects to Temporal at `TEMPORAL_ADDRESS`. The worker registers the workflow and activities at `TEMPORAL_TASK_QUEUE` and must be running for progress.
