#!/bin/bash
# Script para validar endpoints después del deployment en VPS
# Este script debe ejecutarse DESPUÉS del deployment para verificar que todo funciona

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

log_info() {
    echo -e "${PURPLE}[INFO]${NC} $1"
}

# Variables
DOMAIN=${1:-localhost}
PROTOCOL=${2:-http}
BASE_URL="${PROTOCOL}://${DOMAIN}"

# Contadores
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Función para ejecutar test
run_test() {
    local test_name="$1"
    local url="$2"
    local expected_status="$3"
    local expected_content="$4"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    log "🧪 Testing: $test_name"
    log_info "URL: $url"

    # Realizar request
    response=$(curl -s -w "HTTP_STATUS:%{http_code}\n" "$url" 2>/dev/null || echo "HTTP_STATUS:000")

    # Extraer status code
    status_code=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
    content=$(echo "$response" | grep -v "HTTP_STATUS:")

    # Validar status code
    if [ "$status_code" = "$expected_status" ]; then
        log_success "✓ Status Code: $status_code"
    else
        log_error "✗ Status Code: $status_code (expected: $expected_status)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi

    # Validar contenido si se especifica
    if [ -n "$expected_content" ]; then
        if echo "$content" | grep -q "$expected_content"; then
            log_success "✓ Content contains: $expected_content"
        else
            log_error "✗ Content doesn't contain: $expected_content"
            log_info "Actual content: $content"
            FAILED_TESTS=$((FAILED_TESTS + 1))
            return 1
        fi
    fi

    PASSED_TESTS=$((PASSED_TESTS + 1))
    log_success "✅ $test_name: PASSED"
    echo ""
    return 0
}

# Función para test de health check extendido
test_health_extended() {
    local service_name="$1"
    local url="$2"

    log "🏥 Testing extended health check: $service_name"

    # Test básico
    response=$(curl -s "$url" 2>/dev/null || echo "FAILED")

    if [[ "$response" == *"ok"* ]] || [[ "$response" == *"healthy"* ]]; then
        log_success "✓ Basic health check passed"

        # Medir tiempo de respuesta
        response_time=$(curl -w "%{time_total}" -s -o /dev/null "$url" 2>/dev/null || echo "0.000")
        log_info "Response time: ${response_time}s"

        # Verificar headers
        headers=$(curl -I -s "$url" 2>/dev/null || echo "")
        if echo "$headers" | grep -q "200 OK"; then
            log_success "✓ HTTP headers OK"
        else
            log_warning "⚠ Unexpected headers"
        fi

        return 0
    else
        log_error "✗ Health check failed"
        log_info "Response: $response"
        return 1
    fi
}

# Función para test de documentación Swagger
test_swagger_docs() {
    local service_name="$1"
    local url="$2"

    log "📚 Testing Swagger documentation: $service_name"

    # Test que la página carga
    response=$(curl -s -w "HTTP_STATUS:%{http_code}\n" "$url" 2>/dev/null || echo "HTTP_STATUS:000")
    status_code=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
    content=$(echo "$response" | grep -v "HTTP_STATUS:")

    if [ "$status_code" = "200" ]; then
        log_success "✓ Swagger docs accessible"

        # Verificar que contiene elementos típicos de Swagger
        if echo "$content" | grep -q -i "swagger\|openapi\|api documentation"; then
            log_success "✓ Contains Swagger/OpenAPI content"
        else
            log_warning "⚠ Might not be proper Swagger documentation"
        fi

        return 0
    else
        log_error "✗ Swagger docs not accessible (Status: $status_code)"
        return 1
    fi
}

