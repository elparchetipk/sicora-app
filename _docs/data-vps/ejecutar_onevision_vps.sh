#!/bin/bash

# 🚀 Script de Ejecución Automática - Base de Datos OneVision VPS
# Ejecuta todas las fases paso a paso con verificaciones

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de configuración
DB_NAME="onevision_testing"
DB_USER="sicora_user"
CONTAINER_NAME="sicora-postgres"

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[ÉXITO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[ADVERTENCIA]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para ejecutar SQL y mostrar resultado
execute_sql() {
    local phase=$1
    local description=$2
    local sql_file=$3

    log "🔄 Ejecutando $phase: $description"

    if [[ -f "$sql_file" ]]; then
        docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME < "$sql_file"
    else
        error "Archivo SQL no encontrado: $sql_file"
        return 1
    fi

    success "✅ $phase completada"
}

# Función para verificar resultado
verify_phase() {
    local phase=$1
    local verification_sql=$2

    log "🔍 Verificando $phase..."

    result=$(docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -t -c "$verification_sql")
    echo "📊 Resultado: $result"

    read -p "¿Los resultados son correctos? (s/n): " confirm
    if [[ $confirm != "s" && $confirm != "S" ]]; then
        error "Verificación fallida para $phase"
        exit 1
    fi

    success "✅ $phase verificada correctamente"
}

# Función principal
main() {
    log "🚀 Iniciando creación de base de datos OneVision independiente"

    # Verificar conexión a contenedor
    log "🔗 Verificando conexión a PostgreSQL..."
    if ! docker exec $CONTAINER_NAME pg_isready -U $DB_USER; then
        error "No se puede conectar a PostgreSQL. Verificar que el contenedor esté corriendo."
        exit 1
    fi
    success "✅ Conexión establecida"

    # Crear base de datos y esquemas
    log "🏗️ Creando base de datos $DB_NAME y esquemas..."
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d sicora_dev << EOF
-- Crear base de datos independiente
DROP DATABASE IF EXISTS $DB_NAME;
CREATE DATABASE $DB_NAME;
EOF

    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << EOF
-- Crear esquemas necesarios
CREATE SCHEMA IF NOT EXISTS userservice_schema;
CREATE SCHEMA IF NOT EXISTS scheduleservice_schema;
CREATE SCHEMA IF NOT EXISTS attendanceservice_schema;
CREATE SCHEMA IF NOT EXISTS evalinservice_schema;
CREATE SCHEMA IF NOT EXISTS kbservice_schema;
CREATE SCHEMA IF NOT EXISTS aiservice_schema;
CREATE SCHEMA IF NOT EXISTS projectevalservice_schema;
EOF

    success "✅ Base de datos y esquemas creados"

    # FASE 1: Tabla users y coordinación
    log "📋 FASE 1: Tabla users (coordinación)"

    # Crear tabla users
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << 'EOF'
CREATE TABLE userservice_schema.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('ADMIN', 'INSTRUCTOR', 'APPRENTICE', 'COORDINATOR')),
    identification_number VARCHAR(20) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    birth_date DATE,
    status VARCHAR(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_role ON userservice_schema.users(role);
CREATE INDEX idx_users_email ON userservice_schema.users(email);
CREATE INDEX idx_users_identification ON userservice_schema.users(identification_number);
CREATE INDEX idx_users_status ON userservice_schema.users(status);
EOF

    # Insertar coordinación
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << 'EOF'
INSERT INTO userservice_schema.users (
    first_name, last_name, email, password_hash, role,
    identification_number, phone, address, birth_date, status, is_active
) VALUES (
    'María Elena',
    'Rodríguez Gómez',
    'coordinacion.teleinformatica@onevision.edu.co',
    '$2b$12$LQv3c1yqBwEHxPiLNPAl2.PjDthHZ7QRwm6EHNM3GyJNuQhGwkqG2',
    'COORDINATOR',
    '52147896',
    '+57 311 555 0001',
    'Carrera 30 #17-00, Bogotá',
    '1985-03-15',
    'ACTIVE',
    true
);
EOF

    verify_phase "FASE 1" "SELECT COUNT(*) as coordinadores FROM userservice_schema.users WHERE role = 'COORDINATOR';"

    # FASE 2: Tabla venues
    log "📋 FASE 2: Tabla venues (sedes)"

    # Crear tabla venues
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << 'EOF'
CREATE TABLE scheduleservice_schema.venues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    location VARCHAR(500) NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 30,
    venue_type VARCHAR(50) DEFAULT 'CLASSROOM',
    equipment TEXT,
    availability_status VARCHAR(20) DEFAULT 'AVAILABLE',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_venues_type ON scheduleservice_schema.venues(venue_type);
CREATE INDEX idx_venues_status ON scheduleservice_schema.venues(availability_status);
EOF

    # Insertar venues
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << 'EOF'
-- SEDE 1: CGMLTI Calle 52 (50 venues)
DO $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..50 LOOP
        INSERT INTO scheduleservice_schema.venues (
            name, location, capacity, venue_type, equipment, availability_status
        ) VALUES (
            'Aula ' || LPAD(i::text, 3, '0') || ' - Calle 52',
            'CGMLTI Calle 52 #13-65, Bogotá',
            CASE
                WHEN i <= 20 THEN 25
                WHEN i <= 40 THEN 30
                ELSE 35
            END,
            CASE
                WHEN i <= 30 THEN 'CLASSROOM'
                WHEN i <= 40 THEN 'COMPUTER_LAB'
                ELSE 'WORKSHOP'
            END,
            CASE
                WHEN i <= 20 THEN 'Proyector, Tablero, Aire Acondicionado'
                WHEN i <= 30 THEN 'Proyector, Tablero, Computador, Aire Acondicionado'
                WHEN i <= 40 THEN '30 Computadores, Proyector, Aire Acondicionado, Switch de Red'
                ELSE 'Herramientas Especializadas, Proyector, Tablero, Ventilación'
            END,
            'AVAILABLE'
        );
    END LOOP;
END $$;

-- SEDE 2: CGMLTI Fontibón (50 venues)
DO $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 51..100 LOOP
        INSERT INTO scheduleservice_schema.venues (
            name, location, capacity, venue_type, equipment, availability_status
        ) VALUES (
            'Aula ' || LPAD((i-50)::text, 3, '0') || ' - Fontibón',
            'CGMLTI Fontibón, Zona Franca, Bogotá',
            CASE
                WHEN i <= 70 THEN 25
                WHEN i <= 90 THEN 30
                ELSE 35
            END,
            CASE
                WHEN i <= 80 THEN 'CLASSROOM'
                WHEN i <= 95 THEN 'COMPUTER_LAB'
                ELSE 'WORKSHOP'
            END,
            CASE
                WHEN i <= 70 THEN 'Proyector, Tablero, Aire Acondicionado'
                WHEN i <= 80 THEN 'Proyector, Tablero, Computador, Aire Acondicionado'
                WHEN i <= 95 THEN '30 Computadores, Proyector, Aire Acondicionado, Switch de Red'
                ELSE 'Herramientas Especializadas, Proyector, Tablero, Ventilación'
            END,
            'AVAILABLE'
        );
    END LOOP;
END $$;
EOF

    verify_phase "FASE 2" "SELECT COUNT(*) as total_venues FROM scheduleservice_schema.venues;"

    # FASE 3: Academic Programs
    log "📋 FASE 3: Academic Programs (programas)"

    # Crear tabla academic_programs
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << 'EOF'
CREATE TABLE scheduleservice_schema.academic_programs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    program_type VARCHAR(50) NOT NULL,
    duration_months INTEGER NOT NULL,
    coordination VARCHAR(100) NOT NULL,
    level VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_programs_coordination ON scheduleservice_schema.academic_programs(coordination);
CREATE INDEX idx_programs_type ON scheduleservice_schema.academic_programs(program_type);
CREATE INDEX idx_programs_status ON scheduleservice_schema.academic_programs(status);
EOF

    # Insertar programas
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME << 'EOF'
INSERT INTO scheduleservice_schema.academic_programs (name, code, description, program_type, duration_months, coordination, level, status) VALUES
('Análisis y Desarrollo de Software', 'ADSO-2025', 'Formación en desarrollo de aplicaciones web y móviles', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Gestión de Redes de Datos', 'GRD-2025', 'Administración y configuración de redes de computadores', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Sistemas', 'SIS-2025', 'Análisis, diseño e implementación de sistemas de información', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Seguridad Informática', 'SEGINF-2025', 'Protección de sistemas y datos informáticos', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Programación de Software', 'PROGSW-2025', 'Desarrollo de aplicaciones y software especializado', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Mantenimiento de Equipos de Cómputo', 'MANEQC-2025', 'Soporte técnico y mantenimiento de hardware', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Soporte de Infraestructura TI', 'SOPITI-2025', 'Administración de infraestructura tecnológica', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Desarrollo Web', 'DESWEB-2025', 'Creación de sitios y aplicaciones web', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Base de Datos', 'BD-2025', 'Diseño, implementación y administración de bases de datos', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Inteligencia Artificial', 'IA-2025', 'Fundamentos y aplicaciones de IA y Machine Learning', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Ciberseguridad', 'CIBSEG-2025', 'Protección avanzada de sistemas y ciberdefensa', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('DevOps y Cloud Computing', 'DEVOPS-2025', 'Integración continua y computación en la nube', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Diseño Gráfico', 'DISGRA-2025', 'Creación de piezas gráficas y comunicación visual', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Animación Digital', 'ANIMDIG-2025', 'Producción de animaciones 2D y 3D', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Producción Multimedia', 'PRODMUL-2025', 'Desarrollo de contenidos multimedia interactivos', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Fotografía Digital', 'FOTDIG-2025', 'Técnicas avanzadas de fotografía y postproducción', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Edición de Video y Audio', 'VIDAUD-2025', 'Postproducción audiovisual profesional', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('UX/UI Design', 'UXUI-2025', 'Diseño de experiencia e interfaz de usuario', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Modelado y Renderizado 3D', 'MOD3D-2025', 'Creación de modelos tridimensionales y renderizado', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Gestión de Contenidos Digitales', 'GESTCONT-2025', 'Administración de contenidos y marketing digital', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE');
EOF

    verify_phase "FASE 3" "SELECT COUNT(*) as total_programas FROM scheduleservice_schema.academic_programs;"

    success "🎉 ¡FASES 1-3 COMPLETADAS EXITOSAMENTE!"
    log "📋 Resumen de progreso:"
    log "   ✅ FASE 1: Coordinación creada"
    log "   ✅ FASE 2: 100 Venues creados"
    log "   ✅ FASE 3: 20 Programas creados"

    warning "⏸️  PAUSA RECOMENDADA: Verificar datos antes de continuar con FASES 4-8"
    log "🔍 Para verificar datos manualmente:"
    log "   docker exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME"

    read -p "¿Continuar con FASES 4-8 (fichas, instructores, aprendices, horarios, asistencia)? (s/n): " continue_phases

    if [[ $continue_phases == "s" || $continue_phases == "S" ]]; then
        log "🚀 Continuando con FASES 4-8..."
        # Aquí se pueden agregar las fases restantes
        warning "⚠️  FASES 4-8 pendientes de implementación en script"
        log "📖 Consultar PLAN_EJECUCION_VPS_ONEVISION.md para scripts manuales"
    else
        log "⏸️  Ejecución pausada en FASE 3"
        log "📖 Para continuar manualmente, consultar PLAN_EJECUCION_VPS_ONEVISION.md"
    fi
}

# Verificar argumentos
if [[ $# -gt 0 && $1 == "--help" ]]; then
    echo "🚀 Script de Ejecución Automática - Base de Datos OneVision"
    echo ""
    echo "Uso: $0 [--help]"
    echo ""
    echo "Este script ejecuta automáticamente las FASES 1-3 del plan:"
    echo "  - FASE 1: Coordinación (tabla users)"
    echo "  - FASE 2: Sedes (tabla venues)"
    echo "  - FASE 3: Programas (tabla academic_programs)"
    echo ""
    echo "Para FASES 4-8, consultar PLAN_EJECUCION_VPS_ONEVISION.md"
    echo ""
    echo "Requisitos:"
    echo "  - PostgreSQL corriendo en Docker"
    echo "  - Contenedor: $CONTAINER_NAME"
    echo "  - Usuario DB: $DB_USER"
    exit 0
fi

# Ejecutar función principal
main "$@"
