#!/bin/bash
# Script de desarrollo para ProjectEval Service

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "⚠️ No se encontró entorno virtual. Creando..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "🚀 Iniciando ProjectEval Service en modo desarrollo..."
echo "📡 URL: http://localhost:8007"
echo "📚 Docs: http://localhost:8007/docs"
echo "🔗 Redoc: http://localhost:8007/redoc"
echo ""
echo "🛑 Para detener: Ctrl+C"
echo ""

# Ejecutar servicio con recarga automática
uvicorn app.main:app --host 0.0.0.0 --port 8007 --reload
