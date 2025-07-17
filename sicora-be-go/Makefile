# Makefile para SICORA Backend Go Stack

.PHONY: help build clean test test-coverage run-all run-userservice run-scheduleservice run-attendanceservice run-projectevalservice run-evalinservice
.PHONY: docker-build docker-up docker-down dev-setup format lint db-migrate db-seed db-reset benchmark
.PHONY: lint test-quick test-coverage security-scan commit-check pre-commit ci-local

# Variables
SERVICES = userservice scheduleservice attendanceservice projectevalservice evalinservice
DOCKER_COMPOSE = docker compose
GO_VERSION = 1.21

# Colores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Mostrar ayuda
	@echo "$(BLUE)SICORA Backend Go Stack - Comandos Disponibles$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Desarrollo
dev-setup: ## Configuración inicial de desarrollo
	@echo "$(YELLOW)Configurando entorno de desarrollo...$(NC)"
	@go version
	@go mod download
	@go mod tidy
	@echo "$(GREEN)✓ Entorno configurado$(NC)"

build: ## Compilar todos los servicios
	@echo "$(YELLOW)Compilando servicios...$(NC)"
	@for service in $(SERVICES); do \
		echo "Compilando $$service..."; \
		cd $$service && go build -o bin/$$service ./cmd/main.go && cd ..; \
	done
	@echo "$(GREEN)✓ Servicios compilados$(NC)"

clean: ## Limpiar binarios y cache
	@echo "$(YELLOW)Limpiando archivos...$(NC)"
	@for service in $(SERVICES); do \
		rm -rf $$service/bin; \
	done
	@go clean -cache
	@echo "$(GREEN)✓ Limpieza completada$(NC)"

# Quality & CI/CD Commands
lint: ## Ejecutar linting
	@echo "$(YELLOW)Running Go linting...$(NC)"
	@golangci-lint run ./...
	@echo "$(GREEN)✓ Linting passed$(NC)"

test-quick: ## Tests rápidos para CI
	@echo "$(YELLOW)Running quick tests...$(NC)"
	@go test -short ./...
	@echo "$(GREEN)✓ Quick tests passed$(NC)"

test-coverage: ## Tests con cobertura
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	@go test -v -race -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html
	@echo "$(GREEN)✓ Tests with coverage completed$(NC)"

security-scan: ## Análisis de seguridad
	@echo "$(YELLOW)Running security scan...$(NC)"
	@gosec ./...
	@echo "$(GREEN)✓ Security scan completed$(NC)"

format: ## Formatear código
	@echo "$(YELLOW)Formatting code...$(NC)"
	@go fmt ./...
	@goimports -w .
	@echo "$(GREEN)✓ Code formatted$(NC)"

pre-commit: ## Ejecutar verificaciones pre-commit
	@echo "$(YELLOW)Running pre-commit checks...$(NC)"
	@go mod tidy
	@go fmt ./...
	@go vet ./...
	@go test -short ./...
	@echo "$(GREEN)✓ Pre-commit checks passed$(NC)"

commit-check: ## Verificar que el código está listo para commit
	@echo "$(YELLOW)Checking commit readiness...$(NC)"
	@$(MAKE) lint
	@$(MAKE) test-quick
	@$(MAKE) security-scan
	@echo "$(GREEN)✓ Code is ready for commit$(NC)"

ci-local: ## Simular CI localmente
	@echo "$(YELLOW)Ejecutando pipeline CI local...$(NC)"
	@$(MAKE) lint
	@$(MAKE) test-coverage
	@$(MAKE) security-scan
	@$(MAKE) build
	@echo "$(GREEN)✓ CI local completado exitosamente$(NC)"

# Git automation commands
commit: ## Commit automatizado con conventional commits
	@../scripts/universal-autocommit.sh

# Testing
test: ## Ejecutar todos los tests
	@echo "$(YELLOW)Ejecutando tests...$(NC)"
	@for service in $(SERVICES); do \
		echo "Testing $$service..."; \
		cd $$service && go test -v ./... && cd ..; \
	done
	@echo "$(GREEN)✓ Tests completados$(NC)"

test-integration: ## Tests de integración
	@echo "$(YELLOW)Ejecutando tests de integración...$(NC)"
	@$(DOCKER_COMPOSE) -f infra/docker/development/docker-compose.yml up -d postgres redis
	@sleep 5
	@for service in $(SERVICES); do \
		echo "Integration tests para $$service..."; \
		cd $$service && go test -tags=integration ./... && cd ..; \
	done
	@$(DOCKER_COMPOSE) -f infra/docker/development/docker-compose.yml down

benchmark: ## Ejecutar benchmarks
	@echo "$(YELLOW)Ejecutando benchmarks...$(NC)"
	@for service in $(SERVICES); do \
		echo "Benchmark para $$service..."; \
		cd $$service && go test -bench=. ./... && cd ..; \
	done

# Ejecución de servicios
run-all: ## Ejecutar todos los servicios
	@echo "$(YELLOW)Iniciando todos los servicios...$(NC)"
	@for service in $(SERVICES); do \
		echo "Iniciando $$service..."; \
		cd $$service && go run cmd/main.go & cd ..; \
	done
	@echo "$(GREEN)✓ Servicios iniciados$(NC)"

