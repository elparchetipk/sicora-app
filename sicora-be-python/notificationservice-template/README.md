# NotificationService - Microservicio de Notificaciones

## Descripción

NotificationService es un microservicio que proporciona funcionalidades para la gestión de notificaciones en el sistema SICORA. Implementa Clean Architecture para mantener una separación clara de responsabilidades y facilitar el mantenimiento y la escalabilidad.

## Estructura del Proyecto

```
notificationservice/
├── app/
│   ├── __init__.py
│   ├── domain/                     # Capa de dominio
│   │   ├── __init__.py
│   │   ├── entities/               # Entidades del dominio
│   │   │   ├── __init__.py
│   │   │   └── notification.py     # Entidad principal
│   │   ├── repositories/           # Interfaces de repositorios
│   │   │   ├── __init__.py
│   │   │   └── notification_repository.py
│   │   └── value_objects/          # Objetos de valor
│   │       ├── __init__.py
│   │       └── notification_type.py
│   ├── application/                # Capa de aplicación
│   │   ├── __init__.py
│   │   ├── dtos/                   # Data Transfer Objects
│   │   │   ├── __init__.py
│   │   │   └── notification_dtos.py
│   │   └── use_cases/              # Casos de uso
│   │       ├── __init__.py
│   │       └── notification_use_cases.py
│   ├── infrastructure/             # Capa de infraestructura
│   │   ├── __init__.py
│   │   ├── database/               # Configuración de base de datos
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   └── repositories/           # Implementaciones de repositorios
│   │       ├── __init__.py
│   │       └── notification_repository_impl.py
│   └── presentation/               # Capa de presentación
│       ├── __init__.py
│       ├── routers/                # Routers de FastAPI
│       │   ├── __init__.py
│       │   └── notification_router.py
│       └── schemas/                # Schemas de Pydantic
│           ├── __init__.py
│           └── notification_schemas.py
├── main.py                         # Punto de entrada
└── requirements.txt                # Dependencias
```

## Funcionalidades Implementadas

### 1. Gestión de Notificaciones

- **Crear Notificaciones**: Permite crear notificaciones para usuarios con título, mensaje y tipo.
- **Consultar Notificaciones**: Obtiene las notificaciones de un usuario con paginación y filtros.
- **Marcar como Leídas**: Permite marcar notificaciones como leídas.

### 2. Tipos de Notificaciones Soportados

- **Email**: Notificaciones por correo electrónico.
- **Push**: Notificaciones push para dispositivos móviles.
- **In-App**: Notificaciones dentro de la aplicación.

## Arquitectura

El proyecto implementa Clean Architecture con las siguientes capas:

### 1. Domain Layer (Capa de Dominio)

- **Entities**: Contiene la entidad Notification con sus atributos y comportamientos.
- **Value Objects**: Define el objeto de valor NotificationType.
- **Repositories**: Define las interfaces para acceder a los datos.

### 2. Application Layer (Capa de Aplicación)

- **DTOs**: Define los objetos de transferencia de datos.
- **Use Cases**: Implementa la lógica de negocio utilizando las entidades del dominio.

### 3. Infrastructure Layer (Capa de Infraestructura)

- **Database**: Configuración de la base de datos SQLite con SQLAlchemy.
- **Repositories**: Implementaciones concretas de los repositorios definidos en el dominio.

### 4. Presentation Layer (Capa de Presentación)

- **Routers**: Define los endpoints de la API REST.
- **Schemas**: Define los schemas de Pydantic para validación de datos.

## API REST

### Endpoints

```
POST   /api/v1/notifications        # Crear notificación
GET    /api/v1/notifications/{user_id}  # Obtener notificaciones por usuario
PUT    /api/v1/notifications/read   # Marcar notificación como leída
GET    /health                      # Health check
```

### Ejemplos de Uso

#### Crear Notificación

```bash
curl -X POST "http://localhost:8003/api/v1/notifications" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "title": "Nueva actualización",
    "message": "Se ha lanzado una nueva versión de la aplicación",
    "type": "in_app"
  }'
```

#### Obtener Notificaciones de Usuario

```bash
curl -X GET "http://localhost:8003/api/v1/notifications/1?page=1&per_page=10"
```

#### Marcar Notificación como Leída

```bash
curl -X PUT "http://localhost:8003/api/v1/notifications/read" \
  -H "Content-Type: application/json" \
  -d '{
    "notification_id": 1
  }'
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web para crear APIs con Python.
- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **Pydantic**: Validación de datos y serialización.
- **SQLite**: Base de datos ligera para desarrollo.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.

## Configuración y Ejecución

### Requisitos

- Python 3.13+
- pip

### Instalación

1. Clonar el repositorio:

```bash
git clone <repository-url>
cd sicora-app-be-multistack/01-fastapi/notificationservice
```

2. Crear un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Ejecución

```bash
uvicorn main:app --reload --port 8003
```

La API estará disponible en: http://localhost:8003

La documentación Swagger estará disponible en: http://localhost:8003/docs

### Pruebas

Para ejecutar las pruebas (cuando se implementen):

```bash
pytest tests/
```

## Mejoras Futuras

- Implementar tests unitarios y de integración
- Añadir soporte para notificaciones en tiempo real con WebSockets
- Implementar sistema de plantillas para notificaciones
- Añadir soporte para notificaciones programadas
- Integrar con servicios externos de notificaciones (Firebase, AWS SNS, etc.)
- Implementar métricas y monitoreo avanzado

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'feat: add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
