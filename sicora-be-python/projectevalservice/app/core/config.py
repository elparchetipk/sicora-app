from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # App settings
    APP_NAME: str = "ProjectEval Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database settings
    DATABASE_URL: str = (
        "postgresql://projecteval_user:secure_password@localhost:5432/projecteval_db"
    )
    DB_SCHEMA: str = "projectevalservice_schema"
    DB_ECHO: bool = False

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
    ]

    # External services
    USER_SERVICE_URL: str = "http://localhost:8001"
    AISERVICE_URL: str = "http://localhost:8006"

    # Voice processing
    SPEECH_TO_TEXT_PROVIDER: str = "openai"  # openai, azure, google
    OPENAI_API_KEY: str = ""
    AZURE_SPEECH_KEY: str = ""
    AZURE_SPEECH_REGION: str = ""
    GOOGLE_CREDENTIALS_PATH: str = ""

    # File storage
    VOICE_NOTES_STORAGE_PATH: str = "/app/storage/voice_notes"
    MAX_VOICE_NOTE_SIZE_MB: int = 50
    ALLOWED_AUDIO_FORMATS: List[str] = ["wav", "mp3", "m4a", "ogg"]

    # Background tasks
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Performance
    TRANSCRIPTION_TIMEOUT_SECONDS: int = 300
    SENTIMENT_ANALYSIS_TIMEOUT_SECONDS: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
