# 🎯 Multi-Stack Backend Project Structure Guide

**Creado**: 15 de junio de 2025  
**Propósito**: Estructura organizacional para implementación de 6 stacks backend

## 📁 Estructura de Directorios

```
sicora-app-be-multistack/
├── 01-fastapi/          🐍 FastAPI (Python) - Base de Referencia
├── 02-go/               ⚡ Go - Performance y Concurrencia  
├── 03-express/          📱 Express.js (Node.js) - JavaScript Backend
├── 04-nextjs/           🚀 Next.js - TypeScript Backend Only
├── 05-springboot-java/  ☕ Spring Boot Java - Enterprise Standard
├── 06-springboot-kotlin/🔮 Spring Boot Kotlin - Modern JVM
├── _docs/               📚 Documentación Compartida
├── database/            🗄️ Scripts de BD Compartidos
├── nginx/               🌐 Configuración Web Server
├── shared-data/         📊 Datos Compartidos para Bulk Operations
├── tools/               🛠️ Herramientas Multi-Stack
├── sicora-docs/         📖 Documentación Externa (Enlace Simbólico)
└── docker-compose.yml   🐳 Orquestación de Servicios
```

## 🎯 Filosofía del Proyecto

### **Frontend Único + Backend Multistack**

```
📱 React Native + Expo (Frontend único)
├── Consume API de cualquiera de los 6 backends
├── Mismas funcionalidades, diferentes tecnologías
└── Comparación directa de rendimiento y características
```

### **Un Microservicio, Múltiples Implementaciones**

Cada microservicio (UserService, AttendanceService, etc.) se implementa en los 6 stacks, permitiendo:

- ✅ **Comparación directa** de tecnologías backend
- ✅ **Misma base de datos** por microservicio (compartida entre stacks)
- ✅ **APIs consistentes** entre todas las implementaciones
- ✅ **Clean Architecture** aplicada en cada stack
- ✅ **Casos de uso idénticos** con implementaciones diferentes

### **Decisión Arquitectónica: Next.js Backend Only**

**Next.js se implementa exclusivamente como backend** para mantener consistencia:

- **✅ Un frontend único**: React Native + Expo
- **✅ Seis backends diferentes**: Cada uno con sus fortalezas
- **✅ Comparación directa**: Sin interferencia de múltiples frontends
- **✅ Aprovecha características únicas**: Edge Functions, middleware nativo, streaming

### **Orden de Desarrollo Priorizado**

1. **FastAPI** → Producción inmediata ✅
2. **Go** → Performance y concurrencia 🚧
3. **Express.js** → JavaScript ecosystem 🚧
4. **Next.js** → TypeScript + Edge Computing 📋
5. **Spring Boot Java** → Enterprise standard 📋
6. **Spring Boot Kotlin** → Modern JVM 📋

## 🗄️ Estrategia de Bases de Datos

### **Principio: Una BD por Microservicio (Compartida entre Stacks)**

```
UserService (6 stacks) ────→ user_db (PostgreSQL 15)
AttendanceService (6 stacks) ─→ attendance_db (PostgreSQL 15)
ScheduleService (6 stacks) ───→ schedule_db (PostgreSQL 15)
KbService (6 stacks) ────────→ kb_db (PostgreSQL 15 + pgvector)
EvalinService (6 stacks) ────→ evalin_db (PostgreSQL 15)
AIService (6 stacks) ────────→ ai_db (PostgreSQL 15 + Vector DB)
```

**Beneficios**:

- ✅ Comparabilidad directa entre stacks
- ✅ Gestión simplificada (6 BD vs 36)
- ✅ Coherencia de datos para demos
- ✅ Enfoque en lógica de negocio vs setup BD

## 📋 Estado de Microservicios por Stack

| Microservicio | FastAPI | Go | Express | Next.js | Java | Kotlin |
|--------------|---------|----|---------|---------| ------|--------|
| UserService | ✅ 100% | 🚧 75% | 📋 0% | 📋 0% | 📋 0% | 📋 0% |
| AttendanceService | 📋 Migrar | 📋 0% | 📋 0% | 📋 0% | 📋 0% | 📋 0% |
| ScheduleService | ✅ 90% | 📋 0% | 📋 0% | 📋 0% | 📋 0% | 📋 0% |
| KbService | ✅ 85% | 📋 0% | 📋 0% | 📋 0% | 📋 0% | 📋 0% |
| EvalinService | ✅ 95% | 📋 0% | 📋 0% | 📋 0% | 📋 0% | 📋 0% |
| AIService | 📋 Migrar | 📋 0% | 📋 0% | 📋 0% | 📋 0% | 📋 0% |

## 🛠️ Plan de Migración

### **Fase 1: Reestructuración (Esta semana)**

- [x] Crear estructura de directorios multi-stack
- [x] Crear READMEs de orientación por stack
- [ ] Migrar servicios FastAPI existentes a `01-fastapi/`
- [ ] Actualizar docker-compose.yml para nueva estructura
- [ ] Validar funcionamiento post-migración

### **Fase 2: Completar UserService (Próximas 2 semanas)**

- [ ] FastAPI: Preparar para producción en Coordinación
- [ ] Go: Completar del 75% al 100%
- [ ] Express.js: Implementar desde cero

### **Fase 3: UserService Multi-Stack Completo (Mes 1-2)**

- [ ] Next.js: Implementar con API Routes
- [ ] Spring Boot Java: Setup enterprise
- [ ] Spring Boot Kotlin: Comparación directa con Java

## 📚 Documentación

### **Compartida** (`_docs/`)

- **RFs y Historias**: Fuente única de verdad
- **Especificación API**: Endpoints unificados
- **Estrategia BD**: Arquitectura de datos
- **Comparaciones**: Análisis cross-stack

### **Por Stack** (`XX-stack/README.md`)

- **Setup específico**: Instalación y configuración
- **Arquitectura**: Patrones y decisions específicas
- **Comandos**: Development workflow
- **Testing**: Estrategias de prueba

---

## 🛠️ Herramientas de Documentación

### Gestión de Permisos de Documentación Externa

Para proteger la documentación externa (`sicora-docs`) contra modificaciones accidentales:

#### 📜 Scripts Disponibles

**1. sicora-docs-permissions.sh** - Gestión completa de permisos

```bash
# Establecer solo lectura
./tools/sicora-docs-permissions.sh 1

# Habilitar escritura
./tools/sicora-docs-permissions.sh 2

# Ver estado actual
./tools/sicora-docs-permissions.sh
```

**2. sicora-docs-toggle.sh** - Alternar automáticamente

```bash
# Cambiar al modo opuesto automáticamente
./tools/sicora-docs-toggle.sh
```

#### ⚙️ Tareas de VS Code

Puedes ejecutar estos comandos desde la paleta de comandos:

- **`docs:set-readonly`** - Proteger documentación (solo lectura)
- **`docs:set-writable`** - Habilitar edición
- **`docs:toggle-permissions`** - Alternar automáticamente
- **`docs:check-status`** - Ver estado actual

#### 🔒 Modos de Permisos

**Modo Solo Lectura (Recomendado)**:

- Archivos: `444` (r--r--r--) - Solo lectura para todos
- Directorios: `555` (r-xr-xr-x) - Acceso sin modificación

**Modo Escritura (Temporal)**:

- Archivos: `644` (rw-r--r--) - Lectura/escritura para propietario
- Directorios: `755` (rwxr-xr-x) - Acceso completo para propietario

---

**🎯 Próximo Paso**: Migrar servicios FastAPI existentes a `01-fastapi/` y completar UserService en Go.
