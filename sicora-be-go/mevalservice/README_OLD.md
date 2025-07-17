# MEvalService - Microservicio de Comités de Seguimiento y Evaluación

## Descripción

MEvalService es el microservicio encargado de gestionar los Comités de Seguimiento y Evaluación Académico/Disciplinario del SENA, conforme al Reglamento del Aprendiz Acuerdo 009 de 2024.

## Funcionalidades Principales

### Gestión de Comités

- Programación automática de comités mensuales
- Gestión de comités extraordinarios
- Control de quórum y asistencia
- Generación automática de agendas

### Casos de Estudiantes

- Detección automática de casos académicos y disciplinarios
- Gestión del ciclo de vida de casos
- Seguimiento y resolución
- Integración con otros microservicios

### Planes de Mejoramiento

- Creación y seguimiento de planes
- Monitoreo de progreso
- Alertas y notificaciones automáticas

### Sanciones y Apelaciones

- Gestión de sanciones disciplinarias
- Proceso de apelaciones
- Seguimiento de cumplimiento

### Decisiones de Comité

- Registro de decisiones
- Votación digital
- Generación de actas
- Firmas digitales

## Arquitectura

El proyecto sigue Clean Architecture con las siguientes capas:

```
cmd/
  server/          # Punto de entrada de la aplicación
internal/
  domain/
    entities/      # Entidades del dominio
    repositories/  # Interfaces de repositorios
  application/
    dto/           # Objetos de transferencia de datos
    usecases/      # Casos de uso del negocio
  infrastructure/
    database/      # Implementación de base de datos
    repositories/  # Implementación de repositorios
  presentation/
    handlers/      # Controladores HTTP
    routes/        # Definición de rutas
    middleware/    # Middleware HTTP
pkg/               # Utilidades compartidas
tests/             # Pruebas
migrations/        # Migraciones de base de datos
```

## Requisitos

- Go 1.21+
- PostgreSQL 13+
- Docker (opcional)

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd mevalservice
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con los valores apropiados
```

### 3. Instalar dependencias

```bash
make deps
```

### 4. Construir la aplicación

```bash
make build
```

## Uso

### Ejecutar en modo desarrollo

```bash
make dev
```

### Ejecutar pruebas

```bash
make test
```

### Ejecutar con cobertura

```bash
make test-coverage
```

### Construir para producción

```bash
make build
```

### Ejecutar aplicación construida

```bash
make run
```

## API Endpoints

### Comités

- `POST /api/v1/committees` - Crear comité
- `GET /api/v1/committees` - Listar comités
- `GET /api/v1/committees/{id}` - Obtener comité por ID
- `PUT /api/v1/committees/{id}` - Actualizar comité
- `DELETE /api/v1/committees/{id}` - Eliminar comité

### Casos de Estudiantes

- `POST /api/v1/student-cases` - Crear caso
- `GET /api/v1/student-cases/{id}` - Obtener caso por ID
- `PUT /api/v1/student-cases/{id}` - Actualizar caso
- `GET /api/v1/student-cases/pending` - Obtener casos pendientes
- `GET /api/v1/student-cases/overdue` - Obtener casos vencidos

### Health Check

- `GET /health` - Verificar estado del servicio

## Base de Datos

### Configuración

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=sicora_mevalservice
```

### Migraciones

Las migraciones se ejecutan automáticamente al iniciar la aplicación.

## Docker

### Construir imagen

```bash
make docker-build
```

### Ejecutar contenedor

```bash
make docker-run
```

### Usar docker-compose

```bash
make docker-compose-up
```

## Testing

El proyecto incluye pruebas unitarias y de integración:

```bash
# Ejecutar todas las pruebas
make test

# Ejecutar con cobertura
make test-coverage

# Ejecutar pruebas específicas
go test ./internal/domain/entities/...
```

## Contribución

1. Fork el proyecto
2. Crear una rama para la feature (`git checkout -b feature/amazing-feature`)
3. Commit los cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

- **Equipo de Desarrollo**: SICORA Development Team
- **Email**: desarrollo@sicora.edu.co
- **Documentación**: [Confluence/Wiki URL]

## Changelog

### v1.0.0 (Pendiente)

- Implementación inicial del microservicio
- Gestión de comités y casos de estudiantes
- API REST completa
- Integración con base de datos PostgreSQL
- Pruebas unitarias e integración
