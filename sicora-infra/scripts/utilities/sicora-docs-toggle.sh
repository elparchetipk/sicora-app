#!/bin/bash
# ============================================================================
# SICORA-DOCS PERMISSIONS TOGGLE
# ============================================================================
# Script para alternar automáticamente entre permisos de solo lectura y escritura
# Detecta el estado actual y cambia al opuesto
# 
# Uso:
#   ./sicora-docs-toggle.sh    # Alternar permisos automáticamente
# ============================================================================

# Configuración
DOCS_PATH="$HOME/Documentos/epti-dev/sicora-app/sicora-docs"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para verificar si el directorio existe
check_docs_directory() {
    if [ ! -d "$DOCS_PATH" ]; then
        echo -e "${RED}❌ Error: El directorio sicora-docs no existe en:${NC}"
        echo -e "${RED}   $DOCS_PATH${NC}"
        exit 1
    fi
}

# Función para detectar el modo actual
detect_current_mode() {
    local sample_file=$(find "$DOCS_PATH" -type f -name "*.md" | head -1)
    
    if [ -n "$sample_file" ]; then
        local file_perms=$(stat -c "%a" "$sample_file")
        echo "$file_perms"
    else
        echo "unknown"
    fi
}

# Función para establecer modo solo lectura
set_readonly_mode() {
    echo -e "${BLUE}🔒 Cambiando a modo SOLO LECTURA...${NC}"
    
    find "$DOCS_PATH" -type d -exec chmod 555 {} \; 2>/dev/null
    find "$DOCS_PATH" -type f -exec chmod 444 {} \; 2>/dev/null
    
    echo -e "${GREEN}✅ Documentación protegida (solo lectura)${NC}"
}

# Función para establecer modo escritura
set_write_mode() {
    echo -e "${YELLOW}✏️  Cambiando a modo ESCRITURA...${NC}"
    
    find "$DOCS_PATH" -type d -exec chmod 755 {} \; 2>/dev/null
    find "$DOCS_PATH" -type f -exec chmod 644 {} \; 2>/dev/null
    
    echo -e "${YELLOW}✅ Documentación editable (escritura habilitada)${NC}"
    echo -e "${RED}⚠️  Recuerda volver a solo lectura cuando termines${NC}"
}

# Función principal
main() {
    echo -e "${BLUE}🔄 SICORA-DOCS PERMISSIONS TOGGLE${NC}"
    echo ""
    
    check_docs_directory
    
    local current_mode=$(detect_current_mode)
    
    case "$current_mode" in
        "444")
            echo -e "${GREEN}📖 Estado actual: SOLO LECTURA${NC}"
            set_write_mode
            ;;
        "644")
            echo -e "${YELLOW}✏️  Estado actual: ESCRITURA${NC}"
            set_readonly_mode
            ;;
        *)
            echo -e "${RED}⚠️  Estado actual: DESCONOCIDO ($current_mode)${NC}"
            echo -e "${BLUE}🔒 Estableciendo modo SOLO LECTURA por defecto...${NC}"
            set_readonly_mode
            ;;
    esac
    
    echo ""
}

# Ejecutar función principal
main "$@"
