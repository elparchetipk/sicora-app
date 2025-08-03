# 🍃 **HISTORIAS DE USUARIO Y CRITERIOS - INTEGRACIÓN MONGODB**

**Microservicio:** Integración MongoDB NoSQL
**Fecha:** 3 de agosto de 2025
**Versión:** 1.0
**Estado:** 📋 Planificación inicial

---

## 📋 **DOCUMENTACIÓN DE REFERENCIA**

- **[RF MongoDB Integration](../../general/rf_mongodb_integration.md)**: Requisitos funcionales específicos
- **[Especificación de Endpoints API](../../api/endpoints_specification.md)**: Contratos técnicos
- **[Estado del Proyecto](../../reports/ESTADO-ACTUAL-PROYECTO-CONSOLIDADO.md)**: Progreso actual

---

## 🎯 **ALINEACIÓN CON REQUISITOS FUNCIONALES**

Este documento implementa las historias de usuario correspondientes a los siguientes RF:

- **RF-MONGO-001**: Configuración Base
- **RF-MONGO-002**: Knowledge Base Documents
- **RF-MONGO-003**: Dynamic Evaluations
- **RF-MONGO-004**: Audit Logging System
- **RF-MONGO-005**: Notification System

---

## 📊 **PROGRESO POR CATEGORÍA**

| Categoría               | Historias | Completadas | Progreso |
| ----------------------- | --------- | ----------- | -------- |
| **Infraestructura**     | 2         | 0           | 0%       |
| **Knowledge Base**      | 3         | 0           | 0%       |
| **Evaluaciones**        | 2         | 0           | 0%       |
| **Logging & Auditoría** | 2         | 0           | 0%       |
| **Notificaciones**      | 2         | 0           | 0%       |

---

## 🏗️ **ÉPICA: INFRAESTRUCTURA MONGODB**

### **HU-MONGO-001: Configuración Inicial de MongoDB**

**Historia:**

- **Como** DevOps/Desarrollador
- **Quiero** configurar MongoDB 8.x en el entorno de desarrollo
- **Para** tener disponible la base de datos NoSQL para el proyecto educativo

**Criterios de Aceptación:**

#### **AC-MONGO-001.1: Instalación Base**

- MongoDB 8.x Community Edition ejecutándose en Docker
- Container `sicora-mongodb` configurado en puerto 27017
- Base de datos `sicora_nosql` creada e inicializada
- Usuarios y permisos configurados según mejores prácticas
- Variables de entorno para configuración segura

#### **AC-MONGO-001.2: Docker Compose Integration**

```yaml
# Configuración mínima requerida
mongodb:
  image: mongo:8.0-community
  container_name: sicora-mongodb
  environment:
    MONGO_INITDB_ROOT_USERNAME: sicora_admin
    MONGO_INITDB_DATABASE: sicora_nosql
  ports:
    - '27017:27017'
  volumes:
    - mongodb_data:/data/db
```

#### **AC-MONGO-001.3: Conectividad Multi-Stack**

- Conexión exitosa desde servicios Go
- Conexión exitosa desde servicios Python (FastAPI)
- Conexión exitosa desde servicios Node.js
- Conexión exitosa desde servicios Java Spring Boot
- Conexión exitosa desde servicios Kotlin Spring Boot

#### **AC-MONGO-001.4: Validación de Estado**

- Health check endpoint que verifique conectividad
- Logs de conexión sin errores
- Métricas básicas de performance disponibles
- Testing de conexión automatizado en CI/CD

**Prioridad:** 🔴 Alta
**Estimación:** 3 story points
**Stack:** Docker, MongoDB, Multi-backend

---

### **HU-MONGO-002: Configuración de Drivers y Conexiones**

**Historia:**

- **Como** Desarrollador Backend
- **Quiero** tener drivers MongoDB configurados en todos los stacks
- **Para** poder implementar funcionalidades NoSQL en cada microservicio

**Criterios de Aceptación:**

#### **AC-MONGO-002.1: Driver Go Configuration**

```go
// Configuración mínima requerida
client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
database := client.Database("sicora_nosql")
collection := database.Collection("articles")
```

