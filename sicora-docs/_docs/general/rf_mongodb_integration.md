# Requisitos Funcionales - Integración MongoDB NoSQL

**Actualizado: 3 de agosto de 2025**

Este documento describe los requisitos funcionales para la integración de MongoDB Community Edition como base de datos NoSQL complementaria en el proyecto educativo SICORA.

## 📋 **DOCUMENTACIÓN DE REFERENCIA**

- **[Infraestructura MongoDB](./rf_mongodb_infrastructure.md)**: Especificación completa de infraestructura, backup, failover y monitoreo
- **[Historias de Usuario Backend](../stories/be/HU_MongoDB_Integration.md)**: Implementación backend de MongoDB
- **[Historias de Usuario Frontend](../stories/fe/HU_FE_MongoDB_Integration.md)**: Interfaces de usuario para MongoDB

## 📚 Objetivos Educativos

### Propósito Principal

Ampliar el aprendizaje sobre tecnologías de bases de datos mediante la implementación de una solución híbrida que combine:

- **PostgreSQL** (RDBMS) - Para datos estructurados y transaccionales
- **Redis** (Cache/NoSQL Key-Value) - Para cache y sesiones
- **MongoDB** (NoSQL Document) - Para datos semi-estructurados y documentos

### Objetivos de Aprendizaje

1. **Comparación Práctica**: Entender cuándo usar SQL vs NoSQL
2. **Diseño Híbrido**: Implementar arquitecturas multi-base de datos
3. **Modelado de Datos**: Diferencias entre esquemas relacionales y documentales
4. **Rendimiento**: Evaluar performance en diferentes casos de uso
5. **Operaciones**: Administración y mantenimiento de sistemas NoSQL

## 🎯 Casos de Uso Específicos

### 1. Knowledge Base Service (KbService)

**Justificación**: Los artículos, documentos y FAQ tienen estructura variable y requieren flexibilidad de esquema.

**Datos para MongoDB**:

- Artículos técnicos con metadatos dinámicos
- Documentos con versionado
- FAQ con categorización flexible
- Comentarios y evaluaciones anidadas

### 2. Evaluations Service (EvalinService)

**Justificación**: Las evaluaciones pueden tener estructuras muy variables según el tipo.

**Datos para MongoDB**:

- Formularios de evaluación con campos dinámicos
- Respuestas con estructura variable
- Historiales de cambios detallados
- Metadatos de evaluación complejos

### 3. Audit & Logging Service (Nuevo)

**Justificación**: Los logs requieren alta velocidad de escritura y estructura flexible.

**Datos para MongoDB**:

- Logs de auditoría del sistema
- Eventos de usuario con contexto variable
- Métricas de rendimiento
- Trazabilidad de cambios

### 4. Notification Service (Nuevo)

**Justificación**: Las notificaciones necesitan metadatos flexibles y alta disponibilidad.

**Datos para MongoDB**:

- Notificaciones con contenido dinámico
- Configuraciones de usuario flexibles
- Historial de entregas
- Templates personalizables

## 🏗️ Arquitectura de Integración

### Estrategia Híbrida

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │    MongoDB      │
│   (Principal)   │    │    (Cache)      │    │  (Documentos)   │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Users         │    │ • Sessions      │    │ • Articles      │
│ • Schedules     │    │ • Cache         │    │ • Evaluations   │
│ • Attendance    │    │ • Temp Data     │    │ • Logs          │
│ • Projects      │    │ • Rate Limits   │    │ • Notifications │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Principios de Decisión

- **PostgreSQL**: Datos relacionales, transacciones ACID, consistencia fuerte
- **MongoDB**: Documentos, esquemas flexibles, escalabilidad horizontal
- **Redis**: Cache, sesiones, datos temporales

## 📋 Requisitos Funcionales Detallados

### RF-MONGO-001: Configuración Base

**Descripción**: Configurar MongoDB Community Edition en el entorno de desarrollo.

**Criterios de Aceptación**:

- [ ] MongoDB 8.x instalado y configurado
- [ ] Base de datos `sicora_nosql` creada
- [ ] Usuarios y permisos configurados
- [ ] Conexión desde todos los microservicios backends
- [ ] Docker Compose configurado para desarrollo

### RF-MONGO-002: Knowledge Base Documents

**Descripción**: Migrar y ampliar el sistema de gestión de conocimiento a MongoDB.

**Criterios de Aceptación**:

- [ ] Colección `articles` con esquema flexible
- [ ] Versionado de documentos implementado
- [ ] Búsqueda full-text configurada
- [ ] Indexación optimizada para consultas
- [ ] API REST para CRUD de artículos

**Estructura de Documento Ejemplo**:

