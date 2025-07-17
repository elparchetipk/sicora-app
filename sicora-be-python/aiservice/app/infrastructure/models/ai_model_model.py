"""AI Model SQLAlchemy model."""

from sqlalchemy import Column, String, Integer, Float, JSON
from .base_model import BaseModel


class AIModelModel(BaseModel):
    """SQLAlchemy model for AI model configurations."""
    __tablename__ = "ai_models"
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    model_type = Column(String(50), nullable=False, index=True)  # openai_gpt, anthropic_claude, etc.
    model_name = Column(String(200), nullable=False)  # gpt-3.5-turbo, claude-3, etc.
    api_endpoint = Column(String(500), nullable=True)
    api_key_name = Column(String(100), nullable=True)  # Name of env var containing API key
    
    # Model parameters
    max_tokens = Column(Integer, default=4096, nullable=False)
    temperature = Column(Float, default=0.7, nullable=False)
    top_p = Column(Float, default=1.0, nullable=False)
    frequency_penalty = Column(Float, default=0.0, nullable=False)
    presence_penalty = Column(Float, default=0.0, nullable=False)
    context_window = Column(Integer, default=4096, nullable=False)
    cost_per_token = Column(Float, default=0.0, nullable=False)
    
    # Status and metadata
    status = Column(String(20), default="active", nullable=False)  # active, inactive, maintenance, error
    supported_features = Column(JSON, default=list, nullable=False)  # chat, completion, embedding, etc.
    model_metadata = Column(JSON, default=dict, nullable=False)
    
    def __repr__(self):
        return f"<AIModel(id={self.id}, name='{self.name}', type='{self.model_type}', status='{self.status}')>"
    
    @property
    def is_available(self) -> bool:
        """Check if model is available for use."""
        return self.status == "active"
    
    def supports_feature(self, feature: str) -> bool:
        """Check if model supports a specific feature."""
        return feature in self.supported_features
    
    def get_configuration(self) -> dict:
        """Get model configuration parameters."""
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty
        }
    
    def calculate_cost(self, token_count: int) -> float:
        """Calculate cost for given token count."""
        return self.cost_per_token * token_count
