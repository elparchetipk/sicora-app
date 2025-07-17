#!/bin/bash

# =============================================================================
# SICORA-APP Backend Multistack - Bulk Data Loader Utility
# =============================================================================
# Propósito: Utilidad común para carga masiva de datos en todos los stacks
# Autor: SICORA Development Team  
# Fecha: 15 de junio de 2025
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
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

log_header() {
    echo -e "${PURPLE}[BULK-LOADER]${NC} $1"
}

# Configuration
SHARED_DATA_DIR="shared-data"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SHARED_DATA_PATH="$PROJECT_ROOT/$SHARED_DATA_DIR"

# Stack configurations
declare -A STACKS=(
    ["fastapi"]="🐍 FastAPI"
    ["go"]="⚡ Go"
    ["express"]="📱 Express"
    ["nextjs"]="🚀 Next.js"
    ["java"]="☕ Java"
    ["kotlin"]="🔮 Kotlin"
)

# Entity configurations
declare -A ENTITIES=(
    ["users"]="👤 Usuarios"
    ["schedules"]="📅 Horarios"
    ["attendance"]="📝 Asistencia"
    ["evaluations"]="📊 Evaluaciones"
    ["knowledge-base"]="📚 Base de Conocimiento"
    ["ai-training"]="🤖 Entrenamiento IA"
)

# Function to show usage
show_usage() {
    echo "============================================================================="
    log_header "🚀 SICORA-APP Bulk Data Loader Utility"
    echo "============================================================================="
    echo ""
    echo "Uso: $0 [COMANDO] [OPCIONES]"
    echo ""
    echo "COMANDOS:"
    echo "  list-entities     Listar entidades disponibles"
    echo "  list-samples      Listar datasets de ejemplo"
    echo "  list-templates    Listar templates disponibles"
    echo "  validate-csv      Validar archivo CSV"
    echo "  convert-format    Convertir entre formatos"
    echo "  generate-sample   Generar datos de ejemplo"
    echo "  compare-exports   Comparar exports entre stacks"
    echo "  setup-stack       Configurar stack para bulk loading"
    echo ""
    echo "OPCIONES:"
    echo "  -e, --entity      Entidad específica (users, schedules, etc.)"
    echo "  -s, --stack       Stack específico (fastapi, go, express, etc.)"
    echo "  -f, --file        Archivo específico"
    echo "  -o, --output      Directorio de salida"
    echo "  -v, --verbose     Modo verbose"
    echo "  -h, --help        Mostrar esta ayuda"
    echo ""
    echo "EJEMPLOS:"
    echo "  $0 list-entities"
    echo "  $0 validate-csv -f users.csv"
    echo "  $0 generate-sample -e users -s fastapi"
    echo "  $0 convert-format -f users.csv -o users.json"
    echo ""
}

# Function to validate shared-data structure
validate_shared_data() {
    log_info "Validando estructura de shared-data..."
    
    if [ ! -d "$SHARED_DATA_PATH" ]; then
        log_error "Directorio shared-data no encontrado: $SHARED_DATA_PATH"
        return 1
    fi
    
    # Check required directories
    local required_dirs=("imports" "templates" "exports" "samples" "schemas")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$SHARED_DATA_PATH/$dir" ]; then
            log_warning "Directorio requerido no encontrado: $dir"
            log_info "Creando directorio: $SHARED_DATA_PATH/$dir"
            mkdir -p "$SHARED_DATA_PATH/$dir"
        fi
    done
    
    log_success "Estructura de shared-data validada"
    return 0
}

# Function to list entities
list_entities() {
    log_header "📊 Entidades disponibles para carga masiva"
    echo ""
    
    for entity in "${!ENTITIES[@]}"; do
        local entity_emoji="${ENTITIES[$entity]}"
        local imports_dir="$SHARED_DATA_PATH/imports/$entity"
        local template_file="$SHARED_DATA_PATH/templates/${entity}.csv"
        
        echo -n "  $entity_emoji "
        
        if [ -d "$imports_dir" ]; then
            echo -n "✅ Imports "
        else
            echo -n "❌ Imports "
        fi
        
        if [ -f "$template_file" ]; then
            echo "✅ Template"
        else
            echo "❌ Template"
        fi
    done
    echo ""
}

