# 🚀 Plan de Ejecución VPS - Base de Datos OneVision

## 🎯 Estrategia: Base de Datos Independiente

Vamos a crear una base de datos **completamente independiente** para OneVision en el VPS Hostinger, separada de SICORA, para realizar las pruebas de forma aislada.

## 📋 Configuración Inicial VPS

### 1. Conectar al VPS y Preparar Base de Datos

```bash
# Conectar al VPS Hostinger (Fedora Cloud 42)
ssh fedora@TU_IP_VPS

# Verificar que PostgreSQL esté corriendo en Docker
docker ps | grep postgres

# Si no está corriendo, iniciarlo
cd ~/sicora-backend
docker-compose up -d postgres

# Conectar a PostgreSQL
docker exec -it sicora-backend_postgres_1 psql -U sicora_user -d sicora_production
```

### 2. Crear Base de Datos OneVision Independiente

```sql
-- Crear base de datos independiente para OneVision
CREATE DATABASE onevision_testing;

-- Conectar a la nueva base de datos
\c onevision_testing;

-- Crear esquemas necesarios
CREATE SCHEMA IF NOT EXISTS userservice_schema;
CREATE SCHEMA IF NOT EXISTS scheduleservice_schema;
CREATE SCHEMA IF NOT EXISTS attendanceservice_schema;
CREATE SCHEMA IF NOT EXISTS evalinservice_schema;
CREATE SCHEMA IF NOT EXISTS kbservice_schema;
CREATE SCHEMA IF NOT EXISTS aiservice_schema;
CREATE SCHEMA IF NOT EXISTS projectevalservice_schema;

-- Verificar esquemas creados
\dn
```

## 📊 Plan de Ejecución Tabla por Tabla

### FASE 1: Tabla `users` (userservice_schema)

#### Paso 1.1: Crear Tabla Users

```sql
-- SCRIPT: 01_create_users_table.sql
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

-- Índices para optimización
CREATE INDEX idx_users_role ON userservice_schema.users(role);
CREATE INDEX idx_users_email ON userservice_schema.users(email);
CREATE INDEX idx_users_identification ON userservice_schema.users(identification_number);
CREATE INDEX idx_users_status ON userservice_schema.users(status);
```

#### Paso 1.2: Insertar Datos de Prueba - Coordinación

```sql
-- SCRIPT: 02_insert_coordination.sql
-- 1 Coordinador para Teleinformática e Industrias Creativas
INSERT INTO userservice_schema.users (
    id, first_name, last_name, email, password_hash, role,
    identification_number, phone, address, birth_date, status, is_active
) VALUES (
    gen_random_uuid(),
    'María Elena',
    'Rodríguez Gómez',
    'coordinacion.teleinformatica@sena.edu.co',
    '$2b$12$LQv3c1yqBwEHxPiLNPAl2.PjDthHZ7QRwm6EHNM3GyJNuQhGwkqG2', -- password123
    'COORDINATOR',
    '52147896',
    '+57 311 555 0001',
    'Carrera 30 #17-00, Bogotá',
    '1985-03-15',
    'ACTIVE',
    true
);
```

#### Paso 1.3: Verificar Coordinación

```sql
-- VERIFICACIÓN 1: Coordinador creado
SELECT
    first_name, last_name, email, role, identification_number, phone
FROM userservice_schema.users
WHERE role = 'COORDINATOR';

-- Resultado esperado: 1 registro (María Elena Rodríguez Gómez)
```

### FASE 2: Tabla `venues` (scheduleservice_schema)

#### Paso 2.1: Crear Tabla Venues (Sedes)

```sql
-- SCRIPT: 03_create_venues_table.sql
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
```

#### Paso 2.2: Insertar Sedes y Venues

```sql
-- SCRIPT: 04_insert_venues.sql
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
                WHEN i <= 20 THEN 25  -- Aulas pequeñas
                WHEN i <= 40 THEN 30  -- Aulas medianas
                ELSE 35               -- Aulas grandes
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
                WHEN i <= 70 THEN 25  -- Aulas pequeñas
                WHEN i <= 90 THEN 30  -- Aulas medianas
                ELSE 35               -- Aulas grandes
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
```

#### Paso 2.3: Verificar Venues

