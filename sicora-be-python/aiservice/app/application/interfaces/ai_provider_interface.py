"""AI Provider interface for external AI services."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator

from app.domain.value_objects.message import Message
from app.domain.value_objects.ai_prompt import AIPrompt
from app.domain.entities.ai_model import AIModel


class AIProviderInterface(ABC):
    """Abstract interface for AI service providers."""
    
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Message],
        model: AIModel,
        **kwargs
    ) -> Message:
        """Generate a response using the AI model."""
        pass
    
    @abstractmethod
    async def generate_streaming_response(
        self,
        messages: List[Message],
        model: AIModel,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate a streaming response using the AI model."""
        pass
    
    @abstractmethod
    async def generate_completion(
        self,
        prompt: AIPrompt,
        model: AIModel,
        **kwargs
    ) -> str:
        """Generate a text completion."""
        pass
    
    @abstractmethod
    async def generate_embedding(
        self,
        text: str,
        model_name: Optional[str] = None
    ) -> List[float]:
        """Generate text embedding."""
        pass
    
    @abstractmethod
    async def analyze_sentiment(
        self,
        text: str,
        model: Optional[AIModel] = None
    ) -> Dict[str, Any]:
        """Analyze text sentiment."""
        pass
    
    @abstractmethod
    async def summarize_text(
        self,
        text: str,
        model: AIModel,
        max_length: Optional[int] = None
    ) -> str:
        """Summarize text content."""
        pass
    
    @abstractmethod
    async def extract_keywords(
        self,
        text: str,
        model: Optional[AIModel] = None,
        max_keywords: int = 10
    ) -> List[str]:
        """Extract keywords from text."""
        pass
    
    @abstractmethod
    async def classify_content(
        self,
        text: str,
        categories: List[str],
        model: Optional[AIModel] = None
    ) -> Dict[str, float]:
        """Classify text content into categories."""
        pass
    
    @abstractmethod
    async def check_model_availability(self, model: AIModel) -> bool:
        """Check if a model is available."""
        pass
    
    @abstractmethod
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a model."""
        pass
    
    @abstractmethod
    async def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens in text for a specific model."""
        pass
