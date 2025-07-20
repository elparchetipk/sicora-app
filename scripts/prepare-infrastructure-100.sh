#!/bin/bash

# SICORA - Script de Preparación de Infraestructura para Completitud 100%
# Versión: 1.0
# Fecha: 19 de julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"

echo -e "${BLUE}🏗️ SICORA - Preparación de Infraestructura para 100% Completitud${NC}"
echo "=================================================================="
echo ""

# Función para logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar Docker
check_docker() {
    log_info "🐳 Verificando Docker..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker no está instalado"
        exit 1
    fi

    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose no está disponible"
        exit 1
    fi

    log_success "Docker está disponible"
}

# Iniciar PostgreSQL
start_postgresql() {
    log_info "🐘 Iniciando PostgreSQL..."

    cd "$PROJECT_ROOT/sicora-infra"

    # Verificar si PostgreSQL ya está ejecutándose
    if docker compose -f docker/docker-compose.yml ps postgres | grep -q "Up"; then
        log_warning "PostgreSQL ya está ejecutándose"
        return 0
    fi

    # Iniciar PostgreSQL
    docker compose -f docker/docker-compose.yml up -d postgres

    # Esperar a que PostgreSQL esté listo
    log_info "Esperando a que PostgreSQL esté listo..."
    sleep 10

    # Verificar conexión
    for i in {1..30}; do
        if docker compose -f docker/docker-compose.yml exec postgres pg_isready -U sicora_user &>/dev/null; then
            log_success "PostgreSQL está listo"
            return 0
        fi
        sleep 2
    done

    log_error "PostgreSQL no pudo iniciarse correctamente"
    return 1
}

# Iniciar Redis
start_redis() {
    log_info "🔄 Iniciando Redis..."

    cd "$PROJECT_ROOT/sicora-infra"

    # Verificar si Redis ya está ejecutándose
    if docker compose -f docker/docker-compose.yml ps redis | grep -q "Up"; then
        log_warning "Redis ya está ejecutándose"
        return 0
    fi

    # Iniciar Redis
    docker compose -f docker/docker-compose.yml up -d redis

    # Esperar a que Redis esté listo
    log_info "Esperando a que Redis esté listo..."
    sleep 5

    # Verificar conexión usando docker exec
    for i in {1..30}; do
        if docker compose -f docker/docker-compose.yml exec redis redis-cli ping | grep -q "PONG"; then
            log_success "Redis está listo"
            return 0
        fi
        sleep 2
    done

    log_error "Redis no pudo iniciarse correctamente"
    return 1
}

# Crear bases de datos necesarias
create_databases() {
    log_info "🗄️ Creando bases de datos necesarias..."

    cd "$PROJECT_ROOT/sicora-infra"

    # Crear base de datos para APIGateway
    docker compose -f docker/docker-compose.yml exec postgres createdb -U sicora_user sicora_gateway 2>/dev/null || log_warning "Base de datos sicora_gateway ya existe"

    # Crear base de datos para NotificationService
    docker compose -f docker/docker-compose.yml exec postgres createdb -U sicora_user sicora_notifications 2>/dev/null || log_warning "Base de datos sicora_notifications ya existe"

    log_success "Bases de datos verificadas"
}

# Verificar conectividad
verify_connectivity() {
    log_info "🔍 Verificando conectividad..."

    cd "$PROJECT_ROOT/sicora-infra"

    # Verificar PostgreSQL
    if docker compose -f docker/docker-compose.yml exec postgres psql -U sicora_user -d sicora_dev -c "SELECT 1;" &>/dev/null; then
        log_success "✅ PostgreSQL conectividad OK"
    else
        log_error "❌ PostgreSQL no responde"
        return 1
    fi

    # Verificar Redis
    if docker compose -f docker/docker-compose.yml exec redis redis-cli ping | grep -q "PONG"; then
        log_success "✅ Redis conectividad OK"
    else
        log_error "❌ Redis no responde"
        return 1
    fi

    return 0
}

# Mostrar estado de servicios
show_services_status() {
    log_info "📊 Estado actual de servicios:"
    echo ""

    cd "$PROJECT_ROOT/sicora-infra"

    echo -e "${BLUE}PostgreSQL:${NC}"
    docker compose -f docker/docker-compose.yml ps postgres
    echo ""

    echo -e "${BLUE}Redis:${NC}"
    docker compose -f docker/docker-compose.yml ps redis
    echo ""

    echo -e "${BLUE}Puertos disponibles:${NC}"
    echo "  - PostgreSQL: localhost:5433"
    echo "  - Redis: localhost:6379"
    echo ""
}

# Instalar dependencias Python si es necesario
install_python_deps() {
    log_info "🐍 Verificando dependencias Python..."

    # Verificar si pip está disponible
    if ! command -v pip3 &> /dev/null; then
        log_warning "pip3 no está disponible, saltando instalación de dependencias"
        return 0
    fi

    # Instalar dependencias básicas si no están
    pip3 install --user redis &>/dev/null || log_warning "No se pudo instalar redis"
    pip3 install --user psycopg2-binary &>/dev/null || log_warning "No se pudo instalar psycopg2-binary"

    log_success "Dependencias Python verificadas"
}

# Función principal
main() {
    echo -e "${BLUE}Iniciando preparación de infraestructura...${NC}"
    echo ""

    # Verificar Docker
    check_docker

    # Instalar dependencias Python
    install_python_deps

    # Iniciar servicios
    start_postgresql
    start_redis

    # Crear bases de datos
    create_databases

    # Verificar conectividad
    if verify_connectivity; then
        log_success "🎉 Infraestructura lista para desarrollo"
    else
        log_error "❌ Problemas de conectividad detectados"
        return 1
    fi

    # Mostrar estado
    show_services_status

    echo ""
    log_info "📝 Próximos pasos:"
    echo "1. Ejecutar: bash scripts/complete-backend-python-100.sh"
    echo "2. Seleccionar qué fases implementar"
    echo "3. Validar el resultado final"
    echo ""

    return 0
}

# Manejo de señales
cleanup() {
    log_info "🧹 Limpiando recursos..."
    echo ""
    log_info "Para detener servicios más tarde:"
    echo "cd $PROJECT_ROOT/sicora-infra && docker compose -f docker/docker-compose.yml down"
}

trap cleanup EXIT

# Ejecutar función principal
main "$@"
