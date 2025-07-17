# Makefile for Software Factory Service

# Variables
BINARY_NAME=softwarefactoryservice
MAIN_PATH=./cmd/server
BUILD_DIR=./build
DOCKER_IMAGE=sicora/softwarefactoryservice

# Go parameters
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
GOGET=$(GOCMD) get
GOMOD=$(GOCMD) mod

.PHONY: all build clean test deps docker-build docker-run help

# Default target
all: clean deps test build

# Build the binary
build:
	@echo "Building $(BINARY_NAME)..."
	@mkdir -p $(BUILD_DIR)
	$(GOBUILD) -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)
	@echo "Build completed: $(BUILD_DIR)/$(BINARY_NAME)"

# Clean build artifacts
clean:
	@echo "Cleaning..."
	$(GOCLEAN)
	@rm -rf $(BUILD_DIR)
	@echo "Clean completed"

# Run tests
test:
	@echo "Running tests..."
	$(GOTEST) -v ./...
	@echo "Tests completed"

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	$(GOTEST) -v -coverprofile=coverage.out ./...
	$(GOCMD) tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report generated: coverage.html"

# Download dependencies
deps:
	@echo "Downloading dependencies..."
	$(GOMOD) download
	$(GOMOD) tidy
	@echo "Dependencies updated"

# Run the application
run: build
	@echo "Running $(BINARY_NAME)..."
	./$(BUILD_DIR)/$(BINARY_NAME)

# Run the application in development mode
dev:
	@echo "Running in development mode..."
	$(GOCMD) run $(MAIN_PATH)

# Format code
fmt:
	@echo "Formatting code..."
	$(GOCMD) fmt ./...
	@echo "Code formatted"

# Lint code
lint:
	@echo "Linting code..."
	golangci-lint run
	@echo "Linting completed"

# Build Docker image
docker-build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE):latest .
	@echo "Docker image built: $(DOCKER_IMAGE):latest"

# Run with Docker
docker-run:
	@echo "Running with Docker..."
	docker run -p 8080:8080 --env-file .env $(DOCKER_IMAGE):latest

# Database operations
db-migrate:
	@echo "Running database migrations..."
	$(GOCMD) run $(MAIN_PATH) --migrate-only
	@echo "Migrations completed"

# Generate Swagger documentation
swagger:
	@echo "Generating Swagger documentation..."
	swag init -g $(MAIN_PATH)/main.go -o ./docs
	@echo "Swagger documentation generated in ./docs"

# Install development tools
install-tools:
	@echo "Installing development tools..."
	$(GOGET) github.com/swaggo/swag/cmd/swag@latest
	$(GOGET) github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	@echo "Development tools installed"

# Help
help:
	@echo "Available targets:"
	@echo "  build          - Build the binary"
	@echo "  clean          - Clean build artifacts"
	@echo "  test           - Run tests"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo "  deps           - Download and tidy dependencies"
	@echo "  run            - Build and run the application"
	@echo "  dev            - Run in development mode"
	@echo "  fmt            - Format code"
	@echo "  lint           - Lint code"
	@echo "  docker-build   - Build Docker image"
	@echo "  docker-run     - Run with Docker"
	@echo "  db-migrate     - Run database migrations"
	@echo "  swagger        - Generate Swagger documentation"
	@echo "  install-tools  - Install development tools"
	@echo "  help           - Show this help message"

# Development with Docker
setup: ## Setup development environment
	@echo "🔧 Setting up development environment..."
	@echo "Installing Go tools..."
	go install github.com/air-verse/air@latest
	go install github.com/swaggo/swag/cmd/swag@latest
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install github.com/go-delve/delve/cmd/dlv@latest
	go install golang.org/x/tools/cmd/goimports@latest
	go install mvdan.cc/gofumpt@latest
	@echo "✅ Development tools installed"

dev-setup: ## Setup for devcontainer development
	@echo "🐳 Setting up devcontainer environment..."
	@echo "Waiting for database to be ready..."
	@sleep 5
	@echo "✅ Devcontainer setup completed"

dev-start: ## Start development server with hot reload
	@echo "🚀 Starting development server with hot reload..."
	air -c .air.toml

dev-stop: ## Stop development environment
	@echo "🛑 Stopping development environment..."
	docker-compose -f .devcontainer/docker-compose.dev.yml down

dev-restart: dev-stop dev-start ## Restart development environment

dev-logs: ## View development logs
	@echo "📋 Viewing development logs..."
	docker-compose -f .devcontainer/docker-compose.dev.yml logs -f softwarefactory-service

dev-shell: ## Access development container shell
	@echo "🐚 Accessing development container shell..."
	docker-compose -f .devcontainer/docker-compose.dev.yml exec softwarefactory-service zsh

# Docker Development Commands
docker-dev-build: ## Build development Docker image
	@echo "🏗️ Building development Docker image..."
	docker build -f Dockerfile.dev -t $(DOCKER_IMAGE):dev .
	@echo "✅ Development image built: $(DOCKER_IMAGE):dev"

docker-dev-up: ## Start development environment with Docker Compose
	@echo "🚀 Starting development environment..."
	docker-compose -f .devcontainer/docker-compose.dev.yml up -d
	@echo "✅ Development environment started"
	@echo "🌐 API available at: http://localhost:8080"
	@echo "📊 PgAdmin available at: http://localhost:5050"
	@echo "📝 Swagger docs at: http://localhost:8080/swagger/index.html"

docker-dev-down: ## Stop development environment
	@echo "🛑 Stopping development environment..."
	docker-compose -f .devcontainer/docker-compose.dev.yml down
	@echo "✅ Development environment stopped"

docker-dev-reset: ## Reset development environment (remove volumes)
	@echo "🔄 Resetting development environment..."
	docker-compose -f .devcontainer/docker-compose.dev.yml down -v
	docker-compose -f .devcontainer/docker-compose.dev.yml up -d
	@echo "✅ Development environment reset"

docker-dev-logs: ## View development environment logs
	@echo "📋 Viewing development environment logs..."
	docker-compose -f .devcontainer/docker-compose.dev.yml logs -f

docker-dev-db-shell: ## Access PostgreSQL shell in development
	@echo "🐘 Accessing PostgreSQL shell..."
	docker-compose -f .devcontainer/docker-compose.dev.yml exec postgres psql -U postgres -d sicora_db

docker-dev-redis-shell: ## Access Redis shell in development
	@echo "🔴 Accessing Redis shell..."
	docker-compose -f .devcontainer/docker-compose.dev.yml exec redis redis-cli -a dev_redis_password

# Production Docker Commands
docker-prod-build: ## Build production Docker image
	@echo "🏗️ Building production Docker image..."
	docker build -f Dockerfile -t $(DOCKER_IMAGE):latest .
	@echo "✅ Production image built: $(DOCKER_IMAGE):latest"

docker-prod-run: ## Run production Docker container
	@echo "🚀 Running production container..."
	docker run -d \
		--name $(BINARY_NAME)-prod \
		-p 8080:8080 \
		--env-file .env \
		$(DOCKER_IMAGE):latest
	@echo "✅ Production container started"
