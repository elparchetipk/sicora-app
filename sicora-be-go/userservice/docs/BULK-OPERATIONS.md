# Bulk Operations - UserService Go

## Descripción

Las operaciones bulk (masivas) permiten realizar múltiples operaciones sobre usuarios en una sola transacción de base de datos, mejorando significativamente el rendimiento cuando se necesita procesar grandes cantidades de datos.

## Endpoints Implementados

### 1. Bulk Create Users
- **Endpoint**: `POST /api/v1/users/bulk`
- **Descripción**: Crea múltiples usuarios en una operación
- **Límite**: Máximo 100 usuarios por solicitud
- **Autenticación**: Requerida (Admin/Coordinador)

**Ejemplo de Request:**
```json
{
  "users": [
    {
      "nombre": "Juan",
      "apellido": "Perez",
      "email": "juan.perez@sena.edu.co",
      "password": "Password123!",
      "documento": "12345678",
      "rol": "aprendiz",
      "ficha_id": "FIC001",
      "programa_formacion": "Análisis y Desarrollo de Software"
    },
    {
      "nombre": "Maria",
      "apellido": "Garcia",
      "email": "maria.garcia@sena.edu.co",
      "password": "Password123!",
      "documento": "87654321",
      "rol": "instructor",
      "programa_formacion": "Sistemas de Información"
    }
  ]
}
```

**Ejemplo de Response:**
```json
{
  "total_processed": 2,
  "success_count": 1,
  "failure_count": 1,
  "message": "Processed 2 users: 1 success, 1 failed",
  "results": [
    {
      "email": "juan.perez@sena.edu.co",
      "success": true,
      "message": "user created successfully",
      "user_id": "550e8400-e29b-41d4-a716-446655440000"
    },
    {
      "email": "maria.garcia@sena.edu.co",
      "success": false,
      "message": "document number already exists"
    }
  ]
}
```

### 2. Bulk Update Users
- **Endpoint**: `PUT /api/v1/users/bulk`
- **Descripción**: Actualiza múltiples usuarios en una operación
- **Límite**: Máximo 100 usuarios por solicitud
- **Autenticación**: Requerida (Admin/Coordinador)

**Ejemplo de Request:**
```json
{
  "users": [
    {
      "email": "juan.perez@sena.edu.co",
      "nombre": "Juan Carlos",
      "programa_formacion": "Desarrollo de Software v2"
    },
    {
      "email": "maria.garcia@sena.edu.co",
      "is_active": false
    }
  ]
}
```

### 3. Bulk Delete Users
- **Endpoint**: `DELETE /api/v1/users/bulk`
- **Descripción**: Elimina múltiples usuarios en una operación
- **Límite**: Máximo 100 usuarios por solicitud
- **Autenticación**: Requerida (Admin/Coordinador)

**Ejemplo de Request:**
```json
{
  "emails": [
    "user1@sena.edu.co",
    "user2@sena.edu.co"
  ]
}
```

### 4. Bulk Change Status
- **Endpoint**: `PATCH /api/v1/users/bulk/status`
- **Descripción**: Cambia el estado de múltiples usuarios en una operación
- **Límite**: Máximo 100 usuarios por solicitud
- **Autenticación**: Requerida (Admin/Coordinador)

**Ejemplo de Request:**
```json
{
  "emails": [
    "user1@sena.edu.co",
    "user2@sena.edu.co"
  ],
  "is_active": false
}
```

## Códigos de Respuesta

- **200 OK**: Operación completada exitosamente
- **207 Multi-Status**: Operación parcialmente exitosa (algunos usuarios procesados, otros fallaron)
- **400 Bad Request**: Todos los usuarios fallaron o datos de entrada inválidos
- **401 Unauthorized**: Token de autenticación inválido
- **403 Forbidden**: Permisos insuficientes
- **500 Internal Server Error**: Error del servidor

## Características Técnicas

### Transaccionalidad
- Todas las operaciones bulk se ejecutan dentro de transacciones de base de datos
- Si ocurre un error crítico, toda la operación se revierte
- Errores individuales no afectan el procesamiento de otros usuarios

### Validaciones
- Validación de estructura de datos con go-playground/validator
- Validación de unicidad de emails y documentos
- Validación de roles y permisos
- Límite de 100 usuarios por operación para evitar timeout

### Manejo de Errores
- Errores detallados por cada usuario procesado
- Clasificación de errores (validación, duplicados, etc.)
- Respuestas estructuradas con contadores de éxito/fallo

### Performance
- Uso de transacciones para operaciones atómicas
- Minimización de consultas a base de datos
- Validación previa antes de operaciones costosas

## Casos de Uso

1. **Migración de Datos**: Importar usuarios desde sistemas legacy
2. **Inscripción Masiva**: Registrar múltiples aprendices en fichas
3. **Gestión de Estado**: Activar/desactivar usuarios por lotes
4. **Actualización de Información**: Actualizar datos masivamente
5. **Limpieza de Datos**: Eliminar usuarios obsoletos

## Limitaciones

- Máximo 100 usuarios por operación
- Solo usuarios con rol admin/coordinador pueden ejecutar operaciones bulk
- Las operaciones de creación requieren contraseñas válidas
- Los emails deben ser únicos en el sistema
- Los documentos deben ser únicos en el sistema

## Logging y Monitoreo

Todas las operaciones bulk generan logs detallados incluyendo:
- Usuario que ejecuta la operación
- Cantidad de registros procesados
- Errores específicos por usuario
- Tiempo de ejecución
- Resultado final de la operación