- Driver `go.mongodb.org/mongo-driver` instalado
- Connection pool configurado para alta concurrencia
- Context management para operaciones async
- Error handling robusto implementado

#### **AC-MONGO-002.2: Driver Python Configuration**

```python
# Configuración mínima requerida
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient(mongo_uri)
db = client.sicora_nosql
collection = db.articles
```

- Motor driver para AsyncIO configurado
- Pydantic models para validación de documentos
- Connection pooling optimizado
- Logging de operaciones implementado

#### **AC-MONGO-002.3: Driver Node.js Configuration**

```javascript
// Configuración mínima requerida
const { MongoClient } = require('mongodb');
const client = new MongoClient(mongoUri);
const db = client.db('sicora_nosql');
const collection = db.collection('articles');
```

- Driver nativo MongoDB configurado
- Mongoose ODM setup alternativo
- Error handling con retry logic
- Performance monitoring habilitado

#### **AC-MONGO-002.4: Driver Java/Kotlin Configuration**

```kotlin
// Configuración mínima requerida
val client = MongoClients.create(mongoUri)
val database = client.getDatabase("sicora_nosql")
val collection = database.getCollection("articles")
```

- Driver oficial MongoDB configurado
- Spring Data MongoDB integrado
- Reactive streams support
- Health indicators configurados

**Prioridad:** 🔴 Alta
**Estimación:** 5 story points
**Stack:** Go, Python, Node.js, Java, Kotlin

---

## 📚 **ÉPICA: KNOWLEDGE BASE NOSQL**

### **HU-MONGO-003: Migración de Artículos a MongoDB**

**Historia:**

- **Como** Desarrollador del KbService
- **Quiero** migrar el sistema de artículos desde PostgreSQL a MongoDB
- **Para** aprovechar la flexibilidad de esquemas para contenido dinámico

**Criterios de Aceptación:**

#### **AC-MONGO-003.1: Diseño de Schema Flexible**

```json
{
  "_id": ObjectId("..."),
  "title": "Guía de Desarrollo React",
  "slug": "guia-desarrollo-react",
  "content": {
    "markdown": "# Contenido...",
    "html": "<h1>Contenido...</h1>",
    "blocks": [...]
  },
  "metadata": {
    "category": "frontend",
    "tags": ["react", "javascript"],
    "difficulty": "intermediate",
    "customFields": {}
  },
  "author": {
    "id": "usr123",
    "name": "Juan Pérez"
  },
  "versions": [...],
  "stats": {
    "views": 245,
    "likes": 18
  }
}
```

- Esquema de documento flexible definido
- Versionado de contenido implementado
- Metadatos extensibles configurados
- Validación básica de estructura

#### **AC-MONGO-003.2: APIs CRUD MongoDB**

- `POST /api/v1/kb/articles` - Crear artículo en MongoDB
- `GET /api/v1/kb/articles/{id}` - Obtener artículo por ID
- `PUT /api/v1/kb/articles/{id}` - Actualizar artículo
- `DELETE /api/v1/kb/articles/{id}` - Soft delete
- `GET /api/v1/kb/articles/search` - Búsqueda full-text

#### **AC-MONGO-003.3: Migración de Datos**

- Script de migración desde PostgreSQL
- Validación de integridad post-migración
- Rollback strategy en caso de problemas
- Comparación de performance pre/post migración

#### **AC-MONGO-003.4: Indexación Optimizada**

```javascript
// Índices requeridos
db.articles.createIndex({ title: 'text', 'content.markdown': 'text' });
db.articles.createIndex({ slug: 1 }, { unique: true });
db.articles.createIndex({ 'metadata.category': 1 });
db.articles.createIndex({ 'metadata.tags': 1 });
```

**Prioridad:** 🟡 Media
**Estimación:** 8 story points
**Stack:** KbService (Go/Python/Node.js)

---

### **HU-MONGO-004: Sistema de Búsqueda Full-Text**

**Historia:**

- **Como** Usuario del sistema
- **Quiero** buscar artículos mediante texto libre en MongoDB
- **Para** encontrar rápidamente información relevante

**Criterios de Aceptación:**

