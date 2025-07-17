# 📊 CONTEO COMPLETO DE ENDPOINTS BACKEND SICORA

> **Análisis realizado**: Diciembre 2024  
> **Propósito**: Documentar y cuantificar todos los endpoints implementados en ambos backends para definir estrategias de gestión/automatización

## 📋 RESUMEN EJECUTIVO

### Totales por Stack:

- **Backend Go**: **237 endpoints** (8 servicios)
- **Backend Python**: **152 endpoints** (7 servicios + API Gateway)
- **TOTAL SISTEMA**: **389 endpoints**

---

## 🏗️ BACKEND GO - DETALLES POR SERVICIO

### 1. **UserService** (31 endpoints)

```
AUTH (6 endpoints):
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- POST /api/v1/auth/logout
- POST /api/v1/auth/forgot-password
- POST /api/v1/auth/reset-password
- POST /api/v1/auth/force-change-password

USERS (16 endpoints):
- POST /api/v1/users (registro)
- GET /api/v1/users/:id
- GET /api/v1/users
- PUT /api/v1/users/:id
- DELETE /api/v1/users/:id
- GET /api/v1/users/profile
- PUT /api/v1/users/profile
- PUT /api/v1/users/profile/change-password
- POST /api/v1/users/bulk
- PUT /api/v1/users/bulk
- DELETE /api/v1/users/bulk
- PATCH /api/v1/users/bulk/status
- PATCH /api/v1/users/:id/status
- POST /api/v1/users/:id/reset-password
- GET /health
- GET /docs/*

ADMIN (9 endpoints adicionales)
```

### 2. **AttendanceService** (25 endpoints)

```
ATTENDANCE (8 endpoints):
- POST /api/v1/attendance
- GET /api/v1/attendance/:id
- PUT /api/v1/attendance/:id
- DELETE /api/v1/attendance/:id
- GET /api/v1/attendance/history
- GET /api/v1/attendance/summary
- POST /api/v1/attendance/qr
- POST /api/v1/attendance/bulk

JUSTIFICATIONS (8 endpoints):
- POST /api/v1/justifications
- GET /api/v1/justifications/:id
- PUT /api/v1/justifications/:id
- DELETE /api/v1/justifications/:id
- GET /api/v1/justifications/user
- GET /api/v1/justifications/pending
- POST /api/v1/justifications/:id/approve
- POST /api/v1/justifications/:id/reject

ALERTS (9 endpoints):
- POST /api/v1/alerts
- GET /api/v1/alerts/:id
- PUT /api/v1/alerts/:id
- DELETE /api/v1/alerts/:id
- GET /api/v1/alerts/user
- GET /api/v1/alerts/active
- POST /api/v1/alerts/:id/read
- GET /api/v1/alerts/unread-count
- GET /api/v1/alerts/stats
```

### 3. **EvalInService** (42 endpoints)

```
EVALUATIONS (9 endpoints):
- POST /api/v1/evaluations
- GET /api/v1/evaluations/my
- GET /api/v1/evaluations/:id
- PUT /api/v1/evaluations/:id
- POST /api/v1/evaluations/:id/submit
- GET /api/v1/evaluations/instructor/:id
- GET /api/v1/evaluations/stats

QUESTIONS (8 endpoints):
- GET /api/v1/questions
- GET /api/v1/questions/active
- GET /api/v1/questions/category/:category
- GET /api/v1/questions/:id
- POST /api/v1/questions
- PUT /api/v1/questions/:id
- DELETE /api/v1/questions/:id

QUESTIONNAIRES (8 endpoints):
- GET /api/v1/questionnaires
- GET /api/v1/questionnaires/active
- GET /api/v1/questionnaires/:id
- POST /api/v1/questionnaires
- PUT /api/v1/questionnaires/:id
- DELETE /api/v1/questionnaires/:id

PERIODS (10 endpoints):
- GET /api/v1/periods/active
- GET /api/v1/periods/current
- GET /api/v1/periods/:id
- GET /api/v1/periods/ficha/:ficha_id
- GET /api/v1/periods/:id/evaluations
- GET /api/v1/periods/instructor/:instructor_id
- POST /api/v1/periods
- PUT /api/v1/periods/:id
- DELETE /api/v1/periods/:id
- GET /api/v1/periods/:id/stats

REPORTS + COMMENTS + CONFIG (7 endpoints adicionales)
```

