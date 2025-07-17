#!/bin/bash

# Script de verificación de estructura de documentación SICORA
# Verifica que no haya archivos .md en la raíz (excepto README.md)
# y que toda la documentación esté organizada en _docs/

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

log_success() {
    echo -e "${BLUE}[SUCCESS]${NC} $1"
}

# Verificar estructura de documentación
verify_doc_structure() {
    local root_path="$1"
    local errors=0
    
    log_info "Verificando estructura de documentación en: $root_path"
    
    # Verificar que existe la carpeta _docs
    if [ ! -d "$root_path/_docs" ]; then
        log_error "La carpeta _docs no existe en $root_path"
        ((errors++))
    else
        log_success "Carpeta _docs encontrada"
    fi
    
    # Verificar archivos .md en la raíz (solo README.md debe estar permitido)
    log_info "Verificando archivos .md en la raíz..."
    
    local md_files_in_root=$(find "$root_path" -maxdepth 1 -name "*.md" -not -name "README.md" 2>/dev/null || true)
    
    if [ -n "$md_files_in_root" ]; then
        log_error "Se encontraron archivos .md no permitidos en la raíz:"
        echo "$md_files_in_root" | while read -r file; do
            log_error "  - $(basename "$file")"
        done
        ((errors++))
    else
        log_success "No se encontraron archivos .md no permitidos en la raíz"
    fi
    
    # Verificar que README.md principal existe
    if [ ! -f "$root_path/README.md" ]; then
        log_error "README.md principal no encontrado en la raíz"
        ((errors++))
    else
        log_success "README.md principal encontrado"
    fi
    
    # Verificar estructura de carpetas en _docs
    if [ -d "$root_path/_docs" ]; then
        log_info "Verificando estructura de carpetas en _docs..."
        
        local expected_folders=("integracion" "mcp" "configuracion" "desarrollo" "reportes" "guias")
        
        for folder in "${expected_folders[@]}"; do
            if [ ! -d "$root_path/_docs/$folder" ]; then
                log_warn "Carpeta recomendada no encontrada: _docs/$folder"
            else
                log_success "Carpeta encontrada: _docs/$folder"
                
                # Verificar que cada carpeta tiene su README.md
                if [ ! -f "$root_path/_docs/$folder/README.md" ]; then
                    log_warn "README.md no encontrado en _docs/$folder"
                else
                    log_success "README.md encontrado en _docs/$folder"
                fi
            fi
        done
    fi
    
    # Verificar scripts en la raíz (no deberían estar ahí)
    log_info "Verificando scripts en la raíz..."
    
    local sh_files_in_root=$(find "$root_path" -maxdepth 1 -name "*.sh" 2>/dev/null || true)
    
    if [ -n "$sh_files_in_root" ]; then
        log_error "Se encontraron scripts no permitidos en la raíz:"
        echo "$sh_files_in_root" | while read -r file; do
            log_error "  - $(basename "$file")"
        done
        ((errors++))
    else
        log_success "No se encontraron scripts no permitidos en la raíz"
    fi
    
    # Verificar que existe la carpeta scripts
    if [ ! -d "$root_path/scripts" ]; then
        log_error "La carpeta scripts no existe en $root_path"
        ((errors++))
    else
        log_success "Carpeta scripts encontrada"
        
        # Verificar que la carpeta scripts tiene su README.md
        if [ ! -f "$root_path/scripts/README.md" ]; then
            log_warn "README.md no encontrado en scripts/"
        else
            log_success "README.md encontrado en scripts/"
        fi
    fi
    
    return $errors
}

# Función para mover archivos mal ubicados
fix_doc_structure() {
    local root_path="$1"
    
    log_info "Intentando corregir estructura de documentación y scripts..."
    
    # Buscar archivos .md en la raíz (excepto README.md)
    local md_files_in_root=$(find "$root_path" -maxdepth 1 -name "*.md" -not -name "README.md" 2>/dev/null || true)
    
    if [ -n "$md_files_in_root" ]; then
        log_info "Moviendo archivos .md de la raíz a _docs/..."
        
        # Crear carpeta _docs si no existe
        mkdir -p "$root_path/_docs/reportes"
        
        echo "$md_files_in_root" | while read -r file; do
            local filename=$(basename "$file")
            log_info "Moviendo $filename a _docs/reportes/"
            mv "$file" "$root_path/_docs/reportes/"
        done
        
        log_success "Archivos .md movidos correctamente"
    fi
    
    # Buscar scripts .sh en la raíz
    local sh_files_in_root=$(find "$root_path" -maxdepth 1 -name "*.sh" 2>/dev/null || true)
    
    if [ -n "$sh_files_in_root" ]; then
        log_info "Moviendo scripts de la raíz a scripts/..."
        
        # Crear carpeta scripts si no existe
        mkdir -p "$root_path/scripts"
        
        echo "$sh_files_in_root" | while read -r file; do
            local filename=$(basename "$file")
            log_info "Moviendo $filename a scripts/"
            mv "$file" "$root_path/scripts/"
            # Hacer ejecutable
            chmod +x "$root_path/scripts/$filename"
        done
        
        log_success "Scripts movidos correctamente"
    fi
}

