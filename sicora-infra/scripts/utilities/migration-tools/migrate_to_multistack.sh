#!/bin/bash

# Script de Migración Multi-Stack
# Migra servicios existentes a la nueva estructura multi-stack

echo "🚀 Iniciando migración a estructura multi-stack..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    log_error "Este script debe ejecutarse desde el directorio raíz del proyecto (donde está docker-compose.yml)"
    exit 1
fi

# Lista de servicios a migrar
SERVICES=("userservice" "attendanceservice" "scheduleservice" "kbservice" "evalinservice" "aiservice" "apigateway")

# Crear directorio 01-fastapi si no existe
mkdir -p 01-fastapi

log_info "Migrando servicios a 01-fastapi/..."

# Migrar cada servicio
for service in "${SERVICES[@]}"; do
    if [ -d "$service" ]; then
        log_info "Migrando $service..."
        
        # Verificar si el servicio ya existe en destino
        if [ -d "01-fastapi/$service" ]; then
            log_warning "01-fastapi/$service ya existe. Saltando..."
            continue
        fi
        
        # Copiar (no mover) para mantener backup
        cp -r "$service" "01-fastapi/"
        
        if [ $? -eq 0 ]; then
            log_success "✅ $service migrado a 01-fastapi/"
        else
            log_error "❌ Error migrando $service"
        fi
    else
        log_warning "Servicio $service no encontrado en directorio raíz"
    fi
done

log_info "Verificando migración..."

# Verificar que los servicios fueron migrados correctamente
echo -e "\n📁 Estructura 01-fastapi/:"
ls -la 01-fastapi/

echo -e "\n🔍 Verificación de archivos principales:"
for service in "${SERVICES[@]}"; do
    if [ -f "01-fastapi/$service/main.py" ]; then
        log_success "✅ 01-fastapi/$service/main.py"
    elif [ -d "01-fastapi/$service" ]; then
        log_warning "⚠️  01-fastapi/$service/ existe pero sin main.py"
    else
        log_error "❌ 01-fastapi/$service/ no migrado"
    fi
done

echo -e "\n🔄 Próximos pasos manuales:"
echo "1. Actualizar docker-compose.yml para nueva estructura"
echo "2. Actualizar paths en nginx/nginx.conf"
echo "3. Validar que servicios arrancan desde nueva ubicación"
echo "4. Actualizar documentación con nuevos paths"
echo "5. Una vez validado, eliminar servicios de directorio raíz"

echo -e "\n📋 Comandos de validación sugeridos:"
echo "cd 01-fastapi/userservice && python main.py"
echo "cd 01-fastapi/kbservice && uvicorn main:app --reload --port 8001"

log_success "🎉 Migración completada. Revisar próximos pasos manuales."