```sql
-- VERIFICACIÓN 2: Venues creados
SELECT
    COUNT(*) as total_venues,
    COUNT(*) FILTER (WHERE location LIKE '%Calle 52%') as calle_52,
    COUNT(*) FILTER (WHERE location LIKE '%Fontibón%') as fontibon,
    COUNT(*) FILTER (WHERE venue_type = 'CLASSROOM') as classrooms,
    COUNT(*) FILTER (WHERE venue_type = 'COMPUTER_LAB') as labs,
    COUNT(*) FILTER (WHERE venue_type = 'WORKSHOP') as workshops
FROM scheduleservice_schema.venues;

-- Resultado esperado: 100 total (50 Calle 52, 50 Fontibón)
```

### FASE 3: Tabla `academic_programs` (scheduleservice_schema)

#### Paso 3.1: Crear Tabla Academic Programs

```sql
-- SCRIPT: 05_create_academic_programs_table.sql
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
```

#### Paso 3.2: Insertar Programas de Formación

```sql
-- SCRIPT: 06_insert_academic_programs.sql
-- 20 Programas de Teleinformática e Industrias Creativas
INSERT INTO scheduleservice_schema.academic_programs (name, code, description, program_type, duration_months, coordination, level, status) VALUES

-- TELEINFORMÁTICA (12 programas)
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

-- INDUSTRIAS CREATIVAS (8 programas)
('Diseño Gráfico', 'DISGRA-2025', 'Creación de piezas gráficas y comunicación visual', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Animación Digital', 'ANIMDIG-2025', 'Producción de animaciones 2D y 3D', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Producción Multimedia', 'PRODMUL-2025', 'Desarrollo de contenidos multimedia interactivos', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Fotografía Digital', 'FOTDIG-2025', 'Técnicas avanzadas de fotografía y postproducción', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Edición de Video y Audio', 'VIDAUD-2025', 'Postproducción audiovisual profesional', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('UX/UI Design', 'UXUI-2025', 'Diseño de experiencia e interfaz de usuario', 'TECNOLOGIA', 24, 'Teleinformática e Industrias Creativas', 'TECNOLOGO', 'ACTIVE'),
('Modelado y Renderizado 3D', 'MOD3D-2025', 'Creación de modelos tridimensionales y renderizado', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE'),
('Gestión de Contenidos Digitales', 'GESTCONT-2025', 'Administración de contenidos y marketing digital', 'TECNICA', 18, 'Teleinformática e Industrias Creativas', 'TECNICO', 'ACTIVE');
```

#### Paso 3.3: Verificar Programas

```sql
-- VERIFICACIÓN 3: Programas creados
SELECT
    COUNT(*) as total_programas,
    COUNT(*) FILTER (WHERE program_type = 'TECNOLOGIA') as tecnologia,
    COUNT(*) FILTER (WHERE program_type = 'TECNICA') as tecnica,
    COUNT(*) FILTER (WHERE level = 'TECNOLOGO') as tecnologos,
    COUNT(*) FILTER (WHERE level = 'TECNICO') as tecnicos
FROM scheduleservice_schema.academic_programs;

-- Resultado esperado: 20 total (12 tecnología, 8 técnica)

-- Ver lista completa
SELECT code, name, program_type, level, duration_months
FROM scheduleservice_schema.academic_programs
ORDER BY program_type, name;
```

### FASE 4: Tabla `academic_groups` (scheduleservice_schema) - FICHAS

#### Paso 4.1: Crear Tabla Academic Groups

```sql
-- SCRIPT: 07_create_academic_groups_table.sql
CREATE TABLE scheduleservice_schema.academic_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    number VARCHAR(20) UNIQUE NOT NULL,
    academic_program_id UUID NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    shift VARCHAR(20) NOT NULL CHECK (shift IN ('MAÑANA', 'TARDE', 'NOCHE')),
    status VARCHAR(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE', 'COMPLETED', 'SUSPENDED')),
    max_apprentices INTEGER DEFAULT 30,
    current_apprentices INTEGER DEFAULT 0,
    coordinator_id UUID,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_academic_groups_program
        FOREIGN KEY (academic_program_id)
        REFERENCES scheduleservice_schema.academic_programs(id),
    CONSTRAINT fk_academic_groups_coordinator
        FOREIGN KEY (coordinator_id)
        REFERENCES userservice_schema.users(id)
);

CREATE INDEX idx_academic_groups_program ON scheduleservice_schema.academic_groups(academic_program_id);
CREATE INDEX idx_academic_groups_shift ON scheduleservice_schema.academic_groups(shift);
CREATE INDEX idx_academic_groups_status ON scheduleservice_schema.academic_groups(status);
CREATE INDEX idx_academic_groups_dates ON scheduleservice_schema.academic_groups(start_date, end_date);
```

