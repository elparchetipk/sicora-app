# Estrategia de Manejo de Errores - Multistack SICORA-APP

## 📊 Resumen Ejecutivo

El proyecto actualmente **NO tiene una estrategia unificada** de manejo de errores. Cada stack implementa su propio enfoque, creando inconsistencias que afectan la experiencia del usuario y la mantenibilidad del código.

## 🔍 Estado Actual por Stack

### **✅ 1. FastAPI (Python) - IMPLEMENTADO**

**Estrategia**: Global Exception Handlers + Custom Domain Exceptions

```python
# ✅ COMPLETO: Domain exceptions estructuradas
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
            "code": "USER_NOT_FOUND",
            "timestamp": datetime.now(timezone.utc)
        }
    )
```

**Características implementadas:**

- ✅ **Exception handlers específicos** por tipo de error
- ✅ **Códigos de error estructurados** (USER_NOT_FOUND, WEAK_PASSWORD)
- ✅ **Timestamps** en todas las respuestas
- ✅ **Logging automático** de excepciones
- ✅ **Jerarquía de excepciones** (UserDomainException base)
- ✅ **Respuestas JSON consistentes**

**Ejemplos de exceptions:**

```python
# userservice/app/domain/exceptions/user_exceptions.py
class UserNotFoundError(UserDomainException): ...
class WeakPasswordError(UserDomainException): ...
class EmailAlreadyExistsError(UserDomainException): ...
```

### **🚧 2. Go - PARCIALMENTE IMPLEMENTADO**

**Estrategia**: Error handling explícito + HTTP status codes

```go
// 🚧 BÁSICO: Error handling manual en cada handler
if err != nil {
    h.logger.Printf("Error creating user: %v", err)
    c.JSON(http.StatusInternalServerError, gin.H{
        "error":   "Failed to create user",
        "details": err.Error(),
    })
    return
}
```

**Problemas identificados:**

- ❌ **Sin middleware global** de error handling
- ❌ **Inconsistencia** en formato de respuestas
- ❌ **Sin códigos de error** estructurados
- ❌ **Logging disperso** sin estandarización
- ❌ **Sin custom error types**

### **🚧 3. Express/Node.js - BÁSICAMENTE IMPLEMENTADO**

**Estrategia**: Global error middleware + try/catch

```javascript
// ✅ Global error handler implementado
this.app.use((error, req, res, next) => {
  const logger = this.container.get('logger');
  logger.error('Unhandled error:', error);

  res.status(500).json({
    error: 'Internal server error',
    message:
      process.env.NODE_ENV === 'development'
        ? error.message
        : 'Something went wrong',
  });
});
```

**Estado actual:**

- ✅ **Global error middleware** configurado
- ✅ **404 handler** para rutas no encontradas
- ✅ **Environment-based** error details
- ❌ **Sin custom error classes**
- ❌ **Sin códigos de error** estructurados
- ❌ **Sin validation errors** específicos

### **❌ 4. Next.js - NO IMPLEMENTADO**

**Estrategia**: Pendiente de definición

**Estado actual:**

- ❌ **Sin error handling** configurado
- ❌ **Sin middleware** global
- ❌ **Sin exception handlers**
- ❌ **Sin logging** estructurado

### **❌ 5. Spring Boot Java - NO IMPLEMENTADO**

**Estrategia**: Pendiente (@ControllerAdvice + @ExceptionHandler)

**Estado actual:**

- ❌ **Sin @ControllerAdvice** implementado
- ❌ **Sin custom exceptions**
- ❌ **Sin global error handling**
- ❌ **Sin response DTOs** para errores

### **❌ 6. Spring Boot Kotlin - NO IMPLEMENTADO**

**Estrategia**: Pendiente (similar a Java pero con sealed classes)

**Estado actual:**

- ❌ **Sin exception handling** implementado
- ❌ **Sin sealed classes** para errores
- ❌ **Sin error response models**

