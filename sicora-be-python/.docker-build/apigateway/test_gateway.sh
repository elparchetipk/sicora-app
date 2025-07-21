#!/bin/bash

# Script de prueba para SICORA API Gateway
# Verifica todos los endpoints y servicios integrados

set -e

API_GATEWAY_URL="${API_GATEWAY_URL:-http://localhost:8000}"
TIMEOUT="${TIMEOUT:-10}"

echo "🧪 Iniciando pruebas del SICORA API Gateway"
echo "🌐 URL: $API_GATEWAY_URL"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para realizar peticiones
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local expected_status=${4:-200}
    local auth_token=${5:-""}
    
    echo -n "  ${BLUE}[$method]${NC} $endpoint - $description... "
    
    local curl_cmd="curl -s -o /dev/null -w '%{http_code}' --max-time $TIMEOUT"
    
    if [ "$method" = "POST" ]; then
        curl_cmd="$curl_cmd -X POST -H 'Content-Type: application/json' -d '{}'"
    fi
    
    if [ -n "$auth_token" ]; then
        curl_cmd="$curl_cmd -H 'Authorization: Bearer $auth_token'"
    fi
    
    local status_code=$(eval "$curl_cmd $API_GATEWAY_URL$endpoint")
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✅ OK ($status_code)${NC}"
        return 0
    else
        echo -e "${RED}❌ FAIL ($status_code, esperado $expected_status)${NC}"
        return 1
    fi
}

# Función para verificar salud de servicios
check_health() {
    echo "🏥 Verificando salud del sistema..."
    
    local health_response=$(curl -s --max-time $TIMEOUT "$API_GATEWAY_URL/health" || echo '{"error": "timeout"}')
    
    if echo "$health_response" | grep -q '"status".*"healthy"'; then
        echo -e "  ${GREEN}✅ API Gateway está saludable${NC}"
        
        # Mostrar estado de servicios
        echo "  📊 Estado de servicios:"
        echo "$health_response" | python3 -m json.tool 2>/dev/null | grep -E '"(name|status)"' | \
        while read line; do
            if echo "$line" | grep -q '"name"'; then
                service_name=$(echo "$line" | sed 's/.*"name": *"\([^"]*\)".*/\1/')
                echo -n "    - $service_name: "
            elif echo "$line" | grep -q '"status"'; then
                status=$(echo "$line" | sed 's/.*"status": *"\([^"]*\)".*/\1/')
                if [ "$status" = "healthy" ]; then
                    echo -e "${GREEN}$status${NC}"
                elif [ "$status" = "unreachable" ]; then
                    echo -e "${YELLOW}$status${NC}"
                else
                    echo -e "${RED}$status${NC}"
                fi
            fi
        done
    else
        echo -e "  ${RED}❌ API Gateway no está saludable${NC}"
        echo "  Respuesta: $health_response"
    fi
    echo ""
}

# Función principal de pruebas
run_tests() {
    local failed_tests=0
    local total_tests=0
    
    echo "🔍 Probando endpoints públicos..."
    
    # Endpoints públicos
    test_endpoint "GET" "/" "Endpoint raíz" 200 || ((failed_tests++))
    ((total_tests++))
    
    test_endpoint "GET" "/health" "Health check" 200 || ((failed_tests++))
    ((total_tests++))
    
    echo ""
    echo "🔐 Probando endpoints de autenticación..."
    
    # Endpoints de autenticación (deberían retornar 422 sin datos)
    test_endpoint "POST" "/api/v1/users/auth/login" "Login (sin datos)" 422 || ((failed_tests++))
    ((total_tests++))
    
    test_endpoint "POST" "/api/v1/users/auth/register" "Registro (sin datos)" 422 || ((failed_tests++))
    ((total_tests++))
    
    echo ""
    echo "🔒 Probando endpoints protegidos (sin token)..."
    
    # Endpoints protegidos (deberían retornar 401 sin token)
    test_endpoint "GET" "/api/v1/users/users" "Listar usuarios" 401 || ((failed_tests++))
    ((total_tests++))
    
    test_endpoint "GET" "/api/v1/attendance/register" "Asistencia" 401 || ((failed_tests++))
    ((total_tests++))
    
    test_endpoint "GET" "/api/v1/ai/chat/sessions" "Sesiones de chat AI" 401 || ((failed_tests++))
    ((total_tests++))
    
    test_endpoint "GET" "/api/v1/kb/documents" "Documentos KB" 401 || ((failed_tests++))
    ((total_tests++))
    
    echo ""
    echo "🐹 Probando endpoints de servicios Go..."
    
    # Servicios Go (deberían retornar 401 sin token)
    test_endpoint "GET" "/api/v1/go/users" "Usuarios Go" 401 || ((failed_tests++))
    ((total_tests++))
    
    test_endpoint "GET" "/api/v1/go/attendance" "Asistencia Go" 401 || ((failed_tests++))
    ((total_tests++))
    
    test_endpoint "GET" "/api/v1/go/software-factory/projects" "Proyectos SF Go" 401 || ((failed_tests++))
    ((total_tests++))
    
    echo ""
    echo "📊 Resumen de pruebas:"
    echo "  Total de pruebas: $total_tests"
    echo "  Pruebas exitosas: $((total_tests - failed_tests))"
    echo "  Pruebas fallidas: $failed_tests"
    
    if [ $failed_tests -eq 0 ]; then
        echo -e "  ${GREEN}🎉 ¡Todas las pruebas pasaron!${NC}"
        return 0
    else
        echo -e "  ${RED}❌ $failed_tests pruebas fallaron${NC}"
        return 1
    fi
}

# Función para probar documentación
test_docs() {
    echo "📚 Verificando documentación..."
    
    test_endpoint "GET" "/docs" "Swagger UI" 200 || return 1
    test_endpoint "GET" "/redoc" "ReDoc" 200 || return 1
    test_endpoint "GET" "/openapi.json" "OpenAPI Schema" 200 || return 1
    
    echo -e "  ${GREEN}✅ Documentación disponible${NC}"
    echo "  - Swagger UI: $API_GATEWAY_URL/docs"
    echo "  - ReDoc: $API_GATEWAY_URL/redoc"
    echo ""
}

# Función para mostrar información del sistema
show_system_info() {
    echo "ℹ️  Información del sistema:"
    echo "  - API Gateway URL: $API_GATEWAY_URL"
    echo "  - Timeout: ${TIMEOUT}s"
    echo "  - Fecha: $(date)"
    echo ""
}

# Ejecutar todas las pruebas
main() {
    echo "🔧 SICORA API Gateway - Suite de Pruebas"
    echo "========================================"
    echo ""
    
    show_system_info
    check_health
    test_docs
    run_tests
    
    echo ""
    echo "🏁 Pruebas completadas"
}

# Verificar si curl está disponible
if ! command -v curl &> /dev/null; then
    echo "❌ Error: curl no está instalado"
    exit 1
fi

# Verificar si el API Gateway está accesible
if ! curl -s --max-time 5 "$API_GATEWAY_URL" > /dev/null; then
    echo "❌ Error: No se puede conectar al API Gateway en $API_GATEWAY_URL"
    echo "   Asegúrate de que el gateway esté ejecutándose"
    exit 1
fi

# Ejecutar pruebas
main
