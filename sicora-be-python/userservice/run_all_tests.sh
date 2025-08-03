#!/bin/bash

echo "🔧 Ejecutando todos los tests del userservice..."
echo "Python: /home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/venv/bin/python"
echo "================================================"

# Usar el Python del venv padre que tiene todas las dependencias
PYTHON_CMD="/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/venv/bin/python"

# Ejecutar todos los tests
$PYTHON_CMD -m pytest tests/ -v --tb=short

echo "================================================"
echo "✅ Tests completados"
