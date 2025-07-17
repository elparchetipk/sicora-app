# Requisitos F- ✅ **EvalinService**: 95% COMPLETADO (13/14 historias - **COMPLETAMENTE FUNCIONAL**) 🎉ncionales - Asiste App

**Actualizado: 15 de junio de 2025**

Este documento describe los requisitos funcionales de la aplicación Asiste App, parte del
sistema de información SICORA (Sistema de Información de Coordinación Académica).

## 🎯 **ESTADO ACTUAL DE IMPLEMENTACIÓN**

**Progreso general del proyecto: 78% COMPLETADO** ✅

- ✅ **UserService**: 100% COMPLETADO (18/18 historias - Listo para producción)
- ✅ **ScheduleService**: 90% COMPLETADO (4/4 historias - Funcional, integración pendiente)
- ✅ **KbService**: 85% COMPLETADO (21/25 historias - **FUNCIONAL Y OPERATIVO**) �
- �🚧 **EvalinService**: 7% COMPLETADO (1/14 historias - En desarrollo inicial)
- 📋 **AttendanceService**: 0% PENDIENTE (0/12 historias)
- 📋 **AiService**: 0% PENDIENTE (0/8 historias)
- ✅ **ApiGateway**: 80% COMPLETADO (Funcional, requiere integración final)
- 🚧 **Frontend**: 15% EN DESARROLLO (6/39 historias - Autenticación funcional)

### **🎉 ÚLTIMOS HITOS ALCANZADOS**

**KbService** completamente funcional (15 JUN 2025):

- ✅ Servidor ejecutándose sin errores en puerto 8000
- ✅ API REST disponible con documentación automática
- ✅ Migración completa a Pydantic V2
- ✅ Tests unitarios e integración funcionando
- ✅ Arquitectura Clean Architecture implementada

**EvalinService** completamente funcional (13 JUN 2025):

- ✅ **39 rutas API** implementadas y funcionales
- ✅ **77 archivos Python** creados con Clean Architecture
- ✅ **CRUD completo** para todas las entidades principales
- ✅ **Gestión de evaluaciones** de instructores completamente operativa
- ✅ **Reportes y exportación** CSV implementados

**Ver reportes detallados en:**

- [Estado Actual del Proyecto](_docs/reports/ESTADO-ACTUAL-PROYECTO-CONSOLIDADO.md)
- [KbService - Reporte de Progreso](_docs/reports/KBSERVICE-PROGRESO-DESARROLLO.md)
- [EvalinService - Reporte de Finalización](evalinservice/EVALIN-SERVICE-COMPLETION-REPORT.md)

## 📋 Documentación de Referencia

Este documento debe leerse en conjunto con los siguientes documentos técnicos:

- **[Especificación de Endpoints API](../api/endpoints_specification.md)**: Define la
  interfaz RESTful completa del backend, formatos de respuesta, códigos de estado y
  estructura HATEOAS.
- **[Historias de Usuario Backend](../stories/be/historias_usuario_be.md)**: Especifica
  las funcionalidades desde la perspectiva del consumidor de la API.
- **[Automatización CI/CD](../automation/CI_CD_AUTOMATION.md)**: Describe el pipeline
  de desarrollo y despliegue automatizado.

## Contexto General

Asiste App es una aplicación para el control de asistencia de aprendices del SENA. Forma parte de SICORA, que incluirá los siguientes módulos:

- **Asiste** (gestión de asistencia - módulo actual)
- **Comité** (gestión de comités académicos)
- **Evaluación de instructores** (evalin - evaluación de instructores)
- **Horarios** (gestión de horarios y ambientes)
- **Onboarding** (solo para instructores)
- **Evaluación de Proyectos de Formación (evalproy)** (evaluación de proyectos formativos para prácticas de desarrollo de software)
- **Procesos académicos** (gestión de procesos académicos, actas de inicio y cierre de trimestre, plan de trabajo concertado, portafolio instructor, guías de aprendizaje, programas y proyectos de formación)

