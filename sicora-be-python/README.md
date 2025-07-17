# SICORA Backend - Python Stack (FastAPI)

## 🏛️ Sistema de Información para Control de Registros Académicos

Backend de SICORA implementado en Python con FastAPI, diseñado como repositorio independiente con arquitectura de microservicios. Incluye integración completa con IA y servicios avanzados para gestión académica del SENA.

## 🚀 Tecnologías Principales

- **FastAPI** - Framework web moderno y de alto rendimiento
- **SQLAlchemy** - ORM con soporte completo para PostgreSQL
- **Alembic** - Migraciones de base de datos
- **PostgreSQL 15** - Base de datos principal con pgvector
- **Redis** - Cache y gestión de sesiones
- **Pytest** - Framework de testing completo
- **Swagger UI** - Documentación automática de APIs
- **Docker & Docker Compose** - Containerización
- **Uvicorn** - Servidor ASGI de alto rendimiento

## 🎯 Arquitectura de Microservicios

### Servicios Implementados

- **🔐 userservice** - Gestión de usuarios, autenticación JWT
- **📅 scheduleservice** - Gestión de horarios y calendarios académicos
- **✅ attendanceservice** - Control y registro de asistencia
- **👤 evalinservice** - Sistema de evaluación individual
- **📊 projectevalservice** - Sistema de evaluación de proyectos
- **🧠 kbservice** - Base de conocimientos con búsqueda IA
- **🤖 aiservice** - Servicios de inteligencia artificial
- **🌐 apigateway** - Gateway y orquestación de APIs
- **🛠️ softwarefactoryservice** - Gestión de proyectos
- **📱 mevalservice** - Evaluación móvil
- **🔔 notificationservice** - Sistema de notificaciones

### Estructura del Proyecto

```
sicora-be-python/
├── shared/                   # Submódulo sicora-shared
├── infra/                    # Submódulo sicora-infra
├── userservice/              # ✅ Servicio de usuarios
├── scheduleservice/          # ✅ Servicio de horarios
├── attendanceservice/        # ✅ Servicio de asistencia
├── evalinservice/            # ✅ Evaluación individual
├── projectevalservice/       # ✅ Evaluación de proyectos
├── kbservice/                # ✅ Base de conocimientos
├── aiservice/                # ✅ Servicios de IA
├── apigateway/               # ✅ API Gateway
├── softwarefactoryservice/   # ✅ Gestión de proyectos
├── mevalservice/             # ✅ Evaluación móvil
├── notificationservice-template/ # 📋 Template de notificaciones
├── _docs/                    # Documentación organizada
├── scripts/                  # Scripts de automatización
├── database/                 # Scripts de base de datos
├── requirements.txt          # Dependencias principales
├── requirements-dev.txt      # Dependencias de desarrollo
├── pyproject.toml           # Configuración del proyecto
└── docker-compose.yml       # Configuración Docker
```

## 📚 Documentación

Para documentación detallada, consulta la [documentación organizada](./_docs/):

- [📋 Integración](./_docs/integracion/) - Integración de servicios y APIs
- [⚙️ Configuración](./_docs/configuracion/) - Setup y configuración de servicios
- [🔧 Desarrollo](./_docs/desarrollo/) - Guías de desarrollo y arquitectura
- [📊 Reportes](./_docs/reportes/) - Reportes de estado y verificación
- [🎯 Microservicios](./_docs/microservicios/) - Documentación específica de servicios
- [🤖 IA](./_docs/ia/) - Servicios de inteligencia artificial
- [🌐 APIs](./_docs/apis/) - Documentación de APIs y gateway

## 🔧 Desarrollo

### Prerrequisitos

- Python 3.11 o superior
- PostgreSQL 15 (con pgvector)
- Redis
- Docker y Docker Compose

### Configuración Inicial

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurar variables de entorno
cp .env.example .env

# Levantar infraestructura
docker-compose up -d postgres redis

# Ejecutar migraciones
alembic upgrade head

# Iniciar servicios
./start_services.sh
```

### Scripts Disponibles

```bash
# Desarrollo
./start_services.sh       # Iniciar todos los servicios
python -m uvicorn main:app --reload --port 8000

# Testing
pytest                    # Ejecutar todos los tests
pytest --cov             # Tests con cobertura
./scripts/test_integration.sh  # Tests de integración

# Base de datos
alembic upgrade head      # Aplicar migraciones
alembic downgrade -1      # Revertir migración
alembic revision --autogenerate -m "mensaje"  # Nueva migración

