# 📝 **EVALUACIÓN PRÁCTICA - VII TRIMESTRE ADSO**

**Asignatura:** Análisis y Desarrollo de Software  
**Trimestre:** VII  
**Duración:** 1 semana (7 días calendario)  
**Modalidad:** Práctica individual con acceso al repositorio del proyecto  
**Stack:** FastAPI (Python) - UserService y EvalinService

---

## 🎯 **OBJETIVOS DE APRENDIZAJE**

Al finalizar esta evaluación, el estudiante será capaz de:

1. **Analizar** la arquitectura Clean Architecture implementada en microservicios reales
2. **Implementar** nuevas funcionalidades siguiendo los patrones establecidos
3. **Aplicar** buenas prácticas de desarrollo backend con FastAPI
4. **Validar** y **testear** código siguiendo estándares profesionales
5. **Documentar** APIs usando OpenAPI/Swagger
6. **Integrar** servicios mediante comunicación entre microservicios

---

## 📚 **CONTEXTO Y RECURSOS**

### **📖 Documentación de Apoyo**

- **📋 [Instrucciones Detalladas Paso a Paso](EVALUACION-VII-TRIMESTRE-INSTRUCCIONES-DETALLADAS.md)** ← **¡EMPIEZA AQUÍ!**
- **💻 [Plantillas de Código Listas](EVALUACION-VII-TRIMESTRE-PLANTILLAS-CODIGO.md)** ← **Copia y completa el código**
- **📊 [Rúbrica de Evaluación](EVALUACION-VII-TRIMESTRE-RUBRICA.md)** ← **Cómo serás evaluado**

### **Repositorio de Referencia**

- **Ruta:** `/01-fastapi/userservice` y `/01-fastapi/evalinservice`
- **Documentación:** `_docs/` (especialmente historias de usuario y especificación de APIs)
- **Ejemplos:** Código existente como referencia de implementación

### **Servicios a Trabajar**

- **UserService:** Sistema de autenticación y gestión de usuarios (100% implementado)
- **EvalinService:** Sistema de evaluación de instructores (95% implementado)

### **⚡ Quick Start**

1. **Lee primero:** [Instrucciones Detalladas](EVALUACION-VII-TRIMESTRE-INSTRUCCIONES-DETALLADAS.md)
2. **Usa las plantillas:** [Plantillas de Código](EVALUACION-VII-TRIMESTRE-PLANTILLAS-CODIGO.md)
3. **Verifica con:** [Rúbrica de Evaluación](EVALUACION-VII-TRIMESTRE-RUBRICA.md)

---

## 📋 **ESTRUCTURA DE LA EVALUACIÓN**

### **PARTE 1: ANÁLISIS Y COMPRENSIÓN (20 puntos)**

#### **1.1 Análisis de Arquitectura (10 puntos)**

Analiza y documenta la arquitectura Clean Architecture implementada en ambos servicios:

**Entregables:**

1. **Diagrama de arquitectura** mostrando las 4 capas (Domain, Application, Infrastructure, Presentation)
2. **Documento de análisis** (máximo 2 páginas) que explique:
   - Responsabilidades de cada capa
   - Flujo de datos entre capas
   - Patrones de diseño identificados (Repository, Dependency Injection, etc.)
   - Ventajas de esta arquitectura vs arquitectura monolítica

**Criterios de evaluación:**

- Precisión en la identificación de responsabilidades
- Claridad en la explicación del flujo de datos
- Identificación correcta de patrones de diseño

#### **1.2 Análisis de Casos de Uso (10 puntos)**

Selecciona 3 casos de uso (use cases) de cada servicio y documenta:

**Para cada caso de uso:**

1. **Propósito** y funcionalidad
2. **Entradas** y **salidas**
3. **Dependencias** (repositorios, servicios externos)
4. **Flujo de ejecución** paso a paso
5. **Manejo de errores** implementado

**Entregable:** Documento técnico con el análisis completo

---

### **PARTE 2: IMPLEMENTACIÓN PRÁCTICA (50 puntos)**

#### **2.1 Implementar Nueva Funcionalidad en UserService (25 puntos)**

**Funcionalidad a implementar:** **Sistema de Preferencias de Usuario**

**Requerimientos:**

1. **Entidad Domain:** `UserPreferences`

   ```python
   # Campos requeridos:
   - user_id: UUID
   - language: str (es, en)
   - theme: str (light, dark, auto)
   - notifications_email: bool
   - notifications_push: bool
   - timezone: str
   - created_at: datetime
   - updated_at: datetime
   ```

2. **Endpoints a implementar:**

   ```python
   GET /api/v1/users/preferences        # Obtener preferencias del usuario autenticado
   PUT /api/v1/users/preferences        # Actualizar preferencias
   POST /api/v1/users/preferences/reset # Resetear a valores por defecto
   ```

