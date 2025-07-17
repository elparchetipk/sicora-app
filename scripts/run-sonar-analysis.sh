#!/bin/bash

# Script para ejecutar análisis SonarQube en SICORA
# Versión: 1.0

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Verificar si sonar-scanner está instalado
if ! command -v sonar-scanner &> /dev/null; then
    echo -e "${RED}❌ sonar-scanner no encontrado${NC}"
    echo -e "${YELLOW}Instalar desde: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/${NC}"
    exit 1
fi

# Función para análisis global
run_global_analysis() {
    echo -e "${BLUE}🌐 Ejecutando análisis SonarQube global...${NC}"
    
    cd /home/epti/Documentos/epti-dev/sicora-app
    sonar-scanner
    
    echo -e "${GREEN}✅ Análisis global completado${NC}"
}

# Función para análisis individual
run_service_analysis() {
    local service_type=$1
    local service_name=$2
    
    echo -e "${BLUE}🔍 Ejecutando análisis para $service_name ($service_type)...${NC}"
    
    if [ "$service_type" = "go" ]; then
        cd "/home/epti/Documentos/epti-dev/sicora-app/sicora-be-go/$service_name"
    elif [ "$service_type" = "python" ]; then
        cd "/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/$service_name"
    else
        echo -e "${RED}❌ Tipo de servicio inválido: $service_type${NC}"
        return 1
    fi
    
    if [ -f "sonar-project.properties" ]; then
        sonar-scanner
        echo -e "${GREEN}✅ Análisis completado para $service_name${NC}"
    else
        echo -e "${RED}❌ sonar-project.properties no encontrado${NC}"
        return 1
    fi
}

# Función de ayuda
show_help() {
    echo "Uso: $0 [opción]"
    echo ""
    echo "Opciones:"
    echo "  global                    Ejecutar análisis global del proyecto"
    echo "  service <tipo> <nombre>   Ejecutar análisis de servicio específico"
    echo "  list                      Mostrar servicios disponibles"
    echo "  help                      Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 global"
    echo "  $0 service go userservice"
    echo "  $0 service python scheduleservice"
}

# Función para listar servicios
list_services() {
    echo -e "${BLUE}📋 Servicios disponibles:${NC}"
    echo ""
    echo -e "${BLUE}Go Services:${NC}"
    echo "  userservice, scheduleservice, kbservice, evalinservice"
    echo "  mevalservice, projectevalservice, attendanceservice, softwarefactoryservice"
    echo ""
    echo -e "${BLUE}Python Services:${NC}"
    echo "  userservice, scheduleservice, evalinservice, attendanceservice"
    echo "  kbservice, projectevalservice, apigateway"
}

# Procesamiento de argumentos
case "${1:-help}" in
    "global")
        run_global_analysis
        ;;
    "service")
        if [ $# -ne 3 ]; then
            echo -e "${RED}❌ Uso: $0 service <tipo> <nombre>${NC}"
            exit 1
        fi
        run_service_analysis "$2" "$3"
        ;;
    "list")
        list_services
        ;;
    "help"|*)
        show_help
        ;;
esac