```json
{
  "_id": ObjectId("..."),
  "title": "Guía de Desarrollo React",
  "slug": "guia-desarrollo-react",
  "content": "...",
  "author": {
    "id": "usr123",
    "name": "Juan Pérez",
    "email": "juan@example.com"
  },
  "metadata": {
    "category": "frontend",
    "tags": ["react", "javascript", "tutorial"],
    "difficulty": "intermediate",
    "estimatedTime": 30,
    "customFields": {
      "framework": "React 18",
      "dependencies": ["vite", "typescript"]
    }
  },
  "versions": [
    {
      "version": "1.0",
      "createdAt": ISODate("2025-08-03"),
      "changes": "Versión inicial"
    }
  ],
  "stats": {
    "views": 245,
    "likes": 18,
    "comments": 5
  },
  "status": "published",
  "createdAt": ISODate("2025-08-03"),
  "updatedAt": ISODate("2025-08-03")
}
```

### RF-MONGO-003: Dynamic Evaluations

**Descripción**: Implementar evaluaciones con estructura dinámica en MongoDB.

**Criterios de Aceptación**:

- [ ] Colección `evaluations` para formularios dinámicos
- [ ] Soporte para diferentes tipos de preguntas
- [ ] Validación flexible de respuestas
- [ ] Agregaciones para reportes
- [ ] Historial de cambios completo

**Estructura de Evaluación Ejemplo**:

```json
{
  "_id": ObjectId("..."),
  "title": "Evaluación de Instructor - Programación",
  "type": "instructor_evaluation",
  "version": "2.1",
  "sections": [
    {
      "id": "technical_skills",
      "title": "Habilidades Técnicas",
      "questions": [
        {
          "id": "q1",
          "type": "rating",
          "question": "Dominio del lenguaje de programación",
          "scale": { "min": 1, "max": 5 },
          "required": true
        },
        {
          "id": "q2",
          "type": "multiselect",
          "question": "Tecnologías que maneja",
          "options": ["JavaScript", "Python", "Go", "React", "Node.js"],
          "minSelections": 1
        }
      ]
    }
  ],
  "responses": [
    {
      "responseId": ObjectId("..."),
      "evaluatorId": "usr456",
      "evaluatedId": "usr789",
      "submittedAt": ISODate("2025-08-03"),
      "answers": {
        "q1": 4,
        "q2": ["JavaScript", "React", "Node.js"]
      },
      "comments": "Excelente instructor con amplio conocimiento"
    }
  ],
  "settings": {
    "allowAnonymous": false,
    "multipleSubmissions": false,
    "deadline": ISODate("2025-12-31")
  }
}
```

### RF-MONGO-004: Audit Logging System

**Descripción**: Sistema de auditoría y logging usando MongoDB para alta performance.

**Criterios de Aceptación**:

- [ ] Colección `audit_logs` con TTL automático
- [ ] Logging de todas las operaciones críticas
- [ ] Búsqueda y filtrado eficiente
- [ ] Dashboards de monitoreo
- [ ] Alertas automáticas

**Estructura de Log Ejemplo**:

```json
{
  "_id": ObjectId("..."),
  "timestamp": ISODate("2025-08-03T10:30:00Z"),
  "level": "INFO",
  "service": "userservice",
  "action": "user_login",
  "userId": "usr123",
  "sessionId": "sess456",
  "details": {
    "ip": "192.168.1.100",
    "userAgent": "Mozilla/5.0...",
    "success": true,
    "method": "password"
  },
  "context": {
    "requestId": "req789",
    "correlationId": "corr101",
    "traceId": "trace202"
  },
  "metadata": {
    "geolocation": {
      "country": "CO",
      "city": "Bogotá"
    },
    "device": "desktop"
  }
}
```

### RF-MONGO-005: Notification System

**Descripción**: Sistema de notificaciones flexible con MongoDB.

**Criterios de Aceptación**:

- [ ] Colección `notifications` con estados
- [ ] Templates dinámicos
- [ ] Configuraciones de usuario personalizables
- [ ] Queue de envío eficiente
- [ ] Historial de entregas

## 🔧 Requisitos Técnicos

### Conectividad

- **Go**: Driver oficial `go.mongodb.org/mongo-driver`
- **Python**: PyMongo con AsyncIO
- **Node.js**: Driver nativo de MongoDB
- **Java**: MongoDB Java Driver
- **Kotlin**: Driver con corrutinas

### Configuración de Desarrollo

```yaml
# docker-compose.yml
mongodb:
  image: mongo:8.0-community
  container_name: sicora-mongodb
  ports:
    - '27017:27017'
  environment:
    MONGO_INITDB_ROOT_USERNAME: sicora_admin
    MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
    MONGO_INITDB_DATABASE: sicora_nosql
  volumes:
    - mongodb_data:/data/db
    - ./mongodb/init:/docker-entrypoint-initdb.d
```

### Índices Requeridos

```javascript
// Articles Collection
db.articles.createIndex({ title: 'text', content: 'text' });
db.articles.createIndex({ slug: 1 }, { unique: true });
db.articles.createIndex({ 'metadata.category': 1 });
db.articles.createIndex({ 'metadata.tags': 1 });
db.articles.createIndex({ 'author.id': 1 });
db.articles.createIndex({ createdAt: -1 });

// Evaluations Collection
db.evaluations.createIndex({ type: 1, version: 1 });
db.evaluations.createIndex({ 'responses.evaluatedId': 1 });
db.evaluations.createIndex({ 'responses.submittedAt': -1 });

// Audit Logs Collection
db.audit_logs.createIndex({ timestamp: -1 });
db.audit_logs.createIndex({ service: 1, action: 1 });
db.audit_logs.createIndex({ userId: 1 });
db.audit_logs.createIndex({ level: 1 });

// TTL Index for logs (30 days retention)
db.audit_logs.createIndex({ timestamp: 1 }, { expireAfterSeconds: 2592000 });
```

