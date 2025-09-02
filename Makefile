## Monorepo Makefile for Discovery

.PHONY: setup setup-agent setup-frontend install run-worker run-api run-frontend run-cli setup-temporal-mac run-dev help

# Directories
AGENT_DIR ?= discovery-agent
FRONTEND_DIR ?= discovery-ui

# API server configuration
HOST ?= 0.0.0.0
PORT ?= 8080

# Python virtual environment (must already exist; we just source it)
VENV_DIR ?= $(AGENT_DIR)/.venv
VENV_DIR_ABS := $(abspath $(VENV_DIR))
PY := python
PIP := pip

#
# Setup: install dependencies for both projects
# - Python (discovery-agent) via uv
# - Frontend (discovery-ui) via npm
#
setup: setup-frontend

# Optional: validate venv and install agent deps into existing venv
setup-agent:
	@test -f "$(VENV_DIR)/bin/activate" || (echo "Missing venv at $(VENV_DIR). Please create it." && exit 1)
	@if [ -f $(AGENT_DIR)/requirements.txt ]; then \
	  . "$(VENV_DIR)/bin/activate" && pip install -r $(AGENT_DIR)/requirements.txt; \
	elif [ -f $(AGENT_DIR)/pyproject.toml ]; then \
	  . "$(VENV_DIR)/bin/activate" && pip install -e $(AGENT_DIR); \
	else \
	  echo "No requirements.txt or pyproject.toml in $(AGENT_DIR)"; \
	fi

# Install frontend deps for discovery-ui
setup-frontend:
	cd $(FRONTEND_DIR) && npm install

# Test frontend with Playwright
test-frontend:
	cd $(FRONTEND_DIR) && npx playwright test

# Alias for familiarity
install: setup

#
# Backend: Temporal worker and API
#
run-worker:
	@test -f "$(VENV_DIR_ABS)/bin/activate" || (echo "Missing venv at $(VENV_DIR). Please create it." && exit 1)
	cd $(AGENT_DIR) && . "$(VENV_DIR_ABS)/bin/activate" && python -m src.worker

run-api:
	@test -f "$(VENV_DIR_ABS)/bin/activate" || (echo "Missing venv at $(VENV_DIR). Please create it." && exit 1)
	cd $(AGENT_DIR) && . "$(VENV_DIR_ABS)/bin/activate" && python -m uvicorn src.api.server:app --reload --host $(HOST) --port $(PORT)

#
# Frontend: Next.js dev server
#
run-frontend:
	cd $(FRONTEND_DIR) && npm run dev

#
# CLI: Terminal chat client
#
CLI_ARGS ?=
run-cli:
	@test -f "$(VENV_DIR_ABS)/bin/activate" || (echo "Missing venv at $(VENV_DIR). Please create it." && exit 1)
	cd $(AGENT_DIR) && . "$(VENV_DIR_ABS)/bin/activate" && python -m src.chat $(CLI_ARGS)

#
# Development environment setup for Temporal (macOS)
#
setup-temporal-mac:
	brew install temporal
	temporal server start-dev

#
# Run common dev services in parallel
#
run-dev:
	@echo "Starting all development services..."
	@$(MAKE) run-worker & \
	$(MAKE) run-api & \
	$(MAKE) run-frontend & \
	wait

#
# Help
#
help:
	@echo "Available commands:"
	@echo "  make setup               - Install frontend deps (UI via npm). Python uses existing venv at $(VENV_DIR)"
	@echo "  make test-frontend       - Run Playwright tests for discovery-ui"
	@echo "  make run-worker          - Start the Temporal worker (discovery-agent)"
	@echo "  make run-api             - Start the API server (discovery-agent)"
	@echo "  make run-frontend        - Start the frontend dev server (discovery-ui)"
	@echo "  make run-cli             - Run the terminal chat client (discovery-agent/src/chat.py)"
	@echo "  make setup-temporal-mac  - Install and start Temporal server on Mac"
	@echo "  make run-dev             - Start worker, API, and frontend in parallel"
