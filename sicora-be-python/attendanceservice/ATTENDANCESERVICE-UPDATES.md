# Actualizaciones del Microservicio AttendanceService

## Fecha: 23 de junio de 2025

## Resumen de Cambios

Se han implementado las siguientes mejoras y funcionalidades en el microservicio AttendanceService:

### 1. Implementación de Autenticación JWT Completa

- **Descripción**: Se ha implementado un sistema completo de decodificación de tokens JWT para obtener el ID del usuario autenticado en todos los endpoints.
- **Archivos afectados**:
  - `app/infrastructure/auth/jwt_decoder.py` (nuevo)
  - `app/infrastructure/auth/__init__.py` (nuevo)
  - `app/dependencies.py`
  - `app/presentation/routers/justifications.py`
  - `app/presentation/routers/alerts.py`
  - `app/presentation/routers/attendance.py`
- **Beneficios**:
  - Seguridad mejorada al validar correctamente los tokens JWT
  - Obtención del ID del usuario autenticado para su uso en los casos de uso
  - Eliminación de placeholders UUID("00000000-0000-0000-0000-000000000000")
  - Preparación para implementar control de acceso basado en roles

### 2. Implementación del Caso de Uso para Eliminar Justificaciones

- **Descripción**: Se ha implementado un nuevo caso de uso para permitir a los usuarios eliminar justificaciones pendientes.
- **Archivos afectados**:
  - `app/application/dtos/justification_dtos.py`
  - `app/application/use_cases/delete_justification_use_case.py` (nuevo)
  - `app/application/use_cases/__init__.py`
  - `app/dependencies.py`
  - `app/presentation/routers/justifications.py`
- **Beneficios**:
  - Funcionalidad completa para gestionar el ciclo de vida de las justificaciones
  - Validación de permisos para asegurar que solo el propietario o un administrador pueda eliminar una justificación
  - Verificación de que solo se puedan eliminar justificaciones pendientes

## Próximos Pasos

- Implementar la funcionalidad de alertas de inasistencia consecutiva
- Mejorar la documentación de la API
- Implementar pruebas unitarias y de integración para las nuevas funcionalidades
- Implementar control de acceso basado en roles utilizando la información del token JWT

## Notas Técnicas

### Decodificación de Tokens JWT

La implementación utiliza el paquete `pyjwt` para decodificar los tokens JWT y extraer el ID del usuario. La clave secreta y el algoritmo se configuran en el archivo `config.py`.

```python
# Ejemplo de decodificación de token JWT
payload = jwt.decode(
    token,
    settings.JWT_SECRET_KEY,
    algorithms=[settings.JWT_ALGORITHM]
)
user_id = payload.get("sub")
```

### Eliminación de Justificaciones

La implementación verifica que:
1. La justificación exista
2. La justificación esté en estado pendiente
3. El usuario tenga permisos para eliminarla (sea el propietario o un administrador)

```python
# Validar permisos del usuario
user_info = await self.user_service.get_user_info(request.user_id)
is_admin = user_info.get("role") == "admin"
is_owner = justification.student_id == request.user_id

if not (is_admin or is_owner):
    raise UnauthorizedAccessError(
        f"delete justification {justification.id}",
        "student or admin"
    )
```