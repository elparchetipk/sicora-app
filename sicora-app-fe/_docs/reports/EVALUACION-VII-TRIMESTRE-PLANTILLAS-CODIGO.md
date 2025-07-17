# 💻 **PLANTILLAS DE CÓDIGO - EVALUACIÓN VII TRIMESTRE**

**Para:** Estudiantes que necesitan ejemplos específicos de código  
**Propósito:** Plantillas listas para completar y adaptar

---

## 🏗️ **PLANTILLA 1: ENTIDAD USER PREFERENCES**

### **Archivo:** `userservice/app/domain/entities/user_preferences.py`

```python
from datetime import datetime
from typing import Optional
from uuid import UUID
import uuid

class UserPreferences:
    """Entidad de preferencias de usuario."""

    def __init__(
        self,
        user_id: UUID,
        language: str = "es",
        theme: str = "light",
        notifications_email: bool = True,
        notifications_push: bool = True,
        timezone: str = "America/Bogota",
        preferences_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.preferences_id = preferences_id or uuid.uuid4()
        self.user_id = user_id
        self.language = language
        self.theme = theme
        self.notifications_email = notifications_email
        self.notifications_push = notifications_push
        self.timezone = timezone
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

        # ✅ TODO: Llama a la validación
        self._validate()

    def _validate(self):
        """Validar datos de dominio."""
        valid_languages = ["es", "en"]
        valid_themes = ["light", "dark", "auto"]

        # ✅ TODO: Completa estas validaciones
        if self.language not in valid_languages:
            raise ValueError(f"Language must be one of: {valid_languages}")

        if self.theme not in valid_themes:
            raise ValueError(f"Theme must be one of: {valid_themes}")

    def update_language(self, language: str):
        """Actualizar idioma."""
        # ✅ TODO: Actualiza self.language y self.updated_at
        self.language = language
        self.updated_at = datetime.utcnow()
        self._validate()

    def update_theme(self, theme: str):
        """Actualizar tema."""
        # ✅ TODO: Implementa similar a update_language
        pass

    def update_notifications(self, email: bool, push: bool):
        """Actualizar preferencias de notificaciones."""
        # ✅ TODO: Actualiza ambas notificaciones y timestamp
        pass

    def reset_to_defaults(self):
        """Resetear a valores por defecto."""
        # ✅ TODO: Vuelve todos los valores a sus defaults
        self.language = "es"
        self.theme = "light"
        # ... completa el resto
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Convertir a diccionario para respuestas API."""
        return {
            "preferences_id": str(self.preferences_id),
            "user_id": str(self.user_id),
            "language": self.language,
            "theme": self.theme,
            "notifications_email": self.notifications_email,
            "notifications_push": self.notifications_push,
            "timezone": self.timezone,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
```

---

## 🏗️ **PLANTILLA 2: REPOSITORY INTERFACE**

### **Archivo:** `userservice/app/domain/repositories/user_preferences_repository.py`

```python
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.user_preferences import UserPreferences

class UserPreferencesRepositoryInterface(ABC):
    """Interface para repositorio de preferencias de usuario."""

    @abstractmethod
    async def create(self, preferences: UserPreferences) -> UserPreferences:
        """Crear nuevas preferencias en la base de datos."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[UserPreferences]:
        """Obtener preferencias por ID de usuario."""
        pass

    @abstractmethod
    async def update(self, preferences: UserPreferences) -> UserPreferences:
        """Actualizar preferencias existentes."""
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: UUID) -> bool:
        """Eliminar preferencias por ID de usuario."""
        pass
```

---

## 🏗️ **PLANTILLA 3: CASO DE USO**

### **Archivo:** `userservice/app/application/use_cases/get_user_preferences_use_case.py`

```python
from uuid import UUID
from typing import Optional

from app.domain.entities.user_preferences import UserPreferences
from app.domain.repositories.user_preferences_repository import UserPreferencesRepositoryInterface

class GetUserPreferencesUseCase:
    """Caso de uso para obtener preferencias de usuario."""

    def __init__(self, preferences_repository: UserPreferencesRepositoryInterface):
        self.preferences_repository = preferences_repository

    async def execute(self, user_id: UUID) -> UserPreferences:
        """Ejecutar caso de uso."""

        # ✅ TODO: Buscar preferencias existentes
        preferences = await self.preferences_repository.get_by_user_id(user_id)

        # ✅ TODO: Si no existen, crear preferencias por defecto
        if not preferences:
            preferences = UserPreferences(user_id=user_id)
            preferences = await self.preferences_repository.create(preferences)

        return preferences
```

