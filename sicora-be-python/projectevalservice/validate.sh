#!/bin/bash
# Script de validación de conectividad con otros stacks

echo "🔗 Validación de Conectividad - SICORA Stacks"
echo "=============================================="
echo ""

# URLs de servicios
USERSERVICE_URL="http://localhost:8001"
SCHEDULESERVICE_URL="http://localhost:8002"
PROJECTEVAL_URL="http://localhost:8007"
POSTGRES_CONTAINER="sicora_postgres"

# Función para verificar servicio HTTP
check_http_service() {
    local name=$1
    local url=$2
    local endpoint=$3
    
    echo -n "📡 Verificando $name ($url$endpoint)... "
    
    if curl -s --connect-timeout 5 "$url$endpoint" > /dev/null 2>&1; then
        echo "✅ OK"
        return 0
    else
        echo "❌ No disponible"
        return 1
    fi
}

# Función para verificar base de datos
check_database() {
    local schema=$1
    
    echo -n "🗄️ Verificando esquema $schema... "
    
    local table_count=$(docker exec $POSTGRES_CONTAINER psql -U postgres -d sicora_dev -t -c "
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = '$schema' AND table_type = 'BASE TABLE'
        AND table_name != 'alembic_version_$schema'
    " 2>/dev/null | tr -d ' ')
    
    if [ "$table_count" -gt 0 ]; then
        echo "✅ OK ($table_count tablas)"
        return 0
    else
        echo "❌ Sin tablas o no accesible"
        return 1
    fi
}

# Verificar PostgreSQL
echo "🔍 Verificando infraestructura:"
echo "-------------------------------"
echo -n "🐘 PostgreSQL... "
if docker exec $POSTGRES_CONTAINER pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ OK"
    POSTGRES_OK=1
else
    echo "❌ No disponible"
    POSTGRES_OK=0
fi

# Verificar esquemas de base de datos
if [ $POSTGRES_OK -eq 1 ]; then
    echo ""
    echo "🗄️ Verificando esquemas de base de datos:"
    echo "-----------------------------------------"
    check_database "userservice_schema"
    check_database "scheduleservice_schema"
    check_database "attendanceservice_schema"
    check_database "evalinservice_schema"
    check_database "projectevalservice_schema"
fi

echo ""
echo "🚀 Verificando servicios HTTP:"
echo "------------------------------"

# Verificar UserService
check_http_service "UserService" $USERSERVICE_URL "/api/v1/health"
if [ $? -eq 1 ]; then
    check_http_service "UserService (fallback)" $USERSERVICE_URL "/"
fi

# Verificar ScheduleService
check_http_service "ScheduleService" $SCHEDULESERVICE_URL "/api/v1/health"
if [ $? -eq 1 ]; then
    check_http_service "ScheduleService (fallback)" $SCHEDULESERVICE_URL "/"
fi

# Verificar ProjectEvalService
check_http_service "ProjectEvalService" $PROJECTEVAL_URL "/api/v1/health"
if [ $? -eq 1 ]; then
    check_http_service "ProjectEvalService (docs)" $PROJECTEVAL_URL "/docs"
fi

echo ""
echo "🔗 Pruebas de integración:"
echo "-------------------------"

# Test de conectividad interna entre servicios
echo -n "🔄 UserService → ScheduleService... "
if curl -s --connect-timeout 3 "$USERSERVICE_URL/api/v1/external/schedule-health" > /dev/null 2>&1; then
    echo "✅ OK"
else
    echo "⚠️ No configurado o no disponible"
fi

echo -n "🔄 ProjectEval → UserService... "
if curl -s --connect-timeout 3 "$PROJECTEVAL_URL/api/v1/external/user-health" > /dev/null 2>&1; then
    echo "✅ OK"
else
    echo "⚠️ No configurado o no disponible"
fi

echo ""
echo "📊 Resumen de conectividad:"
echo "--------------------------"

# Contar servicios disponibles
AVAILABLE_SERVICES=0
TOTAL_SERVICES=3

for url in $USERSERVICE_URL $SCHEDULESERVICE_URL $PROJECTEVAL_URL; do
    if curl -s --connect-timeout 2 "$url" > /dev/null 2>&1; then
        AVAILABLE_SERVICES=$((AVAILABLE_SERVICES + 1))
    fi
done

echo "🟢 Servicios disponibles: $AVAILABLE_SERVICES/$TOTAL_SERVICES"

if [ $POSTGRES_OK -eq 1 ]; then
    echo "🟢 Base de datos: Operativa"
else
    echo "🔴 Base de datos: No disponible"
fi

# Recomendaciones
echo ""
echo "💡 Recomendaciones:"
echo "------------------"

if [ $POSTGRES_OK -eq 0 ]; then
    echo "❗ Iniciar PostgreSQL: docker compose up -d postgres"
fi

if [ $AVAILABLE_SERVICES -lt $TOTAL_SERVICES ]; then
    echo "❗ Servicios faltantes. Verificar:"
    echo "  - UserService: cd sicora-be-python/userservice && ./dev.sh"
    echo "  - ScheduleService: cd sicora-be-python/scheduleservice && ./dev.sh"
    echo "  - ProjectEvalService: cd sicora-be-python/projectevalservice && ./dev.sh"
fi

echo ""
echo "✅ Validación completada - $(date)"
