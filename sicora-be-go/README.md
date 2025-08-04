# SICORA Backend - Go Stack

## 🏛️ Sistema de Información de Coordinación Académica

Backend de SICORA implementado en Go con arquitectura de microservicios para gestión de usuarios, horarios, asistencia y evaluación de proyectos. Desarrollado para el SENA con enfoque en alta concurrencia y rendimiento.

## 🚀 Tecnologías Principales

- **Go 1.21+** - Lenguaje principal con tipado fuerte
- **Gin** - Framework web de alto rendimiento
- **GORM** - ORM con soporte completo para PostgreSQL
- **PostgreSQL 15** - Base de datos principal
- **Redis** - Cache y gestión de sesiones
- **Docker & Docker Compose** - Containerización
- **Swagger** - Documentación automática de APIs
- **Testify** - Framework de testing

## 🏗️ Arquitectura de Microservicios

### Servicios Implementados

- **🔐 userservice** - Gestión de usuarios, autenticación JWT
- **📅 scheduleservice** - Gestión de horarios y calendarios
- **✅ attendanceservice** - Control de asistencia
- **📊 projectevalservice** - Evaluación de proyectos
- **👤 evalinservice** - Evaluación individual
- **🧠 kbservice** - Base de conocimiento
- **🤖 aiservice** - Servicios de IA
- **🛠️ softwarefactoryservice** - Gestión de proyectos
- **📱 mevalservice** - Evaluación móvil

### Estructura del Proyecto

```
sicora-be-go/
├── shared/                 # Submódulo sicora-shared
├── infra/                  # Submódulo sicora-infra
├── userservice/            # ✅ Servicio de usuarios (COMPLETADO)
├── scheduleservice/        # Servicio de horarios
├── attendanceservice/      # Servicio de asistencia
├── projectevalservice/     # Servicio de evaluación de proyectos
├── evalinservice/          # Servicio de evaluación individual
├── kbservice/              # Servicio de base de conocimiento
├── mevalservice/           # Servicio de evaluación móvil
├── softwarefactoryservice/ # Servicio de gestión de proyectos
├── _docs/                  # Documentación organizada
├── scripts/                # Scripts de automatización
├── go.mod                  # Dependencias principales
├── go.sum                  # Checksums de dependencias
├── docker-compose.yml      # Configuración Docker local
└── Makefile               # Comandos de automatización
```

## 📚 Documentación

Para documentación detallada, consulta la [documentación organizada](./_docs/):

- [📋 Integración](./_docs/integracion/) - Integración con frontend y otros servicios
- [⚙️ Configuración](./_docs/configuracion/) - Setup y configuración de servicios
- [🔧 Desarrollo](./_docs/desarrollo/) - Guías de desarrollo y arquitectura
- [📊 Reportes](./_docs/reportes/) - Reportes de estado y verificación
- [🎯 Microservicios](./_docs/microservicios/) - Documentación específica de servicios
- [🏗️ Infraestructura](./_docs/infraestructura/) - Configuración de infraestructura

## 🔧 Desarrollo

### Prerrequisitos

- Go 1.21 o superior
- Docker y Docker Compose
- PostgreSQL 15 (o via Docker)
- Redis (opcional, para cache)

### Configuración Inicial

```bash
# Clonar dependencias
git submodule update --init --recursive

# Configurar variables de entorno
cp .env.example .env

# Levantar infraestructura
docker-compose -f docker-compose.infra.yml up -d

# Instalar dependencias
go mod tidy

# Ejecutar migraciones
make migrate-up

# Levantar servicios en desarrollo
make dev
```

### Scripts Disponibles

```bash
# Desarrollo
make dev              # Levantar todos los servicios
make dev-user         # Solo userservice
make dev-schedule     # Solo scheduleservice

# Testing
make test             # Ejecutar todos los tests
make test-unit        # Solo tests unitarios
make test-integration # Solo tests de integración

# Base de datos
make migrate-up       # Aplicar migraciones
make migrate-down     # Revertir migraciones
make db-reset         # Resetear BD

# Documentación
make swagger          # Generar documentación Swagger
make docs             # Verificar estructura de documentación
```

## 🎯 Estado del Proyecto

### ✅ Completado

