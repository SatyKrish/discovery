# Discovery Agent (Temporal-first, MVP)

- Temporal **Workflows** orchestrate; all LLM/tool/IO is in **Activities** with retries/timeouts/heartbeats.
- **OpenAI Agents SDK** drives the decision loop inside an Activity (Option B).
- HITL via Temporal signals (`user_message`, `approve_tool`) + query (`get_status`).
- Generic MCP registry (stdio + HTTP) discovers tools and prompt packs; subagents can request extra tools with human approval.
- OTEL tracing included; Search Attributes for filtering in Temporal Web.

## Run
1) Start Temporal: `temporal server start-dev`
2) Install deps: `pip install -e .`
3) Env (recommended via .env.local):
```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_API_VERSION=2024-05-01-preview
# Deployment names (models)
LLM_MODEL_DECISION=gpt-4.1
LLM_MODEL_PLAN=gpt-4.1

# Temporal
TEMPORAL_TARGET=localhost:7233
TEMPORAL_NAMESPACE=default
TASK_QUEUE=agent-queue
OTEL_ENDPOINT=http://localhost:4318/v1/traces   # optional
```

4. Worker: `python -m src.worker`
5. API: `uvicorn src.api.server:app --reload --port 8080`

## Try it

```bash
curl -s -X POST http://localhost:8080/sessions -H 'Content-Type: application/json' \
	-d '{"goal":"Summarize customer feedback and propose next steps", "tenant":"demo", "user_id":"u1"}'
# => {"workflow_id":"session-..."}

curl -s -X POST http://localhost:8080/sessions/<workflow_id>/messages -H 'Content-Type: application/json' \
	-d '{"text":"Here are 3 feedback items..."}'

curl -s http://localhost:8080/sessions/<workflow_id>/status | jq
```
