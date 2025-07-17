# Makefile for MEvalService - Committee Evaluation and Monitoring Service
# Sistema de Comités de Seguimiento y Evaluación Académico/Disciplinario

.PHONY: help install dev clean test lint format migrate setup docker-build docker-run

# Variables
PYTHON := python3
PIP := pip
VENV := venv
PORT := 8009
SERVICE_NAME := mevalservice

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)MEvalService - Committee Evaluation Service$(NC)"
	@echo "$(YELLOW)Available commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

dev-install: ## Install development dependencies
	@echo "$(YELLOW)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-asyncio pytest-cov black isort flake8 mypy
	@echo "$(GREEN)Development dependencies installed!$(NC)"

setup: ## Set up the development environment
	@echo "$(YELLOW)Setting up development environment...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)Created .env file from .env.example$(NC)"; \
		echo "$(YELLOW)Please update .env with your configuration$(NC)"; \
	fi
	make install
	make migrate
	@echo "$(GREEN)Development environment ready!$(NC)"

dev: ## Start development server
	@echo "$(YELLOW)Starting MEvalService development server on port $(PORT)...$(NC)"
	uvicorn app.main:app --reload --host 0.0.0.0 --port $(PORT)

run: ## Start production server
	@echo "$(YELLOW)Starting MEvalService production server...$(NC)"
	uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

test: ## Run tests
	@echo "$(YELLOW)Running tests...$(NC)"
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)Tests completed!$(NC)"

test-fast: ## Run tests without coverage
	@echo "$(YELLOW)Running fast tests...$(NC)"
	pytest tests/ -v -x
	@echo "$(GREEN)Fast tests completed!$(NC)"

lint: ## Run linting
	@echo "$(YELLOW)Running linting...$(NC)"
	flake8 app tests
	mypy app
	@echo "$(GREEN)Linting completed!$(NC)"

format: ## Format code
	@echo "$(YELLOW)Formatting code...$(NC)"
	black app tests
	isort app tests
	@echo "$(GREEN)Code formatted!$(NC)"

format-check: ## Check code formatting
	@echo "$(YELLOW)Checking code formatting...$(NC)"
	black --check app tests
	isort --check-only app tests
	@echo "$(GREEN)Formatting check completed!$(NC)"

migrate: ## Run database migrations
	@echo "$(YELLOW)Running database migrations...$(NC)"
	alembic upgrade head
	@echo "$(GREEN)Migrations completed!$(NC)"

migrate-create: ## Create new migration (usage: make migrate-create MESSAGE="description")
	@echo "$(YELLOW)Creating new migration...$(NC)"
	@if [ -z "$(MESSAGE)" ]; then \
		echo "$(RED)Error: MESSAGE is required. Usage: make migrate-create MESSAGE='description'$(NC)"; \
		exit 1; \
	fi
	alembic revision --autogenerate -m "$(MESSAGE)"
	@echo "$(GREEN)Migration created!$(NC)"

migrate-history: ## Show migration history
	@echo "$(YELLOW)Migration history:$(NC)"
	alembic history --verbose

migrate-current: ## Show current migration
	@echo "$(YELLOW)Current migration:$(NC)"
	alembic current --verbose

migrate-downgrade: ## Downgrade one migration
	@echo "$(YELLOW)Downgrading migration...$(NC)"
	alembic downgrade -1
	@echo "$(GREEN)Migration downgraded!$(NC)"

clean: ## Clean up cache and temporary files
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage .mypy_cache
	@echo "$(GREEN)Cleanup completed!$(NC)"

logs: ## Show service logs
	@echo "$(YELLOW)Showing logs...$(NC)"
	tail -f logs/$(SERVICE_NAME).log 2>/dev/null || echo "$(RED)No log file found$(NC)"

db-shell: ## Open database shell
	@echo "$(YELLOW)Opening database shell...$(NC)"
	@echo "Use \\q to quit"
	psql $$DATABASE_URL

db-reset: ## Reset database (WARNING: This will delete all data!)
	@echo "$(RED)WARNING: This will delete all data in the database!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "$(YELLOW)Resetting database...$(NC)"
	alembic downgrade base
	alembic upgrade head
	@echo "$(GREEN)Database reset completed!$(NC)"

check: ## Run all checks (lint, format-check, test)
	@echo "$(YELLOW)Running all checks...$(NC)"
	make format-check
	make lint
	make test
	@echo "$(GREEN)All checks passed!$(NC)"

docker-build: ## Build Docker image
	@echo "$(YELLOW)Building Docker image...$(NC)"
	docker build -t $(SERVICE_NAME):latest .
	@echo "$(GREEN)Docker image built!$(NC)"

docker-run: ## Run Docker container
	@echo "$(YELLOW)Running Docker container...$(NC)"
	docker run -p $(PORT):$(PORT) --env-file .env $(SERVICE_NAME):latest

docker-dev: ## Run Docker container for development
	@echo "$(YELLOW)Running Docker container for development...$(NC)"
	docker run -p $(PORT):$(PORT) -v $(PWD):/app --env-file .env $(SERVICE_NAME):latest

# Health check
health: ## Check service health
	@echo "$(YELLOW)Checking service health...$(NC)"
	@curl -f http://localhost:$(PORT)/health 2>/dev/null && echo "$(GREEN)Service is healthy!$(NC)" || echo "$(RED)Service is not responding$(NC)"

# Generate API documentation
docs: ## Generate API documentation
	@echo "$(YELLOW)API documentation available at: http://localhost:$(PORT)/docs$(NC)"
	@echo "$(YELLOW)ReDoc documentation available at: http://localhost:$(PORT)/redoc$(NC)"

# Quick start for new developers
quick-start: ## Quick start for new developers
	@echo "$(BLUE)=== MEvalService Quick Start ===$(NC)"
	@echo "$(YELLOW)1. Setting up environment...$(NC)"
	make setup
	@echo "$(YELLOW)2. Running tests...$(NC)"
	make test-fast
	@echo "$(YELLOW)3. Starting development server...$(NC)"
	@echo "$(GREEN)Ready! Run 'make dev' to start the server$(NC)"
	@echo "$(BLUE)Documentation will be available at: http://localhost:$(PORT)/docs$(NC)"

# Development workflow
workflow: ## Show development workflow
	@echo "$(BLUE)=== Development Workflow ===$(NC)"
	@echo "$(YELLOW)1. make setup           $(NC)# Set up environment"
	@echo "$(YELLOW)2. make dev             $(NC)# Start development server"
	@echo "$(YELLOW)3. make migrate-create  $(NC)# Create migrations"
	@echo "$(YELLOW)4. make test            $(NC)# Run tests"
	@echo "$(YELLOW)5. make format          $(NC)# Format code"
	@echo "$(YELLOW)6. make check           $(NC)# Run all checks"
	@echo "$(BLUE)API Docs: http://localhost:$(PORT)/docs$(NC)"