- ✅ **UserService**: Autenticación JWT, CRUD usuarios
- ✅ **Arquitectura base**: Clean Architecture implementada
- ✅ **Base de datos**: PostgreSQL con GORM
- ✅ **Docker**: Containerización completa
- ✅ **Documentación**: Swagger automático
- ✅ **Testing**: Framework de testing configurado
- ✅ **Integración**: API REST funcional

### 🔄 En Desarrollo

- 🔄 **AttendanceService**: Control de asistencia
- 🔄 **ScheduleService**: Gestión de horarios
- 🔄 **ProjectEvalService**: Evaluación de proyectos
- 🔄 **Tests**: Cobertura completa
- 🔄 **Monitoring**: Métricas y observabilidad

### 📋 Próximos Pasos

- 📋 **KbService**: Base de conocimiento
- 📋 **EvalinService**: Evaluación individual
- 📋 **AIService**: Integración con IA
- 📋 **API Gateway**: Centralización de APIs

## 🔗 Integración

### Frontend React

```bash
# Configuración de CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# Endpoints disponibles
http://localhost:8002/api/v1/auth/login
http://localhost:8002/api/v1/users
http://localhost:8002/swagger/index.html
```

### Base de Datos

```bash
# Conexión local
DATABASE_URL=postgres://sicora:password@localhost:5432/sicora_db

# Migraciones automáticas
AUTO_MIGRATE=true
```

## 🧪 Testing

```bash
# Ejecutar tests completos
make test

# Tests con cobertura
make test-coverage

# Tests de integración
make test-integration

# Benchmarks
make benchmark
```

## 🚀 Despliegue

### Desarrollo

```bash
# Levantar stack completo
docker-compose up -d

# Solo backend
docker-compose up -d userservice scheduleservice
```

### Producción

```bash
# Build optimizado
make build

# Deploy con Docker
make deploy-prod

# Verificar salud
make health-check
```

## 📊 Rendimiento

### Benchmarks vs Python

| Métrica | Go   | Python | Mejora |
| ------- | ---- | ------ | ------ |
| Startup | 50ms | 2s     | 40x    |
| Memory  | 15MB | 50MB   | 3.3x   |
| RPS     | 10k  | 2k     | 5x     |
| CPU     | 5%   | 20%    | 4x     |

### Concurrencia

- **Goroutines**: 1M goroutines concurrentes
- **Pooling**: Connection pooling optimizado
- **Channels**: Comunicación asíncrona nativa

## 🔍 Verificación de Calidad

```bash
# Lint completo
make lint

# Verificar arquitectura
make verify-arch

# Análisis de seguridad
make security-scan

# Verificar documentación
./scripts/verify-doc-structure.sh
```

## �️ Herramientas de Desarrollo

### VS Code

- Extensión Go oficial
- Debugger configurado
- Snippets personalizados
- Linting automático

### Scripts de Automatización

```bash
# Verificar versiones de Go
./scripts/verify-go-versions.sh

# Validar integración
./scripts/validate-integration.sh

# Verificar estructura
./scripts/verify-doc-structure.sh
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Sigue los estándares de código Go
4. Agrega tests para nueva funcionalidad
5. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
6. Push a la rama (`git push origin feature/nueva-funcionalidad`)
7. Abre un Pull Request

### Estándares de Código

- **gofmt**: Formateo automático
- **golint**: Linting estricto
- **go vet**: Análisis estático
- **gosec**: Análisis de seguridad

## 📈 Roadmap

### Q3 2025

- ✅ UserService completo
- 🔄 AttendanceService
- 🔄 ScheduleService

### Q4 2025

- 📋 ProjectEvalService
- 📋 KbService
- 📋 API Gateway

### Q1 2026

- 📋 AIService
- 📋 Microservicios avanzados
- 📋 Observabilidad completa

## � Mantenimiento

### Estructura de Documentación

- **Solo README.md** en la raíz
- **Toda documentación** en `_docs/` por categorías
- **Scripts** en `scripts/`
- **Verificación automática** con `./scripts/verify-doc-structure.sh`

### Actualizaciones

```bash
# Actualizar dependencias
go get -u ./...
go mod tidy

# Verificar estructura
./scripts/verify-doc-structure.sh verify

# Actualizar documentación Swagger
make swagger
```

---

_Desarrollado con 🚀 para el SENA por el equipo EPTI_
_Go: Performance meets simplicity_
