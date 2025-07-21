#!/usr/bin/env python3
"""
Script específico para probar conectividad de NotificationService
"""

import asyncio
import sys
import os

# Cambiar al directorio del servicio
service_path = "/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/notificationservice-template"
os.chdir(service_path)
sys.path.insert(0, service_path)


async def test_notification_db():
    """Probar conexión de NotificationService."""
    try:
        from app.infrastructure.database.database import engine, Base
        from app.infrastructure.database.models import NotificationModel
        from sqlalchemy import text

        print("🔌 Probando conexión NotificationService...")

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("✅ NotificationService: Conexión exitosa y tablas creadas")

        # Verificar que la tabla fue creada con la estructura correcta
        async with engine.begin() as conn:
            result = await conn.execute(
                text(
                    "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'notifications'"
                )
            )
            columns = result.fetchall()
            print(f"📋 Estructura de tabla 'notifications': {len(columns)} columnas")
            for col in columns:
                print(f"   - {col[0]}: {col[1]}")

        return True

    except Exception as e:
        print(f"❌ NotificationService: Error de conexión - {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Ejecutar prueba de NotificationService."""
    print("🧪 PRUEBA ESPECÍFICA DE NOTIFICATIONSERVICE")
    print("=" * 50)

    result = await test_notification_db()

    print()
    if result:
        print("✅ NotificationService está listo para usar base de datos")
        return 0
    else:
        print("❌ NotificationService falló la conexión")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
