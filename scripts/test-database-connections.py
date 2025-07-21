#!/usr/bin/env python3
"""
Script de prueba de conectividad de base de datos para APIGateway y NotificationService
"""

import asyncio
import sys
import os

# Añadir paths para imports
sys.path.append("/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/apigateway")
sys.path.append(
    "/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/notificationservice-template"
)


async def test_apigateway_db():
    """Probar conexión de APIGateway."""
    try:
        os.chdir(
            "/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/apigateway"
        )

        from app.infrastructure.database.database import engine, Base
        from app.infrastructure.database.models import (
            RequestLogModel,
            ServiceHealthModel,
        )

        print("🔌 Probando conexión APIGateway...")

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("✅ APIGateway: Conexión exitosa y tablas creadas")
        return True

    except Exception as e:
        print(f"❌ APIGateway: Error de conexión - {e}")
        return False


async def test_notification_db():
    """Probar conexión de NotificationService."""
    try:
        # Cambiar directorio
        original_cwd = os.getcwd()
        os.chdir(
            "/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/notificationservice-template"
        )

        # Limpiar módulos anteriores del cache
        modules_to_remove = []
        for module_name in sys.modules:
            if module_name.startswith("app."):
                modules_to_remove.append(module_name)

        for module_name in modules_to_remove:
            del sys.modules[module_name]

        # Limpiar path y añadir el correcto
        for path in list(sys.path):
            if "apigateway" in path:
                sys.path.remove(path)

        notification_path = "/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/notificationservice-template"
        if notification_path not in sys.path:
            sys.path.insert(0, notification_path)

        # Importar con path correcto
        from app.infrastructure.database.database import engine, Base
        from app.infrastructure.database.models import NotificationModel

        print("🔌 Probando conexión NotificationService...")

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("✅ NotificationService: Conexión exitosa y tablas creadas")

        # Restaurar directorio
        os.chdir(original_cwd)
        return True

    except Exception as e:
        print(f"❌ NotificationService: Error de conexión - {e}")
        if "original_cwd" in locals():
            os.chdir(original_cwd)
        return False


async def main():
    """Ejecutar todas las pruebas."""
    print("🧪 PRUEBAS DE CONECTIVIDAD DE BASE DE DATOS")
    print("=" * 50)

    results = []

    # Probar APIGateway
    results.append(await test_apigateway_db())

    print()

    # Probar NotificationService
    results.append(await test_notification_db())

    print()
    print("📊 RESUMEN:")

    if all(results):
        print("✅ Todas las conexiones funcionan correctamente")
        print("🚀 Los servicios están listos para usar base de datos")
        return 0
    else:
        print("❌ Algunas conexiones fallaron")
        print("🔧 Revisar configuración de base de datos")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
