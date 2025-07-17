# Middleware de Autenticación Optimizado - UserService Go

## Resumen

Se ha implementado un sistema de middleware de autenticación optimizado para el UserService en Go, proporcionando seguridad robusta, gestión avanzada de JWT y middlewares adicionales para una aplicación de nivel enterprise.

## Componentes Implementados

### 1. Servicio JWT (`jwt_service.go`)

**Ubicación**: `internal/infrastructure/auth/jwt_service.go`

**Características**:
- Claims customizados con información completa del usuario
- Generación y validación de tokens JWT
- Soporte para refresh tokens
- Configuración flexible de expiración

**Estructura de Claims**:
```go
type UserClaims struct {
    UserID            uuid.UUID `json:"user_id"`
    Email             string    `json:"email"`
    Role              string    `json:"role"`
    IsActive          bool      `json:"is_active"`
    MustChangePassword bool     `json:"must_change_password"`
    jwt.RegisteredClaims
}
```

### 2. Middleware de Autenticación V2 (`auth_v2.go`)

**Ubicación**: `internal/presentation/middleware/auth_v2.go`

**Funcionalidades**:
- Autenticación JWT con validación robusta
- Extracción automática de información del usuario al contexto
- Validación de estado de usuario activo
- Manejo de rutas que requieren cambio de contraseña
- Sistema de permisos basado en roles

**Middlewares Disponibles**:
- `AuthMiddlewareV2`: Autenticación principal con JWT
- `RequireRoleMiddleware`: Verificación de roles específicos
- `RequirePermissionMiddleware`: Verificación de permisos granulares
- `RequireActiveUserMiddleware`: Verificación de estado activo
- `RequirePasswordChangeMiddleware`: Verificación de cambio de contraseña obligatorio

### 3. Middlewares Avanzados (`advanced.go`)

**Ubicación**: `internal/presentation/middleware/advanced.go`

**Características**:
- Rate limiting por IP
- Headers de seguridad
- Logging avanzado con request ID
- Compresión automática
- Timeout de requests
- Manejo de errores robusto

### 4. Helpers de Contexto

**Funciones Utilitarias**:
```go
GetUserID(c *gin.Context) (uuid.UUID, error)
GetUserRole(c *gin.Context) (string, error)
IsAdmin(c *gin.Context) bool
IsCoordinador(c *gin.Context) bool
CanManageUsers(c *gin.Context) bool
```

## Configuración

### Variables de Entorno
```bash
JWT_SECRET=your-jwt-secret-key
GIN_MODE=release  # Para producción
```

### Configuración del Middleware
```go
authConfig := &middleware.AuthConfig{
    JWTService: jwtService,
    SkipPaths: []string{
        "/health",
        "/docs",
        "/swagger",
        "/api/v1/auth",
        "/api/v1/users", // Solo para POST (registro)
    },
    CacheTTL:        5 * time.Minute,
    EnableBlacklist: true,
}
```

## Integración en Rutas

### Rutas Públicas
- `/api/v1/auth/*` - Login, logout, recuperación de contraseña
- `/api/v1/users` (POST) - Registro de usuarios

### Rutas Protegidas
- Autenticación JWT requerida
- Usuario debe estar activo
- Validación de cambio de contraseña obligatorio

### Rutas de Administrador
- Autenticación JWT requerida
- Usuario debe estar activo
- Rol de admin o coordinador requerido

## Sistema de Permisos

### Roles y Permisos
```go
const (
    PermUserCreate     = "user.create"
    PermUserRead       = "user.read"
    PermUserUpdate     = "user.update"
    PermUserDelete     = "user.delete"
    PermUserBulkCreate = "user.bulk.create"
    PermUserBulkUpdate = "user.bulk.update"
    PermUserBulkDelete = "user.bulk.delete"
    PermUserManage     = "user.manage"
    PermSystemAdmin    = "system.admin"
)
```