# Documentación
./scripts/verify-doc-structure.sh  # Verificar estructura
```

## 🎯 Estado del Proyecto

### ✅ Completado

- ✅ **Arquitectura de microservicios**: Clean Architecture implementada
- ✅ **UserService**: Autenticación JWT completa
- ✅ **ScheduleService**: Gestión de horarios académicos
- ✅ **AttendanceService**: Control de asistencia
- ✅ **EvalinService**: Sistema de evaluación individual
- ✅ **ProjectEvalService**: Evaluación de proyectos
- ✅ **KbService**: Base de conocimientos con IA
- ✅ **AIService**: Servicios de inteligencia artificial
- ✅ **ApiGateway**: Gateway central de APIs
- ✅ **Docker**: Containerización completa
- ✅ **Testing**: Framework de testing configurado

### 🔄 En Desarrollo

- 🔄 **NotificationService**: Sistema de notificaciones
- 🔄 **Monitoring**: Métricas y observabilidad
- 🔄 **Performance**: Optimizaciones de rendimiento
- 🔄 **Security**: Auditoría de seguridad

### 📋 Próximos Pasos

- 📋 **Deployment**: Preparación para producción
- 📋 **Scaling**: Configuración de escalado
- 📋 **Backup**: Estrategias de respaldo
- 📋 **Monitoring**: Dashboards y alertas

## 🤖 Servicios de IA

### KbService - Base de Conocimientos

```bash
# Endpoints disponibles
POST /api/v1/kb/search     # Búsqueda semántica
POST /api/v1/kb/documents  # Subir documentos
GET  /api/v1/kb/documents  # Listar documentos
```

### AIService - Inteligencia Artificial

```bash
# Endpoints disponibles
POST /api/v1/ai/chat       # Chat con IA
POST /api/v1/ai/analyze    # Análisis de texto
POST /api/v1/ai/generate   # Generación de contenido
```

## 🌐 API Gateway

### Rutas Centralizadas

```bash
# Gateway principal
http://localhost:8000

# Servicios individuales
http://localhost:8001/users      # UserService
http://localhost:8002/schedules  # ScheduleService
http://localhost:8003/attendance # AttendanceService
http://localhost:8004/evalin     # EvalinService
http://localhost:8005/projects   # ProjectEvalService
http://localhost:8006/kb         # KbService
http://localhost:8007/ai         # AIService
```

### Documentación Automática

```bash
# Swagger UI
http://localhost:8000/docs

# ReDoc
http://localhost:8000/redoc

# OpenAPI Schema
http://localhost:8000/openapi.json
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests unitarios
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Tests con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_userservice.py
pytest tests/test_aiservice.py
```

### Scripts de Testing

```bash
# Test de integración completo
./scripts/test_integration.sh

# Test de integración simple
./scripts/test_integration_simple.sh

# Test de servicios individuales
./scripts/test_services.sh
```

## 🚀 Despliegue

### Desarrollo

```bash
# Levantar stack completo
docker-compose up -d

# Solo servicios específicos
docker-compose up -d userservice scheduleservice

# Logs
docker-compose logs -f
```

### Producción

```bash
# Build optimizado
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Health check
curl http://localhost:8000/health
```

## 📊 Arquitectura Clean

### Estructura por Servicio

```
userservice/
├── app/
│   ├── domain/          # Entidades y reglas de negocio
│   │   ├── entities/    # Modelos de dominio
│   │   ├── repositories/ # Interfaces de repositorios
│   │   └── services/    # Servicios de dominio
│   ├── application/     # Casos de uso
│   │   ├── use_cases/   # Casos de uso específicos
│   │   └── dtos/        # Data Transfer Objects
│   ├── infrastructure/  # Implementaciones externas
│   │   ├── repositories/ # Implementaciones de repositorios
│   │   ├── database/    # Configuración de BD
│   │   └── external/    # Servicios externos
│   └── presentation/    # API REST
│       ├── controllers/ # Controladores HTTP
│       ├── schemas/     # Schemas de validación
│       └── middleware/  # Middleware
├── tests/               # Tests
├── alembic/            # Migraciones
├── requirements.txt    # Dependencias
└── main.py            # Punto de entrada
```

## 🔍 Verificación de Calidad

```bash
# Linting
flake8 app/
pylint app/

# Formateo
black app/
isort app/

# Type checking
mypy app/

# Security
bandit -r app/

# Verificar estructura
./scripts/verify-doc-structure.sh
```

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/sicora
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: sicora
      POSTGRES_USER: sicora
      POSTGRES_PASSWORD: password
    ports:
      - '5432:5432'

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Sigue los estándares de código Python (PEP 8)
4. Agrega tests para nueva funcionalidad
5. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
6. Push a la rama (`git push origin feature/nueva-funcionalidad`)
7. Abre un Pull Request

### Estándares de Código

- **PEP 8**: Guía de estilo de Python
- **Type hints**: Tipado estático
- **Docstrings**: Documentación de funciones
- **Tests**: Cobertura mínima del 80%

## 📈 Rendimiento

### Métricas vs Go

| Métrica | Python | Go   | Diferencia       |
| ------- | ------ | ---- | ---------------- |
| Startup | 2s     | 50ms | 40x más lento    |
| Memory  | 50MB   | 15MB | 3.3x más memoria |
| RPS     | 2k     | 10k  | 5x menos RPS     |
| CPU     | 20%    | 5%   | 4x más CPU       |

### Optimizaciones

- **Async/await**: Concurrencia nativa
- **Connection pooling**: Pool de conexiones
- **Redis caching**: Cache distribuido
- **FastAPI**: Framework de alto rendimiento

## 🔧 Mantenimiento

### Estructura de Documentación

- **Solo README.md** en la raíz
- **Toda documentación** en `_docs/` por categorías
- **Scripts** en `scripts/`
- **Verificación automática** con `./scripts/verify-doc-structure.sh`

### Actualizaciones

```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Verificar estructura
./scripts/verify-doc-structure.sh verify

# Actualizar documentación
swagger-codegen generate -i openapi.json -l html2 -o docs/
```

---

_Desarrollado con 🐍 para el SENA por el equipo EPTI_
_Python: Versatility meets AI integration_
