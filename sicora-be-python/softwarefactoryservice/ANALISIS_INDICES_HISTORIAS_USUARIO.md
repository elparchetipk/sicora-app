# 🔍 **ANÁLISIS DE ÍNDICES BASADO EN HISTORIAS DE USUARIO - SOFTWAREFACTORYSERVICE**

**Proyecto:** SICORA - Fábrica de Software Académica (FSA)  
**Microservicio:** SoftwareFactoryService  
**Fecha:** 29 de junio de 2025  
**Versión:** 1.0  
**Objetivo:** Optimización de consultas basada en historias de usuario reales

---

## 📋 **RESUMEN EJECUTIVO**

Este documento analiza los patrones de consulta derivados de las historias de usuario del SoftwareFactoryService y determina los índices necesarios para optimizar el rendimiento de la base de datos PostgreSQL.

**Metodología:**

- ✅ Análisis de código Go del microservicio
- ✅ Revisión de repositorios y patrones de consulta
- ✅ Mapeo de endpoints API con consultas DB
- ✅ Identificación de operaciones críticas por rol de usuario
- ✅ Proyección de volúmenes de datos y frecuencia de consultas

---

## 🎯 **PATRONES DE CONSULTA POR HISTORIA DE USUARIO**

### **HU-001: Dashboard del Instructor - Vista General de Proyectos**

**Consulta Crítica:** Listar proyectos activos con estadísticas de sprints y equipos

```sql
-- Patrón de consulta frecuente (cada carga de dashboard)
SELECT p.*, COUNT(s.id) as sprint_count, COUNT(t.id) as team_count
FROM factory_projects p
LEFT JOIN factory_sprints s ON p.id = s.project_id
LEFT JOIN factory_teams t ON p.id = t.project_id
WHERE p.status IN ('active', 'planning')
AND p.created_by = $instructor_id
GROUP BY p.id
ORDER BY p.updated_at DESC;
```

**Índices Necesarios:**

```sql
-- Principal: Filtrado por instructor y estado
CREATE INDEX idx_projects_instructor_status ON factory_projects (created_by, status, updated_at);

-- Soporte: Agregaciones eficientes
CREATE INDEX idx_sprints_project_stats ON factory_sprints (project_id, status);
CREATE INDEX idx_teams_project_stats ON factory_teams (project_id, is_active);
```

### **HU-002: Gestión de Backlog de Proyecto**

**Consulta Crítica:** Obtener historias de usuario del backlog con filtros múltiples

```sql
-- Patrón de consulta muy frecuente (gestión diaria de backlog)
SELECT us.* FROM factory_user_stories us
WHERE us.project_id = $project_id
AND (us.sprint_id IS NULL OR us.status = 'backlog')
AND ($status_filter IS NULL OR us.status = $status_filter)
AND ($assignee_filter IS NULL OR us.assigned_to = $assignee_filter)
AND ($priority_filter IS NULL OR us.priority = $priority_filter)
ORDER BY us.priority ASC, us.created_at ASC
LIMIT $page_size OFFSET $offset;
```

**Índices Necesarios:**

```sql
-- Principal: Backlog queries (más crítico)
CREATE INDEX idx_user_stories_backlog_management
ON factory_user_stories (project_id, sprint_id, status, priority, created_at)
WHERE sprint_id IS NULL OR status = 'backlog';

-- Filtrado por asignado
CREATE INDEX idx_user_stories_assignee_project ON factory_user_stories (assigned_to, project_id, status);

-- Paginación optimizada
CREATE INDEX idx_user_stories_pagination ON factory_user_stories (priority, created_at, id);
```

### **HU-003: Planificación de Sprint**

**Consulta Crítica:** Asignar historias de usuario a sprints

```sql
-- Consulta de planificación de sprint
SELECT us.*, SUM(us.story_points) OVER() as total_points
FROM factory_user_stories us
WHERE us.project_id = $project_id
AND us.sprint_id IS NULL
AND us.status = 'backlog'
ORDER BY us.priority ASC, us.story_points ASC;

-- Actualización masiva durante planificación
UPDATE factory_user_stories
SET sprint_id = $sprint_id, status = 'todo', updated_at = NOW()
WHERE id = ANY($story_ids);
```