#### **AC-MONGO-004.1: Búsqueda Básica**

- Búsqueda por título y contenido
- Soporte para operadores booleanos
- Ranking por relevancia
- Paginación de resultados

#### **AC-MONGO-004.2: Filtros Avanzados**

- Filtro por categoría
- Filtro por tags múltiples
- Filtro por autor
- Filtro por fecha de creación
- Filtro por dificultad

#### **AC-MONGO-004.3: Agregaciones de Metadata**

```javascript
// Pipeline de agregación ejemplo
[
  { $match: { $text: { $search: 'react' } } },
  {
    $group: {
      _id: '$metadata.category',
      count: { $sum: 1 },
    },
  },
  { $sort: { count: -1 } },
];
```

#### **AC-MONGO-004.4: Performance Optimization**

- Tiempo de respuesta < 200ms para búsquedas
- Índices optimizados para queries frecuentes
- Cache de resultados para búsquedas populares
- Monitoring de performance de queries

**Prioridad:** 🟡 Media
**Estimación:** 5 story points
**Stack:** Backend + Frontend

---

### **HU-MONGO-005: Versionado de Documentos**

**Historia:**

- **Como** Editor de contenido
- **Quiero** mantener versiones históricas de artículos en MongoDB
- **Para** poder revertir cambios y auditar modificaciones

**Criterios de Aceptación:**

#### **AC-MONGO-005.1: Sistema de Versiones**

```json
{
  "versions": [
    {
      "version": "1.0",
      "createdAt": ISODate("2025-08-03"),
      "author": "usr123",
      "changes": "Versión inicial",
      "contentSnapshot": {...}
    }
  ]
}
```

- Snapshot completo de cada versión
- Metadata de cambios
- Comparación entre versiones
- Restauración a versión anterior

#### **AC-MONGO-005.2: APIs de Versionado**

- `GET /api/v1/kb/articles/{id}/versions` - Listar versiones
- `GET /api/v1/kb/articles/{id}/versions/{version}` - Obtener versión específica
- `POST /api/v1/kb/articles/{id}/revert/{version}` - Revertir a versión
- `GET /api/v1/kb/articles/{id}/diff/{v1}/{v2}` - Comparar versiones

**Prioridad:** 🟢 Baja
**Estimación:** 3 story points
**Stack:** Backend + Frontend

---

## 📝 **ÉPICA: EVALUACIONES DINÁMICAS**

### **HU-MONGO-006: Formularios de Evaluación Flexibles**

**Historia:**

- **Como** Coordinador Académico
- **Quiero** crear evaluaciones con estructura dinámica en MongoDB
- **Para** adaptar los formularios según diferentes tipos de evaluación

**Criterios de Aceptación:**

#### **AC-MONGO-006.1: Schema Dinámico**

```json
{
  "title": "Evaluación de Instructor",
  "type": "instructor_evaluation",
  "sections": [
    {
      "id": "technical_skills",
      "title": "Habilidades Técnicas",
      "questions": [
        {
          "id": "q1",
          "type": "rating",
          "question": "Dominio técnico",
          "scale": { "min": 1, "max": 5 }
        }
      ]
    }
  ]
}
```

- Soporte para diferentes tipos de preguntas
- Validaciones dinámicas configurables
- Secciones anidadas
- Lógica condicional entre preguntas

#### **AC-MONGO-006.2: Recolección de Respuestas**

- Almacenamiento de respuestas estructuradas
- Validación en tiempo real
- Progreso de evaluación
- Múltiples submisiones configurables

#### **AC-MONGO-006.3: Reportes y Agregaciones**

```javascript
// Pipeline para reportes
[
  { $match: { type: 'instructor_evaluation' } },
  { $unwind: '$responses' },
  {
    $group: {
      _id: '$responses.evaluatedId',
      avgRating: { $avg: '$responses.answers.q1' },
    },
  },
];
```

**Prioridad:** 🟡 Media
**Estimación:** 8 story points
**Stack:** EvalinService

---

### **HU-MONGO-007: Analytics de Evaluaciones**

**Historia:**