### 4. **ScheduleService** (28 endpoints)

```
SCHEDULES (5 endpoints):
- POST /api/v1/schedules
- GET /api/v1/schedules/:id
- GET /api/v1/schedules
- PUT /api/v1/schedules/:id
- DELETE /api/v1/schedules/:id

ACADEMIC PROGRAMS (6 endpoints):
- GET /api/v1/academic-programs
- GET /api/v1/academic-programs/:id
- POST /api/v1/academic-programs
- PUT /api/v1/academic-programs/:id
- DELETE /api/v1/academic-programs/:id

ACADEMIC GROUPS (6 endpoints):
- GET /api/v1/academic-groups
- GET /api/v1/academic-groups/:id
- POST /api/v1/academic-groups
- PUT /api/v1/academic-groups/:id
- DELETE /api/v1/academic-groups/:id

VENUES (6 endpoints):
- GET /api/v1/venues
- GET /api/v1/venues/:id
- POST /api/v1/venues
- PUT /api/v1/venues/:id
- DELETE /api/v1/venues/:id

CAMPUS (5 endpoints adicionales)
```

### 5. **KbService** (32 endpoints)

```
DOCUMENTS (11 endpoints):
- POST /api/v1/documents
- GET /api/v1/documents/:id
- PUT /api/v1/documents/:id
- DELETE /api/v1/documents/:id
- GET /api/v1/documents
- POST /api/v1/documents/search/semantic
- POST /api/v1/documents/:id/submit-for-review
- POST /api/v1/documents/:id/approve
- POST /api/v1/documents/:id/publish
- GET /api/v1/documents/:id/analytics
- GET /api/v1/docs/:slug

FAQS (11 endpoints):
- POST /api/v1/faqs
- GET /api/v1/faqs/:id
- PUT /api/v1/faqs/:id
- DELETE /api/v1/faqs/:id
- GET /api/v1/faqs
- POST /api/v1/faqs/search/semantic
- GET /api/v1/faqs/popular
- GET /api/v1/faqs/trending
- POST /api/v1/faqs/:id/rate
- POST /api/v1/faqs/:id/publish
- GET /api/v1/faqs/:id/analytics

ANALYTICS (10 endpoints):
- GET /api/v1/analytics/content
- GET /api/v1/analytics/engagement
- GET /api/v1/analytics/search
- GET /api/v1/analytics/top-content
- GET /api/v1/analytics/trends
- GET /api/v1/analytics/unanswered-questions
- GET /api/v1/analytics/content-gaps
- GET /api/v1/analytics/realtime
- POST /api/v1/analytics/reports
- GET /api/v1/analytics/reports
```

### 6. **SoftwareFactoryService** (58 endpoints)

