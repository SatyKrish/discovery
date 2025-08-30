# Discovery Agent (Temporal-first, MVP)

- Temporal **Workflows** orchestrate; all LLM/tool/IO is in **Activities** with retries/timeouts/heartbeats.
- **OpenAI Agents SDK** drives the decision loop inside an Activity (Option B).
- HITL via Temporal signals (`user_message`, `approve_tool`) + query (`get_status`).
- OTEL tracing included; Search Attributes for filtering in Temporal Web.

## Run
1) Start Temporal: `temporal server start-dev`
2) Install deps: `pip install -e .`
3) Env:
```bash
export OPENAI_API_KEY=sk-...          # or ANTHROPIC_API_KEY=sk-...
export TEMPORAL_TARGET=localhost:7233
export TEMPORAL_NAMESPACE=default
export TASK_QUEUE=agent-queue
export OTEL_ENDPOINT=http://localhost:4318/v1/traces   # optional
```

4. Worker: `python -m discovery_agent.worker`
5. API: `uvicorn discovery_agent.api.server:app --reload --port 8080`

## Try it

```bash
curl -s -X POST http://localhost:8080/sessions -H 'Content-Type: application/json' \
	-d '{"goal":"Summarize customer feedback and propose next steps", "tenant":"demo", "user_id":"u1"}'
# => {"workflow_id":"session-..."}

curl -s -X POST http://localhost:8080/sessions/<workflow_id>/messages -H 'Content-Type: application/json' \
	-d '{"text":"Here are 3 feedback items..."}'

curl -s http://localhost:8080/sessions/<workflow_id>/status | jq
```
