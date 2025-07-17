#!/bin/bash

# Script de inicio rápido para SICORA Data Loader
# Autor: GitHub Copilot
# Fecha: $(date '+%Y-%m-%d')

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}🚀 SICORA DATA LOADER - INICIO RÁPIDO${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar Python
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_message "Python detectado: $PYTHON_VERSION"
    else
        print_error "Python 3 no encontrado. Instalar Python 3.8 o superior."
        exit 1
    fi
}

# Configurar entorno virtual
setup_venv() {
    if [ ! -d "venv" ]; then
        print_message "Creando entorno virtual..."
        python3 -m venv venv
    else
        print_message "Entorno virtual ya existe"
    fi
    
    print_message "Activando entorno virtual..."
    source venv/bin/activate
    
    print_message "Actualizando pip..."
    pip install --upgrade pip
}

# Instalar dependencias
install_dependencies() {
    print_message "Instalando dependencias..."
    pip install -r requirements.txt
    
    print_message "Verificando instalación de Streamlit..."
    streamlit --version
}

# Configurar entorno
setup_environment() {
    if [ ! -f ".env" ]; then
        print_warning "Archivo .env no encontrado. Copiando desde .env.example..."
        cp .env.example .env
        print_warning "⚠️  Edita el archivo .env con tu configuración de base de datos"
    else
        print_message "Archivo .env ya existe"
    fi
}

# Verificar base de datos
check_database() {
    print_message "Verificando conexión a base de datos..."
    
    # Intentar importar y probar conexión
    python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.append('.')
from config.database import db_config

try:
    if db_config.test_connection():
        print('✅ Conexión a base de datos exitosa')
        
        db_info = db_config.get_database_info()
        if 'error' not in db_info:
            print(f'📊 Base de datos: {db_info[\"database\"]}')
            print(f'🏠 Host: {db_info[\"host\"]}:{db_info[\"port\"]}')
            print(f'📋 Schemas encontrados: {len(db_info[\"schemas\"])}')
            for schema in db_info[\"schemas\"]:
                print(f'   - {schema}')
        else:
            print(f'⚠️  Error obteniendo info: {db_info[\"error\"]}')
    else:
        print('❌ Error de conexión a base de datos')
        print('Verifica la configuración en .env')
        exit(1)
except Exception as e:
    print(f'💥 Error: {str(e)}')
    print('Verifica que PostgreSQL esté corriendo y la configuración sea correcta')
    exit(1)
"
}

# Ejecutar aplicación
run_app() {
    print_message "Iniciando SICORA Data Loader..."
    echo ""
    echo -e "${GREEN}🎉 Aplicación lista! Abriendo en el navegador...${NC}"
    echo ""
    echo -e "${YELLOW}📋 URLs importantes:${NC}"
    echo -e "${YELLOW}   - Aplicación: http://localhost:8501${NC}"
    echo -e "${YELLOW}   - Documentación: README.md${NC}"
    echo ""
    echo -e "${YELLOW}💡 Consejos:${NC}"
    echo -e "${YELLOW}   - Usa Ctrl+C para detener la aplicación${NC}"
    echo -e "${YELLOW}   - Los logs se guardan en data_loader.log${NC}"
    echo -e "${YELLOW}   - Archivos de ejemplo en /examples (si existen)${NC}"
    echo ""
    
    streamlit run app.py --server.port 8501 --server.address localhost
}

# Mostrar ayuda
show_help() {
    echo "Uso: ./start.sh [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  setup    Solo configurar entorno (sin ejecutar)"
    echo "  check    Solo verificar configuración"
    echo "  run      Solo ejecutar (asume configuración lista)"
    echo "  help     Mostrar esta ayuda"
    echo ""
    echo "Sin opciones: configurar y ejecutar completo"
}

# Función principal
main() {
    print_header
    
    case "${1:-}" in
        "setup")
            check_python
            setup_venv
            install_dependencies
            setup_environment
            print_message "✅ Configuración completada. Ejecuta './start.sh run' para iniciar."
            ;;
        "check")
            setup_environment
            check_database
            print_message "✅ Verificación completada."
            ;;
        "run")
            source venv/bin/activate 2>/dev/null || true
            check_database
            run_app
            ;;
        "help")
            show_help
            ;;
        "")
            check_python
            setup_venv
            install_dependencies
            setup_environment
            check_database
            run_app
            ;;
        *)
            print_error "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
