# 📚 Documentación Backend Go SICORA

## 🎯 Organización de Documentación

Esta carpeta contiene toda la documentación específica del backend Go SICORA, organizada por temáticas para facilitar la navegación y mantenimiento.

### 📁 Estructura de Carpetas

```
_docs/
├── README.md (este archivo)
├── integracion/        # Integración con frontend y servicios
├── configuracion/      # Configuración de servicios y entornos
├── desarrollo/         # Guías de desarrollo y arquitectura
├── reportes/          # Reportes de estado y verificación
├── microservicios/    # Documentación específica de servicios
└── infraestructura/   # Configuración de infraestructura
```

## 📋 Categorías de Documentación

### 🔗 [Integración](./integracion/)

Documentación relacionada con la integración de servicios:

- Integración frontend-backend
- Comunicación entre microservicios
- Protocolos de API REST
- Configuración de CORS
- Autenticación y autorización

### ⚙️ [Configuración](./configuracion/)

Setup y configuración del entorno:

- Variables de entorno
- Configuración de bases de datos
- Docker y Docker Compose
- Configuración de desarrollo
- Setup de producción

### 🔧 [Desarrollo](./desarrollo/)

Guías y arquitectura de desarrollo:

- Clean Architecture
- Patrones de diseño
- Estándares de código Go
- Testing y TDD
- Mejores prácticas

### 📊 [Reportes](./reportes/)

Reportes de estado y análisis:

- Verificación de versiones Go
- Estados de completación
- Reportes de stack
- Análisis de rendimiento
- Métricas de calidad

### 🎯 [Microservicios](./microservicios/)

Documentación específica de cada servicio:

- UserService - Gestión de usuarios
- AttendanceService - Control de asistencia
- ScheduleService - Gestión de horarios
- ProjectEvalService - Evaluación de proyectos
- EvalinService - Evaluación individual
- KbService - Base de conocimiento
- AIService - Servicios de IA
- SoftwareFactoryService - Gestión de proyectos
- MevalService - Evaluación móvil

### 🏗️ [Infraestructura](./infraestructura/)

Configuración de infraestructura:

- Docker y contenedores
- Bases de datos
- Redis y cache
- Balanceadores de carga
- Monitoreo y observabilidad

## 🚀 Arquitectura del Backend

### 🏛️ Clean Architecture

```
userservice/
├── cmd/                    # Punto de entrada
│   └── main.go
├── internal/               # Código interno
│   ├── domain/            # Entidades y reglas de negocio
│   ├── application/       # Casos de uso
│   ├── infrastructure/    # Implementaciones externas
│   └── presentation/      # Controladores HTTP
├── pkg/                   # Código reutilizable
├── migrations/            # Migraciones de BD
└── tests/                 # Tests
```

### 🔄 Flujo de Datos

```
HTTP Request → Presentation → Application → Domain → Infrastructure → Database
                    ↓
HTTP Response ← JSON Response ← Use Case ← Business Logic ← Repository
```

## 🛠️ Tecnologías por Capa

### 🎨 Presentation Layer

- **Gin**: Framework web HTTP
- **Swagger**: Documentación automática
- **Middleware**: CORS, Authentication, Logging

### 🧠 Application Layer

- **Use Cases**: Lógica de aplicación
- **DTOs**: Data Transfer Objects
- **Validators**: Validación de entrada

### 🏢 Domain Layer

- **Entities**: Modelos de dominio
- **Repositories**: Interfaces de persistencia
- **Services**: Servicios de dominio

### 🔧 Infrastructure Layer

- **GORM**: ORM para PostgreSQL
- **Redis**: Cache y sesiones
- **JWT**: Autenticación
- **Docker**: Contenedores

## 📊 Guía de Navegación

### 👨‍💻 Para Desarrolladores

1. **Empezar aquí**: Lee este README.md
2. **Arquitectura**: Revisa [Desarrollo](./desarrollo/)
3. **Configuración**: Consulta [Configuración](./configuracion/)
4. **Servicios**: Explora [Microservicios](./microservicios/)

### 🔧 Para DevOps

1. **Infraestructura**: Revisa [Infraestructura](./infraestructura/)
2. **Configuración**: Consulta [Configuración](./configuracion/)
3. **Reportes**: Monitorea [Reportes](./reportes/)

### 🔗 Para Integradores

1. **APIs**: Revisa [Integración](./integracion/)
2. **Microservicios**: Consulta [Microservicios](./microservicios/)
3. **Configuración**: Verifica [Configuración](./configuracion/)

