#!/bin/bash

# Script para verificar las bases de datos y su contenido
# Configuración de conexión
export PGPASSWORD=sicora_password
HOST="localhost"
PORT="5432"
USER="sicora_user"

echo "=== VERIFICACIÓN DE BASES DE DATOS VPS ==="
echo "Fecha: $(date)"
echo ""

# Función para ejecutar consulta
query_db() {
    local db=$1
    local query=$2
    echo "--- Base de datos: $db ---"
    psql -h $HOST -p $PORT -U $USER -d $db -c "$query" 2>/dev/null || echo "Error accediendo a $db"
    echo ""
}

# Verificar bases de datos disponibles
echo "=== BASES DE DATOS DISPONIBLES ==="
psql -h $HOST -p $PORT -U $USER -d postgres -c "\l"
echo ""

# Verificar esquemas en cada base de datos
echo "=== ESQUEMAS EN ONEVISION_TESTING ==="
query_db "onevision_testing" "\dn"

echo "=== ESQUEMAS EN SICORA_DEV ==="
query_db "sicora_dev" "\dn"

# Verificar datos en esquemas específicos
echo "=== VERIFICACIÓN DE DATOS EN ESQUEMAS ==="

# EvalinService
echo "--- EvalinService en onevision_testing ---"
query_db "onevision_testing" "SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'evalinservice_schema';"

echo "--- EvalinService en sicora_dev ---"
query_db "sicora_dev" "SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'evalinservice_schema';"

# UserService (para referencia)
echo "--- UserService en onevision_testing ---"
query_db "onevision_testing" "SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'userservice_schema';"

echo "--- UserService en sicora_dev ---"
query_db "sicora_dev" "SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'userservice_schema';"

echo "=== RESUMEN ==="
echo "Bases de datos encontradas:"
echo "- onevision_testing"
echo "- sicora_dev"
echo "- postgres (default)"
echo ""
echo "Configuración actual en .env:"
echo "POSTGRES_DB=sicora_dev"
echo ""
echo "¿Cuál es la base de datos canónica para el VPS?"
