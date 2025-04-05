# Makefile for Streamlit Sandbox Docker operations

# Variables
IMAGE_NAME := streamlit-sandbox
CONTAINER_NAME := streamlit-sandbox-container
HOST_PORT := 8501
CONTAINER_PORT := 8501
LOG_DIR := $(shell pwd)/log

# Default target
.DEFAULT_GOAL := help

# Targets
.PHONY: help build run run-local stop rm logs lint typecheck clean all

help: ## Display this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

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
	@echo "Ensure dependencies are installed: uv pip install -r requirements.txt"
	@uv run streamlit run src/app.py

stop: ## Stop the running Docker container
	@echo "Stopping Docker container: $(CONTAINER_NAME)..."
	@docker stop $(CONTAINER_NAME) || echo "Container not running or already stopped."

# Note: 'run' uses --rm, so 'rm' target might not be strictly necessary if only 'run' is used.
# Kept for cases where a container might be run without --rm.
rm: ## Remove the stopped Docker container
	@echo "Removing Docker container: $(CONTAINER_NAME)..."
	@docker rm $(CONTAINER_NAME) || echo "Container not found or already removed."

logs: ## View the logs of the running container
	@echo "Viewing logs for container: $(CONTAINER_NAME)..."
	@docker logs -f $(CONTAINER_NAME)

lint: ## Run ruff linter and formatter check
	@echo "Running ruff check..."
	@uv run ruff check src
	@echo "Running ruff format check..."
	@uv run ruff format --check src

typecheck: ## Run pyright type checker
	@echo "Running pyright type check..."
	@uv run pyright src

clean: ## Remove the built Docker image
	@echo "Removing Docker image: $(IMAGE_NAME)..."
	@docker rmi $(IMAGE_NAME) || echo "Image not found or already removed."

all: build run ## Build the image and run the container

# Ensure log directory exists before running
$(LOG_DIR):
	mkdir -p $(LOG_DIR)
