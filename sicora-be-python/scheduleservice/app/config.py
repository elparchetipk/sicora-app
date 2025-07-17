"""Configuration settings for ScheduleService."""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "ScheduleService"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://scheduleservice_user:scheduleservice_password@localhost:5432/sicora_db"
    )
    DATABASE_ECHO: bool = False
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
    ]
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "your-secret-key-change-in-production"
    )
    
    # External Services
    USER_SERVICE_URL: str = os.getenv(
        "USER_SERVICE_URL",
        "http://localhost:8001"
    )
    
    class Config:
        env_file = ".env"


settings = Settings()
