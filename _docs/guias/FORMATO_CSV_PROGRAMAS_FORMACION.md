# 📚 Formato CSV para Carga de Programas de Formación SICORA

**Fecha:** 3 de julio de 2025  
**Versión:** 1.0  
**Ubicación:** `/sicora-app/_docs/guias/`

## 🎯 Propósito

Especificación del formato CSV requerido para la carga masiva de programas de formación académica en la base de datos SICORA, conforme a la estructura del SENA y las entidades del sistema.

## 📋 Estructura del Archivo CSV

### Formato Requerido

```csv
id,name,code,type,duration,description,is_active,created_at
```

### Campos Obligatorios

| Campo      | Tipo    | Descripción                      | Validaciones                                                                    | Ejemplo                                |
| ---------- | ------- | -------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------- |
| `id`       | UUID v4 | Identificador único del programa | Formato UUID válido                                                             | `550e8400-e29b-41d4-a716-446655440000` |
| `name`     | String  | Nombre completo del programa     | Min: 5 chars, Max: 200 chars                                                    | `Análisis y Desarrollo de Software`    |
| `code`     | String  | Código único del programa        | Min: 2 chars, Max: 20 chars, MAYÚSCULAS                                         | `ADSO`                                 |
| `type`     | Enum    | Tipo de programa SENA            | Valores permitidos: `TECNICO`, `TECNOLOGO`, `ESPECIALIZACION`, `COMPLEMENTARIO` | `TECNOLOGO`                            |
| `duration` | Integer | Duración en meses                | Min: 1, Max: 60 meses                                                           | `24`                                   |

### Campos Opcionales

| Campo         | Tipo     | Descripción              | Validaciones                       | Ejemplo                                                       |
| ------------- | -------- | ------------------------ | ---------------------------------- | ------------------------------------------------------------- |
| `description` | String   | Descripción del programa | Max: 1000 chars                    | `Programa de formación integral en desarrollo de software...` |
| `is_active`   | Boolean  | Estado del programa      | `true` o `false` (default: `true`) | `true`                                                        |
| `created_at`  | DateTime | Fecha de creación        | ISO 8601 UTC                       | `2025-07-03T10:30:00Z`                                        |

## 🔧 Uso del Archivo CSV

### Opción 1: Script de Carga Automática (Recomendado)

El script `validate-programs-csv.py` puede procesar el archivo CSV y realizar llamadas individuales a la API:

```bash
# Validar CSV y cargar programas
cd /sicora-app/scripts/
python validate-programs-csv.py --file ../sicora-shared/sample-data/templates/programas_formacion.csv --upload

# Solo validar (sin cargar)
python validate-programs-csv.py --file ../sicora-shared/sample-data/templates/programas_formacion.csv
```

### Opción 2: Carga Manual por Programa

Para cada fila del CSV, realizar una llamada POST individual:

**Backend Python:**

```bash
curl -X POST "http://localhost:8000/api/v1/admin/programs" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Análisis y Desarrollo de Software",
    "code": "ADSO",
    "program_type": "TECNOLOGO",
    "duration_months": 24,
    "description": "Programa de formación integral...",
    "is_active": true
  }'
```

**Backend Go:**

```bash
curl -X POST "http://localhost:8080/api/v1/master-data/academic-programs" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Análisis y Desarrollo de Software",
    "code": "ADSO",
    "type": "TECNOLOGO",
    "duration": 24,
    "description": "Programa de formación integral...",
    "is_active": true
  }'
```

### Opción 3: Implementar Endpoint Bulk (Futuro)

Una vez implementado el endpoint de carga masiva, se podrá enviar el archivo CSV directamente:

```bash
curl -X POST "http://localhost:8000/api/v1/admin/programs/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@programas_formacion.csv"
```

## 🔧 Especificaciones Técnicas

### Configuración del Archivo

- **Encoding:** UTF-8 con BOM
- **Separador:** Coma (`,`)
- **Line Endings:** LF (Unix style)
- **Header:** Obligatorio en la primera línea
- **Extensión:** `.csv`

### Validaciones de Negocio SENA

#### Tipos de Programa Válidos

- **`TECNICO`**: Programas técnicos del SENA (duración típica: 12-18 meses)
- **`TECNOLOGO`**: Programas tecnológicos (duración típica: 24-30 meses)
- **`ESPECIALIZACION`**: Especializaciones técnicas (duración típica: 6-12 meses)
- **`COMPLEMENTARIO`**: Cursos complementarios y cortos (duración típica: 1-6 meses)

