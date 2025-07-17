#!/bin/bash

# Script de Verificación de Integridad Documental SICORA
# Versión: 1.0 - PROTECCIÓN CRÍTICA
# Fecha: 4 de julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"

# Documentos críticos que requieren protección máxima
CRITICAL_DOCS=(
    "_docs/mcp/GUIA_MCP_PRINCIPIANTES.md"
    "_docs/mcp/CHECKLIST_MCP_PRINCIPIANTES.md"  
    "_docs/mcp/RESUMEN_MCP_PRINCIPIANTES.md"
    "_docs/guias/FORMATO_CSV_PROGRAMAS_FORMACION.md"
    "_docs/guias/ESTRATEGIA_POSTMAN_SICORA_EDUCATIVA.md"
    "_docs/reportes/CONTEO_ENDPOINTS_BACKEND_SICORA.md"
    "_docs/reportes/ANALISIS_ENDPOINTS_COMPLETADO.md"
)

# Función para verificar un documento
verify_document() {
    local file="$1"
    local is_critical="$2"
    local full_path="$PROJECT_ROOT/$file"
    
    # Verificar existencia
    if [ ! -f "$full_path" ]; then
        echo -e "${RED}🚨 CRÍTICO: $file NO EXISTE${NC}"
        return 2
    fi
    
    # Verificar que no esté vacío
    if [ ! -s "$full_path" ]; then
        if [ "$is_critical" = "true" ]; then
            echo -e "${RED}🚨 CRÍTICO: $file ESTÁ VACÍO${NC}"
            return 2
        else
            echo -e "${YELLOW}⚠️  ADVERTENCIA: $file está vacío${NC}"
            return 1
        fi
    fi
    
    # Contar líneas
    local line_count=$(wc -l < "$full_path")
    
    # Verificar contenido mínimo
    if [ "$line_count" -lt 5 ]; then
        if [ "$is_critical" = "true" ]; then
            echo -e "${RED}🚨 CRÍTICO: $file tiene muy poco contenido ($line_count líneas)${NC}"
            return 2
        else
            echo -e "${YELLOW}⚠️  ADVERTENCIA: $file tiene poco contenido ($line_count líneas)${NC}"
            return 1
        fi
    fi
    
    # Verificar sintaxis markdown básica
    if ! grep -q "^#" "$full_path"; then
        echo -e "${YELLOW}⚠️  ADVERTENCIA: $file no tiene encabezados markdown${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ OK: $file ($line_count líneas)${NC}"
    return 0
}

# Función para generar reporte de salud
generate_health_report() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local report_file="$PROJECT_ROOT/_docs/reportes/REPORTE_SALUD_DOCUMENTACION.md"
    
    cat > "$report_file" << EOF
# 📊 Reporte de Salud Documental SICORA

**Fecha:** $timestamp  
**Generado por:** verify-doc-integrity.sh  

## 🎯 Resumen Ejecutivo

- **Total documentos verificados:** $total_docs
- **Documentos críticos OK:** $critical_ok
- **Advertencias:** $warning_count
- **Errores críticos:** $critical_error_count

## 📋 Estado por Categoría

### 🚨 Documentos Críticos
$(for doc in "${CRITICAL_DOCS[@]}"; do
    status="$(verify_document "$doc" "true" 2>&1 | head -1)"
    echo "- $doc: $status"
done)

### 📝 Salud General
- ✅ Documentos íntegros: $((total_docs - warning_count - critical_error_count))
- ⚠️  Con advertencias: $warning_count  
- 🚨 Con errores críticos: $critical_error_count

## 🔗 Próximas Acciones

$(if [ $critical_error_count -gt 0 ]; then
    echo "🚨 **ACCIÓN INMEDIATA REQUERIDA:** Restaurar documentos críticos faltantes"
elif [ $warning_count -gt 0 ]; then
    echo "⚠️  **REVISIÓN RECOMENDADA:** Verificar documentos con advertencias"
else
    echo "✅ **ESTADO ÓPTIMO:** Toda la documentación está en buen estado"
fi)

