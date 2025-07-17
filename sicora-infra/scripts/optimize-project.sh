#!/bin/bash

# =============================================================================
# PROJECT PERFORMANCE OPTIMIZER - SICORA APP MULTISTACK
# =============================================================================
# Propósito: Optimizar performance del proyecto y reducir overhead
# Fecha: 15 de junio de 2025
# =============================================================================

set -euo pipefail

echo "⚡ PROJECT PERFORMANCE OPTIMIZER"
echo "================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Función para mostrar tamaño de directorios
show_sizes() {
    echo "📊 TAMAÑOS DE DIRECTORIO:"
    du -sh */ 2>/dev/null | sort -hr | head -10
    echo ""
}

# Función para limpiar archivos temporales
cleanup_temp_files() {
    echo "🧹 Limpiando archivos temporales..."
    
    # Archivos temporales comunes
    find . -name "*.tmp" -delete 2>/dev/null || true
    find . -name "*.temp" -delete 2>/dev/null || true
    find . -name "*~" -delete 2>/dev/null || true
    find . -name ".DS_Store" -delete 2>/dev/null || true
    find . -name "Thumbs.db" -delete 2>/dev/null || true
    
    # Logs antiguos
    find . -name "*.log" -mtime +7 -delete 2>/dev/null || true
    
    # Cachés de Python
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Cachés de Node.js
    find . -name "node_modules" -type d -prune -o -name ".npm" -type d -exec rm -rf {} + 2>/dev/null || true
    
    echo "✅ Limpieza completada"
}

# Función para optimizar .gitignore
optimize_gitignore() {
    echo "🔧 Optimizando .gitignore..."
    
    # Backup del .gitignore actual
    cp .gitignore .gitignore.backup 2>/dev/null || true
    
    # Crear .gitignore optimizado
    cat > .gitignore << 'EOF'
# SICORA-APP MULTISTACK - GITIGNORE OPTIMIZADO
# ============================================

# ENTORNOS VIRTUALES Y DEPENDENCIAS
venv/
venv_*/
node_modules/
.venv/
*.egg-info/

# ARCHIVOS DE BUILD Y COMPILACIÓN
build/
dist/
target/
*.class
*.jar
*.war

# CACHÉS Y TEMPORALES
__pycache__/
*.pyc
*.pyo
.cache/
.pytest_cache/
.mypy_cache/

# LOGS Y DATOS SENSIBLES
*.log
logs/
shared-data/imports/**/*
shared-data/exports/**/*
shared-data/samples/**/*
!shared-data/**/.gitkeep
!shared-data/**/README.md

# CONFIGURACIONES LOCALES
.env
.env.local
*.local
config.local.*

# ARCHIVOS DE SISTEMA
.DS_Store
Thumbs.db
*.swp
*.swo

# IDEs
.vscode/settings.json
.idea/
*.iml

# MANTENER ESTRUCTURA
!shared-data/templates/*.template.*
!shared-data/schemas/
EOF
    
    echo "✅ .gitignore optimizado"
}

# Función para comprimir archivos grandes
compress_large_files() {
    echo "📦 Comprimiendo archivos grandes..."
    
    # Comprimir documentación grande
    if [ -d "_docs" ]; then
        find _docs -name "*.md" -size +100k -exec gzip -k {} \; 2>/dev/null || true
    fi
    
    # Comprimir logs antiguos
    find . -name "*.log" -size +10k -exec gzip {} \; 2>/dev/null || true
    
    echo "✅ Compresión completada"
}

# Función para optimizar estructura de directorios
optimize_structure() {
    echo "🏗️ Optimizando estructura..."
    
    # Crear directorios necesarios pero vacíos con .gitkeep mínimo
    for dir in "shared-data/imports/users" "shared-data/imports/schedules" "shared-data/exports/fastapi"; do
        mkdir -p "$dir"
        echo "# Protected directory" > "$dir/.gitkeep"
    done
    
    # Remover directorios vacíos innecesarios
    find . -type d -empty -not -path "./.git/*" -delete 2>/dev/null || true
    
    echo "✅ Estructura optimizada"
}

# Función principal de optimización
main_optimization() {
    echo "🚀 Iniciando optimización completa..."
    echo ""
    
    show_sizes
    cleanup_temp_files
    optimize_gitignore
    compress_large_files
    optimize_structure
    
    echo ""
    echo "📊 DESPUÉS DE OPTIMIZACIÓN:"
    show_sizes
    
    echo ""
    echo "✅ OPTIMIZACIÓN COMPLETADA"
    echo "🎯 Beneficios:"
    echo "   - Archivos temporales eliminados"
    echo "   - .gitignore optimizado"
    echo "   - Estructura simplificada"
    echo "   - Performance mejorada"
    echo ""
    echo "🔧 Para setup rápido de shared-data:"
    echo "   ./tools/shared-data-fast-setup.sh"
}

# Función para mostrar ayuda
show_help() {
    echo "USO: $0 [OPCIÓN]"
    echo ""
    echo "OPCIONES:"
    echo "  --full          Optimización completa (recomendado)"
    echo "  --cleanup       Solo limpiar archivos temporales"
    echo "  --gitignore     Solo optimizar .gitignore"
    echo "  --sizes         Solo mostrar tamaños"
    echo "  --help          Mostrar esta ayuda"
    echo ""
}

# Procesar argumentos
case "${1:-}" in
    "--full"|"")
        main_optimization
        ;;
    "--cleanup")
        cleanup_temp_files
        ;;
    "--gitignore")
        optimize_gitignore
        ;;
    "--sizes")
        show_sizes
        ;;
    "--help"|"-h")
        show_help
        ;;
    *)
        echo "❌ Opción no válida: $1"
        show_help
        exit 1
        ;;
esac
