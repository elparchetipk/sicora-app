-- 🎲 DATOS SINTÉTICOS EPTI ONEVISION
-- Generado manualmente para demostración
-- IMPORTANTE: Todos los datos son ficticios y NO representan información real del SENA

USE epti_onevision_demo;

-- ==========================================
-- 🔐 ROLES DEL SISTEMA
-- ==========================================

CREATE TABLE IF NOT EXISTS roles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    nivel_acceso INT DEFAULT 1,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles (nombre, slug, descripcion, nivel_acceso) VALUES
('Aprendiz', 'aprendiz', 'Estudiante inscrito en programa de formación EPTI', 1),
('Instructor', 'instructor', 'Docente encargado de la formación en EPTI', 3),
('Coordinador Académico', 'coordinador', 'Coordinador de programas EPTI', 5),
('Administrativo', 'administrativo', 'Personal administrativo EPTI', 4);

-- ==========================================
-- 🏫 CENTROS DE FORMACIÓN EPTI
-- ==========================================

CREATE TABLE IF NOT EXISTS centros_formacion (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    ciudad VARCHAR(100),
    departamento VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(255),
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO centros_formacion (codigo, nombre, ciudad, departamento, telefono, email) VALUES
('EPTI-NO', 'Centro Tecnológico EPTI Norte', 'Bogotá', 'Cundinamarca', '(601) 555-0101', 'norte@epti.edu.co'),
('EPTI-SU', 'Centro de Innovación EPTI Sur', 'Medellín', 'Antioquia', '(604) 555-0102', 'sur@epti.edu.co'),
('EPTI-VR', 'Campus Virtual EPTI Digital', 'Cali', 'Valle del Cauca', '(602) 555-0103', 'virtual@epti.edu.co'),
('EPTI-EM', 'Centro EPTI Empresarial', 'Barranquilla', 'Atlántico', '(605) 555-0104', 'empresarial@epti.edu.co');

-- ==========================================
-- 📚 PROGRAMAS DE FORMACIÓN EPTI
-- ==========================================

CREATE TABLE IF NOT EXISTS programas_formacion (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(300) NOT NULL,
    nivel ENUM('tecnico', 'tecnologo', 'especializacion', 'complementaria') NOT NULL,
    modalidad ENUM('presencial', 'virtual', 'mixta') NOT NULL,
    duracion_horas INT NOT NULL,
    duracion_meses INT NOT NULL,
    centro_id BIGINT NOT NULL,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (centro_id) REFERENCES centros_formacion(id)
);

INSERT INTO programas_formacion (codigo, nombre, nivel, modalidad, duracion_horas, duracion_meses, centro_id) VALUES
('EPTI001', 'Desarrollo de Software Empresarial', 'tecnologo', 'presencial', 2640, 24, 1),
('EPTI002', 'Gestión de Redes y Telecomunicaciones', 'tecnico', 'presencial', 1760, 18, 1),
('EPTI003', 'Análisis de Datos y Business Intelligence', 'tecnologo', 'mixta', 2640, 24, 2),
('EPTI004', 'Ciberseguridad y Ethical Hacking', 'especializacion', 'virtual', 880, 12, 3),
('EPTI005', 'Gestión de Proyectos Tecnológicos', 'tecnologo', 'mixta', 2200, 20, 2),
('EPTI006', 'Marketing Digital y E-commerce', 'tecnico', 'virtual', 1540, 16, 3),
('EPTI007', 'Automatización Industrial 4.0', 'tecnologo', 'presencial', 2640, 24, 4),
('EPTI008', 'Desarrollo de Aplicaciones Móviles', 'tecnico', 'presencial', 1760, 18, 4);

-- ==========================================
-- 👥 USUARIOS DEMO (MUESTRA)
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    documento VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL DEFAULT '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi',
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    genero ENUM('M', 'F') DEFAULT 'M',
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    ciudad VARCHAR(100),
    departamento VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usuarios de ejemplo (todos con datos sintéticos)
INSERT INTO users (documento, nombres, apellidos, email, telefono, fecha_nacimiento, genero, ciudad, departamento) VALUES
-- Coordinadores
('9910001', 'Carlos Eduardo', 'García López', 'demo.carlos.garcia01@epti.edu.co', '3001234567', '1975-03-15', 'M', 'Bogotá', 'Cundinamarca'),
('9910002', 'María Isabel', 'Rodríguez Martínez', 'demo.maria.rodriguez02@epti.edu.co', '3109876543', '1978-07-22', 'F', 'Medellín', 'Antioquia'),

-- Instructores
('9920001', 'Luis Fernando', 'López González', 'demo.luis.lopez01@epti.edu.co', '3201122334', '1985-01-10', 'M', 'Bogotá', 'Cundinamarca'),
('9920002', 'Ana Patricia', 'Martínez Sánchez', 'demo.ana.martinez02@epti.edu.co', '3152233445', '1982-09-18', 'F', 'Cali', 'Valle del Cauca'),
('9920003', 'David Alejandro', 'Pérez Cruz', 'demo.david.perez03@epti.edu.co', '3003344556', '1988-11-05', 'M', 'Medellín', 'Antioquia'),
('9920004', 'Sandra Milena', 'Flores Rivera', 'demo.sandra.flores04@epti.edu.co', '3104455667', '1990-04-12', 'F', 'Barranquilla', 'Atlántico'),

-- Aprendices
('9930001', 'Miguel Ángel', 'Gómez Díaz', 'demo.miguel.gomez01@epti.edu.co', '3205566778', '2000-02-28', 'M', 'Bogotá', 'Cundinamarca'),
('9930002', 'Laura Daniela', 'Reyes Morales', 'demo.laura.reyes02@epti.edu.co', '3156677889', '1999-08-14', 'F', 'Medellín', 'Antioquia'),
('9930003', 'Andrés Felipe', 'Jiménez Herrera', 'demo.andres.jimenez03@epti.edu.co', '3007788990', '2001-06-07', 'M', 'Cali', 'Valle del Cauca'),
('9930004', 'Valeria Sofia', 'Medina Castro', 'demo.valeria.medina04@epti.edu.co', '3108899001', '2000-12-20', 'F', 'Barranquilla', 'Atlántico'),
('9930005', 'Sebastián', 'Ortiz Rubio', 'demo.sebastian.ortiz05@epti.edu.co', '3209900112', '1998-10-03', 'M', 'Bogotá', 'Cundinamarca'),
('9930006', 'Natalia', 'Marín Vargas', 'demo.natalia.marin06@epti.edu.co', '3150011223', '2002-01-16', 'F', 'Medellín', 'Antioquia');

-- ==========================================
-- 🔗 ASIGNACIÓN DE ROLES
-- ==========================================

CREATE TABLE IF NOT EXISTS user_roles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    UNIQUE KEY unique_user_role (user_id, role_id)
);

