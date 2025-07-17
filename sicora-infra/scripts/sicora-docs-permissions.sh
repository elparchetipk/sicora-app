#!/bin/bash
# ============================================================================
# SICORA-DOCS PERMISSIONS MANAGER
# ============================================================================
# Script para gestionar permisos de la documentación externa sicora-docs
# Permite alternar entre modo solo lectura y modo escritura
# 
# Uso:
#   ./sicora-docs-permissions.sh 1    # Modo solo lectura
#   ./sicora-docs-permissions.sh 2    # Modo escritura
#   ./sicora-docs-permissions.sh      # Mostrar estado actual
# ============================================================================

# Configuración
DOCS_PATH="$HOME/Documentos/epti-dev/sicora-app/sicora-docs"
SCRIPT_NAME="$(basename "$0")"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar el banner
show_banner() {
    echo -e "${BLUE}============================================================================${NC}"
    echo -e "${BLUE}                    SICORA-DOCS PERMISSIONS MANAGER${NC}"
    echo -e "${BLUE}============================================================================${NC}"
    echo ""
}

# Función para verificar si el directorio existe
check_docs_directory() {
    if [ ! -d "$DOCS_PATH" ]; then
        echo -e "${RED}❌ Error: El directorio sicora-docs no existe en:${NC}"
        echo -e "${RED}   $DOCS_PATH${NC}"
        echo ""
        echo -e "${YELLOW}💡 Asegúrate de que el directorio existe antes de ejecutar este script.${NC}"
        exit 1
    fi
}

# Función para mostrar el estado actual de permisos
show_current_status() {
    echo -e "${BLUE}📋 Estado actual de permisos:${NC}"
    echo ""
    
    # Verificar permisos de algunos archivos
    local sample_file=$(find "$DOCS_PATH" -type f -name "*.md" | head -1)
    local sample_dir=$(find "$DOCS_PATH" -type d | head -2 | tail -1)
    
    if [ -n "$sample_file" ]; then
        local file_perms=$(stat -c "%a" "$sample_file")
        echo -e "   Archivo ejemplo: $(basename "$sample_file") - Permisos: $file_perms"
    fi
    
    if [ -n "$sample_dir" ]; then
        local dir_perms=$(stat -c "%a" "$sample_dir")
        echo -e "   Directorio ejemplo: $(basename "$sample_dir") - Permisos: $dir_perms"
    fi
    
    echo ""
    
    # Determinar el modo actual
    if [ -n "$sample_file" ]; then
        if [ "$file_perms" = "444" ]; then
            echo -e "${GREEN}✅ Modo actual: SOLO LECTURA${NC}"
        elif [ "$file_perms" = "644" ]; then
            echo -e "${YELLOW}✏️  Modo actual: ESCRITURA${NC}"
        else
            echo -e "${RED}⚠️  Modo actual: PERMISOS PERSONALIZADOS ($file_perms)${NC}"
        fi
    fi
    echo ""
}

# Función para establecer modo solo lectura
set_readonly_mode() {
    echo -e "${BLUE}🔒 Estableciendo modo SOLO LECTURA...${NC}"
    echo ""
    
    echo -e "   📁 Configurando directorios (555)..."
    find "$DOCS_PATH" -type d -exec chmod 555 {} \; 2>/dev/null
    
    echo -e "   📄 Configurando archivos (444)..."
    find "$DOCS_PATH" -type f -exec chmod 444 {} \; 2>/dev/null
    
    echo ""
    echo -e "${GREEN}✅ Documentación configurada en modo SOLO LECTURA${NC}"
    echo -e "${GREEN}   - Los archivos no pueden ser modificados${NC}"
    echo -e "${GREEN}   - Los directorios son accesibles pero no modificables${NC}"
    echo ""
}

# Función para establecer modo escritura
set_write_mode() {
    echo -e "${YELLOW}✏️  Estableciendo modo ESCRITURA...${NC}"
    echo ""
    
    echo -e "   📁 Configurando directorios (755)..."
    find "$DOCS_PATH" -type d -exec chmod 755 {} \; 2>/dev/null
    
    echo -e "   📄 Configurando archivos (644)..."
    find "$DOCS_PATH" -type f -exec chmod 644 {} \; 2>/dev/null
    
    echo ""
    echo -e "${YELLOW}✅ Documentación configurada en modo ESCRITURA${NC}"
    echo -e "${YELLOW}   - Los archivos pueden ser modificados${NC}"
    echo -e "${YELLOW}   - Los directorios son completamente accesibles${NC}"
    echo ""
    echo -e "${RED}⚠️  RECUERDA: Vuelve a modo solo lectura cuando termines de editar${NC}"
    echo ""
}

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}📖 Uso del script:${NC}"
    echo ""
    echo -e "   ${SCRIPT_NAME} 1              # Establecer modo SOLO LECTURA"
    echo -e "   ${SCRIPT_NAME} 2              # Establecer modo ESCRITURA"
    echo -e "   ${SCRIPT_NAME}                # Mostrar estado actual"
    echo -e "   ${SCRIPT_NAME} --help         # Mostrar esta ayuda"
    echo ""
    echo -e "${BLUE}📋 Descripción de modos:${NC}"
    echo ""
    echo -e "${GREEN}   Modo 1 (SOLO LECTURA):${NC}"
    echo -e "   - Archivos: 444 (r--r--r--) - Solo lectura para todos"
    echo -e "   - Directorios: 555 (r-xr-xr-x) - Lectura y acceso, sin escritura"
    echo ""
    echo -e "${YELLOW}   Modo 2 (ESCRITURA):${NC}"
    echo -e "   - Archivos: 644 (rw-r--r--) - Lectura/escritura para propietario"
    echo -e "   - Directorios: 755 (rwxr-xr-x) - Acceso completo para propietario"
    echo ""
}

# Función principal
main() {
    show_banner
    check_docs_directory
    
    case "${1:-}" in
        "1")
            set_readonly_mode
            ;;
        "2")
            set_write_mode
            ;;
        "--help"|"-h")
            show_help
            ;;
        "")
            show_current_status
            show_help
            ;;
        *)
            echo -e "${RED}❌ Opción inválida: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal con todos los argumentos
main "$@"
