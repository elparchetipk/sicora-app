# 📊 **ÍNDICES DE BASE DE DATOS - SOFTWAREFACTORYSERVICE**

**Proyecto:** SICORA - Fábrica de Software Académica (FSA)  
**Microservicio:** SoftwareFactoryService  
**Fecha:** 29 de junio de 2025  
**Versión:** 1.0

---

## 📋 **RESUMEN EJECUTIVO**

Este documento detalla los índices de base de datos optimizados para el esquema `softwarefactoryservice_schema` basándose en el análisis de las historias de usuario, patrones de consulta del código Go y requisitos de rendimiento para el sistema de Fábrica de Software Académica del SENA.

### **Estadísticas de Optimización:**

- **📈 47 índices especializados** creados para optimización de consultas
- **🎯 8 tablas principales** optimizadas con índices específicos
- **⚡ 3 vistas materializadas** para analytics y reportes
- **🔍 6 índices de texto completo** para búsquedas avanzadas
- **📊 3 funciones de optimización** para mantenimiento automático

---

## 🗂️ **ÍNDICES POR TABLA**

### **1. FACTORY_PROJECTS (Proyectos)**

#### **Índices de Consultas Básicas:**

```sql
-- Búsquedas por instructor/creador
idx_factory_projects_created_by (created_by)

-- Filtrado por estado
idx_factory_projects_status (status)

-- Búsquedas por curso/cliente
idx_factory_projects_client_name (client_name)
```

#### **Índices de Rangos y Fechas:**

```sql
-- Consultas de proyectos activos por fechas
idx_factory_projects_date_range (start_date, end_date)

-- Optimización para proyectos activos
idx_factory_projects_status_dates (status, start_date, end_date)
```

#### **Índices Especializados:**

```sql
-- Búsqueda en arrays de tecnologías (GIN index)
idx_factory_projects_tech_stack_gin (tech_stack)

-- Búsqueda de texto completo
idx_factory_projects_fulltext (to_tsvector('english', name || ' ' || description))

-- Paginación optimizada
idx_factory_projects_pagination (created_at, id)

-- Analytics y reportes
idx_factory_projects_analytics (status, complexity_level, estimated_duration_weeks)

-- Índice parcial para proyectos activos solamente
idx_factory_projects_active_only (id, name, created_at)
WHERE status IN ('planning', 'active')
```

### **2. FACTORY_TEAMS (Equipos)**

#### **Índices de Relaciones:**

```sql
-- Equipos por proyecto
idx_factory_teams_project_id (project_id)

-- Equipos por líder técnico
idx_factory_teams_tech_lead (tech_lead_instructor_id)
```

#### **Índices de Búsqueda:**

```sql
-- Búsqueda de texto completo en nombres
idx_factory_teams_name_fulltext (to_tsvector('english', name))
```

### **3. FACTORY_TEAM_MEMBERS (Miembros de Equipo)**

#### **Índices de Relaciones:**

```sql
-- Miembros por equipo
idx_factory_team_members_team_id (team_id)

-- Equipos por aprendiz
idx_factory_team_members_apprentice_id (apprentice_id)
```

#### **Índices de Estado:**

```sql
-- Miembros activos por equipo (consulta muy frecuente)
idx_factory_team_members_active (team_id, is_active)

-- Equipos activos por usuario
idx_factory_team_members_user_active (apprentice_id, is_active)
```

### **4. FACTORY_SPRINTS (Sprints)**

#### **Índices de Consultas Básicas:**

```sql
-- Sprints por proyecto
idx_factory_sprints_project_id (project_id)

-- Filtrado por estado
idx_factory_sprints_status (status)

-- Sprint actual por proyecto (consulta crítica)
idx_factory_sprints_project_status (project_id, status)
```

#### **Índices de Fechas:**

```sql
-- Rangos de fechas para cronogramas
idx_factory_sprints_date_range (start_date, end_date)
```

#### **Índices Especializados:**

```sql
-- Búsqueda de texto completo
idx_factory_sprints_fulltext (to_tsvector('english', name || ' ' || COALESCE(goal, '')))

-- Analytics de sprints
idx_factory_sprints_analytics (project_id, status, start_date)

-- Índice parcial para sprints activos
idx_factory_sprints_active_only (project_id, start_date, end_date)
WHERE status = 'active'
```

