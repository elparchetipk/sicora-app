#!/bin/bash
set -e

echo "🚀 Inicializando ProjectEval Service..."

# Verificar si estamos en el directorio correcto
if [ ! -f "alembic.ini" ]; then
    echo "❌ Error: No se encontró alembic.ini. Ejecutar desde el directorio del servicio."
    exit 1
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "🐍 Activando entorno virtual..."
    source venv/bin/activate
fi

# Verificar PostgreSQL
echo "📦 Verificando PostgreSQL..."
if ! docker compose -f ../../docker-compose.yml ps postgres | grep -q "Up"; then
    echo "📦 Iniciando PostgreSQL..."
    cd ../.. && docker compose up -d postgres && cd - > /dev/null
    echo "⏱️ Esperando a que PostgreSQL esté listo..."
    sleep 8
fi

# Verificar conexión a base de datos
echo "🔗 Verificando conexión a base de datos..."
if ! docker exec sicora_postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "❌ Error: No se puede conectar a PostgreSQL"
    exit 1
fi

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
alembic upgrade head

# Verificar estado
echo "✅ Verificando estado de migraciones..."
CURRENT_VERSION=$(alembic current 2>/dev/null || echo "No version")
if [ "$CURRENT_VERSION" != "No version" ] && [ -n "$CURRENT_VERSION" ]; then
    echo "✅ Migración actual: $CURRENT_VERSION"
else
    echo "⚠️ No se pudo obtener la versión actual de migración"
fi

# Verificar tablas creadas
echo "📋 Verificando tablas creadas..."
TABLE_COUNT=$(docker exec sicora_postgres psql -U postgres -d sicora_dev -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'projectevalservice_schema' AND table_type = 'BASE TABLE' AND table_name != 'alembic_version_projectevalservice';" 2>/dev/null | tr -d ' ')

if [ "$TABLE_COUNT" -eq 3 ]; then
    echo "✅ Todas las tablas principales creadas correctamente (projects, stakeholders, evaluations)"
else
    echo "⚠️ Se encontraron $TABLE_COUNT tablas (se esperaban 3)"
fi

echo ""
echo "🎉 ProjectEval Service inicializado correctamente!"
echo "📡 Para iniciar el servicio: ./dev.sh"
echo "📊 Para monitoreo: ./monitor.sh"
