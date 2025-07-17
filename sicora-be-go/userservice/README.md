# 🔮 Go UserService - Clean Architecture

**Stack**: Go + Gin Framework  
**Patrón**: Clean Architecture + Microservicios  
**Estado**: 🚧 Estructura base implementada

---

## 🏗️ **ESTRUCTURA CLEAN ARCHITECTURE**

```
userservice/
├── go.mod                          # Dependencias Go
├── main.go                         # Punto de entrada
├── internal/                       # Código interno (no exportable)
│   ├── domain/                     # 🟦 DOMINIO (Capa más interna)
│   │   ├── entities/               # Entidades de negocio
│   │   │   ├── user.go             # ✅ Entidad User completa
│   │   │   └── validation.go       # ✅ Validaciones de dominio
│   │   └── repositories/           # Interfaces de repositorio
│   │       └── user_repository.go  # ✅ Interface UserRepository
│   │
│   ├── application/                # 🟨 APLICACIÓN (Casos de uso)
│   │   ├── usecases/               # Casos de uso
│   │   │   └── user_usecases.go    # ✅ Create, Get, List users
│   │   └── dtos/                   # Data Transfer Objects
│   │       └── user_dtos.go        # ✅ DTOs completos
│   │
│   ├── infrastructure/             # 🟥 INFRAESTRUCTURA (Frameworks)
│   │   ├── database/               # 📋 TODO: Configuración DB
│   │   │   ├── connection.go       # Conexión PostgreSQL 15
│   │   │   ├── models/             # Modelos GORM
│   │   │   └── repositories/       # Implementaciones concretas
│   │   ├── config/                 # 📋 TODO: Configuraciones
│   │   └── external/               # 📋 TODO: Servicios externos
│   │
│   └── presentation/               # 🟩 PRESENTACIÓN (API)
│       ├── handlers/               # 📋 TODO: Controladores HTTP
│       ├── middleware/             # 📋 TODO: Middlewares
│       ├── routes/                 # 📋 TODO: Definición de rutas
│       └── validators/             # 📋 TODO: Validadores request
│
├── cmd/                            # 📋 TODO: Comandos de aplicación
├── pkg/                            # 📋 TODO: Código reutilizable
├── tests/                          # 📋 TODO: Tests
└── docs/                           # 📋 TODO: Documentación API
```

---

## ✅ **IMPLEMENTADO (Estructura Base)**

### **🟦 Dominio (Domain Layer)**
- ✅ **Entidad User** con reglas de negocio SICORA
- ✅ **Validaciones** para nombres, emails, documentos, fichas
- ✅ **UserRole** enum (aprendiz, instructor, admin, coordinador)
- ✅ **Interface UserRepository** con todas las operaciones

### **🟨 Aplicación (Application Layer)**
- ✅ **CreateUserUseCase** con validaciones completas
- ✅ **GetUserUseCase** para obtener usuarios
- ✅ **ListUsersUseCase** con filtros y paginación
- ✅ **DTOs completos** para request/response

### **📋 Características del Dominio**
- **Ficha obligatoria** para aprendices (requisito SENA)
- **Email validado** para dominios @sena.edu.co
- **Políticas de contraseña** robustas
- **Validación de documentos** colombianos
- **Soft delete** para usuarios

---

## 📋 **PENDIENTE DE IMPLEMENTAR**

### **🟥 Infraestructura (Infrastructure Layer)**
```bash
# TODO: Implementar
├── database/
│   ├── connection.go        # PostgreSQL 15 + GORM
│   ├── models/user_model.go # Modelo para BD
│   └── repositories/
│       └── postgres_user_repository.go
├── config/
│   ├── database.go          # Config DB
│   ├── server.go            # Config servidor
│   └── env.go               # Variables entorno
└── external/
    ├── email_service.go     # Envío emails
    └── file_service.go      # Manejo archivos
```

### **🟩 Presentación (Presentation Layer)**
```bash
# TODO: Implementar
├── handlers/
│   └── user_handler.go      # Controladores HTTP
├── middleware/
│   ├── auth.go              # Autenticación JWT
│   ├── cors.go              # CORS
│   └── logging.go           # Logging requests
├── routes/
│   └── user_routes.go       # Rutas API
└── validators/
    └── request_validator.go # Validación requests
```

