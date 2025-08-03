#!/bin/bash

# 🔍 DIAGNÓSTICO DE RED DOCKER - SICORA
# Archivo: scripts/diagnose-docker-network.sh
# Descripción: Diagnóstico automatizado de problemas de red en Docker

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

# Función para verificar comandos necesarios
check_dependencies() {
    local deps=("docker" "netstat" "ping" "nc")
    local missing=()

    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done

    # Verificar docker compose (V2, sin guión)
    if ! docker compose version &> /dev/null; then
        missing+=("docker-compose-v2")
    fi

    if [ ${#missing[@]} -ne 0 ]; then
        error "Dependencias faltantes: ${missing[*]}"
        if [[ " ${missing[@]} " =~ " docker-compose-v2 " ]]; then
            echo "Docker Compose V2 no disponible. Verificar instalación de Docker."
        else
            echo "Instalar con: sudo apt install ${missing[*]}"
        fi
        exit 1
    fi
}

# Verificar estado de Docker daemon
check_docker_daemon() {
    log "Verificando Docker daemon..."

    if ! docker info &> /dev/null; then
        error "Docker daemon no está ejecutándose"
        echo "Iniciar con: sudo systemctl start docker"
        exit 1
    fi

    success "Docker daemon está activo"
}

# Verificar contenedores SICORA
check_containers() {
    log "📊 Estado de contenedores SICORA:"

    # Cambiar al directorio correcto
    cd /home/epti/Documentos/epti-dev/sicora-app/sicora-infra/docker 2>/dev/null || cd /home/epti/Documentos/epti-dev/sicora-app

    # Verificar si hay docker-compose.yml
    if [ ! -f "docker-compose.yml" ]; then
        warning "No se encontró docker-compose.yml en el directorio actual"
        echo "Directorio actual: $(pwd)"
        echo "Archivos disponibles:"
        ls -la | grep -E "(yml|yaml)"
        return 1
    fi

    # Mostrar estado de contenedores
    if docker compose ps --quiet | grep -q .; then
        docker compose ps --format table
        success "Contenedores listados correctamente"
    else
        warning "No hay contenedores ejecutándose"
        echo "Iniciar con: docker compose up -d"
    fi
}

# Verificar puertos ocupados
check_ports() {
    log "🔌 Verificando puertos SICORA:"

    local ports=("5432:PostgreSQL Local" "5433:PostgreSQL Docker" "27017:MongoDB" "6379:Redis" "3000:Frontend" "8080:Backend")

    for port_info in "${ports[@]}"; do
        IFS=':' read -r port service <<< "$port_info"

        if netstat -tulpn 2>/dev/null | grep -q ":$port "; then
            # Verificar si es nuestro contenedor o servicio externo
            if netstat -tulpn 2>/dev/null | grep ":$port " | grep -q "docker"; then
                success "$service (Puerto $port) - Docker container"
            else
                warning "$service (Puerto $port) - Servicio local (posible conflicto)"
            fi
        else
            echo "   $service (Puerto $port) - Libre"
        fi
    done
}

# Verificar redes Docker
check_networks() {
    log "🌐 Verificando redes Docker:"

    local networks=$(docker network ls --format "{{.Name}}" | grep -i sicora)

    if [ -n "$networks" ]; then
        echo "$networks" | while read -r network; do
            success "Red encontrada: $network"

            # Mostrar contenedores en la red
            local containers=$(docker network inspect "$network" --format '{{range $id, $config := .Containers}}{{$config.Name}} {{end}}')
            if [ -n "$containers" ]; then
                echo "   Contenedores: $containers"
            else
                echo "   Sin contenedores conectados"
            fi
        done
    else
        warning "No se encontraron redes SICORA"
        echo "Redes disponibles:"
        docker network ls
    fi
}

# Probar conectividad
check_connectivity() {
    log "📡 Probando conectividad de servicios:"

    local services=("sicora_mongodb:27017" "sicora_postgres:5432" "sicora_redis:6379" "sicora-mongodb:27017" "sicora-postgres:5432" "sicora-redis:6379")

    for service_port in "${services[@]}"; do
        IFS=':' read -r service port <<< "$service_port"

        if docker ps --format "{{.Names}}" | grep -q "$service"; then
            # Obtener IP del contenedor
            local ip=$(docker inspect "$service" --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 2>/dev/null)

            if [ -n "$ip" ]; then
                success "$service está ejecutándose (IP: $ip)"

                # Probar conectividad
                if ping -c 1 -W 1 "$ip" > /dev/null 2>&1; then
                    echo "   ✅ Ping OK"
                else
                    echo "   ❌ Ping falló"
                fi

                # Probar puerto específico
                if nc -z "$ip" "$port" 2>/dev/null; then
                    echo "   ✅ Puerto $port accesible"
                else
                    echo "   ❌ Puerto $port inaccesible"
                fi
            else
                warning "$service ejecutándose pero sin IP asignada"
            fi
        else
            echo "   $service no está ejecutándose"
        fi
    done
}

# Verificar logs de errores recientes
check_recent_errors() {
    log "📋 Buscando errores recientes en logs:"

    local error_patterns=("error" "failed" "connection refused" "bind.*address already in use" "network.*unreachable")
    local found_errors=false

    for pattern in "${error_patterns[@]}"; do
        local errors=$(docker compose logs --since 10m 2>/dev/null | grep -i "$pattern" | tail -3)
        if [ -n "$errors" ]; then
            if [ "$found_errors" = false ]; then
                found_errors=true
                echo ""
            fi
            warning "Patrón '$pattern' encontrado:"
            echo "$errors" | sed 's/^/   /'
        fi
    done

    if [ "$found_errors" = false ]; then
        success "No se encontraron errores recientes"
    fi
}

# Verificar recursos del sistema
check_system_resources() {
    log "💻 Verificando recursos del sistema:"

    # Memoria
    local mem_usage=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
    echo "   Memoria utilizada: ${mem_usage}%"

    # Disco
    local disk_usage=$(df / | tail -1 | awk '{printf "%.1f", $3/$2 * 100.0}')
    echo "   Disco utilizado: ${disk_usage}%"

    # Docker system info
    local docker_info=$(docker system df --format "table {{.Type}}\t{{.Size}}" 2>/dev/null | tail -n +2)
    if [ -n "$docker_info" ]; then
        echo "   Uso de Docker:"
        echo "$docker_info" | sed 's/^/     /'
    fi
}

# Generar reporte final
generate_report() {
    log "📄 Generando reporte de diagnóstico..."

    local report_file="/tmp/sicora-docker-diagnosis-$(date +%Y%m%d-%H%M%S).txt"

    {
        echo "REPORTE DE DIAGNÓSTICO DOCKER - SICORA"
        echo "======================================"
        echo "Fecha: $(date)"
        echo "Usuario: $(whoami)"
        echo "Directorio: $(pwd)"
        echo ""

        echo "=== ESTADO DE CONTENEDORES ==="
        docker compose ps 2>/dev/null || echo "Error al obtener estado de contenedores"
        echo ""

        echo "=== REDES DOCKER ==="
        docker network ls | grep sicora
        echo ""

        echo "=== PUERTOS OCUPADOS ==="
        netstat -tulpn | grep -E "(5432|5433|27017|6379)" || echo "Sin puertos SICORA ocupados"
        echo ""

        echo "=== LOGS RECIENTES CON ERRORES ==="
        docker compose logs --since 15m 2>/dev/null | grep -i "error\|failed" | tail -10 || echo "Sin errores recientes"

    } > "$report_file"

    success "Reporte guardado en: $report_file"
    echo "Ver con: cat $report_file"
}

# Función principal
main() {
    echo "🔍 DIAGNÓSTICO DE RED DOCKER - SICORA"
    echo "====================================="
    echo ""

    check_dependencies
    check_docker_daemon
    check_containers
    check_ports
    check_networks
    check_connectivity
    check_recent_errors
    check_system_resources
    generate_report

    echo ""
    success "✅ Diagnóstico completado"
    echo ""
    echo "💡 Próximos pasos sugeridos:"
    echo "   1. Si hay errores, ejecutar: ./scripts/repair-docker-network.sh"
    echo "   2. Para monitoreo continuo: docker compose logs -f"
    echo "   3. Para reinicio completo: docker compose down && docker compose up -d"
}

# Ejecutar función principal
main "$@"