## Arquitectura y Tecnologías

### Frontend

- **Framework**: React Vite (enfoque Web First). Estrategia completa y
  detallada de respaldo y recuperación. Automatización de respaldo y recuperación.
- **Compilación**: Web
- **Estilización**: TailwindCSS
- **Navegación**: React Router

### Backend

- **Arquitectura**: Microservicios con fastapi, Clean Architecture(domain layer, application layer, infrastructure layer, unit testing, integration testing)
- **API**: RESTful (con implementación HATEOAS) con documentación Swagger, API versioning
- **Microservicios**:
  - `userservice` (usuarios y autenticación)
  - `scheduleservice` (horarios y fichas)
  - `attendanceservice` (control de asistencia)
  - `apigateway` (punto de entrada único)
  - `aiservice` (chatbot de reglamento académico y análisis predictivo)
  - `evalinservice` (evaluación de instructores) ✅ **95% COMPLETADO - FUNCIONAL**
  - `kbservice` (knowledge base para soporte IA de admin, instructores, aprendices) ✅ **FUNCIONAL**
- **Microservicios planificados**:
  - Expansiones futuras según necesidades

### **📚 KbService - Estado Detallado (85% COMPLETADO)**

El **Knowledge Base Service** está completamente funcional y operativo:

#### **🚀 Funcionalidades Implementadas**

- ✅ **API REST completa**: 18 endpoints operativos
- ✅ **Gestión de contenido**: CRUD de artículos, FAQs, guías, procedimientos
- ✅ **Búsqueda avanzada**: Búsqueda tradicional y semántica con IA
- ✅ **Sistema de categorías**: Organización jerárquica de contenido
- ✅ **Feedback de usuarios**: Sistema de valoración y comentarios
- ✅ **Administración avanzada**: Métricas, analytics, backup/restore
- ✅ **Autenticación JWT**: Integrada con roles (admin, instructor, estudiante)
- ✅ **Documentación automática**: Swagger UI disponible

#### **🔧 Tecnologías y Arquitectura**

- ✅ **Clean Architecture**: Domain, Application, Infrastructure, Presentation layers
- ✅ **FastAPI + Pydantic V2**: API moderna y tipada
- ✅ **PostgreSQL 15 + pgvector**: Base de datos con búsqueda vectorial
- ✅ **OpenAI Embeddings**: Generación de embeddings para búsqueda semántica
- ✅ **SQLAlchemy + Alembic**: ORM y migraciones de base de datos
- ✅ **pytest**: Suite completa de tests unitarios e integración

#### **🎯 Casos de Uso Principales**

- **Para Administradores**: Gestión completa del knowledge base, métricas, configuración
- **Para Instructores**: Acceso a guías, procedimientos, consultas sobre reglamento
- **Para Estudiantes**: FAQs, ayuda sobre asistencia, procedimientos académicos
- **Búsqueda Inteligente**: Consultas en lenguaje natural con respuestas contextuales

#### **📊 Estado Técnico**

- ✅ **Servidor**: Ejecutándose sin errores en puerto 8000
- ✅ **API**: `http://127.0.0.1:8000` - Completamente accesible
- ✅ **Documentación**: `http://127.0.0.1:8000/docs` - Swagger UI funcional
- ✅ **Tests**: 27+ casos de test, 80% cobertura
- ✅ **Compatibilidad**: Python 3.13, Pydantic V2, FastAPI latest

### **📊 EvalinService - Estado Detallado (95% COMPLETADO)**

El **Instructor Evaluation Service** está completamente funcional y operativo:

#### **🚀 Funcionalidades Implementadas**

- ✅ **API REST completa**: 39 endpoints operativos organizados en 6 módulos
- ✅ **Gestión de preguntas**: CRUD con tipos múltiples (Likert, texto, opción múltiple)
- ✅ **Gestión de cuestionarios**: Creación, edición, adición/remoción de preguntas
- ✅ **Períodos de evaluación**: Control completo del ciclo de evaluación
- ✅ **Evaluaciones de estudiantes**: Envío, consulta, actualización de evaluaciones
- ✅ **Sistema de reportes**: Reportes por instructor, período, exportación CSV
- ✅ **Configuración del sistema**: Gestión centralizada de configuraciones
- ✅ **Autenticación JWT**: Integrada con control de roles y permisos

