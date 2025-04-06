# Variables
IMAGE_NAME := streamlit-sandbox
CONTAINER_NAME := streamlit-sandbox-container
HOST_PORT := 8501
CONTAINER_PORT := 8501
LOG_DIR := $(shell pwd)/log

# Detect OS for platform-specific commands
OS := $(shell uname -s)
ifeq ($(OS),Darwin)
	ACTIVATE_CMD := source .venv/bin/activate
else ifeq ($(OS),Linux)
	ACTIVATE_CMD := source .venv/bin/activate
else
	ACTIVATE_CMD := .\.venv\Scripts\activate
endif

# Default target
.DEFAULT_GOAL := help

# Targets
.PHONY: help build run run-local stop rm logs lint typecheck clean all setup sync lock update test clean-all

help: ## Display this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Setup development environment with uv
	@echo "Setting up development environment using uv..."
	@pip install -U uv
	@echo "Creating virtual environment..."
	@uv venv -f .venv
	@echo "Installing dependencies including development packages..."
	@uv sync --reinstall
	@echo "Setup complete! Activate the virtual environment with: $(ACTIVATE_CMD)"

sync: ## Sync project dependencies to latest locked versions
	@echo "Syncing dependencies..."
	@uv sync

lock: ## Update lockfile with latest compatible dependencies
	@echo "Updating lockfile..."
	@uv lock

update: ## Update all dependencies to latest versions
	@echo "Upgrading all dependencies..."
	@uv lock --upgrade

build: ## Build the Docker image
	@echo "Building Docker image: $(IMAGE_NAME)..."
	@docker build -t $(IMAGE_NAME) .

run: ## Run the Docker container (background, logs mounted)
	@echo "Running Docker container: $(CONTAINER_NAME)..."
	@mkdir -p $(LOG_DIR) # Ensure host log directory exists
	@docker run -d --rm \
		-p $(HOST_PORT):$(CONTAINER_PORT) \
		-v "$(LOG_DIR):/app/log" \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME)
	@echo "Container $(CONTAINER_NAME) started. Access at http://localhost:$(HOST_PORT)"
	@echo "Logs are mounted to $(LOG_DIR)"

run-local: ## Run the Streamlit app locally
	@echo "Running Streamlit app locally..."
	@uv run streamlit run src/app.py

stop: ## Stop the running Docker container
	@echo "Stopping Docker container: $(CONTAINER_NAME)..."
	@docker stop $(CONTAINER_NAME) || echo "Container not running or already stopped."

logs: ## View the logs of the running container
	@echo "Viewing logs for container: $(CONTAINER_NAME)..."
	@docker logs -f $(CONTAINER_NAME)

lint: ## Run ruff linter and formatter
	@echo "Running ruff check..."
	@uv run python -m ruff check src
	@echo "Running ruff format..."
	@uv run python -m ruff format src
	@uv run mypy .

typecheck: ## Run pyright type checker
	@echo "Running pyright type check..."
	@uv run pyright src

test: ## Run tests with pytest
	@echo "Running tests..."
	@uv run python -m pytest tests

clean: ## Clean up environment and temporary files
	@echo "Cleaning up..."
	@rm -rf __pycache__ .pytest_cache .ruff_cache
	@echo "Removing Docker image: $(IMAGE_NAME)..."
	@docker rmi $(IMAGE_NAME) 2>/dev/null || echo "Image not found or already removed."

clean-all: clean ## Deep clean - removes virtual environment and lock files
	@echo "Deep cleaning..."
	@rm -rf .venv uv.lock

all: build run ## Build the image and run the container

# Ensure log directory exists before running
$(LOG_DIR):
	mkdir -p $(LOG_DIR)