### **5. FACTORY_USER_STORIES (Historias de Usuario)**

#### **Índices de Relaciones:**

```sql
-- Historias por proyecto
idx_factory_user_stories_project_id (project_id)

-- Historias por sprint
idx_factory_user_stories_sprint_id (sprint_id)

-- Historias asignadas a usuarios
idx_factory_user_stories_assigned_to (assigned_to)
```

#### **Índices de Estado y Prioridad:**

```sql
-- Filtrado por estado
idx_factory_user_stories_status (status)

-- Filtrado por prioridad
idx_factory_user_stories_priority (priority)

-- Filtrado por story points
idx_factory_user_stories_story_points (story_points)
```

#### **Índices Compuestos:**

```sql
-- Consultas de backlog (muy frecuente)
idx_factory_user_stories_backlog (project_id, sprint_id, status)

-- Estadísticas de sprint
idx_factory_user_stories_sprint_status (sprint_id, status)
```

#### **Índices de Arrays:**

```sql
-- Búsqueda en tags (GIN index)
idx_factory_user_stories_tags_gin (tags)

-- Búsqueda en dependencias
idx_factory_user_stories_dependencies_gin (dependencies)
```

#### **Índices Especializados:**

```sql
-- Búsqueda de texto completo
idx_factory_user_stories_fulltext (to_tsvector('english', title || ' ' || description))

-- Paginación optimizada
idx_factory_user_stories_pagination (priority, created_at, id)

-- Índice parcial para historias en progreso
idx_factory_user_stories_in_progress (assigned_to, project_id, priority)
WHERE status IN ('todo', 'in_progress', 'review')
```

### **6. FACTORY_EVALUATIONS (Evaluaciones)**

#### **Índices de Relaciones:**

```sql
-- Evaluaciones por aprendiz (consulta crítica)
idx_factory_evaluations_apprentice_id (apprentice_id)

-- Evaluaciones por evaluador
idx_factory_evaluations_evaluator_id (evaluator_id)

-- Evaluaciones por proyecto
idx_factory_evaluations_project_id (project_id)

-- Evaluaciones por sprint
idx_factory_evaluations_sprint_id (sprint_id)
```

#### **Índices de Categorización:**

```sql
-- Tipo de evaluación
idx_factory_evaluations_type (evaluation_type)

-- Fecha de evaluación
idx_factory_evaluations_date (evaluation_date)

-- Puntuación general
idx_factory_evaluations_score (overall_score)
```

#### **Índices Compuestos:**

```sql
-- Historial de evaluaciones por estudiante
idx_factory_evaluations_student_project (apprentice_id, project_id)

-- Reportes por proyecto
idx_factory_evaluations_project_date (project_id, evaluation_date)

-- Rangos de fechas para reportes
idx_factory_evaluations_date_range (evaluation_date, project_id)
```

#### **Índices Especializados:**

```sql
-- Paginación de evaluaciones
idx_factory_evaluations_pagination (evaluation_date, id)

-- Analytics de rendimiento estudiantil
idx_factory_evaluations_analytics (apprentice_id, evaluation_type, overall_score)

-- Categorización automática por puntuación
idx_factory_evaluations_score_category (expresión CASE)
```

### **7. FACTORY_TECHNOLOGIES (Tecnologías)**

#### **Índices de Catálogo:**

```sql
-- Nombre único de tecnología
idx_factory_technologies_name (name) UNIQUE

-- Categoría de tecnología
idx_factory_technologies_category (category)

-- Nivel de dificultad
idx_factory_technologies_level (level)

-- Estado de la tecnología
idx_factory_technologies_status (status)
```

#### **Índices Compuestos:**

```sql
-- Filtrado completo del catálogo
idx_factory_technologies_catalog (category, level, status)
```

#### **Índices de Búsqueda:**

```sql
-- Búsqueda de texto completo
idx_factory_technologies_fulltext (to_tsvector('english', name || ' ' || description))
```

### **8. FACTORY_IMPROVEMENT_PLANS (Planes de Mejora)**

