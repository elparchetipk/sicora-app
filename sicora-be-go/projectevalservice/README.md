# SICORA ProjectEvalService - Go Implementation

## Descripción

Microservicio para la gestión y evaluación de proyectos formativos de desarrollo de software, implementado en Go con Clean Architecture.

## Funcionalidades Principales

### Gestión de Proyectos
- ✅ Crear proyectos formativos
- ✅ Listar proyectos por instructor
- ✅ Actualizar información de proyectos
- ✅ Cambiar estado de proyectos (activo/inactivo/archivado)
- ✅ Eliminar proyectos

### Gestión de Entregas
- ✅ Crear entregas de estudiantes
- ✅ Validar URLs de repositorio y deployment
- ✅ Listar entregas por proyecto
- ✅ Listar entregas por estudiante
- ✅ Control de fechas límite

### Sistema de Evaluación
- ✅ Crear evaluaciones técnicas detalladas
- ✅ Criterios de evaluación múltiples:
  - Funcionalidad (20%)
  - Calidad de código (15%)
  - Arquitectura (15%)
  - Documentación (10%)
  - Testing (15%)
  - Deployment (10%)
  - Seguridad (10%)
  - Rendimiento (5%)
- ✅ Comentarios específicos por criterio
- ✅ Cálculo automático de calificaciones
- ✅ Sistema de publicación de evaluaciones

## Arquitectura

### Clean Architecture
```
├── internal/
│   ├── domain/
│   │   ├── entities/          # Entidades de negocio
│   │   ├── repositories/      # Interfaces de repositorios
│   │   └── errors/           # Errores del dominio
│   ├── application/
│   │   └── usecases/         # Casos de uso
│   ├── infrastructure/
│   │   ├── database/         # Implementación BD
│   │   └── auth/             # Autenticación JWT
│   └── presentation/
│       ├── handlers/         # Controladores HTTP
│       ├── middleware/       # Middleware
│       └── routes/          # Definición de rutas
├── tests/                   # Tests
├── docs/                    # Documentación
└── main.go                  # Punto de entrada
```

## Tecnologías

- **Go 1.23**: Lenguaje de programación
- **Gin**: Framework web
- **GORM**: ORM para base de datos
- **PostgreSQL 15**: Base de datos
- **JWT**: Autenticación
- **Swagger**: Documentación API
- **Docker**: Contenedorización

## Instalación

### Prerrequisitos
- Go 1.23+
- PostgreSQL 15
- Docker (opcional)

### Configuración Local

1. **Clonar y configurar:**
```bash
cd 02-go/projectevalservice
cp .env.example .env
```

2. **Instalar dependencias:**
```bash
go mod tidy
```

3. **Configurar base de datos:**
```bash
# Crear base de datos
createdb sicora_projecteval_db
```

4. **Ejecutar aplicación:**
```bash
go run main.go
```

### Con Docker

```bash
docker build -t projectevalservice .
docker run -p 8007:8007 projectevalservice
```

## API Endpoints

### Proyectos
- `POST /api/v1/projects` - Crear proyecto
- `GET /api/v1/projects` - Listar proyectos
- `GET /api/v1/projects/:id` - Obtener proyecto
- `PUT /api/v1/projects/:id` - Actualizar proyecto
- `DELETE /api/v1/projects/:id` - Eliminar proyecto

### Entregas
- `POST /api/v1/submissions` - Crear entrega
- `GET /api/v1/submissions` - Listar entregas
- `GET /api/v1/submissions/:id` - Obtener entrega
- `GET /api/v1/submissions/pending` - Entregas pendientes

### Evaluaciones
- `POST /api/v1/evaluations` - Crear evaluación
- `GET /api/v1/evaluations` - Listar evaluaciones
- `GET /api/v1/evaluations/:id` - Obtener evaluación
- `PATCH /api/v1/evaluations/:id/complete` - Completar evaluación
- `PATCH /api/v1/evaluations/:id/publish` - Publicar evaluación

## Documentación API

Swagger UI disponible en: `http://localhost:8007/swagger/index.html`

## Testing

```bash
# Ejecutar tests
go test ./...

# Tests con cobertura
go test -cover ./...

# Tests verbose
go test -v ./...
```

## Base de Datos

### Entidades Principales

1. **projects**: Proyectos formativos
2. **submissions**: Entregas de estudiantes
3. **evaluations**: Evaluaciones técnicas

### Relaciones
- Un proyecto puede tener múltiples entregas
- Una entrega puede tener múltiples evaluaciones
- Un instructor puede evaluar múltiples entregas

## Seguridad

- **JWT Authentication**: Tokens con expiración
- **Role-based Access**: Roles de instructor, estudiante, admin
- **Input Validation**: Validación completa de datos
- **CORS**: Configuración de orígenes permitidos

## Logging y Monitoreo

- Logs estructurados con Gin
- Health check endpoint: `/health`
- Métricas de rendimiento

## Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DB_HOST` | Host de PostgreSQL | localhost |
| `DB_PORT` | Puerto de PostgreSQL | 5432 |
| `DB_USER` | Usuario de BD | postgres |
| `DB_PASSWORD` | Contraseña de BD | postgres |
| `DB_NAME` | Nombre de BD | sicora_projecteval_db |
| `JWT_SECRET` | Secreto para JWT | - |
| `PORT` | Puerto del servidor | 8007 |
| `GIN_MODE` | Modo de Gin | debug |

## Contribución

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'feat: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Estado del Proyecto

✅ **COMPLETADO AL 100%**

- [x] Arquitectura Clean Architecture
- [x] Entidades del dominio
- [x] Casos de uso implementados
- [x] Repositorios con GORM
- [x] Handlers y rutas
- [x] Autenticación JWT
- [x] Middleware de seguridad
- [x] Documentación Swagger
- [x] Docker configuration
- [x] Variables de entorno
- [x] Estructura de tests

## Próximos Pasos

1. Ejecutar `go mod tidy` para descargar dependencias
2. Configurar base de datos PostgreSQL
3. Ejecutar migraciones
4. Generar documentación Swagger
5. Implementar tests unitarios
6. Configurar CI/CD

## AutoCommit Service

El proyecto incluye un servicio de autocommit automatizado que sigue las convenciones de commits del proyecto.

### Activar AutoCommit

```bash
# Iniciar el servicio de autocommit (monitoreo automático cada 30s)
bash scripts/activate-autocommit.sh start

# Verificar estado del servicio
bash scripts/activate-autocommit.sh status

# Detener el servicio
bash scripts/activate-autocommit.sh stop

# Ejecutar commit manual
bash scripts/activate-autocommit.sh commit
```

### Convenciones de Commit

El autocommit usa las siguientes convenciones:

- `feat(domain)`: nuevas entidades del dominio
- `feat(api)`: nuevos endpoints/handlers
- `feat(application)`: nuevos casos de uso
- `feat(infrastructure)`: repositorios/servicios
- `test(unit)`: tests unitarios
- `docs`: documentación
- `config(docker)`: configuración de contenedores
- `chore(deps)`: actualización de dependencias

### Verificaciones Automáticas

Antes de cada commit, el sistema ejecuta:

1. `go mod tidy` - Limpieza de dependencias
2. `go build ./...` - Verificación de compilación
3. `go test ./tests` - Ejecución de tests
4. Análisis automático de cambios para determinar tipo de commit
