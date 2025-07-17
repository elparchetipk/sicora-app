# 🔧 **GUÍA TÉCNICA DE IMPLEMENTACIÓN - EVALUACIÓN VII TRIMESTRE**

**Complemento a:** EVALUACION-VII-TRIMESTRE-ADSO.md  
**Propósito:** Ejemplos de código y guías específicas para estudiantes

---

## 🏗️ **EJEMPLOS DE IMPLEMENTACIÓN**

### **PARTE 2.1: Sistema de Preferencias de Usuario**

#### **1. Entidad Domain (UserPreferences)**

```python
# userservice/app/domain/entities/user_preferences.py
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

        # Validaciones de dominio
        self._validate()

    def _validate(self):
        """Validaciones de dominio."""
        valid_languages = ["es", "en"]
        valid_themes = ["light", "dark", "auto"]

        if self.language not in valid_languages:
            raise ValueError(f"Language must be one of: {valid_languages}")

        if self.theme not in valid_themes:
            raise ValueError(f"Theme must be one of: {valid_themes}")

    def update_language(self, language: str):
        """Actualizar idioma."""
        self.language = language
        self.updated_at = datetime.utcnow()
        self._validate()

    def update_theme(self, theme: str):
        """Actualizar tema."""
        self.theme = theme
        self.updated_at = datetime.utcnow()
        self._validate()

    def update_notifications(self, email: bool, push: bool):
        """Actualizar preferencias de notificaciones."""
        self.notifications_email = email
        self.notifications_push = push
        self.updated_at = datetime.utcnow()

    def reset_to_defaults(self):
        """Resetear a valores por defecto."""
        self.language = "es"
        self.theme = "light"
        self.notifications_email = True
        self.notifications_push = True
        self.timezone = "America/Bogota"
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Convertir a diccionario."""
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

#### **2. Repository Interface**

```python
# userservice/app/domain/repositories/user_preferences_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.user_preferences import UserPreferences

