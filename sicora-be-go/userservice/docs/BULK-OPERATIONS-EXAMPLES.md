# Bulk Operations Examples

Este archivo contiene ejemplos de uso para las operaciones bulk del UserService Go.

## Configuración para Pruebas

### Variables de Entorno
```bash
export JWT_SECRET="your-secret-key-for-testing"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="sicora_userservice"
export DB_USER="sicora_user"
export DB_PASSWORD="sicora_password"
```

### Obtener Token de Autenticación
```bash
# Login como admin
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@sena.edu.co",
    "password": "admin123"
  }'
```

## Ejemplos de Operaciones Bulk

### 1. Crear Usuarios Masivamente

```bash
curl -X POST http://localhost:8001/api/v1/users/bulk \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "users": [
      {
        "nombre": "Carlos",
        "apellido": "Rodriguez",
        "email": "carlos.rodriguez@sena.edu.co",
        "password": "Password123!",
        "documento": "11111111",
        "rol": "aprendiz",
        "ficha_id": "FIC001",
        "programa_formacion": "Análisis y Desarrollo de Software"
      },
      {
        "nombre": "Ana",
        "apellido": "Martinez",
        "email": "ana.martinez@sena.edu.co",
        "password": "Password123!",
        "documento": "22222222",
        "rol": "aprendiz",
        "ficha_id": "FIC001",
        "programa_formacion": "Análisis y Desarrollo de Software"
      },
      {
        "nombre": "Luis",
        "apellido": "Gonzalez",
        "email": "luis.gonzalez@sena.edu.co",
        "password": "Password123!",
        "documento": "33333333",
        "rol": "instructor",
        "programa_formacion": "Desarrollo de Software"
      }
    ]
  }'
```

### 2. Actualizar Usuarios Masivamente

```bash
curl -X PUT http://localhost:8001/api/v1/users/bulk \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "users": [
      {
        "email": "carlos.rodriguez@sena.edu.co",
        "programa_formacion": "Desarrollo de Software Avanzado"
      },
      {
        "email": "ana.martinez@sena.edu.co",
        "ficha_id": "FIC002"
      }
    ]
  }'
```

### 3. Cambiar Estado Masivamente

```bash
# Desactivar usuarios
curl -X PATCH http://localhost:8001/api/v1/users/bulk/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "emails": [
      "carlos.rodriguez@sena.edu.co",
      "ana.martinez@sena.edu.co"
    ],
    "is_active": false
  }'

# Activar usuarios
curl -X PATCH http://localhost:8001/api/v1/users/bulk/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "emails": [
      "carlos.rodriguez@sena.edu.co",
      "ana.martinez@sena.edu.co"
    ],
    "is_active": true
  }'
```

### 4. Eliminar Usuarios Masivamente

```bash
curl -X DELETE http://localhost:8001/api/v1/users/bulk \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "emails": [
      "carlos.rodriguez@sena.edu.co",
      "ana.martinez@sena.edu.co"
    ]
  }'
```

## Respuestas Esperadas

### Respuesta Exitosa (200 OK)
```json
{
  "total_processed": 3,
  "success_count": 3,
  "failure_count": 0,
  "message": "Processed 3 users: 3 success, 0 failed",
  "results": [
    {
      "email": "carlos.rodriguez@sena.edu.co",
      "success": true,
      "message": "user created successfully",
      "user_id": "550e8400-e29b-41d4-a716-446655440001"
    },
    {
      "email": "ana.martinez@sena.edu.co",
      "success": true,
      "message": "user created successfully",
      "user_id": "550e8400-e29b-41d4-a716-446655440002"
    },
    {
      "email": "luis.gonzalez@sena.edu.co",
      "success": true,
      "message": "user created successfully",
      "user_id": "550e8400-e29b-41d4-a716-446655440003"
    }
  ]
}
```

### Respuesta Parcial (207 Multi-Status)
```json
{
  "total_processed": 2,
  "success_count": 1,
  "failure_count": 1,
  "message": "Processed 2 users: 1 success, 1 failed",
  "results": [
    {
      "email": "new.user@sena.edu.co",
      "success": true,
      "message": "user created successfully",
      "user_id": "550e8400-e29b-41d4-a716-446655440004"
    },
    {
      "email": "duplicate.user@sena.edu.co",
      "success": false,
      "message": "user already exists"
    }
  ]
}
```

### Respuesta de Error (400 Bad Request)
```json
{
  "error": "INVALID_INPUT",
  "message": "Invalid request format",
  "data": {
    "details": "validation error: users is required"
  }
}
```

## Scripts de Prueba

### Script para Crear Datos de Prueba
```bash
#!/bin/bash

# Obtener token
TOKEN=$(curl -s -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@sena.edu.co", "password": "admin123"}' | \
  jq -r '.data.access_token')

# Crear usuarios de prueba
curl -X POST http://localhost:8001/api/v1/users/bulk \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @bulk_users_example.json

echo "Bulk users created"
```

### Archivo bulk_users_example.json
```json
{
  "users": [
    {
      "nombre": "Usuario",
      "apellido": "Prueba1",
      "email": "test1@sena.edu.co",
      "password": "Password123!",
      "documento": "10000001",
      "rol": "aprendiz",
      "ficha_id": "FIC001",
      "programa_formacion": "Test Program"
    },
    {
      "nombre": "Usuario",
      "apellido": "Prueba2",
      "email": "test2@sena.edu.co",
      "password": "Password123!",
      "documento": "10000002",
      "rol": "aprendiz",
      "ficha_id": "FIC001",
      "programa_formacion": "Test Program"
    }
  ]
}
```

## Comandos de Verificación

### Verificar Usuarios Creados
```bash
curl -X GET http://localhost:8001/api/v1/users \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Verificar Usuario Específico
```bash
curl -X GET http://localhost:8001/api/v1/users/USER_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
