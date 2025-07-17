# Makefile para ProjectEval Service
.PHONY: help setup dev test lint format clean build deploy db-up db-migrate db-downgrade db-reset monitor validate

# Variables
PYTHON = python3
PIP = pip
UVICORN = uvicorn
DOCKER_COMPOSE = docker compose
SERVICE_NAME = projectevalservice
PORT = 8007

help: ## Mostrar ayuda
	@echo "📋 Comandos disponibles para ProjectEval Service:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

setup: ## Configurar entorno y ejecutar migraciones
	@echo "🚀 Configurando ProjectEval Service..."
	@chmod +x setup.sh dev.sh monitor.sh validate.sh
	@./setup.sh

dev: ## Iniciar servicio en modo desarrollo
	@echo "🚀 Iniciando en modo desarrollo..."
	@chmod +x dev.sh
	@./dev.sh

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	@if [ -d "venv" ]; then source venv/bin/activate; fi
	@$(PYTHON) -m pytest tests/ -v --cov=app --cov-report=term-missing

lint: ## Verificar código con pycodestyle
	@echo "🔍 Verificando código..."
	@if [ -d "venv" ]; then source venv/bin/activate; fi
	@pycodestyle app/ --max-line-length=88 --ignore=E203,W503
	@echo "✅ Código verificado"

format: ## Formatear código con black
	@echo "🎨 Formateando código..."
	@if [ -d "venv" ]; then source venv/bin/activate; fi
	@black app/ --line-length=88
	@echo "✅ Código formateado"

clean: ## Limpiar archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.log" -delete
	@echo "✅ Limpieza completada"

# Comandos de Docker
build: ## Construir imagen Docker
	@echo "🐳 Construyendo imagen Docker..."
	@docker build -t sicora/$(SERVICE_NAME):latest .
	@echo "✅ Imagen construida"

deploy: build ## Desplegar servicio con Docker
	@echo "🚀 Desplegando servicio..."
	@$(DOCKER_COMPOSE) up -d $(SERVICE_NAME)
	@echo "✅ Servicio desplegado en puerto $(PORT)"

# Comandos de Base de Datos
db-up: ## Iniciar PostgreSQL
	@echo "🐘 Iniciando PostgreSQL..."
	@cd ../.. && $(DOCKER_COMPOSE) up -d postgres
	@echo "⏱️ Esperando a que PostgreSQL esté listo..."
	@sleep 5
	@echo "✅ PostgreSQL iniciado"

db-migrate: ## Ejecutar migraciones de base de datos
	@echo "🗄️ Ejecutando migraciones..."
	@if [ -d "venv" ]; then source venv/bin/activate; fi
	@alembic upgrade head
	@echo "✅ Migraciones ejecutadas"

db-downgrade: ## Hacer rollback de migración
	@echo "⬇️ Haciendo rollback de migración..."
	@if [ -d "venv" ]; then source venv/bin/activate; fi
	@alembic downgrade -1
	@echo "✅ Rollback completado"

db-reset: ## Reiniciar base de datos completa (CUIDADO)
	@echo "⚠️ CUIDADO: Esto eliminará todos los datos"
	@read -p "¿Estás seguro? (yes/no): " confirm && [ "$$confirm" = "yes" ]
	@echo "🗄️ Reiniciando base de datos..."
	@docker exec sicora_postgres psql -U postgres -d sicora_dev -c "DROP SCHEMA IF EXISTS projectevalservice_schema CASCADE;"
	@docker exec sicora_postgres psql -U postgres -d sicora_dev -c "CREATE SCHEMA projectevalservice_schema;"
	@docker exec sicora_postgres psql -U postgres -d sicora_dev -c "GRANT ALL PRIVILEGES ON SCHEMA projectevalservice_schema TO sicora_migrator;"
	@$(MAKE) db-migrate
	@echo "✅ Base de datos reiniciada"

# Comandos de Monitoreo
monitor: ## Ejecutar monitoreo de rendimiento
	@echo "📊 Ejecutando monitoreo..."
	@chmod +x monitor.sh
	@./monitor.sh

validate: ## Validar conectividad con otros stacks
	@echo "🔗 Validando conectividad..."
	@chmod +x validate.sh
	@./validate.sh

# Comandos de instalación
install: ## Instalar dependencias
	@echo "📦 Instalando dependencias..."
	@$(PYTHON) -m venv venv
	@source venv/bin/activate && $(PIP) install -r requirements.txt
	@echo "✅ Dependencias instaladas"

install-dev: install ## Instalar dependencias de desarrollo
	@echo "📦 Instalando dependencias de desarrollo..."
	@source venv/bin/activate && $(PIP) install pytest pytest-cov black pycodestyle
	@echo "✅ Dependencias de desarrollo instaladas"

# Comando de información
info: ## Mostrar información del servicio
	@echo "📋 Información del Servicio:"
	@echo "  Nombre: ProjectEval Service"
	@echo "  Puerto: $(PORT)"
	@echo "  Esquema DB: projectevalservice_schema"
	@echo "  URL Docs: http://localhost:$(PORT)/docs"
	@echo "  URL Health: http://localhost:$(PORT)/api/v1/health"

# Estado del servicio
status: ## Mostrar estado del servicio y dependencias
	@echo "📊 Estado del servicio:"
	@echo ""
	@echo "🐘 PostgreSQL:"
	@docker exec sicora_postgres pg_isready -U postgres 2>/dev/null && echo "  ✅ Disponible" || echo "  ❌ No disponible"
	@echo ""
	@echo "🗄️ Esquema de base de datos:"
	@docker exec sicora_postgres psql -U postgres -d sicora_dev -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'projectevalservice_schema';" 2>/dev/null | sed 's/^/  📋 Tablas: /' || echo "  ❌ No accesible"
	@echo ""
	@echo "📡 Servicio HTTP:"
	@curl -s --connect-timeout 2 http://localhost:$(PORT)/docs > /dev/null 2>&1 && echo "  ✅ Disponible en http://localhost:$(PORT)" || echo "  ❌ No disponible"
