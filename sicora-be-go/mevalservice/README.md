# MEvalService - Microservicio de Comités de Evaluación

## 🎯 Descripción

MEvalService es el microservicio del SENA para la gestión integral de Comités de Seguimiento y Evaluación Académico/Disciplinario, desarrollado en cumplimiento del **Acuerdo 009 de 2024**. Implementa Clean Architecture y proporciona una API REST completa para la gestión de comités, casos de estudiantes, planes de mejoramiento, sanciones y apelaciones.

## 🏗️ Arquitectura

```
mevalservice/
├── cmd/
│   └── server/                     # Punto de entrada de la aplicación
├── internal/
│   ├── domain/                     # Capa de Dominio (Clean Architecture)
│   │   ├── entities/               # Entidades del negocio
│   │   └── repositories/           # Interfaces de repositorios
│   ├── application/                # Capa de Aplicación
│   │   ├── dto/                    # Data Transfer Objects
│   │   └── usecases/               # Casos de uso del negocio
│   ├── infrastructure/             # Capa de Infraestructura
│   │   ├── database/               # Configuración de base de datos
│   │   └── repositories/           # Implementación de repositorios
│   ├── presentation/               # Capa de Presentación
│   │   ├── handlers/               # Controladores HTTP
│   │   ├── routes/                 # Configuración de rutas
│   │   └── middleware/             # Middleware HTTP
│   ├── jobs/                       # Trabajos automáticos (cron)
│   └── services/                   # Servicios externos
├── tests/                          # Pruebas (unitarias e integración)
├── migrations/                     # Migraciones de base de datos
└── docs/                          # Documentación adicional
```

## 🚀 Características Principales

### ✅ Funcionalidades Implementadas

- **Gestión de Comités**: CRUD completo con tipos (académico/disciplinario) y subtipos (mensual/extraordinario/apelación/especial)
- **Casos de Estudiantes**: Gestión integral de casos con estados, prioridades y seguimiento
- **Planes de Mejoramiento**: Creación, seguimiento de progreso y evaluación
- **Sanciones**: Gestión de sanciones disciplinarias con tipos y estados
- **Apelaciones**: Sistema completo de apelaciones con procesamiento y resolución
- **Trabajos Automáticos**: Creación automática de comités, alertas y reportes
- **API REST**: Endpoints completos con documentación
- **Validación**: Validación robusta de datos de entrada
- **Logging**: Sistema de logging estructurado
- **Pruebas**: Pruebas unitarias e integración

### 🔄 Flujos Automáticos

- **Comités Mensuales**: Creación automática el primer lunes de cada mes
- **Alertas de Vencimiento**: Notificaciones diarias de casos vencidos
- **Seguimiento de Planes**: Verificación semanal de progreso
- **Gestión de Sanciones**: Verificación diaria de vencimientos
- **Control de Apelaciones**: Alertas de plazos próximos a vencer
- **Reportes Mensuales**: Generación automática de métricas de rendimiento

## 🛠️ Tecnologías

- **Lenguaje**: Go 1.23 + toolchain go1.24.4
- **Framework Web**: Gin
- **ORM**: GORM
- **Base de Datos**: PostgreSQL
- **Cron Jobs**: robfig/cron
- **Testing**: Testify
- **UUID**: Google UUID
- **Variables de Entorno**: godotenv

## 📋 Requisitos Previos

- Go 1.23 o superior
- PostgreSQL 12+
- Make (opcional, para comandos automatizados)

## 🚀 Instalación y Configuración

### 1. Clonar y configurar

```bash
cd sicora-be-go/mevalservice
cp .env.example .env
```

### 2. Configurar variables de entorno

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=sicora_mevalservice
DB_SSLMODE=disable
DB_TIMEZONE=UTC

# Application
APP_ENV=development
PORT=8080
```

### 3. Instalar dependencias

```bash
go mod download
```

### 4. Crear base de datos

```sql
CREATE DATABASE sicora_mevalservice;
```

### 5. Ejecutar migraciones

Las migraciones se ejecutan automáticamente al iniciar la aplicación.

## 🏃‍♂️ Ejecución

### Desarrollo

```bash
# Opción 1: Con go run
go run cmd/server/main.go

# Opción 2: Con make
make run

# Opción 3: Compilar y ejecutar
make build
./server
```

### Producción

```bash
make build-prod
./server
```

### Con Docker

```bash
make docker-build
make docker-run
```

## 🧪 Pruebas

```bash
# Todas las pruebas
make test

# Pruebas con cobertura
make test-coverage

# Solo pruebas unitarias
go test ./tests/... -v

# Solo pruebas de integración
go test ./tests/integration_test.go -v
```

## 📚 API

### Endpoints Principales

```
GET  /health                           # Health check
POST /api/v1/committees                # Crear comité
GET  /api/v1/committees                # Listar comités
POST /api/v1/student-cases             # Crear caso
GET  /api/v1/student-cases/pending     # Casos pendientes
POST /api/v1/improvement-plans         # Crear plan
PATCH /api/v1/improvement-plans/{id}/progress  # Actualizar progreso
POST /api/v1/sanctions                 # Crear sanción
POST /api/v1/appeals                   # Crear apelación
PATCH /api/v1/appeals/{id}/process     # Procesar apelación
```

Ver [API_DOCUMENTATION.md](API_DOCUMENTATION.md) para documentación completa.

### Ejemplo de uso

```bash
# Health check
curl http://localhost:8080/health