#### Reglas de Unicidad

- **`code`**: Debe ser único en todo el sistema
- **`name`**: Debe ser único por tipo de programa
- **`id`**: UUID único global

## 📝 Ejemplos de Uso

### Ejemplo 1: Programa ADSO (Tecnólogo)

```csv
id,name,code,type,duration,description,is_active,created_at
550e8400-e29b-41d4-a716-446655440001,"Análisis y Desarrollo de Software",ADSO,TECNOLOGO,24,"Programa de formación integral en desarrollo de software con enfoque en metodologías ágiles y tecnologías modernas",true,2025-07-03T10:30:00Z
```

### Ejemplo 2: Múltiples Programas

```csv
id,name,code,type,duration,description,is_active,created_at
550e8400-e29b-41d4-a716-446655440001,"Análisis y Desarrollo de Software",ADSO,TECNOLOGO,24,"Programa de formación integral en desarrollo de software",true,2025-07-03T10:30:00Z
550e8400-e29b-41d4-a716-446655440002,"Gestión de Redes de Datos",GRD,TECNOLOGO,24,"Programa enfocado en administración de infraestructura de redes",true,2025-07-03T10:30:00Z
550e8400-e29b-41d4-a716-446655440003,"Sistemas",SIS,TECNICO,18,"Programa técnico en mantenimiento de sistemas",true,2025-07-03T10:30:00Z
550e8400-e29b-41d4-a716-446655440004,"Inglés Básico",ENG1,COMPLEMENTARIO,3,"Curso complementario de inglés nivel básico",true,2025-07-03T10:30:00Z
```

### Ejemplo 3: Plantilla Vacía

```csv
id,name,code,type,duration,description,is_active,created_at
```

## 🛠️ Herramientas de Validación

### Script de Validación Python

```python
import pandas as pd
import uuid
from datetime import datetime

def validate_programs_csv(file_path):
    """Valida archivo CSV de programas de formación."""

    # Leer CSV
    df = pd.read_csv(file_path)

    # Validaciones
    errors = []

    # Campos obligatorios
    required_fields = ['id', 'name', 'code', 'type', 'duration']
    for field in required_fields:
        if field not in df.columns:
            errors.append(f"Campo obligatorio faltante: {field}")

    # Tipos de programa válidos
    valid_types = ['TECNICO', 'TECNOLOGO', 'ESPECIALIZACION', 'COMPLEMENTARIO']
    invalid_types = df[~df['type'].isin(valid_types)]
    if not invalid_types.empty:
        errors.append(f"Tipos inválidos encontrados: {invalid_types['type'].unique()}")

    # Validar UUIDs
    for idx, row in df.iterrows():
        try:
            uuid.UUID(str(row['id']))
        except ValueError:
            errors.append(f"Fila {idx+2}: ID no es un UUID válido: {row['id']}")

    # Validar duración
    invalid_duration = df[(df['duration'] < 1) | (df['duration'] > 60)]
    if not invalid_duration.empty:
        errors.append("Duraciones inválidas (debe estar entre 1 y 60 meses)")

    return errors

# Uso
errors = validate_programs_csv('programas_formacion.csv')
if errors:
    print("❌ Errores encontrados:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ Archivo CSV válido")
```

### Script de Generación Go

```go
package main

import (
    "encoding/csv"
    "os"
    "time"
    "github.com/google/uuid"
)

func generateProgramsCSV(filename string) error {
    file, err := os.Create(filename)
    if err != nil {
        return err
    }
    defer file.Close()

    writer := csv.NewWriter(file)
    defer writer.Flush()

    // Header
    header := []string{"id", "name", "code", "type", "duration", "description", "is_active", "created_at"}
    writer.Write(header)

    // Ejemplo de programa
    program := []string{
        uuid.New().String(),
        "Análisis y Desarrollo de Software",
        "ADSO",
        "TECNOLOGO",
        "24",
        "Programa de formación en desarrollo de software",
        "true",
        time.Now().UTC().Format(time.RFC3339),
    }
    writer.Write(program)

    return nil
}
```

## 🔍 Validaciones Automáticas del Sistema

### Backend Go (ScheduleService)

El sistema valida automáticamente:

- Formato UUID del campo `id`
- Longitud mínima/máxima de campos
- Tipos de programa permitidos
- Unicidad de códigos
- Rango de duración válido

