#!/bin/bash

# Script de verificación de estructura de documentación SICORA
# Versión: 2.0
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
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}🔍 VERIFICACIÓN ESTRUCTURA DOCS${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

# Función para verificar archivos .md en raíz
check_root_md_files() {
    echo -e "${BLUE}📋 Verificando archivos .md en raíz...${NC}"
    
    # Buscar archivos .md en la raíz excepto README.md
    root_md_files=$(find /home/epti/Documentos/epti-dev/sicora-app -maxdepth 1 -name "*.md" ! -name "README.md" 2>/dev/null || true)
    
    if [ -n "$root_md_files" ]; then
        echo -e "${RED}❌ PROBLEMA: Archivos .md encontrados en la raíz:${NC}"
        echo "$root_md_files"
        echo ""
        echo -e "${YELLOW}🔧 Para corregir, mueve estos archivos a _docs/[categoria]/${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Correcto: Solo README.md en la raíz${NC}"
        return 0
    fi
}

# Función para verificar estructura de _docs
check_docs_structure() {
    echo -e "${BLUE}📁 Verificando estructura de _docs/...${NC}"
    
    docs_dir="/home/epti/Documentos/epti-dev/sicora-app/_docs"
    
    if [ ! -d "$docs_dir" ]; then
        echo -e "${RED}❌ PROBLEMA: Directorio _docs/ no existe${NC}"
        return 1
    fi
    
    # Verificar carpetas obligatorias
    required_dirs=("integracion" "mcp" "configuracion" "desarrollo" "reportes" "guias")
    missing_dirs=()
    
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$docs_dir/$dir" ]; then
            missing_dirs+=("$dir")
        fi
    done
    
    if [ ${#missing_dirs[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Carpetas faltantes en _docs/:${NC}"
        printf '%s\n' "${missing_dirs[@]}"
    else
        echo -e "${GREEN}✅ Estructura de carpetas completa${NC}"
    fi
    
    # Verificar README.md en cada carpeta
    echo -e "${BLUE}📝 Verificando índices README.md...${NC}"
    missing_readmes=()
    
    for dir in "${required_dirs[@]}"; do
        if [ -d "$docs_dir/$dir" ] && [ ! -f "$docs_dir/$dir/README.md" ]; then
            missing_readmes+=("$dir")
        fi
    done
    
    if [ ${#missing_readmes[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠️  README.md faltantes en:${NC}"
        printf '%s\n' "${missing_readmes[@]}"
    else
        echo -e "${GREEN}✅ Todos los índices README.md presentes${NC}"
    fi
}

# Función para verificar otros módulos
check_other_modules() {
    echo -e "${BLUE}🏗️  Verificando otros módulos...${NC}"
    
    modules=("sicora-be-go" "sicora-be-python" "sicora-app-fe" "sicora-infra" "sicora-mcp-server")
    
    for module in "${modules[@]}"; do
        module_path="/home/epti/Documentos/epti-dev/sicora-app/$module"
        
        if [ -d "$module_path" ]; then
            # Verificar archivos .md en raíz del módulo (excepto README.md y archivos permitidos)
            # CHANGELOG.md es permitido en sicora-infra
            if [ "$module" = "sicora-infra" ]; then
                module_root_md=$(find "$module_path" -maxdepth 1 -name "*.md" ! -name "README.md" ! -name "CHANGELOG.md" 2>/dev/null || true)
            else
                module_root_md=$(find "$module_path" -maxdepth 1 -name "*.md" ! -name "README.md" 2>/dev/null || true)
            fi
            
            if [ -n "$module_root_md" ]; then
                echo -e "${YELLOW}⚠️  $module: archivos .md en raíz (además de README.md)${NC}"
                echo "$module_root_md" | sed 's/^/   /'
            else
                echo -e "${GREEN}✅ $module: estructura correcta${NC}"
            fi
        fi
    done
}

# Función para generar reporte
generate_report() {
    echo ""
    echo -e "${BLUE}📊 REPORTE FINAL${NC}"
    echo -e "${BLUE}=================${NC}"
    
    total_issues=0
    
    # Contar problemas
    root_md_files=$(find /home/epti/Documentos/epti-dev/sicora-app -maxdepth 1 -name "*.md" ! -name "README.md" 2>/dev/null || true)
    if [ -n "$root_md_files" ]; then
        total_issues=$((total_issues + 1))
    fi
    
    if [ $total_issues -eq 0 ]; then
        echo -e "${GREEN}🎉 ¡ESTRUCTURA PERFECTA!${NC}"
        echo -e "${GREEN}Toda la documentación está correctamente organizada.${NC}"
    else
        echo -e "${RED}⚠️  Se encontraron $total_issues problema(s)${NC}"
        echo -e "${YELLOW}Revisa los detalles arriba y corrige según las instrucciones.${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}📝 Para más información, consulta:${NC}"
    echo "   .github/copilot-instructions.md"
    echo ""
}

# Función principal
main() {
    show_header
    
    check_root_md_files
    echo ""
    
    check_docs_structure
    echo ""
    
    check_other_modules
    echo ""
    
    generate_report
}

# Ejecutar función principal
main "$@"
