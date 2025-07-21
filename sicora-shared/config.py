"""
Configuración centralizada para SICORA Backend Python.

Este módulo maneja toda la configuración de la aplicación usando Pydantic Settings,
permitiendo configuración a través de variables de entorno, archivos .env, y valores por defecto.
"""

import os
from typing import Optional, List
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings
from enum import Enum


class Environment(str, Enum):
    """Entornos de ejecución disponibles."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    TEST = "test"  # Alias para testing
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Niveles de logging disponibles."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseConfig(BaseSettings):
    """Configuración de base de datos."""

    # Database connection
    host: str = Field(default="localhost", description="Host de la base de datos")
    port: int = Field(default=5433, description="Puerto de la base de datos")
    username: str = Field(
        default="sicora_user", description="Usuario de la base de datos"
    )
    password: str = Field(
        default="sicora_password", description="Contraseña de la base de datos"
    )
    database: str = Field(
        default="sicora_dev", description="Nombre de la base de datos"
    )

    # Connection pool settings
    pool_size: int = Field(default=10, description="Tamaño del pool de conexiones")
    max_overflow: int = Field(default=20, description="Máximo overflow del pool")
    pool_timeout: int = Field(default=30, description="Timeout del pool en segundos")
    pool_recycle: int = Field(
        default=3600, description="Tiempo de reciclaje de conexiones"
    )

    # Query settings
    echo: bool = Field(default=False, description="Echo de queries SQL")
    echo_pool: bool = Field(default=False, description="Echo del pool de conexiones")

    model_config = ConfigDict(env_prefix="DB_", case_sensitive=False, extra="ignore")

    @property
    def url(self) -> str:
        """Construir URL de conexión a la base de datos."""
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def sync_url(self) -> str:
        """Construir URL de conexión síncrona a la base de datos."""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseSettings):
    """Configuración de Redis."""

    host: str = Field(default="localhost", description="Host de Redis")
    port: int = Field(default=6379, description="Puerto de Redis")
    password: Optional[str] = Field(default=None, description="Contraseña de Redis")
    database: int = Field(default=0, description="Base de datos de Redis")

    # Connection settings
    socket_timeout: int = Field(default=5, description="Timeout de socket")
    socket_connect_timeout: int = Field(default=5, description="Timeout de conexión")
    retry_on_timeout: bool = Field(default=True, description="Reintentar en timeout")

    model_config = ConfigDict(env_prefix="REDIS_", case_sensitive=False, extra="ignore")

    @property
    def url(self) -> str:
        """Construir URL de conexión a Redis."""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.database}"
        return f"redis://{self.host}:{self.port}/{self.database}"


class SecurityConfig(BaseSettings):
    """Configuración de seguridad."""

    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Clave secreta para signing",
    )
    algorithm: str = Field(default="HS256", description="Algoritmo de encriptación")
    access_token_expire_minutes: int = Field(
        default=30, description="Minutos de expiración del token de acceso"
    )
    refresh_token_expire_days: int = Field(
        default=30, description="Días de expiración del refresh token"
    )

    # Password settings
    min_password_length: int = Field(
        default=8, description="Longitud mínima de contraseña"
    )
    password_require_uppercase: bool = Field(
        default=True, description="Requerir mayúsculas"
    )
    password_require_lowercase: bool = Field(
        default=True, description="Requerir minúsculas"
    )
    password_require_numbers: bool = Field(default=True, description="Requerir números")
    password_require_special: bool = Field(
        default=True, description="Requerir caracteres especiales"
    )

    # CORS settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Orígenes permitidos para CORS",
    )
    cors_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Métodos HTTP permitidos",
    )
    cors_headers: List[str] = Field(default=["*"], description="Headers permitidos")

    model_config = ConfigDict(
        env_prefix="SECURITY_", case_sensitive=False, extra="ignore"
    )

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v, info):
        """Validar que la secret key no sea la por defecto en producción."""
        # info.data contiene el diccionario de datos validados hasta el momento
        environment = info.data.get("environment", Environment.DEVELOPMENT)
        if (
            environment == Environment.PRODUCTION
            and v == "dev-secret-key-change-in-production"
        ):
            raise ValueError("Must set SECURITY_SECRET_KEY in production")
        return v


class APIConfig(BaseSettings):
    """Configuración de API."""

    title: str = Field(default="SICORA Backend API", description="Título de la API")
    description: str = Field(
        default="Backend API para el Sistema SICORA",
        description="Descripción de la API",
    )
    version: str = Field(default="1.0.0", description="Versión de la API")

    # Server settings
    host: str = Field(default="0.0.0.0", description="Host del servidor")
    port: int = Field(default=8000, description="Puerto del servidor")
    workers: int = Field(default=1, description="Número de workers")

    # Request settings
    max_request_size: int = Field(
        default=16 * 1024 * 1024, description="Tamaño máximo de request"
    )
    request_timeout: int = Field(
        default=30, description="Timeout de request en segundos"
    )

    # Rate limiting
    rate_limit_enabled: bool = Field(
        default=True, description="Habilitar rate limiting"
    )
    rate_limit_requests: int = Field(default=100, description="Requests por minuto")
    rate_limit_window: int = Field(
        default=60, description="Ventana de tiempo en segundos"
    )

    model_config = ConfigDict(env_prefix="API_", case_sensitive=False, extra="ignore")


class LoggingConfig(BaseSettings):
    """Configuración de logging."""

    level: LogLevel = Field(default=LogLevel.INFO, description="Nivel de logging")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Formato de logging",
    )

    # File logging
    log_to_file: bool = Field(default=False, description="Guardar logs en archivo")
    log_file_path: str = Field(
        default="logs/sicora.log", description="Ruta del archivo de log"
    )
    log_file_max_size: int = Field(
        default=10 * 1024 * 1024, description="Tamaño máximo del archivo"
    )
    log_file_backup_count: int = Field(default=5, description="Número de backups")

    # Structured logging
    structured_logging: bool = Field(
        default=True, description="Usar logging estructurado"
    )
    include_trace_id: bool = Field(default=True, description="Incluir trace ID")

    model_config = ConfigDict(env_prefix="LOG_", case_sensitive=False, extra="ignore")


class MonitoringConfig(BaseSettings):
    """Configuración de monitoreo."""

    # Metrics
    metrics_enabled: bool = Field(default=True, description="Habilitar métricas")
    metrics_path: str = Field(default="/metrics", description="Path de métricas")

    # Health checks
    health_check_enabled: bool = Field(
        default=True, description="Habilitar health checks"
    )
    health_check_path: str = Field(
        default="/health", description="Path de health check"
    )

    # Tracing
    tracing_enabled: bool = Field(default=False, description="Habilitar tracing")
    tracing_sample_rate: float = Field(default=0.1, description="Rate de sampling")

    # Profiling
    profiling_enabled: bool = Field(default=False, description="Habilitar profiling")

    model_config = ConfigDict(
        env_prefix="MONITORING_", case_sensitive=False, extra="ignore"
    )


class ExternalServicesConfig(BaseSettings):
    """Configuración de servicios externos."""

    # Email service
    email_enabled: bool = Field(
        default=False, description="Habilitar servicio de email"
    )
    email_smtp_host: str = Field(default="localhost", description="Host SMTP")
    email_smtp_port: int = Field(default=587, description="Puerto SMTP")
    email_username: Optional[str] = Field(default=None, description="Usuario SMTP")
    email_password: Optional[str] = Field(default=None, description="Contraseña SMTP")
    email_use_tls: bool = Field(default=True, description="Usar TLS")

    # AI Service
    openai_api_key: Optional[str] = Field(default=None, description="API Key de OpenAI")
    openai_model: str = Field(default="gpt-3.5-turbo", description="Modelo de OpenAI")
    openai_max_tokens: int = Field(default=1000, description="Máximo de tokens")

    model_config = ConfigDict(
        env_prefix="EXTERNAL_", case_sensitive=False, extra="ignore"
    )


class Settings(BaseSettings):
    """Configuración principal de la aplicación."""

    # Environment
    environment: Environment = Field(
        default=Environment.DEVELOPMENT, description="Entorno de ejecución"
    )
    debug: bool = Field(default=True, description="Modo debug")

    # Service identification
    service_name: str = Field(
        default="sicora-backend", description="Nombre del servicio"
    )
    service_version: str = Field(default="1.0.0", description="Versión del servicio")

    # Sub-configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    external: ExternalServicesConfig = Field(default_factory=ExternalServicesConfig)

    model_config = ConfigDict(case_sensitive=False, extra="ignore")

    @classmethod
    def from_env_file(cls, env_file: str):
        """Crear configuración desde un archivo específico."""
        return cls(_env_file=env_file)

    @field_validator("debug")
    @classmethod
    def set_debug_based_on_environment(cls, v, info):
        """Configurar debug basado en el entorno."""
        environment = info.data.get("environment", Environment.DEVELOPMENT)
        if environment == Environment.PRODUCTION:
            return False
        return v

    def get_database_url(self, service_name: Optional[str] = None) -> str:
        """Obtener URL de base de datos para un servicio específico."""
        if service_name:
            # Override database name for specific service
            db_name = f"sicora_{service_name}"
            if self.environment == Environment.TESTING:
                db_name += "_test"
            return f"postgresql+asyncpg://{self.database.username}:{self.database.password}@{self.database.host}:{self.database.port}/{db_name}"
        return self.database.url

    def is_production(self) -> bool:
        """Verificar si estamos en producción."""
        return self.environment == Environment.PRODUCTION

    def is_development(self) -> bool:
        """Verificar si estamos en desarrollo."""
        return self.environment == Environment.DEVELOPMENT

    def is_testing(self) -> bool:
        """Verificar si estamos en testing."""
        return self.environment == Environment.TESTING


# Instancia global de configuración
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency para obtener configuración en FastAPI.

    Usage:
        @app.get("/info")
        def get_info(settings: Settings = Depends(get_settings)):
            return {"service": settings.service_name}
    """
    return settings


def load_config_from_file(file_path: str) -> Settings:
    """Cargar configuración desde archivo específico."""
    return Settings(_env_file=file_path)


def get_service_config(service_name: str) -> dict:
    """Obtener configuración específica para un servicio."""
    base_config = {
        "service_name": service_name,
        "database_url": settings.get_database_url(service_name),
        "redis_url": settings.redis.url,
        "environment": settings.environment,
        "debug": settings.debug,
        "log_level": settings.logging.level,
    }
    return base_config
