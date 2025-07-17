"""Configuration module for MEvalService.

This module handles all configuration settings for the Committee Evaluation Service,
including database connections, external service URLs, and business logic parameters.
"""

import os
from functools import lru_cache
from typing import Optional, List

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for MEvalService."""
    
    # API Configuration
    api_title: str = Field(default="MEval Service - Comités de Seguimiento y Evaluación")
    api_version: str = Field(default="1.0.0")
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8009)
    debug: bool = Field(default=False)
    reload: bool = Field(default=False)
    
    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")
    db_schema: str = Field(default="mevalservice_schema")
    db_pool_size: int = Field(default=20)
    db_max_overflow: int = Field(default=30)
    
    # Security Configuration
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=1440)  # 24 hours
    
    # External Service URLs
    user_service_url: str = Field(..., env="USER_SERVICE_URL")
    schedule_service_url: str = Field(..., env="SCHEDULE_SERVICE_URL")
    attendance_service_url: str = Field(..., env="ATTENDANCE_SERVICE_URL")
    notification_service_url: str = Field(..., env="NOTIFICATION_SERVICE_URL")
    evalin_service_url: Optional[str] = Field(default=None, env="EVALIN_SERVICE_URL")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/3")
    redis_password: Optional[str] = Field(default=None)
    cache_ttl: int = Field(default=3600)  # 1 hour
    
    # Scheduled Jobs Configuration
    enable_scheduled_jobs: bool = Field(default=True)
    monthly_analysis_cron: str = Field(default="0 8 * * 0")  # Sunday 8:00 AM
    alert_check_cron: str = Field(default="0 */4 * * *")     # Every 4 hours
    cleanup_cron: str = Field(default="0 2 * * *")           # Daily 2:00 AM
    
    # Committee Configuration
    default_quorum_size: int = Field(default=3)
    max_committee_members: int = Field(default=7)
    convocation_notice_days: int = Field(default=8)
    appeal_deadline_days: int = Field(default=5)
    
    # Detection Algorithm Parameters
    excellence_grade_threshold: float = Field(default=4.5)
    excellence_period_months: int = Field(default=3)
    absence_percentage_threshold: float = Field(default=20.0)
    plan_compliance_threshold: float = Field(default=80.0)
    
    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")
    log_file: Optional[str] = Field(default=None)
    
    # Notification Configuration
    notification_from_email: str = Field(default="comites@sena.edu.co")
    notification_from_name: str = Field(default="Comités CGMLTI")
    enable_email_notifications: bool = Field(default=True)
    enable_sms_notifications: bool = Field(default=False)
    
    # Testing Configuration
    testing: bool = Field(default=False)
    test_database_url: Optional[str] = Field(default=None)
    
    # Monitoring Configuration
    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9009)
    health_check_interval: int = Field(default=30)
    
    # Performance Configuration
    max_concurrent_requests: int = Field(default=100)
    request_timeout: int = Field(default=30)
    connection_timeout: int = Field(default=10)
    
    # Compliance and Audit Configuration
    audit_log_retention_days: int = Field(default=2555)  # 7 years
    document_retention_years: int = Field(default=7)
    enable_audit_trail: bool = Field(default=True)
    
    @validator("excellence_grade_threshold")
    def validate_grade_threshold(cls, v):
        """Validate that grade threshold is within valid range."""
        if not 0.0 <= v <= 5.0:
            raise ValueError("Grade threshold must be between 0.0 and 5.0")
        return v
    
    @validator("absence_percentage_threshold")
    def validate_absence_threshold(cls, v):
        """Validate that absence threshold is within valid percentage range."""
        if not 0.0 <= v <= 100.0:
            raise ValueError("Absence percentage must be between 0.0 and 100.0")
        return v
    
    @validator("plan_compliance_threshold")
    def validate_compliance_threshold(cls, v):
        """Validate that compliance threshold is within valid percentage range."""
        if not 0.0 <= v <= 100.0:
            raise ValueError("Compliance percentage must be between 0.0 and 100.0")
        return v
    
    @property
    def database_url_sync(self) -> str:
        """Get synchronous database URL."""
        return self.database_url.replace("postgresql://", "postgresql://")
    
    @property
    def database_url_async(self) -> str:
        """Get asynchronous database URL."""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")
    
    @property
    def test_database_url_sync(self) -> Optional[str]:
        """Get synchronous test database URL."""
        if self.test_database_url:
            return self.test_database_url.replace("postgresql://", "postgresql://")
        return None
    
    def get_service_url(self, service_name: str) -> str:
        """Get URL for a specific external service."""
        service_urls = {
            "user": self.user_service_url,
            "schedule": self.schedule_service_url,
            "attendance": self.attendance_service_url,
            "notification": self.notification_service_url,
            "evalin": self.evalin_service_url,
        }
        
        url = service_urls.get(service_name.lower())
        if not url:
            raise ValueError(f"Unknown service: {service_name}")
        return url
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Convenience function to get settings
settings = get_settings()
