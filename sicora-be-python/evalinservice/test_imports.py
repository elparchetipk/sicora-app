#!/usr/bin/env python3
"""
Script para probar las importaciones del EvalinService sin depender de PostgreSQL.
"""

import os
import sys

# Configurar SQLite para testing
os.environ["DATABASE_URL"] = "sqlite:///test.db"
os.environ["USER_SERVICE_URL"] = "http://localhost:8000"
os.environ["SCHEDULE_SERVICE_URL"] = "http://localhost:8001"
os.environ["NOTIFICATION_SERVICE_URL"] = "http://localhost:8002"

def test_imports():
    """Probar las importaciones principales del servicio."""
    
    print("🔧 Configurando variables de entorno para testing...")
    print(f"DATABASE_URL: {os.environ['DATABASE_URL']}")
    
    try:
        print("\n1️⃣ Probando importación de database...")
        from app.infrastructure.database.database import SessionLocal, Base
        print("✅ Database importado correctamente")
        
        print("\n2️⃣ Probando importación de modelos...")
        import app.infrastructure.models
        print("✅ Modelos importados correctamente")
        
        print("\n3️⃣ Probando importación de repositorios...")
        import app.infrastructure.repositories
        print("✅ Repositorios importados correctamente")
        
        print("\n4️⃣ Probando importación de use cases...")
        import app.application.use_cases
        print("✅ Use cases importados correctamente")
        
        print("\n5️⃣ Probando importación de schemas...")
        import app.presentation.schemas
        print("✅ Schemas importados correctamente")
        
        print("\n6️⃣ Probando importación de container...")
        from app.presentation.dependencies.container import container
        print("✅ Container importado correctamente")
        
        print("\n7️⃣ Probando importación de routers...")
        from app.presentation.routers.evaluation_router import router as eval_router
        from app.presentation.routers.question_router import router as question_router
        from app.presentation.routers.questionnaire_router import router as questionnaire_router
        from app.presentation.routers.period_router import router as period_router
        print("✅ Routers importados correctamente")
        
        print("\n8️⃣ Probando importación de main app...")
        from main import app
        print("✅ Main app importada correctamente")
        
        print("\n🎯 ¡Todas las importaciones exitosas!")
        print(f"📋 Rutas disponibles: {len(app.routes)} rutas")
        
        # Listar algunas rutas para verificar
        print("\n📍 Algunas rutas disponibles:")
        for route in app.routes[:10]:  # Mostrar las primeras 10 rutas
            if hasattr(route, 'path'):
                print(f"  - {route.path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante las importaciones: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
