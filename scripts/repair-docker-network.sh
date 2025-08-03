#!/bin/bash

# 🔧 REPARACIÓN AUTOMÁTICA DE RED DOCKER - SICORA
# Archivo: scripts/repair-docker-network.sh
# Descripción: Script para reparar problemas comunes de red en Docker

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función de logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Función para pedir confirmación
confirm() {
    local message="$1"
    local default="${2:-y}"

    if [ "$default" = "y" ]; then
        local prompt="[Y/n]"
    else
        local prompt="[y/N]"
    fi

    read -p "$message $prompt: " -n 1 -r
    echo

    if [ "$default" = "y" ]; then
        [[ $REPLY =~ ^[Nn]$ ]] && return 1 || return 0
    else
        [[ $REPLY =~ ^[Yy]$ ]] && return 0 || return 1
    fi
}

# Función para backup de configuración
backup_config() {
    log "📦 Creando backup de configuración..."

    local backup_dir="/tmp/sicora-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_dir"

    # Backup de docker-compose.yml
    if [ -f "docker-compose.yml" ]; then
        cp docker-compose.yml "$backup_dir/"
        success "Backup de docker-compose.yml creado"
    fi

    # Backup de .env
    if [ -f ".env" ]; then
        cp .env "$backup_dir/"
        success "Backup de .env creado"
    fi

    echo "📍 Backup guardado en: $backup_dir"
}

# Detener servicios de forma segura
stop_services() {
    log "🛑 Deteniendo servicios SICORA..."

    # Cambiar al directorio correcto
    cd /home/epti/Documentos/epti-dev/sicora-app/sicora-infra/docker 2>/dev/null || cd /home/epti/Documentos/epti-dev/sicora-app

    if [ -f "docker-compose.yml" ]; then
        if docker compose ps --quiet | grep -q .; then
            docker compose down
            success "Servicios detenidos correctamente"
        else
            warning "No hay servicios ejecutándose"
        fi
    else
        error "No se encontró docker-compose.yml"
        return 1
    fi
}

# Limpiar redes huérfanas
clean_networks() {
    log "🧹 Limpiando redes Docker..."

    # Listar redes huérfanas
    local orphan_networks=$(docker network ls --filter "dangling=true" --format "{{.Name}}")

    if [ -n "$orphan_networks" ]; then
        warning "Redes huérfanas encontradas:"
        echo "$orphan_networks" | sed 's/^/   /'

        if confirm "¿Eliminar redes huérfanas?"; then
            docker network prune -f
            success "Redes huérfanas eliminadas"
        fi
    else
        success "No se encontraron redes huérfanas"
    fi
}

# Recrear red principal de SICORA
recreate_main_network() {
    log "🌐 Recreando red principal de SICORA..."

    local network_name="sicora-network"

    # Verificar si existe la red
    if docker network ls --format "{{.Name}}" | grep -q "^${network_name}$"; then
        warning "La red $network_name ya existe"

        if confirm "¿Recrear la red $network_name?"; then
            docker network rm "$network_name" 2>/dev/null || true
            success "Red anterior eliminada"
        else
            log "Manteniendo red existente"
            return 0
        fi
    fi

    # Crear nueva red
    if docker network create "$network_name" --driver bridge; then
        success "Red $network_name creada correctamente"
    else
        error "Error al crear la red $network_name"
        return 1
    fi
}

