#!/usr/bin/env python3
"""
Script básico para validar la configuración del EvalinService.
Verifica que se puede importar la aplicación y que los endpoints básicos respondan.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Probar que se pueden importar los módulos principales."""
    print("Testing imports...")
    
    try:
        from main import app
        print("✓ Main app import successful")
    except Exception as e:
        print(f"✗ Main app import failed: {e}")
        return False
    
    try:
        from app.domain.entities.question import Question
        print("✓ Domain entities import successful")
    except Exception as e:
        print(f"✗ Domain entities import failed: {e}")
        return False
    
    try:
        from app.application.use_cases.create_question_use_case import CreateQuestionUseCase
        print("✓ Use cases import successful")
    except Exception as e:
        print(f"✗ Use cases import failed: {e}")
        return False
    
    try:
        from app.infrastructure.models.question_model import QuestionModel
        print("✓ Infrastructure models import successful")
    except Exception as e:
        print(f"✗ Infrastructure models import failed: {e}")
        return False
    
    try:
        from app.presentation.routers.question_router import router
        print("✓ Presentation routers import successful")
    except Exception as e:
        print(f"✗ Presentation routers import failed: {e}")
        return False
    
    return True

def test_app_creation():
    """Probar que se puede crear la aplicación FastAPI."""
    print("\nTesting app creation...")
    
    try:
        from main import app
        
        # Verificar que la app tiene los routers
        routes = [route.path for route in app.routes]
        expected_routes = ["/api/v1/questions", "/api/v1/questionnaires", "/api/v1/periods"]
        
        for expected_route in expected_routes:
            if any(expected_route in route for route in routes):
                print(f"✓ Route {expected_route} found")
            else:
                print(f"✗ Route {expected_route} not found")
                return False
        
        print("✓ App creation successful")
        return True
        
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        return False

def test_database_models():
    """Probar que los modelos de base de datos están bien definidos."""
    print("\nTesting database models...")
    
    try:
        from app.infrastructure.database.database import Base
        from app.infrastructure.models import QuestionModel, QuestionnaireModel, EvaluationPeriodModel, EvaluationModel
        
        # Verificar que los modelos están registrados
        tables = Base.metadata.tables.keys()
        expected_tables = ['questions', 'questionnaires', 'evaluation_periods', 'evaluations']
        
        for expected_table in expected_tables:
            if expected_table in tables:
                print(f"✓ Table {expected_table} defined")
            else:
                print(f"✗ Table {expected_table} not defined")
                return False
        
        print("✓ Database models validation successful")
        return True
        
    except Exception as e:
        print(f"✗ Database models validation failed: {e}")
        return False

def main():
    """Ejecutar todas las pruebas de validación."""
    print("🚀 EvalinService Setup Validation")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_creation,
        test_database_models
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    success_count = sum(results)
    total_count = len(results)
    
    if success_count == total_count:
        print(f"✅ All tests passed! ({success_count}/{total_count})")
        print("🎉 EvalinService is ready to run!")
        return 0
    else:
        print(f"❌ Some tests failed ({success_count}/{total_count})")
        print("🔧 Please fix the issues before running the service.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)