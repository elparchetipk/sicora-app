# Estrategia de Bases de Datos - Backend Multi-Stack

**Actualizado: 15 de junio de 2025**

## 🎯 **Objetivos de la Estrategia**

Esta estrategia de bases de datos está diseñada específicamente para un proyecto educativo que implementa 6 tecnologías backend diferentes (FastAPI, Go, Express.js, Next.js, Spring Boot Java, Spring Boot Kotlin) para el mismo conjunto de microservicios.

### **Principios Fundamentales**

1. **Comparabilidad Cross-Stack**: Permitir a estudiantes comparar cómo diferentes tecnologías manejan los mismos datos
2. **Realismo Arquitectónico**: Mantener los principios de microservicios (una BD por servicio)
3. **Diversidad Tecnológica**: Mostrar diferentes tipos de bases de datos según el caso de uso
4. **Mantenibilidad**: Evitar N×6 bases de datos (una por stack×servicio)

## 🏗️ **Arquitectura de Datos**

### **Regla Central: Una Base de Datos por Microservicio (Compartida entre Stacks)**

```
UserService (6 stacks) ──→ user_db (PostgreSQL)
AttendanceService (6 stacks) ──→ attendance_db (PostgreSQL)
ScheduleService (6 stacks) ──→ schedule_db (PostgreSQL)
KbService (6 stacks) ──→ kb_db (PostgreSQL/MongoDB híbrido)
EvalinService (6 stacks) ──→ evalin_db (PostgreSQL)
AIService (6 stacks) ──→ ai_db (PostgreSQL + Vector DB)
```

### **Ventajas del Enfoque**

#### **Para Estudiantes**

- **Comparación directa**: Ver cómo FastAPI vs Go vs Express.js manejan el mismo esquema
- **Foco en la lógica**: Concentrarse en ORMs, migraciones, y lógica de negocio
- **Coherencia de datos**: Mismos datos para todas las demostraciones

#### **Para Desarrollo**

- **Gestión simplificada**: 6 bases de datos en lugar de 36 (6×6)
- **Migraciones unificadas**: Un solo esquema por microservicio
- **Testing consistente**: Mismos datos de prueba para todos los stacks

#### **Para Producción**

- **Escalabilidad independiente**: Cada servicio puede escalar su BD independientemente
- **Tecnología apropiada**: Elegir la BD óptima por caso de uso, no por stack

## 🗄️ **Especificación por Microservicio**

### **UserService - PostgreSQL**

```sql
Database: user_db
Tables: users, roles, permissions, user_roles, sessions
Indices: email (unique), document_number (unique)
Cache: Redis (sessions, user profiles)
```

**Justificación**: Datos estructurados, ACID crítico para autenticación, relaciones complejas de roles.

### **AttendanceService - PostgreSQL**

```sql
Database: attendance_db
Tables: attendance_records, justifications, attendance_periods
Indices: user_id, date, schedule_id
Cache: Redis (resúmenes diarios, métricas)
```

**Justificación**: Integridad transaccional para registros de asistencia, reportes que requieren agregaciones complejas.

### **ScheduleService - PostgreSQL**

```sql
Database: schedule_db
Tables: schedules, groups, venues, schedule_assignments
Indices: user_id, group_id, date_range, venue_id
Cache: Redis (horarios activos, calendarios)
```

**Justificación**: Relaciones complejas entre horarios, grupos y usuarios. Restricciones de integridad críticas.

### **KbService - Híbrido PostgreSQL + MongoDB**

#### **Fase 1 (Actual) - PostgreSQL**

```sql
Database: kb_db
Tables: articles, categories, faqs, feedback, embeddings
Extensions: pgvector (búsquedas vectoriales)
Cache: Redis (búsquedas frecuentes, artículos populares)
```

#### **Fase 2 (Planificada) - Híbrido**

```javascript
// MongoDB: Contenido flexible
kb_content_db(MongoDB);
Collections: (articles, documents, multimedia_content);

// PostgreSQL: Estructura y relaciones
kb_structure_db(PostgreSQL);
Tables: (categories, tags, user_feedback, search_analytics);
```

**Justificación**: El contenido del knowledge base es variable (texto, multimedia, documentos), pero las relaciones y métricas requieren estructura.

### **EvalinService - PostgreSQL**

```sql
Database: evalin_db
Tables: questions, questionnaires, evaluation_periods, evaluations, responses
Indices: period_id, instructor_id, student_id
Cache: Redis (reportes activos, métricas en tiempo real)
```