### **🔧 Aplicación Completa**
```bash
# TODO: Implementar
├── main.go                  # Servidor principal
├── cmd/
│   └── migrate.go           # Migraciones DB
├── pkg/
│   ├── logger/              # Logger personalizado
│   ├── jwt/                 # Manejo JWT
│   └── errors/              # Manejo errores
└── tests/
    ├── unit/                # Tests unitarios
    └── integration/         # Tests integración
```

---

## 🚀 **SIGUIENTE FASE: INFRAESTRUCTURA**

### **Prioridad 1: Base de Datos**
1. **Configurar PostgreSQL 15** con GORM
2. **Crear modelos** de BD para User
3. **Implementar repository** concreto
4. **Setup migraciones** automáticas

### **Prioridad 2: API REST**
1. **Configurar Gin** server
2. **Implementar handlers** HTTP
3. **Setup rutas** RESTful
4. **Validación requests** con validator

### **Prioridad 3: Seguridad**
1. **Autenticación JWT**
2. **Middleware CORS**
3. **Rate limiting**
4. **Logging** estructurado

---

## 🎯 **ENDPOINTS A IMPLEMENTAR**

### **CRUD Básico**
```
POST   /api/v1/users           # Crear usuario
GET    /api/v1/users/{id}      # Obtener usuario
GET    /api/v1/users           # Listar usuarios
PUT    /api/v1/users/{id}      # Actualizar usuario
DELETE /api/v1/users/{id}      # Eliminar usuario
```

### **Operaciones Especiales**
```
POST   /api/v1/users/bulk      # Creación masiva
GET    /api/v1/users/ficha/{id} # Usuarios por ficha
GET    /api/v1/users/stats     # Estadísticas
POST   /api/v1/auth/login      # Autenticación
POST   /api/v1/auth/refresh    # Refresh token
```

---

## 🔧 **COMANDOS DE DESARROLLO**

### **Setup Inicial**
```bash
# Instalar dependencias
cd 02-go/userservice
go mod tidy

# Generar documentación
swag init

# Ejecutar tests
go test ./...

# Ejecutar servidor
go run main.go
```

### **Base de Datos**
```bash
# Migrar BD
go run cmd/migrate.go up

# Rollback
go run cmd/migrate.go down

# Crear nueva migración
go run cmd/migrate.go create add_users_table
```

---

## 📊 **INTEGRACIÓN CON SHARED-DATA**

### **Carga Masiva**
```go
// Acceso a shared-data desde Go
sharedDataPath := "../../shared-data"
usersFile := filepath.Join(sharedDataPath, "imports", "users", "users.csv")

// Implementar bulk loader
func BulkCreateFromCSV(filePath string) error {
    // Lee CSV desde shared-data
    // Valida con esquemas JSON
    // Crea usuarios en lotes
}
```

### **Exportación**
```go
// Exportar a shared-data
exportPath := "../../shared-data/exports/go"
err := ExportUsersToCSV(users, filepath.Join(exportPath, "users.csv"))
```

---

## 🏆 **VENTAJAS DE ESTA ESTRUCTURA**

### **Clean Architecture Benefits**
- ✅ **Independiente de framework** (fácil cambio de Gin a Fiber)
- ✅ **Testeable** cada capa por separado
- ✅ **Mantenible** cambios aislados por capa
- ✅ **Escalable** estructura clara para equipos grandes

### **Go Specific Benefits**
- ✅ **Performance** nativo y compilado
- ✅ **Concurrencia** con goroutines
- ✅ **Tipado fuerte** con interfaces
- ✅ **Deployments** fáciles (single binary)

### **Consistencia Multistack**
- ✅ **Misma lógica de dominio** que FastAPI
- ✅ **Endpoints compatibles** misma API
- ✅ **Shared-data integration** común
- ✅ **Clean Architecture** consistente

---

**Siguiente paso**: Implementar capa de infraestructura (database + config + repositories concretos)
