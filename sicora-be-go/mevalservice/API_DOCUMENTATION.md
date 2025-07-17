# MEvalService API Documentation

## Overview

MEvalService es el microservicio para la gestión de Comités de Seguimiento y Evaluación Académico/Disciplinario del SENA, implementado según el Acuerdo 009 de 2024.

## Base URL

```
http://localhost:8080/api/v1
```

## Health Check

### GET /health

Verifica el estado del servicio.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "MEvalService",
  "version": "1.0.0"
}
```

## Committees (Comités)

### POST /committees

Crea un nuevo comité.

**Request Body:**

```json
{
  "name": "Comité Académico Enero 2024",
  "type": "ACADEMIC", // ACADEMIC | DISCIPLINARY
  "subType": "MONTHLY", // MONTHLY | EXTRAORDINARY | APPEAL | SPECIAL
  "center": "Centro Biotecnología Industrial",
  "startDate": "2024-01-01T09:00:00Z",
  "endDate": "2024-01-31T17:00:00Z",
  "description": "Comité mensual para evaluación académica"
}
```

**Response (201):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Comité Académico Enero 2024",
  "type": "ACADEMIC",
  "subType": "MONTHLY",
  "center": "Centro Biotecnología Industrial",
  "status": "ACTIVE",
  "startDate": "2024-01-01T09:00:00Z",
  "endDate": "2024-01-31T17:00:00Z",
  "description": "Comité mensual para evaluación académica",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

### GET /committees

Obtiene todos los comités.

### GET /committees/{id}

Obtiene un comité por ID.

### PUT /committees/{id}

Actualiza un comité.

### DELETE /committees/{id}

Elimina un comité.

### GET /committees/by-center?center={center}

Obtiene comités por centro de formación.

### GET /committees/by-type?type={type}

Obtiene comités por tipo.

## Student Cases (Casos de Estudiantes)

### POST /student-cases

Crea un nuevo caso de estudiante.

**Request Body:**

```json
{
  "studentId": "123e4567-e89b-12d3-a456-426614174001",
  "committeeId": "123e4567-e89b-12d3-a456-426614174000",
  "caseNumber": "CASE-2024-001",
  "type": "ACADEMIC", // ACADEMIC | DISCIPLINARY
  "severity": "MEDIUM", // LOW | MEDIUM | HIGH | CRITICAL
  "priority": "NORMAL", // LOW | NORMAL | HIGH | URGENT
  "title": "Bajo rendimiento académico",
  "description": "El estudiante presenta calificaciones deficientes en múltiples competencias",
  "evidence": "Notas del trimestre, reportes de instructores",
  "reportedBy": "123e4567-e89b-12d3-a456-426614174002",
  "dueDate": "2024-02-15T17:00:00Z"
}
```

**Response (201):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174003",
  "studentId": "123e4567-e89b-12d3-a456-426614174001",
  "committeeId": "123e4567-e89b-12d3-a456-426614174000",
  "caseNumber": "CASE-2024-001",
  "type": "ACADEMIC",
  "severity": "MEDIUM",
  "status": "OPEN",
  "priority": "NORMAL",
  "title": "Bajo rendimiento académico",
  "description": "El estudiante presenta calificaciones deficientes en múltiples competencias",
  "evidence": "Notas del trimestre, reportes de instructores",
  "reportedBy": "123e4567-e89b-12d3-a456-426614174002",
  "reportDate": "2024-01-15T10:30:00Z",
  "dueDate": "2024-02-15T17:00:00Z",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

### GET /student-cases/{id}

Obtiene un caso por ID.

### PUT /student-cases/{id}

Actualiza un caso.

### GET /student-cases/by-student?studentId={id}

Obtiene casos por estudiante.

### GET /student-cases/pending

Obtiene casos pendientes.

### GET /student-cases/overdue

Obtiene casos vencidos.

## Improvement Plans (Planes de Mejoramiento)

### POST /improvement-plans

Crea un plan de mejoramiento.

**Request Body:**

```json
{
  "studentCaseId": "123e4567-e89b-12d3-a456-426614174003",
  "studentId": "123e4567-e89b-12d3-a456-426614174001",
  "supervisorId": "123e4567-e89b-12d3-a456-426614174004",
  "planNumber": "PLAN-2024-001",
  "title": "Plan de Recuperación Académica",
  "description": "Plan integral para mejorar el rendimiento académico del estudiante",
  "objectives": "Alcanzar calificaciones aprobatorias en todas las competencias",
  "activities": "Tutorías semanales, trabajo en grupos de estudio, talleres de refuerzo",
  "resources": "Material didáctico, acceso a laboratorios, apoyo psicopedagógico",
  "timeline": "3 meses con seguimiento semanal",
  "evaluationCriteria": "Evaluaciones mensuales, participación en actividades",
  "startDate": "2024-01-20T09:00:00Z",
  "endDate": "2024-04-20T17:00:00Z"
}
```

### GET /improvement-plans/{id}

Obtiene un plan por ID.

### PUT /improvement-plans/{id}

Actualiza un plan.

### GET /improvement-plans/student-case/{studentCaseId}

Obtiene planes por caso de estudiante.

### PATCH /improvement-plans/{id}/progress

Actualiza el progreso del plan.

**Request Body:**

```json
{
  "progress": 75,
  "notes": "El estudiante muestra gran mejora en matemáticas y ciencias"
}
```

## Sanctions (Sanciones)

### POST /sanctions

Crea una sanción.

**Request Body:**

```json
{
  "studentCaseId": "123e4567-e89b-12d3-a456-426614174003",
  "studentId": "123e4567-e89b-12d3-a456-426614174001",
  "sanctionNumber": "SANC-2024-001",
  "type": "LLAMADO_ATENCION", // LLAMADO_ATENCION | CONDICIONAMIENTO | CANCELACION_MATRICULA
  "severity": "LOW", // LOW | MEDIUM | HIGH
  "title": "Llamado de atención por inasistencias",
  "description": "Llamado de atención formal por exceso de faltas injustificadas",
  "startDate": "2024-01-20T09:00:00Z",
  "endDate": "2024-02-20T17:00:00Z",
  "conditions": "Asistir puntualmente a todas las clases",
  "requiredActions": "Presentar justificación médica para futuras inasistencias",
  "issuedBy": "123e4567-e89b-12d3-a456-426614174005",
  "approvedBy": "123e4567-e89b-12d3-a456-426614174006"
}
```

### GET /sanctions/{id}

Obtiene una sanción por ID.

### GET /sanctions/student/{studentId}

Obtiene sanciones por estudiante.

### PATCH /sanctions/{id}/activate

Activa una sanción.

### PATCH /sanctions/{id}/complete

Marca una sanción como completada.

## Appeals (Apelaciones)

### POST /appeals

Crea una apelación.

**Request Body:**

```json
{
  "studentCaseId": "123e4567-e89b-12d3-a456-426614174003",
  "studentId": "123e4567-e89b-12d3-a456-426614174001",
  "appealNumber": "APP-2024-001",
  "type": "DECISION_APPEAL", // DECISION_APPEAL | SANCTION_APPEAL | PROCESS_APPEAL
  "reason": "Considero que la decisión fue injusta y no se basó en evidencia completa",
  "evidence": "Documentación adicional que demuestra asistencia",
  "requestedBy": "123e4567-e89b-12d3-a456-426614174001",
  "requestDate": "2024-01-25T10:00:00Z",
  "priority": "HIGH"
}
```

### GET /appeals/{id}

Obtiene una apelación por ID.

### GET /appeals/student/{studentId}

Obtiene apelaciones por estudiante.

### PATCH /appeals/{id}/process

Procesa una apelación (acepta/rechaza).

**Request Body:**

```json
{
  "accepted": true,
  "resolution": "Apelación aceptada. Decisión original revertida tras revisión de evidencia adicional."
}
```

## Error Responses

Todos los endpoints pueden retornar los siguientes errores:

### 400 Bad Request

```json
{
  "error": "Invalid request",
  "message": "Campo requerido faltante: title"
}
```

### 404 Not Found

```json
{
  "error": "Resource not found",
  "message": "Committee with the specified ID was not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "message": "Failed to connect to database"
}
```

## Success Responses

Para operaciones que no retornan datos específicos:

```json
{
  "success": true,
  "message": "Operation completed successfully"
}
```

## Status Values

### Committee Status

- `ACTIVE`: Comité activo
- `INACTIVE`: Comité inactivo
- `COMPLETED`: Comité completado
- `CANCELLED`: Comité cancelado

### Case Status

- `OPEN`: Caso abierto
- `IN_PROGRESS`: En progreso
- `UNDER_REVIEW`: Bajo revisión
- `RESOLVED`: Resuelto
- `CLOSED`: Cerrado
- `APPEALED`: Apelado

### Plan Status

- `DRAFT`: Borrador
- `ACTIVE`: Activo
- `IN_PROGRESS`: En progreso
- `COMPLETED`: Completado
- `CANCELLED`: Cancelado
- `SUSPENDED`: Suspendido

### Sanction Status

- `DRAFT`: Borrador
- `ACTIVE`: Activa
- `COMPLETED`: Completada
- `REVOKED`: Revocada
- `SUSPENDED`: Suspendida

### Appeal Status

- `SUBMITTED`: Enviada
- `UNDER_REVIEW`: Bajo revisión
- `ACCEPTED`: Aceptada
- `REJECTED`: Rechazada
- `WITHDRAWN`: Retirada

## Authentication

**Nota:** En la versión actual, la autenticación no está implementada. En producción, todos los endpoints deberían requerir autenticación JWT.

```
Authorization: Bearer <jwt_token>
```

## Rate Limiting

**Nota:** No implementado en la versión actual. En producción, se recomienda implementar rate limiting.

## Pagination

Para endpoints que retornan listas, se puede implementar paginación:

```
GET /committees?page=1&limit=10&sort=createdAt&order=desc
```

## Filtering

Muchos endpoints soportan filtros adicionales:

```
GET /student-cases?status=OPEN&type=ACADEMIC&priority=HIGH
```

## Automated Jobs

El sistema incluye trabajos automáticos que se ejecutan en segundo plano:

- **Creación de comités mensuales**: Primer lunes de cada mes a las 09:00
- **Alertas de casos vencidos**: Todos los días a las 08:00
- **Verificación de progreso de planes**: Todos los lunes a las 10:00
- **Verificación de vencimiento de sanciones**: Todos los días a las 07:00
- **Alertas de plazos de apelaciones**: Todos los días a las 09:00
- **Reportes mensuales**: Último día del mes a las 17:00

## Environment Variables

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=sicora_mevalservice
DB_SSLMODE=disable
DB_TIMEZONE=UTC

# Application
APP_ENV=development
PORT=8080

# Test Database
TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_USER=postgres
TEST_DB_PASSWORD=password
TEST_DB_NAME=mevalservice_test
TEST_DB_SSLMODE=disable
```