---
**Próxima verificación:** $(date -d '+1 day' '+%Y-%m-%d %H:%M:%S')
EOF
    
    echo -e "${BLUE}📄 Reporte generado: $report_file${NC}"
}

# Función principal
main() {
    echo -e "${BLUE}🔍 VERIFICACIÓN DE INTEGRIDAD DOCUMENTAL SICORA${NC}"
    echo -e "${BLUE}$(date)${NC}"
    echo ""
    
    local total_docs=0
    local critical_ok=0
    local warning_count=0
    local critical_error_count=0
    
    # Verificar documentos críticos primero
    echo -e "${BLUE}🚨 VERIFICANDO DOCUMENTOS CRÍTICOS${NC}"
    echo "=="
    
    for doc in "${CRITICAL_DOCS[@]}"; do
        verify_document "$doc" "true"
        case $? in
            0) critical_ok=$((critical_ok + 1)) ;;
            1) warning_count=$((warning_count + 1)) ;;
            2) critical_error_count=$((critical_error_count + 1)) ;;
        esac
        total_docs=$((total_docs + 1))
    done
    
    echo ""
    echo -e "${BLUE}📝 VERIFICANDO OTROS DOCUMENTOS${NC}"
    echo "=="
    
    # Verificar otros documentos
    while IFS= read -r -d '' file; do
        local relative_path="${file#$PROJECT_ROOT/}"
        
        # Saltar si ya es crítico
        local is_critical=false
        for critical_doc in "${CRITICAL_DOCS[@]}"; do
            if [ "$relative_path" = "$critical_doc" ]; then
                is_critical=true
                break
            fi
        done
        
        if [ "$is_critical" = "false" ]; then
            verify_document "$relative_path" "false"
            case $? in
                0) ;; # OK, no hacer nada
                1) warning_count=$((warning_count + 1)) ;;
                2) critical_error_count=$((critical_error_count + 1)) ;;
            esac
            total_docs=$((total_docs + 1))
        fi
        
    done < <(find "$PROJECT_ROOT" -name "*.md" -type f -print0)
    
    # Resumen final
    echo ""
    echo -e "${BLUE}📊 RESUMEN DE VERIFICACIÓN${NC}"
    echo "=================================="
    echo -e "Total documentos: $total_docs"
    echo -e "${GREEN}✅ Documentos críticos OK: $critical_ok/${#CRITICAL_DOCS[@]}${NC}"
    
    if [ $warning_count -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Advertencias: $warning_count${NC}"
    fi
    
    if [ $critical_error_count -gt 0 ]; then
        echo -e "${RED}🚨 Errores críticos: $critical_error_count${NC}"
        echo ""
        echo -e "${RED}🚨 ACCIÓN REQUERIDA: Documentos críticos necesitan atención inmediata${NC}"
    fi
    
    # Generar reporte
    generate_health_report
    
    # Código de salida basado en severidad
    if [ $critical_error_count -gt 0 ]; then
        return 2  # Error crítico
    elif [ $warning_count -gt 0 ]; then
        return 1  # Advertencias
    else
        return 0  # Todo OK
    fi
}

# Función de ayuda
show_help() {
    echo "Script de Verificación de Integridad Documental SICORA"
    echo ""
    echo "Uso: $0 [opciones]"
    echo ""
    echo "Opciones:"
    echo "  -h, --help         Mostrar esta ayuda"
    echo "  --critical-only    Solo verificar documentos críticos"
    echo "  --report-only      Solo generar reporte de salud"
    echo ""
    echo "Códigos de salida:"
    echo "  0 - Todo correcto"
    echo "  1 - Advertencias encontradas"  
    echo "  2 - Errores críticos encontrados"
}

# Procesar argumentos
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    --critical-only)
        echo -e "${BLUE}🚨 MODO: Solo documentos críticos${NC}"
        for doc in "${CRITICAL_DOCS[@]}"; do
            verify_document "$doc" "true"
        done
        exit $?
        ;;
    --report-only)
        echo -e "${BLUE}📄 MODO: Solo generar reporte${NC}"
        # Variables para el reporte (simplificadas)
        total_docs=0
        critical_ok=0
        warning_count=0
        critical_error_count=0
        generate_health_report
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
