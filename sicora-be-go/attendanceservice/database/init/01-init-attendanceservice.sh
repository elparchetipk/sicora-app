#!/bin/bash
set -e

echo "Initializing AttendanceService database..."

# Crear schema para AttendanceService
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Crear schema para AttendanceService
    CREATE SCHEMA IF NOT EXISTS attendanceservice;
    
    -- Otorgar permisos al usuario
    GRANT ALL PRIVILEGES ON SCHEMA attendanceservice TO attendanceservice_user;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA attendanceservice TO attendanceservice_user;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA attendanceservice TO attendanceservice_user;
    
    -- Establecer permisos por defecto para nuevas tablas
    ALTER DEFAULT PRIVILEGES IN SCHEMA attendanceservice 
    GRANT ALL PRIVILEGES ON TABLES TO attendanceservice_user;
    
    ALTER DEFAULT PRIVILEGES IN SCHEMA attendanceservice 
    GRANT ALL PRIVILEGES ON SEQUENCES TO attendanceservice_user;
    
    -- Establecer schema por defecto
    ALTER USER attendanceservice_user SET search_path = attendanceservice, public;
    
    echo "AttendanceService schema created successfully!"
EOSQL

echo "Database initialization completed!"
