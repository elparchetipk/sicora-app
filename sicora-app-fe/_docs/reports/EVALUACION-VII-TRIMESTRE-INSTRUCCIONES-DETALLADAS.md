# 🎯 **EVALUACIÓN VII TRIMESTRE - INSTRUCCIONES PASO A PASO**

**Para:** Estudiantes de Análisis y Desarrollo de Software - VII Trimestre  
**Tiempo:** 7 días calendario  
**Modalidad:** Individual

---

## 📋 **QUÉ VAS A HACER EN ESTA EVALUACIÓN**

Vas a implementar **DOS nuevas funcionalidades** en el sistema SICORA-APP usando el stack FastAPI como base:

1. **📱 Sistema de Preferencias de Usuario** en UserService
2. **💬 Sistema de Comentarios en Evaluaciones** en EvalinService
3. **🔗 Comunicación entre los dos servicios**

**¿Por qué estas funcionalidades?** Porque son reales y te permitirán entender cómo funciona una arquitectura profesional de microservicios.

---

## 🛠️ **PREPARACIÓN INICIAL (30 minutos)**

### **Paso 1: Configurar tu Entorno**

```bash
# 1. Clonar el repositorio (si no lo tienes)
git clone [URL_DEL_REPOSITORIO]
cd sicora-app-be-multistack

# 2. Ir al directorio FastAPI
cd 01-fastapi

# 3. Crear entorno virtual
python3 -m venv venv_evaluacion
source venv_evaluacion/bin/activate

# 4. Instalar dependencias para ambos servicios
cd userservice
pip install -r requirements.txt
cd ../evalinservice
pip install -r requirements.txt
```

### **Paso 2: Verificar que Todo Funciona**

```bash
# Terminal 1 - UserService
cd userservice
uvicorn main:app --reload --port 8001

# Terminal 2 - EvalinService
cd evalinservice
uvicorn main:app --reload --port 8004

# Verificar en navegador:
# http://localhost:8001/docs (UserService)
# http://localhost:8004/docs (EvalinService)
```

**✅ Si ves la documentación Swagger, estás listo.**

---

## 📅 **PLAN DE TRABAJO DÍA A DÍA**

### **DÍA 1: ANÁLISIS Y COMPRENSIÓN**

#### **Tarea 1.1: Analizar la Arquitectura (2 horas)**

**QUÉ HACER:**

1. Abrir ambos servicios (userservice y evalinservice)
2. Revisar la estructura de carpetas
3. Crear un documento que explique:

```
📁 userservice/app/
├── 📁 domain/          ← ¿Qué hay aquí? ¿Para qué sirve?
├── 📁 application/     ← ¿Qué tipos de archivos hay?
├── 📁 infrastructure/ ← ¿Cómo se conecta a la BD?
└── 📁 presentation/   ← ¿Dónde están las APIs?
```

**ENTREGABLE:**

- Archivo: `docs/analisis_arquitectura.md`
- Contenido: Explicar qué hace cada capa con ejemplos específicos del código

#### **Tarea 1.2: Estudiar 3 Casos de Uso (2 horas)**

**QUÉ HACER:**

1. Ir a `userservice/app/application/use_cases/`
2. Elegir 3 archivos diferentes (ej: `create_user_use_case.py`)
3. Para cada uno, responder:
   - ¿Qué hace este caso de uso?
   - ¿Qué recibe como entrada?
   - ¿Qué devuelve?
   - ¿Con qué repositorios se conecta?

**ENTREGABLE:**

- Archivo: `docs/analisis_casos_uso.md`

---

### **DÍA 2-3: SISTEMA DE PREFERENCIAS DE USUARIO**

#### **Lo que vas a crear:**

Un sistema donde cada usuario pueda configurar:

- Idioma (español/inglés)
- Tema visual (claro/oscuro)
- Notificaciones (email/push)
- Zona horaria

#### **Paso 2.1: Crear la Entidad (45 minutos)**

**ARCHIVO A CREAR:** `userservice/app/domain/entities/user_preferences.py`

**QUÉ ESCRIBIR:**

