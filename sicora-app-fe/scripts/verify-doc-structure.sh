#!/bin/bash

# Script de verificación de estructura de documentación para sicora-app-fe
# Aplica las mismas reglas que sicora-app pero para el frontend

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
log_info() {
    echo -e "[INFO] $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar estructura
verify_structure() {
    local errors=0
    
    log_info "Verificando estructura de documentación en: $PROJECT_ROOT"
    
    # Verificar carpeta _docs
    if [ ! -d "$PROJECT_ROOT/_docs" ]; then
        log_error "Carpeta _docs no encontrada"
        errors=$((errors + 1))
    else
        log_success "Carpeta _docs encontrada"
    fi
    
    # Verificar archivos .md en la raíz (solo README.md está permitido)
    log_info "Verificando archivos .md en la raíz..."
    local md_files=($(find "$PROJECT_ROOT" -maxdepth 1 -name "*.md" -type f))
    local forbidden_files=()
    
    for file in "${md_files[@]}"; do
        local basename=$(basename "$file")
        if [[ "$basename" != "README.md" ]]; then
            forbidden_files+=("$basename")
        fi
    done
    
    if [ ${#forbidden_files[@]} -eq 0 ]; then
        log_success "No se encontraron archivos .md no permitidos en la raíz"
    else
        log_error "Archivos .md encontrados en la raíz (deben moverse a _docs/):"
        for file in "${forbidden_files[@]}"; do
            echo "  - $file"
        done
        errors=$((errors + 1))
    fi
    
    # Verificar README.md principal
    if [ -f "$PROJECT_ROOT/README.md" ]; then
        log_success "README.md principal encontrado"
    else
        log_error "README.md principal no encontrado"
        errors=$((errors + 1))
    fi
    
    # Verificar carpeta scripts
    if [ -d "$PROJECT_ROOT/scripts" ]; then
        log_success "Carpeta scripts encontrada"
        
        # Verificar README.md en scripts
        if [ -f "$PROJECT_ROOT/scripts/README.md" ]; then
            log_success "README.md encontrado en scripts/"
        else
            log_warning "README.md no encontrado en scripts/"
        fi
    else
        log_warning "Carpeta scripts no encontrada"
    fi
    
    # Verificar scripts en la raíz (solo algunos están permitidos)
    log_info "Verificando scripts en la raíz..."
    local script_files=($(find "$PROJECT_ROOT" -maxdepth 1 -name "*.sh" -type f))
    local forbidden_scripts=()
    
    for file in "${script_files[@]}"; do
        local basename=$(basename "$file")
        # Permitir algunos scripts específicos del frontend
        if [[ "$basename" != "deploy.sh" && "$basename" != "build.sh" ]]; then
            forbidden_scripts+=("$basename")
        fi
    done
    
    if [ ${#forbidden_scripts[@]} -eq 0 ]; then
        log_success "No se encontraron scripts no permitidos en la raíz"
    else
        log_warning "Scripts encontrados en la raíz (considerar mover a scripts/):"
        for file in "${forbidden_scripts[@]}"; do
            echo "  - $file"
        done
    fi
    
    return $errors
}

# Función para auto-organizar archivos
auto_organize() {
    log_info "Iniciando auto-organización de archivos..."
    
    # Crear carpetas en _docs si no existen
    local categories=("integracion" "configuracion" "desarrollo" "reportes" "guias" "diseno")
    
    for category in "${categories[@]}"; do
        if [ ! -d "$PROJECT_ROOT/_docs/$category" ]; then
            mkdir -p "$PROJECT_ROOT/_docs/$category"
            log_success "Carpeta creada: _docs/$category"
        fi
    done
    
    # Mover archivos .md según su contenido/nombre
    local md_files=($(find "$PROJECT_ROOT" -maxdepth 1 -name "*.md" -type f))
    
    for file in "${md_files[@]}"; do
        local basename=$(basename "$file")
        
        # Saltar README.md
        if [[ "$basename" == "README.md" ]]; then
            continue
        fi
        
        # Determinar categoría según nombre del archivo
        local category=""
        case "$basename" in
            *INTEGRACION*|*INTEGRATION*)
                category="integracion"
                ;;
            *CONFIGURACION*|*CONFIG*|*SETUP*|*HOSTINGER*)
                category="configuracion"
                ;;
            *DESARROLLO*|*DEVELOPMENT*|*PLAN*)
                category="desarrollo"
                ;;
            *REPORTE*|*REPORT*|*STATUS*|*ESTADO*|*RESUMEN*)
                category="reportes"
                ;;
            *GUIA*|*GUIDE*|*TUTORIAL*|*COMPLETADA*|*COMPLETADO*)
                category="guias"
                ;;
            *DESIGN*|*BRANDING*|*UI*|*UX*|*COLOR*)
                category="diseno"
                ;;
            *)
                category="general"
                ;;
        esac
        
        # Crear carpeta general si no existe
        if [[ "$category" == "general" && ! -d "$PROJECT_ROOT/_docs/general" ]]; then
            mkdir -p "$PROJECT_ROOT/_docs/general"
            log_success "Carpeta creada: _docs/general"
        fi
        
        # Mover archivo
        if [ -n "$category" ]; then
            mv "$file" "$PROJECT_ROOT/_docs/$category/"
            log_success "Movido: $basename -> _docs/$category/"
        fi
    done
    
    # Crear README.md en cada carpeta si no existe
    for category in "${categories[@]}" "general"; do
        if [ -d "$PROJECT_ROOT/_docs/$category" ] && [ ! -f "$PROJECT_ROOT/_docs/$category/README.md" ]; then
            cat > "$PROJECT_ROOT/_docs/$category/README.md" << EOF
