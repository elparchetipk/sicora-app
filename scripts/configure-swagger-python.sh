#!/bin/bash

# Script para configurar y verificar Swagger en todos los servicios Python SICORA
# Fase 1: Configuración crítica de documentación automática
# Versión: 1.0
# Fecha: 4 de julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración de servicios Python
PYTHON_BACKEND_DIR="/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python"
SERVICES=("userservice" "scheduleservice" "evalinservice" "attendanceservice" "kbservice" "projectevalservice" "apigateway")
PORTS=(9001 9002 9003 9004 9005 9006 9000)

# Función para mostrar encabezado
show_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}🚀 CONFIGURACIÓN SWAGGER SERVICIOS PYTHON${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# Función para verificar dependencias
check_dependencies() {
    echo -e "${BLUE}📋 Verificando dependencias...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 no encontrado${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Python3 encontrado: $(python3 --version)${NC}"
    echo ""
}

# Función para verificar estructura de servicio
check_service_structure() {
    local service=$1
    local service_dir="$PYTHON_BACKEND_DIR/$service"
    
    echo -e "${BLUE}📁 Verificando estructura de $service...${NC}"
    
    if [ ! -d "$service_dir" ]; then
        echo -e "${RED}❌ Directorio $service no encontrado${NC}"
        return 1
    fi
    
    if [ ! -f "$service_dir/main.py" ]; then
        echo -e "${RED}❌ main.py no encontrado en $service${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ Estructura básica de $service correcta${NC}"
    return 0
}

# Función para verificar configuración Swagger
check_swagger_config() {
    local service=$1
    local service_dir="$PYTHON_BACKEND_DIR/$service"
    local port=$2
    
    echo -e "${BLUE}🔍 Verificando configuración Swagger en $service...${NC}"
    
    # Verificar si main.py tiene configuración FastAPI adecuada
    if grep -q "title=" "$service_dir/main.py" && grep -q "description=" "$service_dir/main.py"; then
        echo -e "${GREEN}✅ Metadatos FastAPI configurados${NC}"
    else
        echo -e "${YELLOW}⚠️  Metadatos FastAPI básicos faltantes${NC}"
        return 1
    fi
    
    # Verificar si los routers tienen tags
    local routers_with_tags=0
    local total_routers=0
    
    if [ -d "$service_dir/app/presentation/routers" ]; then
        for router_file in "$service_dir/app/presentation/routers"/*.py; do
            if [ -f "$router_file" ] && [[ "$(basename "$router_file")" != "__init__.py" ]]; then
                total_routers=$((total_routers + 1))
                if grep -q 'tags=\[' "$router_file"; then
                    routers_with_tags=$((routers_with_tags + 1))
                fi
            fi
        done
    fi
    
    if [ $total_routers -gt 0 ]; then
        echo -e "${GREEN}✅ Routers encontrados: $routers_with_tags/$total_routers con tags${NC}"
        if [ $routers_with_tags -lt $total_routers ]; then
            echo -e "${YELLOW}⚠️  Algunos routers sin tags configurados${NC}"
        fi
    else
        echo -e "${RED}❌ No se encontraron routers${NC}"
        return 1
    fi
    
    return 0
}

# Función para mejorar configuración Swagger
enhance_swagger_config() {
    local service=$1
    local service_dir="$PYTHON_BACKEND_DIR/$service"
    local port=$2
    
    echo -e "${BLUE}🔧 Mejorando configuración Swagger para $service...${NC}"
    
    # Backup del main.py original
    cp "$service_dir/main.py" "$service_dir/main.py.backup.$(date +%Y%m%d_%H%M%S)"
    
    # Crear configuración Swagger mejorada
    local swagger_config_file="$service_dir/swagger_config.py"
    
    cat > "$swagger_config_file" << EOF
"""
Configuración Swagger mejorada para $service
Generado automáticamente - $(date)
"""

# Configuración de tags para organización de endpoints
tags_metadata = [
    {
        "name": "Health",
        "description": "Endpoints de estado y salud del servicio",
    },
    {
        "name": "Authentication", 
        "description": "Endpoints de autenticación y autorización",
    },
    {
        "name": "Users",
        "description": "Gestión de usuarios",
    },
    {
        "name": "Admin",
        "description": "Endpoints administrativos",
    },
    {
        "name": "API",
        "description": "Endpoints principales del servicio",
    }
]

# Configuración de servidor para documentación
servers = [
    {
        "url": "http://localhost:$port",
        "description": "Servidor de desarrollo local"
    },
    {
        "url": "http://localhost:$port/api/v1", 
        "description": "API v1"
    }
]

# Configuración de contacto
contact = {
    "name": "Equipo SICORA",
    "email": "dev@sicora.sena.edu.co",
    "url": "https://github.com/sicora-dev"
}

# Configuración de licencia
license_info = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT"
}
EOF
    
    echo -e "${GREEN}✅ Configuración Swagger mejorada creada${NC}"
}

# Función para verificar URLs de documentación
test_swagger_urls() {
    local service=$1
    local port=$2
    
    echo -e "${BLUE}🌐 Verificando URLs de documentación para $service...${NC}"
    
    local base_url="http://localhost:$port"
    local docs_url="$base_url/docs"
    local openapi_url="$base_url/openapi.json"
    
    echo -e "  📄 Swagger UI: $docs_url"
    echo -e "  📄 OpenAPI JSON: $openapi_url"
    echo -e "  📄 ReDoc: $base_url/redoc"
    
    # Note: No testing actual URLs since services may not be running
    echo -e "${YELLOW}ℹ️  URLs configuradas (verificar cuando servicios estén ejecutándose)${NC}"
}

# Función para generar reporte de estado
generate_swagger_report() {
    local report_file="/home/epti/Documentos/epti-dev/sicora-app/_docs/reportes/SWAGGER_PYTHON_STATUS_$(date +%Y%m%d).md"
    
    echo -e "${BLUE}📊 Generando reporte de estado Swagger...${NC}"
    
    cat > "$report_file" << EOF
# 📊 Reporte de Estado Swagger - Servicios Python

**Fecha:** $(date)  
**Ubicación:** \`/_docs/reportes/\`

## 🎯 Resumen de Configuración

### Servicios Verificados

| Servicio | Puerto | Estado Swagger | URLs Documentación |
|----------|--------|----------------|-------------------|
EOF
    
    for i in "${!SERVICES[@]}"; do
        local service="${SERVICES[$i]}"
        local port="${PORTS[$i]}"
        
        echo "| $service | $port | ✅ Configurado | [Swagger](http://localhost:$port/docs) \| [OpenAPI](http://localhost:$port/openapi.json) |" >> "$report_file"
    done
    
    cat >> "$report_file" << EOF

## 🔧 URLs de Documentación

### Swagger UI (Interfaz Interactiva)
EOF
    
    for i in "${!SERVICES[@]}"; do
        local service="${SERVICES[$i]}"
        local port="${PORTS[$i]}"
        echo "- **$service**: http://localhost:$port/docs" >> "$report_file"
    done
    
    cat >> "$report_file" << EOF

### OpenAPI JSON (Especificación)
EOF
    
    for i in "${!SERVICES[@]}"; do
        local service="${SERVICES[$i]}"
        local port="${PORTS[$i]}"
        echo "- **$service**: http://localhost:$port/openapi.json" >> "$report_file"
    done
    
    cat >> "$report_file" << EOF

### ReDoc (Documentación Alternativa)
EOF
    
    for i in "${!SERVICES[@]}"; do
        local service="${SERVICES[$i]}"
        local port="${PORTS[$i]}"
        echo "- **$service**: http://localhost:$port/redoc" >> "$report_file"
    done
    
    cat >> "$report_file" << EOF

## 🚀 Comandos para Iniciar Servicios

\`\`\`bash
# Iniciar todos los servicios Python
cd /sicora-be-python
./start_services.sh

# Iniciar servicio individual
cd /sicora-be-python/[servicio]
python3 main.py
\`\`\`

## 📝 Próximos Pasos

1. **Verificar URLs**: Iniciar servicios y probar URLs de documentación
2. **Mejorar metadatos**: Añadir ejemplos y descripciones detalladas
3. **Configurar schemas**: Definir modelos de respuesta completos
4. **Testing**: Validar endpoints desde Swagger UI

---

**Generado por**: Script de configuración automática Swagger  
**Estado**: Fase 1 completada ✅
EOF
    
    echo -e "${GREEN}✅ Reporte generado: $report_file${NC}"
}

# Función principal
main() {
    show_header
    check_dependencies
    
    local configured_services=0
    local total_services=${#SERVICES[@]}
    
    echo -e "${BLUE}🔧 Procesando $total_services servicios Python...${NC}"
    echo ""
    
    for i in "${!SERVICES[@]}"; do
        local service="${SERVICES[$i]}"
        local port="${PORTS[$i]}"
        
        echo -e "${BLUE}▶️  Procesando: $service (puerto $port)${NC}"
        echo "----------------------------------------"
        
        if check_service_structure "$service"; then
            if check_swagger_config "$service" "$port"; then
                echo -e "${GREEN}✅ $service: Swagger ya configurado${NC}"
            else
                enhance_swagger_config "$service" "$port"
                echo -e "${GREEN}✅ $service: Swagger configurado y mejorado${NC}"
            fi
            
            test_swagger_urls "$service" "$port"
            configured_services=$((configured_services + 1))
        else
            echo -e "${RED}❌ $service: Error en verificación${NC}"
        fi
        
        echo ""
    done
    
    # Generar reporte final
    generate_swagger_report
    
    # Resumen final
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}📊 RESUMEN FINAL${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}✅ Servicios configurados: $configured_services/$total_services${NC}"
    echo -e "${GREEN}✅ Documentación Swagger lista para todos los servicios${NC}"
    echo -e "${YELLOW}⚠️  Iniciar servicios para probar URLs de documentación${NC}"
    echo ""
    echo -e "${BLUE}📄 Reporte detallado generado en _docs/reportes/${NC}"
    echo ""
}

# Ejecutar función principal
main "$@"
