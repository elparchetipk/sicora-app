#!/bin/bash

# Script de inicialización para SoftwareFactoryService migrations
# Crea la migración inicial basada en las entidades Go definidas

set -e

echo "🚀 Inicializando migraciones para SoftwareFactoryService..."

# Verificar que estamos en el directorio correcto
if [ ! -f "alembic.ini" ]; then
    echo "❌ Error: No se encontró alembic.ini. Ejecuta este script desde el directorio sicora-be-python/softwarefactoryservice/"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual e instalar dependencias
echo "📦 Instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Verificar conexión a la base de datos
echo "🔌 Verificando conexión a la base de datos..."
python3 -c "
import psycopg2
import os

try:
    conn = psycopg2.connect(
        'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db'
    )
    print('✅ Conexión a la base de datos exitosa')
    conn.close()
except Exception as e:
    print(f'❌ Error de conexión: {e}')
    print('⚠️ Asegúrate de que PostgreSQL esté ejecutándose y que el esquema esté inicializado')
    print('   Ejecuta: sicora-be-python/database/init/01_init_db_users_schemas.sql')
    exit(1)
"

# Crear migración inicial
echo "📝 Creando migración inicial..."
venv/bin/alembic revision --autogenerate -m "Initial migration for SoftwareFactoryService schema"

echo "✅ Inicialización completada!"
echo ""
echo "🎯 Próximos pasos:"
echo "   1. Revisar la migración generada en alembic/versions/"
echo "   2. Ejecutar: make migrate"
echo "   3. Verificar las tablas creadas en el esquema softwarefactoryservice_schema"
echo ""
echo "📋 Comandos útiles:"
echo "   make migrate          # Ejecutar migraciones"
echo "   make migrate-history  # Ver historial"
echo "   make migrate-current  # Ver estado actual"
