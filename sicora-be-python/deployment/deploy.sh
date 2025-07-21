#!/bin/bash
# Script de deployment para SICORA Backend Python
# Maneja deployment para diferentes entornos

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
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

# Verificar argumentos
if [ $# -lt 1 ]; then
    log_error "Uso: $0 <environment> [service]"
    log "Entornos disponibles: development, testing, staging, production"
    log "Servicios disponibles: apigateway, notification, all"
    exit 1
fi

ENVIRONMENT=$1
SERVICE=${2:-all}
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

log "🚀 Iniciando deployment de SICORA Backend Python"
log "📁 Directorio del proyecto: $PROJECT_ROOT"
log "🌍 Entorno: $ENVIRONMENT"
log "🔧 Servicio: $SERVICE"

# Validar entorno
case $ENVIRONMENT in
    development|testing|staging|production)
        log_success "Entorno válido: $ENVIRONMENT"
        ;;
    *)
        log_error "Entorno inválido: $ENVIRONMENT"
        log "Entornos válidos: development, testing, staging, production"
        exit 1
        ;;
esac

# Función para verificar dependencias
check_dependencies() {
    log "🔍 Verificando dependencias..."

    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 no está instalado"
        exit 1
    fi

    # Verificar Docker (para staging/production)
    if [[ "$ENVIRONMENT" == "staging" || "$ENVIRONMENT" == "production" ]]; then
        if ! command -v docker &> /dev/null; then
            log_error "Docker no está instalado"
            exit 1
        fi

        if ! command -v docker compose &> /dev/null; then
            log_error "Docker Compose no está instalado"
            exit 1
        fi
    fi

    log_success "Dependencias verificadas"
}

# Función para configurar entorno Python
setup_python_env() {
    log "🐍 Configurando entorno Python..."

    cd "$PROJECT_ROOT"

    # Crear/activar entorno virtual si es development/testing
    if [[ "$ENVIRONMENT" == "development" || "$ENVIRONMENT" == "testing" ]]; then
        if [ ! -d "venv" ]; then
            log "Creando entorno virtual..."
            python3 -m venv venv
        fi

        source venv/bin/activate
        log "Entorno virtual activado"
    fi

    # Instalar dependencias
    log "Instalando dependencias..."
    pip install -r requirements.txt

    if [[ "$ENVIRONMENT" == "development" || "$ENVIRONMENT" == "testing" ]]; then
        pip install -r requirements-dev.txt
    fi

    log_success "Entorno Python configurado"
}

# Función para configurar variables de entorno
setup_environment() {
    log "⚙️ Configurando variables de entorno..."

    local env_file=".env.${ENVIRONMENT}"

    if [ ! -f "$PROJECT_ROOT/$env_file" ]; then
        log_error "Archivo de configuración no encontrado: $env_file"
        exit 1
    fi

    # Copiar archivo de entorno
    cp "$PROJECT_ROOT/$env_file" "$PROJECT_ROOT/.env"
    log_success "Variables de entorno configuradas desde $env_file"
}

# Función para ejecutar tests
run_tests() {
    if [[ "$ENVIRONMENT" == "development" || "$ENVIRONMENT" == "testing" ]]; then
        log "🧪 Ejecutando tests..."

        cd "$PROJECT_ROOT"

        # Configurar base de datos de test
        if [ -f "scripts/setup_test_db_simple.py" ]; then
            python scripts/setup_test_db_simple.py
        fi

        # Ejecutar tests
        python -m pytest tests/ -v --tb=short

        if [ $? -eq 0 ]; then
            log_success "Tests ejecutados exitosamente"
        else
            log_error "Fallos en los tests"
            exit 1
        fi
    else
        log_warning "Tests omitidos en entorno $ENVIRONMENT"
    fi
}

# Función para deploy de development/testing
deploy_local() {
    log "🏠 Deployment local para $ENVIRONMENT"

    cd "$PROJECT_ROOT"

    case $SERVICE in
        apigateway)
            log "Iniciando APIGateway..."
            cd apigateway
            uvicorn main:app --host 0.0.0.0 --port 8000 --reload
            ;;
        notification)
            log "Iniciando NotificationService..."
            cd notificationservice-template
            uvicorn main:app --host 0.0.0.0 --port 8001 --reload
            ;;
        all)
            log "Iniciando todos los servicios..."
            log_warning "Para desarrollo, ejecute cada servicio en terminales separadas:"
            log "APIGateway: cd apigateway && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
            log "NotificationService: cd notificationservice-template && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"
            ;;
    esac
}

# Función para deploy con Docker
deploy_docker() {
    log "🐳 Deployment con Docker para $ENVIRONMENT"

    cd "$PROJECT_ROOT"

    # Construir imágenes
    log "Construyendo imágenes Docker..."

    if [[ "$SERVICE" == "apigateway" || "$SERVICE" == "all" ]]; then
        docker build -f deployment/Dockerfile.apigateway -t sicora-apigateway:$ENVIRONMENT .
    fi

    if [[ "$SERVICE" == "notification" || "$SERVICE" == "all" ]]; then
        docker build -f deployment/Dockerfile.notification -t sicora-notification:$ENVIRONMENT .
    fi

    # Ejecutar con docker-compose
    log "Iniciando servicios con Docker Compose..."
    docker compose -f deployment/docker-compose.$ENVIRONMENT.yml up -d

    log_success "Servicios iniciados con Docker"
}

# Función para verificar salud de servicios
health_check() {
    log "🏥 Verificando salud de servicios..."

    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        log "Intento $attempt/$max_attempts..."

        # Verificar APIGateway
        if [[ "$SERVICE" == "apigateway" || "$SERVICE" == "all" ]]; then
            if curl -f -s http://localhost:8000/health > /dev/null; then
                log_success "APIGateway está saludable"
            else
                log_warning "APIGateway no responde en el intento $attempt"
            fi
        fi

        # Verificar NotificationService
        if [[ "$SERVICE" == "notification" || "$SERVICE" == "all" ]]; then
            if curl -f -s http://localhost:8001/health > /dev/null; then
                log_success "NotificationService está saludable"
            else
                log_warning "NotificationService no responde en el intento $attempt"
            fi
        fi

        sleep 2
        ((attempt++))
    done
}

# Función principal
main() {
    log "🎯 Iniciando proceso de deployment..."

    check_dependencies
    setup_environment
    setup_python_env
    run_tests

    # Seleccionar tipo de deployment
    case $ENVIRONMENT in
        development|testing)
            deploy_local
            ;;
        staging|production)
            deploy_docker
            health_check
            ;;
    esac

    log_success "🎉 Deployment completado exitosamente!"
    log "📊 Para monitorear los servicios:"
    log "   - Health: curl http://localhost:8000/health"
    log "   - Metrics: curl http://localhost:8000/metrics"
    log "   - Docs: http://localhost:8000/docs"
}

# Ejecutar función principal
main "$@"