run-userservice: ## Ejecutar userservice
	@echo "$(YELLOW)Iniciando UserService...$(NC)"
	@cd userservice && go run cmd/main.go

run-scheduleservice: ## Ejecutar scheduleservice
	@echo "$(YELLOW)Iniciando ScheduleService...$(NC)"
	@cd scheduleservice && go run cmd/main.go

run-attendanceservice: ## Ejecutar attendanceservice
	@echo "$(YELLOW)Iniciando AttendanceService...$(NC)"
	@cd attendanceservice && go run cmd/main.go

run-projectevalservice: ## Ejecutar projectevalservice
	@echo "$(YELLOW)Iniciando ProjectEvalService...$(NC)"
	@cd projectevalservice && go run main.go

run-evalinservice: ## Ejecutar evalinservice
	@echo "$(YELLOW)Iniciando EvalinService...$(NC)"
	@cd evalinservice && go run cmd/main.go

# Docker
docker-build: ## Construir imágenes Docker
	@echo "$(YELLOW)Construyendo imágenes Docker...$(NC)"
	@$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)✓ Imágenes construidas$(NC)"

docker-up: ## Levantar servicios con Docker
	@echo "$(YELLOW)Iniciando servicios con Docker...$(NC)"
	@$(DOCKER_COMPOSE) -f infra/docker/development/docker-compose.yml up -d
	@echo "$(GREEN)✓ Servicios iniciados$(NC)"

docker-down: ## Detener servicios Docker
	@echo "$(YELLOW)Deteniendo servicios Docker...$(NC)"
	@$(DOCKER_COMPOSE) -f infra/docker/development/docker-compose.yml down
	@echo "$(GREEN)✓ Servicios detenidos$(NC)"

# Base de datos
db-migrate: ## Ejecutar migraciones
	@echo "$(YELLOW)Ejecutando migraciones...$(NC)"
	@for service in $(SERVICES); do \
		if [ -d "$$service/migrations" ]; then \
			echo "Migraciones para $$service..."; \
			cd $$service && go run migrations/main.go && cd ..; \
		fi; \
	done
	@echo "$(GREEN)✓ Migraciones completadas$(NC)"

db-seed: ## Cargar datos de prueba
	@echo "$(YELLOW)Cargando datos de prueba...$(NC)"
	@for service in $(SERVICES); do \
		if [ -f "$$service/seeds/main.go" ]; then \
			echo "Seeds para $$service..."; \
			cd $$service && go run seeds/main.go && cd ..; \
		fi; \
	done
	@echo "$(GREEN)✓ Datos cargados$(NC)"

db-reset: ## Resetear base de datos
	@echo "$(YELLOW)Reseteando base de datos...$(NC)"
	@$(DOCKER_COMPOSE) -f infra/docker/development/docker-compose.yml down -v
	@$(DOCKER_COMPOSE) -f infra/docker/development/docker-compose.yml up -d postgres
	@sleep 5
	@make db-migrate
	@make db-seed
	@echo "$(GREEN)✓ Base de datos reseteada$(NC)"

# Calidad de código
format: ## Formatear código
	@echo "$(YELLOW)Formateando código...$(NC)"
	@gofmt -w .
	@goimports -w .
	@echo "$(GREEN)✓ Código formateado$(NC)"

lint: ## Análisis estático
	@echo "$(YELLOW)Ejecutando análisis estático...$(NC)"
	@if command -v golangci-lint >/dev/null 2>&1; then \
		golangci-lint run ./...; \
	else \
		echo "$(RED)golangci-lint no instalado. Instalando...$(NC)"; \
		go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest; \
		golangci-lint run ./...; \
	fi
	@echo "$(GREEN)✓ Análisis completado$(NC)"

# Información
status: ## Mostrar estado de servicios
	@echo "$(BLUE)Estado de servicios:$(NC)"
	@for service in $(SERVICES); do \
		if pgrep -f "$$service" > /dev/null; then \
			echo "$(GREEN)✓ $$service: Running$(NC)"; \
		else \
			echo "$(RED)✗ $$service: Stopped$(NC)"; \
		fi; \
	done

logs: ## Mostrar logs de Docker
	@$(DOCKER_COMPOSE) -f infra/docker/development/docker-compose.yml logs -f

# Submódulos
update-submodules: ## Actualizar submódulos
	@echo "$(YELLOW)Actualizando submódulos...$(NC)"
	@git submodule update --remote
	@echo "$(GREEN)✓ Submódulos actualizados$(NC)"

# Swagger
swagger: ## Generar documentación Swagger
	@echo "$(YELLOW)Generando documentación Swagger...$(NC)"
	@for service in $(SERVICES); do \
		if [ -f "$$service/cmd/main.go" ]; then \
			echo "Swagger para $$service..."; \
			cd $$service && swag init -g cmd/main.go && cd ..; \
		fi; \
	done
	@echo "$(GREEN)✓ Documentación generada$(NC)"