class UserPreferencesRepositoryInterface(ABC):
    """Interface para repositorio de preferencias de usuario."""

    @abstractmethod
    async def create(self, preferences: UserPreferences) -> UserPreferences:
        """Crear nuevas preferencias."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[UserPreferences]:
        """Obtener preferencias por ID de usuario."""
        pass

    @abstractmethod
    async def update(self, preferences: UserPreferences) -> UserPreferences:
        """Actualizar preferencias."""
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: UUID) -> bool:
        """Eliminar preferencias por ID de usuario."""
        pass
```

#### **3. Caso de Uso - GetUserPreferencesUseCase**

```python
# userservice/app/application/use_cases/get_user_preferences_use_case.py
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
        # Buscar preferencias existentes
        preferences = await self.preferences_repository.get_by_user_id(user_id)

        # Si no existen, crear preferencias por defecto
        if not preferences:
            preferences = UserPreferences(user_id=user_id)
            preferences = await self.preferences_repository.create(preferences)

        return preferences
```

#### **4. Modelo SQLAlchemy**

```python
# userservice/app/infrastructure/database/models/user_preferences_model.py
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
```

#### **5. Router (Endpoint)**

```python
# userservice/app/presentation/routers/preferences_router.py
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
        preferences = await get_preferences_uc.execute(current_user.user_id)
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
```

---

### **PARTE 2.2: Sistema de Comentarios en Evaluaciones**

#### **1. Entidad Domain (EvaluationComment)**

```python
# evalinservice/app/domain/entities/evaluation_comment.py
from datetime import datetime
from typing import Optional
from uuid import UUID
import uuid

class EvaluationComment:
    """Entidad de comentario en evaluación."""

    def __init__(
        self,
        evaluation_id: UUID,
        user_id: UUID,
        comment_text: str,
        is_private: bool = False,
        comment_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.comment_id = comment_id or uuid.uuid4()
        self.evaluation_id = evaluation_id
        self.user_id = user_id
        self.comment_text = comment_text.strip()
        self.is_private = is_private
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

        # Validaciones
        self._validate()

    def _validate(self):
        """Validaciones de dominio."""
        if not self.comment_text or len(self.comment_text.strip()) < 5:
            raise ValueError("Comment text must be at least 5 characters long")

        if len(self.comment_text) > 1000:
            raise ValueError("Comment text cannot exceed 1000 characters")

    def update_text(self, new_text: str):
        """Actualizar texto del comentario."""
        self.comment_text = new_text.strip()
        self.updated_at = datetime.utcnow()
        self._validate()

    def make_private(self):
        """Hacer comentario privado."""
        self.is_private = True
        self.updated_at = datetime.utcnow()

    def make_public(self):
        """Hacer comentario público."""
        self.is_private = False
        self.updated_at = datetime.utcnow()

    def can_be_edited_by(self, user_id: UUID) -> bool:
        """Verificar si puede ser editado por el usuario."""
        return self.user_id == user_id

    def can_be_viewed_by(self, user_id: UUID, user_role: str) -> bool:
        """Verificar si puede ser visto por el usuario."""
        if self.user_id == user_id:
            return True  # Autor siempre puede ver

        if not self.is_private:
            return True  # Comentarios públicos todos pueden ver

        # Comentarios privados solo admin/coordinador
        return user_role in ["admin", "coordinador"]
```

#### **2. Caso de Uso - CreateCommentUseCase**

```python
# evalinservice/app/application/use_cases/create_comment_use_case.py
from uuid import UUID
from typing import Optional

from app.domain.entities.evaluation_comment import EvaluationComment
from app.domain.repositories.comment_repository import CommentRepositoryInterface
from app.domain.repositories.evaluation_repository import EvaluationRepositoryInterface
from app.domain.exceptions.evaluation_exceptions import (
    EvaluationNotFoundError,
    EvaluationClosedError
)

class CreateCommentUseCase:
    """Caso de uso para crear comentario."""

    def __init__(
        self,
        comment_repository: CommentRepositoryInterface,
        evaluation_repository: EvaluationRepositoryInterface
    ):
        self.comment_repository = comment_repository
        self.evaluation_repository = evaluation_repository

    async def execute(
        self,
        evaluation_id: UUID,
        user_id: UUID,
        comment_text: str,
        is_private: bool = False
    ) -> EvaluationComment:
        """Ejecutar caso de uso."""

        # Verificar que la evaluación existe
        evaluation = await self.evaluation_repository.get_by_id(evaluation_id)
        if not evaluation:
            raise EvaluationNotFoundError(f"Evaluation {evaluation_id} not found")

        # Verificar que la evaluación no esté cerrada
        if evaluation.status == "closed":
            raise EvaluationClosedError("Cannot add comments to closed evaluations")

        # Crear comentario
        comment = EvaluationComment(
            evaluation_id=evaluation_id,
            user_id=user_id,
            comment_text=comment_text,
            is_private=is_private
        )

        # Guardar en repositorio
        return await self.comment_repository.create(comment)
```

---

### **PARTE 3: Comunicación Entre Servicios**

#### **1. Service Client para UserService**

```python
# evalinservice/app/infrastructure/external_services/user_service_client.py
import httpx
from typing import Dict, Any, Optional
from uuid import UUID
import asyncio

class UserServiceClient:
    """Cliente para comunicarse con UserService."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    async def notify_user_activity(
        self,
        user_id: UUID,
        activity_data: Dict[str, Any]
    ) -> bool:
        """Notificar actividad de usuario."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/users/activity-log",
                    json={
                        "user_id": str(user_id),
                        "service_source": "evalinservice",
                        "activity_type": "evaluation_completed",
                        "activity_data": activity_data
                    }
                )
                return response.status_code == 201
        except Exception as e:
            # Log error pero no fallar el proceso principal
            print(f"Error notifying user activity: {e}")
            return False
```

#### **2. Caso de Uso con Notificación**

```python
# evalinservice/app/application/use_cases/complete_evaluation_use_case.py
from uuid import UUID
from datetime import datetime

from app.domain.entities.evaluation import Evaluation
from app.domain.repositories.evaluation_repository import EvaluationRepositoryInterface
from app.infrastructure.external_services.user_service_client import UserServiceClient

class CompleteEvaluationUseCase:
    """Caso de uso para completar evaluación con notificación."""

    def __init__(
        self,
        evaluation_repository: EvaluationRepositoryInterface,
        user_service_client: UserServiceClient
    ):
        self.evaluation_repository = evaluation_repository
        self.user_service_client = user_service_client

    async def execute(self, evaluation_id: UUID, user_id: UUID) -> Evaluation:
        """Completar evaluación y notificar."""

        # Completar evaluación
        evaluation = await self.evaluation_repository.complete_evaluation(
            evaluation_id, user_id
        )

        # Notificar a UserService (async, no blocking)
        activity_data = {
            "evaluation_id": str(evaluation_id),
            "completed_at": datetime.utcnow().isoformat(),
            "evaluation_type": evaluation.evaluation_type
        }

        # Ejecutar notificación en background
        await self._notify_activity(user_id, activity_data)

        return evaluation

    async def _notify_activity(self, user_id: UUID, activity_data: dict):
        """Notificar actividad en background."""
        try:
            await self.user_service_client.notify_user_activity(
                user_id, activity_data
            )
        except Exception as e:
            # Log pero no fallar el proceso principal
            print(f"Background notification failed: {e}")
```

---

## 🧪 **EJEMPLOS DE TESTING**

### **Test Unitario para Entidad**

```python
# tests/unit/test_user_preferences.py
import pytest
from uuid import uuid4
from app.domain.entities.user_preferences import UserPreferences

class TestUserPreferences:

    def test_create_preferences_with_defaults(self):
        """Test crear preferencias con valores por defecto."""
        user_id = uuid4()
        prefs = UserPreferences(user_id=user_id)

        assert prefs.user_id == user_id
        assert prefs.language == "es"
        assert prefs.theme == "light"
        assert prefs.notifications_email is True
        assert prefs.notifications_push is True

    def test_invalid_language_raises_error(self):
        """Test idioma inválido lanza excepción."""
        user_id = uuid4()

        with pytest.raises(ValueError, match="Language must be one of"):
            UserPreferences(user_id=user_id, language="invalid")

    def test_update_language(self):
        """Test actualización de idioma."""
        user_id = uuid4()
        prefs = UserPreferences(user_id=user_id)

        prefs.update_language("en")
        assert prefs.language == "en"

    def test_reset_to_defaults(self):
        """Test reset a valores por defecto."""
        user_id = uuid4()
        prefs = UserPreferences(
            user_id=user_id,
            language="en",
            theme="dark",
            notifications_email=False
        )

        prefs.reset_to_defaults()

        assert prefs.language == "es"
        assert prefs.theme == "light"
        assert prefs.notifications_email is True
```

### **Test de Integración para API**

```python
# tests/integration/test_preferences_api.py
import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_get_preferences_creates_defaults(
    client: AsyncClient,
    authenticated_user_headers
):
    """Test obtener preferencias crea por defecto si no existen."""

    response = await client.get(
        "/api/v1/users/preferences",
        headers=authenticated_user_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["language"] == "es"
    assert data["theme"] == "light"
    assert data["notifications_email"] is True

@pytest.mark.asyncio
async def test_update_preferences(
    client: AsyncClient,
    authenticated_user_headers
):
    """Test actualizar preferencias."""

    update_data = {
        "language": "en",
        "theme": "dark",
        "notifications_email": False,
        "notifications_push": True,
        "timezone": "UTC"
    }

    response = await client.put(
        "/api/v1/users/preferences",
        json=update_data,
        headers=authenticated_user_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["language"] == "en"
    assert data["theme"] == "dark"
    assert data["notifications_email"] is False

@pytest.mark.asyncio
async def test_invalid_language_returns_400(
    client: AsyncClient,
    authenticated_user_headers
):
    """Test idioma inválido retorna 400."""

    update_data = {"language": "invalid"}

    response = await client.put(
        "/api/v1/users/preferences",
        json=update_data,
        headers=authenticated_user_headers
    )

    assert response.status_code == 400
    assert "Language must be one of" in response.json()["detail"]
```

---

## 📋 **CHECKLIST DE ENTREGA**

### **Pre-entrega (Autovalidación)**

- [ ] **Domain Layer**
  - [ ] Entidades implementadas con validaciones
  - [ ] Excepciones específicas del dominio
  - [ ] Repository interfaces definidos

- [ ] **Application Layer**
  - [ ] Use cases implementados correctamente
  - [ ] DTOs/Schemas para request/response
  - [ ] Manejo de errores apropiado

- [ ] **Infrastructure Layer**
  - [ ] Modelos SQLAlchemy implementados
  - [ ] Repository implementations completas
  - [ ] Migraciones de base de datos

- [ ] **Presentation Layer**
  - [ ] Routers con endpoints funcionales
  - [ ] Validación de entrada (Pydantic)
  - [ ] Documentación Swagger completa

- [ ] **Testing**
  - [ ] Tests unitarios para use cases
  - [ ] Tests de integración para APIs
  - [ ] Coverage mínimo del 80%
  - [ ] Tests de manejo de errores

- [ ] **Comunicación Entre Servicios**
  - [ ] Cliente HTTP implementado
  - [ ] Notificaciones funcionando
  - [ ] Manejo de errores de red

### **Documentación**

- [ ] README con instrucciones de instalación
- [ ] Análisis de arquitectura completado
- [ ] Documentación de casos de uso
- [ ] Reflexión personal incluida

---

**¡Esta guía técnica te proporcionará las bases para una implementación exitosa! Recuerda seguir los patrones establecidos en el código existente y mantener la consistencia arquitectónica.**