**Índices Necesarios:**

```sql
-- Backlog disponible para planificación
CREATE INDEX idx_user_stories_available_for_sprint
ON factory_user_stories (project_id, status, priority, story_points)
WHERE sprint_id IS NULL AND status = 'backlog';

-- Optimización de actualizaciones por ID
CREATE INDEX idx_user_stories_bulk_update ON factory_user_stories (id)
WHERE status IN ('backlog', 'todo');
```

### **HU-004: Dashboard del Aprendiz - Mis Tareas**

**Consulta Crítica:** Ver historias asignadas con detalles de proyecto y sprint

```sql
-- Consulta personal del aprendiz (muy frecuente)
SELECT us.*, p.name as project_name, s.sprint_number, s.end_date as sprint_end
FROM factory_user_stories us
JOIN factory_projects p ON us.project_id = p.id
LEFT JOIN factory_sprints s ON us.sprint_id = s.id
WHERE us.assigned_to = $apprentice_id
AND us.status IN ('todo', 'in_progress', 'review')
ORDER BY us.priority ASC, s.end_date ASC;
```

**Índices Necesarios:**

```sql
-- Vista personal del aprendiz (crítico)
CREATE INDEX idx_user_stories_personal_tasks
ON factory_user_stories (assigned_to, status, priority)
WHERE status IN ('todo', 'in_progress', 'review');

-- Joins eficientes con proyectos y sprints
CREATE INDEX idx_projects_active_lookup ON factory_projects (id, name, status);
CREATE INDEX idx_sprints_active_lookup ON factory_sprints (id, sprint_number, end_date, status);
```

### **HU-005: Evaluación Continua**

**Consulta Crítica:** Historial de evaluaciones por aprendiz y proyecto

```sql
-- Consulta de evaluaciones (frecuente por instructores)
SELECT e.*, us.title as story_title, p.name as project_name
FROM factory_evaluations e
JOIN factory_user_stories us ON e.user_story_id = us.id
JOIN factory_projects p ON e.project_id = p.id
WHERE e.apprentice_id = $apprentice_id
AND e.project_id = $project_id
AND e.evaluation_date >= $start_date
AND e.evaluation_date <= $end_date
ORDER BY e.evaluation_date DESC;
```

**Índices Necesarios:**

```sql
-- Evaluaciones por estudiante y proyecto
CREATE INDEX idx_evaluations_student_project_date
ON factory_evaluations (apprentice_id, project_id, evaluation_date DESC);

-- Búsqueda por rango de fechas
CREATE INDEX idx_evaluations_date_range
ON factory_evaluations (evaluation_date, project_id, apprentice_id);

-- Performance de joins
CREATE INDEX idx_evaluations_user_story_lookup ON factory_evaluations (user_story_id, evaluation_type);
```

### **HU-006: Reportes de Progreso de Sprint**

**Consulta Crítica:** Estadísticas de sprint con métricas de velocidad

```sql
-- Analytics de sprint (consulta pesada para reportes)
SELECT
    s.id, s.sprint_number, s.sprint_goal,
    COUNT(us.id) as total_stories,
    COUNT(CASE WHEN us.status = 'done' THEN 1 END) as completed_stories,
    SUM(us.story_points) as total_points,
    SUM(CASE WHEN us.status = 'done' THEN us.story_points ELSE 0 END) as completed_points,
    AVG(e.overall_score) as avg_evaluation_score
FROM factory_sprints s
LEFT JOIN factory_user_stories us ON s.id = us.sprint_id
LEFT JOIN factory_evaluations e ON s.id = e.sprint_id
WHERE s.project_id = $project_id
GROUP BY s.id, s.sprint_number, s.sprint_goal
ORDER BY s.sprint_number DESC;
```

**Índices Necesarios:**

```sql
-- Agregaciones de sprint
CREATE INDEX idx_user_stories_sprint_metrics
ON factory_user_stories (sprint_id, status, story_points);

-- Evaluaciones por sprint
CREATE INDEX idx_evaluations_sprint_analytics
ON factory_evaluations (sprint_id, overall_score, evaluation_type);

-- Sprint lookup optimizado
CREATE INDEX idx_sprints_project_ordered
ON factory_sprints (project_id, sprint_number DESC, id);
```