### Backend Python (ScheduleService)

Incluye validaciones adicionales:

- Formato ISO 8601 para fechas
- Enum validation para `ProgramType`
- Business rules específicas del SENA
- Consistencia referencial

## 📂 Ubicación de Archivos

### Estructura Recomendada

```
sicora-app/
├── sicora-shared/
│   └── sample-data/
│       ├── imports/
│       │   └── programs/
│       │       └── programas_formacion.csv
│       └── templates/
│           └── programs.template.csv
```

### Endpoints Disponibles

#### Backend Go (ScheduleService)

- **Crear programa individual:** `POST /api/v1/master-data/academic-programs`
- **Listar programas:** `GET /api/v1/master-data/academic-programs`

#### Backend Python (ScheduleService)

- **Crear programa individual:** `POST /api/v1/admin/programs`
- **Listar programas:** `GET /api/v1/admin/programs`

**⚠️ Nota Importante:** Actualmente NO existen endpoints de carga masiva (bulk) implementados para programas académicos.

#### Referencia: Endpoint de Bulk Upload Existente (Schedules)

El backend Python incluye un endpoint de ejemplo para carga masiva de horarios:

- **Carga masiva de horarios:** `POST /api/v1/admin/schedules/upload`

Este endpoint acepta archivos CSV y procesa múltiples registros en una sola operación, sirviendo como referencia para implementar funcionalidad similar para programas académicos.

#### Implementación Sugerida para Programas

Para implementar carga masiva de programas académicos, se sugiere:

**Backend Python:**

```python
@router.post("/programs/upload", response_model=BulkUploadResultResponse)
async def bulk_upload_programs(
    file: UploadFile = File(...),
    use_case: BulkUploadProgramsUseCase = Depends(get_bulk_upload_programs_use_case),
):
    """Bulk upload academic programs from CSV file."""
```

**Backend Go:**

```go
func (h *MasterDataHandler) BulkUploadAcademicPrograms(c *gin.Context) {
    // Implementation for bulk upload of academic programs
}
```

## 🚨 Errores Comunes y Soluciones

### Error: "Tipo de programa inválido"

**Causa:** Usar valores no permitidos en el campo `type`
**Solución:** Usar solo: `TECNICO`, `TECNOLOGO`, `ESPECIALIZACION`, `COMPLEMENTARIO`

### Error: "Código duplicado"

**Causa:** Intentar cargar un programa con código ya existente
**Solución:** Verificar unicidad de códigos antes de la carga

### Error: "UUID inválido"

**Causa:** Formato incorrecto en el campo `id`
**Solución:** Generar UUIDs válidos usando herramientas apropiadas

### Error: "Duración fuera de rango"

**Causa:** Valores de duración menores a 1 o mayores a 60
**Solución:** Ajustar duración según los límites del SENA

## 📊 Límites y Restricciones

### Volumen de Carga

- **Máximo recomendado:** 1,000 programas por archivo
- **Tamaño máximo:** 10 MB por archivo CSV
- **Timeout:** 5 minutos por proceso de carga

### Restricciones de Negocio

- Un código de programa debe ser único globalmente
- Los programas TECNOLOGO requieren duración mínima de 18 meses
- Los cursos COMPLEMENTARIOS no pueden exceder 12 meses

## 🔗 Relaciones con Otras Entidades

### Dependencias

Después de cargar programas, se pueden cargar:

- **Fichas/Grupos Académicos:** Que referencian programas
- **Horarios:** Que dependen de fichas y programas
- **Usuarios:** Aprendices matriculados en programas específicos

### Orden de Carga Recomendado

1. Programas de Formación (este CSV)
2. Campus y Sedes
3. Aulas/Venues
4. Usuarios (Instructores)
5. Fichas/Grupos Académicos
6. Horarios

## 📞 Soporte

Para dudas sobre este formato CSV:

- **Backend Go:** Ver documentación en `/scheduleservice/docs/`
- **Backend Python:** Ver documentación en `/scheduleservice/app/docs/`
- **Validaciones:** Ejecutar scripts de validación antes de carga
- **Logs:** Revisar logs del sistema para errores específicos

---

**✅ Esta especificación está alineada con:**

- Reglamento del Aprendiz SENA (Acuerdo 009 de 2024)
- Arquitectura multistack SICORA
- Estándares de validación del sistema
- Convenciones de carga masiva del proyecto
