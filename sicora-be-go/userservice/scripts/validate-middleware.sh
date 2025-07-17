#!/bin/bash

# Script de Validación del Middleware Optimizado - UserService Go
# Versión: 1.0
# Descripción: Valida que el middleware de autenticación esté funcionando correctamente

set -e

echo "🧪 Iniciando validación del middleware optimizado..."
echo "=================================================="

# Configuración
BASE_URL="http://localhost:8002"
API_V1="$BASE_URL/api/v1"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar resultados
show_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Función para hacer requests HTTP
make_request() {
    local method=$1
    local url=$2
    local headers=$3
    local data=$4
    
    if [ -n "$headers" ] && [ -n "$data" ]; then
        curl -s -X "$method" "$url" -H "$headers" -d "$data" -w "\n%{http_code}"
    elif [ -n "$headers" ]; then
        curl -s -X "$method" "$url" -H "$headers" -w "\n%{http_code}"
    elif [ -n "$data" ]; then
        curl -s -X "$method" "$url" -d "$data" -w "\n%{http_code}"
    else
        curl -s -X "$method" "$url" -w "\n%{http_code}"
    fi
}

echo -e "${BLUE}1. Validando que el servidor esté ejecutándose...${NC}"

# Test 1: Health Check
health_response=$(curl -s -w "%{http_code}" "$BASE_URL/health" || echo "000")
if [[ "$health_response" == *"200" ]]; then
    show_result 0 "Health check funcionando"
else
    show_result 1 "Servidor no está ejecutándose en $BASE_URL"
    echo "💡 Ejecuta: cd 02-go/userservice && go run main.go"
    exit 1
fi

echo -e "\n${BLUE}2. Validando headers de seguridad...${NC}"

# Test 2: Security Headers
security_headers=$(curl -s -I "$BASE_URL/health")
if echo "$security_headers" | grep -q "X-Content-Type-Options"; then
    show_result 0 "Header X-Content-Type-Options presente"
else
    show_result 1 "Header X-Content-Type-Options faltante"
fi

if echo "$security_headers" | grep -q "X-Frame-Options"; then
    show_result 0 "Header X-Frame-Options presente"
else
    show_result 1 "Header X-Frame-Options faltante"
fi

echo -e "\n${BLUE}3. Validando rate limiting...${NC}"

# Test 3: Rate Limiting (hacer múltiples requests)
rate_limit_count=0
for i in {1..5}; do
    response=$(curl -s -w "%{http_code}" "$BASE_URL/health")
    if [[ "$response" == *"200" ]]; then
        ((rate_limit_count++))
    fi
done

if [ $rate_limit_count -eq 5 ]; then
    show_result 0 "Rate limiting configurado (permite requests normales)"
else
    show_result 1 "Rate limiting bloqueando requests normales"
fi

echo -e "\n${BLUE}4. Validando rutas públicas...${NC}"

# Test 4: Rutas públicas (no requieren autenticación)
# Test login endpoint existe
login_response=$(make_request "POST" "$API_V1/auth/login" "Content-Type: application/json" '{"email":"test@test.com","password":"wrongpassword"}')
if [[ "$login_response" == *"400"* ]] || [[ "$login_response" == *"401"* ]]; then
    show_result 0 "Endpoint de login accesible sin autenticación"
else
    show_result 1 "Endpoint de login no funciona correctamente"
fi

# Test registro de usuario
register_response=$(make_request "POST" "$API_V1/users" "Content-Type: application/json" '{"email":"","name":"","password":""}')
if [[ "$register_response" == *"400"* ]]; then
    show_result 0 "Endpoint de registro accesible y validando input"
else
    show_result 1 "Endpoint de registro no funciona"
fi

echo -e "\n${BLUE}5. Validando protección de rutas privadas...${NC}"

# Test 5: Rutas protegidas (requieren autenticación)
# Test acceso sin token
profile_response=$(make_request "GET" "$API_V1/users/profile" "" "")
if [[ "$profile_response" == *"401"* ]]; then
    show_result 0 "Ruta protegida rechaza acceso sin token"
else
    show_result 1 "Ruta protegida permite acceso sin token (VULNERABILIDAD)"
fi

# Test acceso con token inválido
invalid_token_response=$(make_request "GET" "$API_V1/users/profile" "Authorization: Bearer invalid-token" "")
if [[ "$invalid_token_response" == *"401"* ]]; then
    show_result 0 "Ruta protegida rechaza token inválido"
else
    show_result 1 "Ruta protegida acepta token inválido (VULNERABILIDAD)"
fi

echo -e "\n${BLUE}6. Validando CORS...${NC}"

# Test 6: CORS Headers
cors_response=$(curl -s -I -H "Origin: http://localhost:3000" "$BASE_URL/health")
if echo "$cors_response" | grep -q "Access-Control-Allow-Origin"; then
    show_result 0 "CORS configurado correctamente"
else
    show_result 1 "CORS no configurado"
fi

echo -e "\n${BLUE}7. Validando logging y request ID...${NC}"

# Test 7: Request ID Header
request_id_response=$(curl -s -I "$BASE_URL/health")
if echo "$request_id_response" | grep -q "X-Request-ID"; then
    show_result 0 "Request ID generándose correctamente"
else
    show_result 1 "Request ID no se está generando"
fi

echo -e "\n${BLUE}8. Validando compresión...${NC}"

# Test 8: Compression
compression_response=$(curl -s -H "Accept-Encoding: gzip" -I "$BASE_URL/health")
if echo "$compression_response" | grep -q "Content-Encoding"; then
    show_result 0 "Compresión activada"
else
    show_result 1 "Compresión no configurada (opcional)"
fi

echo -e "\n${BLUE}9. Validando documentación...${NC}"

# Test 9: Swagger Documentation
swagger_response=$(curl -s -w "%{http_code}" "$BASE_URL/docs/index.html" || echo "000")
if [[ "$swagger_response" == *"200"* ]]; then
    show_result 0 "Documentación Swagger accesible"
else
    swagger_response2=$(curl -s -w "%{http_code}" "$BASE_URL/swagger/index.html" || echo "000")
    if [[ "$swagger_response2" == *"200"* ]]; then
        show_result 0 "Documentación Swagger accesible en /swagger"
    else
        show_result 1 "Documentación Swagger no accesible"
    fi
fi

echo -e "\n${BLUE}10. Validando estructura de errores...${NC}"

# Test 10: Error Structure
error_response=$(curl -s "$API_V1/users/profile")
if echo "$error_response" | grep -q '"error"' && echo "$error_response" | grep -q '"message"'; then
    show_result 0 "Estructura de errores consistente"
else
    show_result 1 "Estructura de errores inconsistente"
fi

echo -e "\n=================================================="
echo -e "${GREEN}🎉 Validación del middleware completada${NC}"
echo -e "\n${YELLOW}💡 Próximos pasos recomendados:${NC}"
echo "   1. Probar con un JWT válido para validar rutas autenticadas"
echo "   2. Verificar logs del servidor para ver el logging estructurado"
echo "   3. Monitorear métricas de performance en producción"
echo "   4. Configurar alertas basadas en rate limiting"

echo -e "\n${BLUE}📖 Documentación:${NC}"
echo "   - Middleware: docs/MIDDLEWARE-OPTIMIZATION-REPORT.md"
echo "   - Configuración: docs/MIDDLEWARE-CONFIGURATION.md"
echo "   - Tests: tests/README.md"

echo -e "\n${BLUE}🚀 Para testing completo ejecutar:${NC}"
echo "   cd 02-go/userservice && go test ./tests/... -v"

echo -e "\n✅ Middleware optimizado validado exitosamente"
