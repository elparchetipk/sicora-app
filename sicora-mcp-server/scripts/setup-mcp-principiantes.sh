#!/bin/bash

# Script interactivo para configurar y usar MCP por primera vez
# SICORA - Sistema de Información de Coordinación Académica

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

log_success() {
    echo -e "${CYAN}[SUCCESS]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}[PASO]${NC} $1"
}

# Función para pausar y esperar input del usuario
pause_for_user() {
    echo -e "${BLUE}Presiona Enter para continuar...${NC}"
    read
}

# Mostrar bienvenida
show_welcome() {
    clear
    echo -e "${CYAN}===========================================${NC}"
    echo -e "${CYAN}🤖 CONFIGURACIÓN MCP SICORA - PRINCIPIANTES${NC}"
    echo -e "${CYAN}===========================================${NC}"
    echo ""
    echo -e "${GREEN}¡Bienvenido a la configuración de MCP!${NC}"
    echo ""
    echo "MCP (Model Context Protocol) te permitirá tener un asistente de IA"
    echo "especializado en tu proyecto SICORA con herramientas específicas."
    echo ""
    echo -e "${YELLOW}¿Qué haremos hoy?${NC}"
    echo "1. Verificar que todo esté instalado correctamente"
    echo "2. Configurar el servidor MCP"
    echo "3. Conectar con VS Code"
    echo "4. Hacer tu primera prueba"
    echo ""
    pause_for_user
}

# Verificar prerequisitos
check_prerequisites() {
    log_step "1/5 - Verificando prerequisitos..."
    
    # Verificar Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_info "✅ Node.js encontrado: $NODE_VERSION"
    else
        log_error "❌ Node.js no encontrado. Por favor instala Node.js >= 18.0.0"
        exit 1
    fi
    
    # Verificar pnpm
    if command -v pnpm &> /dev/null; then
        PNPM_VERSION=$(pnpm --version)
        log_info "✅ pnpm encontrado: $PNPM_VERSION"
    else
        log_warn "⚠️  pnpm no encontrado. Instalando..."
        npm install -g pnpm
        log_success "✅ pnpm instalado correctamente"
    fi
    
    # Verificar VS Code
    if command -v code &> /dev/null; then
        log_info "✅ VS Code encontrado"
    else
        log_warn "⚠️  VS Code no encontrado en PATH. Asegúrate de tenerlo instalado."
    fi
    
    # Verificar directorio del proyecto
    if [ -f "package.json" ]; then
        log_info "✅ Estás en el directorio correcto del servidor MCP"
    else
        log_error "❌ No se encontró package.json. Ejecuta este script desde sicora-mcp-server/"
        exit 1
    fi
    
    log_success "✅ Todos los prerequisitos están listos"
    pause_for_user
}

# Configurar el servidor MCP
setup_mcp_server() {
    log_step "2/5 - Configurando servidor MCP..."
    
    log_info "Instalando dependencias con pnpm..."
    pnpm install
    
    log_info "Compilando el servidor MCP..."
    pnpm run build
    
    log_info "Verificando que el servidor compile correctamente..."
    if [ -f "dist/index.js" ]; then
        log_success "✅ Servidor MCP compilado correctamente"
    else
        log_error "❌ Error al compilar el servidor MCP"
        exit 1
    fi
    
    log_success "✅ Servidor MCP configurado correctamente"
    pause_for_user
}

# Configurar VS Code
setup_vscode() {
    log_step "3/5 - Configurando VS Code..."
    
    # Verificar archivo de configuración MCP
    MCP_CONFIG="../.vscode/mcp.json"
    if [ -f "$MCP_CONFIG" ]; then
        log_info "✅ Archivo de configuración MCP encontrado"
        log_info "Contenido de la configuración:"
        echo -e "${BLUE}$(cat $MCP_CONFIG)${NC}"
    else
        log_error "❌ No se encontró .vscode/mcp.json"
        log_info "Creando configuración MCP..."
        
        mkdir -p ../.vscode
        cat > "$MCP_CONFIG" << EOF
{
  "servers": {
    "sicora-mcp": {
      "command": "pnpm",
      "args": ["--dir", "sicora-mcp-server", "run", "start"],
      "env": {
        "NODE_ENV": "production",
        "SICORA_PROJECT_ROOT": "$(pwd)/..",
        "SICORA_FRONTEND_PATH": "$(pwd)/../sicora-app-fe",
        "SICORA_BACKEND_PATH": "$(pwd)/../sicora-be-go"
      }
    }
  }
}
EOF
        log_success "✅ Configuración MCP creada"
    fi
    
    log_warn "⚠️  IMPORTANTE: Necesitas reiniciar VS Code para que detecte la configuración MCP"
    echo ""
    echo -e "${YELLOW}Por favor:${NC}"
    echo "1. Cierra VS Code completamente"
    echo "2. Abre VS Code desde el directorio del proyecto"
    echo "3. Verifica que GitHub Copilot esté instalado"
    echo ""
    pause_for_user
}