### **Archivo:** `userservice/app/application/use_cases/update_user_preferences_use_case.py`

```python
from uuid import UUID
from typing import Optional

from app.domain.entities.user_preferences import UserPreferences
from app.domain.repositories.user_preferences_repository import UserPreferencesRepositoryInterface
from app.domain.exceptions.user_exceptions import UserPreferencesNotFoundError

class UpdateUserPreferencesUseCase:
    """Caso de uso para actualizar preferencias."""

    def __init__(self, preferences_repository: UserPreferencesRepositoryInterface):
        self.preferences_repository = preferences_repository

    async def execute(
        self,
        user_id: UUID,
        language: Optional[str] = None,
        theme: Optional[str] = None,
        notifications_email: Optional[bool] = None,
        notifications_push: Optional[bool] = None,
        timezone: Optional[str] = None
    ) -> UserPreferences:
        """Actualizar preferencias de usuario."""

        # ✅ TODO: Obtener preferencias existentes
        preferences = await self.preferences_repository.get_by_user_id(user_id)
        if not preferences:
            raise UserPreferencesNotFoundError(f"Preferences for user {user_id} not found")

        # ✅ TODO: Actualizar solo los campos que se proporcionaron
        if language is not None:
            preferences.update_language(language)

        if theme is not None:
            preferences.update_theme(theme)

        # ✅ TODO: Completa para notifications y timezone

        # ✅ TODO: Guardar cambios
        return await self.preferences_repository.update(preferences)
```

---

## 🏗️ **PLANTILLA 4: MODELO SQLALCHEMY**

### **Archivo:** `userservice/app/infrastructure/database/models/user_preferences_model.py`

```python
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.infrastructure.database.base import Base

class UserPreferencesModel(Base):
    """Modelo de base de datos para preferencias de usuario."""

    __tablename__ = "user_preferences"

    preferences_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, unique=True)
    language = Column(String(2), nullable=False, default="es")
    theme = Column(String(10), nullable=False, default="light")
    notifications_email = Column(Boolean, nullable=False, default=True)
    notifications_push = Column(Boolean, nullable=False, default=True)
    timezone = Column(String(50), nullable=False, default="America/Bogota")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_entity(self):
        """Convertir modelo a entidad de dominio."""
        from app.domain.entities.user_preferences import UserPreferences

        return UserPreferences(
            preferences_id=self.preferences_id,
            user_id=self.user_id,
            language=self.language,
            theme=self.theme,
            notifications_email=self.notifications_email,
            notifications_push=self.notifications_push,
            timezone=self.timezone,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_entity(cls, preferences):
        """Crear modelo desde entidad de dominio."""
        return cls(
            preferences_id=preferences.preferences_id,
            user_id=preferences.user_id,
            language=preferences.language,
            theme=preferences.theme,
            notifications_email=preferences.notifications_email,
            notifications_push=preferences.notifications_push,
            timezone=preferences.timezone,
            created_at=preferences.created_at,
            updated_at=preferences.updated_at
        )
```

---

## 🏗️ **PLANTILLA 5: REPOSITORY IMPLEMENTATION**

### **Archivo:** `userservice/app/infrastructure/repositories/user_preferences_repository_impl.py`

