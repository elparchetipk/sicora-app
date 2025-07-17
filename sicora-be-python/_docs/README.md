# 📚 Documentación Backend Python SICORA

## 🎯 Organización de Documentación

Esta carpeta contiene toda la documentación específica del backend Python SICORA, organizada por temáticas para facilitar la navegación y mantenimiento.

### 📁 Estructura de Carpetas

```
_docs/
├── README.md (este archivo)
├── integracion/        # Integración de servicios y APIs
├── configuracion/      # Configuración de servicios y entornos
├── desarrollo/         # Guías de desarrollo y arquitectura
├── reportes/          # Reportes de estado y verificación
├── microservicios/    # Documentación específica de servicios
├── ia/                # Servicios de inteligencia artificial
└── apis/              # Documentación de APIs y gateway
```

## 📋 Categorías de Documentación

### 🔗 [Integración](./integracion/)

Documentación relacionada con la integración de servicios:

- Integración AIService-KbService
- Comunicación entre microservicios
- Protocolos de API REST
- Configuración de CORS
- Autenticación y autorización
- Gateway de APIs

### ⚙️ [Configuración](./configuracion/)

Setup y configuración del entorno:

- Variables de entorno
- Configuración de bases de datos
- PostgreSQL con pgvector
- Redis para cache
- Docker y Docker Compose
- Configuración de desarrollo y producción

### 🔧 [Desarrollo](./desarrollo/)

Guías y arquitectura de desarrollo:

- Clean Architecture en Python
- Patrones de diseño FastAPI
- Estándares de código (PEP 8)
- Testing con pytest
- Async/await patterns
- Mejores prácticas Python

### 📊 [Reportes](./reportes/)

Reportes de estado y análisis:

- Estados de completación de servicios
- Reportes de integración
- Análisis de rendimiento
- Métricas de calidad
- Comparativas con otros stacks

### 🎯 [Microservicios](./microservicios/)

Documentación específica de cada servicio:

- UserService - Gestión de usuarios y autenticación
- ScheduleService - Gestión de horarios académicos
- AttendanceService - Control de asistencia
- EvalinService - Sistema de evaluación individual
- ProjectEvalService - Evaluación de proyectos
- KbService - Base de conocimientos
- AIService - Servicios de inteligencia artificial
- ApiGateway - Gateway central de APIs
- SoftwareFactoryService - Gestión de proyectos
- MevalService - Evaluación móvil
- NotificationService - Sistema de notificaciones

### 🤖 [IA](./ia/)

Servicios de inteligencia artificial:

- AIService - Servicios principales de IA
- KbService - Base de conocimientos con búsqueda semántica
- Integración con OpenAI
- Modelos de embedding
- Procesamiento de lenguaje natural
- Análisis de texto y documentos

### 🌐 [APIs](./apis/)

Documentación de APIs y gateway:

- ApiGateway - Configuración central
- Documentación Swagger/OpenAPI
- Endpoints de cada servicio
- Esquemas de validación
- Rate limiting y seguridad
- Versionado de APIs

## 🚀 Arquitectura del Backend

### 🏛️ Clean Architecture en Python

```
userservice/
├── app/
│   ├── domain/             # Capa de dominio
│   │   ├── entities/       # Entidades de negocio
│   │   ├── repositories/   # Interfaces de repositorios
│   │   └── services/       # Servicios de dominio
│   ├── application/        # Capa de aplicación
│   │   ├── use_cases/      # Casos de uso
│   │   └── dtos/          # Data Transfer Objects
│   ├── infrastructure/     # Capa de infraestructura
│   │   ├── repositories/   # Implementaciones de repositorios
│   │   ├── database/      # Configuración de BD
│   │   └── external/      # Servicios externos
│   └── presentation/      # Capa de presentación
│       ├── controllers/   # Controladores HTTP
│       ├── schemas/       # Schemas de validación
│       └── middleware/    # Middleware
├── tests/                 # Tests por capas
├── alembic/              # Migraciones de BD
└── main.py               # Punto de entrada
```

### 🔄 Flujo de Datos

```
HTTP Request → FastAPI → Controller → Use Case → Domain Service → Repository → Database
                  ↓
HTTP Response ← Pydantic ← DTO ← Business Logic ← Entity ← SQLAlchemy
```