- **Como** Administrador del sistema
- **Quiero** generar analytics de evaluaciones usando agregaciones MongoDB
- **Para** obtener insights sobre el rendimiento académico

**Criterios de Aceptación:**

#### **AC-MONGO-007.1: Métricas Básicas**

- Promedio de calificaciones por instructor
- Distribución de respuestas por pregunta
- Tendencias temporales de evaluaciones
- Comparativas entre programas de formación

#### **AC-MONGO-007.2: Dashboards Dinámicos**

- Filtros interactivos por fecha, programa, instructor
- Gráficos generados desde agregaciones MongoDB
- Exportación de reportes en PDF/Excel
- Alertas automáticas por umbrales

**Prioridad:** 🟢 Baja
**Estimación:** 5 story points
**Stack:** Backend + Frontend

---

## 📊 **ÉPICA: LOGGING Y AUDITORÍA**

### **HU-MONGO-008: Sistema de Audit Logs**

**Historia:**

- **Como** Administrador de seguridad
- **Quiero** almacenar logs de auditoría en MongoDB
- **Para** tener trazabilidad completa de operaciones críticas

**Criterios de Aceptación:**

#### **AC-MONGO-008.1: Estructura de Logs**

```json
{
  "timestamp": ISODate("2025-08-03T10:30:00Z"),
  "level": "INFO",
  "service": "userservice",
  "action": "user_login",
  "userId": "usr123",
  "details": {
    "ip": "192.168.1.100",
    "success": true
  },
  "context": {
    "requestId": "req789",
    "correlationId": "corr101"
  }
}
```

- Logging de todas las operaciones CRUD
- Metadata contextual completa
- Correlación entre requests
- TTL automático (30 días)

#### **AC-MONGO-008.2: Performance de Escritura**

- Throughput mínimo: 10,000 logs/segundo
- Latencia máxima: 50ms por operación
- Batch writing para optimización
- Buffer automático en memoria

#### **AC-MONGO-008.3: Consultas de Auditoría**

- Búsqueda por usuario, acción, fecha
- Filtros por nivel de severity
- Exportación de logs para compliance
- Alertas automáticas por patrones sospechosos

**Prioridad:** 🟡 Media
**Estimación:** 6 story points
**Stack:** Todos los servicios

---

### **HU-MONGO-009: Monitoring y Alertas**

**Historia:**

- **Como** DevOps Engineer
- **Quiero** monitorear el comportamiento de MongoDB en tiempo real
- **Para** detectar problemas de performance y disponibilidad

**Criterios de Aceptación:**

#### **AC-MONGO-009.1: Métricas de Performance**

- Latencia promedio de queries
- Throughput de operaciones read/write
- Uso de memoria y CPU
- Tamaño de collections y índices

#### **AC-MONGO-009.2: Alertas Automáticas**

- Latencia > 1000ms sostenida
- Fallos de conexión > 5%
- Uso de memoria > 80%
- Queries lentas > 5 segundos

**Prioridad:** 🟢 Baja
**Estimación:** 4 story points
**Stack:** DevOps + Monitoring

---

## 🔔 **ÉPICA: SISTEMA DE NOTIFICACIONES**

### **HU-MONGO-010: Notificaciones Flexibles**

**Historia:**

- **Como** Usuario del sistema
- **Quiero** recibir notificaciones personalizadas almacenadas en MongoDB
- **Para** estar informado de eventos relevantes con contenido dinámico

**Criterios de Aceptación:**

#### **AC-MONGO-010.1: Schema de Notificaciones**

```json
{
  "userId": "usr123",
  "type": "evaluation_reminder",
  "title": "Evaluación Pendiente",
  "content": {
    "template": "evaluation_reminder",
    "variables": {
      "instructorName": "Juan Pérez",
      "deadline": "2025-08-10"
    }
  },
  "status": "pending",
  "channels": ["email", "push", "in-app"],
  "createdAt": ISODate("2025-08-03"),
  "scheduledFor": ISODate("2025-08-05")
}
```

- Templates dinámicos de contenido
- Múltiples canales de entrega
- Programación de envío
- Estados de entrega tracking

#### **AC-MONGO-010.2: Sistema de Templates**

