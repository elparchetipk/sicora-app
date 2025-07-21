#!/usr/bin/env python3
"""
Script de gestión de configuración para SICORA Backend Python.

Este script permite:
- Validar configuración para diferentes entornos
- Generar archivos de configuración de ejemplo
- Verificar variables de entorno requeridas
- Migrar configuración entre entornos
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Optional
from pathlib import Path

# Añadir el path del proyecto para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.config import Settings, Environment


class ConfigManager:
    """Gestor de configuración para diferentes entornos."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_files = {
            Environment.DEVELOPMENT: self.project_root / ".env.development",
            Environment.TESTING: self.project_root / ".env.testing",
            Environment.TEST: self.project_root / ".env.test",
            Environment.STAGING: self.project_root / ".env.staging",
            Environment.PRODUCTION: self.project_root / ".env.production",
        }

    def validate_environment(self, environment: Environment) -> Dict[str, any]:
        """Validar configuración de un entorno específico."""
        print(f"🔍 Validando configuración para entorno: {environment.value}")

        # Cargar configuración del entorno
        config_file = self.config_files.get(environment)
        if not config_file or not config_file.exists():
            return {
                "valid": False,
                "error": f"Archivo de configuración no encontrado: {config_file}",
                "warnings": [],
                "missing_vars": [],
            }  # Cargar y validar settings
        try:
            # Temporal override del entorno
            original_environment = os.environ.get("ENVIRONMENT")
            os.environ["ENVIRONMENT"] = environment.value

            settings = Settings.from_env_file(str(config_file))

            # Restaurar configuración original
            if original_environment:
                os.environ["ENVIRONMENT"] = original_environment
            elif "ENVIRONMENT" in os.environ:
                del os.environ["ENVIRONMENT"]

            warnings = []
            missing_vars = []

            # Validaciones específicas por entorno
            if environment == Environment.PRODUCTION:
                # Verificar que no use valores por defecto inseguros
                if (
                    settings.security.secret_key
                    == "dev-secret-key-change-in-production"
                ):
                    warnings.append("Usando secret key por defecto en producción")
                    missing_vars.append("SECURITY_SECRET_KEY")

                if (
                    "CHANGEME" in settings.database.password
                    or "MUST_BE_CHANGED" in settings.database.password
                ):
                    warnings.append("Usando contraseña de DB por defecto en producción")

                if settings.redis.password and (
                    "CHANGEME" in settings.redis.password
                    or "MUST_BE_CHANGED" in settings.redis.password
                ):
                    warnings.append(
                        "Usando contraseña de Redis por defecto en producción"
                    )

            elif environment == Environment.DEVELOPMENT:
                # Verificar configuración de desarrollo
                if not settings.debug:
                    warnings.append("Debug deshabilitado en desarrollo")

            result = {
                "valid": len(missing_vars) == 0,
                "settings": settings,
                "warnings": warnings,
                "missing_vars": missing_vars,
                "config_file": str(config_file),
            }

            if result["valid"]:
                print(f"✅ Configuración válida para {environment.value}")
            else:
                print(f"❌ Configuración inválida para {environment.value}")

            return result

        except Exception as e:
            return {
                "valid": False,
                "error": f"Error al validar configuración: {str(e)}",
                "warnings": [],
                "missing_vars": [],
            }

    def generate_example_config(
        self, environment: Environment, output_file: Optional[str] = None
    ):
        """Generar archivo de configuración de ejemplo."""
        print(f"📝 Generando configuración de ejemplo para {environment.value}")

        # Cargar configuración base
        settings = Settings()

        # Generar contenido del archivo
        config_content = f"""# SICORA Backend Python - Configuración de {environment.value.title()}
# Archivo de ejemplo generado automáticamente

# Environment
ENVIRONMENT={environment.value}
DEBUG={'true' if environment != Environment.PRODUCTION else 'false'}

# Service Information
SERVICE_NAME=sicora-backend
SERVICE_VERSION=1.0.0

# Database Configuration
DB_HOST={settings.database.host}
DB_PORT={settings.database.port}
DB_USERNAME={settings.database.username}
DB_PASSWORD=your_password_here
DB_DATABASE=sicora_{environment.value}
DB_POOL_SIZE={settings.database.pool_size}
DB_MAX_OVERFLOW={settings.database.max_overflow}

# Redis Configuration
REDIS_HOST={settings.redis.host}
REDIS_PORT={settings.redis.port}
REDIS_DATABASE={settings.redis.database}

# Security Configuration
SECURITY_SECRET_KEY=your_secret_key_here
SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES={settings.security.access_token_expire_minutes}
SECURITY_CORS_ORIGINS={settings.security.cors_origins}

# API Configuration
API_TITLE=SICORA Backend API ({environment.value.title()})
API_VERSION={settings.api.version}
API_HOST={settings.api.host}
API_PORT={settings.api.port}

# Logging Configuration
LOG_LEVEL={settings.logging.level.value}
LOG_TO_FILE={'true' if environment != Environment.TESTING else 'false'}
LOG_STRUCTURED_LOGGING=true

# Monitoring Configuration
MONITORING_METRICS_ENABLED=true
MONITORING_HEALTH_CHECK_ENABLED=true
MONITORING_TRACING_ENABLED={'true' if environment in [Environment.STAGING, Environment.PRODUCTION] else 'false'}

# External Services Configuration
EXTERNAL_EMAIL_ENABLED={'true' if environment != Environment.TESTING else 'false'}
EXTERNAL_OPENAI_API_KEY=your_openai_key_here
"""

        # Determinar archivo de salida
        if output_file:
            output_path = Path(output_file)
        else:
            output_path = self.project_root / f".env.{environment.value}.example"

        # Escribir archivo
        output_path.write_text(config_content)
        print(f"✅ Archivo generado: {output_path}")

    def check_environment_variables(self, environment: Environment) -> Dict[str, any]:
        """Verificar variables de entorno requeridas."""
        print(f"🔍 Verificando variables de entorno para {environment.value}")

        required_vars = {
            Environment.PRODUCTION: [
                "SECRET_KEY_PRODUCTION",
                "DB_PASSWORD_PRODUCTION",
                "DB_HOST_PRODUCTION",
                "REDIS_PASSWORD_PRODUCTION",
                "EMAIL_PASSWORD_PRODUCTION",
            ],
            Environment.STAGING: ["SECRET_KEY_STAGING", "DB_PASSWORD_STAGING"],
            Environment.DEVELOPMENT: [],
            Environment.TESTING: [],
        }

        missing_vars = []
        present_vars = []

        for var in required_vars.get(environment, []):
            if os.environ.get(var):
                present_vars.append(var)
            else:
                missing_vars.append(var)

        result = {
            "environment": environment.value,
            "missing_vars": missing_vars,
            "present_vars": present_vars,
            "all_present": len(missing_vars) == 0,
        }

        if result["all_present"]:
            print(f"✅ Todas las variables requeridas están presentes")
        else:
            print(f"❌ Variables faltantes: {', '.join(missing_vars)}")

        return result

    def compare_environments(self, env1: Environment, env2: Environment):
        """Comparar configuración entre dos entornos."""
        print(f"🔄 Comparando configuración: {env1.value} vs {env2.value}")

        result1 = self.validate_environment(env1)
        result2 = self.validate_environment(env2)

        if not result1["valid"] or not result2["valid"]:
            print("❌ No se puede comparar debido a configuración inválida")
            return

        settings1 = result1["settings"]
        settings2 = result2["settings"]

        # Comparar configuraciones importantes
        differences = []

        if settings1.database.host != settings2.database.host:
            differences.append(
                f"DB Host: {settings1.database.host} vs {settings2.database.host}"
            )

        if settings1.database.port != settings2.database.port:
            differences.append(
                f"DB Port: {settings1.database.port} vs {settings2.database.port}"
            )

        if settings1.debug != settings2.debug:
            differences.append(f"Debug: {settings1.debug} vs {settings2.debug}")

        if settings1.logging.level != settings2.logging.level:
            differences.append(
                f"Log Level: {settings1.logging.level} vs {settings2.logging.level}"
            )

        print(f"\n📊 Diferencias encontradas:")
        if differences:
            for diff in differences:
                print(f"  • {diff}")
        else:
            print("  • No se encontraron diferencias significativas")


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Gestor de configuración SICORA Backend"
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # Comando validate
    validate_parser = subparsers.add_parser("validate", help="Validar configuración")
    validate_parser.add_argument(
        "--environment",
        "-e",
        choices=[env.value for env in Environment],
        default=Environment.DEVELOPMENT.value,
        help="Entorno a validar",
    )

    # Comando generate
    generate_parser = subparsers.add_parser(
        "generate", help="Generar configuración de ejemplo"
    )
    generate_parser.add_argument(
        "--environment",
        "-e",
        choices=[env.value for env in Environment],
        default=Environment.DEVELOPMENT.value,
        help="Entorno para generar",
    )
    generate_parser.add_argument("--output", "-o", help="Archivo de salida")

    # Comando check-env
    check_parser = subparsers.add_parser(
        "check-env", help="Verificar variables de entorno"
    )
    check_parser.add_argument(
        "--environment",
        "-e",
        choices=[env.value for env in Environment],
        default=Environment.PRODUCTION.value,
        help="Entorno a verificar",
    )

    # Comando compare
    compare_parser = subparsers.add_parser("compare", help="Comparar entornos")
    compare_parser.add_argument("env1", choices=[env.value for env in Environment])
    compare_parser.add_argument("env2", choices=[env.value for env in Environment])

    # Comando validate-all
    subparsers.add_parser("validate-all", help="Validar todos los entornos")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    config_manager = ConfigManager()

    if args.command == "validate":
        env = Environment(args.environment)
        result = config_manager.validate_environment(env)

        print(f"\n📋 Resultado de validación:")
        print(f"  Válido: {'✅' if result['valid'] else '❌'}")
        if "error" in result:
            print(f"  Error: {result['error']}")
        if result.get("warnings"):
            print(f"  Advertencias: {', '.join(result['warnings'])}")
        if result.get("missing_vars"):
            print(f"  Variables faltantes: {', '.join(result['missing_vars'])}")

    elif args.command == "generate":
        env = Environment(args.environment)
        config_manager.generate_example_config(env, args.output)

    elif args.command == "check-env":
        env = Environment(args.environment)
        result = config_manager.check_environment_variables(env)

        print(f"\n📋 Variables de entorno:")
        if result["present_vars"]:
            print(f"  Presentes: {', '.join(result['present_vars'])}")
        if result["missing_vars"]:
            print(f"  Faltantes: {', '.join(result['missing_vars'])}")

    elif args.command == "compare":
        env1 = Environment(args.env1)
        env2 = Environment(args.env2)
        config_manager.compare_environments(env1, env2)

    elif args.command == "validate-all":
        print("🔍 Validando todos los entornos...\n")

        for env in Environment:
            result = config_manager.validate_environment(env)
            status = "✅" if result["valid"] else "❌"
            print(f"{status} {env.value.title()}")
            if not result["valid"] and "error" in result:
                print(f"    Error: {result['error']}")


if __name__ == "__main__":
    main()