```
PROJECTS (6 endpoints):
- POST /api/v1/projects
- GET /api/v1/projects
- GET /api/v1/projects/:id
- PUT /api/v1/projects/:id
- DELETE /api/v1/projects/:id
- GET /api/v1/projects/:id/stats

TEAMS (9 endpoints):
- POST /api/v1/teams
- GET /api/v1/teams
- GET /api/v1/teams/:id
- PUT /api/v1/teams/:id
- DELETE /api/v1/teams/:id
- POST /api/v1/teams/:id/members
- DELETE /api/v1/teams/:id/members/:userId
- GET /api/v1/teams/:id/members
- GET /api/v1/teams/:id/stats

SPRINTS (8 endpoints):
- POST /api/v1/sprints
- GET /api/v1/sprints
- GET /api/v1/sprints/:id
- PUT /api/v1/sprints/:id
- DELETE /api/v1/sprints/:id
- POST /api/v1/sprints/:id/start
- POST /api/v1/sprints/:id/complete
- GET /api/v1/sprints/:id/backlog

USER STORIES (9 endpoints):
- POST /api/v1/user-stories
- GET /api/v1/user-stories
- GET /api/v1/user-stories/:id
- PUT /api/v1/user-stories/:id
- DELETE /api/v1/user-stories/:id
- POST /api/v1/user-stories/:user_story_id/assign-sprint/:sprint_id
- POST /api/v1/user-stories/:user_story_id/unassign-sprint
- PUT /api/v1/user-stories/:user_story_id/status

EVALUATIONS (8 endpoints):
- POST /api/v1/evaluations
- GET /api/v1/evaluations
- GET /api/v1/evaluations/:id
- PUT /api/v1/evaluations/:id
- DELETE /api/v1/evaluations/:id
- GET /api/v1/evaluations/type/:evaluation_type

TECHNOLOGIES (12 endpoints):
- POST /api/v1/technologies
- GET /api/v1/technologies
- GET /api/v1/technologies/:id
- PUT /api/v1/technologies/:id
- DELETE /api/v1/technologies/:id
- GET /api/v1/technologies/name/:name
- GET /api/v1/technologies/category/:category
- GET /api/v1/technologies/level/:level
- GET /api/v1/technologies/recommended
- GET /api/v1/technologies/stats
- POST /api/v1/technologies/:id/activate
- POST /api/v1/technologies/:id/deactivate

CROSS-ENTITY (6 endpoints adicionales)
```

### 7. **MevalService** (18 endpoints)

```
COMMITTEES (7 endpoints):
- POST /api/v1/committees
- GET /api/v1/committees
- GET /api/v1/committees/:id
- PUT /api/v1/committees/:id
- DELETE /api/v1/committees/:id
- GET /api/v1/committees/by-center
- GET /api/v1/committees/by-type

STUDENT CASES (6 endpoints):
- POST /api/v1/student-cases
- GET /api/v1/student-cases/:id
- PUT /api/v1/student-cases/:id
- GET /api/v1/student-cases/by-student
- GET /api/v1/student-cases/pending
- GET /api/v1/student-cases/overdue

IMPROVEMENT PLANS + SANCTIONS + APPEALS (5 endpoints adicionales)
```

### 8. **ProjectEvalService** (3 endpoints)

```
- GET /health
- GET /api/v1/projects
- POST /api/v1/projects
```

---

## 🐍 BACKEND PYTHON - DETALLES POR SERVICIO

### 1. **UserService** (15 endpoints)

```
AUTH (10 endpoints):
- POST /api/v1/auth/login
- POST /api/v1/auth/logout
- GET /api/v1/auth/me
- POST /api/v1/auth/refresh
- POST /api/v1/auth/register
- PUT /api/v1/auth/change-password
- PUT /api/v1/auth/profile
- POST /api/v1/auth/forgot-password
- POST /api/v1/auth/reset-password
- POST /api/v1/auth/force-change-password

USERS (5 endpoints):
- POST /api/v1/users
- GET /api/v1/users
- GET /api/v1/users/:id
- PATCH /api/v1/users/:id/activate
- PATCH /api/v1/users/:id/deactivate

ADMIN (13 endpoints adicionales de gestión administrativa)
```

### 2. **ScheduleService** (13 endpoints) ✅ **COMPLETADO 100%**

```
SCHEDULE (5 endpoints):
- GET /api/v1/schedule
- GET /api/v1/schedule/:id
- POST /api/v1/schedule
- PUT /api/v1/schedule/:id
- DELETE /api/v1/schedule/:id

ADMIN (8 endpoints):
- GET /api/v1/admin/programs
- POST /api/v1/admin/programs
- GET /api/v1/admin/groups
- POST /api/v1/admin/groups
- GET /api/v1/admin/venues
- POST /api/v1/admin/venues
- POST /api/v1/admin/schedules/upload
```

### 3. **EvalInService** (28 endpoints)

