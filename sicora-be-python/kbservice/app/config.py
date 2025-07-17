"""Environment configuration for the Knowledge Base Service."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./kb.db"
    DATABASE_ECHO: bool = False
    
    # JWT settings (for validating tokens from userservice)
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    
    # AI/ML settings
    OPENAI_API_KEY: Optional[str] = None
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_DIMENSION: int = 1536
    MAX_CONTENT_LENGTH: int = 8000
    OPENAI_BATCH_SIZE: int = 100  # Batch size for OpenAI embedding requests
    OPENAI_REQUEST_TIMEOUT: int = 60  # Timeout in seconds for OpenAI requests
    OPENAI_MAX_RETRIES: int = 3  # Maximum retries for failed requests
    
    # Vector search settings
    VECTOR_SIMILARITY_THRESHOLD: float = 0.7
    MAX_SEARCH_RESULTS: int = 20
    
    # Cache settings
    REDIS_URL: Optional[str] = None
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    
    # Integration settings
    USERSERVICE_URL: str = "http://localhost:8001"
    AISERVICE_URL: str = "http://localhost:8005"
    
    # Application settings
    APP_NAME: str = "SICORA KbService"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]  # En producción, especificar dominios exactos
    
    # Search settings
    SEARCH_RESULT_SNIPPET_LENGTH: int = 200
    SEARCH_HIGHLIGHT_PRE_TAG: str = "<mark>"
    SEARCH_HIGHLIGHT_POST_TAG: str = "</mark>"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