```python
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.user_preferences import UserPreferences
from app.domain.repositories.user_preferences_repository import UserPreferencesRepositoryInterface
from app.infrastructure.database.models.user_preferences_model import UserPreferencesModel

class UserPreferencesRepositoryImpl(UserPreferencesRepositoryInterface):
    """Implementación del repositorio de preferencias."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, preferences: UserPreferences) -> UserPreferences:
        """Crear nuevas preferencias."""
        # ✅ TODO: Convertir entidad a modelo
        model = UserPreferencesModel.from_entity(preferences)

        # ✅ TODO: Agregar a la sesión y hacer commit
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)

        # ✅ TODO: Convertir modelo de vuelta a entidad
        return model.to_entity()

    async def get_by_user_id(self, user_id: UUID) -> Optional[UserPreferences]:
        """Obtener preferencias por ID de usuario."""
        # ✅ TODO: Hacer query para buscar por user_id
        query = select(UserPreferencesModel).where(UserPreferencesModel.user_id == user_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()

        # ✅ TODO: Convertir a entidad si existe
        if model:
            return model.to_entity()
        return None

    async def update(self, preferences: UserPreferences) -> UserPreferences:
        """Actualizar preferencias."""
        # ✅ TODO: Buscar modelo existente
        query = select(UserPreferencesModel).where(
            UserPreferencesModel.user_id == preferences.user_id
        )
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            raise ValueError("Preferences not found")

        # ✅ TODO: Actualizar campos del modelo
        model.language = preferences.language
        model.theme = preferences.theme
        model.notifications_email = preferences.notifications_email
        model.notifications_push = preferences.notifications_push
        model.timezone = preferences.timezone
        model.updated_at = preferences.updated_at

        # ✅ TODO: Guardar cambios
        await self.db.commit()
        await self.db.refresh(model)

        return model.to_entity()

    async def delete_by_user_id(self, user_id: UUID) -> bool:
        """Eliminar preferencias por ID de usuario."""
        # ✅ TODO: Implementa la eliminación
        pass
```

---

## 🏗️ **PLANTILLA 6: SCHEMAS PYDANTIC**

### **Archivo:** `userservice/app/presentation/schemas/user_preferences_schemas.py`

```python
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class UpdateUserPreferencesRequest(BaseModel):
    """Schema para actualizar preferencias."""
    language: Optional[str] = Field(None, pattern="^(es|en)$", description="Idioma del usuario")
    theme: Optional[str] = Field(None, pattern="^(light|dark|auto)$", description="Tema visual")
    notifications_email: Optional[bool] = Field(None, description="Recibir notificaciones por email")
    notifications_push: Optional[bool] = Field(None, description="Recibir notificaciones push")
    timezone: Optional[str] = Field(None, max_length=50, description="Zona horaria")

class UserPreferencesResponse(BaseModel):
    """Schema para respuesta de preferencias."""
    preferences_id: UUID
    user_id: UUID
    language: str
    theme: str
    notifications_email: bool
    notifications_push: bool
    timezone: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, preferences):
        """Crear desde entidad de dominio."""
        return cls(
            preferences_id=preferences.preferences_id,
            user_id=preferences.user_id,
            language=preferences.language,
            theme=preferences.theme,
            notifications_email=preferences.notifications_email,
            notifications_push=preferences.notifications_push,
            timezone=preferences.timezone,
            created_at=preferences.created_at,
            updated_at=preferences.updated_at
        )

    class Config:
        from_attributes = True
```

---

## 🏗️ **PLANTILLA 7: ROUTER (ENDPOINTS)**

### **Archivo:** `userservice/app/presentation/routers/preferences_router.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.application.use_cases.get_user_preferences_use_case import GetUserPreferencesUseCase
from app.application.use_cases.update_user_preferences_use_case import UpdateUserPreferencesUseCase
from app.presentation.schemas.user_preferences_schemas import (
    UserPreferencesResponse,
    UpdateUserPreferencesRequest
)
from app.dependencies import get_current_user
from app.presentation.schemas.user_schemas import UserSchema

router = APIRouter(prefix="/preferences", tags=["User Preferences"])

@router.get("/", response_model=UserPreferencesResponse)
async def get_user_preferences(
    current_user: UserSchema = Depends(get_current_user),
    get_preferences_uc: GetUserPreferencesUseCase = Depends()
):
    """Obtener preferencias del usuario autenticado."""
    try:
        # ✅ TODO: Ejecutar caso de uso
        preferences = await get_preferences_uc.execute(current_user.user_id)

        # ✅ TODO: Convertir a schema de respuesta
        return UserPreferencesResponse.from_entity(preferences)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving preferences: {str(e)}"
        )

@router.put("/", response_model=UserPreferencesResponse)
async def update_user_preferences(
    request: UpdateUserPreferencesRequest,
    current_user: UserSchema = Depends(get_current_user),
    update_preferences_uc: UpdateUserPreferencesUseCase = Depends()
):
    """Actualizar preferencias del usuario."""
    try:
        # ✅ TODO: Ejecutar caso de uso con datos del request
        preferences = await update_preferences_uc.execute(
            user_id=current_user.user_id,
            language=request.language,
            theme=request.theme,
            notifications_email=request.notifications_email,
            notifications_push=request.notifications_push,
            timezone=request.timezone
        )

        return UserPreferencesResponse.from_entity(preferences)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating preferences: {str(e)}"
        )