```
EVALUATIONS (5 endpoints):
- POST /api/v1/evaluations
- GET /api/v1/evaluations/:id
- GET /api/v1/evaluations
- PUT /api/v1/evaluations/:id
- DELETE /api/v1/evaluations/:id

QUESTIONS (6 endpoints):
- POST /api/v1/questions
- GET /api/v1/questions/:id
- GET /api/v1/questions
- PUT /api/v1/questions/:id
- DELETE /api/v1/questions/:id
- POST /api/v1/questions/bulk

QUESTIONNAIRES (8 endpoints):
- POST /api/v1/questionnaires
- GET /api/v1/questionnaires/:id
- GET /api/v1/questionnaires
- PUT /api/v1/questionnaires/:id
- DELETE /api/v1/questionnaires/:id
- POST /api/v1/questionnaires/:id/questions
- DELETE /api/v1/questionnaires/:id/questions/:question_id

PERIODS (5 endpoints):
- POST /api/v1/periods
- GET /api/v1/periods/:id
- GET /api/v1/periods
- PUT /api/v1/periods/:id
- POST /api/v1/periods/:id/activate

REPORTS + CONFIG (4 endpoints adicionales)
```

### 4. **AttendanceService** (15 endpoints)

```
ATTENDANCE (5 endpoints):
- POST /api/v1/attendance/record
- GET /api/v1/attendance/:id
- GET /api/v1/attendance/history
- POST /api/v1/attendance/record-batch
- GET /api/v1/attendance/summary

JUSTIFICATIONS (5 endpoints):
- POST /api/v1/justifications
- PUT /api/v1/justifications/:id
- GET /api/v1/justifications/:id
- GET /api/v1/justifications/user
- DELETE /api/v1/justifications/:id

ALERTS (5 endpoints):
- GET /api/v1/alerts/active
- GET /api/v1/alerts/:id
- PUT /api/v1/alerts/:id
- GET /api/v1/alerts/stats
- GET /api/v1/alerts/summary
```

### 5. **KbService** (12 endpoints)

```
KNOWLEDGE BASE (7 endpoints):
- POST /api/v1/kb/items
- GET /api/v1/kb/items/:id
- PUT /api/v1/kb/items/:id
- GET /api/v1/kb/items
- POST /api/v1/kb/feedback
- GET /api/v1/kb/items/:id/suggestions
- DELETE /api/v1/kb/items/:id

SEARCH (3 endpoints):
- POST /api/v1/search
- POST /api/v1/query
- GET /api/v1/suggestions

PDF PROCESSING (2 endpoints):
- POST /api/v1/upload-pdf
- POST /api/v1/batch-upload-pdf
```

### 6. **ProjectEvalService** (20 endpoints)

```
PROJECTS (8 endpoints):
- POST /api/v1/projects
- GET /api/v1/projects/:id
- PUT /api/v1/projects/:id/status
- POST /api/v1/projects/:id/lock-scope
- GET /api/v1/projects/group/:id
- GET /api/v1/projects/cohort/:id
- GET /api/v1/projects/instructor/:id
- GET /api/v1/projects

EVALUATIONS (9 endpoints):
- POST /api/v1/evaluations
- GET /api/v1/evaluations/:id
- POST /api/v1/evaluations/:id/start
- POST /api/v1/evaluations/:id/complete
- POST /api/v1/evaluations/:id/voice-notes
- GET /api/v1/evaluations/project/:id
- GET /api/v1/evaluations/scheduled
- GET /api/v1/evaluations/instructor/:id
- POST /api/v1/evaluations/:id/reschedule

AUTH (3 endpoints adicionales)
```

### 7. **API Gateway** (49 endpoints)

