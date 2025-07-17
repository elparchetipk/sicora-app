# Schedule Service - Go Implementation

Microservicio para gestión de horarios académicos implementado en Go con Clean Architecture.

## 📋 Funcionalidades

### ✅ Historias de Usuario Implementadas
- **HU-BE-017**: Obtener Horarios - Consulta filtrada de horarios
- **HU-BE-018**: Gestión CRUD de Horarios - Administración completa
- **HU-BE-019**: Carga Masiva de Horarios - Upload CSV con validaciones
- **HU-BE-020**: Gestión de Entidades Maestras - Programas, fichas, ambientes

### 🏗️ Arquitectura

```
scheduleservice/
├── cmd/server/           # Entry point
├── configs/              # Configuration management
├── internal/
│   ├── domain/           # Business logic & entities
│   │   ├── entities/     # Domain entities
│   │   └── repositories/ # Repository interfaces
│   ├── application/      # Use cases & DTOs
│   │   ├── dtos/         # Data Transfer Objects
│   │   └── usecases/     # Business use cases
│   ├── infrastructure/   # External concerns
│   │   ├── database/     # GORM models & repos
│   │   └── auth/         # Authentication
│   └── presentation/     # HTTP layer
│       ├── handlers/     # HTTP handlers
│       ├── routes/       # Route definitions
│       └── middleware/   # HTTP middleware
├── pkg/                  # Shared utilities
├── tests/                # Test suites
├── docs/                 # API documentation
├── go.mod               # Go modules
└── README.md
```

### 🛠️ Tecnologías

- **Framework**: Gin (HTTP)
- **ORM**: GORM
- **Database**: PostgreSQL 15
- **Authentication**: JWT
- **Documentation**: Swagger
- **Testing**: Testify
- **Validation**: go-playground/validator

### 🚀 Configuración y Ejecución

#### Prerequisitos

- Go 1.23+
- PostgreSQL 15
- Docker (opcional)

#### Configuración Local

1. **Clonar y navegar al proyecto**:
```bash
cd /ruta/al/proyecto/02-go/scheduleservice
```

2. **Instalar dependencias**:
```bash
go mod tidy
```

3. **Configurar variables de entorno**:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. **Configurar base de datos**:
```sql
CREATE DATABASE scheduleservice_db;
```

5. **Ejecutar el servicio**:
```bash
go run cmd/server/main.go
```

#### Con Docker

```bash
# Desde la raíz del proyecto multistack
docker-compose up scheduleservice
```

### 📚 API Documentation

Una vez ejecutando el servicio:
- **Swagger UI**: http://localhost:8002/swagger/index.html
- **Health Check**: http://localhost:8002/health

### 🗂️ Endpoints Principales

#### Horarios
- `GET /api/v1/schedules` - Listar horarios (con filtros)
- `POST /api/v1/schedules` - Crear horario
- `GET /api/v1/schedules/{id}` - Obtener horario por ID
- `PUT /api/v1/schedules/{id}` - Actualizar horario
- `DELETE /api/v1/schedules/{id}` - Eliminar horario

#### Entidades Maestras
- `GET /api/v1/master/programs` - Listar programas académicos
- `POST /api/v1/master/programs` - Crear programa académico
- `GET /api/v1/master/groups` - Listar fichas/grupos
- `POST /api/v1/master/groups` - Crear ficha/grupo
- `GET /api/v1/master/venues` - Listar ambientes
- `POST /api/v1/master/venues` - Crear ambiente
- `GET /api/v1/master/campuses` - Listar sedes
- `POST /api/v1/master/campuses` - Crear sede

#### Administración
- `POST /api/v1/admin/schedules/upload` - Carga masiva CSV

### 🧪 Testing

```bash
# Ejecutar todos los tests
go test ./...

# Ejecutar tests con cobertura
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### 📊 Modelos de Datos

#### Schedule (Horario)
- ID, AcademicGroupID, InstructorID, VenueID
- Subject, DayOfWeek, StartTime, EndTime
- BlockIdentifier, StartDate, EndDate, Status

#### AcademicProgram (Programa Académico)
- ID, Name, Code, Type, Duration, Description

#### AcademicGroup (Ficha/Grupo)
- ID, Number, AcademicProgramID, Quarter, Year, Shift

#### Venue (Ambiente)
- ID, Name, Code, Type, Capacity, CampusID, Floor

#### Campus (Sede)
- ID, Name, Code, Address, City

### 🔧 Características Técnicas

- **Clean Architecture**: Separación clara de responsabilidades
- **Dependency Injection**: Inversión de dependencias
- **Repository Pattern**: Abstracción de acceso a datos
- **Use Cases**: Lógica de negocio encapsulada
- **DTOs**: Validación y transformación de datos
- **Middleware**: Autenticación, CORS, logging
- **Error Handling**: Manejo robusto de errores
- **Logging**: Logging estructurado
- **Validation**: Validación automática con tags
- **Migrations**: Migración automática de esquemas

### 🔒 Seguridad

- Autenticación JWT obligatoria
- Validación de roles y permisos
- Validación de entrada de datos
- Prevención de conflictos de horarios
- CORS configurado

### 📈 Performance

- Connection pooling en base de datos
- Queries optimizadas con preloading
- Paginación en listados
- Índices en campos críticos
- Operaciones batch para bulk operations

### 🐳 Docker

```dockerfile
# Dockerfile incluido para despliegue
# Imagen multistage para optimización
```

### 🧑‍💻 Desarrollo

#### Agregar nueva funcionalidad

1. **Entidad de dominio** (`internal/domain/entities/`)
2. **Repository interface** (`internal/domain/repositories/`)
3. **DTOs** (`internal/application/dtos/`)
4. **Use cases** (`internal/application/usecases/`)
5. **Model** (`internal/infrastructure/database/models/`)
6. **Repository implementation** (`internal/infrastructure/database/repositories/`)
7. **Handler** (`internal/presentation/handlers/`)
8. **Routes** (`internal/presentation/routes/`)
9. **Tests** (`tests/`)

### 📚 Referencias

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Gin Framework](https://gin-gonic.com/)
- [GORM](https://gorm.io/)
- [Swagger](https://swagger.io/)

### 🤝 Contribución

1. Fork el proyecto
2. Crear feature branch
3. Commit los cambios
4. Push al branch
5. Crear Pull Request

---

**Estado**: 🚧 En desarrollo activo
**Versión**: 1.0.0
**Licencia**: MIT
