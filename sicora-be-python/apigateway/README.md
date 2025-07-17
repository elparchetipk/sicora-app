# SICORA API Gateway

Gateway principal para todos los microservicios de SICORA, integrando tanto el stack Python como el stack Go.

## 🚀 Características

- **Integración Completa**: Soporte para todos los microservicios de ambos stacks (Python/FastAPI y Go)
- **Autenticación Centralizada**: Middleware de autenticación con cache y fallback
- **Health Checks**: Monitoreo del estado de todos los servicios
- **Documentación Automática**: Swagger UI y ReDoc integrados
- **Manejo de Errores**: Gestión robusta de errores y timeouts
- **CORS Configurado**: Soporte para aplicaciones web
- **Docker Ready**: Dockerfile y docker-compose incluidos

## 📋 Servicios Integrados

### Stack Python (FastAPI)

- **UserService** (`/api/v1/users`) - Gestión de usuarios y autenticación
- **AttendanceService** (`/api/v1/attendance`) - Registro de asistencia
- **EvalinService** (`/api/v1/evalin`) - Evaluaciones internas
- **ScheduleService** (`/api/v1/schedules`) - Gestión de horarios
- **MevalService** (`/api/v1/meval`) - Meta-evaluaciones y análisis
- **KBService** (`/api/v1/kb`) - Base de conocimiento
- **AIService** (`/api/v1/ai`) - Asistente de IA y chat inteligente

### Stack Go

- **UserService Go** (`/api/v1/go/users`) - Gestión de usuarios (Go)
- **AttendanceService Go** (`/api/v1/go/attendance`) - Asistencia (Go)
- **ScheduleService Go** (`/api/v1/go/schedules`) - Horarios (Go)
- **EvalinService Go** (`/api/v1/go/evaluations`) - Evaluaciones (Go)
- **ProjectEvalService Go** (`/api/v1/go/project-evaluations`) - Evaluaciones de proyecto
- **SoftwareFactoryService Go** (`/api/v1/go/software-factory`) - Fábrica de software

## 🔧 Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- Docker (opcional)
- Servicios de SICORA ejecutándose

### Instalación Local

1. **Clonar y configurar**:

```bash
cd sicora-be-python/apigateway
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configurar variables de entorno**:

```bash
export JWT_SECRET_KEY="your-secret-key"
export GATEWAY_PORT=8000
export DEBUG=false
export PYTHON_SERVICES_ENABLED=true
export GO_SERVICES_ENABLED=true
```

3. **Iniciar el gateway**:

```bash
./start_gateway.sh
# O directamente:
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Instalación con Docker

```bash
# Construir imagen
docker build -t sicora/apigateway .

# Ejecutar con docker-compose
docker-compose up -d
```

## 📖 Uso

### Endpoints Principales

- **Documentación**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **API Root**: `http://localhost:8000/`

### Autenticación

El API Gateway maneja la autenticación de forma centralizada:

1. **Login**: `POST /api/v1/users/auth/login`
2. **Usar token**: Incluir `Authorization: Bearer <token>` en headers
3. **Validation**: El gateway valida automáticamente los tokens

### Ejemplo de Uso

```bash
# 1. Login
curl -X POST "http://localhost:8000/api/v1/users/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# 2. Usar servicios con token
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/v1/ai/chat/sessions"

# 3. Verificar salud
curl "http://localhost:8000/health"
```

## 🧪 Pruebas

Ejecutar suite de pruebas completa:

```bash
./test_gateway.sh
```

O configurar URL personalizada:

```bash
API_GATEWAY_URL=http://localhost:8000 ./test_gateway.sh
```

## 🔒 Seguridad

### Autenticación

- Tokens JWT validados con UserService
- Cache de tokens para mejor rendimiento
- Fallback a servicios Go si Python falla
- Endpoints públicos configurables

### Autorización

- Roles: `admin`, `instructor`, `coordinador`, `aprendiz`
- Middleware de roles específicos
- Validación automática por endpoint

### Configuración de Seguridad