# Función principal de validación
main() {
    log "🚀 Iniciando validación de endpoints SICORA Backend"
    log "🌐 Base URL: $BASE_URL"
    echo ""

    # Tests de health checks básicos
    log "=== HEALTH CHECKS BÁSICOS ==="
    run_test "API Gateway Health" "$BASE_URL/health/api" "200" "ok"
    run_test "Notification Service Health" "$BASE_URL/health/notification" "200" "ok"

    # Tests de health checks directos (para debugging)
    if [ "$DOMAIN" = "localhost" ]; then
        log "=== HEALTH CHECKS DIRECTOS (localhost only) ==="
        run_test "API Gateway Direct Health" "http://localhost:8000/health" "200" "ok"
        run_test "Notification Service Direct Health" "http://localhost:8001/health" "200" "ok"
    fi

    # Tests de endpoints principales
    log "=== ENDPOINTS PRINCIPALES ==="
    run_test "API Gateway Root" "$BASE_URL/api/" "200" ""
    run_test "Notification Service Root" "$BASE_URL/notifications/" "200" ""

    # Tests de documentación
    log "=== DOCUMENTACIÓN SWAGGER ==="
    test_swagger_docs "API Gateway" "$BASE_URL/api/docs"
    test_swagger_docs "Notification Service" "$BASE_URL/notifications/docs"

    # Tests extendidos de health
    log "=== HEALTH CHECKS EXTENDIDOS ==="
    test_health_extended "API Gateway" "$BASE_URL/health/api"
    test_health_extended "Notification Service" "$BASE_URL/health/notification"

    # Test de status page
    log "=== STATUS PAGE ==="
    run_test "Status Page" "$BASE_URL/status" "200" "SICORA"

    # Resumen final
    echo ""
    log "=== RESUMEN DE RESULTADOS ==="
    log_info "Total tests ejecutados: $TOTAL_TESTS"
    log_success "Tests pasados: $PASSED_TESTS"

    if [ $FAILED_TESTS -gt 0 ]; then
        log_error "Tests fallidos: $FAILED_TESTS"
        echo ""
        log_error "❌ Validación FALLIDA - Revisar configuración del deployment"

        # Sugerencias de debugging
        echo ""
        log "🔍 DEBUGGING SUGGESTIONS:"
        log "1. Verificar que los contenedores estén corriendo:"
        log "   docker ps"
        log ""
        log "2. Verificar logs de servicios:"
        log "   docker logs sicora-backend_apigateway_1"
        log "   docker logs sicora-backend_notification_1"
        log ""
        log "3. Verificar configuración de Nginx:"
        log "   sudo nginx -t"
        log "   sudo systemctl status nginx"
        log ""
        log "4. Verificar conectividad interna:"
        log "   curl http://localhost:8000/health"
        log "   curl http://localhost:8001/health"

        exit 1
    else
        log_success "✅ Validación EXITOSA - Todos los tests pasaron"
        echo ""
        log "🎉 ¡SICORA Backend está correctamente desplegado y funcionando!"
        echo ""
        log "📝 URLs importantes:"
        log "   API Gateway: $BASE_URL/api/"
        log "   Notification Service: $BASE_URL/notifications/"
        log "   API Documentation: $BASE_URL/api/docs"
        log "   Notification Documentation: $BASE_URL/notifications/docs"
        log "   Health Check API: $BASE_URL/health/api"
        log "   Health Check Notifications: $BASE_URL/health/notification"
        echo ""
        log "✅ El backend está listo para integración con el frontend"

        exit 0
    fi
}

# Función de ayuda
show_help() {
    echo "Uso: $0 [DOMAIN] [PROTOCOL]"
    echo ""
    echo "Parámetros:"
    echo "  DOMAIN    - Dominio o IP del servidor (default: localhost)"
    echo "  PROTOCOL  - http o https (default: http)"
    echo ""
    echo "Ejemplos:"
    echo "  $0                          # Test localhost con http"
    echo "  $0 mi-servidor.com          # Test mi-servidor.com con http"
    echo "  $0 mi-servidor.com https    # Test mi-servidor.com con https"
    echo "  $0 192.168.1.100            # Test IP específica con http"
}

# Verificar argumentos
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

# Ejecutar validación
main "$@"
