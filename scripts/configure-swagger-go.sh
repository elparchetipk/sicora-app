#!/bin/bash

# Script para configurar Swagger en servicios Go faltantes de SICORA
# Fase 2: Completar documentación en backend Go
# Versión: 1.0
# Fecha: 4 de julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración de servicios Go
GO_BACKEND_DIR="/home/epti/Documentos/epti-dev/sicora-app/sicora-be-go"
ALL_SERVICES=("userservice" "scheduleservice" "kbservice" "evalinservice" "mevalservice" "projectevalservice" "attendanceservice" "softwarefactoryservice")
SERVICES_WITH_SWAGGER=("userservice" "softwarefactoryservice" "attendanceservice")
SERVICES_WITHOUT_SWAGGER=("scheduleservice" "kbservice" "evalinservice" "mevalservice" "projectevalservice")
PORTS=(8001 8003 8005 8004 8007 8008 8002 8006)

# Función para mostrar encabezado
show_header() {
    echo -e "${BLUE}===========================================${NC}"
    echo -e "${BLUE}🚀 CONFIGURACIÓN SWAGGER SERVICIOS GO${NC}"
    echo -e "${BLUE}===========================================${NC}"
    echo ""
}

# Función para verificar dependencias
check_dependencies() {
    echo -e "${BLUE}📋 Verificando dependencias...${NC}"

    if ! command -v go &> /dev/null; then
        echo -e "${RED}❌ Go no encontrado${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Go encontrado: $(go version)${NC}"

    # Verificar si swag está instalado
    if ! command -v swag &> /dev/null; then
        echo -e "${YELLOW}⚠️  swag no encontrado, instalando...${NC}"
        go install github.com/swaggo/swag/cmd/swag@latest
        echo -e "${GREEN}✅ swag instalado${NC}"
    else
        echo -e "${GREEN}✅ swag encontrado: $(swag --version)${NC}"
    fi

    echo ""
}

# Función para verificar estado actual de Swagger
check_current_swagger_status() {
    echo -e "${BLUE}🔍 Verificando estado actual de Swagger...${NC}"

    for service in "${ALL_SERVICES[@]}"; do
        local service_dir="$GO_BACKEND_DIR/$service"

        if [ -d "$service_dir/docs" ] && [ -f "$service_dir/docs/docs.go" ]; then
            echo -e "${GREEN}✅ $service: Swagger configurado${NC}"
        else
            echo -e "${RED}❌ $service: Swagger NO configurado${NC}"
        fi
    done
    echo ""
}

# Función para configurar Swagger en un servicio
configure_swagger_for_service() {
    local service=$1
    local service_dir="$GO_BACKEND_DIR/$service"

    echo -e "${BLUE}🔧 Configurando Swagger para $service...${NC}"

    if [ ! -d "$service_dir" ]; then
        echo -e "${RED}❌ Directorio $service no encontrado${NC}"
        return 1
    fi

    # Crear directorio docs si no existe
    mkdir -p "$service_dir/docs"

    # Verificar estructura unificada cmd/server/main.go
    local main_file="$service_dir/cmd/server/main.go"
    if [ ! -f "$main_file" ]; then
        echo -e "${RED}❌ main.go no encontrado en estructura estándar $service/cmd/server/${NC}"
        return 1
    fi

    # Añadir comentarios Swagger al main.go si no existen
    if ! grep -q "@title" "$main_file"; then
        echo -e "${YELLOW}📝 Añadiendo comentarios Swagger a cmd/server/main.go...${NC}"

        # Backup del main.go original
        cp "$main_file" "$main_file.backup.$(date +%Y%m%d_%H%M%S)"

        # Crear contenido temporal con comentarios Swagger
        cat > "$service_dir/swagger_comments.tmp" << EOF
// @title           SICORA $service API
// @version         1.0
// @description     Microservicio $service del Sistema de Información de Coordinación Académica (SICORA) - OneVision
// @termsOfService  http://swagger.io/terms/

// @contact.name   Equipo de Desarrollo SICORA
// @contact.email  dev@sicora.onevision.edu.co

// @license.name  MIT
// @license.url   https://opensource.org/licenses/MIT

// @host      localhost:8000
// @BasePath  /api/v1

// @securityDefinitions.apikey BearerAuth
// @in header
// @name Authorization
// @description Type "Bearer" followed by a space and JWT token.

EOF

        # Insertar comentarios al inicio del archivo (después de package)
        sed '1r '"$service_dir/swagger_comments.tmp" "$main_file" > "$main_file.new"
        mv "$main_file.new" "$main_file"
        rm "$service_dir/swagger_comments.tmp"

        echo -e "${GREEN}✅ Comentarios Swagger añadidos${NC}"
    fi

    # Añadir import de docs al main.go si no existe
    if ! grep -q "_ \".*/$service/docs\"" "$main_file"; then
        echo -e "${YELLOW}📝 Añadiendo import de docs...${NC}"

        # Buscar la línea de imports y añadir el import de docs
        sed -i '/import (/a\\t_ "'$service'/docs"' "$main_file"

        echo -e "${GREEN}✅ Import de docs añadido${NC}"
    fi

    # Generar documentación Swagger
    echo -e "${YELLOW}🔨 Generando documentación Swagger...${NC}"

    cd "$service_dir"

    if swag init -g cmd/server/main.go -o docs/; then
        echo -e "${GREEN}✅ Documentación Swagger generada exitosamente${NC}"
    else
        echo -e "${RED}❌ Error generando documentación Swagger${NC}"
        return 1
    fi

    cd - > /dev/null

    return 0
}