## 🎯 Estrategia Unificada Propuesta

### **1. Estructura de Respuesta de Error Estándar**

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "Usuario no encontrado",
    "details": "No se encontró usuario con ID: 123e4567-e89b-12d3",
    "timestamp": "2025-06-16T10:30:00Z",
    "path": "/api/v1/users/123e4567-e89b-12d3",
    "correlationId": "abc-123-def"
  }
}
```

### **2. Códigos de Error Unificados**

```typescript
// Códigos comunes a todos los stacks
enum ErrorCodes {
  // Authentication/Authorization
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',
  INSUFFICIENT_PERMISSIONS = 'INSUFFICIENT_PERMISSIONS',

  // User Management
  USER_NOT_FOUND = 'USER_NOT_FOUND',
  EMAIL_ALREADY_EXISTS = 'EMAIL_ALREADY_EXISTS',
  WEAK_PASSWORD = 'WEAK_PASSWORD',

  // Validation
  INVALID_INPUT = 'INVALID_INPUT',
  REQUIRED_FIELD_MISSING = 'REQUIRED_FIELD_MISSING',

  // System
  INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR',
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  DATABASE_ERROR = 'DATABASE_ERROR',
}
```

### **3. Mapeo de HTTP Status Codes**

| Error Code               | HTTP Status | Descripción             |
| ------------------------ | ----------- | ----------------------- |
| INVALID_CREDENTIALS      | 401         | Credenciales no válidas |
| INSUFFICIENT_PERMISSIONS | 403         | Sin permisos            |
| USER_NOT_FOUND           | 404         | Recurso no encontrado   |
| EMAIL_ALREADY_EXISTS     | 409         | Conflicto de datos      |
| WEAK_PASSWORD            | 400         | Datos no válidos        |
| INTERNAL_SERVER_ERROR    | 500         | Error interno           |

## 🔧 Implementación por Stack

### **🐍 FastAPI (Python) - MANTENER ACTUAL**

```python
# ✅ Ya implementado correctamente
@app.exception_handler(UserDomainException)
async def domain_exception_handler(request: Request, exc: UserDomainException):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": type(exc).__name__.upper(),
                "message": str(exc),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": str(request.url.path)
            }
        }
    )
```

### **⚡ Go (Gin) - IMPLEMENTAR**

```go
// TODO: Middleware global de error handling
func ErrorMiddleware() gin.HandlerFunc {
    return gin.CustomRecovery(func(c *gin.Context, recovered interface{}) {
        err, ok := recovered.(error)
        if !ok {
            err = fmt.Errorf("unknown error: %v", recovered)
        }

        c.JSON(http.StatusInternalServerError, ErrorResponse{
            Error: ErrorDetails{
                Code:      "INTERNAL_SERVER_ERROR",
                Message:   "Error interno del servidor",
                Timestamp: time.Now().UTC(),
                Path:      c.Request.URL.Path,
            },
        })
    })
}

// TODO: Custom error types
type DomainError struct {
    Code    string
    Message string
}

func (e DomainError) Error() string {
    return e.Message
}
```

### **📱 Express/Node.js - MEJORAR ACTUAL**

```javascript
// TODO: Mejorar error handler existente
class CustomError extends Error {
  constructor(code, message, statusCode = 500) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
    this.timestamp = new Date().toISOString();
  }
}

// TODO: Mejorar global error handler
this.app.use((error, req, res, next) => {
  const errorResponse = {
    error: {
      code: error.code || 'INTERNAL_SERVER_ERROR',
      message: error.message,
      timestamp: error.timestamp || new Date().toISOString(),
      path: req.path,
      correlationId: req.correlationId,
    },
  };

  res.status(error.statusCode || 500).json(errorResponse);
});
```

### **🚀 Next.js - IMPLEMENTAR COMPLETO**

```typescript
// TODO: Global error handling con TypeScript
// middleware.ts
export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500
  ) {
    super(message);
  }
}

