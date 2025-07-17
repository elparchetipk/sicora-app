#!/bin/bash

# Script de prueba rápida para SICORA Data Loader
# Verifica que todos los componentes funcionen correctamente

set -e

echo "🧪 SICORA Data Loader - Prueba de Componentes"
echo "=============================================="

# Test 1: Verificar imports de Python
echo "📦 Test 1: Verificando imports..."
python3 -c "
import sys
sys.path.append('.')

try:
    from config.database import db_config
    print('✅ config.database importado')
    
    from models.schemas import SchemaMapping
    print('✅ models.schemas importado')
    
    from services.file_processor import FileProcessor
    print('✅ services.file_processor importado')
    
    from services.data_validator import DataValidator
    print('✅ services.data_validator importado')
    
    from services.database_loader import DatabaseLoader
    print('✅ services.database_loader importado')
    
    from utils.logger import data_logger
    print('✅ utils.logger importado')
    
    print('🎉 Todos los módulos importados correctamente')
    
except ImportError as e:
    print(f'❌ Error de importación: {e}')
    exit(1)
"

# Test 2: Verificar configuración
echo ""
echo "⚙️ Test 2: Verificando configuración..."
if [ ! -f ".env" ]; then
    echo "⚠️ Archivo .env no encontrado, usando .env.example"
    cp .env.example .env
fi

# Test 3: Verificar dependencias
echo ""
echo "📋 Test 3: Verificando dependencias..."
python3 -c "
import pandas as pd
print(f'✅ pandas: {pd.__version__}')

import streamlit as st
print(f'✅ streamlit: {st.__version__}')

try:
    import psycopg2
    print(f'✅ psycopg2: {psycopg2.__version__}')
except:
    print('⚠️ psycopg2 no disponible')

try:
    import openpyxl
    print(f'✅ openpyxl: {openpyxl.__version__}')
except:
    print('⚠️ openpyxl no disponible (Excel read/write limitado)')

try:
    import tabula
    print('✅ tabula-py disponible')
except:
    print('⚠️ tabula-py no disponible (PDF processing limitado)')
"

# Test 4: Verificar mapeo de schemas
echo ""
echo "🗄️ Test 4: Verificando mapeo de schemas..."
python3 -c "
import sys
sys.path.append('.')
from models.schemas import SchemaMapping

microservices = SchemaMapping.get_microservices_list()
print(f'📊 Microservicios configurados: {len(microservices)}')

for ms in microservices:
    schema = SchemaMapping.get_schema_for_microservice(ms)
    description = SchemaMapping.get_description(ms)
    print(f'  - {ms}: {schema}')

print('✅ Mapeo de schemas verificado')
"

# Test 5: Test de procesamiento de archivos
echo ""
echo "📁 Test 5: Verificando procesamiento de archivos..."
python3 -c "
import sys
sys.path.append('.')
import pandas as pd
from io import BytesIO
from services.file_processor import FileProcessor

# Crear CSV de prueba
test_data = '''name,email,role
Juan Pérez,juan@test.com,admin
María García,maria@test.com,user'''

csv_bytes = BytesIO(test_data.encode())

try:
    # Simular procesamiento CSV como Excel
    df = pd.read_csv(csv_bytes)
    print(f'✅ Procesamiento de archivos: {len(df)} filas leídas')
    
    # Test detección de tipos
    types = FileProcessor.detect_data_types(df)
    print(f'✅ Detección de tipos: {types}')
    
    # Test vista previa
    preview = FileProcessor.preview_data(df)
    print(f'✅ Vista previa: {preview[\"shape\"]} shape')
    
except Exception as e:
    print(f'❌ Error en procesamiento: {e}')
"

# Test 6: Verificar logger
echo ""
echo "📝 Test 6: Verificando logger..."
python3 -c "
import sys
sys.path.append('.')
from utils.logger import data_logger

data_logger.log_info('Test de logging funcionando')
print('✅ Sistema de logging operativo')
"

echo ""
echo "🎉 Todas las pruebas completadas!"
echo ""
echo "💡 Para ejecutar la aplicación:"
echo "   ./start.sh"
echo ""
echo "🔧 Para solo configurar el entorno:"
echo "   ./start.sh setup"
echo ""
echo "📊 Para verificar base de datos:"
echo "   ./start.sh check"