# Iniciar el servidor MCP
start_mcp_server() {
    log_step "4/5 - Iniciando servidor MCP..."
    
    log_info "Iniciando servidor MCP en modo background..."
    log_warn "El servidor se ejecutará en segundo plano"
    
    # Verificar si ya hay un servidor ejecutándose
    if pgrep -f "sicora-mcp-server" > /dev/null; then
        log_info "Ya hay un servidor MCP ejecutándose"
        log_info "Deteniéndolo para reiniciar..."
        pkill -f "sicora-mcp-server" || true
        sleep 2
    fi
    
    # Iniciar servidor
    log_info "Iniciando servidor MCP..."
    pnpm start &
    SERVER_PID=$!
    
    # Esperar un poco para que inicie
    sleep 3
    
    # Verificar que esté ejecutándose
    if kill -0 $SERVER_PID 2>/dev/null; then
        log_success "✅ Servidor MCP iniciado correctamente (PID: $SERVER_PID)"
        echo $SERVER_PID > .mcp_server_pid
    else
        log_error "❌ Error al iniciar el servidor MCP"
        exit 1
    fi
    
    log_success "✅ Servidor MCP ejecutándose en background"
    pause_for_user
}

# Hacer primera prueba
first_test() {
    log_step "5/5 - Primera prueba de MCP..."
    
    echo -e "${CYAN}🎉 ¡Todo listo! Ahora puedes usar MCP${NC}"
    echo ""
    echo -e "${GREEN}¿Cómo usar MCP?${NC}"
    echo ""
    echo "1. Abre VS Code (si no está abierto)"
    echo "2. Abre el chat de GitHub Copilot"
    echo "3. Haz preguntas específicas sobre SICORA"
    echo ""
    echo -e "${YELLOW}Ejemplos de preguntas:${NC}"
    echo "• '¿Cuál es el estado actual del proyecto SICORA?'"
    echo "• 'Necesito un componente React para mostrar usuarios'"
    echo "• '¿Cómo está la integración frontend-backend?'"
    echo "• 'Genera un handler de Go para autenticación'"
    echo ""
    echo -e "${BLUE}Herramientas MCP disponibles:${NC}"
    echo "• sicora-analyze - Análisis del proyecto"
    echo "• sicora-generate - Generación de código"
    echo "• sicora-integrate - Verificación de integración"
    echo "• sicora-test - Gestión de pruebas"
    echo "• sicora-document - Actualización de documentación"
    echo ""
    echo -e "${PURPLE}Estado del servidor:${NC}"
    pnpm run mcp:status
    echo ""
    echo -e "${GREEN}¡Listo para usar MCP! 🚀${NC}"
}

# Mostrar información de ayuda
show_help() {
    echo -e "${CYAN}Ayuda - Script de configuración MCP${NC}"
    echo ""
    echo "Uso: $0 [opción]"
    echo ""
    echo "Opciones:"
    echo "  setup    - Configuración completa paso a paso"
    echo "  check    - Solo verificar prerequisitos"
    echo "  server   - Solo configurar servidor MCP"
    echo "  vscode   - Solo configurar VS Code"
    echo "  start    - Solo iniciar servidor MCP"
    echo "  test     - Solo hacer prueba"
    echo "  help     - Mostrar esta ayuda"
    echo ""
    echo "Sin opciones: Ejecuta configuración completa"
}

# Función principal
main() {
    case "${1:-setup}" in
        "setup")
            show_welcome
            check_prerequisites
            setup_mcp_server
            setup_vscode
            start_mcp_server
            first_test
            ;;
        "check")
            check_prerequisites
            ;;
        "server")
            setup_mcp_server
            ;;
        "vscode")
            setup_vscode
            ;;
        "start")
            start_mcp_server
            ;;
        "test")
            first_test
            ;;
        "help")
            show_help
            ;;
        *)
            echo -e "${RED}Opción desconocida: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