```python
from datetime import datetime
from typing import Optional
from uuid import UUID
import uuid

class UserPreferences:
    def __init__(
        self,
        user_id: UUID,
        language: str = "es",           # "es" o "en"
        theme: str = "light",           # "light", "dark", "auto"
        notifications_email: bool = True,
        notifications_push: bool = True,
        timezone: str = "America/Bogota",
        preferences_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        # TU CÓDIGO AQUÍ: Asignar todas las variables
        # TU CÓDIGO AQUÍ: Llamar self._validate()

    def _validate(self):
        # TU CÓDIGO AQUÍ: Validar que language sea "es" o "en"
        # TU CÓDIGO AQUÍ: Validar que theme sea "light", "dark" o "auto"
        pass

    def update_language(self, language: str):
        # TU CÓDIGO AQUÍ: Cambiar idioma y actualizar timestamp
        pass

    def reset_to_defaults(self):
        # TU CÓDIGO AQUÍ: Volver a valores por defecto
        pass
```

**✅ CHECKPOINT:** La entidad debe poder crearse sin errores.

#### **Paso 2.2: Crear el Repository Interface (30 minutos)**

**ARCHIVO A CREAR:** `userservice/app/domain/repositories/user_preferences_repository.py`

**QUÉ ESCRIBIR:**

```python
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain.entities.user_preferences import UserPreferences

class UserPreferencesRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, preferences: UserPreferences) -> UserPreferences:
        """Crear nuevas preferencias."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[UserPreferences]:
        """Buscar preferencias por ID de usuario."""
        pass

    # TU CÓDIGO AQUÍ: Agregar métodos update y delete
```

#### **Paso 2.3: Crear el Caso de Uso (45 minutos)**

**ARCHIVO A CREAR:** `userservice/app/application/use_cases/get_user_preferences_use_case.py`

**QUÉ ESCRIBIR:**

```python
from uuid import UUID
from app.domain.entities.user_preferences import UserPreferences
from app.domain.repositories.user_preferences_repository import UserPreferencesRepositoryInterface

class GetUserPreferencesUseCase:
    def __init__(self, preferences_repository: UserPreferencesRepositoryInterface):
        # TU CÓDIGO AQUÍ: Guardar el repositorio
        pass

    async def execute(self, user_id: UUID) -> UserPreferences:
        # TU CÓDIGO AQUÍ:
        # 1. Buscar preferencias existentes
        # 2. Si no existen, crear con valores por defecto
        # 3. Devolver las preferencias
        pass
```

#### **Paso 2.4: Crear el Modelo de Base de Datos (30 minutos)**

**ARCHIVO A CREAR:** `userservice/app/infrastructure/database/models/user_preferences_model.py`

**QUÉ ESCRIBIR:**

```python
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infrastructure.database.base import Base

class UserPreferencesModel(Base):
    __tablename__ = "user_preferences"

    preferences_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    # TU CÓDIGO AQUÍ: Agregar resto de columnas
```

#### **Paso 2.5: Implementar el Repository (45 minutos)**

**ARCHIVO A CREAR:** `userservice/app/infrastructure/repositories/user_preferences_repository_impl.py`

**PLANTILLA:**

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repositories.user_preferences_repository import UserPreferencesRepositoryInterface
from app.infrastructure.database.models.user_preferences_model import UserPreferencesModel

class UserPreferencesRepositoryImpl(UserPreferencesRepositoryInterface):
    def __init__(self, db: AsyncSession):
        # TU CÓDIGO AQUÍ
        pass

    async def create(self, preferences):
        # TU CÓDIGO AQUÍ: Convertir entidad a modelo y guardar en BD
        pass

    async def get_by_user_id(self, user_id):
        # TU CÓDIGO AQUÍ: Buscar en BD y convertir a entidad
        pass
```

#### **Paso 2.6: Crear los Endpoints (60 minutos)**

**ARCHIVO A CREAR:** `userservice/app/presentation/routers/preferences_router.py`

**QUÉ CREAR:**

```python
from fastapi import APIRouter, Depends
from app.presentation.schemas.user_preferences_schemas import UserPreferencesResponse

router = APIRouter(prefix="/preferences", tags=["User Preferences"])

@router.get("/", response_model=UserPreferencesResponse)
async def get_user_preferences():
    # TU CÓDIGO AQUÍ: Obtener preferencias del usuario autenticado
    pass

@router.put("/", response_model=UserPreferencesResponse)
async def update_user_preferences():
    # TU CÓDIGO AQUÍ: Actualizar preferencias
    pass

@router.post("/reset")
async def reset_preferences():
    # TU CÓDIGO AQUÍ: Resetear a valores por defecto
    pass
