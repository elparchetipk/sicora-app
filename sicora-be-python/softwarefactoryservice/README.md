# SoftwareFactoryService Migration Service

Este directorio contiene las migraciones de base de datos para el microservicio `softwarefactoryservice`, que está implementado en Go pero utiliza el patrón centralizado de migraciones con Alembic desde el stack FastAPI/Python.

## Estructura

```
softwarefactoryservice/
├── alembic/
│   ├── versions/          # Archivos de migración
│   ├── env.py            # Configuración de Alembic
│   └── script.py.mako    # Template para nuevas migraciones
├── alembic.ini           # Configuración de Alembic
├── requirements.txt      # Dependencias
└── README.md            # Este archivo
```

## Configuración

Este servicio de migraciones maneja el esquema `softwarefactoryservice_schema` en la base de datos PostgreSQL compartida `sicora_db`.

### Variables de Entorno

```bash
DATABASE_URL=postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db
```

## Uso

### Crear una nueva migración

```bash
alembic revision --autogenerate -m "descripción de la migración"
```

### Ejecutar migraciones

```bash
alembic upgrade head
```

### Ver historial de migraciones

```bash
alembic history --verbose
```

### Ver migración actual

```bash
alembic current --verbose
```

## Notas Importantes

1. **Esquema Dedicado**: Este servicio maneja únicamente el esquema `softwarefactoryservice_schema`
2. **Coordinación con Go**: Las entidades están definidas en Go con GORM, pero las migraciones se manejan aquí
3. **Tabla de Versiones**: Usa `alembic_version_softwarefactoryservice` para evitar conflictos
4. **Sincronización**: Mantener sincronizadas las entidades Go con las migraciones Alembic

## Entidades del Microservicio

El `softwarefactoryservice` maneja las siguientes entidades principales:

- **Project**: Proyectos de la fábrica de software
- **Team**: Equipos de desarrollo
- **TeamMember**: Miembros de equipos
- **Sprint**: Sprints de desarrollo
- **UserStory**: Historias de usuario
- **Evaluation**: Evaluaciones de aprendices
- **Technology**: Tecnologías utilizadas

## Integración

Este servicio de migraciones se coordina con:

- **Microservicio Go**: `sicora-be-go/softwarefactoryservice`
- **Base de datos**: PostgreSQL esquema `softwarefactoryservice_schema`
- **Inicialización**: Script `database/init/01_init_db_users_schemas.sql`