## 🛠️ Tecnologías por Capa

### 🎨 Presentation Layer

- **FastAPI**: Framework web de alto rendimiento
- **Pydantic**: Validación y serialización de datos
- **Swagger UI**: Documentación automática
- **Middleware**: CORS, Authentication, Logging

### 🧠 Application Layer

- **Use Cases**: Lógica de aplicación
- **DTOs**: Pydantic models para transferencia
- **Dependency Injection**: Sistema nativo de FastAPI

### 🏢 Domain Layer

- **Entities**: Modelos de dominio puros
- **Repositories**: Interfaces abstractas
- **Services**: Lógica de negocio
- **Value Objects**: Objetos de valor

### 🔧 Infrastructure Layer

- **SQLAlchemy**: ORM para PostgreSQL
- **Alembic**: Migraciones de BD
- **Redis**: Cache y sesiones
- **pgvector**: Búsqueda vectorial para IA

## 📊 Guía de Navegación

### 👨‍💻 Para Desarrolladores Python

1. **Empezar aquí**: Lee este README.md
2. **Arquitectura**: Revisa [Desarrollo](./desarrollo/)
3. **Configuración**: Consulta [Configuración](./configuracion/)
4. **Servicios**: Explora [Microservicios](./microservicios/)
5. **IA**: Revisa [IA](./ia/) para servicios inteligentes

### 🔧 Para DevOps

1. **Infraestructura**: Revisa [Configuración](./configuracion/)
2. **APIs**: Consulta [APIs](./apis/)
3. **Reportes**: Monitorea [Reportes](./reportes/)

### 🤖 Para Desarrolladores de IA

1. **Servicios IA**: Revisa [IA](./ia/)
2. **Integración**: Consulta [Integración](./integracion/)
3. **APIs**: Verifica [APIs](./apis/)

## 🎯 Servicios Implementados

### ✅ UserService (COMPLETADO)

**Puerto**: 8001  
**Funcionalidades**:

- ✅ Autenticación JWT
- ✅ CRUD de usuarios
- ✅ Refresh tokens
- ✅ Middleware de seguridad
- ✅ Swagger automático

**Endpoints**:

- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/users` - Listar usuarios
- `POST /api/v1/users` - Crear usuario

### ✅ AIService (COMPLETADO)

**Puerto**: 8007  
**Funcionalidades**:

- ✅ Chat con IA
- ✅ Análisis de texto
- ✅ Generación de contenido
- ✅ Integración OpenAI

**Endpoints**:

- `POST /api/v1/ai/chat` - Chat conversacional
- `POST /api/v1/ai/analyze` - Análisis de texto
- `POST /api/v1/ai/generate` - Generación

### ✅ KbService (COMPLETADO)

**Puerto**: 8006  
**Funcionalidades**:

- ✅ Base de conocimientos
- ✅ Búsqueda semántica
- ✅ Embeddings vectoriales
- ✅ Gestión de documentos

**Endpoints**:

- `POST /api/v1/kb/search` - Búsqueda semántica
- `POST /api/v1/kb/documents` - Subir documentos
- `GET /api/v1/kb/documents` - Listar documentos

### ✅ ApiGateway (COMPLETADO)

**Puerto**: 8000  
**Funcionalidades**:

- ✅ Enrutamiento centralizado
- ✅ Rate limiting
- ✅ Autenticación global
- ✅ Documentación unificada

### 🔄 Otros Servicios

- **ScheduleService** (Puerto: 8002) - 🔄 En desarrollo
- **AttendanceService** (Puerto: 8003) - 🔄 En desarrollo
- **EvalinService** (Puerto: 8004) - ✅ Completado
- **ProjectEvalService** (Puerto: 8005) - ✅ Completado

## 🤖 Integración de IA

### Arquitectura de IA

```
Frontend → ApiGateway → AIService ↔ KbService ↔ PostgreSQL+pgvector
                           ↓              ↓
                      OpenAI API    Embeddings DB