# Función para generar reporte
generate_report() {
    local root_path="$1"
    local report_file="$root_path/_docs/reportes/VERIFICACION_ESTRUCTURA_DOCUMENTACION.md"
    
    log_info "Generando reporte de verificación..."
    
    mkdir -p "$(dirname "$report_file")"
    
    cat > "$report_file" << EOF
# Reporte de Verificación - Estructura de Documentación y Scripts SICORA

## Fecha de Verificación
$(date '+%d de %B de %Y a las %H:%M:%S')

## Estructura Verificada

### ✅ Archivos en la Raíz
- README.md principal: $([ -f "$root_path/README.md" ] && echo "✅ Presente" || echo "❌ Ausente")

### ✅ Carpeta _docs
- Carpeta _docs: $([ -d "$root_path/_docs" ] && echo "✅ Presente" || echo "❌ Ausente")

### ✅ Carpeta scripts
- Carpeta scripts: $([ -d "$root_path/scripts" ] && echo "✅ Presente" || echo "❌ Ausente")
- README.md en scripts: $([ -f "$root_path/scripts/README.md" ] && echo "✅ Presente" || echo "❌ Ausente")

### ✅ Subcarpetas en _docs
EOF

    local folders=("integracion" "mcp" "configuracion" "desarrollo" "reportes" "guias")
    for folder in "${folders[@]}"; do
        if [ -d "$root_path/_docs/$folder" ]; then
            echo "- $folder/: ✅ Presente" >> "$report_file"
            if [ -f "$root_path/_docs/$folder/README.md" ]; then
                echo "  - README.md: ✅ Presente" >> "$report_file"
            else
                echo "  - README.md: ❌ Ausente" >> "$report_file"
            fi
        else
            echo "- $folder/: ❌ Ausente" >> "$report_file"
        fi
    done
    
    cat >> "$report_file" << EOF

### ❌ Archivos .md Mal Ubicados
EOF
    
    local md_files_in_root=$(find "$root_path" -maxdepth 1 -name "*.md" -not -name "README.md" 2>/dev/null || true)
    if [ -n "$md_files_in_root" ]; then
        echo "$md_files_in_root" | while read -r file; do
            echo "- $(basename "$file")" >> "$report_file"
        done
    else
        echo "- Ninguno (✅ Estructura correcta)" >> "$report_file"
    fi
    
    cat >> "$report_file" << EOF

## Recomendaciones

$([ -n "$md_files_in_root" ] && echo "1. Mover archivos .md de la raíz a la carpeta apropiada en _docs/" || echo "1. La estructura de documentación es correcta")

2. Verificar que todos los enlaces en README.md principal apunten a la nueva estructura
3. Actualizar índices de carpetas cuando se agregue nueva documentación
4. Seguir las instrucciones en .github/copilot-instructions.md

## Estado General
$([ -z "$md_files_in_root" ] && echo "✅ ESTRUCTURA CORRECTA" || echo "⚠️  REQUIERE CORRECCIÓN")

---
Generado automáticamente por el script de verificación de estructura de documentación SICORA.
EOF

    log_success "Reporte generado en: $report_file"
}

# Función principal
main() {
    local root_path="${1:-$(pwd)}"
    local action="${2:-verify}"
    
    echo "🔍 Verificación de Estructura de Documentación SICORA"
    echo "======================================================"
    echo "Directorio: $root_path"
    echo "Acción: $action"
    echo ""
    
    case "$action" in
        "verify")
            verify_doc_structure "$root_path"
            local exit_code=$?
            generate_report "$root_path"
            
            if [ $exit_code -eq 0 ]; then
                log_success "Verificación completada sin errores"
            else
                log_error "Verificación completada con $exit_code errores"
                echo ""
                log_info "Para corregir automáticamente, ejecuta:"
                log_info "$0 $root_path fix"
            fi
            
            exit $exit_code
            ;;
        "fix")
            fix_doc_structure "$root_path"
            verify_doc_structure "$root_path"
            generate_report "$root_path"
            ;;
        *)
            echo "Uso: $0 [directorio] [verify|fix]"
            echo ""
            echo "Acciones:"
            echo "  verify  - Verificar estructura (por defecto)"
            echo "  fix     - Corregir estructura automáticamente"
            exit 1
            ;;
    esac
}

# Ejecutar función principal con argumentos
main "$@"