**Justificación**: Formularios estructurados, reportes complejos, análisis estadístico que requiere agregaciones SQL.

### **AIService - PostgreSQL + Vector Database**

```sql
Database: ai_db (PostgreSQL)
Tables: conversations, chat_sessions, training_data, model_configs

Vector Storage: Pinecone/Weaviate (Fase futura)
Data: embeddings, vector searches, similarity indices
```

**Justificación**: Metadatos relacionales + almacenamiento especializado para vectores de alta dimensión.

## 🔄 **Roadmap de Evolución**

### **Fase 1: PostgreSQL + Redis (Actual)**

- **Estado**: ✅ Implementado
- **Tecnologías**: PostgreSQL 15, Redis 7, pgvector
- **Servicios**: Todos los servicios funcionando

### **Fase 2: Incorporación NoSQL (6 meses)**

- **MongoDB para KbService**: Contenido documental flexible
- **Elasticsearch**: Búsquedas avanzadas y analytics (opcional)
- **Objetivo**: Mostrar casos híbridos SQL/NoSQL

### **Fase 3: Bases de Datos Especializadas (12 meses)**

- **Neo4j**: Análisis de relaciones académicas complejas
  - Estudiante → Instructor → Programa → Competencia
  - Patrones de asistencia en redes
  - Recomendaciones basadas en grafos
- **Vector Database dedicada**: Pinecone/Weaviate para IA avanzada

### **Fase 4: Casos de Uso Avanzados (18 meses)**

- **Time Series Database**: InfluxDB para métricas temporales
- **Distributed SQL**: CockroachDB para geo-distribución
- **Event Store**: Para Event Sourcing y CQRS

## 🛠️ **Configuración de Desarrollo**

### **Docker Compose - Servicios de Base de Datos**

```yaml
version: '3.8'
services:
  # PostgreSQL instances per microservice
  user-db:
    image: postgres:15
    environment:
      POSTGRES_DB: user_db
    volumes:
      - user_data:/var/lib/postgresql/data

  attendance-db:
    image: postgres:15
    environment:
      POSTGRES_DB: attendance_db
    volumes:
      - attendance_data:/var/lib/postgresql/data

  # Shared services
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  # Future: MongoDB for KbService
  # mongodb:
  #   image: mongo:7
  #   volumes:
  #     - mongo_data:/data/db
```

### **Migraciones Cross-Stack**

Cada stack implementará migraciones compatibles:

- **Alembic** (Python/FastAPI)
- **golang-migrate** (Go)
- **TypeORM** (Node.js/Express)
- **Entity Framework** (C#)
- **Flyway** (Java/Kotlin)

## 📋 **Casos de Uso Educativos**

### **Comparación de ORMs**

Estudiantes pueden ver cómo el mismo esquema se maneja en:

- **SQLAlchemy** (Python)
- **GORM** (Go)
- **TypeORM** (TypeScript)
- **Entity Framework** (C#)
- **JPA/Hibernate** (Java/Kotlin)

### **Estrategias de Caché**

Comparar implementaciones de Redis cache en diferentes tecnologías:

- Cache-aside, Write-through, Write-behind
- TTL strategies, invalidation patterns
- Distributed locking

### **Performance y Optimización**

- Query optimization por tecnología
- Connection pooling strategies
- N+1 problem solutions
- Bulk operations efficiency

## 🚀 **Plan de Implementación**

### **Paso 1: Consolidar PostgreSQL (Actual)**

- [x] Verificar esquemas consistentes entre servicios
- [x] Configurar pgvector para KbService
- [x] Implementar Redis cache común

### **Paso 2: Documentar Estrategias de Acceso**

- [ ] Crear guías de ORM por stack
- [ ] Documentar patrones de cache por servicio
- [ ] Establecer convenciones de nombrado

### **Paso 3: Preparar Migración NoSQL**

- [ ] Identificar datos candidatos para MongoDB en KbService
- [ ] Diseñar esquema híbrido PostgreSQL/MongoDB
- [ ] Crear scripts de migración incremental

### **Paso 4: Implementar Monitoreo**

- [ ] Métricas de performance por stack
- [ ] Alertas de consistencia de datos
- [ ] Dashboards de uso por tecnología

Esta estrategia asegura que el proyecto educativo mantenga valor pedagógico mientras demuestra prácticas reales de arquitectura de bases de datos en microservicios.