-- Asignar roles a usuarios demo
INSERT INTO user_roles (user_id, role_id) VALUES
-- Coordinadores
(1, 3), (2, 3),
-- Instructores  
(3, 2), (4, 2), (5, 2), (6, 2),
-- Aprendices
(7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1);

-- ==========================================
-- 📊 CONSULTAS DE VERIFICACIÓN
-- ==========================================

-- Estadísticas de usuarios por rol
SELECT 
    r.nombre as rol,
    COUNT(ur.user_id) as cantidad_usuarios
FROM roles r
LEFT JOIN user_roles ur ON r.id = ur.role_id
GROUP BY r.id, r.nombre
ORDER BY r.nivel_acceso DESC;

-- Verificar que todos los emails son de EPTI
SELECT 
    'Emails EPTI' as verificacion,
    COUNT(*) as total,
    COUNT(CASE WHEN email LIKE '%@epti.edu.co' THEN 1 END) as epti_emails,
    COUNT(CASE WHEN email LIKE 'demo.%' THEN 1 END) as demo_prefijo
FROM users;

-- Verificar documentos sintéticos
SELECT 
    'Documentos Demo' as verificacion,
    COUNT(*) as total,
    COUNT(CASE WHEN documento LIKE '99%' THEN 1 END) as demo_documentos
FROM users;

-- ==========================================
-- ✅ CONFIRMACIÓN
-- ==========================================

SELECT '🎉 Base de datos EPTI ONEVISION configurada correctamente' as mensaje;
SELECT '🔒 Todos los datos son sintéticos y seguros' as seguridad;
SELECT '📊 Datos listos para desarrollo y demostraciones' as estado;
