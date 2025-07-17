# 🌐 CONFIGURACIÓN HOSTINGER - EPTI ONEVISION

## 🎯 OBJETIVO

Configurar el entorno de base de datos en Hostinger para EPTI ONEVISION con datos sintéticos que replican la estructura del SENA pero protegen completamente la información institucional.

---

## 🔐 PRINCIPIOS DE SEGURIDAD

### **🚫 PROHIBICIONES ABSOLUTAS**

- ❌ NUNCA conectar con bases de datos reales del SENA
- ❌ NUNCA usar credenciales de producción del SENA
- ❌ NUNCA exponer datos reales en el entorno de demostración
- ❌ NUNCA usar nombres, documentos o información personal real

### **✅ GARANTÍAS DE PROTECCIÓN**

- ✅ Base de datos completamente separada (`epti_onevision_demo`)
- ✅ Todos los datos son sintéticos y autogenerados
- ✅ Credenciales independientes para EPTI
- ✅ Hosting completamente separado (Hostinger)
- ✅ Dominio diferente (`epti.onevision.co` vs dominios SENA)

---

## 🏗️ CONFIGURACIÓN DE BASE DE DATOS

### **1. Crear Base de Datos en Hostinger**

```sql
-- Crear base de datos principal
CREATE DATABASE epti_onevision_demo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Crear usuario dedicado
CREATE USER 'epti_user'@'%' IDENTIFIED BY 'EptiDemo2024#Secure';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON epti_onevision_demo.* TO 'epti_user'@'%';
FLUSH PRIVILEGES;
```

### **2. Configuración de Conexión**

```env
# .env.hostinger - Configuración para Hostinger
DATABASE_HOST=your-database-host.hostinger.com
DATABASE_PORT=3306
DATABASE_NAME=epti_onevision_demo
DATABASE_USER=epti_user
DATABASE_PASSWORD=EptiDemo2024#Secure

# URLs de la aplicación
VITE_API_URL=https://api.epti.onevision.co
VITE_APP_URL=https://epti.onevision.co
VITE_ENVIRONMENT=hostinger

# Configuración de branding
VITE_BRAND_MODE=EPTI
VITE_BRAND_NAME="EPTI ONEVISION"
VITE_BRAND_DESCRIPTION="Plataforma de Gestión Académica EPTI"
VITE_BRAND_LOGO="/logos/epti-logo.png"

# Configuración de funcionalidades
VITE_ENABLE_DEMO_DATA=true
VITE_ENABLE_DATA_GENERATION=true
VITE_DEMO_MODE=true
```

---

## 📊 PROCESO DE IMPLEMENTACIÓN

### **Paso 1: Preparar el Entorno**

```bash
# 1. Generar datos sintéticos
cd sicora-app-fe
pnpm generate:data

# 2. Verificar archivos generados
ls -la database/
# - epti_demo_data.sql (Script de creación)
# - epti_demo_data.json (Datos en formato JSON)
```

### **Paso 2: Configurar Hostinger**

1. **Acceder al Panel de Hostinger**
   - Ir a hPanel > Bases de Datos MySQL
   - Crear nueva base de datos: `epti_onevision_demo`
   - Crear usuario: `epti_user`

2. **Importar Esquema**

   ```bash
   # Subir epti_demo_data.sql via phpMyAdmin o comando
   mysql -h database-host.hostinger.com -u epti_user -p epti_onevision_demo < database/epti_demo_data.sql
   ```

3. **Verificar Importación**

   ```sql
   USE epti_onevision_demo;

   -- Verificar tablas creadas
   SHOW TABLES;

   -- Verificar datos importados
   SELECT COUNT(*) FROM users;
   SELECT COUNT(*) FROM fichas_formacion;
   SELECT COUNT(*) FROM programas_formacion;
   ```

### **Paso 3: Configurar Backend**

```bash
# En el backend (Node.js/Express)
cd ../sicora-be-express

# Instalar dependencias de BD
npm install mysql2 sequelize

# Configurar conexión
cat > config/database.hostinger.js << EOF
module.exports = {
  development: {
    host: process.env.DATABASE_HOST,
    port: process.env.DATABASE_PORT,
    database: process.env.DATABASE_NAME,
    username: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
    dialect: 'mysql',
    dialectOptions: {
      charset: 'utf8mb4',
      timezone: 'America/Bogota'
    },
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
};
EOF
```

---

## 🔍 VALIDACIONES DE SEGURIDAD

### **Checklist de Seguridad Pre-Deploy**

- [ ] **Base de datos separada**: ✅ `epti_onevision_demo`
- [ ] **Usuario dedicado**: ✅ `epti_user` (no admin)
- [ ] **Datos sintéticos**: ✅ Verificar que todos los nombres/emails contienen "demo" o prefijos EPTI
- [ ] **Credenciales únicas**: ✅ No reutilizar credenciales del SENA
- [ ] **Hosting separado**: ✅ Hostinger (no servidores SENA)
- [ ] **Dominio diferente**: ✅ `epti.onevision.co`
- [ ] **Variables de entorno**: ✅ Configuradas para Hostinger

### **Script de Validación**

```sql
-- Validar que todos los datos son sintéticos
-- Los emails deben contener 'demo.' o '@epti.edu.co'
SELECT COUNT(*) as emails_sospechosos
FROM users
WHERE email NOT LIKE '%demo.%'
  AND email NOT LIKE '%@epti.edu.co';

-- Los documentos deben tener prefijo '99'
SELECT COUNT(*) as documentos_sospechosos
FROM users
WHERE documento NOT LIKE '99%';

-- Los nombres de programas deben contener referencias EPTI
SELECT COUNT(*) as programas_sospechosos
FROM programas_formacion
WHERE nombre NOT LIKE '%EPTI%'
  AND codigo NOT LIKE 'EPTI%';

-- Resultado esperado: 0 en todos los casos
```

---

## 📈 MONITOREO Y MÉTRICAS

### **Dashboard de Datos Demo**

```sql
-- Estadísticas del entorno demo
SELECT
    'Usuarios' as entidad,
    COUNT(*) as total,
    COUNT(CASE WHEN created_at >= CURDATE() - INTERVAL 7 DAY THEN 1 END) as ultimos_7_dias
FROM users

UNION ALL

SELECT
    'Fichas Activas' as entidad,
    COUNT(*) as total,
    COUNT(CASE WHEN estado = 'ejecucion' THEN 1 END) as activas
FROM fichas_formacion

UNION ALL

SELECT
    'Programas' as entidad,
    COUNT(*) as total,
    COUNT(CASE WHEN estado = 'activo' THEN 1 END) as activos
FROM programas_formacion;
```

### **Alertas de Seguridad**

```sql
-- Crear vista para monitoreo de seguridad
CREATE VIEW v_security_monitor AS
SELECT
    'Emails no EPTI' as alerta,
    COUNT(*) as cantidad
FROM users
WHERE email NOT LIKE '%@epti.edu.co'

UNION ALL

SELECT
    'Documentos sin prefijo demo' as alerta,
    COUNT(*) as cantidad
FROM users
WHERE documento NOT LIKE '99%';
```

---

## 🚀 COMANDOS DE DESPLIEGUE

### **Deploy Completo**

```bash
# 1. Generar datos frescos
pnpm generate:data

# 2. Build para Hostinger
pnpm build:hostinger

# 3. Subir archivos (FTP/Git)
# - Subir dist/ a public_html/
# - Subir database/epti_demo_data.sql
# - Configurar variables de entorno en Hostinger

# 4. Importar base de datos
# Via phpMyAdmin o línea de comandos en Hostinger

# 5. Verificar funcionamiento
curl https://epti.onevision.co/api/health
```

### **Mantenimiento de Datos**

```bash
# Regenerar datos cada mes (cron job)
0 0 1 * * cd /home/user/sicora-app-fe && pnpm generate:data && mysql -h db-host -u epti_user -p epti_onevision_demo < database/epti_demo_data.sql
```

---

## 📞 CONTACTO Y SOPORTE

**Para Configuración Hostinger:**

- 📧 Soporte: soporte@epti.onevision.co
- 📱 WhatsApp: +57 300 XXX XXXX
- 🌐 Panel: https://hpanel.hostinger.com

**Credenciales de Emergencia:**

- Usuario DB: `epti_backup`
- Permisos: Solo lectura
- Uso: Auditorías y respaldos

---

## ⚠️ DISCLAIMER

**🔒 RECORDATORIO CRÍTICO:**

- Todos los datos en este entorno son COMPLETAMENTE SINTÉTICOS
- NO representan información real del SENA o sus usuarios
- El uso es exclusivo para demostraciones de EPTI ONEVISION
- Cualquier similitud con datos reales es PURA COINCIDENCIA
- Mantener separación absoluta de sistemas productivos del SENA