3. **Casos de uso requeridos:**
   - `GetUserPreferencesUseCase`
   - `UpdateUserPreferencesUseCase`
   - `ResetUserPreferencesUseCase`

**Criterios de evaluación:**

- Implementación completa de todas las capas
- Seguimiento de patrones establecidos
- Validaciones apropiadas
- Manejo de errores
- Tests unitarios (mínimo 80% coverage)

#### **2.2 Implementar Nueva Funcionalidad en EvalinService (25 puntos)**

**Funcionalidad a implementar:** **Sistema de Comentarios en Evaluaciones**

**Requerimientos:**

1. **Entidad Domain:** `EvaluationComment`

   ```python
   # Campos requeridos:
   - comment_id: UUID
   - evaluation_id: UUID
   - user_id: UUID (quien comenta)
   - comment_text: str
   - is_private: bool (solo visible para admin/coordinador)
   - created_at: datetime
   - updated_at: datetime
   ```

2. **Endpoints a implementar:**

   ```python
   POST /api/v1/evaluations/{evaluation_id}/comments    # Agregar comentario
   GET /api/v1/evaluations/{evaluation_id}/comments     # Listar comentarios
   PUT /api/v1/evaluations/comments/{comment_id}        # Editar comentario
   DELETE /api/v1/evaluations/comments/{comment_id}     # Eliminar comentario
   ```

3. **Reglas de negocio:**
   - Solo el autor puede editar/eliminar sus comentarios
   - Comentarios privados solo visibles para admin/coordinador
   - No se pueden agregar comentarios a evaluaciones cerradas

**Criterios de evaluación:**

- Correcta implementación de reglas de negocio
- Integración con sistema de permisos existente
- Validaciones de seguridad
- Tests de integración

---

### **PARTE 3: INTEGRACIÓN Y COMUNICACIÓN ENTRE SERVICIOS (20 puntos)**

#### **3.1 Implementar Comunicación entre Servicios (20 puntos)**

**Funcionalidad a implementar:** **Notificación automática cuando se completa una evaluación**

**Requerimiento:**
Cuando un estudiante complete una evaluación en EvalinService, debe enviarse una notificación al UserService para registrar la actividad del usuario.

**Implementación requerida:**

1. **En EvalinService:**

   ```python
   # Agregar notificación después de completar evaluación
   class NotifyUserActivityUseCase:
       async def execute(self, user_id: UUID, activity_data: dict):
           # Enviar datos a UserService
   ```

2. **En UserService:**

   ```python
   # Nuevo endpoint para recibir notificaciones de actividad
   POST /api/v1/users/activity-log

   # Entidad para almacenar actividades
   class UserActivity:
       - activity_id: UUID
       - user_id: UUID
       - service_source: str
       - activity_type: str
       - activity_data: dict
       - timestamp: datetime
   ```

**Criterios de evaluación:**

- Comunicación HTTP correcta entre servicios
- Manejo de errores de red
- Logging apropiado
- Tests de integración

---

### **PARTE 4: TESTING Y CALIDAD DE CÓDIGO (10 puntos)**

#### **4.1 Tests Unitarios y de Integración (10 puntos)**

**Requerimientos:**

1. **Tests unitarios** para todos los casos de uso implementados
2. **Tests de integración** para los endpoints implementados
3. **Coverage mínimo:** 85% en las nuevas funcionalidades
4. **Tests de errores:** Validar manejo de excepciones

**Herramientas a usar:**

- `pytest` para testing
- `pytest-cov` para coverage
- `httpx` para tests de API

**Ejemplo de estructura de tests:**

```python
tests/
├── unit/
│   ├── test_user_preferences_use_cases.py
│   └── test_evaluation_comment_use_cases.py
├── integration/
│   ├── test_user_preferences_api.py
│   └── test_evaluation_comments_api.py
└── test_service_communication.py
```

---

## 🚀 **EJERCICIOS PRÁCTICOS ADICIONALES**

### **Ejercicio 1: Optimización de Consultas (Bonus: 5 puntos)**

Identifica y optimiza 2 consultas SQL en los servicios que podrían mejorar su rendimiento. Documenta:

- Consulta original
- Problema identificado
- Solución propuesta
- Medición de mejora

### **Ejercicio 2: Documentación API (Bonus: 5 puntos)**

Mejora la documentación Swagger de los nuevos endpoints con:

- Ejemplos de request/response
- Códigos de error detallados
- Descripciones completas
- Tags y categorización

### **Ejercicio 3: Análisis de Seguridad (Bonus: 5 puntos)**

Realiza un análisis de seguridad de las nuevas funcionalidades:

- Validación de entrada
- Autorización apropiada
- Prevención de ataques comunes (SQL injection, XSS, etc.)
- Recomendaciones de mejora

---

## 📝 **ENTREGABLES Y CRONOGRAMA**

### **Cronograma Sugerido**