## 📊 Comparativa Educativa: PostgreSQL vs MongoDB

### Casos de Uso PostgreSQL

| Característica | PostgreSQL | Justificación                           |
| -------------- | ---------- | --------------------------------------- |
| **Users**      | ✅         | Relaciones complejas, ACID transactions |
| **Schedules**  | ✅         | Datos estructurados, consultas JOIN     |
| **Attendance** | ✅         | Integridad referencial crítica          |
| **Projects**   | ✅         | Relaciones many-to-many complejas       |

### Casos de Uso MongoDB

| Característica    | MongoDB | Justificación                            |
| ----------------- | ------- | ---------------------------------------- |
| **Articles**      | ✅      | Contenido variable, metadatos flexibles  |
| **Evaluations**   | ✅      | Esquemas dinámicos, estructuras anidadas |
| **Logs**          | ✅      | Alta velocidad escritura, TTL automático |
| **Notifications** | ✅      | Templates flexibles, escalabilidad       |

## 🚀 Fases de Implementación

### Fase 1: Infraestructura Base (Semana 1)

- [ ] Configuración Docker Compose
- [ ] Instalación MongoDB Community
- [ ] Configuración de usuarios y permisos
- [ ] Testing de conectividad básica

### Fase 2: Knowledge Base Migration (Semana 2-3)

- [ ] Diseño de esquemas de documentos
- [ ] Implementación de APIs CRUD
- [ ] Migración de datos existentes
- [ ] Implementación de búsqueda full-text

### Fase 3: Dynamic Evaluations (Semana 4-5)

- [ ] Diseño de evaluaciones flexibles
- [ ] Implementación de validaciones
- [ ] APIs para formularios dinámicos
- [ ] Sistema de reportes con agregaciones

### Fase 4: Logging & Monitoring (Semana 6)

- [ ] Sistema de audit logs
- [ ] Configuración de TTL
- [ ] Dashboards de monitoreo
- [ ] Alertas automáticas

### Fase 5: Notification System (Semana 7-8)

- [ ] Sistema de notificaciones
- [ ] Templates dinámicos
- [ ] Queue de procesamiento
- [ ] Configuraciones de usuario

## 📈 Métricas y Monitoreo

### KPIs de Performance

- **Latencia de escritura**: < 50ms (MongoDB) vs < 100ms (PostgreSQL)
- **Throughput de lecturas**: Comparativa entre bases de datos
- **Uso de memoria**: Impacto de cada base de datos
- **Tiempo de consultas complejas**: Agregaciones vs JOINs

### Métricas de Aprendizaje

- **Complejidad de desarrollo**: Tiempo de implementación
- **Facilidad de mantenimiento**: Esfuerzo de administración
- **Escalabilidad**: Comportamiento bajo carga
- **Flexibilidad**: Facilidad para cambios de esquema

## 🔒 Seguridad y Backup

### Configuración de Seguridad

- [ ] Autenticación SCRAM-SHA-256
- [ ] Autorización basada en roles
- [ ] Encriptación en tránsito (TLS)
- [ ] Auditoría de operaciones sensibles

### Estrategia de Backup

- [ ] Backup automático diario con mongodump
- [ ] Replica sets para alta disponibilidad
- [ ] Backup incremental con oplog
- [ ] Testing de recuperación mensual

## 📚 Documentación y Training

### Material de Aprendizaje

- [ ] Guía de migración SQL → NoSQL
- [ ] Comparativas de performance
- [ ] Best practices para modelado
- [ ] Troubleshooting guide

### Casos de Estudio

- [ ] Migración de Knowledge Base
- [ ] Implementación de evaluaciones dinámicas
- [ ] Optimización de consultas
- [ ] Escalabilidad horizontal

---

## ✅ Checklist de Implementación

### Pre-requisitos

- [ ] Docker y Docker Compose configurados
- [ ] MongoDB Community Edition disponible
- [ ] Drivers para todos los lenguajes instalados
- [ ] Variables de entorno configuradas

### Desarrollo

- [ ] Esquemas de documentos definidos
- [ ] APIs REST implementadas
- [ ] Testing de integración completado
- [ ] Documentación técnica actualizada

### Producción

- [ ] Configuración de seguridad aplicada
- [ ] Backup strategy implementada
- [ ] Monitoreo configurado
- [ ] Performance testing completado

---

**Nota**: Este documento forma parte del proyecto educativo SICORA y debe actualizarse conforme se implementen las funcionalidades descritas. La integración de MongoDB busca ampliar el conocimiento sobre tecnologías de bases de datos y arquitecturas híbridas.