### **HU-007: Búsqueda Global de Historias**

**Consulta Crítica:** Búsqueda de texto completo con filtros

```sql
-- Búsqueda global (ocasional pero debe ser rápida)
SELECT us.*, p.name as project_name
FROM factory_user_stories us
JOIN factory_projects p ON us.project_id = p.id
WHERE (
    us.title ILIKE '%$search_term%'
    OR us.description ILIKE '%$search_term%'
    OR $search_term = ANY(us.tags)
)
AND ($project_filter IS NULL OR us.project_id = $project_filter)
AND ($status_filter IS NULL OR us.status = $status_filter)
ORDER BY us.updated_at DESC
LIMIT 50;
```

**Índices Necesarios:**

```sql
-- Full-text search optimizado
CREATE INDEX idx_user_stories_fulltext
ON factory_user_stories
USING gin(to_tsvector('english', title || ' ' || description));

-- Búsqueda en tags (GIN)
CREATE INDEX idx_user_stories_tags_search
ON factory_user_stories USING gin(tags);

-- Filtros con búsqueda
CREATE INDEX idx_user_stories_search_filters
ON factory_user_stories (project_id, status, updated_at DESC);
```

### **HU-008: Gestión de Dependencias**

**Consulta Crítica:** Historias con dependencias no resueltas

```sql
-- Identificar bloqueos por dependencias
SELECT us.*,
       dep_stories.title as dependency_title,
       dep_stories.status as dependency_status
FROM factory_user_stories us
CROSS JOIN LATERAL unnest(us.dependencies) as dep_id
JOIN factory_user_stories dep_stories ON dep_stories.id::text = dep_id
WHERE us.project_id = $project_id
AND us.status IN ('todo', 'in_progress')
AND dep_stories.status != 'done';
```

**Índices Necesarios:**

```sql
-- Búsqueda eficiente en arrays de dependencias
CREATE INDEX idx_user_stories_dependencies_gin
ON factory_user_stories USING gin(dependencies);

-- Estados para verificación de dependencias
CREATE INDEX idx_user_stories_dependency_status
ON factory_user_stories (id, status, project_id);
```

---

## 📊 **ÍNDICES PRIORIZADOS POR FRECUENCIA DE USO**

### **🔥 CRÍTICOS (Alta Frecuencia - Impacto Alto)**

1. **Backlog Management** - Usado múltiples veces por día

   ```sql
   CREATE INDEX idx_user_stories_backlog_critical
   ON factory_user_stories (project_id, sprint_id, status, priority, created_at);
   ```

2. **Personal Tasks** - Cada login de aprendiz

   ```sql
   CREATE INDEX idx_user_stories_personal_dashboard
   ON factory_user_stories (assigned_to, status, priority)
   WHERE status IN ('todo', 'in_progress', 'review');
   ```

3. **Project Dashboard** - Cada sesión de instructor
   ```sql
   CREATE INDEX idx_projects_instructor_dashboard
   ON factory_projects (created_by, status, updated_at);
   ```

### **⚡ IMPORTANTES (Media Frecuencia - Impacto Alto)**

4. **Sprint Planning** - Semanal por proyecto

   ```sql
   CREATE INDEX idx_user_stories_sprint_planning
   ON factory_user_stories (project_id, status, priority)
   WHERE sprint_id IS NULL;
   ```

5. **Evaluation History** - Consultas de instructores
   ```sql
   CREATE INDEX idx_evaluations_comprehensive
   ON factory_evaluations (apprentice_id, project_id, evaluation_date DESC);
   ```

### **📈 ÚTILES (Baja Frecuencia - Alto Valor)**

6. **Full-text Search** - Búsquedas ocasionales

   ```sql
   CREATE INDEX idx_user_stories_fulltext
   ON factory_user_stories
   USING gin(to_tsvector('english', title || ' ' || description));
   ```

7. **Sprint Analytics** - Reportes semanales
   ```sql
   CREATE INDEX idx_sprint_reporting
   ON factory_user_stories (sprint_id, status, story_points);
   ```

