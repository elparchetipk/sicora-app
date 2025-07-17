# sicora-shared

Este módulo es el **punto único de referencia** para modelos de datos, contratos de API, migraciones y utilidades compartidas entre todos los stacks y microservicios de SICORA.

## Objetivo

- Centralizar la definición de entidades, esquemas y contratos de datos.
- Evitar duplicidad de modelos y migraciones en los diferentes stacks.
- Facilitar la interoperabilidad y el versionado de la base de datos.

## Estructura recomendada

- `schemas/entities/` — Modelos de entidades (usuarios, horarios, asistencia, etc.)
- `schemas/requests/` — Esquemas de validación para requests
- `schemas/responses/` — Esquemas de validación para responses
- `api-contracts/` — Contratos de API (OpenAPI, gRPC, GraphQL, etc.)
- `migrations/` — Scripts de migración y versionado de base de datos
- `sample-data/` — Datos de ejemplo y utilidades para pruebas

## Uso recomendado

1. Todos los stacks deben importar o consumir los modelos y contratos desde este módulo.
2. Las migraciones de base de datos deben gestionarse y versionarse aquí o en el stack de referencia.
3. Cualquier cambio en los modelos debe ser versionado y comunicado a todos los equipos.

## Ejemplo de consumo

```python
# Python
from sicora_shared.schemas.entities.user import User
```

## Notas

- Elimina archivos vacíos y mantén solo la estructura útil.
- Documenta cualquier cambio relevante en este archivo.
