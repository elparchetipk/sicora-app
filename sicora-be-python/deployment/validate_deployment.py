#!/usr/bin/env python3
"""
Script de validación de deployment para SICORA Backend Python.
Verifica que todas las configuraciones estén correctas antes del deployment.
"""

import asyncio
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
import httpx
import psutil


class DeploymentValidator:
    """Validador de configuración de deployment."""

    def __init__(self, environment: str):
        self.environment = environment
        self.project_root = Path(__file__).parent.parent
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def log_error(self, message: str):
        """Registrar un error."""
        self.errors.append(message)
        print(f"❌ ERROR: {message}")

    def log_warning(self, message: str):
        """Registrar una advertencia."""
        self.warnings.append(message)
        print(f"⚠️ WARNING: {message}")

    def log_success(self, message: str):
        """Registrar un éxito."""
        print(f"✅ {message}")

    def log_info(self, message: str):
        """Registrar información."""
        print(f"ℹ️ {message}")

    def validate_environment_file(self):
        """Validar que existe el archivo de entorno."""
        env_file = self.project_root / f".env.{self.environment}"

        if not env_file.exists():
            self.log_error(f"Archivo de entorno no encontrado: {env_file}")
            return False

        # Verificar que tiene las variables necesarias
        required_vars = ["DATABASE_URL", "SECRET_KEY", "ENVIRONMENT"]

        env_content = env_file.read_text()
        missing_vars = []

        for var in required_vars:
            if f"{var}=" not in env_content:
                missing_vars.append(var)

        if missing_vars:
            self.log_error(f"Variables faltantes en {env_file}: {missing_vars}")
            return False

        self.log_success(f"Archivo de entorno válido: {env_file}")
        return True

    def validate_python_dependencies(self):
        """Validar dependencias de Python."""
        requirements_file = self.project_root / "requirements.txt"

        if not requirements_file.exists():
            self.log_error("Archivo requirements.txt no encontrado")
            return False

        try:
            import fastapi
            import uvicorn
            import sqlalchemy
            import pydantic
            import httpx
            import pytest

            self.log_success("Dependencias principales de Python disponibles")
            return True

        except ImportError as e:
            self.log_error(f"Dependencia faltante: {e}")
            return False

    def validate_docker_setup(self):
        """Validar configuración de Docker (solo para staging/production)."""
        if self.environment in ["development", "testing"]:
            return True

        # Verificar que Docker está disponible
        if not self._command_available("docker"):
            self.log_error("Docker no está disponible")
            return False

        if not self._command_available("docker compose"):
            self.log_error("Docker Compose no está disponible")
            return False

        # Verificar archivos Docker
        dockerfile_api = self.project_root / "deployment" / "Dockerfile.apigateway"
        dockerfile_notif = self.project_root / "deployment" / "Dockerfile.notification"
        compose_file = (
            self.project_root / "deployment" / f"docker-compose.{self.environment}.yml"
        )

        missing_files = []
        for file_path in [dockerfile_api, dockerfile_notif, compose_file]:
            if not file_path.exists():
                missing_files.append(str(file_path))

        if missing_files:
            self.log_error(f"Archivos Docker faltantes: {missing_files}")
            return False

        self.log_success("Configuración de Docker válida")
        return True

    def validate_database_connectivity(self):
        """Validar conectividad a la base de datos."""
        self.log_info("Verificando conectividad a base de datos...")

        # En desarrollo/testing, verificar PostgreSQL local
        if self.environment in ["development", "testing"]:
            try:
                import psycopg2

                conn = psycopg2.connect(
                    host="localhost",
                    port="5433",
                    database=(
                        "sicora_dev"
                        if self.environment == "development"
                        else "sicora_test"
                    ),
                    user="sicora_user",
                    password="sicora_password",
                )
                conn.close()
                self.log_success("Conectividad a base de datos verificada")
                return True

            except Exception as e:
                self.log_warning(f"No se pudo conectar a la base de datos: {e}")
                return False
        else:
            self.log_info("Verificación de BD omitida para entorno remoto")
            return True

    def validate_port_availability(self):
        """Validar que los puertos necesarios están disponibles."""
        required_ports = [8000, 8001]  # APIGateway, NotificationService

        if self.environment in ["development", "testing"]:
            busy_ports = []
            for port in required_ports:
                if self._port_in_use(port):
                    busy_ports.append(port)

            if busy_ports:
                self.log_warning(f"Puertos en uso: {busy_ports}")
                return False

        self.log_success("Puertos disponibles")
        return True

    def validate_system_resources(self):
        """Validar recursos del sistema."""
        # Verificar memoria
        memory = psutil.virtual_memory()
        if memory.available < 1024 * 1024 * 1024:  # 1GB
            self.log_warning("Memoria disponible baja (< 1GB)")

        # Verificar espacio en disco
        disk = psutil.disk_usage("/")
        if disk.free < 5 * 1024 * 1024 * 1024:  # 5GB
            self.log_warning("Espacio en disco bajo (< 5GB)")

        self.log_success("Recursos del sistema verificados")
        return True

    async def validate_service_health(self):
        """Validar salud de servicios (si están ejecutándose)."""
        services = [
            ("APIGateway", "http://localhost:8000/health"),
            ("NotificationService", "http://localhost:8001/health"),
        ]

        async with httpx.AsyncClient(timeout=5.0) as client:
            for service_name, url in services:
                try:
                    response = await client.get(url)
                    if response.status_code == 200:
                        self.log_success(f"{service_name} está saludable")
                    else:
                        self.log_warning(
                            f"{service_name} responde con status {response.status_code}"
                        )
                except Exception:
                    self.log_info(
                        f"{service_name} no está ejecutándose (normal para validación pre-deployment)"
                    )

    def _command_available(self, command: str) -> bool:
        """Verificar si un comando está disponible."""
        return os.system(f"command -v {command} > /dev/null 2>&1") == 0

    def _port_in_use(self, port: int) -> bool:
        """Verificar si un puerto está en uso."""
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                return True
        return False

    async def run_validation(self) -> bool:
        """Ejecutar todas las validaciones."""
        print(f"🔍 Validando configuración para entorno: {self.environment}")
        print("=" * 60)

        validations = [
            ("Archivo de entorno", self.validate_environment_file),
            ("Dependencias Python", self.validate_python_dependencies),
            ("Configuración Docker", self.validate_docker_setup),
            ("Conectividad BD", self.validate_database_connectivity),
            ("Disponibilidad puertos", self.validate_port_availability),
            ("Recursos sistema", self.validate_system_resources),
        ]

        success_count = 0
        for name, validation_func in validations:
            print(f"\n📋 Validando: {name}")
            if validation_func():
                success_count += 1

        # Validación asíncrona
        print(f"\n📋 Validando: Salud de servicios")
        await self.validate_service_health()

        print("\n" + "=" * 60)
        print(f"📊 Resumen de validación:")
        print(f"   ✅ Exitosas: {success_count}/{len(validations)}")
        print(f"   ⚠️ Advertencias: {len(self.warnings)}")
        print(f"   ❌ Errores: {len(self.errors)}")

        if self.errors:
            print("\n❌ ERRORES ENCONTRADOS:")
            for error in self.errors:
                print(f"   - {error}")

        if self.warnings:
            print("\n⚠️ ADVERTENCIAS:")
            for warning in self.warnings:
                print(f"   - {warning}")

        is_valid = len(self.errors) == 0

        if is_valid:
            print("\n🎉 ¡Validación exitosa! El sistema está listo para deployment.")
        else:
            print("\n❌ Validación fallida. Corrija los errores antes del deployment.")

        return is_valid


async def main():
    """Función principal."""
    if len(sys.argv) != 2:
        print("Uso: validate_deployment.py <environment>")
        print("Entornos: development, testing, staging, production")
        sys.exit(1)

    environment = sys.argv[1]

    if environment not in ["development", "testing", "staging", "production"]:
        print(f"Error: Entorno inválido '{environment}'")
        print("Entornos válidos: development, testing, staging, production")
        sys.exit(1)

    validator = DeploymentValidator(environment)
    is_valid = await validator.run_validation()

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    asyncio.run(main())