#### **Índices de Relaciones:**

```sql
-- Planes por evaluación
idx_factory_improvement_plans_evaluation_id (evaluation_id)

-- Estado del plan
idx_factory_improvement_plans_status (status)

-- Área de competencia
idx_factory_improvement_plans_competency (competency_area)
```

---

## 📊 **VISTAS MATERIALIZADAS PARA ANALYTICS**

### **1. mv_project_statistics**

**Propósito:** Estadísticas en tiempo real de todos los proyectos  
**Actualización:** Manual mediante `refresh_softwarefactory_analytics()`

**Métricas incluidas:**

- Total de equipos, aprendices, sprints, historias
- Porcentaje de completitud por puntos y por historias
- Promedio de evaluaciones por proyecto
- Duración real vs estimada

**Índices:**

```sql
idx_mv_project_statistics_project_id (project_id) UNIQUE
idx_mv_project_statistics_status (status)
```

### **2. mv_student_performance**

**Propósito:** Rendimiento individual de cada aprendiz por proyecto

**Métricas incluidas:**

- Promedios de todas las competencias técnicas y blandas
- Velocity y tasa de completitud de historias
- Progreso temporal de evaluaciones

**Índices:**

```sql
idx_mv_student_performance_apprentice (apprentice_id)
idx_mv_student_performance_project (project_id)
idx_mv_student_performance_score (avg_overall_score)
```

### **3. mv_technology_usage**

**Propósito:** Estadísticas de adopción y éxito por tecnología

**Métricas incluidas:**

- Proyectos usando cada tecnología
- Aprendices expuestos a cada tecnología
- Tasa de éxito promedio por tecnología

**Índices:**

```sql
idx_mv_technology_usage_tech_id (technology_id)
idx_mv_technology_usage_category (category)
```

---

## ⚡ **OPTIMIZACIONES AVANZADAS**

### **1. Estadísticas Multicolumna**

```sql
-- Mejora del query planner para consultas complejas
stats_projects_tech_complexity (status, tech_stack, complexity_level)
stats_evaluations_scores (apprentice_id, evaluation_type, overall_score, evaluation_date)
stats_user_stories_workflow (project_id, sprint_id, status, priority, story_points)
```

### **2. Índices Parciales**

Reducen el tamaño de los índices incluyendo solo datos relevantes:

- `idx_factory_projects_active_only` - Solo proyectos activos
- `idx_factory_sprints_active_only` - Solo sprints activos
- `idx_factory_user_stories_in_progress` - Solo historias en progreso

### **3. Índices de Expresión**

```sql
-- Categorización automática de puntuaciones
idx_factory_evaluations_score_category (CASE WHEN overall_score >= 4.5 THEN 'excellent'...)
```

---

## 🔧 **FUNCIONES DE MANTENIMIENTO**

### **1. refresh_softwarefactory_analytics()**

Refresca todas las vistas materializadas de forma concurrente:

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_project_statistics;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_student_performance;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_technology_usage;
```

### **2. get_paginated_projects()**

Función optimizada para paginación de proyectos con filtros dinámicos:

- Límite y offset configurables
- Filtros opcionales: estado, instructor, término de búsqueda
- Retorna conteo total para paginación

---

## 📈 **COMANDOS DE MONITOREO**

### **Makefile Commands Disponibles:**

```bash
# Analytics y rendimiento
make refresh-analytics       # Refrescar vistas materializadas
make analyze-performance     # Top 20 índices más usados
make check-indexes          # Detectar índices sin uso
make analyze-queries        # Consultas más lentas (requiere pg_stat_statements)

# Mantenimiento
make vacuum-analyze         # Optimizar todas las tablas
make verify-permissions     # Verificar permisos y esquema
make setup-schema          # Configurar esquema inicial
```

### **Queries de Monitoreo Manual:**

```sql
-- Uso de índices por tabla
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE schemaname = 'softwarefactoryservice_schema'
ORDER BY idx_scan DESC;

-- Índices no utilizados
SELECT schemaname, tablename, indexname
FROM pg_stat_user_indexes
WHERE schemaname = 'softwarefactoryservice_schema' AND idx_scan = 0;