### Mapeo de Roles
- **admin**: Todos los permisos
- **coordinador**: Gestión básica de usuarios, operaciones bulk
- **instructor**: Lectura de usuarios, gestión de horarios
- **aprendiz**: Solo perfil personal y lectura de horarios

## Stack de Middlewares

### Orden de Aplicación Global
1. `RequestIDMiddleware` - Generación de ID único por request
2. `SecurityHeadersMiddleware` - Headers de seguridad HTTP
3. `LoggingMiddleware` - Logging de requests/responses
4. `CORSMiddleware` - Configuración de CORS
5. `RateLimitMiddleware` - Rate limiting (100 req/min)
6. `CompressionMiddleware` - Compresión gzip
7. `TimeoutMiddleware` - Timeout de 30 segundos
8. `ErrorMiddleware` - Manejo centralizado de errores
9. `NotFoundMiddleware` - Respuestas 404 consistentes

### Orden de Aplicación en Rutas Protegidas
1. `AuthMiddlewareV2` - Autenticación JWT
2. `RequireActiveUserMiddleware` - Verificación de usuario activo
3. `RequirePasswordChangeMiddleware` - Verificación de cambio de contraseña
4. `RequireRoleMiddleware` - Verificación de roles (solo rutas admin)

## Rate Limiting

### Configuración
- **Límite**: 100 requests por minuto por IP
- **Ventana**: 1 minuto
- **Estrategia**: Sliding window
- **Limpieza**: Automática de requests expirados

### Headers de Respuesta
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Seguridad

### Headers de Seguridad Aplicados
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'
```

### Validaciones JWT
- Verificación de firma
- Validación de expiración
- Verificación de issuer
- Verificación de claims customizados

## Logging

### Información Registrada
- Request ID único
- Método HTTP y path
- IP del cliente
- User-Agent
- Tiempo de respuesta
- Status code
- Información del usuario autenticado (si aplica)

### Formato de Log
```
[USERSERVICE-GO] 2024/01/01 12:00:00 [INFO] [req-123] GET /api/v1/users/profile user:john@example.com role:admin 200 45ms
```

## Testing y Validación

### Casos de Prueba Principales
1. **Autenticación exitosa** con token válido
2. **Rechazo** de tokens inválidos/expirados
3. **Validación de roles** en rutas protegidas
4. **Rate limiting** funcionando correctamente
5. **Headers de seguridad** presentes
6. **Logging** completo de requests

### Comandos de Validación
```bash
# Verificar health check
curl http://localhost:8002/health

# Test de autenticación
curl -H "Authorization: Bearer <token>" http://localhost:8002/api/v1/users/profile

# Test de rate limiting (ejecutar 100+ veces)
for i in {1..110}; do curl http://localhost:8002/health; done
```

## Beneficios del Middleware Optimizado

### Seguridad
- Autenticación robusta con JWT
- Validación de estado de usuario
- Sistema de permisos granular
- Headers de seguridad automáticos
- Rate limiting para prevenir ataques

### Performance
- Cache de validaciones JWT (5 min TTL)
- Compresión automática de respuestas
- Logging eficiente con request ID
- Timeout para prevenir recursos colgados

### Mantenibilidad
- Separación clara de responsabilidades
- Helpers de contexto reutilizables
- Configuración centralizada
- Middlewares modulares y composables

### Observabilidad
- Logging estructurado con contexto
- Request ID para trazabilidad
- Métricas de rate limiting
- Headers informativos de estado

## Próximos Pasos

1. **Implementar cache de blacklist** para tokens revocados
2. **Agregar métricas** de middleware (Prometheus)
3. **Implementar circuit breaker** para servicios externos
4. **Agregar middleware de validación** de input
5. **Configurar alertas** basadas en logs de seguridad

## Conclusión

El middleware optimizado proporciona una base sólida de seguridad y observabilidad para el UserService, siguiendo las mejores prácticas de desarrollo de APIs enterprise. La implementación es modular, testeable y fácil de mantener, preparada para escalar en un entorno de producción.