## 🎯 Servicios Implementados

### ✅ UserService (COMPLETADO)

**Puerto**: 8002  
**Funcionalidades**:

- ✅ Autenticación JWT
- ✅ CRUD de usuarios
- ✅ Refresh tokens
- ✅ Middleware de seguridad
- ✅ Documentación Swagger

**Endpoints**:

- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/users` - Listar usuarios
- `POST /api/v1/users` - Crear usuario
- `GET /swagger/index.html` - Documentación

### 🔄 AttendanceService (EN DESARROLLO)

**Puerto**: 8003  
**Funcionalidades**:

- 🔄 Control de asistencia
- 🔄 Horarios de entrada/salida
- 🔄 Reportes de asistencia
- 🔄 Integración con calendario

### 🔄 ScheduleService (EN DESARROLLO)

**Puerto**: 8004  
**Funcionalidades**:

- 🔄 Gestión de horarios
- 🔄 Calendarios académicos
- 🔄 Programación de clases
- 🔄 Notificaciones

### 📋 Próximos Servicios

- **ProjectEvalService** (Puerto: 8005)
- **EvalinService** (Puerto: 8006)
- **KbService** (Puerto: 8007)
- **AIService** (Puerto: 8008)

## 📝 Convenciones de Documentación

### 📏 Nomenclatura

- **Archivos**: `TITULO_DOCUMENTO.md` (mayúsculas con guiones bajos)
- **Prefijos por tipo**:
  - `STACK_` - Estados de stack
  - `VERIFICATION_` - Verificaciones
  - `COMPLETION_` - Completaciones
  - `INTEGRATION_` - Integraciones
  - `CONFIG_` - Configuraciones
  - `ARCH_` - Arquitectura

### 📚 Estructura de Documento

```markdown
# Título del Documento

## 🎯 Objetivo

Descripción clara del propósito

## 🛠️ Tecnologías

Tecnologías utilizadas

## 📋 Implementación

Detalles de implementación

## ✅ Conclusiones

Resumen y siguientes pasos

## 📚 Referencias

Enlaces y recursos relacionados
```

## 🔄 Mantenimiento

### ✅ Reglas de Organización

1. **Solo README.md en la raíz** del backend
2. **Toda documentación en `_docs/`** por categorías
3. **Scripts en `scripts/`**
4. **Actualizar índices** cuando se agregue documentación

### 🛠️ Herramientas de Verificación

```bash
# Verificar estructura
./scripts/verify-doc-structure.sh

# Organizar archivos automáticamente
./scripts/verify-doc-structure.sh organize

# Verificar versiones de Go
./scripts/verify-go-versions.sh

# Validar integración
./scripts/validate-integration.sh
```

### 📈 Actualización Regular

- Revisar enlaces rotos mensualmente
- Actualizar documentación de servicios
- Sincronizar con cambios de arquitectura
- Mantener ejemplos actualizados

## 🔍 Métricas de Calidad

### 📊 Cobertura de Documentación

| Categoría       | Archivos | Estado       |
| --------------- | -------- | ------------ |
| Integración     | 0        | 🔄 Por crear |
| Configuración   | 0        | 🔄 Por crear |
| Desarrollo      | 0        | 🔄 Por crear |
| Reportes        | 3        | ✅ Completo  |
| Microservicios  | 0        | 🔄 Por crear |
| Infraestructura | 0        | 🔄 Por crear |

### 🎯 Objetivos de Documentación

- **100% de servicios documentados**
- **Ejemplos funcionales en cada endpoint**
- **Guías de instalación actualizadas**
- **Diagramas de arquitectura claros**

## 📚 Recursos Adicionales

### 🔗 Enlaces Útiles

- [Documentación oficial de Go](https://golang.org/doc/)
- [Gin Web Framework](https://gin-gonic.com/)
- [GORM Documentation](https://gorm.io/docs/)
- [Docker Compose](https://docs.docker.com/compose/)

### 📖 Guías de Estilo

- [Effective Go](https://golang.org/doc/effective_go.html)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### 🧪 Testing

- [Testing in Go](https://golang.org/doc/tutorial/add-a-test)
- [Testify Framework](https://github.com/stretchr/testify)
- [Table-driven tests](https://github.com/golang/go/wiki/TableDrivenTests)

---

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

---

_Esta documentación se actualiza automáticamente. Última actualización: Julio 2025_
_Desarrollado con 🚀 para el SENA - Backend Go SICORA_