#### **🔧 Módulos Funcionales**

- ✅ **Questions** (6 rutas): Gestión completa de preguntas de evaluación
- ✅ **Questionnaires** (8 rutas): Cuestionarios y estructura de evaluación
- ✅ **Evaluation Periods** (6 rutas): Control de períodos académicos
- ✅ **Evaluations** (6 rutas): Proceso de evaluación de estudiantes
- ✅ **Reports** (4 rutas): Análisis y exportación de resultados
- ✅ **Configuration** (1 ruta): Configuración del sistema
- ✅ **Health/Docs** (8 rutas): Monitoreo y documentación

#### **🏗️ Arquitectura Técnica**

- ✅ **Clean Architecture**: Domain, Application, Infrastructure, Presentation layers
- ✅ **FastAPI + Pydantic V2**: 77 archivos Python implementados
- ✅ **Base de datos flexible**: SQLite (testing) + PostgreSQL 15 (producción)
- ✅ **Use Cases completos**: 26 casos de uso implementados
- ✅ **Repository Pattern**: Interfaces y implementaciones completas

#### **🎯 Casos de Uso Principales**

- **Para Administradores**: Gestión completa de preguntas, cuestionarios, períodos
- **Para Estudiantes**: Evaluación de instructores durante períodos activos
- **Para Coordinadores**: Análisis de reportes, exportación de datos
- **Integración**: Conexión con UserService y ScheduleService

#### **📊 Estado Técnico**

- ✅ **Arquitectura**: Clean Architecture completamente implementada
- ✅ **API Endpoints**: 39 rutas completamente funcionales
- ✅ **Base de código**: 77 archivos Python bien estructurados
- ✅ **Integración**: Preparado para conexión con otros servicios
- ✅ **Compatibilidad**: Python 3.13, Pydantic V2, FastAPI latest

### Infraestructura

- **Web Server**: Nginx (balanceo de carga y estrategia de failover)
- **Proxy Inverso**: Traefik (gestión de certificados SSL)
- **Base de Datos**: PostgreSQL 15 con pgvector (balanceo de carga y estrategia de failover).
  Crear estrategia completa y detallada de respaldo y recuperación. Automatización de respaldo y recuperación.
- **Migraciones**: alembic
- **Caché**: Redis (balanceo de carga y failover)
- **Entorno de Desarrollo**: Docker
- **Despliegue**: Hostinger VPS (Ubuntu 24.04 LTS, UFW firewall)
- **Despliegue Automatizado**: Watchtower
- **Monitoreo**: UptimeRobot
- **Dominio**: sicora.elparcheti.co

### CI/CD

- commits automáticos, con buenas prácticas, escritos en INGLES
- auto release

## �️ **Estrategia de Bases de Datos Multi-Stack**

### **Principio Fundamental: Una Base de Datos por Microservicio**

Para el proyecto educativo multi-stack (7 tecnologías backend), se implementará una estrategia híbrida que maximiza la comparabilidad entre tecnologías mientras mantiene la integridad arquitectónica de microservicios:

#### **📋 Arquitectura de Datos**