# Function to list samples
list_samples() {
    log_header "📦 Datasets de ejemplo disponibles"
    echo ""
    
    local samples_dir="$SHARED_DATA_PATH/samples"
    
    if [ ! -d "$samples_dir" ]; then
        log_warning "Directorio de samples no encontrado"
        return 1
    fi
    
    for size_dir in "$samples_dir"/*; do
        if [ -d "$size_dir" ]; then
            local size=$(basename "$size_dir")
            echo "  📊 $size:"
            
            for file in "$size_dir"/*.csv; do
                if [ -f "$file" ]; then
                    local filename=$(basename "$file")
                    local line_count=$(wc -l < "$file" 2>/dev/null || echo "0")
                    echo "    - $filename ($line_count líneas)"
                fi
            done
            echo ""
        fi
    done
}

# Function to list templates
list_templates() {
    log_header "📋 Templates disponibles"
    echo ""
    
    local templates_dir="$SHARED_DATA_PATH/templates"
    
    if [ ! -d "$templates_dir" ]; then
        log_warning "Directorio de templates no encontrado"
        return 1
    fi
    
    for template in "$templates_dir"/*.csv; do
        if [ -f "$template" ]; then
            local filename=$(basename "$template")
            local entity=${filename%.csv}
            
            echo "  📄 $filename"
            echo "    Entidad: $entity"
            
            # Show first line (headers)
            if [ -f "$template" ]; then
                local headers=$(head -n1 "$template")
                echo "    Headers: $headers"
            fi
            echo ""
        fi
    done
}

# Function to validate CSV file
validate_csv() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        log_error "Archivo no encontrado: $file"
        return 1
    fi
    
    log_info "Validando archivo CSV: $file"
    
    # Basic CSV validation
    local line_count=$(wc -l < "$file")
    local first_line=$(head -n1 "$file")
    
    log_info "Líneas totales: $line_count"
    log_info "Headers: $first_line"
    
    # Check for common issues
    if [ "$line_count" -lt 2 ]; then
        log_warning "Archivo parece estar vacío (solo headers)"
    fi
    
    # Check for UTF-8 encoding
    if ! file "$file" | grep -q "UTF-8"; then
        log_warning "Archivo podría no estar en UTF-8"
    fi
    
    log_success "Validación CSV básica completada"
}

# Function to generate sample data
generate_sample() {
    local entity="$1"
    local stack="$2"
    local size="${3:-small}"
    
    log_info "Generando datos de ejemplo para $entity ($stack - $size)"
    
    local output_dir="$SHARED_DATA_PATH/samples/$size"
    mkdir -p "$output_dir"
    
    local template_file="$SHARED_DATA_PATH/templates/${entity}.csv"
    local output_file="$output_dir/${entity}-${stack}-sample.csv"
    
    if [ ! -f "$template_file" ]; then
        log_error "Template no encontrado: $template_file"
        return 1
    fi
    
    # Copy template as starting point
    cp "$template_file" "$output_file"
    
    log_success "Sample generado: $output_file"
    log_info "Personaliza el archivo con datos específicos para $stack"
}

# Function to setup stack for bulk loading
setup_stack() {
    local stack="$1"
    
    log_header "🔧 Configurando stack $stack para carga masiva"
    
    local stack_dir=""
    case $stack in
        "fastapi") stack_dir="01-fastapi" ;;
        "go") stack_dir="02-go" ;;
        "express") stack_dir="03-express" ;;
        "nextjs") stack_dir="04-nextjs" ;;
        "java") stack_dir="05-springboot-java" ;;
        "kotlin") stack_dir="06-springboot-kotlin" ;;
        *) 
            log_error "Stack no válido: $stack"
            return 1
            ;;
    esac
    
    local full_stack_path="$PROJECT_ROOT/$stack_dir"
    
    if [ ! -d "$full_stack_path" ]; then
        log_error "Directorio del stack no encontrado: $full_stack_path"
        return 1
    fi
    
    # Create bulk-loader directory in stack
    local bulk_dir="$full_stack_path/bulk-loader"
    mkdir -p "$bulk_dir"
    
    # Create symlink to shared-data
    local shared_link="$bulk_dir/shared-data"
    if [ ! -L "$shared_link" ]; then
        ln -s "../../../$SHARED_DATA_DIR" "$shared_link"
        log_success "Symlink creado: $shared_link"
    else
        log_info "Symlink ya existe: $shared_link"
    fi
    
    # Create example bulk loader script for the stack
    local example_script="$bulk_dir/bulk-loader-example.txt"
    
    case $stack in
        "fastapi")
            cat > "$example_script" << 'EOF'
# Python FastAPI Bulk Loader Example
import pandas as pd
from pathlib import Path

# Path to shared data
SHARED_DATA = Path("shared-data")

# Load users
users_df = pd.read_csv(SHARED_DATA / "imports" / "users" / "users.csv")
print(f"Loaded {len(users_df)} users")

# Validate against schema
# Add your validation logic here

# Insert to database
# Add your database insertion logic here
EOF
            ;;
        "go")
            cat > "$example_script" << 'EOF'
// Go Bulk Loader Example
package main

import (
    "encoding/csv"
    "os"
    "path/filepath"
)

func main() {
    // Path to shared data
    sharedDataPath := "shared-data"
    usersFile := filepath.Join(sharedDataPath, "imports", "users", "users.csv")
    
    // Open CSV file
    file, err := os.Open(usersFile)
    if err != nil {
        panic(err)
    }
    defer file.Close()
    
    // Read CSV
    reader := csv.NewReader(file)
    records, err := reader.ReadAll()
    if err != nil {
        panic(err)
    }
    
    // Process records
    // Add your processing logic here
}
EOF
            ;;
        "express")
            cat > "$example_script" << 'EOF'
// Node.js Express Bulk Loader Example
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Path to shared data
const sharedDataPath = path.join(__dirname, 'shared-data');
const usersFile = path.join(sharedDataPath, 'imports', 'users', 'users.csv');

// Load users
const users = [];
fs.createReadStream(usersFile)
  .pipe(csv())
  .on('data', (data) => users.push(data))
  .on('end', () => {
    console.log(`Loaded ${users.length} users`);
    // Add your processing logic here
  });
EOF
            ;;
    esac
    
    log_success "Stack $stack configurado para bulk loading"
    log_info "Ejemplo disponible en: $example_script"
}

# Main execution
main() {
    local command="${1:-}"
    
    # Validate shared-data structure first
    validate_shared_data || exit 1
    
    case $command in
        "list-entities")
            list_entities
            ;;
        "list-samples")
            list_samples
            ;;
        "list-templates")
            list_templates
            ;;
        "validate-csv")
            local file="${2:-}"
            if [ -z "$file" ]; then
                log_error "Especifica un archivo CSV con -f o --file"
                exit 1
            fi
            validate_csv "$file"
            ;;
        "generate-sample")
            local entity="${2:-users}"
            local stack="${3:-fastapi}"
            local size="${4:-small}"
            generate_sample "$entity" "$stack" "$size"
            ;;
        "setup-stack")
            local stack="${2:-}"
            if [ -z "$stack" ]; then
                log_error "Especifica un stack"
                exit 1
            fi
            setup_stack "$stack"
            ;;
        "compare-exports")
            log_info "Función compare-exports en desarrollo"
            ;;
        "convert-format")
            log_info "Función convert-format en desarrollo"
            ;;
        "-h"|"--help"|"help"|"")
            show_usage
            ;;
        *)
            log_error "Comando no reconocido: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"
