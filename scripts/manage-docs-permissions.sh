#!/bin/bash

# 🔒 GESTOR DE PERMISOS SICORA-DOCS
# Script para habilitar/deshabilitar temporalmente el modo de solo lectura

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SICORA_DOCS_DIR="/home/epti/Documentos/epti-dev/sicora-app/sicora-docs"
BACKUP_PERMISSIONS_FILE="/tmp/sicora-docs-permissions-backup.txt"

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}🔒 GESTOR DE PERMISOS SICORA-DOCS${NC}"
    echo "============================================"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos:"
    echo "  unlock    - Desactivar modo solo lectura (permisos de escritura)"
    echo "  lock      - Activar modo solo lectura (solo lectura y ejecución)"
    echo "  status    - Mostrar estado actual de permisos"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 unlock   # Habilitar escritura para actualizar documentación"
    echo "  $0 lock     # Restaurar modo solo lectura por seguridad"
    echo "  $0 status   # Ver permisos actuales"
}

# Función para verificar que el directorio existe
check_directory() {
    if [ ! -d "$SICORA_DOCS_DIR" ]; then
        echo -e "${RED}❌ Error: Directorio sicora-docs no encontrado en $SICORA_DOCS_DIR${NC}"
        exit 1
    fi
}

# Función para mostrar el estado actual
show_status() {
    echo -e "${BLUE}📊 ESTADO ACTUAL DE PERMISOS${NC}"
    echo "================================="
    echo ""
    echo -e "${BLUE}Directorio:${NC} $SICORA_DOCS_DIR"
    echo ""

    # Mostrar permisos actuales
    local current_perms=$(ls -ld "$SICORA_DOCS_DIR" | cut -d' ' -f1)
    echo -e "${BLUE}Permisos actuales:${NC} $current_perms"

    # Interpretar permisos
    if [[ $current_perms =~ ^d.w ]]; then
        echo -e "${GREEN}✅ Estado: ESCRITURA HABILITADA${NC}"
        echo -e "${YELLOW}⚠️  Recuerda activar modo solo lectura después de actualizar${NC}"
    else
        echo -e "${GREEN}🔒 Estado: SOLO LECTURA (SEGURO)${NC}"
        echo -e "${BLUE}ℹ️  Use 'unlock' para habilitar escritura temporalmente${NC}"
    fi

    echo ""
    echo -e "${BLUE}Contenido del directorio:${NC}"
    ls -la "$SICORA_DOCS_DIR" | head -10

    if [ $(ls -1 "$SICORA_DOCS_DIR" | wc -l) -gt 8 ]; then
        echo "... ($(ls -1 "$SICORA_DOCS_DIR" | wc -l) archivos total)"
    fi
}

# Función para desbloquear (habilitar escritura)
unlock_directory() {
    check_directory

    echo -e "${YELLOW}🔓 DESBLOQUEANDO SICORA-DOCS TEMPORALMENTE${NC}"
    echo "=============================================="

    # Guardar permisos actuales para backup
    ls -ld "$SICORA_DOCS_DIR" > "$BACKUP_PERMISSIONS_FILE"
    echo -e "${BLUE}📝 Permisos actuales guardados en backup${NC}"

    # Cambiar permisos del directorio principal
    echo -e "${BLUE}🔧 Habilitando permisos de escritura...${NC}"
    chmod u+w "$SICORA_DOCS_DIR"

    # Cambiar permisos recursivamente para contenido
    find "$SICORA_DOCS_DIR" -type d -exec chmod u+w {} \;
    find "$SICORA_DOCS_DIR" -type f -exec chmod u+w {} \;

    echo -e "${GREEN}✅ SICORA-DOCS DESBLOQUEADO${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  RECORDATORIO IMPORTANTE:${NC}"
    echo -e "${YELLOW}   • Este es un estado temporal para actualización${NC}"
    echo -e "${YELLOW}   • Use '$0 lock' para restaurar seguridad${NC}"
    echo -e "${YELLOW}   • No olvide bloquear después de actualizar${NC}"
    echo ""

    show_status
}

# Función para bloquear (solo lectura)
lock_directory() {
    check_directory

    echo -e "${BLUE}🔒 ACTIVANDO MODO SOLO LECTURA${NC}"
    echo "================================"

    # Cambiar permisos recursivamente para contenido
    echo -e "${BLUE}🔧 Aplicando permisos de solo lectura...${NC}"
    find "$SICORA_DOCS_DIR" -type f -exec chmod u-w {} \;
    find "$SICORA_DOCS_DIR" -type d -exec chmod u-w {} \;

    # Cambiar permisos del directorio principal
    chmod u-w "$SICORA_DOCS_DIR"

    # Limpiar archivo de backup
    if [ -f "$BACKUP_PERMISSIONS_FILE" ]; then
        rm -f "$BACKUP_PERMISSIONS_FILE"
        echo -e "${BLUE}🗑️  Archivo de backup de permisos eliminado${NC}"
    fi

    echo -e "${GREEN}✅ SICORA-DOCS BLOQUEADO (SOLO LECTURA)${NC}"
    echo -e "${GREEN}🔒 Directorio protegido contra escritura accidental${NC}"
    echo ""

    show_status
}

# Función para verificar si hay cambios pendientes
check_pending_changes() {
    if [ -f "$BACKUP_PERMISSIONS_FILE" ]; then
        echo -e "${YELLOW}⚠️  ATENCIÓN: Hay una sesión de escritura activa${NC}"
        echo -e "${YELLOW}   Backup de permisos encontrado en: $BACKUP_PERMISSIONS_FILE${NC}"
        echo -e "${YELLOW}   Use '$0 lock' para restaurar modo solo lectura${NC}"
        echo ""
    fi
}

# Función principal
main() {
    local command=${1:-help}

    case $command in
        "unlock")
            check_pending_changes
            unlock_directory
            ;;
        "lock")
            lock_directory
            ;;
        "status")
            check_pending_changes
            show_status
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Comando no reconocido: $command${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Verificar argumentos y ejecutar
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

main "$@"
