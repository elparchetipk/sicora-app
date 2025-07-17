# 🏢 EPTI ONEVISION - Esquema de Base de Datos

## 🔒 PRINCIPIOS DE PROTECCIÓN DE DATOS

### **Separación Absoluta**

- ❌ **NUNCA usar datos reales del SENA**
- ✅ **Estructura idéntica con datos sintéticos**
- ✅ **Entorno completamente independiente en Hostinger**
- ✅ **Generación automática de datos de prueba**

---

## 📊 ESTRUCTURA DE BASE DE DATOS

### **🗄️ Base de Datos: `epti_onevision_demo`**

```sql
-- Base de datos principal para EPTI ONEVISION
CREATE DATABASE epti_onevision_demo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

---

## 👥 **ESQUEMA: USUARIOS Y AUTENTICACIÓN**

### **Tabla: users**

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    documento VARCHAR(20) UNIQUE NOT NULL,
    tipo_documento ENUM('CC', 'CE', 'TI', 'PAS') DEFAULT 'CC',
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified_at TIMESTAMP NULL,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    genero ENUM('M', 'F', 'O') DEFAULT 'O',
    estado ENUM('activo', 'inactivo', 'suspendido') DEFAULT 'activo',
    foto_perfil VARCHAR(500),
    direccion TEXT,
    ciudad VARCHAR(100),
    departamento VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_documento (documento),
    INDEX idx_email (email),
    INDEX idx_estado (estado)
);
```

### **Tabla: roles**

```sql
CREATE TABLE roles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    nivel_acceso INT DEFAULT 1,
    permisos JSON,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_slug (slug),
    INDEX idx_nivel (nivel_acceso)
);
```

### **Tabla: user_roles**

```sql
CREATE TABLE user_roles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    asignado_por BIGINT,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NULL,
    activo BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (asignado_por) REFERENCES users(id) ON DELETE SET NULL,

    UNIQUE KEY unique_user_role (user_id, role_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id)
);
```

---

## 🏫 **ESQUEMA: ESTRUCTURA ACADÉMICA**

### **Tabla: centros_formacion**

```sql
CREATE TABLE centros_formacion (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    direccion TEXT,
    ciudad VARCHAR(100),
    departamento VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(255),
    director_id BIGINT,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (director_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_codigo (codigo),
    INDEX idx_estado (estado)
);
```

### **Tabla: programas_formacion**

```sql
CREATE TABLE programas_formacion (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(300) NOT NULL,
    nivel ENUM('tecnico', 'tecnologo', 'especializacion', 'complementaria') NOT NULL,
    modalidad ENUM('presencial', 'virtual', 'mixta') NOT NULL,
    duracion_horas INT NOT NULL,
    duracion_meses INT NOT NULL,
    version VARCHAR(10) DEFAULT '1.0',
    area_conocimiento VARCHAR(200),
    sector_economico VARCHAR(200),
    centro_id BIGINT NOT NULL,
    coordinador_id BIGINT,
    estado ENUM('activo', 'inactivo', 'revision') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (centro_id) REFERENCES centros_formacion(id) ON DELETE CASCADE,
    FOREIGN KEY (coordinador_id) REFERENCES users(id) ON DELETE SET NULL,

    INDEX idx_codigo (codigo),
    INDEX idx_nivel (nivel),
    INDEX idx_modalidad (modalidad),
    INDEX idx_centro (centro_id)
);
```

### **Tabla: fichas_formacion**

```sql
CREATE TABLE fichas_formacion (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    numero_ficha VARCHAR(20) UNIQUE NOT NULL,
    programa_id BIGINT NOT NULL,
    centro_id BIGINT NOT NULL,
    jornada ENUM('mañana', 'tarde', 'noche', 'mixta', 'fin_semana') NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin_lectiva DATE NOT NULL,
    fecha_fin_practica DATE NOT NULL,
    cupos_disponibles INT DEFAULT 30,
    cupos_ocupados INT DEFAULT 0,
    instructor_lider_id BIGINT,
    estado ENUM('programada', 'ejecucion', 'finalizada', 'cancelada') DEFAULT 'programada',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (programa_id) REFERENCES programas_formacion(id) ON DELETE CASCADE,
    FOREIGN KEY (centro_id) REFERENCES centros_formacion(id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_lider_id) REFERENCES users(id) ON DELETE SET NULL,

    INDEX idx_numero_ficha (numero_ficha),
    INDEX idx_programa (programa_id),
    INDEX idx_fecha_inicio (fecha_inicio),
    INDEX idx_estado (estado)
);
```

---

## 👨‍🎓 **ESQUEMA: APRENDICES E INSCRIPCIONES**

### **Tabla: aprendices**

```sql
CREATE TABLE aprendices (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNIQUE NOT NULL,
    ficha_id BIGINT NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    estado_matricula ENUM('matriculado', 'desertor', 'aplazado', 'graduado', 'cancelado') DEFAULT 'matriculado',
    modalidad_actual ENUM('lectiva', 'practica', 'finalizado') DEFAULT 'lectiva',
    empresa_practica VARCHAR(300),
    tutor_empresa VARCHAR(200),
    telefono_tutor VARCHAR(20),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (ficha_id) REFERENCES fichas_formacion(id) ON DELETE CASCADE,

    INDEX idx_ficha (ficha_id),
    INDEX idx_estado (estado_matricula),
    INDEX idx_modalidad (modalidad_actual)
);
```

