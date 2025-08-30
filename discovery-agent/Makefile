# Helper targets to run Temporal worker and FastAPI server

.PHONY: install api worker dev fmt test venv venv-info venv-shell cli

VENV_DIR:=.venv
# Make all recipes run inside the venv by prepending it to PATH
export VIRTUAL_ENV:=$(abspath $(VENV_DIR))
export PATH:=$(VIRTUAL_ENV)/bin:$(PATH)
export PYTHONPATH:=$(abspath src):$(PYTHONPATH)

PY=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# Default API endpoint for CLI (override with `make cli API=http://host:port`)
API?=http://localhost:8080
CLI_ARGS?=

venv: $(VENV_DIR)/bin/python

$(VENV_DIR)/bin/python:
	python3 -m venv $(VENV_DIR)
	$(PIP) -V || true
	$(VENV_DIR)/bin/python -m pip install --upgrade pip

install: venv
ifneq (,$(wildcard requirements.txt))
	@echo "Installing from requirements.txt"
	$(PIP) install -r requirements.txt
else ifneq (,$(wildcard pyproject.toml))
	@echo "Installing project in editable mode (pyproject.toml detected)"
	$(PIP) install -e .
else
	@echo "No pyproject.toml or requirements.txt found. Please add one." && exit 1
endif

api: venv
	$(VENV_DIR)/bin/uvicorn api.server:app --host $${HOST:-0.0.0.0} --port $${PORT:-8080} --reload

worker: venv
	$(PY) -m worker

# Run both api and worker in separate terminals (macOS only suggestion)
# Use: make api  (in one terminal)
# and: make worker (in another)

dev: api

fmt:
	@echo "No formatter configured. Consider adding ruff/black."

test: venv
	$(VENV_DIR)/bin/pytest -q

# Show current venv details
venv-info: venv
	@echo "VIRTUAL_ENV=$(VIRTUAL_ENV)"
	@echo "python=$$(which python)"
	@echo "pip=$$(which pip)"
	$(PY) -V || true
	$(PIP) -V || true

# Open an interactive subshell with the venv activated (type 'exit' to leave)
venv-shell: venv
	@echo "Starting interactive shell with venv activated. Type 'exit' to leave."
	$(SHELL) -i -c "source $(VENV_DIR)/bin/activate; exec $(SHELL) -i"

# Run the terminal chat client against the API
cli: venv
	$(PY) src/cli_chat.py --api $(API) $(CLI_ARGS)
