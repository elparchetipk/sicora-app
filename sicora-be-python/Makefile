# Makefile para SICORA Backend Python Stack (FastAPI)

.PHONY: help install clean test test-coverage run-all run-userservice run-scheduleservice run-attendanceservice run-evalinservice run-evalproyservice run-kbservice run-aiservice run-apigateway
.PHONY: docker-build docker-up docker-down dev-setup format lint db-migrate db-seed db-reset coverage
.PHONY: lint test-quick test-coverage security-scan commit-check pre-commit ci-local format-check

# Variables
SERVICES = userservice scheduleservice attendanceservice evalinservice evalproyservice kbservice aiservice apigateway
PYTHON = python3.13
VENV = venv
DOCKER_COMPOSE = docker compose

# Colores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Mostrar ayuda
	@echo "$(BLUE)SICORA Backend Python Stack - Comandos Disponibles$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Desarrollo
dev-setup: ## Configuración inicial de desarrollo
	@echo "$(YELLOW)Configurando entorno de desarrollo Python...$(NC)"
	@$(PYTHON) --version
	@$(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip setuptools wheel
	@$(VENV)/bin/pip install --no-cache-dir -r requirements.txt
	@echo "$(GREEN)✓ Entorno configurado. Activa con: source $(VENV)/bin/activate$(NC)"

dev-install: ## Instalar dependencias de desarrollo
	@echo "$(YELLOW)Instalando dependencias de desarrollo...$(NC)"
	@$(VENV)/bin/pip install --no-cache-dir -r requirements-dev.txt
	@echo "$(GREEN)✓ Dependencias de desarrollo instaladas$(NC)"

install: ## Instalar dependencias básicas
	@echo "$(YELLOW)Instalando dependencias básicas...$(NC)"
	@$(VENV)/bin/pip install --no-cache-dir -r requirements.txt
	@echo "$(GREEN)✓ Dependencias instaladas$(NC)"

clean: ## Limpiar cache y archivos temporales
	@echo "$(YELLOW)Limpiando archivos...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@echo "$(GREEN)✓ Limpieza completada$(NC)"

# Quality & CI/CD Commands
lint: ## Ejecutar linters
	@echo "$(YELLOW)Running Python linting...$(NC)"
	@$(VENV)/bin/flake8 app/ --max-line-length=88 --extend-ignore=E203,W503
	@$(VENV)/bin/black --check app/
	@$(VENV)/bin/isort --check-only app/
	@echo "$(GREEN)✓ Linting passed$(NC)"

format: ## Formatear código
	@echo "$(YELLOW)Formatting Python code...$(NC)"
	@$(VENV)/bin/black app/
	@$(VENV)/bin/isort app/ --profile black
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Verificar formato sin modificar
	@echo "$(YELLOW)Checking Python code format...$(NC)"
	@$(VENV)/bin/black --check app/
	@$(VENV)/bin/isort --check-only app/
	@echo "$(GREEN)✓ Format check passed$(NC)"

test-quick: ## Tests rápidos para CI
	@echo "$(YELLOW)Running quick tests...$(NC)"
	@$(VENV)/bin/pytest -v --tb=short --maxfail=5
	@echo "$(GREEN)✓ Quick tests passed$(NC)"

test-coverage: ## Tests con cobertura
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	@$(VENV)/bin/pytest --cov=app --cov-report=xml --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Tests with coverage completed$(NC)"

security-scan: ## Análisis de seguridad
	@echo "$(YELLOW)Running security scan...$(NC)"
	@$(VENV)/bin/bandit -r app/
	@$(VENV)/bin/safety check
	@echo "$(GREEN)✓ Security scan completed$(NC)"

pre-commit: ## Ejecutar verificaciones pre-commit
	@echo "$(YELLOW)Running pre-commit checks...$(NC)"
	@$(VENV)/bin/black app/
	@$(VENV)/bin/isort app/ --profile black
	@$(VENV)/bin/flake8 app/ --max-line-length=88 --extend-ignore=E203,W503
	@$(VENV)/bin/pytest -v --tb=short --maxfail=5
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
	@echo "$(GREEN)✓ CI local completado exitosamente$(NC)"

# Ejecución de servicios
run-all: ## Ejecutar todos los servicios
	@echo "$(YELLOW)Iniciando todos los servicios FastAPI...$(NC)"
	@echo "$(BLUE)Servicios disponibles en:$(NC)"
	@echo "  - APIGateway: http://localhost:8000"
	@echo "  - UserService: http://localhost:8001"
	@echo "  - ScheduleService: http://localhost:8002"
	@echo "  - AttendanceService: http://localhost:8003"
	@echo "  - EvalinService: http://localhost:8004"
	@echo "  - EvalproyService: http://localhost:8005"
	@echo "  - KbService: http://localhost:8006"
	@echo "  - AIService: http://localhost:8007"

run-apigateway: ## Ejecutar API Gateway
	@echo "$(YELLOW)Iniciando API Gateway...$(NC)"
	@cd apigateway && ../$(VENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run-userservice: ## Ejecutar UserService
	@echo "$(YELLOW)Iniciando UserService...$(NC)"
	@cd userservice && ../$(VENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8001 --reload

run-scheduleservice: ## Ejecutar ScheduleService
	@echo "$(YELLOW)Iniciando ScheduleService...$(NC)"
	@cd scheduleservice && ../$(VENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8002 --reload

run-attendanceservice: ## Ejecutar AttendanceService
	@echo "$(YELLOW)Iniciando AttendanceService...$(NC)"
	@cd attendanceservice && ../$(VENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8003 --reload

run-evalinservice: ## Ejecutar EvalinService
	@echo "$(YELLOW)Iniciando EvalinService...$(NC)"
	@cd evalinservice && ../$(VENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8004 --reload

run-evalproyservice: ## Ejecutar EvalproyService
	@echo "$(YELLOW)Iniciando EvalproyService...$(NC)"
	@cd evalproyservice && ../$(VENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8005 --reload

run-kbservice: ## Ejecutar KbService
	@echo "$(YELLOW)Iniciando KbService...$(NC)"
	@cd kbservice && ../$(VENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8006 --reload

run-aiservice: ## Ejecutar AIService
	@echo "$(YELLOW)Iniciando AIService...$(NC)"
	@cd aiservice && ../$(VENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8007 --reload

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
		if [ -f "$$service/alembic.ini" ]; then \
			echo "Migraciones para $$service..."; \
			cd $$service && ../$(VENV)/bin/alembic upgrade head && cd ..; \
		fi; \
	done
	@echo "$(GREEN)✓ Migraciones completadas$(NC)"

db-seed: ## Cargar datos de prueba
	@echo "$(YELLOW)Cargando datos de prueba...$(NC)"
	@for service in $(SERVICES); do \
		if [ -f "$$service/seed_data.py" ]; then \
			echo "Seeds para $$service..."; \
			cd $$service && ../$(VENV)/bin/python seed_data.py && cd ..; \
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

# Información
status: ## Mostrar estado de servicios
	@echo "$(BLUE)Estado de servicios FastAPI:$(NC)"
	@for port in 8000 8001 8002 8003 8004 8005 8006 8007; do \
		if curl -s http://localhost:$$port/health > /dev/null 2>&1; then \
			echo "$(GREEN)✓ Puerto $$port: Running$(NC)"; \
		else \
			echo "$(RED)✗ Puerto $$port: Stopped$(NC)"; \
		fi; \
	done

validate: ## Validar compatibilidad Python 3.13
	@echo "$(YELLOW)Validando compatibilidad Python 3.13...$(NC)"
	@$(PYTHON) scripts/validate-python313.py

validate-env: ## Validar entorno virtual
	@echo "$(YELLOW)Validando entorno virtual...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(RED)❌ Entorno virtual no encontrado$(NC)"; \
		echo "$(BLUE)Ejecuta: make dev-setup$(NC)"; \
		exit 1; \
	fi
	@$(VENV)/bin/python --version
	@$(VENV)/bin/pip list | head -5
	@echo "$(GREEN)✓ Entorno virtual válido$(NC)"

logs: ## Mostrar logs de Docker
	@$(DOCKER_COMPOSE) -f infra/docker/development/docker-compose.yml logs -f

# Submódulos
update-submodules: ## Actualizar submódulos
	@echo "$(YELLOW)Actualizando submódulos...$(NC)"
	@git submodule update --remote
	@echo "$(GREEN)✓ Submódulos actualizados$(NC)"

# Entorno virtual
venv: ## Crear entorno virtual
	@echo "$(YELLOW)Creando entorno virtual...$(NC)"
	@$(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@echo "$(GREEN)✓ Entorno virtual creado. Activa con: source $(VENV)/bin/activate$(NC)"

activate: ## Mostrar comando para activar entorno virtual
	@echo "$(BLUE)Para activar el entorno virtual, ejecuta:$(NC)"
	@echo "source $(VENV)/bin/activate"

commit: ## Commit automatizado con conventional commits
	@../scripts/universal-autocommit.sh