@router.post("/reset")
async def reset_preferences(
    current_user: UserSchema = Depends(get_current_user),
    # ✅ TODO: Agregar dependencia para caso de uso de reset
):
    """Resetear preferencias a valores por defecto."""
    try:
        # ✅ TODO: Implementar reset de preferencias
        pass
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error resetting preferences: {str(e)}"
        )
```

---

## 🏗️ **PLANTILLA 8: DEPENDENCY INJECTION**

### **Archivo:** Agregar a `userservice/app/dependencies.py`

```python
# ✅ TODO: Agregar estas dependencias al archivo existente

from app.application.use_cases.get_user_preferences_use_case import GetUserPreferencesUseCase
from app.application.use_cases.update_user_preferences_use_case import UpdateUserPreferencesUseCase
from app.infrastructure.repositories.user_preferences_repository_impl import UserPreferencesRepositoryImpl

async def get_user_preferences_use_case(
    db: AsyncSession = Depends(get_db_session)
) -> GetUserPreferencesUseCase:
    """Crear instancia del caso de uso."""
    repository = UserPreferencesRepositoryImpl(db)
    return GetUserPreferencesUseCase(repository)

async def get_update_user_preferences_use_case(
    db: AsyncSession = Depends(get_db_session)
) -> UpdateUserPreferencesUseCase:
    """Crear instancia del caso de uso."""
    repository = UserPreferencesRepositoryImpl(db)
    return UpdateUserPreferencesUseCase(repository)
```

---

## 🏗️ **PLANTILLA 9: TESTS UNITARIOS**

### **Archivo:** `userservice/tests/unit/test_user_preferences.py`

```python
import pytest
from uuid import uuid4
from datetime import datetime

from app.domain.entities.user_preferences import UserPreferences

class TestUserPreferences:

    def test_create_preferences_with_defaults(self):
        """Test crear preferencias con valores por defecto."""
        user_id = uuid4()
        prefs = UserPreferences(user_id=user_id)

        # ✅ TODO: Verificar valores por defecto
        assert prefs.user_id == user_id
        assert prefs.language == "es"
        assert prefs.theme == "light"
        assert prefs.notifications_email is True
        assert prefs.notifications_push is True
        assert prefs.timezone == "America/Bogota"

    def test_create_preferences_with_custom_values(self):
        """Test crear preferencias con valores personalizados."""
        user_id = uuid4()
        prefs = UserPreferences(
            user_id=user_id,
            language="en",
            theme="dark",
            notifications_email=False
        )

        # ✅ TODO: Verificar valores personalizados
        assert prefs.language == "en"
        assert prefs.theme == "dark"
        assert prefs.notifications_email is False

    def test_invalid_language_raises_error(self):
        """Test idioma inválido lanza excepción."""
        user_id = uuid4()

        # ✅ TODO: Verificar que "invalid" lance ValueError
        with pytest.raises(ValueError, match="Language must be one of"):
            UserPreferences(user_id=user_id, language="invalid")

    def test_invalid_theme_raises_error(self):
        """Test tema inválido lanza excepción."""
        # ✅ TODO: Implementa similar al test anterior
        pass

    def test_update_language(self):
        """Test actualización de idioma."""
        user_id = uuid4()
        prefs = UserPreferences(user_id=user_id)

        old_updated_at = prefs.updated_at

        # ✅ TODO: Actualizar idioma y verificar cambios
        prefs.update_language("en")

        assert prefs.language == "en"
        assert prefs.updated_at > old_updated_at

    def test_reset_to_defaults(self):
        """Test reset a valores por defecto."""
        user_id = uuid4()
        prefs = UserPreferences(
            user_id=user_id,
            language="en",
            theme="dark",
            notifications_email=False
        )

        # ✅ TODO: Hacer reset y verificar valores por defecto
        prefs.reset_to_defaults()

        assert prefs.language == "es"
        assert prefs.theme == "light"
        assert prefs.notifications_email is True

    def test_to_dict_contains_all_fields(self):
        """Test conversión a diccionario."""
        user_id = uuid4()
        prefs = UserPreferences(user_id=user_id)

        # ✅ TODO: Convertir a dict y verificar campos
        data = prefs.to_dict()

        assert "preferences_id" in data
        assert "user_id" in data
        assert "language" in data
        # ... verifica todos los campos
