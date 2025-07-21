#!/bin/bash

# Script de inicio para SICORA API Gateway
# Configuración de variables de entorno y inicio del servidor

set -e

echo "🚀 Iniciando SICORA API Gateway..."

# Verificar variables de entorno críticas
if [ -z "$JWT_SECRET_KEY" ]; then
    echo "⚠️  JWT_SECRET_KEY no configurado, usando valor por defecto"
    export JWT_SECRET_KEY="sicora-gateway-secret-key-2024"
fi

# Configuración por defecto
export GATEWAY_HOST="${GATEWAY_HOST:-0.0.0.0}"
export GATEWAY_PORT="${GATEWAY_PORT:-8000}"
export DEBUG="${DEBUG:-false}"

# Servicios habilitados
export PYTHON_SERVICES_ENABLED="${PYTHON_SERVICES_ENABLED:-true}"
export GO_SERVICES_ENABLED="${GO_SERVICES_ENABLED:-true}"

# Timeouts
export SERVICE_TIMEOUT="${SERVICE_TIMEOUT:-30}"
export HEALTH_CHECK_TIMEOUT="${HEALTH_CHECK_TIMEOUT:-5}"

echo "📋 Configuración del Gateway:"
echo "   - Host: $GATEWAY_HOST"
echo "   - Puerto: $GATEWAY_PORT"
echo "   - Debug: $DEBUG"
echo "   - Servicios Python: $PYTHON_SERVICES_ENABLED"
echo "   - Servicios Go: $GO_SERVICES_ENABLED"

# Instalar dependencias si no existen
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

echo "📦 Activando entorno virtual..."
source venv/bin/activate

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Verificar conectividad con servicios críticos
echo "🔍 Verificando servicios críticos..."

check_service() {
    local service_name=$1
    local service_url=$2
    echo -n "   Verificando $service_name... "
    if curl -s --max-time 3 "$service_url/health" > /dev/null 2>&1; then
        echo "✅ OK"
        return 0
    else
        echo "❌ No disponible"
        return 1
    fi
}

# Verificar algunos servicios críticos
if [ "$PYTHON_SERVICES_ENABLED" = "true" ]; then
    check_service "UserService" "${USER_SERVICE_URL:-http://userservice:8001}" || true
    check_service "AIService" "${AI_SERVICE_URL:-http://aiservice:8007}" || true
    check_service "KBService" "${KB_SERVICE_URL:-http://kbservice:8006}" || true
fi

if [ "$GO_SERVICES_ENABLED" = "true" ]; then
    check_service "UserService-Go" "${USER_GO_SERVICE_URL:-http://userservice-go:8101}" || true
fi

echo "🚀 Iniciando servidor API Gateway..."

# Iniciar el servidor
if [ "$DEBUG" = "true" ]; then
    uvicorn main:app --host "$GATEWAY_HOST" --port "$GATEWAY_PORT" --reload --log-level debug
else
    uvicorn main:app --host "$GATEWAY_HOST" --port "$GATEWAY_PORT" --workers 4
fi