#### Paso 4.2: Insertar 100 Fichas

```sql
-- SCRIPT: 08_insert_academic_groups.sql
-- Generar 100 fichas distribuidas en los 20 programas
DO $$
DECLARE
    program_record RECORD;
    coordinator_id UUID;
    ficha_counter INTEGER := 1;
    fichas_per_program INTEGER;
    start_date_var DATE;
    end_date_var DATE;
    shifts TEXT[] := ARRAY['MAÑANA', 'TARDE', 'NOCHE'];
    shift_choice TEXT;
BEGIN
    -- Obtener ID del coordinador
    SELECT id INTO coordinator_id
    FROM userservice_schema.users
    WHERE role = 'COORDINATOR'
    LIMIT 1;

    -- Crear fichas para cada programa
    FOR program_record IN
        SELECT id, name, code, duration_months
        FROM scheduleservice_schema.academic_programs
        ORDER BY code
    LOOP
        -- 5 fichas por programa (100 total / 20 programas)
        fichas_per_program := 5;

        FOR i IN 1..fichas_per_program LOOP
            -- Fechas escalonadas cada 3 meses
            start_date_var := '2024-01-01'::DATE + ((i-1) * INTERVAL '3 months');
            end_date_var := start_date_var + (program_record.duration_months * INTERVAL '1 month');

            -- Alternar turnos
            shift_choice := shifts[((ficha_counter - 1) % 3) + 1];

            INSERT INTO scheduleservice_schema.academic_groups (
                number, academic_program_id, start_date, end_date,
                shift, status, max_apprentices, coordinator_id
            ) VALUES (
                LPAD(ficha_counter::text, 6, '0'), -- 000001, 000002, etc.
                program_record.id,
                start_date_var,
                end_date_var,
                shift_choice,
                CASE
                    WHEN i <= 3 THEN 'ACTIVE'
                    WHEN i = 4 THEN 'COMPLETED'
                    ELSE 'INACTIVE'
                END,
                CASE
                    WHEN shift_choice = 'MAÑANA' THEN 30
                    WHEN shift_choice = 'TARDE' THEN 28
                    ELSE 25  -- NOCHE
                END,
                coordinator_id
            );

            ficha_counter := ficha_counter + 1;
        END LOOP;
    END LOOP;
END $$;
```

#### Paso 4.3: Verificar Fichas

```sql
-- VERIFICACIÓN 4: Fichas creadas
SELECT
    COUNT(*) as total_fichas,
    COUNT(*) FILTER (WHERE shift = 'MAÑANA') as mañana,
    COUNT(*) FILTER (WHERE shift = 'TARDE') as tarde,
    COUNT(*) FILTER (WHERE shift = 'NOCHE') as noche,
    COUNT(*) FILTER (WHERE status = 'ACTIVE') as activas,
    COUNT(*) FILTER (WHERE status = 'COMPLETED') as completadas,
    COUNT(*) FILTER (WHERE status = 'INACTIVE') as inactivas
FROM scheduleservice_schema.academic_groups;

-- Resultado esperado: 100 fichas total
```

### FASE 5: Tabla `users` - INSTRUCTORES (userservice_schema)

#### Paso 5.1: Insertar 100 Instructores