```

**✅ CHECKPOINT:** Los 3 endpoints deben aparecer en http://localhost:8001/docs

---

### **DÍA 4-5: SISTEMA DE COMENTARIOS EN EVALUACIONES**

#### **Lo que vas a crear:**

Un sistema donde los usuarios puedan:

- Agregar comentarios a evaluaciones
- Ver comentarios de evaluaciones
- Editar sus propios comentarios
- Marcar comentarios como privados (solo admin)

#### **Pasos Similares:**

1. **Entidad:** `EvaluationComment` en `evalinservice/app/domain/entities/`
2. **Repository Interface:** En `evalinservice/app/domain/repositories/`
3. **Casos de Uso:** Create, Get, Update, Delete
4. **Modelo BD:** En `evalinservice/app/infrastructure/database/models/`
5. **Repository Impl:** En `evalinservice/app/infrastructure/repositories/`
6. **Endpoints:** En `evalinservice/app/presentation/routers/`

**PLANTILLA DE LA ENTIDAD:**

```python
class EvaluationComment:
    def __init__(
        self,
        evaluation_id: UUID,
        user_id: UUID,
        comment_text: str,
        is_private: bool = False,
        # más campos...
    ):
        # TU CÓDIGO AQUÍ: Validar que comment_text tenga al menos 5 caracteres
        # TU CÓDIGO AQUÍ: Validar que no supere 1000 caracteres
        pass

    def can_be_edited_by(self, user_id: UUID) -> bool:
        # TU CÓDIGO AQUÍ: Solo el autor puede editar
        pass
```

**ENDPOINTS A CREAR:**

```
POST /api/v1/evaluations/{evaluation_id}/comments    # Agregar comentario
GET  /api/v1/evaluations/{evaluation_id}/comments    # Listar comentarios
PUT  /api/v1/evaluations/comments/{comment_id}       # Editar comentario
DELETE /api/v1/evaluations/comments/{comment_id}     # Eliminar comentario
```

---

### **DÍA 6: COMUNICACIÓN ENTRE SERVICIOS**

#### **Lo que vas a crear:**

Cuando se complete una evaluación en EvalinService, automáticamente se debe notificar al UserService para registrar la actividad.

#### **Paso 6.1: Cliente HTTP en EvalinService (45 minutos)**

**ARCHIVO A CREAR:** `evalinservice/app/infrastructure/external_services/user_service_client.py`

```python
import httpx
from uuid import UUID

class UserServiceClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url

    async def notify_user_activity(self, user_id: UUID, activity_data: dict) -> bool:
        # TU CÓDIGO AQUÍ: Hacer POST a UserService
        # URL: {base_url}/api/v1/users/activity-log
        # Payload: user_id, service_source, activity_type, activity_data
        pass
```

#### **Paso 6.2: Endpoint Receptor en UserService (30 minutos)**

**AGREGAR A:** `userservice/app/presentation/routers/users_router.py`

```python
@router.post("/activity-log")
async def log_user_activity():
    # TU CÓDIGO AQUÍ: Recibir datos de actividad y guardarlos
    pass
```

#### **Paso 6.3: Entidad UserActivity (30 minutos)**

**ARCHIVO A CREAR:** `userservice/app/domain/entities/user_activity.py`

```python
class UserActivity:
    def __init__(
        self,
        user_id: UUID,
        service_source: str,        # "evalinservice"
        activity_type: str,         # "evaluation_completed"
        activity_data: dict,        # datos adicionales
        # más campos...
    ):
        # TU CÓDIGO AQUÍ
        pass
```

---

### **DÍA 7: TESTING Y DOCUMENTACIÓN**

#### **Tests que DEBES crear:**

1. **Test de la Entidad UserPreferences:**

```python
# tests/unit/test_user_preferences.py
def test_create_preferences_with_defaults():
    user_id = uuid4()
    prefs = UserPreferences(user_id=user_id)
    assert prefs.language == "es"
    assert prefs.theme == "light"

def test_invalid_language_raises_error():
    # TU CÓDIGO AQUÍ: Verificar que "invalid" lance excepción
    pass
```

2. **Test del Endpoint GET /preferences:**

```python
# tests/integration/test_preferences_api.py
async def test_get_preferences_returns_defaults():
    # TU CÓDIGO AQUÍ: Hacer GET y verificar respuesta
    pass
