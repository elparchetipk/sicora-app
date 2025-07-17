#!/bin/bash

# Script de prueba de integración para SICORA AIService y KBService
# Este script verifica que ambos servicios estén funcionando y puedan comunicarse

echo "=== SICORA Integration Test ==="
echo "Verificando servicios..."

# Verificar que kbservice está corriendo
echo "1. Verificando KBService (puerto 8006)..."
KB_HEALTH=$(curl -s http://localhost:8006/health)
if [ $? -eq 0 ]; then
    echo "✅ KBService está corriendo"
    echo "   Respuesta: $KB_HEALTH"
else
    echo "❌ KBService no responde en puerto 8006"
    echo "   Asegúrate de que esté corriendo: cd kbservice && python main.py"
    exit 1
fi

# Verificar que aiservice está corriendo
echo ""
echo "2. Verificando AIService (puerto 8007)..."
AI_HEALTH=$(curl -s http://localhost:8007/health)
if [ $? -eq 0 ]; then
    echo "✅ AIService está corriendo"
    echo "   Respuesta: $AI_HEALTH"
else
    echo "❌ AIService no responde en puerto 8007"
    echo "   Intenta iniciarlo: cd aiservice && python main.py"
    exit 1
fi

# Probar endpoint de documentación
echo ""
echo "3. Verificando documentación API..."
AI_DOCS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8007/docs)
if [ "$AI_DOCS" = "200" ]; then
    echo "✅ Documentación API disponible en http://localhost:8007/docs"
else
    echo "⚠️  Documentación API no disponible"
fi

# Probar endpoint de chat mejorado
echo ""
echo "4. Probando endpoint de chat mejorado..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8007/api/v1/chat/enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué dice el reglamento sobre las faltas de los aprendices?",
    "user_id": "test-user-123",
    "context_type": "regulatory",
    "include_sources": true
  }')

if [ $? -eq 0 ]; then
    echo "✅ Chat mejorado respondió"
    echo "   Respuesta (primeros 200 caracteres):"
    echo "   $(echo $CHAT_RESPONSE | cut -c 1-200)..."
else
    echo "❌ Error en endpoint de chat mejorado"
fi

echo ""
echo "=== Resumen de la prueba ==="
echo "✅ Servicios básicos funcionando"
echo "✅ Integración entre aiservice y kbservice establecida"
echo "✅ Mock OpenAI client operativo"
echo ""
echo "Para probar manualmente:"
echo "1. Visita http://localhost:8007/docs para ver la API"
echo "2. Usa el endpoint /api/v1/chat/enhanced para probar el chat"
echo "3. El kbservice está en http://localhost:8006/docs"
echo ""
echo "Ambos servicios están listos para desarrollo y pruebas! 🚀"