# ${category^} - Frontend SICORA

## Documentación de ${category^}

Esta carpeta contiene la documentación relacionada con ${category} del frontend SICORA.

## Archivos

$(ls -1 "$PROJECT_ROOT/_docs/$category" | grep -v README.md | sed 's/^/- /')

---
*Generado automáticamente por el script de organización*
EOF
            log_success "README.md creado en _docs/$category/"
        fi
    done
}

# Función para generar reporte
generate_report() {
    local report_file="$PROJECT_ROOT/_docs/reports/VERIFICACION_ESTRUCTURA_DOCUMENTACION_FE.md"
    
    # Crear carpeta reports si no existe
    mkdir -p "$PROJECT_ROOT/_docs/reports"
    
    cat > "$report_file" << EOF
# Reporte de Verificación - Estructura de Documentación Frontend SICORA

## Fecha de Verificación
$(date '+%d de %B de %Y a las %H:%M:%S')

## Estructura Verificada

### ✅ Archivos en la Raíz
- README.md principal: $([ -f "$PROJECT_ROOT/README.md" ] && echo "✅ Presente" || echo "❌ Ausente")

### ✅ Carpeta _docs
- Carpeta _docs: $([ -d "$PROJECT_ROOT/_docs" ] && echo "✅ Presente" || echo "❌ Ausente")

### ✅ Carpeta scripts
- Carpeta scripts: $([ -d "$PROJECT_ROOT/scripts" ] && echo "✅ Presente" || echo "❌ Ausente")
- README.md en scripts: $([ -f "$PROJECT_ROOT/scripts/README.md" ] && echo "✅ Presente" || echo "❌ Ausente")

### ✅ Subcarpetas en _docs
EOF

    # Agregar estado de subcarpetas
    local categories=("integracion" "configuracion" "desarrollo" "reportes" "guias" "diseno" "general")
    for category in "${categories[@]}"; do
        if [ -d "$PROJECT_ROOT/_docs/$category" ]; then
            echo "- $category/: ✅ Presente" >> "$report_file"
            echo "  - README.md: $([ -f "$PROJECT_ROOT/_docs/$category/README.md" ] && echo "✅ Presente" || echo "❌ Ausente")" >> "$report_file"
        fi
    done
    
    # Agregar archivos .md mal ubicados
    local md_files=($(find "$PROJECT_ROOT" -maxdepth 1 -name "*.md" -type f))
    local forbidden_files=()
    
    for file in "${md_files[@]}"; do
        local basename=$(basename "$file")
        if [[ "$basename" != "README.md" ]]; then
            forbidden_files+=("$basename")
        fi
    done
    
    cat >> "$report_file" << EOF

### ❌ Archivos .md Mal Ubicados
EOF
    
    if [ ${#forbidden_files[@]} -eq 0 ]; then
        echo "- Ninguno (✅ Estructura correcta)" >> "$report_file"
    else
        for file in "${forbidden_files[@]}"; do
            echo "- $file" >> "$report_file"
        done
    fi
    
    cat >> "$report_file" << EOF

## Recomendaciones

1. $([ ${#forbidden_files[@]} -eq 0 ] && echo "La estructura de documentación es correcta" || echo "Mover archivos .md de la raíz a _docs/")

2. Verificar que todos los enlaces en README.md principal apunten a la nueva estructura
3. Actualizar índices de carpetas cuando se agregue nueva documentación
4. Seguir las instrucciones de organización del proyecto principal

## Estado General
$([ ${#forbidden_files[@]} -eq 0 ] && echo "✅ ESTRUCTURA CORRECTA" || echo "⚠️ REQUIERE ORGANIZACIÓN")

---
Generado automáticamente por el script de verificación de estructura de documentación Frontend SICORA.
EOF
    
    log_success "Reporte generado en: $report_file"
}

# Función principal
main() {
    echo -e "${BLUE}🔍 Verificación de Estructura de Documentación SICORA Frontend${NC}"
    echo "======================================================"
    echo "Directorio: $PROJECT_ROOT"
    echo "Acción: ${1:-verify}"
    echo ""
    
    case "${1:-verify}" in
        "verify")
            verify_structure
            generate_report
            if [ $? -eq 0 ]; then
                log_success "Verificación completada sin errores"
            else
                log_error "Verificación completada con errores"
                exit 1
            fi
            ;;
        "organize")
            auto_organize
            verify_structure
            generate_report
            log_success "Organización completada"
            ;;
        *)
            echo "Uso: $0 [verify|organize]"
            echo "  verify   - Solo verificar estructura"
            echo "  organize - Organizar automáticamente archivos"
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