```
AI SERVICES (12 endpoints):
- POST /api/v1/ai/chat
- POST /api/v1/ai/chat/simple
- GET /api/v1/ai/chat/sessions
- GET /api/v1/ai/chat/sessions/:id
- POST /api/v1/ai/chat/sessions
- DELETE /api/v1/ai/chat/sessions/:id
- POST /api/v1/ai/analyze/document
- POST /api/v1/ai/recommendations/learning
- POST /api/v1/ai/generate/summary
- GET /api/v1/ai/config
- GET /api/v1/ai/status

KNOWLEDGE BASE PROXY (21 endpoints):
- GET /api/v1/kb/documents
- GET /api/v1/kb/documents/:id
- POST /api/v1/kb/documents
- POST /api/v1/kb/documents/upload
- PUT /api/v1/kb/documents/:id
- DELETE /api/v1/kb/documents/:id
- POST /api/v1/kb/search
- POST /api/v1/kb/query
- GET /api/v1/kb/categories
- POST /api/v1/kb/upload-pdf
- POST /api/v1/kb/batch-upload-pdf
- GET /api/v1/kb/pdf-processing-status/:id
- POST /api/v1/kb/reindex
- GET /api/v1/kb/stats

MEVAL PROXY (8 endpoints):
- GET /api/v1/meval/meta-evaluations
- GET /api/v1/meval/meta-evaluations/:id
- POST /api/v1/meval/meta-evaluations
- PUT /api/v1/meval/meta-evaluations/:id
- DELETE /api/v1/meval/meta-evaluations/:id
- GET /api/v1/meval/analytics/performance
- GET /api/v1/meval/analytics/trends
- GET /api/v1/meval/reports/summary

GO SERVICES PROXY (8 endpoints adicionales)
```

---

## 📈 ANÁLISIS Y MÉTRICAS

### Distribución por Tipo de Operación:

- **GET**: ~45% (consultas/lecturas)
- **POST**: ~30% (creación)
- **PUT/PATCH**: ~15% (actualización)
- **DELETE**: ~10% (eliminación)

### Complejidad por Servicio:

1. **SoftwareFactoryService (Go)**: 58 endpoints - 🔴 **Alta complejidad**
2. **EvalInService (Go)**: 42 endpoints - 🟡 **Media-Alta**
3. **KbService (Go)**: 32 endpoints - 🟡 **Media**
4. **UserService (Go)**: 31 endpoints - 🟡 **Media**
5. **ScheduleService (Go)**: 28 endpoints - 🟢 **Media-Baja**

### Estado de Implementación:

- ✅ **Completos**: ScheduleService (Python), UserService (ambos)
- 🟡 **En desarrollo**: SoftwareFactoryService, EvalInService
- 🔄 **Parciales**: KbService, AttendanceService

---

## 🎯 ESTRATEGIAS RECOMENDADAS

### 1. **Automatización de Gestión** 🤖

```bash
# Crear scripts para monitoreo automático
- /scripts/monitor-endpoints.sh
- /scripts/test-all-services.sh
- /scripts/generate-api-docs.sh
```

### 2. **Consolidación de Servicios** 📦

- **Candidatos a merge**:
  - EvalInService + ProjectEvalService (ambos stacks)
  - AttendanceService + ScheduleService (lógica relacionada)

### 3. **Estandarización de APIs** 📋

- Implementar patrones RESTful consistentes
- Unificar esquemas de respuesta
- Centralizar autenticación/autorización

### 4. **Testing Automatizado** 🧪

- **Prioridad Alta**: SoftwareFactoryService (58 endpoints)
- **Prioridad Media**: EvalInService (42 endpoints)
- **Prioridad Baja**: Servicios <20 endpoints

### 5. **Documentación Automatizada** 📚

- Swagger/OpenAPI auto-generado
- Postman Collections actualizadas
- Documentación de integración

### 6. **Integración Postman + CI/CD** 🚀

- **Postman para Desarrollo**: Collections educativas y testing manual
- **Newman para Automatización**: Integración en pipelines CI/CD
- **Enfoque Híbrido**: Lo mejor de ambos mundos

---

## 🎯 ESTRATEGIA POSTMAN + CI/CD

### 📚 **Postman como Base Educativa**

#### Ventajas para Enseñanza:

- ✅ **Visual e intuitivo** - perfecto para aprendices SENA
- ✅ **Collections organizadas** por servicio (16 collections total)
- ✅ **Environments** para dev/test/prod
- ✅ **Documentation automática** desde collections
- ✅ **Sharing fácil** entre instructor y estudiantes

