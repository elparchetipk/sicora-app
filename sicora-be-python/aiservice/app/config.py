"""Environment configuration for AI Service."""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """AI Service application settings."""
    
    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    DB_SCHEMA: str = "public"  # AÑADIDO: Para especificar el esquema de la BD, se carga desde .env
    DATABASE_ECHO: bool = False
    
    # AI Provider settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_DEFAULT_MODEL: str = "gpt-3.5-turbo"
    
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_DEFAULT_MODEL: str = "claude-3-haiku-20240307"
    
    # Embedding settings
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_DIMENSION: int = 1536
    
    # Vector Store settings
    VECTOR_STORE_TYPE: str = "chromadb"  # chromadb, pinecone, weaviate
    CHROMADB_PATH: str = "./chromadb"
    CHROMADB_COLLECTION: str = "ai_knowledge_base"
    
    # Pinecone settings (if using Pinecone)
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_INDEX_NAME: str = "ai-knowledge-base"
    
    # Redis Cache settings
    REDIS_URL: str = "redis://localhost:6379/1"
    REDIS_PASSWORD: Optional[str] = None
    CACHE_TTL_SECONDS: int = 3600
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Token limits
    MAX_TOKENS_PER_REQUEST: int = 4000
    MAX_CONTEXT_WINDOW: int = 8000
    TOKEN_BUFFER: int = 200
    
    # Knowledge base settings
    MAX_KNOWLEDGE_ENTRIES: int = 10000
    SIMILARITY_THRESHOLD: float = 0.75
    MAX_SEARCH_RESULTS: int = 10
    
    # Processing settings
    MAX_CONCURRENT_REQUESTS: int = 10
    REQUEST_TIMEOUT_SECONDS: int = 60
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY_SECONDS: int = 1
    
    # Monitoring and analytics
    ENABLE_ANALYTICS: bool = True
    ANALYTICS_RETENTION_DAYS: int = 90
    LOG_CONVERSATIONS: bool = True
    
    # Security settings
    API_KEY_HEADER: str = "X-API-Key"
    ENABLE_API_KEY_AUTH: bool = False
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Application settings
    APP_NAME: str = "SICORA AI Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Feature flags
    ENABLE_STREAMING_RESPONSES: bool = True
    ENABLE_FUNCTION_CALLING: bool = False
    ENABLE_IMAGE_ANALYSIS: bool = False
    ENABLE_CODE_EXECUTION: bool = False
    
    # Model configuration defaults
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 1000
    DEFAULT_TOP_P: float = 1.0
    DEFAULT_FREQUENCY_PENALTY: float = 0.0
    DEFAULT_PRESENCE_PENALTY: float = 0.0
    
    # Content safety
    ENABLE_CONTENT_FILTER: bool = True
    MAX_CONTENT_LENGTH: int = 50000
    BLOCKED_WORDS: List[str] = []
    
    # Backup and maintenance
    BACKUP_ENABLED: bool = True
    BACKUP_INTERVAL_HOURS: int = 24
    BACKUP_RETENTION_DAYS: int = 30
    MAINTENANCE_MODE: bool = False
    
    # KbService Integration
    KB_SERVICE_URL: str = "http://kbservice:8006/api/v1"
    KB_SERVICE_TIMEOUT: int = 30
    KB_INTEGRATION_ENABLED: bool = True
    
    # OpenAI Configuration for Enhanced Chat
    OPENAI_ORGANIZATION: Optional[str] = None
    OPENAI_TIMEOUT: int = 30
    
    # Enhanced Chat Settings
    DEFAULT_CHAT_MODEL: str = "gpt-4"
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 1000
    KNOWLEDGE_SEARCH_LIMIT: int = 5
    CONVERSATION_HISTORY_LIMIT: int = 10
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get settings singleton instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def get_database_url() -> str:
    """Get database URL with environment-specific defaults."""
    if settings.ENVIRONMENT == "test":
        return "sqlite+aiosqlite:///./test_ai.db"
    elif settings.ENVIRONMENT == "production":
        return settings.DATABASE_URL or "postgresql+asyncpg://user:password@localhost:5432/ai_service"
    else:
        return settings.DATABASE_URL


def get_redis_url() -> str:
    """Get Redis URL with environment-specific defaults."""
    if settings.ENVIRONMENT == "test":
        return "redis://localhost:6379/15"  # Use different DB for tests
    return settings.REDIS_URL


def is_development() -> bool:
    """Check if running in development environment."""
    return settings.ENVIRONMENT == "development"


def is_production() -> bool:
    """Check if running in production environment."""
    return settings.ENVIRONMENT == "production"


def get_log_config() -> dict:
    """Get logging configuration."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
            "detailed": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s (%(filename)s:%(lineno)d): %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "default" if is_production() else "detailed",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console"],
        },
        "loggers": {
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }
