#!/bin/bash

# 🏥 VERIFICACIÓN DE SALUD AUTOMÁTICA - SERVICIOS SICORA
# Archivo: scripts/health-check-services.sh
# Descripción: Monitoreo continuo de la salud de servicios Docker

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
HEALTH_CHECK_INTERVAL=30
MAX_RETRIES=3
LOG_FILE="/tmp/sicora-health-$(date +%Y%m%d).log"

# Función de logging
log() {
    local message="$1"
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')
    echo -e "${BLUE}[$timestamp]${NC} $message"
    echo "[$timestamp] $message" >> "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] SUCCESS: $1" >> "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1" >> "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$LOG_FILE"
}

# Verificar conectividad a un servicio
check_service_connectivity() {
    local service_name="$1"
    local host="$2"
    local port="$3"
    local timeout="${4:-5}"

    if timeout "$timeout" nc -z "$host" "$port" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Verificar salud de MongoDB
check_mongodb_health() {
    local service="MongoDB"
    local retries=0

    while [ $retries -lt $MAX_RETRIES ]; do
        # Verificar conectividad básica
        if check_service_connectivity "$service" "localhost" "27017" 3; then
            # Verificar acceso con mongo client (si está disponible)
            if command -v mongosh &> /dev/null; then
                if mongosh --eval "db.adminCommand('ping')" --quiet localhost:27017 &>/dev/null; then
                    success "$service - Conectividad y acceso OK"
                    return 0
                else
                    warning "$service - Puerto accesible pero servicio no responde"
                fi
            else
                success "$service - Puerto accesible (mongosh no disponible para test completo)"
                return 0
            fi
        else
            warning "$service - Puerto 27017 no accesible (intento $((retries + 1))/$MAX_RETRIES)"
        fi

        retries=$((retries + 1))
        [ $retries -lt $MAX_RETRIES ] && sleep 2
    done

    error "$service - Falló después de $MAX_RETRIES intentos"
    return 1
}

# Verificar salud de PostgreSQL
check_postgresql_health() {
    local service="PostgreSQL"
    local retries=0

    while [ $retries -lt $MAX_RETRIES ]; do
        # Verificar puerto 5433 (Docker)
        if check_service_connectivity "$service" "localhost" "5433" 3; then
            # Verificar acceso con psql (si está disponible)
            if command -v psql &> /dev/null; then
                if PGPASSWORD=sicora_password psql -h localhost -p 5433 -U sicora_user -d sicora_dev -c "SELECT 1;" &>/dev/null; then
                    success "$service - Conectividad y acceso OK"
                    return 0
                else
                    warning "$service - Puerto accesible pero falló autenticación"
                fi
            else
                success "$service - Puerto accesible (psql no disponible para test completo)"
                return 0
            fi
        else
            warning "$service - Puerto 5433 no accesible (intento $((retries + 1))/$MAX_RETRIES)"
        fi

        retries=$((retries + 1))
        [ $retries -lt $MAX_RETRIES ] && sleep 2
    done

    error "$service - Falló después de $MAX_RETRIES intentos"
    return 1
}

# Verificar salud de Redis
check_redis_health() {
    local service="Redis"
    local retries=0

    while [ $retries -lt $MAX_RETRIES ]; do
        # Verificar conectividad básica
        if check_service_connectivity "$service" "localhost" "6379" 3; then
            # Verificar acceso con redis-cli (si está disponible)
            if command -v redis-cli &> /dev/null; then
                if redis-cli -h localhost -p 6379 ping 2>/dev/null | grep -q "PONG"; then
                    success "$service - Conectividad y acceso OK"
                    return 0
                else
                    warning "$service - Puerto accesible pero servicio no responde"
                fi
            else
                success "$service - Puerto accesible (redis-cli no disponible para test completo)"
                return 0
            fi
        else
            warning "$service - Puerto 6379 no accesible (intento $((retries + 1))/$MAX_RETRIES)"
        fi

        retries=$((retries + 1))
        [ $retries -lt $MAX_RETRIES ] && sleep 2
    done

    error "$service - Falló después de $MAX_RETRIES intentos"
    return 1
}

# Verificar contenedores Docker
check_docker_containers() {
    log "🐳 Verificando estado de contenedores Docker..."

    local containers=("sicora_mongodb" "sicora_postgres" "sicora_redis" "sicora-mongodb" "sicora-postgres" "sicora-redis")
    local found_containers=()

    for container in "${containers[@]}"; do
        if docker ps --format "{{.Names}}" | grep -q "^${container}$"; then
            local status=$(docker inspect "$container" --format='{{.State.Status}}' 2>/dev/null)
            local health=$(docker inspect "$container" --format='{{.State.Health.Status}}' 2>/dev/null)

            if [ "$status" = "running" ]; then
                if [ "$health" = "healthy" ] || [ "$health" = "<no value>" ]; then
                    success "$container - Running (Status: $status)"
                else
                    warning "$container - Running pero Health: $health"
                fi
            else
                error "$container - Estado: $status"
            fi

            found_containers+=("$container")
        fi
    done

    if [ ${#found_containers[@]} -eq 0 ]; then
        warning "No se encontraron contenedores SICORA ejecutándose"
        return 1
    else
        log "Contenedores encontrados: ${#found_containers[@]}"
    fi
}

# Verificar uso de recursos
check_resource_usage() {
    log "💻 Verificando uso de recursos..."

    # Memoria del sistema
    local mem_total=$(free -m | awk 'NR==2{printf "%.0f", $2}')
    local mem_used=$(free -m | awk 'NR==2{printf "%.0f", $3}')
    local mem_percent=$(awk "BEGIN {printf \"%.1f\", ($mem_used/$mem_total)*100}")

    echo "   Memoria: ${mem_used}MB/${mem_total}MB (${mem_percent}%)"

    # Disco
    local disk_percent=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    echo "   Disco: ${disk_percent}% utilizado"

    # Recursos Docker específicos
    if docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null | grep -q sicora; then
        echo "   Contenedores SICORA:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep sicora | sed 's/^/     /'
    fi

    # Alertas de recursos
    if [ "$mem_percent" = "$(echo "$mem_percent > 90" | bc 2>/dev/null)" ]; then
        warning "Memoria del sistema muy alta: ${mem_percent}%"
    fi

    if [ "$disk_percent" -gt 90 ] 2>/dev/null; then
        warning "Espacio en disco muy bajo: ${disk_percent}%"
    fi
}

# Verificar logs de errores recientes
check_recent_errors() {
    log "📋 Verificando errores recientes..."

    local error_count=0
    local warning_count=0

    # Buscar errores en logs de Docker
    if command -v docker &> /dev/null; then
        local recent_errors=$(docker compose logs --since 5m 2>/dev/null | grep -i "error\|failed\|exception" | wc -l)
        local recent_warnings=$(docker compose logs --since 5m 2>/dev/null | grep -i "warning\|warn" | wc -l)

        error_count=$((error_count + recent_errors))
        warning_count=$((warning_count + recent_warnings))
    fi

    if [ "$error_count" -gt 0 ]; then
        warning "Se encontraron $error_count errores en los últimos 5 minutos"
        echo "   Ver detalles con: docker compose logs --since 5m | grep -i error"
    fi

    if [ "$warning_count" -gt 0 ]; then
        echo "   $warning_count warnings encontrados (normal en ciertos casos)"
    fi

    if [ "$error_count" -eq 0 ] && [ "$warning_count" -eq 0 ]; then
        success "No se encontraron errores recientes"
    fi
}

# Ejecutar verificación completa
run_health_check() {
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')

    echo "🏥 VERIFICACIÓN DE SALUD SICORA - $timestamp"
    echo "============================================="
    echo ""

    local failures=0

    # Verificar contenedores
    if ! check_docker_containers; then
        failures=$((failures + 1))
    fi

    echo ""

    # Verificar servicios
    log "🔍 Verificando conectividad de servicios..."

    if ! check_mongodb_health; then
        failures=$((failures + 1))
    fi

    if ! check_postgresql_health; then
        failures=$((failures + 1))
    fi

    if ! check_redis_health; then
        failures=$((failures + 1))
    fi

    echo ""

    # Verificar recursos y errores
    check_resource_usage
    echo ""
    check_recent_errors

    echo ""
    echo "================================================="

    if [ $failures -eq 0 ]; then
        success "✅ Todos los servicios están saludables"
        return 0
    else
        warning "⚠️  $failures servicio(s) presentan problemas"
        echo ""
        echo "💡 Acciones recomendadas:"
        echo "   1. Revisar logs: docker compose logs"
        echo "   2. Ejecutar diagnóstico: ./scripts/diagnose-docker-network.sh"
        echo "   3. Reparar problemas: ./scripts/repair-docker-network.sh"
        return 1
    fi
}

# Modo monitoreo continuo
run_continuous_monitoring() {
    log "🔄 Iniciando monitoreo continuo (intervalo: ${HEALTH_CHECK_INTERVAL}s)"
    log "📄 Logs guardándose en: $LOG_FILE"
    echo "   Presiona Ctrl+C para detener"
    echo ""

    local check_count=0

    while true; do
        check_count=$((check_count + 1))

        echo "🔄 Verificación #$check_count"
        echo "===================="

        if run_health_check; then
            echo "✅ Verificación #$check_count completada - Todo OK"
        else
            echo "⚠️  Verificación #$check_count completada - Con problemas"
        fi

        echo ""
        echo "⏳ Próxima verificación en ${HEALTH_CHECK_INTERVAL} segundos..."
        echo "============================================="
        echo ""

        sleep "$HEALTH_CHECK_INTERVAL"
    done
}

# Función de ayuda
show_help() {
    echo "🏥 VERIFICACIÓN DE SALUD SICORA"
    echo "==============================="
    echo ""
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  check         Ejecutar verificación única (por defecto)"
    echo "  monitor       Ejecutar monitoreo continuo"
    echo "  status        Estado rápido de servicios"
    echo "  help          Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0                    # Verificación única"
    echo "  $0 monitor           # Monitoreo continuo"
    echo "  $0 status            # Estado rápido"
    echo ""
}

# Estado rápido
quick_status() {
    echo "⚡ ESTADO RÁPIDO SICORA"
    echo "======================"

    # Contenedores
    local running_containers=$(docker ps --format "{{.Names}}" | grep -c sicora 2>/dev/null || echo "0")
    echo "🐳 Contenedores ejecutándose: $running_containers"

    # Puertos
    local open_ports=()
    for port in 27017 5433 6379; do
        if nc -z localhost "$port" 2>/dev/null; then
            open_ports+=("$port")
        fi
    done
    echo "🔌 Puertos accesibles: ${open_ports[*]:-ninguno}"

    # Memoria
    local mem_percent=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    echo "💻 Uso de memoria: ${mem_percent}%"

    echo ""
    if [ ${#open_ports[@]} -gt 0 ] && [ "$running_containers" -gt 0 ]; then
        success "Estado general: OK"
    else
        warning "Estado general: Con problemas"
    fi
}

# Función principal
main() {
    case "${1:-check}" in
        "check")
            run_health_check
            ;;
        "monitor")
            run_continuous_monitoring
            ;;
        "status")
            quick_status
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            echo "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
}

# Manejo de señales para limpieza
cleanup() {
    echo ""
    log "🛑 Deteniendo monitoreo..."
    exit 0
}

trap cleanup INT TERM

# Verificar dependencias básicas
if ! command -v docker &> /dev/null; then
    error "Docker no está instalado o no está en PATH"
    exit 1
fi

# Ejecutar función principal
main "$@"
