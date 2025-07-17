#!/bin/bash

# Script de Backup Automático de Documentación SICORA
# Versión: 1.0 - PROTECCIÓN CRÍTICA
# Fecha: 4 de julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
BACKUP_BASE_DIR="/tmp/sicora-docs-backup"
PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_BASE_DIR/$TIMESTAMP"

# Función para crear backup de un archivo
backup_file() {
    local source_file="$1"
    local relative_path="${source_file#$PROJECT_ROOT/}"
    local backup_file="$BACKUP_DIR/$relative_path"
    local backup_file_dir="$(dirname "$backup_file")"
    
    # Verificar que el archivo existe y no está vacío
    if [ ! -f "$source_file" ]; then
        echo -e "${RED}❌ ERROR: $source_file no existe${NC}"
        return 1
    fi
    
    if [ ! -s "$source_file" ]; then
        echo -e "${YELLOW}⚠️  ADVERTENCIA: $source_file está vacío${NC}"
    fi
    
    # Crear directorio de backup
    mkdir -p "$backup_file_dir"
    
    # Copiar archivo
    cp "$source_file" "$backup_file"
    
    # Verificar integridad del backup
    if [ -f "$backup_file" ] && [ "$(wc -l < "$source_file")" -eq "$(wc -l < "$backup_file")" ]; then
        echo -e "${GREEN}✅ BACKUP EXITOSO: $relative_path${NC}"
        return 0
    else
        echo -e "${RED}❌ FALLO EN BACKUP: $relative_path${NC}"
        return 1
    fi
}

# Función principal
main() {
    echo -e "${BLUE}🛡️  INICIO DE BACKUP DOCUMENTAL SICORA${NC}"
    echo -e "${BLUE}Timestamp: $TIMESTAMP${NC}"
    echo -e "${BLUE}Destino: $BACKUP_DIR${NC}"
    echo ""
    
    # Crear directorio base de backup
    mkdir -p "$BACKUP_DIR"
    
    local backup_count=0
    local error_count=0
    
    # Buscar todos los archivos .md en el proyecto
    while IFS= read -r -d '' file; do
        if backup_file "$file"; then
            backup_count=$((backup_count + 1))
        else
            error_count=$((error_count + 1))
        fi
    done < <(find "$PROJECT_ROOT" -name "*.md" -type f -print0)
    
    # Crear manifiesto del backup
    echo "# BACKUP SICORA DOCUMENTACIÓN" > "$BACKUP_DIR/MANIFEST.md"
    echo "Timestamp: $TIMESTAMP" >> "$BACKUP_DIR/MANIFEST.md"
    echo "Archivos respaldados: $backup_count" >> "$BACKUP_DIR/MANIFEST.md"
    echo "Errores: $error_count" >> "$BACKUP_DIR/MANIFEST.md"
    echo "" >> "$BACKUP_DIR/MANIFEST.md"
    echo "## Archivos incluidos:" >> "$BACKUP_DIR/MANIFEST.md"
    find "$BACKUP_DIR" -name "*.md" -not -name "MANIFEST.md" | sort >> "$BACKUP_DIR/MANIFEST.md"
    
    # Resumen final
    echo ""
    echo -e "${BLUE}📊 RESUMEN DE BACKUP${NC}"
    echo -e "${GREEN}✅ Archivos respaldados: $backup_count${NC}"
    if [ $error_count -gt 0 ]; then
        echo -e "${RED}❌ Errores: $error_count${NC}"
    fi
    echo -e "${BLUE}📁 Ubicación: $BACKUP_DIR${NC}"
    
    # Limpiar backups antiguos (mantener últimos 10)
    echo ""
    echo -e "${BLUE}🧹 Limpiando backups antiguos...${NC}"
    cd "$BACKUP_BASE_DIR" 2>/dev/null || true
    ls -1t | tail -n +11 | xargs -r rm -rf
    echo -e "${GREEN}✅ Limpieza completada${NC}"
    
    return $error_count
}

# Función de ayuda
show_help() {
    echo "Script de Backup Automático de Documentación SICORA"
    echo ""
    echo "Uso: $0 [opciones]"
    echo ""
    echo "Opciones:"
    echo "  -h, --help     Mostrar esta ayuda"
    echo "  --verify       Solo verificar archivos sin crear backup"
    echo ""
    echo "Ejemplos:"
    echo "  $0                 # Crear backup completo"
    echo "  $0 --verify        # Solo verificar integridad"
}

# Procesar argumentos
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    --verify)
        echo -e "${BLUE}🔍 MODO VERIFICACIÓN ÚNICAMENTE${NC}"
        # Solo verificar sin crear backup
        find "$PROJECT_ROOT" -name "*.md" -type f | while read -r file; do
            if [ ! -s "$file" ]; then
                echo -e "${RED}❌ VACÍO: $file${NC}"
            else
                line_count=$(wc -l < "$file")
                echo -e "${GREEN}✅ OK: $file ($line_count líneas)${NC}"
            fi
        done
        exit 0
        ;;
    "")
        main
        exit $?
        ;;
    *)
        echo -e "${RED}❌ Opción desconocida: $1${NC}"
        show_help
        exit 1
        ;;
esac