```

### Flujo de Búsqueda Semántica

1. **Usuario hace pregunta** en frontend
2. **ApiGateway** enruta a AIService
3. **AIService** genera embedding de la pregunta
4. **KbService** busca documentos similares
5. **AIService** genera respuesta contextual
6. **Frontend** muestra respuesta enriquecida

## 📝 Convenciones de Documentación

### 📏 Nomenclatura

- **Archivos**: `TITULO_DOCUMENTO.md` (mayúsculas con guiones bajos)
- **Prefijos por tipo**:
  - `INTEGRACION_` - Documentación de integración
  - `CONFIG_` - Configuraciones
  - `DEVELOPMENT_` - Desarrollo
  - `SERVICE_` - Servicios específicos
  - `AI_` - Servicios de IA
  - `API_` - Documentación de APIs

### 📚 Estructura de Documento

```markdown
# Título del Documento

## 🎯 Objetivo

Descripción clara del propósito

## 🛠️ Tecnologías

Tecnologías específicas utilizadas

## 📋 Implementación

Detalles técnicos de implementación

## 🔄 Endpoints/APIs

Documentación de endpoints (si aplica)

## ✅ Conclusiones

Resumen y siguientes pasos

## 📚 Referencias

Enlaces y recursos relacionados
```

## 🔄 Mantenimiento

### ✅ Reglas de Organización

1. **Solo README.md en la raíz** del backend Python
2. **Toda documentación en `_docs/`** por categorías
3. **Scripts en `scripts/`**
4. **Actualizar índices** cuando se agregue documentación

### 🛠️ Herramientas de Verificación

```bash
# Verificar estructura
./scripts/verify-doc-structure.sh

# Organizar archivos automáticamente
./scripts/verify-doc-structure.sh organize

# Tests de integración
./scripts/test_integration.sh

# Tests simples
./scripts/test_integration_simple.sh
```

### 📈 Actualización Regular

- Revisar enlaces rotos mensualmente
- Actualizar documentación de servicios
- Sincronizar con cambios de APIs
- Mantener ejemplos de IA actualizados

## 🔍 Métricas de Calidad

### 📊 Cobertura de Documentación

| Categoría      | Archivos | Estado       |
| -------------- | -------- | ------------ |
| Integración    | 1        | ✅ Iniciado  |
| Configuración  | 0        | 🔄 Por crear |
| Desarrollo     | 0        | 🔄 Por crear |
| Reportes       | 1        | ✅ Iniciado  |
| Microservicios | 0        | 🔄 Por crear |
| IA             | 0        | 🔄 Por crear |
| APIs           | 0        | 🔄 Por crear |

### 🎯 Objetivos de Documentación

- **100% de servicios documentados**
- **Ejemplos funcionales de IA**
- **Guías de integración actualizadas**
- **Diagramas de arquitectura claros**

## 📚 Recursos Adicionales

### 🔗 Enlaces Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

### 📖 Guías de Estilo

- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Clean Architecture in Python](https://github.com/cosmic-python/book)

### 🧪 Testing y IA

- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest for AI Services](https://docs.pytest.org/en/stable/)
- [Testing OpenAI Integration](https://platform.openai.com/docs/guides/testing)

## 🚨 Alertas Importantes

### ⚠️ Estructura Requerida

- **PROHIBIDO**: Archivos `.md` en la raíz (excepto README.md)
- **REQUERIDO**: Toda documentación en `_docs/`
- **OBLIGATORIO**: README.md en cada subcarpeta

### 🔒 Preservación de Estructura

Esta organización se mantiene automáticamente mediante:

- Scripts de verificación
- Configuración de VS Code
- Instrucciones de Copilot
- Verificaciones de CI/CD

### 🤖 Consideraciones de IA

- **API Keys**: Nunca incluir en documentación
- **Embeddings**: Documentar modelos utilizados
- **Rate Limits**: Considerar límites de OpenAI
- **Costos**: Monitorear uso de APIs

---

## 📊 Estadísticas del Proyecto

### 📁 Servicios por Estado

- **Completados**: 6 servicios (UserService, AIService, KbService, etc.)
- **En desarrollo**: 4 servicios
- **Planificados**: 2 servicios

### 🤖 Capacidades de IA

- **Chat conversacional**: ✅ Implementado
- **Búsqueda semántica**: ✅ Implementado
- **Análisis de texto**: ✅ Implementado
- **Generación de contenido**: ✅ Implementado

---

_Esta documentación se actualiza automáticamente. Última actualización: Julio 2025_
_Desarrollado con 🐍 para el SENA - Backend Python SICORA con IA_