```sql
-- SCRIPT: 09_insert_instructors.sql
-- Generar 100 instructores realistas
DO $$
DECLARE
    i INTEGER;
    first_names TEXT[] := ARRAY[
        'Carlos', 'María', 'José', 'Ana', 'Luis', 'Laura', 'David', 'Carmen', 'Miguel', 'Elena',
        'Roberto', 'Patricia', 'Fernando', 'Isabel', 'Alejandro', 'Mónica', 'Ricardo', 'Andrea',
        'Antonio', 'Claudia', 'Pedro', 'Rosa', 'Manuel', 'Sandra', 'Francisco', 'Diana',
        'Jorge', 'Beatriz', 'Rafael', 'Gloria', 'Alberto', 'Esperanza', 'Sergio', 'Pilar',
        'Andrés', 'Teresa', 'Ramón', 'Amparo', 'Javier', 'Dolores', 'Enrique', 'Mercedes',
        'Rubén', 'Cristina', 'Vicente', 'Concepción', 'Eduardo', 'Remedios', 'Salvador', 'Josefa'
    ];
    last_names TEXT[] := ARRAY[
        'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez', 'Pérez',
        'Gómez', 'Martín', 'Jiménez', 'Ruiz', 'Hernández', 'Díaz', 'Moreno', 'Muñoz',
        'Álvarez', 'Romero', 'Alonso', 'Gutiérrez', 'Navarro', 'Torres', 'Domínguez', 'Vázquez',
        'Ramos', 'Gil', 'Ramírez', 'Serrano', 'Blanco', 'Suárez', 'Molina', 'Morales',
        'Ortega', 'Delgado', 'Castro', 'Ortiz', 'Rubio', 'Marín', 'Sanz', 'Iglesias',
        'Medina', 'Garrido', 'Cortés', 'Castillo', 'Santos', 'Lozano', 'Guerrero', 'Cano',
        'Prieto', 'Méndez', 'Cruz', 'Flores', 'Herrera', 'Peña', 'León', 'Cabrera'
    ];
    first_name TEXT;
    last_name TEXT;
    email TEXT;
    identification TEXT;
    phone TEXT;
    birth_year INTEGER;
BEGIN
    FOR i IN 1..100 LOOP
        -- Seleccionar nombres aleatorios
        first_name := first_names[((i * 7) % array_length(first_names, 1)) + 1];
        last_name := last_names[((i * 11) % array_length(last_names, 1)) + 1];

        -- Generar email único
        email := lower(first_name) || '.' || lower(last_name) || '.' || LPAD(i::text, 3, '0') || '@sena.edu.co';

        -- Generar identificación única
        identification := (25000000 + i)::text;

        -- Generar teléfono
        phone := '+57 31' || (1 + (i % 9))::text || ' ' ||
                LPAD(((100 + i) % 900 + 100)::text, 3, '0') || ' ' ||
                LPAD(((1000 + i * 7) % 9000 + 1000)::text, 4, '0');

        -- Año de nacimiento (30-55 años)
        birth_year := 1969 + (i % 26);

        INSERT INTO userservice_schema.users (
            first_name, last_name, email, password_hash, role,
            identification_number, phone, address, birth_date, status, is_active
        ) VALUES (
            first_name,
            last_name,
            email,
            '$2b$12$LQv3c1yqBwEHxPiLNPAl2.PjDthHZ7QRwm6EHNM3GyJNuQhGwkqG2', -- password123
            'INSTRUCTOR',
            identification,
            phone,
            'Calle ' || ((i % 50) + 1)::text || ' #' || ((i % 30) + 10)::text || '-' || LPAD(((i % 99) + 1)::text, 2, '0') || ', Bogotá',
            (birth_year || '-' || LPAD(((i % 12) + 1)::text, 2, '0') || '-' || LPAD(((i % 28) + 1)::text, 2, '0'))::DATE,
            'ACTIVE',
            true
        );
    END LOOP;
END $$;
```

#### Paso 5.2: Verificar Instructores

```sql
-- VERIFICACIÓN 5: Instructores creados
SELECT
    COUNT(*) as total_instructores,
    COUNT(*) FILTER (WHERE status = 'ACTIVE') as activos
FROM userservice_schema.users
WHERE role = 'INSTRUCTOR';

-- Resultado esperado: 100 instructores activos
```

### FASE 6: Tabla `users` - APRENDICES (userservice_schema)

#### Paso 6.1: Insertar ~2,750 Aprendices (25-30 por ficha)

