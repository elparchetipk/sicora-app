# Makefile for SICORA KbService

.PHONY: help build run test clean docker-up docker-down migrate lint format deps check

# Default target
help:
	@echo "Available targets:"
	@echo "  build        - Build the application"
	@echo "  run          - Run the application"
	@echo "  test         - Run tests"
	@echo "  test-cover   - Run tests with coverage"
	@echo "  clean        - Clean build artifacts"
	@echo "  docker-up    - Start Docker services"
	@echo "  docker-down  - Stop Docker services"
	@echo "  docker-logs  - View Docker logs"
	@echo "  migrate      - Run database migrations"
	@echo "  lint         - Run linter"
	@echo "  format       - Format code"
	@echo "  deps         - Download dependencies"
	@echo "  check        - Run all checks (lint, test, etc.)"
	@echo "  dev          - Start development environment"

# Build the application
build:
	@echo "Building KbService..."
	go build -o bin/kbservice ./cmd/server

# Run the application
run:
	@echo "Running KbService..."
	go run ./cmd/server

# Run tests
test:
	@echo "Running tests..."
	go test -v ./...

# Run tests with coverage
test-cover:
	@echo "Running tests with coverage..."
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report generated: coverage.html"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf bin/
	rm -f coverage.out coverage.html
	go clean ./...

# Start Docker services
docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d

# Stop Docker services
docker-down:
	@echo "Stopping Docker services..."
	docker-compose down

# View Docker logs
docker-logs:
	@echo "Viewing Docker logs..."
	docker-compose logs -f kbservice

# Build and start Docker services
docker-build:
	@echo "Building and starting Docker services..."
	docker-compose up -d --build

# Run database migrations
migrate:
	@echo "Running database migrations..."
	go run ./cmd/server -migrate

# Run linter
lint:
	@echo "Running linter..."
	golangci-lint run

# Format code
format:
	@echo "Formatting code..."
	go fmt ./...
	goimports -w .

# Download dependencies
deps:
	@echo "Downloading dependencies..."
	go mod download
	go mod tidy

# Install development tools
install-tools:
	@echo "Installing development tools..."
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install golang.org/x/tools/cmd/goimports@latest

# Run all checks
check: lint test
	@echo "All checks passed!"

# Start development environment
dev: docker-up
	@echo "Development environment started!"
	@echo "Services:"
	@echo "  - PostgreSQL: localhost:5432"
	@echo "  - Redis: localhost:6379"
	@echo "  - Elasticsearch: localhost:9200"
	@echo "  - Kibana: localhost:5601"
	@echo "  - Prometheus: localhost:9090"
	@echo "  - Grafana: localhost:3000 (admin/admin)"
	@echo ""
	@echo "Starting KbService..."
	@sleep 10  # Wait for services to be ready
	make run

# Stop development environment
dev-stop: docker-down
	@echo "Development environment stopped!"

# Database operations
db-reset:
	@echo "Resetting database..."
	docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS sicora_kb;"
	docker-compose exec postgres psql -U postgres -c "CREATE DATABASE sicora_kb;"
	make migrate

# Backup database
db-backup:
	@echo "Backing up database..."
	docker-compose exec postgres pg_dump -U postgres sicora_kb > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Restore database
db-restore:
	@echo "Restoring database..."
	@read -p "Enter backup file path: " file; \
	docker-compose exec -T postgres psql -U postgres sicora_kb < $$file

# Generate API documentation
docs:
	@echo "Generating API documentation..."
	swag init -g cmd/server/main.go -o docs/

# Performance testing
perf-test:
	@echo "Running performance tests..."
	go test -bench=. -benchmem ./...

# Security scan
security:
	@echo "Running security scan..."
	gosec ./...

# Generate mocks for testing
mocks:
	@echo "Generating mocks..."
	mockgen -source=internal/domain/repositories/document_repository.go -destination=mocks/document_repository_mock.go
	mockgen -source=internal/domain/repositories/faq_repository.go -destination=mocks/faq_repository_mock.go

# Production build
build-prod:
	@echo "Building for production..."
	CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-extldflags "-static"' -o bin/kbservice ./cmd/server

# Docker production build
docker-prod:
	@echo "Building production Docker image..."
	docker build -t sicora/kbservice:latest .

# Health check
health:
	@echo "Checking service health..."
	curl -f http://localhost:8080/health || exit 1

# Load sample data
seed:
	@echo "Loading sample data..."
	go run ./scripts/seed/main.go

# Monitor logs
logs:
	@echo "Monitoring logs..."
	tail -f logs/app.log

# Git hooks setup
setup-hooks:
	@echo "Setting up git hooks..."
	cp scripts/hooks/pre-commit .git/hooks/
	chmod +x .git/hooks/pre-commit

# Update dependencies
update-deps:
	@echo "Updating dependencies..."
	go get -u ./...
	go mod tidy

# Vendor dependencies
vendor:
	@echo "Vendoring dependencies..."
	go mod vendor