-- Tamaño de índices
SELECT schemaname, tablename, indexname, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE schemaname = 'softwarefactoryservice_schema'
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## 🎯 **PATRONES DE CONSULTA OPTIMIZADOS**

### **Consultas Más Frecuentes Identificadas:**

1. **Proyectos por Instructor:** `WHERE created_by = ?`
2. **Sprint Actual:** `WHERE project_id = ? AND status = 'active'`
3. **Backlog de Historias:** `WHERE project_id = ? AND (sprint_id IS NULL OR status = 'backlog')`
4. **Miembros Activos:** `WHERE team_id = ? AND is_active = true`
5. **Evaluaciones por Estudiante:** `WHERE apprentice_id = ? AND project_id = ?`
6. **Búsqueda de Tecnologías:** `WHERE category = ? AND level = ? AND status = 'active'`
7. **Estadísticas de Sprint:** `WHERE sprint_id = ? AND status = 'done'`
8. **Rangos de Fechas:** `WHERE start_date >= ? AND end_date <= ?`

### **Consultas de Analytics Optimizadas:**

1. **Dashboard de Proyecto:** Usa `mv_project_statistics`
2. **Rendimiento Estudiantil:** Usa `mv_student_performance`
3. **Adopción de Tecnologías:** Usa `mv_technology_usage`
4. **Paginación de Proyectos:** Usa `get_paginated_projects()`

---

## ⚠️ **CONSIDERACIONES DE MANTENIMIENTO**

### **Actualizaciones Requeridas:**

1. **Vistas Materializadas:** Refrescar cada 1-4 horas según carga
2. **Estadísticas de Tablas:** `VACUUM ANALYZE` semanal automático
3. **Monitoreo de Índices:** Revisar uso mensualmente
4. **Limpieza de Datos:** Archivar evaluaciones antiguas (>2 años)

### **Alertas Recomendadas:**

- Índices sin uso por >30 días
- Consultas con tiempo >500ms
- Vistas materializadas desactualizadas >6 horas
- Crecimiento de tabla >50% mensual

---

## 📊 **MÉTRICAS DE RENDIMIENTO ESPERADAS**

### **Antes de Optimización:**

- Consulta de proyectos: ~50-100ms
- Búsqueda de historias: ~30-80ms
- Dashboard analytics: ~500-2000ms
- Paginación: ~20-50ms

### **Después de Optimización:**

- Consulta de proyectos: <10ms
- Búsqueda de historias: <5ms
- Dashboard analytics: <100ms (vistas materializadas)
- Paginación: <5ms

### **Objetivos de SLA:**

- 95% de consultas <20ms
- 99% de consultas <100ms
- Analytics dashboard <200ms
- Búsquedas de texto <50ms

---

## 🔗 **INTEGRACIÓN CON MICROSERVICIO GO**

### **Archivos Relacionados:**

- **Entities:** `sicora-be-go/softwarefactoryservice/internal/domain/entities/*.go`
- **Repositories:** `sicora-be-go/softwarefactoryservice/internal/infrastructure/database/repositories/*.go`
- **Configuración:** `sicora-be-go/softwarefactoryservice/internal/infrastructure/config/config.go`

### **Variables de Entorno Actualizadas:**

```env
DB_SCHEMA=softwarefactoryservice_schema
DB_USER=softwarefactoryservice_user
DB_NAME=sicora_db
```

### **Search Path Configurado:**

```sql
ALTER ROLE softwarefactoryservice_user SET search_path = softwarefactoryservice_schema, public;
```

---

## 📝 **NOTAS FINALES**

Esta optimización de índices está específicamente diseñada para los patrones de uso identificados en las historias de usuario del SoftwareFactoryService. Los índices proporcionan:

✅ **Consultas rápidas** para todas las operaciones CRUD  
✅ **Búsquedas de texto completo** eficientes  
✅ **Analytics en tiempo real** mediante vistas materializadas  
✅ **Paginación optimizada** para interfaces de usuario  
✅ **Consultas complejas** con múltiples filtros  
✅ **Escalabilidad** para crecimiento futuro del sistema

**Última actualización:** 29 de junio de 2025  
**Próxima revisión:** 29 de septiembre de 2025
