# 🔒 POLÍTICAS DE PROTECCIÓN DE DATOS - SHARED-DATA

**Fecha de implementación**: 15 de junio de 2025  
**Alcance**: Directorio shared-data/ completo  
**Clasificación**: DATOS SENSIBLES - ACCESO RESTRINGIDO

---

## 🎯 **OBJETIVOS DE SEGURIDAD**

### **Protección de Información Personal**
- **Datos de aprendices**: Nombres, documentos, emails, fichas
- **Datos de instructores**: Información personal y profesional
- **Datos académicos**: Evaluaciones, asistencia, desempeño
- **Metadatos sensibles**: Patrones de uso, estadísticas

### **Control de Acceso**
- **Solo stacks autorizados**: 01-fastapi a 06-springboot-kotlin
- **Sin acceso directo**: Usuarios, sistemas externos, herramientas
- **Logging completo**: Todas las operaciones de acceso
- **Auditoría**: Trazabilidad completa de cambios

---

## 🔐 **NIVELES DE CLASIFICACIÓN**

### **🔴 CRÍTICO - Nunca exponer**
- **Datos reales de producción**: Información personal real
- **Credenciales**: Contraseñas, tokens, keys
- **Configuraciones sensibles**: Conexiones DB, APIs
- **Logs detallados**: Que puedan exponer patrones

### **🟡 SENSIBLE - Solo desarrollo autorizado**
- **Datos sintéticos realistas**: Que simulen información real
- **Templates con ejemplos**: Con datos ficticios pero realistas
- **Configuraciones de desarrollo**: Sin credenciales reales
- **Logs de desarrollo**: Sin información personal

### **🟢 PÚBLICO - Puede ser compartido**
- **Documentación**: README.md, especificaciones
- **Esquemas de validación**: JSON Schema sin datos
- **Templates vacíos**: Solo estructura, sin ejemplos
- **Herramientas**: Scripts sin datos embebidos

---

## 📂 **POLÍTICAS POR DIRECTORIO**

### **📁 imports/ - 🔴 CRÍTICO**
```
ACCESO: Solo stacks autorizados
CONTENIDO: Archivos fuente para importación
PROTECCIÓN: Todos los archivos .csv/.json/.xlsx ignorados en git
EXCEPCIÓN: Solo README.md y .gitkeep
```

**Archivos protegidos:**
- `users/*.csv` - Datos personales de usuarios
- `schedules/*.csv` - Información académica
- `attendance/*.csv` - Registros de asistencia
- `evaluations/*.csv` - Evaluaciones confidenciales

### **📁 templates/ - 🟡 SENSIBLE**
```
ACCESO: Solo stacks + documentación
CONTENIDO: Plantillas con ejemplos ficticios
PROTECCIÓN: Solo .template.csv permitidos en git
EJEMPLOS: Datos sintéticos, no reales
```

**Archivos permitidos:**
- `users.template.csv` - Plantilla sin datos reales
- `schedules.template.csv` - Estructura sin información real
- Solo headers y 1-2 filas de ejemplo ficticio

### **📁 exports/ - 🔴 CRÍTICO**
```
ACCESO: Solo stack que generó + stack consumidor
CONTENIDO: Datos exportados por cada stack
PROTECCIÓN: Todo contenido ignorado en git
AUDITORÍA: Log de todas las operaciones
```

**Estructura protegida:**
```
exports/
├── fastapi/     # Solo acceso desde FastAPI
├── go/          # Solo acceso desde Go
├── express/     # Solo acceso desde Express
├── nextjs/      # Solo acceso desde Next.js
├── java/        # Solo acceso desde Java
└── kotlin/      # Solo acceso desde Kotlin
```

### **📁 samples/ - 🟡 SENSIBLE**
```
ACCESO: Solo stacks para testing
CONTENIDO: Datasets de ejemplo sintéticos
PROTECCIÓN: Archivos de datos ignorados en git
DATOS: Solo sintéticos, nunca reales
```

**Políticas por tamaño:**
- `small/` - Máximo 100 registros sintéticos
- `medium/` - Máximo 10K registros sintéticos
- `large/` - Solo para testing de performance

### **📁 schemas/ - 🟢 PÚBLICO**
```
ACCESO: Público dentro del proyecto
CONTENIDO: Esquemas de validación JSON
PROTECCIÓN: Sin datos, solo estructura
VERSIONADO: Controlado en git
```

---

## 🛡️ **CONTROLES DE SEGURIDAD IMPLEMENTADOS**

### **🚫 Git Protection**
```bash
# Todos los archivos de datos ignorados
imports/**/*.csv
exports/**/*.json
samples/**/*.xlsx

# Solo estructura y documentación
!README.md
!*.template.csv
!schemas/*.json
```