```sql
-- SCRIPT: 10_insert_apprentices.sql
-- Generar aprendices para cada ficha
DO $$
DECLARE
    ficha_record RECORD;
    i INTEGER;
    apprentices_count INTEGER;
    first_names TEXT[] := ARRAY[
        'Juan', 'María', 'Pedro', 'Ana', 'Luis', 'Carmen', 'José', 'Laura', 'Carlos', 'Elena',
        'Miguel', 'Patricia', 'Antonio', 'Isabel', 'Francisco', 'Rosa', 'Manuel', 'Lucía',
        'David', 'Pilar', 'Jesús', 'Dolores', 'Javier', 'Teresa', 'Daniel', 'Cristina',
        'Rafael', 'Amparo', 'Alejandro', 'Mercedes', 'Fernando', 'Esperanza', 'Sergio', 'Gloria',
        'Jorge', 'Beatriz', 'Roberto', 'Remedios', 'Alberto', 'Josefa', 'Ricardo', 'Concepción',
        'Andrés', 'Inmaculada', 'Ángel', 'Montserrat', 'Ramón', 'Ángeles', 'Vicente', 'Encarnación'
    ];
    last_names TEXT[] := ARRAY[
        'Jiménez', 'Ruiz', 'López', 'García', 'Martínez', 'González', 'Pérez', 'Sánchez',
        'Romero', 'Gómez', 'Fernández', 'Moreno', 'Díaz', 'Álvarez', 'Muñoz', 'Hernández',
        'Torres', 'Navarro', 'Domínguez', 'Ramos', 'Vázquez', 'Gil', 'Serrano', 'Ramírez',
        'Blanco', 'Molina', 'Morales', 'Suárez', 'Ortega', 'Castro', 'Delgado', 'Ortiz'
    ];
    first_name TEXT;
    last_name TEXT;
    email TEXT;
    identification TEXT;
    phone TEXT;
    birth_year INTEGER;
    counter INTEGER := 1;
BEGIN
    FOR ficha_record IN
        SELECT id, number, max_apprentices
        FROM scheduleservice_schema.academic_groups
        ORDER BY number
    LOOP
        -- Variar cantidad de aprendices (25-30)
        apprentices_count := 25 + (counter % 6); -- 25-30 aprendices

        FOR i IN 1..apprentices_count LOOP
            -- Seleccionar nombres aleatorios
            first_name := first_names[((counter * 3 + i) % array_length(first_names, 1)) + 1];
            last_name := last_names[((counter * 5 + i) % array_length(last_names, 1)) + 1];

            -- Generar email único para aprendiz
            email := lower(first_name) || '.' || lower(last_name) || '.' || counter::text || '.' || i::text || '@misena.edu.co';

            -- Generar identificación única para aprendices (1M+)
            identification := (1000000000 + counter * 100 + i)::text;

            -- Generar teléfono móvil
            phone := '+57 3' || ((counter + i) % 9 + 1)::text || (counter % 10)::text || ' ' ||
                    LPAD(((counter * 10 + i) % 900 + 100)::text, 3, '0') || ' ' ||
                    LPAD(((counter * 100 + i * 7) % 9000 + 1000)::text, 4, '0');

            -- Edad aprendices: 18-25 años
            birth_year := 1999 + ((counter + i) % 8);

            INSERT INTO userservice_schema.users (
                first_name, last_name, email, password_hash, role,
                identification_number, phone, address, birth_date, status, is_active
            ) VALUES (
                first_name,
                last_name,
                email,
                '$2b$12$LQv3c1yqBwEHxPiLNPAl2.PjDthHZ7QRwm6EHNM3GyJNuQhGwkqG2', -- password123
                'APPRENTICE',
                identification,
                phone,
                'Calle ' || ((counter + i) % 80 + 1)::text || ' #' || ((counter + i) % 40 + 5)::text || '-' || LPAD((((counter + i) % 150) + 1)::text, 3, '0') || ', Bogotá',
                (birth_year || '-' || LPAD((((counter + i) % 12) + 1)::text, 2, '0') || '-' || LPAD((((counter + i) % 28) + 1)::text, 2, '0'))::DATE,
                'ACTIVE',
                true
            );
        END LOOP;

        -- Actualizar contador de aprendices en la ficha
        UPDATE scheduleservice_schema.academic_groups
        SET current_apprentices = apprentices_count
        WHERE id = ficha_record.id;

        counter := counter + 1;
    END LOOP;
END $$;
```

#### Paso 6.2: Verificar Aprendices

```sql
-- VERIFICACIÓN 6: Aprendices creados
SELECT
    COUNT(*) as total_aprendices,
    COUNT(*) FILTER (WHERE status = 'ACTIVE') as activos,
    ROUND(AVG(current_apprentices), 2) as promedio_por_ficha
FROM userservice_schema.users u
RIGHT JOIN scheduleservice_schema.academic_groups ag ON true
WHERE u.role = 'APPRENTICE';

-- Resultado esperado: ~2,750 aprendices (25-30 por ficha)
```