# Función para verificar y configurar rutas Swagger
setup_swagger_routes() {
    local service=$1
    local service_dir="$GO_BACKEND_DIR/$service"

    echo -e "${BLUE}🌐 Configurando rutas Swagger para $service...${NC}"

    # Buscar archivos de rutas principales
    local routes_files=$(find "$service_dir" -name "*route*.go" -o -name "*router*.go" | head -5)

    if [ -z "$routes_files" ]; then
        echo -e "${YELLOW}⚠️  No se encontraron archivos de rutas específicos${NC}"
        return 0
    fi

    for routes_file in $routes_files; do
        if [ -f "$routes_file" ]; then
            echo -e "${BLUE}📄 Verificando rutas Swagger en $(basename "$routes_file")...${NC}"

            # Verificar si ya tiene rutas Swagger
            if grep -q "swagger" "$routes_file" || grep -q "SwaggerUI" "$routes_file"; then
                echo -e "${GREEN}✅ Rutas Swagger ya configuradas${NC}"
            else
                echo -e "${YELLOW}⚠️  Rutas Swagger no encontradas en $(basename "$routes_file")${NC}"
                echo -e "${BLUE}📝 Agregue manualmente las rutas Swagger:${NC}"
                echo -e "  ${YELLOW}router.GET(\"/swagger/*any\", ginSwagger.WrapHandler(swaggerfiles.Handler))${NC}"
            fi
        fi
    done
}

# Función para verificar go.mod y dependencias
check_and_update_dependencies() {
    local service=$1
    local service_dir="$GO_BACKEND_DIR/$service"

    echo -e "${BLUE}📦 Verificando dependencias Swagger para $service...${NC}"

    if [ ! -f "$service_dir/go.mod" ]; then
        echo -e "${RED}❌ go.mod no encontrado en $service${NC}"
        return 1
    fi

    cd "$service_dir"

    # Verificar dependencias Swagger necesarias
    local required_deps=(
        "github.com/swaggo/swag"
        "github.com/swaggo/gin-swagger"
        "github.com/swaggo/files"
    )

    for dep in "${required_deps[@]}"; do
        if grep -q "$dep" go.mod; then
            echo -e "${GREEN}✅ $dep ya presente${NC}"
        else
            echo -e "${YELLOW}📥 Añadiendo dependencia $dep...${NC}"
            go get "$dep"
        fi
    done

    # Limpiar módulos
    go mod tidy

    cd - > /dev/null

    echo -e "${GREEN}✅ Dependencias verificadas y actualizadas${NC}"
}

