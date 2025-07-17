# MEvalService Makefile

.PHONY: build test run clean deps docker-build docker-run migrate help

# Go parameters
BINARY_NAME=mevalservice
MAIN_PATH=./cmd/server
BINARY_PATH=./bin/$(BINARY_NAME)

# Database parameters
DB_NAME=sicora_mevalservice
DB_USER=postgres
DB_HOST=localhost
DB_PORT=5432

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

deps: ## Download dependencies
	go mod download
	go mod tidy

build: deps ## Build the application
	@echo "Building $(BINARY_NAME)..."
	@mkdir -p bin
	go build -o $(BINARY_PATH) $(MAIN_PATH)

test: ## Run tests
	@echo "Running tests..."
	go test -v ./internal/...

test-coverage: ## Run tests with coverage
	@echo "Running tests with coverage..."
	go test -coverprofile=coverage.out ./internal/...
	go tool cover -html=coverage.out -o coverage.html

run: build ## Run the application
	@echo "Starting $(BINARY_NAME)..."
	$(BINARY_PATH)

dev: ## Run the application in development mode
	@echo "Starting $(BINARY_NAME) in development mode..."
	go run $(MAIN_PATH)

clean: ## Clean build artifacts
	@echo "Cleaning..."
	rm -rf bin/
	rm -f coverage.out coverage.html

lint: ## Run linter
	@echo "Running linter..."
	golangci-lint run

# Database commands
migrate-up: ## Run database migrations up
	@echo "Running database migrations up..."
	# TODO: Implement migration commands

migrate-down: ## Run database migrations down
	@echo "Running database migrations down..."
	# TODO: Implement migration commands

migrate-create: ## Create a new migration file
	@echo "Creating new migration..."
	# TODO: Implement migration creation

# Docker commands
docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t $(BINARY_NAME):latest .

docker-run: ## Run Docker container
	@echo "Running Docker container..."
	docker run -p 8080:8080 --env-file .env $(BINARY_NAME):latest

docker-compose-up: ## Start services with docker-compose
	@echo "Starting services with docker-compose..."
	docker-compose up -d

docker-compose-down: ## Stop services with docker-compose
	@echo "Stopping services with docker-compose..."
	docker-compose down

# Development database setup
db-create: ## Create development database
	@echo "Creating database $(DB_NAME)..."
	createdb -h $(DB_HOST) -p $(DB_PORT) -U $(DB_USER) $(DB_NAME)

db-drop: ## Drop development database
	@echo "Dropping database $(DB_NAME)..."
	dropdb -h $(DB_HOST) -p $(DB_PORT) -U $(DB_USER) $(DB_NAME)

db-reset: db-drop db-create ## Reset development database

# Code generation
gen: ## Generate code (swagger, mocks, etc.)
	@echo "Generating code..."
	# TODO: Add code generation commands

# Install tools
install-tools: ## Install development tools
	@echo "Installing development tools..."
	go install github.com/swaggo/swag/cmd/swag@latest
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Format code
fmt: ## Format Go code
	@echo "Formatting code..."
	go fmt ./...

# Check for security vulnerabilities  
security: ## Check for security vulnerabilities
	@echo "Checking for security vulnerabilities..."
	go list -json -m all | nancy sleuth

# Documentation
docs: ## Generate documentation
	@echo "Generating documentation..."
	# TODO: Add documentation generation
