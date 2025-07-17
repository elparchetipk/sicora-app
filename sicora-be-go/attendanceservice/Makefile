# Makefile para AttendanceService

.PHONY: help build run stop clean test docker-build docker-run docker-stop docker-clean

# Variables
DOCKER_IMAGE_NAME = attendanceservice
DOCKER_CONTAINER_NAME = attendanceservice
DOCKER_COMPOSE_FILE = docker-compose.yml

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@echo "  build          - Compilar la aplicación"
	@echo "  run            - Ejecutar la aplicación localmente"
	@echo "  test           - Ejecutar tests"
	@echo "  docker-build   - Construir imagen Docker"
	@echo "  docker-run     - Ejecutar con Docker Compose"
	@echo "  docker-stop    - Detener servicios Docker"
	@echo "  docker-clean   - Limpiar recursos Docker"
	@echo "  clean          - Limpiar archivos temporales"

build: ## Compilar la aplicación
	@echo "Compilando AttendanceService..."
	go mod tidy
	go build -o main ./cmd/server
	@echo "Compilación completada!"

run: build ## Ejecutar la aplicación localmente
	@echo "Ejecutando AttendanceService..."
	./main

test: ## Ejecutar tests
	@echo "Ejecutando tests..."
	go test ./tests/integration/... -v
	@echo "Tests completados!"

docker-build: ## Construir imagen Docker
	@echo "Construyendo imagen Docker..."
	docker build -t $(DOCKER_IMAGE_NAME) .
	@echo "Imagen Docker construida!"

docker-run: ## Ejecutar con Docker Compose
	@echo "Iniciando servicios con Docker Compose..."
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d
	@echo "Servicios iniciados!"
	@echo "AttendanceService disponible en: http://localhost:8003"
	@echo "Swagger UI disponible en: http://localhost:8003/swagger/index.html"
	@echo "Health check: http://localhost:8003/health"

docker-stop: ## Detener servicios Docker
	@echo "Deteniendo servicios Docker..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	@echo "Servicios detenidos!"

docker-clean: docker-stop ## Limpiar recursos Docker
	@echo "Limpiando recursos Docker..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down -v --rmi all
	docker system prune -f
	@echo "Recursos Docker limpiados!"

clean: ## Limpiar archivos temporales
	@echo "Limpiando archivos temporales..."
	rm -f main
	go clean
	@echo "Limpieza completada!"

logs: ## Ver logs de Docker
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f

status: ## Ver estado de servicios
	docker compose -f $(DOCKER_COMPOSE_FILE) ps