# Crear comité
curl -X POST http://localhost:8080/api/v1/committees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Comité Académico Enero 2024",
    "type": "ACADEMIC",
    "subType": "MONTHLY",
    "center": "Centro Biotecnología Industrial",
    "startDate": "2024-01-01T09:00:00Z",
    "endDate": "2024-01-31T17:00:00Z",
    "description": "Comité mensual para evaluación académica"
  }'
```

## 🗄️ Base de Datos

### Entidades Principales

- **Committee**: Comités de evaluación
- **CommitteeMember**: Miembros de comités
- **StudentCase**: Casos de estudiantes
- **ImprovementPlan**: Planes de mejoramiento
- **Sanction**: Sanciones disciplinarias
- **Appeal**: Apelaciones
- **CommitteeDecision**: Decisiones de comité

### Migraciones

```sql
-- Estructura principal en migrations/001_initial_schema.sql
-- Se ejecutan automáticamente al iniciar la aplicación
```

## 🔧 Comandos Make

```bash
make help           # Mostrar ayuda
make run            # Ejecutar en desarrollo
make build          # Compilar
make build-prod     # Compilar para producción
make test           # Ejecutar pruebas
make test-coverage  # Pruebas con cobertura
make clean          # Limpiar archivos compilados
make lint           # Ejecutar linter
make format         # Formatear código
make deps           # Actualizar dependencias
make docker-build   # Construir imagen Docker
make docker-run     # Ejecutar con Docker
```

## 📊 Monitoreo y Métricas

### Logs

```bash
# Ver logs en tiempo real
tail -f logs/mevalservice.log

# Logs estructurados en formato JSON
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "MEvalService",
  "message": "Committee created successfully",
  "committee_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### Health Check

```bash
curl http://localhost:8080/health
```

### Métricas (Futuro)

- Prometheus metrics endpoint: `/metrics`
- Grafana dashboards
- Alert manager integration

## 🔐 Seguridad

### Implementado

- Validación robusta de entrada
- Logging de seguridad
- Error handling seguro

### Por Implementar

- Autenticación JWT
- Autorización basada en roles
- Rate limiting
- HTTPS/TLS
- Encriptación de datos sensibles

## 🚀 Despliegue

### Desarrollo Local

```bash
make run
```

### Docker

```bash
make docker-build
make docker-run
```

### Kubernetes (Futuro)

```yaml
# k8s/deployment.yaml
# k8s/service.yaml
# k8s/configmap.yaml
```

## 🧩 Integración con Otros Servicios

### UserService

- Validación de estudiantes
- Información de instructores
- Roles y permisos

### NotificationService

- Emails automáticos
- Notificaciones push
- SMS para alertas urgentes

### DocumentService

- Almacenamiento de evidencias
- Generación de reportes PDF
- Firmas digitales

## 📈 Rendimiento

### Optimizaciones Implementadas

- Connection pooling de base de datos
- Índices optimizados
- Consultas eficientes con GORM
- Paginación en listados

### Métricas Objetivo

- Response time < 200ms (95th percentile)
- Throughput > 1000 RPS
- Uptime > 99.9%
- Database connections < 100

## 🐛 Troubleshooting

### Problemas Comunes

1. **Error de conexión a BD**

   ```bash
   # Verificar variables de entorno
   cat .env
   # Verificar conectividad
   pg_isready -h localhost -p 5432
   ```

2. **Puerto en uso**

   ```bash
   # Cambiar puerto en .env
   PORT=8081
   ```

3. **Migraciones fallidas**
   ```bash
   # Ejecutar migraciones manualmente
   psql -d sicora_mevalservice -f migrations/001_initial_schema.sql
   ```

## 🤝 Contribución

### Estructura de Commits

```
feat: añadir endpoint para casos urgentes
fix: corregir validación de fechas
docs: actualizar API documentation
test: añadir pruebas para apelaciones
```

### Pull Requests

1. Fork del repositorio
2. Crear rama feature
3. Implementar cambios
4. Añadir pruebas
5. Actualizar documentación
6. Crear PR

## 📄 Licencia

Proyecto del SENA - Uso interno únicamente.

## 👥 Equipo

- **Backend Developer**: Implementación en Go
- **QA Engineer**: Pruebas y calidad
- **DevOps Engineer**: Despliegue y monitoreo
- **Product Owner**: Requisitos y normativa

## 📞 Soporte

- **Issues**: GitHub Issues
- **Email**: devteam@sicora.edu
- **Slack**: #sicora-backend
- **Documentación**: `/docs` directory

## 🔮 Roadmap

### v1.1 (Q2 2024)

- [ ] Autenticación JWT
- [ ] Notificaciones en tiempo real
- [ ] Dashboard administrativo
- [ ] Métricas y monitoring

### v1.2 (Q3 2024)

- [ ] Integración completa con otros servicios
- [ ] Mobile API optimizada
- [ ] Reportes avanzados
- [ ] Audit trails

### v1.3 (Q4 2024)

- [ ] AI/ML para predicción de riesgos
- [ ] Workflow automation
- [ ] Advanced analytics
- [ ] Multi-tenant support

---

**Desarrollado para el SENA en cumplimiento del Acuerdo 009 de 2024**
