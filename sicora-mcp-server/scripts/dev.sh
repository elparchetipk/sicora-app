#!/bin/bash

# Script de desarrollo para el servidor MCP SICORA
# Proporciona comandos rápidos para desarrollo

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Mostrar ayuda
show_help() {
    echo "🔧 Servidor MCP SICORA - Herramientas de desarrollo"
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  setup     - Configurar servidor MCP por primera vez"
    echo "  start     - Iniciar servidor en producción"
    echo "  dev       - Iniciar en modo desarrollo"
    echo "  build     - Compilar TypeScript"
    echo "  clean     - Limpiar archivos compilados"
    echo "  test      - Ejecutar pruebas"
    echo "  watch     - Modo desarrollo con recarga automática"
    echo "  status    - Mostrar estado del servidor"
    echo "  logs      - Mostrar logs del servidor"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 setup   # Configurar por primera vez"
    echo "  $0 dev     # Iniciar en modo desarrollo"
    echo "  $0 build   # Compilar el proyecto"
    echo ""
}

# Verificar prerequisitos
check_prerequisites() {
    if ! command -v pnpm &> /dev/null; then
        log_error "pnpm no está instalado. Instalando..."
        npm install -g pnpm
    fi
    
    if [ ! -f "package.json" ]; then
        log_error "No se encontró package.json. Ejecute desde el directorio sicora-mcp-server"
        exit 1
    fi
}

# Configurar servidor por primera vez
setup_server() {
    log_info "Configurando servidor MCP SICORA..."
    
    check_prerequisites
    
    log_info "Instalando dependencias..."
    pnpm install
    
    log_info "Compilando proyecto..."
    pnpm run build
    
    log_info "Configurando VS Code..."
    ./scripts/configure-mcp.sh
    
    log_info "✅ Configuración completada"
}

# Iniciar servidor en producción
start_server() {
    log_info "Iniciando servidor MCP en producción..."
    check_prerequisites
    
    if [ ! -f "dist/index.js" ]; then
        log_warn "No se encontró dist/index.js. Compilando..."
        pnpm run build
    fi
    
    pnpm run start
}

# Iniciar en modo desarrollo
start_dev() {
    log_info "Iniciando servidor MCP en modo desarrollo..."
    check_prerequisites
    pnpm run dev
}

# Compilar proyecto
build_project() {
    log_info "Compilando proyecto TypeScript..."
    check_prerequisites
    pnpm run build
    log_info "✅ Compilación completada"
}

# Limpiar archivos compilados
clean_project() {
    log_info "Limpiando archivos compilados..."
    rm -rf dist
    log_info "✅ Limpieza completada"
}

# Ejecutar pruebas
run_tests() {
    log_info "Ejecutando pruebas..."
    check_prerequisites
    pnpm run test
}

# Modo desarrollo con recarga automática
start_watch() {
    log_info "Iniciando modo desarrollo con recarga automática..."
    check_prerequisites
    pnpm run watch
}

# Mostrar estado del servidor
show_status() {
    log_info "Estado del servidor MCP SICORA:"
    
    if [ -f "dist/index.js" ]; then
        log_info "✅ Compilado: dist/index.js existe"
    else
        log_warn "⚠️  No compilado: dist/index.js no existe"
    fi
    
    if [ -d "node_modules" ]; then
        log_info "✅ Dependencias: node_modules existe"
    else
        log_warn "⚠️  Dependencias: node_modules no existe"
    fi
    
    if pgrep -f "sicora-mcp-server" > /dev/null; then
        log_info "✅ Servidor: Ejecutándose"
    else
        log_warn "⚠️  Servidor: No está ejecutándose"
    fi
}

# Mostrar logs del servidor
show_logs() {
    log_info "Logs del servidor MCP SICORA:"
    # Aquí se pueden agregar comandos para mostrar logs
    log_debug "Funcionalidad de logs en desarrollo"
}

# Procesar argumentos
case "${1:-help}" in
    "setup")
        setup_server
        ;;
    "start")
        start_server
        ;;
    "dev")
        start_dev
        ;;
    "build")
        build_project
        ;;
    "clean")
        clean_project
        ;;
    "test")
        run_tests
        ;;
    "watch")
        start_watch
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "help"|*)
        show_help
        ;;
esac
