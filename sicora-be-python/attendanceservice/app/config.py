"""Environment configuration for AttendanceService."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings for AttendanceService."""
    
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://attendanceservice_user:attendanceservice_password@postgres:5432/sicora_db"
    DATABASE_ECHO: bool = False
    
    # JWT settings (for token validation)
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    
    # File upload settings
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB for justification PDFs
    ALLOWED_FILE_TYPES: list[str] = ["application/pdf"]
    UPLOAD_DIRECTORY: str = "/app/uploads/justifications"
    
    # QR Code settings
    QR_CODE_REFRESH_SECONDS: int = 15
    QR_CODE_SECRET: str = "qr-code-secret-change-in-production"
    
    # Attendance settings
    ATTENDANCE_GRACE_PERIOD_MINUTES: int = 15  # Grace period for late attendance
    CONSECUTIVE_ABSENCES_ALERT_THRESHOLD: int = 3
    MONTHLY_ATTENDANCE_ALERT_THRESHOLD: float = 0.8  # 80%
    
    # External service URLs
    USERSERVICE_URL: str = "http://userservice:8000"
    SCHEDULESERVICE_URL: str = "http://scheduleservice:8000"
    
    # Application settings
    APP_NAME: str = "SICORA AttendanceService"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]  # En producción, especificar dominios exactos
    
    # External services URLs
    USER_SERVICE_URL: str = "http://userservice:8000"
    SCHEDULE_SERVICE_URL: str = "http://scheduleservice:8000"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