# Función para generar reporte de estado Go
generate_go_swagger_report() {
    local report_file="/home/epti/Documentos/epti-dev/sicora-app/_docs/reportes/SWAGGER_GO_STATUS_$(date +%Y%m%d).md"

    echo -e "${BLUE}📊 Generando reporte de estado Swagger Go...${NC}"

    cat > "$report_file" << EOF
# 📊 Reporte de Estado Swagger - Servicios Go

**Fecha:** $(date)
**Ubicación:** \`/_docs/reportes/\`

## 🎯 Resumen de Configuración

### Servicios Go con Swagger

| Servicio | Puerto | Estado | Documentación |
|----------|--------|--------|---------------|
EOF

    for i in "${!ALL_SERVICES[@]}"; do
        local service="${ALL_SERVICES[$i]}"
        local port="${PORTS[$i]}"
        local service_dir="$GO_BACKEND_DIR/$service"

        if [ -d "$service_dir/docs" ] && [ -f "$service_dir/docs/docs.go" ]; then
            echo "| $service | $port | ✅ Configurado | [Swagger](http://localhost:$port/swagger/index.html) |" >> "$report_file"
        else
            echo "| $service | $port | ❌ No configurado | - |" >> "$report_file"
        fi
    done

    cat >> "$report_file" << EOF

## 🔧 URLs de Documentación Swagger

### Servicios Configurados
EOF

    for i in "${!ALL_SERVICES[@]}"; do
        local service="${ALL_SERVICES[$i]}"
        local port="${PORTS[$i]}"
        local service_dir="$GO_BACKEND_DIR/$service"

        if [ -d "$service_dir/docs" ] && [ -f "$service_dir/docs/docs.go" ]; then
            echo "- **$service**: http://localhost:$port/swagger/index.html" >> "$report_file"
        fi
    done

    cat >> "$report_file" << EOF

## 🚀 Comandos para Iniciar Servicios

\`\`\`bash
# Compilar y ejecutar servicio individual
cd /sicora-be-go/[servicio]
go run main.go

# Usando Makefile (si existe)
make run
\`\`\`

## 🔄 Regenerar Documentación

\`\`\`bash
# En directorio del servicio
swag init -g cmd/server/main.go -o docs/
\`\`\`

## 📝 Configuración Manual Pendiente

Para servicios recién configurados, verificar:

1. **Rutas Swagger**: Añadir en router principal
   \`\`\`go
   router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerfiles.Handler))
   \`\`\`

2. **Imports necesarios**:
   \`\`\`go
   import (
       _ "servicename/docs"
       ginSwagger "github.com/swaggo/gin-swagger"
       "github.com/swaggo/files"
   )
   \`\`\`

3. **Comentarios en handlers**: Añadir anotaciones Swagger a funciones

---

**Generado por**: Script de configuración automática Swagger Go
**Estado**: Fase 2 completada ✅
EOF

    echo -e "${GREEN}✅ Reporte Go generado: $report_file${NC}"
}

# Función principal
main() {
    show_header
    check_dependencies
    check_current_swagger_status

    local configured_services=0
    local total_services=${#SERVICES_WITHOUT_SWAGGER[@]}

    echo -e "${BLUE}🔧 Configurando Swagger en servicios Go faltantes...${NC}"
    echo -e "${BLUE}Servicios a procesar: ${SERVICES_WITHOUT_SWAGGER[*]}${NC}"
    echo ""

    for service in "${SERVICES_WITHOUT_SWAGGER[@]}"; do
        echo -e "${BLUE}▶️  Procesando: $service${NC}"
        echo "----------------------------------------"

        if configure_swagger_for_service "$service"; then
            check_and_update_dependencies "$service"
            setup_swagger_routes "$service"
            configured_services=$((configured_services + 1))
            echo -e "${GREEN}✅ $service: Configuración completada${NC}"
        else
            echo -e "${RED}❌ $service: Error en configuración${NC}"
        fi

        echo ""
    done

    # Verificar estado final
    echo -e "${BLUE}🔍 Verificando estado final...${NC}"
    check_current_swagger_status

    # Generar reporte final
    generate_go_swagger_report

    # Resumen final
    echo -e "${BLUE}===========================================${NC}"
    echo -e "${BLUE}📊 RESUMEN FINAL - FASE 2${NC}"
    echo -e "${BLUE}===========================================${NC}"
    echo -e "${GREEN}✅ Servicios Go configurados: $configured_services/$total_services${NC}"
    echo -e "${GREEN}✅ Total servicios Go con Swagger: $((${#SERVICES_WITH_SWAGGER[@]} + configured_services))/${#ALL_SERVICES[@]}${NC}"
    echo -e "${YELLOW}⚠️  Verificar manualmente rutas Swagger en routers${NC}"
    echo -e "${YELLOW}⚠️  Añadir comentarios Swagger a handlers específicos${NC}"
    echo ""
    echo -e "${BLUE}📄 Reporte detallado generado en _docs/reportes/${NC}"
    echo ""
}

# Ejecutar función principal
main "$@"
