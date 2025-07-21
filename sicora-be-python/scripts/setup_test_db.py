#!/usr/bin/env python3
"""
Script para configurar las bases de datos de prueba.
Crea las tablas necesarias para los tests de integración.
"""

import asyncio
import os
import sys
from pathlib import Path

# Añadir el directorio root al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "apigateway"))
sys.path.insert(0, str(project_root / "notificationservice-template"))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def create_test_databases():
    """Crear las bases de datos de prueba si no existen."""

    # Configuración para conectar como superuser
    admin_engine = create_async_engine(
        "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/postgres",
        echo=True,
    )

    # Crear base de datos de prueba
    async with admin_engine.begin() as conn:
        # Verificar si existe la DB de test
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'sicora_test'")
        )
        if not result.fetchone():
            # PostgreSQL no permite CREATE DATABASE en transacciones,
            # necesitamos commitear la transacción actual
            await conn.commit()
            await conn.execute(text("CREATE DATABASE sicora_test"))
            print("✅ Base de datos 'sicora_test' creada")
        else:
            print("ℹ️ Base de datos 'sicora_test' ya existe")

    await admin_engine.dispose()


async def setup_apigateway_tables():
    """Configurar las tablas del APIGateway."""
    print("\n🔧 Configurando tablas del APIGateway...")

    # Cambiar directorio al APIGateway
    original_dir = os.getcwd()
    os.chdir(project_root / "apigateway")

    try:
        # Importar modelos del APIGateway
        from app.infrastructure.database.database import Base
        from app.infrastructure.database.models import (
            RequestLogModel,
            ServiceHealthModel,
        )

        # Crear engine para la DB de test
        test_engine = create_async_engine(
            "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_test",
            echo=True,
        )

        # Crear tablas
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tablas del APIGateway creadas")

        await test_engine.dispose()

    finally:
        os.chdir(original_dir)


async def setup_notification_tables():
    """Configurar las tablas del NotificationService."""
    print("\n📱 Configurando tablas del NotificationService...")

    # Cambiar el directorio de trabajo temporalmente
    original_dir = os.getcwd()
    os.chdir(project_root / "notificationservice-template")

    try:
        # Importar modelos del NotificationService
        from app.infrastructure.database.database import Base
        from app.infrastructure.database.models import NotificationModel

        # Crear engine para la DB de test
        test_engine = create_async_engine(
            "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_test",
            echo=True,
        )

        # Crear tablas
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tablas del NotificationService creadas")

        await test_engine.dispose()

    finally:
        os.chdir(original_dir)


async def verify_setup():
    """Verificar que las tablas fueron creadas correctamente."""
    print("\n🔍 Verificando configuración...")

    test_engine = create_async_engine(
        "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_test",
        echo=False,
    )

    async with test_engine.begin() as conn:
        # Verificar tablas del APIGateway
        result = await conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('request_logs', 'service_health')"
            )
        )
        api_tables = [row[0] for row in result.fetchall()]

        # Verificar tablas del NotificationService
        result = await conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'notifications'"
            )
        )
        notification_tables = [row[0] for row in result.fetchall()]

        print(f"✅ Tablas del APIGateway: {api_tables}")
        print(f"✅ Tablas del NotificationService: {notification_tables}")

        if (
            "request_logs" in api_tables
            and "service_health" in api_tables
            and "notifications" in notification_tables
        ):
            print(
                "\n🎉 Configuración de base de datos de prueba completada exitosamente!"
            )
            return True
        else:
            print("\n❌ Faltan algunas tablas")
            return False

    await test_engine.dispose()


async def main():
    """Función principal."""
    print("🚀 Configurando base de datos de prueba para SICORA Backend Python")

    try:
        await create_test_databases()
        await setup_apigateway_tables()
        await setup_notification_tables()
        success = await verify_setup()

        if success:
            print(
                "\n✅ Configuración completada. Los tests de integración están listos para ejecutarse."
            )
        else:
            print("\n❌ Error en la configuración. Revisa los logs para más detalles.")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
