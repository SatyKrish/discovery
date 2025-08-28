# Helper targets to run Temporal worker and FastAPI server

.PHONY: install api worker dev fmt test

PY=python3
PIP=pip3

install:
	$(PIP) install -r requirements.txt

api:
	uvicorn api:app --host $${HOST:-0.0.0.0} --port $${PORT:-8000} --reload

worker:
	$(PY) -m temporal.temporal_worker

# Run both api and worker in separate terminals (macOS only suggestion)
# Use: make api  (in one terminal)
# and: make worker (in another)

dev: api

fmt:
	@echo "No formatter configured. Consider adding ruff/black."

test:
	pytest -q
