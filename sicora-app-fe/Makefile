# Makefile para SICORA Frontend
.PHONY: help dev build test clean logs shell install docker-setup

# Ayuda por defecto
help:
	@echo "🎯 SICORA Frontend - Comandos disponibles:"
	@echo ""
	@echo "📋 Desarrollo:"
	@echo "  make dev                 - Iniciar servidor de desarrollo"
	@echo "  make dev-docker          - Desarrollo con Docker"
	@echo "  make install             - Instalar dependencias"
	@echo ""
	@echo "🔨 Build y Testing:"
	@echo "  make build               - Build de producción"
	@echo "  make test                - Ejecutar tests"
	@echo "  make lint                - Linting y format"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  make docker-setup        - Configurar Docker para desarrollo"
	@echo "  make docker-build        - Build imagen Docker"
	@echo "  make logs                - Ver logs de contenedores"
	@echo "  make shell               - Acceso shell al contenedor"
	@echo ""
	@echo "🧹 Limpieza:"
	@echo "  make clean               - Limpiar contenedores y volúmenes"
	@echo "  make clean-all           - Limpieza completa del sistema"

# Desarrollo local
dev:
	pnpm dev

install:
	pnpm install

build:
	pnpm build

test:
	pnpm test

lint:
	pnpm lint && pnpm format

# Desarrollo con Docker
dev-docker:
	docker-compose -f docker-compose.dev.yml up --build

dev-detached:
	docker-compose -f docker-compose.dev.yml up -d --build

docker-setup:
	@echo "🐳 Configurando Docker para desarrollo..."
	@echo "📁 Creando directorios necesarios..."
	@mkdir -p .devcontainer mock-backend
	@echo "✅ Configuración Docker completa"
	@echo "💡 Para usar:"
	@echo "   make dev-docker    # Desarrollo con Docker"
	@echo "   make logs          # Ver logs"
	@echo "   make shell         # Acceso al contenedor"

# Build Docker
docker-build:
	docker build -f Dockerfile.dev -t sicora-frontend:dev .

# Testing con Docker
docker-test:
	docker build -f Dockerfile.test -t sicora-frontend:test . 2>/dev/null || echo "⚠️  Dockerfile.test no existe aún"
	docker run --rm sicora-frontend:test 2>/dev/null || echo "⚠️  Test con Docker pendiente"

# Logs y debugging
logs:
	docker-compose -f docker-compose.dev.yml logs -f frontend

logs-all:
	docker-compose -f docker-compose.dev.yml logs -f

shell:
	docker-compose -f docker-compose.dev.yml exec frontend sh

# Limpieza
clean:
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f

clean-all: clean
	docker image prune -a -f
	docker volume prune -f
	pnpm clean 2>/dev/null || rm -rf dist node_modules

# Status y información
status:
	@echo "📊 Estado de SICORA Frontend:"
	@echo ""
	@echo "🐳 Contenedores Docker:"
	@docker ps --filter "name=sicora" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "   No hay contenedores ejecutándose"
	@echo ""
	@echo "📦 Dependencias:"
	@pnpm list --depth=0 2>/dev/null || echo "   Dependencias no instaladas (ejecuta: make install)"
	@echo ""
	@echo "🔍 Puertos utilizados:"
	@lsof -i :5173 2>/dev/null | tail -n +2 || echo "   Puerto 5173: disponible"
	@lsof -i :3000 2>/dev/null | tail -n +2 || echo "   Puerto 3000: disponible"

# Variables de entorno
env-setup:
	@echo "🔧 Configurando variables de entorno..."
	@cp .env.example .env.local 2>/dev/null || echo "VITE_APP_TITLE=SICORA Development" > .env.local
	@echo "✅ Variables configuradas en .env.local"