```bash
# Variables críticas
export JWT_SECRET_KEY="your-secret-key-here"
export CORS_ORIGINS="https://your-frontend.com"
export SERVICE_TIMEOUT=30
```

## 📊 Monitoreo

### Health Checks

El endpoint `/health` proporciona:

- Estado del gateway
- Estado de todos los servicios
- Tiempos de respuesta
- Servicios disponibles/no disponibles

### Logs

```bash
# Ver logs en desarrollo
uvicorn main:app --log-level debug

# En Docker
docker logs sicora-apigateway
```

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable                  | Descripción                | Valor por Defecto       |
| ------------------------- | -------------------------- | ----------------------- |
| `GATEWAY_HOST`            | Host del gateway           | `0.0.0.0`               |
| `GATEWAY_PORT`            | Puerto del gateway         | `8000`                  |
| `DEBUG`                   | Modo debug                 | `false`                 |
| `JWT_SECRET_KEY`          | Clave secreta JWT          | `sicora-gateway-secret` |
| `SERVICE_TIMEOUT`         | Timeout para servicios     | `30`                    |
| `PYTHON_SERVICES_ENABLED` | Habilitar servicios Python | `true`                  |
| `GO_SERVICES_ENABLED`     | Habilitar servicios Go     | `true`                  |

### URLs de Servicios

Configurar URLs personalizadas:

```bash
export USER_SERVICE_URL="http://custom-userservice:8001"
export AI_SERVICE_URL="http://custom-aiservice:8007"
export USER_GO_SERVICE_URL="http://custom-userservice-go:8101"
```

## 🐛 Troubleshooting

### Problemas Comunes

1. **503 Service Unavailable**:

   - Verificar que los servicios estén ejecutándose
   - Revisar URLs de servicios en `service_discovery.py`
   - Comprobar conectividad de red

2. **401 Unauthorized**:

   - Verificar que UserService esté disponible
   - Comprobar configuración JWT
   - Revisar logs de autenticación

3. **Timeout Errors**:
   - Aumentar `SERVICE_TIMEOUT`
   - Verificar latencia de red
   - Revisar recursos del servidor

### Verificación Rápida

```bash
# Verificar conectividad básica
curl -v http://localhost:8000/health

# Verificar servicios críticos
curl -v http://userservice:8001/health
curl -v http://aiservice:8007/health
```

## 📝 Desarrollo

### Agregar Nuevos Servicios

1. **Actualizar `service_discovery.py`**:

```python
DEFAULT_SERVICE_URLS = {
    # ... servicios existentes ...
    "nuevo-servicio": "http://nuevoservicio:8009"
}
```

2. **Crear router en `routers/`**:

```python
# routers/nuevo_servicio.py
from fastapi import APIRouter
router = APIRouter(tags=["nuevo-servicio"])
```

3. **Registrar en `main.py`**:

```python
from routers.nuevo_servicio import router as nuevo_router
app.include_router(nuevo_router, prefix="/api/v1/nuevo", tags=["nuevo"])
```

### Estructura del Proyecto

```
apigateway/
├── main.py                 # Aplicación principal
├── config.py              # Configuración
├── requirements.txt       # Dependencias
├── Dockerfile             # Imagen Docker
├── docker-compose.yml     # Orquestación
├── start_gateway.sh       # Script de inicio
├── test_gateway.sh        # Suite de pruebas
├── middleware/
│   ├── auth.py            # Autenticación
│   └── auth_v2.py         # Versión mejorada
├── routers/               # Routers por servicio
│   ├── users.py
│   ├── ai.py
│   ├── knowledge_base.py
│   ├── go_services.py
│   └── ...
├── utils/
│   └── service_discovery.py  # Descubrimiento de servicios
└── health/
    └── checker.py         # Health checks
```

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Hacer commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📄 Licencia

Este proyecto es parte de SICORA y está sujeto a las políticas del SENA.

## 🆘 Soporte

Para soporte técnico:

- Crear issue en el repositorio
- Contactar al equipo de desarrollo
- Revisar documentación en `/docs`

---

**SICORA API Gateway v2.0.0** - Sistema Integral de Control de Registro de Asistencia
