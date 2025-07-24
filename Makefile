# Define the source path of your retry_command.sh script
# Using $(CURDIR) to get the absolute path of the Makefile's directory.
RETRY_SCRIPT_SOURCE := $(CURDIR)/retry_command.sh

# Define the target directory for the symbolic link
# This is a common location for user executables, accessible system-wide.
# NOTE: Creating/removing links here will require 'sudo make link'/'sudo make unlink'.
# Assuming /usr/local/bin is always present.
LINK_TARGET_DIR := /usr/local/bin

# Define the name of the symbolic link (now without .sh extension)
LINK_NAME := retry_command

.PHONY: help install install-dev lint format type-check test test-cov clean all link unlink check dev-setup quick-check
.DEFAULT_GOAL := help

PYTHON := python3
PIP := pip3

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	$(PIP) install -e .

install-dev: ## Install development dependencies
	$(PIP) install -e ".[dev]"

lint: ## Run linting (flake8)
	@echo "Running flake8..."
	flake8 .

format: ## Format code with black and isort
	@echo "Running black..."
	black .
	@echo "Running isort..."
	isort .

format-check: ## Check if code is formatted correctly
	@echo "Checking black formatting..."
	black --check .
	@echo "Checking isort formatting..."
	isort --check-only .

type-check: ## Run type checking with mypy
	@echo "Running mypy..."
	mypy .

test: ## Run tests
	@echo "Running pytest..."
	pytest

test-cov: ## Run tests with coverage
	@echo "Running pytest with coverage..."
	pytest --cov=. --cov-report=html --cov-report=term

clean: unlink ## Clean up generated files and the retry_command.sh link
	@echo "Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

all: format lint type-check test ## Run all checks (format, lint, type-check, test)

check: lint type-check ## Run lint and type checking only

# Development workflow commands
dev-setup: install-dev ## Setup development environment
	@echo "Development environment setup complete!"
	@echo "You can now run 'make all' to run all checks"

quick-check: format lint ## Quick format and lint check

# --- New targets for retry_command.sh link management ---
link: ## Create a symbolic link to retry_command.sh in $(LINK_TARGET_DIR) and make it executable
	@echo "Creating symbolic link for $(RETRY_SCRIPT_SOURCE) to $(LINK_TARGET_DIR)/$(LINK_NAME)..."
	ln -sf $(RETRY_SCRIPT_SOURCE) $(LINK_TARGET_DIR)/$(LINK_NAME)
	chmod +x $(LINK_TARGET_DIR)/$(LINK_NAME)
	@echo "Link created and made executable: $(LINK_TARGET_DIR)/$(LINK_NAME)"

unlink: ## Remove the symbolic link to retry_command.sh
	@echo "Removing symbolic link $(LINK_TARGET_DIR)/$(LINK_NAME)..."
	rm -f $(LINK_TARGET_DIR)/$(LINK_NAME)
	@echo "Link removed."
