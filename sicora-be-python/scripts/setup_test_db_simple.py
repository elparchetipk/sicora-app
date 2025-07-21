#!/usr/bin/env python3
"""
Script simplificado para configurar las bases de datos de prueba.
"""

import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import (
    text,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    Text,
    JSON,
)
from sqlalchemy.sql import func


async def create_test_databases():
    """Crear las bases de datos de prueba si no existen."""
    print("🚀 Configurando base de datos de prueba para SICORA Backend Python")

    # Configuración para conectar como superuser
    admin_engine = create_async_engine(
        "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/postgres",
        echo=False,
    )

    async with admin_engine.begin() as conn:
        # Verificar si existe la DB de test
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'sicora_test'")
        )
        if not result.fetchone():
            await conn.commit()
            await conn.execute(text("CREATE DATABASE sicora_test"))
            print("✅ Base de datos 'sicora_test' creada")
        else:
            print("ℹ️ Base de datos 'sicora_test' ya existe")

    await admin_engine.dispose()


async def create_tables():
    """Crear todas las tablas necesarias para los tests."""
    print("\n🔧 Creando tablas...")

    # Crear engine para la DB de test
    test_engine = create_async_engine(
        "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_test",
        echo=False,
    )

    metadata = MetaData()

    # Tabla para request logs del APIGateway
    request_logs = Table(
        "request_logs",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", String(50), nullable=True, index=True),
        Column("service_name", String(100), nullable=False, index=True),
        Column("endpoint", String(500), nullable=False),
        Column("method", String(10), nullable=False),
        Column("status_code", Integer, nullable=False),
        Column("response_time_ms", Float, nullable=False),
        Column("request_size_bytes", Integer, default=0),
        Column("response_size_bytes", Integer, default=0),
        Column("ip_address", String(45), nullable=False),
        Column("user_agent", Text, nullable=True),
        Column("timestamp", DateTime, default=func.now(), nullable=False, index=True),
        Column("status", String(20), nullable=False),
        Column("error_message", Text, nullable=True),
    )

    # Tabla para service health del APIGateway
    service_health = Table(
        "service_health",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("service_name", String(100), nullable=False, unique=True, index=True),
        Column("is_healthy", Boolean, default=True, nullable=False),
        Column("last_check", DateTime, default=func.now(), nullable=False),
        Column("response_time_ms", Float, nullable=True),
        Column("error_message", Text, nullable=True),
        Column("service_metadata", JSON, nullable=True),
    )

    # Tabla para notificaciones
    notifications = Table(
        "notifications",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", Integer, nullable=False, index=True),
        Column("title", String, nullable=False),
        Column("message", String, nullable=False),
        Column("type", String, nullable=False),
        Column("read_status", Boolean, default=False, nullable=False),
        Column("created_at", DateTime, default=func.now(), nullable=False),
    )

    # Crear todas las tablas
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        print("✅ Todas las tablas creadas exitosamente")

    await test_engine.dispose()


async def verify_setup():
    """Verificar que las tablas fueron creadas correctamente."""
    print("\n🔍 Verificando configuración...")

    test_engine = create_async_engine(
        "postgresql+asyncpg://sicora_user:sicora_password@localhost:5433/sicora_test",
        echo=False,
    )

    async with test_engine.begin() as conn:
        # Verificar todas las tablas
        result = await conn.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name IN ('request_logs', 'service_health', 'notifications')
                ORDER BY table_name
            """
            )
        )
        tables = [row[0] for row in result.fetchall()]

        print(f"✅ Tablas creadas: {tables}")

        expected_tables = ["notifications", "request_logs", "service_health"]
        if all(table in tables for table in expected_tables):
            print("\n🎉 ¡Configuración completada exitosamente!")
            print("Los tests de integración están listos para ejecutarse.")
            return True
        else:
            missing = set(expected_tables) - set(tables)
            print(f"\n❌ Faltan tablas: {missing}")
            return False

    await test_engine.dispose()


async def main():
    """Función principal."""
    try:
        await create_test_databases()
        await create_tables()
        success = await verify_setup()

        if not success:
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
