#!/bin/bash

# Script para verificar la integración Frontend-Backend SICORA
# Verifica que el UserService de Go esté funcionando correctamente

echo "🔍 Verificando integración Frontend-Backend SICORA..."
echo "============================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de configuración
BACKEND_URL="http://localhost:8002"
HEALTH_ENDPOINT="/api/v1/users"
TIMEOUT=5

echo -e "${BLUE}Backend URL:${NC} $BACKEND_URL"
echo -e "${BLUE}Timeout:${NC} ${TIMEOUT}s"
echo ""

# Función para verificar si un puerto está abierto
check_port() {
    local port=$1
    if command -v nc >/dev/null 2>&1; then
        nc -z localhost $port >/dev/null 2>&1
        return $?
    elif command -v timeout >/dev/null 2>&1; then
        timeout 1 bash -c "</dev/tcp/localhost/$port" >/dev/null 2>&1
        return $?
    else
        # Fallback usando curl
        curl -s --connect-timeout 1 "http://localhost:$port" >/dev/null 2>&1
        return $?
    fi
}

# 1. Verificar si el puerto 8002 está abierto
echo "1️⃣  Verificando puerto 8002..."
if check_port 8002; then
    echo -e "   ${GREEN}✅ Puerto 8002 está abierto${NC}"
else
    echo -e "   ${RED}❌ Puerto 8002 no está abierto${NC}"
    echo -e "   ${YELLOW}💡 Asegúrate de que el UserService de Go esté ejecutándose${NC}"
    echo -e "   ${YELLOW}   Comando: cd sicora-be-go/userservice && ./dev.sh${NC}"
    exit 1
fi

# 2. Verificar conectividad HTTP básica
echo ""
echo "2️⃣  Verificando conectividad HTTP..."
if curl -s --connect-timeout $TIMEOUT "$BACKEND_URL" >/dev/null 2>&1; then
    echo -e "   ${GREEN}✅ Conectividad HTTP establecida${NC}"
else
    echo -e "   ${RED}❌ No se puede conectar al backend${NC}"
    echo -e "   ${YELLOW}💡 Verifica que el servidor esté respondiendo en $BACKEND_URL${NC}"
    exit 1
fi

# 3. Verificar endpoint de usuarios (sin autenticación)
echo ""
echo "3️⃣  Verificando endpoint de usuarios..."
RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" --connect-timeout $TIMEOUT "$BACKEND_URL$HEALTH_ENDPOINT")
HTTP_STATUS=$(echo $RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
RESPONSE_BODY=$(echo $RESPONSE | sed -e 's/HTTPSTATUS\:.*//g')

if [ "$HTTP_STATUS" -eq 401 ] || [ "$HTTP_STATUS" -eq 403 ]; then
    echo -e "   ${GREEN}✅ Endpoint responde correctamente (requiere autenticación)${NC}"
    echo -e "   ${BLUE}   Status: $HTTP_STATUS (esperado para endpoint protegido)${NC}"
elif [ "$HTTP_STATUS" -eq 200 ]; then
    echo -e "   ${GREEN}✅ Endpoint responde correctamente${NC}"
    echo -e "   ${BLUE}   Status: $HTTP_STATUS${NC}"
elif [ "$HTTP_STATUS" -ge 500 ]; then
    echo -e "   ${RED}❌ Error del servidor (Status: $HTTP_STATUS)${NC}"
    echo -e "   ${YELLOW}💡 Revisa los logs del backend Go${NC}"
    exit 1
else
    echo -e "   ${YELLOW}⚠️  Respuesta inesperada (Status: $HTTP_STATUS)${NC}"
    if [ ! -z "$RESPONSE_BODY" ]; then
        echo -e "   ${BLUE}   Respuesta: $RESPONSE_BODY${NC}"
    fi
fi

# 4. Verificar estructura de respuesta JSON (si es posible)
echo ""
echo "4️⃣  Verificando formato de respuesta..."
if echo "$RESPONSE_BODY" | jq . >/dev/null 2>&1; then
    echo -e "   ${GREEN}✅ Respuesta en formato JSON válido${NC}"
else
    if [ ! -z "$RESPONSE_BODY" ]; then
        echo -e "   ${YELLOW}⚠️  Respuesta no es JSON válido o está vacía${NC}"
        echo -e "   ${BLUE}   Contenido: $RESPONSE_BODY${NC}"
    else
        echo -e "   ${BLUE}ℹ️  Sin contenido en respuesta (normal para endpoints protegidos)${NC}"
    fi
fi

# 5. Verificar CORS headers (importante para desarrollo)
echo ""
echo "5️⃣  Verificando headers CORS..."
CORS_HEADERS=$(curl -s -I --connect-timeout $TIMEOUT "$BACKEND_URL$HEALTH_ENDPOINT" | grep -i "access-control")
if [ ! -z "$CORS_HEADERS" ]; then
    echo -e "   ${GREEN}✅ Headers CORS encontrados${NC}"
    echo "$CORS_HEADERS" | while read line; do
        echo -e "   ${BLUE}   $line${NC}"
    done
else
    echo -e "   ${YELLOW}⚠️  No se encontraron headers CORS${NC}"
    echo -e "   ${YELLOW}💡 Puede causar problemas en desarrollo frontend${NC}"
fi

# 6. Verificar otros endpoints importantes
echo ""
echo "6️⃣  Verificando endpoints de autenticación..."

# Login endpoint
LOGIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout $TIMEOUT "$BACKEND_URL/api/v1/auth/login")
if [ "$LOGIN_STATUS" -eq 405 ] || [ "$LOGIN_STATUS" -eq 400 ] || [ "$LOGIN_STATUS" -eq 422 ]; then
    echo -e "   ${GREEN}✅ Endpoint de login disponible${NC}"
    echo -e "   ${BLUE}   /api/v1/auth/login - Status: $LOGIN_STATUS${NC}"
else
    echo -e "   ${YELLOW}⚠️  Endpoint de login: Status $LOGIN_STATUS${NC}"
fi

# Register endpoint
REGISTER_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout $TIMEOUT "$BACKEND_URL/api/v1/users")
if [ "$REGISTER_STATUS" -eq 405 ] || [ "$REGISTER_STATUS" -eq 400 ] || [ "$REGISTER_STATUS" -eq 422 ]; then
    echo -e "   ${GREEN}✅ Endpoint de registro disponible${NC}"
    echo -e "   ${BLUE}   /api/v1/users - Status: $REGISTER_STATUS${NC}"
else
    echo -e "   ${YELLOW}⚠️  Endpoint de registro: Status $REGISTER_STATUS${NC}"
fi

echo ""
echo "============================================="
echo -e "${GREEN}🎉 Verificación completada${NC}"
echo ""
echo -e "${BLUE}Próximos pasos:${NC}"
echo "1. Iniciar el frontend: cd sicora-app-fe && npm run dev"
echo "2. Usar el panel de pruebas de integración en la app"
echo "3. Revisar logs del backend si hay problemas"
echo ""
echo -e "${YELLOW}📋 Notas importantes:${NC}"
echo "• El backend debe estar ejecutándose en puerto 8002"
echo "• Los endpoints protegidos requieren autenticación JWT"
echo "• Revisa la documentación en INTEGRACION_FRONTEND_BACKEND_COMPLETADA.md"
