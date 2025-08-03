#!/bin/bash

# Script para ejecutar todos los tests del userservice

echo "🧪 Ejecutando tests del UserService..."
echo "📍 Directorio: $(pwd)"

# Activar el entorno virtual
source venv/bin/activate

# Verificar pytest
echo "🔍 Verificando pytest..."
python -c "import pytest; print(f'✅ pytest {pytest.__version__} disponible')"

# Ejecutar tests por categorías
echo ""
echo "🔬 === TESTS UNITARIOS ==="
python -m pytest tests/unit/ -v --tb=short

echo ""
echo "🔗 === TESTS DE INTEGRACIÓN ==="
python -m pytest tests/integration/ -v --tb=short

echo ""
echo "🚀 === TESTS E2E ==="
python -m pytest tests/e2e/ -v --tb=short

echo ""
echo "⚙️ === TESTS DE SETUP ==="
python -m pytest tests/setup/ -v --tb=short

echo ""
echo "🐛 === TESTS DE DEBUG ==="
python -m pytest tests/debug/ -v --tb=short

echo ""
echo "📊 === RESUMEN COMPLETO ==="
python -m pytest tests/ --tb=short --no-header -q

echo ""
echo "✅ Tests completados!"