### FASE 7: Tabla `schedules` (scheduleservice_schema) - HORARIOS

#### Paso 7.1: Crear Tabla Schedules

```sql
-- SCRIPT: 11_create_schedules_table.sql
CREATE TABLE scheduleservice_schema.schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    academic_group_id UUID NOT NULL,
    venue_id UUID NOT NULL,
    instructor_id UUID NOT NULL,
    subject_name VARCHAR(255) NOT NULL,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_schedules_group
        FOREIGN KEY (academic_group_id)
        REFERENCES scheduleservice_schema.academic_groups(id),
    CONSTRAINT fk_schedules_venue
        FOREIGN KEY (venue_id)
        REFERENCES scheduleservice_schema.venues(id),
    CONSTRAINT fk_schedules_instructor
        FOREIGN KEY (instructor_id)
        REFERENCES userservice_schema.users(id)
);

CREATE INDEX idx_schedules_group ON scheduleservice_schema.schedules(academic_group_id);
CREATE INDEX idx_schedules_venue ON scheduleservice_schema.schedules(venue_id);
CREATE INDEX idx_schedules_instructor ON scheduleservice_schema.schedules(instructor_id);
CREATE INDEX idx_schedules_day_time ON scheduleservice_schema.schedules(day_of_week, start_time);
CREATE INDEX idx_schedules_dates ON scheduleservice_schema.schedules(start_date, end_date);
```

#### Paso 7.2: Insertar Horarios (UN horario único por ficha)

```sql
-- SCRIPT: 12_insert_schedules.sql
-- Generar UN horario principal por ficha (no múltiples)
DO $$
DECLARE
    ficha_record RECORD;
    instructor_ids UUID[];
    venue_ids UUID[];
    subjects TEXT[] := ARRAY[
        'Programación Orientada a Objetos', 'Base de Datos Relacional', 'Desarrollo Web Frontend',
        'Desarrollo Web Backend', 'Redes de Computadores', 'Seguridad Informática',
        'Análisis y Diseño de Sistemas', 'Estructura de Datos', 'Algoritmos de Programación',
        'Gestión de Proyectos TI', 'Inglés Técnico', 'Emprendimiento Digital',
        'Diseño Gráfico Digital', 'Animación 2D/3D', 'Edición de Video',
        'Fotografía Digital', 'UX/UI Design', 'Marketing Digital'
    ];
    start_time TIME;
    end_time TIME;
    selected_instructor UUID;
    selected_venue UUID;
    selected_subject TEXT;
BEGIN
    -- Obtener IDs de instructores y venues
    SELECT array_agg(id) INTO instructor_ids
    FROM userservice_schema.users
    WHERE role = 'INSTRUCTOR' AND status = 'ACTIVE';

    SELECT array_agg(id) INTO venue_ids
    FROM scheduleservice_schema.venues
    WHERE availability_status = 'AVAILABLE';

    FOR ficha_record IN
        SELECT id, number, shift, start_date, end_date
        FROM scheduleservice_schema.academic_groups
        WHERE status = 'ACTIVE'
        ORDER BY number
    LOOP
        -- Definir horarios según turno
        CASE ficha_record.shift
            WHEN 'MAÑANA' THEN
                start_time := '06:00:00';
                end_time := '12:00:00';
            WHEN 'TARDE' THEN
                start_time := '12:00:00';
                end_time := '18:00:00';
            WHEN 'NOCHE' THEN
                start_time := '18:00:00';
                end_time := '22:00:00';
        END CASE;

        -- Seleccionar instructor aleatorio
        selected_instructor := instructor_ids[((ficha_record.number::integer) % array_length(instructor_ids, 1)) + 1];

        -- Seleccionar venue aleatorio
        selected_venue := venue_ids[((ficha_record.number::integer) % array_length(venue_ids, 1)) + 1];

        -- Seleccionar materia aleatoria
        selected_subject := subjects[((ficha_record.number::integer) % array_length(subjects, 1)) + 1];

        -- Insertar UN SOLO horario por ficha (Lunes a Viernes)
        FOR day_num IN 1..5 LOOP  -- Lunes a Viernes
            INSERT INTO scheduleservice_schema.schedules (
                academic_group_id, venue_id, instructor_id, subject_name,
                day_of_week, start_time, end_time, start_date, end_date
            ) VALUES (
                ficha_record.id,
                selected_venue,
                selected_instructor,
                selected_subject,
                day_num,
                start_time,
                end_time,
                ficha_record.start_date,
                ficha_record.end_date
            );
        END LOOP;
    END LOOP;
END $$;
```

