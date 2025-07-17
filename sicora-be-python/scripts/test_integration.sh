#!/bin/bash

# Script para probar la integración entre aiservice y kbservice
# Test integration between aiservice and kbservice

echo "🚀 Iniciando prueba de integración aiservice-kbservice"
echo "=================================================="

# Configurar entorno virtual
echo "📦 Activando entorno virtual..."
source /home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/venv/bin/activate

# Verificar servicios corriendo
echo "🔍 Verificando servicios corriendo..."
ps aux | grep python | grep -E "(kbservice|aiservice)" || echo "No hay servicios Python corriendo"

# Probar kbservice health check
echo "🏥 Probando health check de kbservice..."
curl -s http://localhost:8006/health || echo "❌ kbservice no responde"

# Probar aiservice health check
echo "🏥 Probando health check de aiservice..."
curl -s http://localhost:8007/health || echo "❌ aiservice no responde"

# Probar endpoints de kbservice
echo "📚 Probando endpoints de kbservice..."
curl -s http://localhost:8006/api/v1/knowledge/search?query=reglamento || echo "❌ No se puede acceder a búsqueda de kbservice"

# Probar chat mejorado de aiservice
echo "🤖 Probando chat mejorado de aiservice..."
curl -X POST -H "Content-Type: application/json" \
  -d '{"message": "¿Qué es el reglamento del aprendiz?", "context": {"user_role": "student"}}' \
  http://localhost:8007/api/v1/chat/enhanced || echo "❌ No se puede acceder al chat mejorado"

echo "✅ Prueba de integración completada"