| Día         | Actividades                                 | Entregables            |
| ----------- | ------------------------------------------- | ---------------------- |
| **Día 1-2** | Análisis de arquitectura y casos de uso     | Documentos de análisis |
| **Día 3-4** | Implementación UserService (Preferencias)   | Código + Tests         |
| **Día 5-6** | Implementación EvalinService (Comentarios)  | Código + Tests         |
| **Día 7**   | Integración servicios + Documentación final | Proyecto completo      |

### **Formato de Entrega**

**Estructura del repositorio a entregar:**

```
apellido_nombre_evaluacion_vii/
├── README.md                          # Instrucciones de instalación y ejecución
├── docs/
│   ├── arquitectura_analisis.pdf      # Parte 1.1
│   ├── casos_uso_analisis.pdf         # Parte 1.2
│   └── reflexiones_aprendizaje.pdf    # Reflexión personal
├── userservice/
│   ├── app/domain/entities/user_preferences.py
│   ├── app/application/use_cases/preferences_use_cases.py
│   ├── app/infrastructure/repositories/preferences_repository.py
│   ├── app/presentation/routers/preferences_router.py
│   └── tests/
├── evalinservice/
│   ├── app/domain/entities/evaluation_comment.py
│   ├── app/application/use_cases/comment_use_cases.py
│   ├── app/infrastructure/repositories/comment_repository.py
│   ├── app/presentation/routers/comment_router.py
│   └── tests/
├── integration/
│   ├── service_communication.py
│   └── tests/test_integration.py
└── requirements.txt                   # Dependencias adicionales si las hay
```

---

## 🏆 **CRITERIOS DE EVALUACIÓN**

### **Rúbrica de Calificación**

| Aspecto              | Excelente (90-100%)                        | Bueno (80-89%)                             | Aceptable (70-79%)                           | Insuficiente (<70%)              |
| -------------------- | ------------------------------------------ | ------------------------------------------ | -------------------------------------------- | -------------------------------- |
| **Arquitectura**     | Comprende perfectamente Clean Architecture | Comprende conceptos principales            | Comprende parcialmente                       | No comprende la arquitectura     |
| **Implementación**   | Código profesional, patrones correctos     | Código funcional con pequeños errores      | Código funcional básico                      | Código no funcional o incompleto |
| **Testing**          | Tests completos, >90% coverage             | Tests adecuados, >80% coverage             | Tests básicos, >70% coverage                 | Tests insuficientes o ausentes   |
| **Buenas Prácticas** | Código limpio, documentado, estándares     | Código organizado, pocas inconsistencias   | Código funcional con algunas malas prácticas | Código desorganizado             |
| **Integración**      | Comunicación robusta entre servicios       | Comunicación funcional con errores menores | Comunicación básica                          | Comunicación no funcional        |

### **Distribución de Puntos**

- **Parte 1 (Análisis):** 20 puntos
- **Parte 2 (Implementación):** 50 puntos
- **Parte 3 (Integración):** 20 puntos
- **Parte 4 (Testing):** 10 puntos
- **Ejercicios Bonus:** Hasta 15 puntos adicionales

**Total:** 100 puntos + 15 bonus = 115 puntos máximo

---

## 💡 **RECURSOS Y BUENAS PRÁCTICAS**

### **Documentación de Referencia**

1. **Clean Architecture:** Revisar implementación en UserService
2. **FastAPI Docs:** https://fastapi.tiangolo.com/
3. **Pydantic:** Para validaciones y schemas
4. **SQLAlchemy:** Para modelos de base de datos
5. **Pytest:** Para testing

### **Buenas Prácticas a Seguir**

1. **Nomenclatura:** Seguir convenciones PEP 8
2. **Documentación:** Docstrings en funciones y clases
3. **Validaciones:** Usar Pydantic para validar entrada
4. **Errores:** Usar excepciones específicas del domain
5. **Logging:** Implementar logs informativos
6. **Seguridad:** Validar permisos y autenticación

### **Comandos Útiles**

```bash
# Ejecutar tests con coverage
pytest --cov=app --cov-report=html

# Formatear código
black .

# Linting
flake8 .

# Ejecutar servicios
uvicorn main:app --reload --port 8001
```

---

## 🎓 **REFLEXIÓN FINAL**

**Pregunta de reflexión (incluir en entrega):**

_"Después de trabajar con esta arquitectura y estos microservicios, reflexiona sobre las siguientes preguntas (máximo 1 página):_

1. _¿Qué ventajas y desventajas identificaste en la arquitectura Clean Architecture?_
2. _¿Cómo contribuye esta experiencia a tu formación como desarrollador backend?_
3. _¿Qué aspectos te resultaron más desafiantes y cómo los superaste?_
4. _¿Cómo aplicarías estos conocimientos en un proyecto real de la industria?"_

---

**¡Éxito en tu evaluación! Recuerda que este es un ejercicio de aprendizaje profesional que te preparará para la industria del desarrollo de software.**
