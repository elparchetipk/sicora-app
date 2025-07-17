from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application settings
    app_name: str = "ProjectEval Service"
    version: str = "1.0.0"
    description: str = "Sistema de Evaluación de Proyectos Formativos - SICORA SENA"
    debug: bool = False

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8007

    # Database settings
    database_url: str = "sqlite+aiosqlite:///./projectevalservice.db"
    database_test_url: str = "sqlite+aiosqlite:///./projectevalservice_test.db"

    # Security settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # External services URLs
    userservice_url: str = "http://localhost:8001"
    scheduleservice_url: str = "http://localhost:8002"

    # File upload settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_extensions: str = ".pdf,.doc,.docx,.txt,.zip,.rar"
    upload_path: str = "./uploads"

    def get_allowed_extensions(self) -> list[str]:
        """Convert the comma-separated string to a list"""
        return [ext.strip() for ext in self.allowed_file_extensions.split(",")]

    # AI and Voice settings
    openai_api_key: Optional[str] = None
    azure_speech_key: Optional[str] = None
    azure_speech_region: Optional[str] = None

    # Background tasks
    redis_url: str = "redis://localhost:6379"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    # CORS settings
    cors_origins: str = "*"  # En producción, especificar dominios exactos separados por comas

    def get_cors_origins(self) -> list[str]:
        """Convert the comma-separated string to a list"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