### **🔒 Permisos de Sistema**
```bash
# Solo stacks pueden acceder
chmod 750 shared-data/
chmod 640 shared-data/**/*.csv

# Solo lectura para exports de otros stacks
chmod 444 exports/other-stack/*.csv
```

### **📝 Logging de Acceso**
```bash
# Todas las operaciones loggeadas
access.log: timestamp, stack, operation, file, result
security.log: failed_access_attempts, unauthorized_access
audit.log: data_modifications, schema_changes
```

### **🔍 Validación de Integridad**
```bash
# Checksums para detectar modificaciones
md5sum imports/**/*.csv > .checksums
sha256sum exports/**/*.json >> .checksums
```

---

## 🚨 **PROCEDIMIENTOS DE EMERGENCIA**

### **🔥 En caso de exposición accidental**
1. **Inmediato**: Revocar acceso al archivo expuesto
2. **5 minutos**: Notificar al equipo de seguridad
3. **15 minutos**: Evaluar alcance de la exposición
4. **30 minutos**: Implementar medidas correctivas
5. **24 horas**: Reporte completo de incidente

### **🧹 Limpieza de datos sensibles**
```bash
# Script de limpieza de emergencia
./tools/emergency-cleanup.sh --purge-sensitive
./tools/emergency-cleanup.sh --reset-permissions
./tools/emergency-cleanup.sh --audit-access
```

### **🔄 Recuperación de incidente**
1. **Restaurar desde backup limpio**
2. **Re-generar datos sintéticos**
3. **Validar integridad de esquemas**
4. **Verificar permisos de acceso**
5. **Auditoría completa post-incidente**

---

## 📋 **CHECKLIST DE CUMPLIMIENTO**

### **✅ Antes de cualquier commit**
- [ ] Verificar que no hay archivos .csv/.json en staging
- [ ] Confirmar que solo README.md y schemas/ están incluidos
- [ ] Ejecutar `git status` y revisar archivos listados
- [ ] Verificar .gitignore está actualizado

### **✅ Antes de cualquier deploy**
- [ ] Auditar logs de acceso recientes
- [ ] Verificar integridad de checksums
- [ ] Confirmar permisos de directorio
- [ ] Validar configuraciones de seguridad

### **✅ Mantenimiento semanal**
- [ ] Rotar logs de acceso y auditoría
- [ ] Actualizar checksums de archivos
- [ ] Revisar intentos de acceso fallidos
- [ ] Limpiar archivos temporales antiguos

---

## 🔧 **HERRAMIENTAS DE SEGURIDAD**

### **📊 Monitor de Acceso**
```bash
# Monitoreo continuo de acceso
./tools/access-monitor.sh --watch
./tools/access-monitor.sh --report-daily
```

### **🔍 Auditor de Integridad**
```bash
# Verificación de integridad
./tools/integrity-checker.sh --verify-all
./tools/integrity-checker.sh --generate-report
```# 1. Optimizar proyecto (15 seg)
chmod +x tools/optimize-project.sh
./tools/optimize-project.sh --full

# 2. Setup shared-data (15 seg)  
chmod +x tools/shared-data-fast-setup.sh
./tools/shared-data-fast-setup.sh

# 3. Listo para usar
ls shared-data/templates/

### **🧹 Limpiador Automático**
```bash
# Limpieza automática programada
./tools/auto-cleaner.sh --schedule-daily
./tools/auto-cleaner.sh --purge-old-logs
```

---

## 📞 **CONTACTOS DE SEGURIDAD**

### **🚨 Incidentes de Seguridad**
- **Equipo Principal**: sicora-security@sena.edu.co
- **Backup**: project-lead@sena.edu.co
- **Escalación**: ciso@sena.edu.co

### **📋 Soporte Técnico**
- **Desarrolladores**: sicora-dev@sena.edu.co
- **DevOps**: sicora-ops@sena.edu.co
- **Auditoría**: sicora-audit@sena.edu.co

---

## 📚 **REFERENCIAS NORMATIVAS**

### **📖 Marcos de Referencia**
- **Ley 1581 de 2012**: Protección de Datos Personales (Colombia)
- **GDPR**: Reglamento General de Protección de Datos
- **ISO 27001**: Gestión de Seguridad de la Información
- **NIST**: Framework de Ciberseguridad

### **📋 Políticas Internas SENA**
- **Manual de Imagen Corporativa**: _docs/general/manual_imagen_corporativa_sena.md
- **Requisitos Funcionales**: _docs/general/rf.md
- **Clean Architecture**: CLEAN-ARCHITECTURE.md

---

**IMPORTANTE**: Esta política es de cumplimiento obligatorio para todos los stacks del proyecto SICORA-APP Backend Multistack. Su incumplimiento puede resultar en la suspensión del acceso al directorio shared-data/ y escalación al equipo de seguridad institucional.