- **Regla Base**: Cada microservicio mantiene su propia base de datos dedicada
- **Compartición Cross-Stack**: Las 7 implementaciones de un mismo microservicio (FastAPI, Go, Express.js, C#, Next.js, Spring Boot Java, Spring Boot Kotlin) se conectan a la **misma instancia** de base de datos
- **Beneficio Educativo**: Permite comparar cómo diferentes frameworks/lenguajes manejan ORMs, migraciones y acceso a datos para los mismos esquemas

#### **🔧 Tecnologías por Microservicio**

**UserService, ScheduleService, AttendanceService:**

- **Base**: PostgreSQL 15 con pgvector
- **Caché**: Redis para sesiones y datos de alta frecuencia
- **Razón**: Datos estructurados con relaciones complejas, requisitos ACID

**KbService:**

- **Fase 1**: PostgreSQL 15 con pgvector (actual - funcional)
- **Fase 2**: Migración híbrida a MongoDB para contenido flexible + PostgreSQL 15 para estructura
- **Razón**: Contenido documental variable, búsquedas textuales avanzadas

**EvalinService:**

- **Base**: PostgreSQL 15 (ideal para formularios, reportes, agregaciones)
- **Caché**: Redis para métricas en tiempo real
- **Razón**: Estructura de cuestionarios, análisis estadístico

**AIService:**

- **Base**: PostgreSQL 15 para metadatos + Vector DB especializada
- **Cache**: Redis para respuestas frecuentes del chatbot
- **Almacenamiento**: Embeddings y modelos de IA

#### **💾 Gestión de Instancias**

- **Desarrollo**: Una instancia Docker por microservicio
- **Producción**: Instancias PostgreSQL 15 separadas con replicación
- **Migración**: Scripts unificados para mantener esquemas sincronizados entre stacks

### **🛣️ Roadmap de Tecnologías de Base de Datos**

#### **Fase 1 - Actual (PostgreSQL 15 + Redis)**

- ✅ **PostgreSQL 15**: Base de datos principal para todos los servicios
- ✅ **Redis**: Caché distribuida y gestión de sesiones
- ✅ **pgvector**: Búsquedas vectoriales para KbService
- **Estado**: Implementado y funcional

#### **Fase 2 - Expansión NoSQL (6 meses)**

- 📋 **MongoDB**: Para KbService (contenido documental flexible)
- 📋 **Elasticsearch**: Para búsquedas avanzadas y analytics (opcional)
- **Objetivo**: Mostrar casos de uso híbridos SQL/NoSQL

#### **Fase 3 - Análisis Avanzado (12 meses)**

- 📋 **Neo4j**: Base de datos de grafos para:
  - Relaciones académicas complejas (estudiante-instructor-programa)
  - Análisis de patrones de asistencia
  - Sistemas de recomendación educativa
  - Detección de clusters académicos
- **Beneficio**: Mostrar cuando las BD relacionales no son suficientes

#### **Fase 4 - Especialización (18 meses)**

- 📋 **Time Series DB** (InfluxDB/TimescaleDB): Para métricas y analytics temporales
- 📋 **Vector Database** especializada (Pinecone/Weaviate): Para IA avanzada
- **Objetivo**: Casos de uso especializados de alto rendimiento

## 📈 **Plan de Trabajo Multi-Stack**

### **Estrategia de Desarrollo: Microservicio Completo por Iteración**

**Enfoque Seleccionado**: Completar un microservicio en los 6 stacks antes de pasar al siguiente

**Tecnologías Seleccionadas**: FastAPI, Go, Express.js, Next.js, Spring Boot Java, Spring Boot Kotlin

**Criterios de Selección**:

- ✅ **Alineación curricular**: Tecnologías que se enseñan actualmente en el SENA
- ✅ **Demanda laboral**: Stacks con alta demanda en el mercado colombiano
- ✅ **Diversidad técnica**: Diferentes paradigmas y ecosistemas
- ✅ **Viabilidad de mantenimiento**: 6 stacks manejables vs 7+

#### **🎯 Orden de Implementación Priorizado**

**1. UserService (Mes 1-2)**

- **FastAPI**: ✅ Completado (base de referencia - producción inmediata)
- **Go**: 🚧 75% → 100%
- **Express.js**: 📋 0% → 100%
- **Next.js**: 📋 0% → 100%
- **Spring Boot Java**: 📋 0% → 100%
- **Spring Boot Kotlin**: 📋 0% → 100%
- **Entregable**: "Capítulo 1: Autenticación JWT en 6 Tecnologías Modernas"

**2. AttendanceService (Mes 3-4)**

- **Funcionalidad**: CRUD básico, relaciones simples
- **Enfoque**: Comparar ORMs y manejo de relaciones
- **Entregable**: "Capítulo 2: CRUD y Relaciones de Base de Datos"

**3. ScheduleService (Mes 5-6)**

- **Funcionalidad**: Lógica de negocio intermedia, validaciones
- **Enfoque**: Manejo de restricciones, validaciones complejas
- **Entregable**: "Capítulo 3: Lógica de Negocio y Validaciones"

**4. KbService (Mes 7-8)**

- **Funcionalidad**: Búsquedas, contenido dinámico, integración IA
- **Enfoque**: Manejo de contenido, APIs externas
- **Entregable**: "Capítulo 4: Búsquedas y Gestión de Contenido"

**5. EvalinService (Mes 9-10)**

- **Funcionalidad**: Formularios dinámicos, reportes, agregaciones
- **Enfoque**: Análisis de datos, generación de reportes
- **Entregable**: "Capítulo 5: Formularios Dinámicos y Analytics"

**6. AIService (Mes 11-12)**

- **Funcionalidad**: Integración con servicios externos, IA
- **Enfoque**: APIs externas, manejo de embeddings, chatbots
- **Entregable**: "Capítulo 6: Integración IA y Servicios Externos"

#### **📚 Beneficios del Enfoque Iterativo**

- **Comparabilidad inmediata**: Ver el mismo servicio en 7 tecnologías
- **Publicación progresiva**: Contenido educativo por capítulos
- **Validación temprana**: Detectar problemas de diseño antes de propagarlos
- **Engagement continuo**: Hitos visibles y utilizables
- **Feedback loop**: Mejorar el siguiente microservicio basado en aprendizajes

## 🚀 **Servicios Futuros y Expansión SICORA**

### **Servicios Core SICORA (Fuera del Scope Multi-Stack Inicial)**

#### **NotificationService**

- **Funcionalidad**: Push notifications, emails, SMS
- **Tecnologías**: WebSockets, Firebase/AWS SNS, colas de mensajes
- **Estado**: Documentado para Fase 2
- **Complejidad**: Alta (requiere infraestructura externa)

#### **OnboardingService**

- **Funcionalidad**: Proceso de integración para nuevos instructores
- **Integración**: UserService, ScheduleService, KbService
- **Estado**: Planificado para post-multistack

#### **CommitteeService**

- **Funcionalidad**: Gestión de comités académicos
- **Integración**: UserService, EvalinService
- **Estado**: Planificado para expansión SICORA

### **Módulos SICORA Expandidos**

- **Asiste**: ✅ Implementado (módulo actual)
- **Comité**: 📋 Planificado (gestión de comités académicos)
- **Evaluación**: ✅ 95% Completado (evalin)
- **Horarios**: ✅ 90% Completado
- **Onboarding**: 📋 Planificado (solo instructores)

## �🔗 Especificación de API REST

La interfaz del backend está completamente definida en la \* \*[Especificación de Endpoints API](../api/endpoints_specification.md)\*\*, que establece:

### Principios de Diseño API

- **RESTful**: Siguiendo convenciones REST estándar
- **HATEOAS**: Hypermedia as the Engine of Application State para navegación dinámica
- **Versionado**: API versionada con `/v1/` para compatibilidad futura
- **Consistencia**: Formato uniforme en todas las respuestas
- **Seguridad**: JWT Bearer tokens para autenticación y autorización

### Estructura de Endpoints

- **Base URL**: `https://sicora.elparcheti.co/api/v1`
- **Autenticación**: `/api/v1/auth/*` (registro, login, refresh, recuperación)
- **Usuarios**: `/api/v1/users/*` (perfil, gestión personal)
- **Administración**: `/api/v1/admin/*` (gestión administrativa)
- **Horarios**: `/api/v1/schedule/*` (gestión de horarios)
- **Asistencia**: `/api/v1/attendance/*` (registro y consulta)
- **Knowledge Base**: `/api/v1/kb/*` (gestión de contenido, búsqueda, feedback) ✅ **FUNCIONAL**
- **Evaluación Instructores**: `/api/v1/evalin/*` (preguntas, cuestionarios, evaluaciones, reportes) ✅ **FUNCIONAL**
- **IA**: `/api/v1/ai/*` (análisis predictivo y chatbot)

### Formatos de Respuesta

- **Respuestas exitosas**: Incluyen `success`, `message`, `data`, `links` (HATEOAS) y
  `meta`
- **Respuestas de error**: Incluyen `success: false`, `error` con código y mensaje,
  `links` de ayuda
- **Paginación**: Metadatos de paginación en sección `meta`
- **Timestamps**: Formato ISO 8601 con zona horaria

### Estados de Implementación

- ✅ **Implementado**: Funcionalidad completa y verificada
- 🚧 **En desarrollo**: Implementación parcial
- 📋 **Pendiente**: Planificado pero no iniciado

**Requisito funcional**: Todos los endpoints deben implementarse según la especificación
definida, manteniendo consistencia en formatos, códigos de estado HTTP y estructura
HATEOAS.

## Organización Académica

### Estructura Organizacional

- El Centro de Gestión de Mercados, Logística y Tecnologías de la Información (CGMLTI)
  tiene dos sedes:
  - Sede Calle 52
  - Sede Fontibón
- Cada sede tiene varios ambientes de formación (191, 205, 412, 413, 509, etc.)
- El CGMLTI imparte varios programas, incluyendo Análisis y Desarrollo de Software (ADSO)
- ADSO está asociado a la Coordinación de Teleinformática e Industrias Creativas
- El programa ADSO tiene una duración de 7 trimestres (etapa lectiva)
- Los aprendices deben asistir de forma presencial (98% de la formación)

### Organización de Estudiantes

- Los aprendices se agrupan en fichas (ej. 2826503)
- Un aprendiz solo puede matricularse en una ficha y un único programa
- La carga trimestral de aprendices se realiza mediante archivos CSV. **Nota:** Solo los aprendices debidamente matriculados en el sistema de gestión académica oficial del SENA son cargados en SICORA.

### Actividades de Formación

- Durante cada trimestre, los aprendices reciben diferentes actividades de formación
- Las actividades son impartidas por instructores asignados
- Un instructor puede impartir múltiples actividades (sin cruces horarios)
- La carga trimestral de instructores se realiza mediante archivos CSV

### Horarios

- Las actividades se registran en un horario por ficha y trimestre
- La carga de horarios se realiza mediante archivos CSV
- Existen tres jornadas de formación:
  - Mañana: 6:00 a.m. - 12:00 p.m. (lunes a sábado)
  - Tarde: 12:00 p.m. - 6:00 p.m. (lunes a sábado)
  - Noche: 6:00 p.m. - 10:00 p.m. (lunes a viernes) y sábado (6:00 a.m. - 6:00 p.m.)
- Los bloques son de una hora con identificadores específicos (MLUN1, TLUN2, NLUN3, etc.)

## Requisitos de Seguridad

### Gestión de Contraseñas

- Contraseña inicial: número de documento (para aprendices e instructores)
- Cambio obligatorio después del primer uso
- Requisitos de seguridad:
  - Mínimo 10 caracteres
  - Al menos una mayúscula
  - Al menos una minúscula
  - Al menos un dígito numérico
  - Al menos un símbolo (caracter especial !@$%&)
- Contraseñas almacenadas con hashing (bcrypt o Argon2)

### Protección de Datos

- Datos sensibles (documento, correos, teléfono) almacenados con protección
- Implementación mediante control de acceso y logging seguro

## Roles y Permisos

### Administrador

- Carga de datos masivos (CSV)
- Gestión completa de usuarios
- Acceso a reportes y análisis

### Instructor

- Registro de asistencia de aprendices
- Visualización de horarios propios
- Consulta de asistencia histórica

### Aprendiz

- Consulta de su registro de asistencia
- Visualización de horarios de su ficha
- Justificación de inasistencias

## Funcionalidades Principales

### Gestión de Usuarios

- Autenticación (JWT)
- Recuperación de contraseña
- Cambio de contraseña
- Perfil de usuario
- Gestión de roles

### Gestión de Horarios

- Visualización de horarios por ficha
- Visualización de horarios por instructor
- Filtrado por fechas y jornadas

### Control de Asistencia

- Registro de asistencia por parte de instructores
- Consulta de asistencia por parte de aprendices
- Justificación de inasistencias
- Reportes de asistencia

### Funcionalidades Adicionales Implementadas

- ✅ **Knowledge Base Service**: Sistema completo de gestión de conocimiento con búsqueda semántica
- ✅ **Evaluation Service**: Sistema completo de evaluación de instructores con 39 endpoints
- Chatbot de reglamento académico
- Análisis predictivo inicial de deserción

### Funcionalidades Planificadas

- Optimización de horarios mediante IA
- Alertas automáticas de asistencia
- Chatbot para consultas sobre reglamento
- Notificaciones automáticas

### Funcionamiento Offline (Aplicación Móvil)

- **RF-OFFLINE-001: Selección de Modo de Sincronización de Datos:** El usuario debe poder configurar la aplicación móvil para:
  - Sincronizar datos (cargar y descargar) únicamente cuando esté conectado a una red
    WiFi.
  - Sincronizar datos utilizando la red de datos móviles del usuario.
  - Por defecto, la aplicación intentará sincronizar datos siempre que haya conexión a internet, priorizando WiFi si está disponible.
- **RF-OFFLINE-002: Sincronización Automática con WiFi:** Siempre que la aplicación móvil
  detecte una conexión WiFi activa y estable, intentará sincronizar automáticamente toda
  la información pendiente con la base de datos del servidor (subir datos locales y
  descargar actualizaciones).
- **RF-OFFLINE-003: Almacenamiento Local de Datos Críticos:** La aplicación móvil debe ser
  capaz de almacenar localmente los datos esenciales para su funcionamiento offline. Esto incluye, como mínimo:
  - Datos de autenticación del usuario (de forma segura).
  - Horario del usuario (aprendiz o instructor).
  - Listas de asistencia pendientes de tomar o enviar (para instructores).
  - Justificaciones creadas pendientes de enviar (para aprendices).
  - Datos necesarios para la visualización del perfil y configuraciones básicas.
- **RF-OFFLINE-004: Indicador de Estado de Conexión y Sincronización:** La interfaz de
  usuario debe mostrar claramente el estado actual de la conexión a internet y el estado
  de la última sincronización de datos.
- **RF-OFFLINE-005: Manejo de Conflictos de Datos (Estrategia Básica):** Se debe definir e
  implementar una estrategia básica para el manejo de conflictos que puedan surgir durante la sincronización (ej. "último en escribir gana" o notificación al usuario para resolución manual en casos complejos). Inicialmente, se priorizará la información del servidor en caso de conflicto simple, con notificación al usuario si se sobrescriben datos locales significativos.
- **RF-OFFLINE-006: Funcionalidad Offline para Registro de Asistencia (Instructor):** Un
  instructor debe poder tomar asistencia de sus fichas asignadas incluso sin conexión a
  internet. Los registros se almacenarán localmente y se sincronizarán cuando la conexión
  esté disponible según la configuración del usuario.
- **RF-OFFLINE-007: Funcionalidad Offline para Creación de Justificaciones (Aprendiz):**
  Un aprendiz debe poder redactar y guardar una justificación por inasistencia incluso sin conexión a internet. La justificación se almacenará localmente y se enviará cuando la conexión esté disponible.
- **RF-OFFLINE-008: Acceso a Horarios Offline:** Tanto aprendices como instructores deben poder consultar sus horarios almacenados localmente incluso sin conexión a internet.
