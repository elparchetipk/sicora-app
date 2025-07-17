# Bulk Operations - Schedule Service

## Descripción General

El ScheduleService incluye operaciones masivas (bulk operations) que permiten crear múltiples horarios de manera eficiente mediante:

1. **Bulk Create JSON**: Crear múltiples horarios enviando un array JSON
2. **CSV Upload**: Cargar horarios desde archivo CSV

## Endpoints Disponibles

### 1. Bulk Create (JSON)

**Endpoint**: `POST /api/v1/schedules/bulk`

**Autenticación**: Bearer Token requerido

**Permisos**: `schedule.bulk.create`

**Request Body**:
```json
{
  "schedules": [
    {
      "academic_group_id": "550e8400-e29b-41d4-a716-446655440000",
      "instructor_id": "550e8400-e29b-41d4-a716-446655440001",
      "venue_id": "550e8400-e29b-41d4-a716-446655440002",
      "subject": "Programación de Software",
      "day_of_week": 1,
      "start_time": "08:00",
      "end_time": "10:00",
      "block_identifier": "MLUN1",
      "start_date": "2024-01-15",
      "end_date": "2024-06-15"
    },
    {
      "academic_group_id": "550e8400-e29b-41d4-a716-446655440000",
      "instructor_id": "550e8400-e29b-41d4-a716-446655440001",
      "venue_id": "550e8400-e29b-41d4-a716-446655440003",
      "subject": "Base de Datos",
      "day_of_week": 2,
      "start_time": "14:00",
      "end_time": "16:00",
      "block_identifier": "MMAR2",
      "start_date": "2024-01-15",
      "end_date": "2024-06-15"
    }
  ]
}
```

**Response**:
```json
{
  "total": 2,
  "succeeded": 2,
  "errors": 0,
  "created": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440100",
      "academic_group_id": "550e8400-e29b-41d4-a716-446655440000",
      "instructor_id": "550e8400-e29b-41d4-a716-446655440001",
      "venue_id": "550e8400-e29b-41d4-a716-446655440002",
      "subject": "Programación de Software",
      "day_of_week": 1,
      "day_of_week_name": "Lunes",
      "start_time": "08:00",
      "end_time": "10:00",
      "block_identifier": "MLUN1",
      "start_date": "2024-01-15",
      "end_date": "2024-06-15",
      "status": "ACTIVE",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "failed": []
}
```

### 2. CSV Upload

**Endpoint**: `POST /api/v1/schedules/upload-csv`

**Autenticación**: Bearer Token requerido

**Permisos**: `schedule.bulk.create`

**Content-Type**: `multipart/form-data`

**Form Field**: `file` (archivo CSV)

**Formato CSV Esperado**:
```csv
academic_group_id,instructor_id,venue_id,subject,day_of_week,start_time,end_time,block_identifier,start_date,end_date
550e8400-e29b-41d4-a716-446655440000,550e8400-e29b-41d4-a716-446655440001,550e8400-e29b-41d4-a716-446655440002,"Programación de Software",1,08:00,10:00,MLUN1,2024-01-15,2024-06-15
550e8400-e29b-41d4-a716-446655440000,550e8400-e29b-41d4-a716-446655440001,550e8400-e29b-41d4-a716-446655440003,"Base de Datos",2,14:00,16:00,MMAR2,2024-01-15,2024-06-15
550e8400-e29b-41d4-a716-446655440000,550e8400-e29b-41d4-a716-446655440004,550e8400-e29b-41d4-a716-446655440002,"Análisis y Diseño",3,10:00,12:00,MMIE1,2024-01-15,2024-06-15
```

**Response**:
```json
{
  "processed_rows": 3,
  "success_rows": 3,
  "error_rows": 0,
  "errors": [],
  "created": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440100",
      "subject": "Programación de Software",
      "day_of_week_name": "Lunes",
      "start_time": "08:00",
      "end_time": "10:00"
    }
  ],
  "summary": {
    "total_processed": 3,
    "successful": 3,
    "failed": 0,
    "success_rate": 100
  }
}
```

## Validaciones Implementadas

### 1. Validaciones de Negocio
- **Conflictos de horario**: Verifica que no haya superposición de horarios en el mismo ambiente
- **Existencia de entidades**: Valida que existan el grupo académico, instructor y ambiente
- **Rangos de tiempo**: Verifica que la hora de fin sea posterior a la hora de inicio
- **Rangos de fechas**: Verifica que la fecha de fin sea posterior a la fecha de inicio
- **Día de la semana**: Debe ser un valor entre 1 (Lunes) y 7 (Domingo)

### 2. Validaciones de Formato
- **UUIDs**: Todos los IDs deben ser UUIDs válidos
- **Formato de tiempo**: Horas en formato HH:MM (24h)
- **Formato de fecha**: Fechas en formato YYYY-MM-DD
- **Campos requeridos**: Todos los campos son obligatorios

### 3. Límites del Sistema
- **Bulk JSON**: Máximo 100 horarios por operación
- **CSV Upload**: Máximo 5MB de tamaño de archivo
- **Formato de archivo**: Solo archivos .csv son aceptados

## Manejo de Errores

### Errores Parciales
Si algunos horarios fallan y otros son exitosos, el sistema:
- Retorna HTTP Status 207 (Multi-Status)
- Incluye lista detallada de errores con índices
- Procesa todos los horarios válidos
- Proporciona resumen de éxitos y fallos

### Errores Comunes
```json
{
  "total": 2,
  "succeeded": 1,
  "errors": 1,
  "created": [...],
  "failed": [
    {
      "index": 1,
      "error": "academic group not found",
      "details": "academic group 550e8400-e29b-41d4-a716-446655440999 does not exist"
    }
  ]
}
```

## Características Técnicas

### 1. Transaccionalidad
- Cada horario se procesa independientemente
- Errores en un horario no afectan a otros
- Operaciones atómicas por horario individual

### 2. Performance
- Procesamiento secuencial con validaciones completas
- Logging detallado para troubleshooting
- Respuestas con información completa de resultados

### 3. Seguridad
- Autenticación JWT requerida
- Permisos granulares por tipo de operación
- Validación de tamaño de archivos
- Sanitización de entrada de datos

## Ejemplos de Uso

### cURL - Bulk Create
```bash
curl -X POST http://localhost:8002/api/v1/schedules/bulk \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "schedules": [
      {
        "academic_group_id": "550e8400-e29b-41d4-a716-446655440000",
        "instructor_id": "550e8400-e29b-41d4-a716-446655440001",
        "venue_id": "550e8400-e29b-41d4-a716-446655440002",
        "subject": "Programación de Software",
        "day_of_week": 1,
        "start_time": "08:00",
        "end_time": "10:00",
        "block_identifier": "MLUN1",
        "start_date": "2024-01-15",
        "end_date": "2024-06-15"
      }
    ]
  }'
```

### cURL - CSV Upload
```bash
curl -X POST http://localhost:8002/api/v1/schedules/upload-csv \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@schedules.csv"
```
