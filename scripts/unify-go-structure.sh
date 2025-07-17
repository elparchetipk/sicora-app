#!/bin/bash

# Script de Unificación de Estructura main.go para Microservicios Go SICORA
# Versión: 1.0
# Fecha: 4 de julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar encabezado
show_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}🏗️  UNIFICACIÓN ESTRUCTURA MAIN.GO SICORA${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

# Función para análisis de estructura actual
analyze_current_structure() {
    echo -e "${BLUE}📋 Analizando estructura actual...${NC}"
    echo ""
    
    # Buscar todos los main.go
    echo -e "${YELLOW}Servicios con main.go en raíz:${NC}"
    for service in */; do
        service_name=${service%/}
        if [ -f "$service/$service_name/main.go" ]; then
            echo -e "  ❌ $service_name/main.go"
        elif [ -f "$service/main.go" ]; then
            echo -e "  ❌ $service_name/main.go"
        fi
    done
    
    echo ""
    echo -e "${GREEN}Servicios con main.go en cmd/server/:${NC}"
    for service in */; do
        service_name=${service%/}
        if [ -f "$service/cmd/server/main.go" ]; then
            echo -e "  ✅ $service_name/cmd/server/main.go"
        fi
    done
    echo ""
}

# Función para migrar un servicio
migrate_service() {
    local service_dir="$1"
    local service_name=$(basename "$service_dir")
    
    echo -e "${BLUE}🔄 Migrando $service_name...${NC}"
    
    # Verificar si ya tiene la estructura correcta
    if [ -f "$service_dir/cmd/server/main.go" ]; then
        echo -e "  ✅ $service_name ya tiene estructura correcta"
        return 0
    fi
    
    # Buscar main.go en la raíz
    if [ -f "$service_dir/main.go" ]; then
        echo -e "  📁 Creando estructura cmd/server/"
        mkdir -p "$service_dir/cmd/server"
        
        echo -e "  📋 Moviendo main.go"
        mv "$service_dir/main.go" "$service_dir/cmd/server/main.go"
        
        # Actualizar imports si es necesario
        echo -e "  🔧 Actualizando imports relativos..."
        update_imports "$service_dir" "$service_name"
        
        echo -e "  ✅ $service_name migrado exitosamente"
        return 0
    fi
    
    echo -e "  ⚠️  $service_name: No se encontró main.go"
    return 1
}

# Función para actualizar imports
update_imports() {
    local service_dir="$1"
    local service_name="$2"
    local main_file="$service_dir/cmd/server/main.go"
    
    # Backup del archivo original
    cp "$main_file" "$main_file.backup"
    
    # Actualizar imports relativos (ejemplo común)
    sed -i 's|"\./|"../../|g' "$main_file"
    sed -i 's|"internal/|"../../internal/|g' "$main_file"
    sed -i 's|"pkg/|"../../pkg/|g' "$main_file"
    sed -i 's|"config/|"../../config/|g' "$main_file"
    sed -i 's|"handlers/|"../../handlers/|g' "$main_file"
    sed -i 's|"models/|"../../models/|g' "$main_file"
    sed -i 's|"routes/|"../../routes/|g' "$main_file"
    
    echo -e "    🔄 Imports actualizados (backup en main.go.backup)"
}

# Función para actualizar Dockerfile si existe
update_dockerfile() {
    local service_dir="$1"
    local service_name="$2"
    
    if [ -f "$service_dir/Dockerfile" ]; then
        echo -e "  🐳 Actualizando Dockerfile..."
        
        # Backup del Dockerfile
        cp "$service_dir/Dockerfile" "$service_dir/Dockerfile.backup"
        
        # Actualizar ruta en Dockerfile
        sed -i 's|COPY main.go|COPY cmd/server/main.go cmd/server/|g' "$service_dir/Dockerfile"
        sed -i 's|RUN go build -o main main.go|RUN go build -o main cmd/server/main.go|g' "$service_dir/Dockerfile"
        sed -i 's|CMD \["./main"\]|CMD ["./main"]|g' "$service_dir/Dockerfile"
        
        echo -e "    🔄 Dockerfile actualizado (backup en Dockerfile.backup)"
    fi
}

# Función para actualizar Makefile si existe
update_makefile() {
    local service_dir="$1"
    local service_name="$2"
    
    if [ -f "$service_dir/Makefile" ]; then
        echo -e "  🔧 Actualizando Makefile..."
        
        # Backup del Makefile
        cp "$service_dir/Makefile" "$service_dir/Makefile.backup"
        
        # Actualizar comandos de build
        sed -i 's|go build -o bin/|go build -o bin/|g' "$service_dir/Makefile"
        sed -i 's|main.go|cmd/server/main.go|g' "$service_dir/Makefile"
        
        echo -e "    🔄 Makefile actualizado (backup en Makefile.backup)"
    fi
}

# Función para crear estructura estándar si no existe
create_standard_structure() {
    local service_dir="$1"
    local service_name="$2"
    
    echo -e "${BLUE}📁 Creando estructura estándar para $service_name...${NC}"
    
    # Crear directorios estándar si no existen
    mkdir -p "$service_dir/cmd/server"
    mkdir -p "$service_dir/internal/config"
    mkdir -p "$service_dir/internal/handlers"
    mkdir -p "$service_dir/internal/models"
    mkdir -p "$service_dir/internal/routes"
    mkdir -p "$service_dir/internal/services"
    mkdir -p "$service_dir/pkg"
    mkdir -p "$service_dir/docs"
    
    echo -e "  ✅ Estructura estándar creada"
}

# Función para generar reporte final
generate_report() {
    echo ""
    echo -e "${BLUE}📊 REPORTE DE MIGRACIÓN${NC}"
    echo -e "${BLUE}========================${NC}"
    
    local migrated=0
    local already_correct=0
    local errors=0
    
    for service in */; do
        service_name=${service%/}
        if [ -f "$service/cmd/server/main.go" ]; then
            echo -e "✅ $service_name: Estructura correcta"
            already_correct=$((already_correct + 1))
        elif [ -f "$service/main.go" ]; then
            echo -e "❌ $service_name: Requiere migración"
            errors=$((errors + 1))
        else
            echo -e "⚠️  $service_name: Sin main.go encontrado"
        fi
    done
    
    echo ""
    echo -e "${GREEN}📈 Estadísticas:${NC}"
    echo -e "  ✅ Servicios con estructura correcta: $already_correct"
    echo -e "  🔄 Servicios migrados: $migrated"
    echo -e "  ❌ Servicios con errores: $errors"
    
    echo ""
    echo -e "${BLUE}📋 Estructura estándar recomendada:${NC}"
    echo "servicio/"
    echo "├── cmd/"
    echo "│   └── server/"
    echo "│       └── main.go"
    echo "├── internal/"
    echo "│   ├── config/"
    echo "│   ├── handlers/"
    echo "│   ├── models/"
    echo "│   ├── routes/"
    echo "│   └── services/"
    echo "├── pkg/"
    echo "├── docs/"
    echo "├── Dockerfile"
    echo "├── Makefile"
    echo "└── go.mod"
}

# Función principal
main() {
    show_header
    
    # Verificar que estamos en el directorio correcto
    if [ ! -d "userservice" ] || [ ! -d "scheduleservice" ]; then
        echo -e "${RED}❌ Error: Ejecutar desde sicora-be-go/${NC}"
        exit 1
    fi
    
    analyze_current_structure
    
    echo -e "${YELLOW}¿Deseas proceder con la migración? (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}🚀 Iniciando migración...${NC}"
        echo ""
        
        # Servicios que necesitan migración
        services_to_migrate=()
        
        for service in */; do
            service_name=${service%/}
            if [ -f "$service/main.go" ] && [ ! -f "$service/cmd/server/main.go" ]; then
                services_to_migrate+=("$service")
            fi
        done
        
        for service in "${services_to_migrate[@]}"; do
            migrate_service "$service"
            update_dockerfile "$service" "$(basename "$service")"
            update_makefile "$service" "$(basename "$service")"
            echo ""
        done
        
        echo -e "${GREEN}✅ Migración completada${NC}"
    else
        echo -e "${YELLOW}🚫 Migración cancelada${NC}"
    fi
    
    generate_report
}

# Ejecutar función principal
main "$@"
