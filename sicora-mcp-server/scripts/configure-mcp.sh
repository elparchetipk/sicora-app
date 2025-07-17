#!/bin/bash

# Configuración del servidor MCP SICORA con pnpm
# Script para configurar automáticamente el servidor MCP

set -e

echo "🚀 Configurando servidor MCP SICORA con pnpm..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si pnpm está instalado
if ! command -v pnpm &> /dev/null; then
    log_error "pnpm no está instalado. Instalando pnpm..."
    npm install -g pnpm
    log_info "pnpm instalado correctamente"
fi

# Verificar si estamos en el directorio correcto
if [ ! -f "package.json" ]; then
    log_error "No se encontró package.json. Ejecute este script desde el directorio sicora-mcp-server"
    exit 1
fi

# Instalar dependencias
log_info "Instalando dependencias con pnpm..."
pnpm install

# Compilar el proyecto
log_info "Compilando el proyecto TypeScript..."
pnpm run build

# Verificar que la compilación fue exitosa
if [ ! -f "dist/index.js" ]; then
    log_error "La compilación falló. No se encontró dist/index.js"
    exit 1
fi

# Probar el servidor
log_info "Probando el servidor MCP..."
timeout 5s pnpm run start || log_warn "El servidor se ejecutó por 5 segundos (test básico)"

# Configurar VS Code
PROJECT_ROOT=$(dirname "$(pwd)")
VSCODE_DIR="$PROJECT_ROOT/.vscode"
MCP_CONFIG="$VSCODE_DIR/mcp.json"

log_info "Configurando VS Code MCP..."

# Crear directorio .vscode si no existe
mkdir -p "$VSCODE_DIR"

# Generar configuración MCP
cat > "$MCP_CONFIG" << EOF
{
  "servers": {
    "sicora-mcp": {
      "command": "pnpm",
      "args": ["--dir", "sicora-mcp-server", "run", "start"],
      "env": {
        "NODE_ENV": "production",
        "SICORA_PROJECT_ROOT": "$PROJECT_ROOT",
        "SICORA_FRONTEND_PATH": "$PROJECT_ROOT/sicora-app-fe",
        "SICORA_BACKEND_PATH": "$PROJECT_ROOT/sicora-be-go"
      }
    }
  }
}
EOF

log_info "Configuración MCP guardada en: $MCP_CONFIG"

# Mostrar información final
echo ""
echo "✅ Configuración completada exitosamente"
echo ""
echo "📋 Comandos disponibles:"
echo "  pnpm run start    - Iniciar servidor MCP"
echo "  pnpm run dev      - Iniciar en modo desarrollo"
echo "  pnpm run build    - Compilar TypeScript"
echo "  pnpm run watch    - Modo desarrollo con recarga automática"
echo ""
echo "🔧 Para usar el servidor MCP:"
echo "  1. Reinicia VS Code"
echo "  2. El servidor MCP estará disponible automáticamente"
echo "  3. Usa Ctrl+Shift+P -> 'MCP: Connect to Server' si es necesario"
echo ""
echo "📁 Rutas configuradas:"
echo "  - Proyecto: $PROJECT_ROOT"
echo "  - Frontend: $PROJECT_ROOT/sicora-app-fe"
echo "  - Backend: $PROJECT_ROOT/sicora-be-go"
echo ""