#### Paso 7.3: Verificar Horarios

```sql
-- VERIFICACIÓN 7: Horarios creados
SELECT
    COUNT(*) as total_horarios,
    COUNT(DISTINCT academic_group_id) as fichas_con_horario,
    COUNT(*) FILTER (WHERE day_of_week BETWEEN 1 AND 5) as dias_laborales,
    COUNT(DISTINCT venue_id) as venues_utilizados,
    COUNT(DISTINCT instructor_id) as instructores_asignados
FROM scheduleservice_schema.schedules;

-- Resultado esperado: ~375 horarios (75 fichas activas × 5 días)
```

### FASE 8: Tabla `attendance_records` (attendanceservice_schema) - ASISTENCIA

#### Paso 8.1: Crear Tabla Attendance Records

```sql
-- SCRIPT: 13_create_attendance_table.sql
CREATE TABLE attendanceservice_schema.attendance_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    schedule_id UUID NOT NULL,
    attendance_date DATE NOT NULL,
    check_in_time TIMESTAMP WITH TIME ZONE,
    check_out_time TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('PRESENT', 'ABSENT', 'LATE', 'EXCUSED')),
    location_verified BOOLEAN DEFAULT false,
    device_info JSONB,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_attendance_user
        FOREIGN KEY (user_id)
        REFERENCES userservice_schema.users(id),
    CONSTRAINT fk_attendance_schedule
        FOREIGN KEY (schedule_id)
        REFERENCES scheduleservice_schema.schedules(id)
);

CREATE INDEX idx_attendance_user ON attendanceservice_schema.attendance_records(user_id);
CREATE INDEX idx_attendance_schedule ON attendanceservice_schema.attendance_records(schedule_id);
CREATE INDEX idx_attendance_date ON attendanceservice_schema.attendance_records(attendance_date);
CREATE INDEX idx_attendance_status ON attendanceservice_schema.attendance_records(status);
```

#### Paso 8.2: Insertar Registros de Asistencia (último mes)

```sql
-- SCRIPT: 14_insert_attendance_records.sql
-- Generar asistencia para el último mes de fichas activas
DO $$
DECLARE
    schedule_record RECORD;
    apprentice_record RECORD;
    date_counter DATE;
    attendance_status TEXT;
    check_in TIMESTAMP;
    check_out TIMESTAMP;
    attendance_rate DECIMAL := 0.85; -- 85% de asistencia promedio
BEGIN
    FOR schedule_record IN
        SELECT s.id as schedule_id, s.academic_group_id, s.day_of_week,
               s.start_time, s.end_time, s.start_date, s.end_date,
               ag.current_apprentices
        FROM scheduleservice_schema.schedules s
        JOIN scheduleservice_schema.academic_groups ag ON s.academic_group_id = ag.id
        WHERE ag.status = 'ACTIVE'
    LOOP
        -- Obtener aprendices de la ficha
        FOR apprentice_record IN
            SELECT u.id as user_id
            FROM userservice_schema.users u
            WHERE u.role = 'APPRENTICE' AND u.status = 'ACTIVE'
            LIMIT schedule_record.current_apprentices
        LOOP
            -- Generar asistencia para el último mes (enero 2025)
            date_counter := '2025-01-01'::DATE;

            WHILE date_counter <= '2025-01-31'::DATE LOOP
                -- Solo días que coinciden con el horario
                IF EXTRACT(DOW FROM date_counter) =
                   CASE schedule_record.day_of_week
                       WHEN 1 THEN 1  -- Lunes
                       WHEN 2 THEN 2  -- Martes
                       WHEN 3 THEN 3  -- Miércoles
                       WHEN 4 THEN 4  -- Jueves
                       WHEN 5 THEN 5  -- Viernes
                       ELSE 0
                   END
                   AND schedule_record.day_of_week BETWEEN 1 AND 5 THEN

                    -- Determinar estado de asistencia (85% presente)
                    IF random() < attendance_rate THEN
                        attendance_status := 'PRESENT';
                        check_in := date_counter + schedule_record.start_time +
                                   (random() * INTERVAL '10 minutes'); -- Llegada +/- 10 min
                        check_out := date_counter + schedule_record.end_time +
                                    (random() * INTERVAL '15 minutes'); -- Salida +/- 15 min
                    ELSE
                        -- 15% ausencias/tardanzas/excusas
                        CASE (random() * 3)::INTEGER
                            WHEN 0 THEN
                                attendance_status := 'ABSENT';
                                check_in := NULL;
                                check_out := NULL;
                            WHEN 1 THEN
                                attendance_status := 'LATE';
                                check_in := date_counter + schedule_record.start_time +
                                           INTERVAL '20 minutes' + (random() * INTERVAL '30 minutes');
                                check_out := date_counter + schedule_record.end_time;
                            ELSE
                                attendance_status := 'EXCUSED';
                                check_in := NULL;
                                check_out := NULL;
                        END CASE;
                    END IF;

                    INSERT INTO attendanceservice_schema.attendance_records (
                        user_id, schedule_id, attendance_date,
                        check_in_time, check_out_time, status,
                        location_verified, device_info
                    ) VALUES (
                        apprentice_record.user_id,
                        schedule_record.schedule_id,
                        date_counter,
                        check_in,
                        check_out,
                        attendance_status,
                        CASE WHEN attendance_status = 'PRESENT' THEN true ELSE false END,
                        CASE WHEN attendance_status = 'PRESENT' THEN
                            '{"device": "mobile", "app_version": "1.0.0"}'::JSONB
                        ELSE NULL END
                    );
                END IF;

                date_counter := date_counter + INTERVAL '1 day';
            END LOOP;
        END LOOP;
    END LOOP;
END $$;
```

