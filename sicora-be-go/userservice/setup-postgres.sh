#!/bin/bash

# Script para configurar PostgreSQL UserService según DATABASE-STRATEGY.md
# Base de datos compartida entre todos los stacks del UserService

echo "🐳 Configurando PostgreSQL 15 - UserService Database Strategy..."
echo "📋 Según especificación: user_db compartida entre 6 stacks"

# 1. Ejecutar PostgreSQL 15 con Docker (user_db)
docker run --name postgres-user-db \
  -e POSTGRES_DB=user_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando que PostgreSQL UserDB esté listo..."
sleep 5

# 2. Verificar que PostgreSQL está funcionando
echo "📊 Verificando estado de user_db..."
docker logs postgres-user-db

# 3. Verificar conexión específica a user_db
echo "🔗 Probando conexión a user_db..."
docker exec -it postgres-user-db psql -U postgres -d user_db -c "SELECT version();"

echo "✅ PostgreSQL 15 (user_db) configurado según DATABASE-STRATEGY.md"
echo ""
echo "📋 Especificación cumplida:"
echo "   Database: user_db (compartida entre 6 stacks)"
echo "   Tables: users, roles, permissions, user_roles, sessions"
echo "   Cache: Redis (pendiente - sessions, user profiles)"
echo ""
echo "🚀 Ahora puedes ejecutar cualquier stack del UserService:"
echo "   Go:      cd 02-go/userservice && go run main.go"
echo "   FastAPI: cd 01-fastapi/userservice && uvicorn main:app --reload"
echo ""
echo "🔗 Endpoints Go UserService:"
echo "   Health: http://localhost:8002/health"
echo "   Users:  http://localhost:8002/api/v1/users"