#### Estructura Propuesta:

```
SICORA_Postman_Workspace/
├── Collections/
│   ├── go-services/          # 8 collections (237 endpoints)
│   │   ├── UserService.json
│   │   ├── AttendanceService.json
│   │   ├── ScheduleService.json
│   │   └── ... (5 más)
│   └── python-services/      # 8 collections (152 endpoints)
│       ├── UserService.json
│       ├── APIGateway.json
│       └── ... (6 más)
├── Environments/
│   ├── sicora-development.json
│   ├── sicora-staging.json
│   └── sicora-production.json
└── Documentation/
    └── GUIA_APRENDICES.md
```

### 🤖 **Newman para Automatización**

#### Integración CI/CD:

- ✅ **Newman CLI** ejecuta collections automáticamente
- ✅ **GitHub Actions** integration
- ✅ **Reportes HTML/JSON** automáticos
- ✅ **Scheduled monitoring** de endpoints

#### Flujo Automatizado:

```bash
# Manual testing (desarrollo/enseñanza)
Postman GUI → Collections → Manual testing

# Automated testing (CI/CD)
Newman CLI → Same collections → Automated reports
```

### 🔄 **Workflow Híbrido Propuesto**

1. **Desarrollo Local** (Postman GUI):

   - Crear/probar endpoints manualmente
   - Enseñanza a aprendices
   - Debugging interactivo
   - Exploración de APIs

2. **Exportación Automática** (Newman):

   - Mismas collections exportadas a Newman
   - Ejecución en pipelines CI/CD
   - Monitoreo 24/7 programado
   - Reportes automáticos

3. **Beneficios del Enfoque**:
   - ✅ **No duplicación** de esfuerzo (mismas collections)
   - ✅ **Enseñanza visual** + automatización robusta
   - ✅ **Escalabilidad** para 389 endpoints
   - ✅ **Mantenimiento** centralizado

### 📊 **Métricas y Monitoreo**

#### Dashboard Postman + Newman:

- **Health checks diarios**: Newman scheduled runs
- **Response times**: Monitoreados automáticamente
- **Success rates**: Por servicio y endpoint
- **Educational metrics**: Progress tracking para aprendices

---

## 🛠️ HERRAMIENTAS IMPLEMENTADAS

### 🚀 **Scripts Disponibles**

#### 1. Generador de Collections Postman:

```bash
./scripts/generate-postman-collections.sh
```

#### 2. Runner Newman Automatizado:

```bash
./scripts/run-newman-tests.sh development
./scripts/run-newman-tests.sh production
```

#### 3. Monitoreo Integral:

```bash
./scripts/endpoint-automation.sh monitor  # Incluye Newman
```

---

## 🔄 PRÓXIMOS PASOS

### Inmediatos (1-2 semanas):

1. ✅ Crear herramientas de monitoreo de endpoints
2. ✅ Implementar tests de integración para servicios principales
3. ✅ Actualizar documentación API
4. 🆕 **Generar Collections Postman para enseñanza**
5. 🆕 **Implementar Newman CI/CD integration**

### Corto plazo (1 mes):

1. 🔄 Consolidar servicios duplicados
2. 🔄 Estandarizar patrones de respuesta
3. 🔄 Implementar circuit breakers
4. 🆕 **Entrenar aprendices en Postman workflows**
5. 🆕 **Automatizar generación de collections desde Swagger**

### Mediano plazo (3 meses):

1. 🔄 Migrar servicios menores a microservicios
2. 🔄 Implementar API Gateway completo
3. 🔄 Automatizar deployment por servicio
4. 🆕 **Dashboard web para métricas Postman + Newman**
5. 🆕 **Integración con Prometheus/Grafana**

---

**Generado**: Diciembre 2024  
**Última actualización**: \_docs/reportes/CONTEO_ENDPOINTS_BACKEND_SICORA.md  
**Contacto**: Equipo SICORA Development