#### Paso 8.3: Verificar Registros de Asistencia

```sql
-- VERIFICACIÓN 8: Registros de asistencia
SELECT
    COUNT(*) as total_registros,
    COUNT(*) FILTER (WHERE status = 'PRESENT') as presentes,
    COUNT(*) FILTER (WHERE status = 'ABSENT') as ausentes,
    COUNT(*) FILTER (WHERE status = 'LATE') as tardanzas,
    COUNT(*) FILTER (WHERE status = 'EXCUSED') as excusados,
    ROUND((COUNT(*) FILTER (WHERE status = 'PRESENT'))::DECIMAL / COUNT(*) * 100, 2) as porcentaje_asistencia
FROM attendanceservice_schema.attendance_records;

-- Resultado esperado: ~85% de asistencia
```

## 🔄 Proceso de Validación por Fase - ACTUALIZADO

### Comandos de Conexión VPS

```bash
# Conectar a PostgreSQL en VPS
docker exec -it sicora-backend_postgres_1 psql -U sicora_user -d onevision_testing

# Ver esquemas
\dn

# Ver tablas completas
\dt userservice_schema.*
\dt scheduleservice_schema.*
\dt attendanceservice_schema.*
```

## 📋 Checklist de Ejecución - COMPLETO

- [ ] **FASE 1**: Tabla `users` - Coordinación ✅
- [ ] **FASE 2**: Tabla `venues` - Sedes ✅
- [ ] **FASE 3**: Tabla `academic_programs` - Programas ✅
- [ ] **FASE 4**: Tabla `academic_groups` - Fichas ✅
- [ ] **FASE 5**: Tabla `users` - Instructores ✅
- [ ] **FASE 6**: Tabla `users` - Aprendices ✅
- [ ] **FASE 7**: Tabla `schedules` - Horarios ✅
- [ ] **FASE 8**: Tabla `attendance_records` - Asistencia ✅

## 🎯 Datos Finales Esperados

- **1 Coordinador** (Teleinformática e Industrias Creativas)
- **100 Venues** (50 Calle 52, 50 Fontibón)
- **20 Programas** (12 Tecnología, 8 Técnica)
- **100 Fichas** (5 por programa, turnos variados)
- **100 Instructores** (distribuidos)
- **~2,750 Aprendices** (25-30 por ficha)
- **~375 Horarios** (75 fichas activas × 5 días)
- **~206,250 Registros de Asistencia** (enero 2025, 85% asistencia)

¿Estás listo para empezar con la FASE 1? 🚀
