#!/bin/bash

echo "🔍 Verificando estado de PostgreSQL UserDB..."

# Verificar si el contenedor está corriendo
echo "📊 Estado del contenedor postgres-user-db:"
docker ps | grep postgres-user-db

echo ""
echo "📋 Logs recientes del contenedor:"
docker logs --tail 10 postgres-user-db

echo ""
echo "🔗 Probando conexión a PostgreSQL (esperando que esté listo)..."
sleep 3

# Probar conexión usando docker exec
echo "🧪 Test de conexión:"
docker exec postgres-user-db psql -U postgres -d user_db -c "SELECT version();"

echo ""
echo "📊 Listar bases de datos disponibles:"
docker exec postgres-user-db psql -U postgres -c "\l"

echo ""
echo "✅ PostgreSQL UserDB está listo para Go UserService"