```

#### **Documentación a crear:**

1. **README.md** con:
   - Cómo instalar
   - Cómo ejecutar
   - Cómo probar

2. **docs/reflexion_personal.md** respondiendo:
   - ¿Qué aprendiste de Clean Architecture?
   - ¿Qué fue lo más difícil?
   - ¿Cómo aplicarías esto en un trabajo real?

---

## 📦 **ESTRUCTURA FINAL DE ENTREGA**

```
apellido_nombre_evaluacion/
├── README.md                     ← Instrucciones para ejecutar tu código
├── docs/
│   ├── analisis_arquitectura.md  ← Tu análisis de las capas
│   ├── analisis_casos_uso.md     ← Tu análisis de 3 casos de uso
│   └── reflexion_personal.md     ← Tu reflexión sobre el aprendizaje
├── userservice/
│   ├── app/domain/entities/user_preferences.py
│   ├── app/domain/entities/user_activity.py
│   ├── app/application/use_cases/get_user_preferences_use_case.py
│   ├── app/application/use_cases/update_user_preferences_use_case.py
│   ├── app/infrastructure/repositories/user_preferences_repository_impl.py
│   ├── app/presentation/routers/preferences_router.py
│   └── tests/
├── evalinservice/
│   ├── app/domain/entities/evaluation_comment.py
│   ├── app/application/use_cases/create_comment_use_case.py
│   ├── app/infrastructure/external_services/user_service_client.py
│   ├── app/presentation/routers/comment_router.py
│   └── tests/
└── requirements.txt              ← Si agregaste nuevas dependencias
```

---

## ✅ **CHECKLIST DE VERIFICACIÓN ANTES DE ENTREGAR**

### **Funcionalidad UserService:**

- [ ] Puedo crear preferencias: `POST /api/v1/users/preferences`
- [ ] Puedo obtener preferencias: `GET /api/v1/users/preferences`
- [ ] Puedo actualizar preferencias: `PUT /api/v1/users/preferences`
- [ ] Puedo resetear preferencias: `POST /api/v1/users/preferences/reset`

### **Funcionalidad EvalinService:**

- [ ] Puedo agregar comentario: `POST /api/v1/evaluations/{id}/comments`
- [ ] Puedo ver comentarios: `GET /api/v1/evaluations/{id}/comments`
- [ ] Puedo editar mi comentario: `PUT /api/v1/evaluations/comments/{id}`
- [ ] Puedo eliminar mi comentario: `DELETE /api/v1/evaluations/comments/{id}`

### **Comunicación entre Servicios:**

- [ ] Al completar evaluación se notifica a UserService
- [ ] UserService recibe y guarda la actividad

### **Testing:**

- [ ] Al menos 5 tests unitarios ejecutan sin errores
- [ ] Al menos 3 tests de integración funcionan
- [ ] Coverage > 70%

### **Documentación:**

- [ ] README explica cómo ejecutar el código
- [ ] Análisis de arquitectura completado
- [ ] Reflexión personal incluida

---

## 🆘 **¿TIENES DUDAS? AQUÍ TIENES AYUDA**

### **Comandos Útiles:**

```bash
# Ejecutar tests
pytest tests/ -v

# Ver coverage
pytest --cov=app --cov-report=html

# Verificar que tu código funciona
curl http://localhost:8001/api/v1/users/preferences

# Ver logs de errores
uvicorn main:app --reload --log-level debug
```

### **Errores Comunes:**

1. **"Module not found"** → Verificar PYTHONPATH y imports
2. **"Table doesn't exist"** → Crear migración de BD
3. **"401 Unauthorized"** → Verificar autenticación en headers
4. **"422 Validation Error"** → Verificar esquemas Pydantic

### **Dónde Buscar Ejemplos:**

- **Entidades:** Revisar `userservice/app/domain/entities/user.py`
- **Casos de Uso:** Revisar `userservice/app/application/use_cases/`
- **Endpoints:** Revisar `userservice/app/presentation/routers/`
- **Tests:** Revisar carpeta `tests/` existente

---

## 🎯 **CRITERIOS DE ÉXITO SIMPLES**

**Pregúntate:**

1. ¿Mi código se ejecuta sin errores?
2. ¿Los endpoints aparecen en la documentación Swagger?
3. ¿Puedo hacer requests y recibir respuestas correctas?
4. ¿Mis tests pasan?
5. ¿Entendí cómo funciona la arquitectura?

**Si respondes SÍ a todo, vas por buen camino.**

---

**¡Ahora sí tienes claro QUÉ hacer cada día! Recuerda: es mejor entregar algo funcional y sencillo que algo complejo que no funciona.**