```

---

## 🏗️ **PLANTILLA 10: TESTS DE INTEGRACIÓN**

### **Archivo:** `userservice/tests/integration/test_preferences_api.py`

```python
import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_get_preferences_creates_defaults(
    client: AsyncClient,
    authenticated_user_headers
):
    """Test obtener preferencias crea por defecto si no existen."""

    # ✅ TODO: Hacer GET request
    response = await client.get(
        "/api/v1/users/preferences",
        headers=authenticated_user_headers
    )

    # ✅ TODO: Verificar respuesta
    assert response.status_code == 200
    data = response.json()

    assert data["language"] == "es"
    assert data["theme"] == "light"
    assert data["notifications_email"] is True

@pytest.mark.asyncio
async def test_update_preferences_valid_data(
    client: AsyncClient,
    authenticated_user_headers
):
    """Test actualizar preferencias con datos válidos."""

    update_data = {
        "language": "en",
        "theme": "dark",
        "notifications_email": False,
        "notifications_push": True,
        "timezone": "UTC"
    }

    # ✅ TODO: Hacer PUT request
    response = await client.put(
        "/api/v1/users/preferences",
        json=update_data,
        headers=authenticated_user_headers
    )

    # ✅ TODO: Verificar respuesta
    assert response.status_code == 200
    data = response.json()

    assert data["language"] == "en"
    assert data["theme"] == "dark"
    assert data["notifications_email"] is False

@pytest.mark.asyncio
async def test_update_preferences_invalid_language(
    client: AsyncClient,
    authenticated_user_headers
):
    """Test actualizar con idioma inválido retorna 400."""

    update_data = {"language": "invalid"}

    # ✅ TODO: Hacer PUT request con dato inválido
    response = await client.put(
        "/api/v1/users/preferences",
        json=update_data,
        headers=authenticated_user_headers
    )

    # ✅ TODO: Verificar error 400
    assert response.status_code == 400
    assert "Language must be one of" in response.json()["detail"]

@pytest.mark.asyncio
async def test_reset_preferences(
    client: AsyncClient,
    authenticated_user_headers
):
    """Test reset de preferencias."""

    # ✅ TODO: Primero actualizar preferencias
    await client.put(
        "/api/v1/users/preferences",
        json={"language": "en", "theme": "dark"},
        headers=authenticated_user_headers
    )

    # ✅ TODO: Hacer reset
    response = await client.post(
        "/api/v1/users/preferences/reset",
        headers=authenticated_user_headers
    )

    # ✅ TODO: Verificar que volvieron a defaults
    assert response.status_code == 200

    # Verificar que efectivamente se resetearon
    get_response = await client.get(
        "/api/v1/users/preferences",
        headers=authenticated_user_headers
    )
    data = get_response.json()
    assert data["language"] == "es"
    assert data["theme"] == "light"
```

---

## 📝 **INSTRUCCIONES DE USO DE PLANTILLAS**

### **Cómo usar estas plantillas:**

1. **Copia el código** de cada plantilla
2. **Busca los comentarios `✅ TODO:`** - esas son las partes que debes completar
3. **Reemplaza los TODO** con tu código
4. **Ejecuta tests** para verificar que funciona

### **Orden recomendado de implementación:**

1. Entidad (`UserPreferences`)
2. Repository Interface
3. Casos de Uso básicos
4. Modelo SQLAlchemy
5. Repository Implementation
6. Schemas Pydantic
7. Router (Endpoints)
8. Tests

### **Comandos para verificar:**

```bash
# Verificar sintaxis
python -m py_compile app/domain/entities/user_preferences.py

# Ejecutar tests específicos
pytest tests/unit/test_user_preferences.py -v

# Verificar endpoint en Swagger
# http://localhost:8001/docs
```

### **¿Necesitas ayuda con alguna plantilla?**

- **Errores de import:** Revisa las rutas de los imports
- **Errores de validación:** Revisa los schemas Pydantic
- **Errores de BD:** Verifica que el modelo tenga todas las columnas
- **Tests fallan:** Ejecuta un test a la vez para identificar el problema

---

**Estas plantillas te dan la estructura base. ¡Ahora solo completa los TODOs y tendrás una implementación funcional!**