---

## 📅 **ESQUEMA: HORARIOS Y PROGRAMACIÓN**

### **Tabla: ambientes_formacion**

```sql
CREATE TABLE ambientes_formacion (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('aula', 'laboratorio', 'taller', 'auditorio', 'virtual') NOT NULL,
    capacidad INT DEFAULT 30,
    centro_id BIGINT NOT NULL,
    ubicacion VARCHAR(200),
    recursos_disponibles JSON,
    estado ENUM('disponible', 'mantenimiento', 'ocupado', 'inactivo') DEFAULT 'disponible',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (centro_id) REFERENCES centros_formacion(id) ON DELETE CASCADE,

    INDEX idx_codigo (codigo),
    INDEX idx_tipo (tipo),
    INDEX idx_centro (centro_id),
    INDEX idx_estado (estado)
);
```

### **Tabla: horarios**

```sql
CREATE TABLE horarios (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    ficha_id BIGINT NOT NULL,
    instructor_id BIGINT NOT NULL,
    ambiente_id BIGINT NOT NULL,
    competencia VARCHAR(300),
    resultado_aprendizaje TEXT,
    dia_semana ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    activo BOOLEAN DEFAULT TRUE,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (ficha_id) REFERENCES fichas_formacion(id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (ambiente_id) REFERENCES ambientes_formacion(id) ON DELETE CASCADE,

    INDEX idx_ficha (ficha_id),
    INDEX idx_instructor (instructor_id),
    INDEX idx_ambiente (ambiente_id),
    INDEX idx_dia_hora (dia_semana, hora_inicio),
    INDEX idx_fecha_rango (fecha_inicio, fecha_fin)
);
```

---

## 📊 **ESQUEMA: ASISTENCIA Y SEGUIMIENTO**

### **Tabla: asistencias**

```sql
CREATE TABLE asistencias (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    aprendiz_id BIGINT NOT NULL,
    horario_id BIGINT NOT NULL,
    fecha DATE NOT NULL,
    hora_llegada TIME,
    hora_salida TIME,
    estado ENUM('asistio', 'falta', 'tardanza', 'excusa', 'permiso') NOT NULL,
    justificacion TEXT,
    registrado_por BIGINT,
    metodo_registro ENUM('manual', 'qr', 'biometrico', 'automatico') DEFAULT 'manual',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (aprendiz_id) REFERENCES aprendices(id) ON DELETE CASCADE,
    FOREIGN KEY (horario_id) REFERENCES horarios(id) ON DELETE CASCADE,
    FOREIGN KEY (registrado_por) REFERENCES users(id) ON DELETE SET NULL,

    UNIQUE KEY unique_asistencia (aprendiz_id, horario_id, fecha),
    INDEX idx_fecha (fecha),
    INDEX idx_estado (estado),
    INDEX idx_aprendiz_fecha (aprendiz_id, fecha)
);
```

---

## 🔐 **ESQUEMA: SEGURIDAD Y AUDITORÍA**

### **Tabla: sessions**

```sql
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id BIGINT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    payload LONGTEXT NOT NULL,
    last_activity INT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_last_activity (last_activity)
);
```

### **Tabla: audit_logs**

```sql
CREATE TABLE audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(100),
    record_id BIGINT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,

    INDEX idx_user_action (user_id, action),
    INDEX idx_table_record (table_name, record_id),
    INDEX idx_created_at (created_at)
);
```

---

## 🎯 **DATOS DE EJEMPLO EPTI ONEVISION**

### **Nombres de Programas Sintéticos:**

- "Desarrollo de Software Empresarial"
- "Gestión de Redes y Telecomunicaciones"
- "Análisis de Datos y Business Intelligence"
- "Ciberseguridad y Ethical Hacking"
- "Gestión de Proyectos Tecnológicos"
- "Marketing Digital y E-commerce"
- "Automatización Industrial 4.0"
- "Desarrollo de Aplicaciones Móviles"

### **Centros de Formación Ficticios:**

- "Centro Tecnológico EPTI Norte"
- "Centro de Innovación EPTI Sur"
- "Campus Virtual EPTI Digital"
- "Centro EPTI Empresarial"

---

## 🚀 **PRÓXIMOS PASOS**

1. **Generador de Datos Sintéticos** - Script automático
2. **Seeders de Base de Datos** - Población inicial
3. **API de Datos Demo** - Endpoints de prueba
4. **Dashboard de Monitoreo** - Verificación de datos

---

## 📋 **CHECKLIST DE IMPLEMENTACIÓN**

- [ ] Crear esquema en Hostinger
- [ ] Implementar generador de datos
- [ ] Validar estructura con backend
- [ ] Generar datos de prueba suficientes
- [ ] Configurar entorno de desarrollo
- [ ] Documentar APIs de acceso
- [ ] Implementar sistema de backup
- [ ] Configurar monitoreo de datos

---

**🔒 RECORDATORIO: Todos los datos son sintéticos y NO representan información real del SENA**