# Verificar conflictos de puertos
resolve_port_conflicts() {
    log "🔌 Verificando conflictos de puertos..."

    local conflicted_ports=()
    local ports=("5432" "27017" "6379")

    for port in "${ports[@]}"; do
        if netstat -tulpn 2>/dev/null | grep -q ":$port " && ! netstat -tulpn 2>/dev/null | grep ":$port " | grep -q "docker"; then
            conflicted_ports+=("$port")
        fi
    done

    if [ ${#conflicted_ports[@]} -gt 0 ]; then
        warning "Puertos en conflicto detectados: ${conflicted_ports[*]}"
        echo ""
        echo "Servicios locales que pueden estar causando conflictos:"

        for port in "${conflicted_ports[@]}"; do
            echo "Puerto $port:"
            netstat -tulpn 2>/dev/null | grep ":$port " | sed 's/^/   /'
        done

        echo ""
        echo "💡 Soluciones sugeridas:"
        echo "   1. Detener servicios locales: sudo systemctl stop postgresql redis-server"
        echo "   2. Cambiar puertos en docker-compose.yml"
        echo "   3. Usar puertos alternativos (ej: PostgreSQL en 5433)"

        if confirm "¿Intentar detener servicios locales conflictivos?"; then
            sudo systemctl stop postgresql 2>/dev/null && success "PostgreSQL local detenido" || warning "No se pudo detener PostgreSQL"
            sudo systemctl stop redis-server 2>/dev/null && success "Redis local detenido" || warning "No se pudo detener Redis"
        fi
    else
        success "No se detectaron conflictos de puertos"
    fi
}

# Limpiar volúmenes huérfanos (opcional)
clean_volumes() {
    log "🗂️  Verificando volúmenes Docker..."

    local orphan_volumes=$(docker volume ls --filter "dangling=true" --format "{{.Name}}")

    if [ -n "$orphan_volumes" ]; then
        warning "Volúmenes huérfanos encontrados:"
        echo "$orphan_volumes" | sed 's/^/   /'

        echo ""
        echo "⚠️  ADVERTENCIA: Eliminar volúmenes eliminará TODOS los datos persistentes"
        echo "   Esto incluye bases de datos, archivos de configuración, etc."

        if confirm "¿Eliminar volúmenes huérfanos? (PELIGROSO)" "n"; then
            docker volume prune -f
            warning "Volúmenes eliminados - Los datos se han perdido"
        else
            log "Volúmenes conservados"
        fi
    else
        success "No se encontraron volúmenes huérfanos"
    fi
}

# Iniciar servicios
start_services() {
    log "🚀 Iniciando servicios SICORA..."

    if [ -f "docker-compose.yml" ]; then
        # Iniciar en modo detached
        if docker compose up -d; then
            success "Servicios iniciados correctamente"

            # Esperar un momento para la inicialización
            log "⏳ Esperando inicialización de servicios..."
            sleep 10

            # Verificar estado
            docker compose ps
        else
            error "Error al iniciar servicios"
            return 1
        fi
    else
        error "No se encontró docker-compose.yml"
        return 1
    fi
}

# Verificar salud de servicios
verify_health() {
    log "🏥 Verificando salud de servicios..."

    local services=("mongodb:27017" "postgres:5432" "redis:6379")
    local all_healthy=true

    for service_port in "${services[@]}"; do
        IFS=':' read -r service port <<< "$service_port"

        # Buscar contenedor por nombre (varios formatos posibles)
        local container_name=""
        for name_pattern in "sicora_${service}" "sicora-${service}" "${service}"; do
            if docker ps --format "{{.Names}}" | grep -q "^${name_pattern}$"; then
                container_name="$name_pattern"
                break
            fi
        done

        if [ -n "$container_name" ]; then
            # Verificar si el contenedor está healthy
            local status=$(docker inspect "$container_name" --format='{{.State.Status}}')

            if [ "$status" = "running" ]; then
                # Probar conectividad al puerto
                local ip=$(docker inspect "$container_name" --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')

                if nc -z "$ip" "$port" 2>/dev/null; then
                    success "$service ($container_name) - Saludable"
                else
                    warning "$service ($container_name) - Puerto $port no accesible"
                    all_healthy=false
                fi
            else
                error "$service ($container_name) - Estado: $status"
                all_healthy=false
            fi
        else
            warning "$service - Contenedor no encontrado"
            all_healthy=false
        fi
    done

    if [ "$all_healthy" = true ]; then
        success "Todos los servicios están saludables"
    else
        warning "Algunos servicios presentan problemas"
        echo ""
        echo "💡 Para más detalles, ejecutar:"
        echo "   docker compose logs"
        echo "   ./scripts/diagnose-docker-network.sh"
    fi
}

# Función principal
main() {
    echo "🔧 REPARACIÓN AUTOMÁTICA DE RED DOCKER - SICORA"
    echo "=============================================="
    echo ""

    # Verificar que Docker esté ejecutándose
    if ! docker info &> /dev/null; then
        error "Docker daemon no está ejecutándose"
        echo "Iniciar con: sudo systemctl start docker"
        exit 1
    fi

    # Cambiar al directorio correcto
    if [ -d "/home/epti/Documentos/epti-dev/sicora-app/sicora-infra/docker" ]; then
        cd /home/epti/Documentos/epti-dev/sicora-app/sicora-infra/docker
    elif [ -d "/home/epti/Documentos/epti-dev/sicora-app" ]; then
        cd /home/epti/Documentos/epti-dev/sicora-app
    else
        error "No se encontró el directorio del proyecto SICORA"
        exit 1
    fi

    log "Trabajando en directorio: $(pwd)"

    # Ejecutar pasos de reparación
    backup_config
    stop_services
    resolve_port_conflicts
    clean_networks
    recreate_main_network

    # Preguntar sobre limpieza de volúmenes
    if confirm "¿Ejecutar limpieza de volúmenes? (ELIMINA DATOS)"; then
        clean_volumes
    fi

    start_services
    verify_health

    echo ""
    success "🎉 Reparación completada"
    echo ""
    echo "📋 Resumen de acciones realizadas:"
    echo "   ✅ Backup de configuración creado"
    echo "   ✅ Servicios reiniciados"
    echo "   ✅ Redes Docker limpiadas"
    echo "   ✅ Red principal recreada"
    echo "   ✅ Conflictos de puertos verificados"
    echo "   ✅ Salud de servicios verificada"
    echo ""
    echo "💡 Próximos pasos:"
    echo "   1. Verificar logs: docker compose logs"
    echo "   2. Monitorear: docker compose ps"
    echo "   3. Diagnóstico: ./scripts/diagnose-docker-network.sh"
}

# Ejecutar función principal
main "$@"
