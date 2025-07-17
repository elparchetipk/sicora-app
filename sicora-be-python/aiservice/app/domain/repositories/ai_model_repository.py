"""AI Model repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.ai_model import AIModel, ModelType, ModelStatus


class AIModelRepository(ABC):
    """Abstract repository for AI model management."""
    
    @abstractmethod
    async def create(self, model: AIModel) -> AIModel:
        """Create a new AI model configuration."""
        pass
    
    @abstractmethod
    async def get_by_id(self, model_id: UUID) -> Optional[AIModel]:
        """Get AI model by ID."""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[AIModel]:
        """Get AI model by name."""
        pass
    
    @abstractmethod
    async def get_by_type(self, model_type: ModelType) -> List[AIModel]:
        """Get AI models by type."""
        pass
    
    @abstractmethod
    async def get_active_models(self) -> List[AIModel]:
        """Get all active AI models."""
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[AIModel]:
        """Get all available AI models."""
        pass
    
    @abstractmethod
    async def update(self, model: AIModel) -> AIModel:
        """Update an existing AI model."""
        pass
    
    @abstractmethod
    async def delete(self, model_id: UUID) -> bool:
        """Delete an AI model configuration."""
        pass
    
    @abstractmethod
    async def update_status(self, model_id: UUID, status: ModelStatus) -> bool:
        """Update model status."""
        pass
    
    @abstractmethod
    async def get_models_by_feature(self, feature: str) -> List[AIModel]:
        """Get models that support a specific feature."""
        pass
    
    @abstractmethod
    async def get_default_model(self, model_type: Optional[ModelType] = None) -> Optional[AIModel]:
        """Get the default model for a type."""
        pass
    
    @abstractmethod
    async def get_model_statistics(self) -> dict:
        """Get model usage statistics."""
        pass