- Templates reutilizables por tipo
- Variables dinámicas inyectables
- Localización multi-idioma
- Versionado de templates

#### **AC-MONGO-010.3: Queue de Procesamiento**

- Cola FIFO para procesamiento
- Retry automático en fallos
- Dead letter queue para errores
- Monitoring de throughput

**Prioridad:** 🟢 Baja
**Estimación:** 7 story points
**Stack:** Nuevo NotificationService

---

### **HU-MONGO-011: Configuraciones de Usuario**

**Historia:**

- **Como** Usuario
- **Quiero** configurar mis preferencias de notificaciones
- **Para** recibir solo información relevante en mis canales preferidos

**Criterios de Aceptación:**

#### **AC-MONGO-011.1: Preferencias Flexibles**

```json
{
  "userId": "usr123",
  "preferences": {
    "evaluations": {
      "enabled": true,
      "channels": ["email", "push"],
      "frequency": "immediate"
    },
    "system_updates": {
      "enabled": false
    },
    "custom_rules": [
      {
        "condition": "priority = high",
        "action": "force_all_channels"
      }
    ]
  }
}
```

- Configuración granular por tipo
- Reglas personalizadas
- Horarios de entrega
- Blacklist/whitelist de remitentes

**Prioridad:** 🟢 Baja
**Estimación:** 4 story points
**Stack:** Backend + Frontend

---

## 🧪 **ÉPICA: TESTING Y VALIDACIÓN**

### **HU-MONGO-012: Testing de Integración**

**Historia:**

- **Como** Desarrollador
- **Quiero** tener tests automatizados para todas las operaciones MongoDB
- **Para** garantizar la calidad y estabilidad de la integración NoSQL

**Criterios de Aceptación:**

#### **AC-MONGO-012.1: Unit Tests**

- Tests para cada operación CRUD
- Mocking de conexiones MongoDB
- Validación de schemas de documentos
- Coverage mínimo del 80%

#### **AC-MONGO-012.2: Integration Tests**

- Tests end-to-end con MongoDB real
- Validación de performance
- Tests de concurrencia
- Tests de failover y recovery

#### **AC-MONGO-012.3: Performance Tests**

- Load testing con datos realistas
- Stress testing de throughput
- Memory leak detection
- Benchmark vs PostgreSQL

**Prioridad:** 🔴 Alta
**Estimación:** 6 story points
**Stack:** Testing Framework

---

## 📋 **CHECKLIST DE IMPLEMENTACIÓN**

### **Fase 1: Infraestructura (Semana 1)**

- [ ] HU-MONGO-001: Configuración inicial MongoDB
- [ ] HU-MONGO-002: Drivers y conexiones
- [ ] HU-MONGO-012: Testing básico

### **Fase 2: Knowledge Base (Semana 2-3)**

- [ ] HU-MONGO-003: Migración de artículos
- [ ] HU-MONGO-004: Búsqueda full-text
- [ ] HU-MONGO-005: Versionado

### **Fase 3: Evaluaciones (Semana 4-5)**

- [ ] HU-MONGO-006: Formularios dinámicos
- [ ] HU-MONGO-007: Analytics

### **Fase 4: Logging (Semana 6)**

- [ ] HU-MONGO-008: Audit logs
- [ ] HU-MONGO-009: Monitoring

### **Fase 5: Notificaciones (Semana 7-8)**

- [ ] HU-MONGO-010: Sistema de notificaciones
- [ ] HU-MONGO-011: Configuraciones de usuario

---

## 📊 **MÉTRICAS DE ÉXITO**

### **Performance Targets**

- Latencia promedio < 100ms para queries simples
- Throughput > 1000 ops/segundo
- Availability > 99.9%
- Tiempo de startup < 30 segundos

### **Learning Objectives**

- Comparación práctica SQL vs NoSQL
- Entendimiento de agregaciones MongoDB
- Experiencia con múltiples drivers
- Conocimiento de best practices NoSQL

---

**Nota:** Estas historias de usuario forman parte del proyecto educativo SICORA y deben implementarse siguiendo las mejores prácticas de desarrollo ágil y clean architecture.
