.PHONY: help install install-dev lint format type-check test test-cov clean all
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

clean: ## Clean up generated files
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