// pages/api/_middleware.ts
export async function middleware(req: NextRequest) {
  return NextResponse.next();
}

// TODO: Error boundary para API routes
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // ... logic
  } catch (error) {
    if (error instanceof ApiError) {
      return res.status(error.statusCode).json({
        error: {
          code: error.code,
          message: error.message,
          timestamp: new Date().toISOString(),
          path: req.url,
        },
      });
    }
    // ... global handler
  }
}
```

### **☕ Java Spring Boot - IMPLEMENTAR COMPLETO**

```java
// TODO: Global exception handler
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(
        UserNotFoundException ex,
        HttpServletRequest request
    ) {
        ErrorResponse error = ErrorResponse.builder()
            .code("USER_NOT_FOUND")
            .message(ex.getMessage())
            .timestamp(Instant.now())
            .path(request.getRequestURI())
            .build();

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
}

// TODO: Custom exceptions
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String userId) {
        super("Usuario no encontrado con ID: " + userId);
    }
}

// TODO: Error response DTO
@Data
@Builder
public class ErrorResponse {
    private ErrorDetails error;

    @Data
    @Builder
    public static class ErrorDetails {
        private String code;
        private String message;
        private Instant timestamp;
        private String path;
        private String correlationId;
    }
}
```

### **🔮 Kotlin Spring Boot - IMPLEMENTAR COMPLETO**

```kotlin
// TODO: Sealed classes para errores
sealed class DomainException(message: String) : Exception(message)

data class UserNotFoundException(val userId: String) :
    DomainException("Usuario no encontrado con ID: $userId")

data class EmailAlreadyExistsException(val email: String) :
    DomainException("Email ya existe: $email")

// TODO: Global exception handler
@ControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException::class)
    fun handleUserNotFound(
        ex: UserNotFoundException,
        request: HttpServletRequest
    ): ResponseEntity<ErrorResponse> {
        val error = ErrorResponse(
            error = ErrorDetails(
                code = "USER_NOT_FOUND",
                message = ex.message!!,
                timestamp = Instant.now(),
                path = request.requestURI
            )
        )
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error)
    }
}

// TODO: Error response data class
data class ErrorResponse(val error: ErrorDetails)

data class ErrorDetails(
    val code: String,
    val message: String,
    val timestamp: Instant,
    val path: String,
    val correlationId: String? = null
)
```

## 📋 Plan de Implementación

### **Fase 1: Definición de Estándares (1 semana)**

1. **Finalizar códigos de error** unificados
2. **Definir estructura** de respuesta JSON
3. **Crear documentación** de error handling
4. **Establecer logging** estándar

### **Fase 2: Implementación por Prioridad (4 semanas)**

**Semana 1**: Go UserService error handling
**Semana 2**: Express/Node.js mejoras  
**Semana 3**: Next.js implementación completa
**Semana 4**: Java/Kotlin Spring Boot

### **Fase 3: Testing y Documentación (1 semana)**

1. **Tests unitarios** para error handlers
2. **Tests de integración**
3. **Documentación API** con ejemplos de errores
4. **Postman collections** con casos de error

## 🎓 Valor Educativo

Esta implementación permitirá a los estudiantes:

1. **Comparar enfoques** de error handling entre tecnologías
2. **Entender trade-offs** entre simplicidad y robustez
3. **Aplicar patrones** como Exception Hierarchy y Global Handlers
4. **Implementar logging** y monitoring efectivo
5. **Diseñar APIs** con buena experiencia de developer

## 🚨 Urgencia de Implementación

**Prioridad ALTA**: Esta es una **brecha crítica** que debe resolverse antes de continuar con más features. Sin manejo consistente de errores:

- Los usuarios tendrán experiencias inconsistentes
- El debugging será mucho más difícil
- La integración entre servicios será problemática
- El proyecto perderá valor educativo y profesional

**Recomendación**: Priorizar la implementación del error handling en Go y Express antes de continuar con nuevas funcionalidades.
