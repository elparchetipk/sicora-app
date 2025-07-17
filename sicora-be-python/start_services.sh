#!/bin/bash

# Script para iniciar ambos servicios de SICORA
# Uso: ./start_services.sh

echo "=== Iniciando servicios SICORA ==="

# Verificar que estamos en el directorio correcto
if [ ! -d "kbservice" ] || [ ! -d "aiservice" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio sicora-be-python"
    exit 1
fi

# Verificar entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Activando entorno virtual..."
    source venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "❌ Error activando entorno virtual"
        exit 1
    fi
fi

echo "✅ Entorno virtual activo: $VIRTUAL_ENV"

# Función para matar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    if [ ! -z "$KBSERVICE_PID" ]; then
        kill $KBSERVICE_PID 2>/dev/null
        echo "   KBService detenido"
    fi
    if [ ! -z "$AISERVICE_PID" ]; then
        kill $AISERVICE_PID 2>/dev/null
        echo "   AIService detenido"
    fi
    echo "👋 Servicios detenidos"
    exit 0
}

# Configurar trap para cleanup
trap cleanup SIGINT SIGTERM

# Iniciar KBService
echo ""
echo "🚀 Iniciando KBService (puerto 8006)..."
cd kbservice
python main.py &
KBSERVICE_PID=$!
cd ..

# Esperar un poco para que KBService inicie
sleep 3

# Verificar que KBService está corriendo
if kill -0 $KBSERVICE_PID 2>/dev/null; then
    echo "✅ KBService iniciado (PID: $KBSERVICE_PID)"
else
    echo "❌ Error iniciando KBService"
    exit 1
fi

# Iniciar AIService
echo ""
echo "🚀 Iniciando AIService (puerto 8007)..."
cd aiservice
python main.py &
AISERVICE_PID=$!
cd ..

# Esperar un poco para que AIService inicie
sleep 3

# Verificar que AIService está corriendo
if kill -0 $AISERVICE_PID 2>/dev/null; then
    echo "✅ AIService iniciado (PID: $AISERVICE_PID)"
else
    echo "❌ Error iniciando AIService"
    kill $KBSERVICE_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Ambos servicios iniciados exitosamente!"
echo ""
echo "📊 Estado de servicios:"
echo "   • KBService:  http://localhost:8006 (PID: $KBSERVICE_PID)"
echo "   • AIService:  http://localhost:8007 (PID: $AISERVICE_PID)"
echo ""
echo "📖 Documentación API:"
echo "   • KBService:  http://localhost:8006/docs"
echo "   • AIService:  http://localhost:8007/docs"
echo ""
echo "⚡ Para probar la integración:"
echo "   chmod +x test_integration_simple.sh && ./test_integration_simple.sh"
echo ""
echo "🛑 Presiona Ctrl+C para detener ambos servicios"

# Mantener el script corriendo y mostrar logs
while true; do
    sleep 1
    # Verificar que ambos procesos siguen corriendo
    if ! kill -0 $KBSERVICE_PID 2>/dev/null; then
        echo "❌ KBService se detuvo inesperadamente"
        cleanup
    fi
    if ! kill -0 $AISERVICE_PID 2>/dev/null; then
        echo "❌ AIService se detuvo inesperadamente"
        cleanup
    fi
done