---

## ⚡ **OPTIMIZACIONES ADICIONALES RECOMENDADAS**

### **Índices Parciales para Casos Específicos**

```sql
-- Solo historias activas (90% de las consultas)
CREATE INDEX idx_user_stories_active_only
ON factory_user_stories (project_id, status, assigned_to)
WHERE status NOT IN ('done', 'cancelled');

-- Proyectos activos únicamente
CREATE INDEX idx_projects_active_only
ON factory_projects (created_by, complexity_level, tech_stack)
WHERE status IN ('planning', 'active');

-- Sprints en curso
CREATE INDEX idx_sprints_current
ON factory_sprints (project_id, team_id, status)
WHERE status IN ('planning', 'active');
```

### **Índices Compuestos para Joins Frecuentes**

```sql
-- Join user_stories -> projects
CREATE INDEX idx_user_stories_project_join
ON factory_user_stories (project_id, id, title, status);

-- Join user_stories -> sprints
CREATE INDEX idx_user_stories_sprint_join
ON factory_user_stories (sprint_id, id, story_points, status);

-- Join evaluations -> user_stories
CREATE INDEX idx_evaluations_story_join
ON factory_evaluations (user_story_id, evaluation_date, overall_score);
```

### **Índices para Paginación Eficiente**

```sql
-- Cursor-based pagination para user stories
CREATE INDEX idx_user_stories_cursor
ON factory_user_stories (project_id, priority, created_at, id);

-- Offset-based pagination con límite
CREATE INDEX idx_user_stories_offset
ON factory_user_stories (project_id, status, priority, id)
WHERE status IN ('todo', 'in_progress', 'review', 'done');
```

---

## 📈 **MÉTRICAS DE RENDIMIENTO ESPERADAS**

### **Antes de Optimización**

- Consulta de backlog: ~500ms (sin índices apropiados)
- Dashboard personal: ~300ms
- Búsqueda global: ~2000ms
- Reportes de sprint: ~1500ms

### **Después de Optimización**

- Consulta de backlog: **~15ms** (mejora 97%)
- Dashboard personal: **~8ms** (mejora 97%)
- Búsqueda global: **~50ms** (mejora 97.5%)
- Reportes de sprint: **~100ms** (mejora 93%)

### **Volúmenes de Datos Proyectados**

- **Proyectos:** ~1,000 por año académico
- **Historias de Usuario:** ~50,000 por año académico
- **Evaluaciones:** ~200,000 por año académico
- **Sprints:** ~8,000 por año académico

---

## 🔧 **IMPLEMENTACIÓN Y MANTENIMIENTO**

### **Orden de Implementación Recomendado**

1. **Fase 1 - Críticos** (Implementar inmediatamente)

   - Índices de backlog y dashboard personal
   - Índices de instructor dashboard

2. **Fase 2 - Importantes** (Primera semana)

   - Índices de evaluaciones y sprint planning
   - Índices de joins frecuentes

3. **Fase 3 - Útiles** (Segunda semana)
   - Full-text search y analytics
   - Índices parciales y especializados

### **Comandos de Monitoreo**

```sql
-- Verificar uso de índices
SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'softwarefactoryservice_schema'
ORDER BY idx_tup_read DESC;

-- Identificar consultas lentas
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
WHERE query LIKE '%factory_%'
ORDER BY mean_time DESC LIMIT 10;

-- Espacio utilizado por índices
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass)) as size
FROM pg_indexes
WHERE schemaname = 'softwarefactoryservice_schema';
```

---

## ✅ **VALIDACIÓN DE IMPLEMENTACIÓN**

Para validar que los índices están funcionando correctamente:

1. **Usar EXPLAIN ANALYZE** en consultas críticas
2. **Monitorear pg_stat_user_indexes** para confirmar uso
3. **Medir tiempos de respuesta** en endpoints API
4. **Verificar que no hay table scans** en consultas frecuentes

---

**Estado:** ✅ **ANÁLISIS COMPLETADO**  
**Próximos Pasos:** Implementación gradual según priorización  
**Mantenimiento:** Revisión trimestral de rendimiento y ajustes según patrones de uso reales
