#!/bin/bash
# Script de Inicialización Git para SICORA - Versión Mínima
# Configuración básica para desarrollo inicial

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Funciones básicas
log() {
    echo -e "${BLUE}[INIT-GIT]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo -e "${BLUE}🚀 Inicializando Git para SICORA (Configuración Mínima)${NC}"
echo "========================================================"

# Verificar si ya estamos en un repositorio Git
if [ -d ".git" ]; then
    log "Repositorio ya inicializado"
else
    log "Inicializando repositorio Git..."
    git init
    success "Repositorio Git inicializado"
fi

# Configuración básica del usuario
log "Configurando usuario Git..."
git config user.name "SICORA Team"
git config user.email "desarrollo@onevision.com"
success "Usuario Git configurado"

# Configuración mínima esencial
log "Aplicando configuración mínima..."
git config core.autocrlf false
git config pull.rebase false  # Usar merge por defecto (más simple)
git config push.default simple
git config init.defaultBranch main

# Solo aliases esenciales
git config alias.st status
git config alias.lg "log --oneline --graph --decorate"
git config alias.last "log -1 HEAD"

success "Configuración básica aplicada"

# Configuración de hooks mínima (sin enforcement estricto)
log "Configurando hooks básicos..."
mkdir -p .githooks

# Hook de pre-commit mínimo (solo advertencias, no bloquea)
cat > .githooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook mínimo - Solo advertencias

echo "🔍 Verificación básica antes del commit..."

# Verificar archivos grandes (solo advertencia)
large_files=$(find . -type f -size +50M -not -path "./.git/*" 2>/dev/null || true)
if [ -n "$large_files" ]; then
    echo "⚠️  Archivos grandes detectados:"
    echo "$large_files"
    echo "Considera usar Git LFS para archivos grandes"
fi

# Verificar credenciales en código (solo advertencia)
if git diff --cached --name-only | xargs grep -l "password\|secret\|key\|token" 2>/dev/null; then
    echo "⚠️  Posibles credenciales detectadas en el código"
    echo "Revisa los archivos antes de confirmar el commit"
fi

echo "✅ Verificación básica completada"
exit 0  # Nunca bloquear en etapa inicial
EOF

chmod +x .githooks/pre-commit
git config core.hooksPath .githooks

success "Hooks básicos configurados (modo no-bloqueante)"

# Crear .gitignore básico si no existe
if [ ! -f ".gitignore" ]; then
    log "Creando .gitignore básico..."
    cat > .gitignore << 'EOF'
# Node.js
node_modules/
npm-debug.log*
pnpm-debug.log*

# Environment variables
.env
.env.local

# Build directories
dist/
build/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
venv/

# Go
*.exe
*.out
vendor/

# Docker
docker-compose.override.yml

# Temporary files
*.tmp
*.log

# SICORA specific
sicora-data/
backup/
EOF
    success ".gitignore básico creado"
else
    log ".gitignore ya existe"
fi

# Verificar configuración básica
log "Verificando configuración..."
echo "  Usuario: $(git config user.name) <$(git config user.email)>"
echo "  Rama por defecto: $(git config init.defaultBranch)"

# Crear primer commit si no hay commits (simplificado)
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    log "Creando commit inicial..."
    git add .gitignore .githooks/ 2>/dev/null || true
    git commit -m "chore: configuración inicial Git para SICORA

- Configuración básica de Git
- .gitignore esencial
- Hooks básicos no-bloqueantes" || true
    success "Commit inicial creado"
else
    log "El repositorio ya tiene commits"
fi

echo ""
success "🎉 Inicialización Git completada (configuración mínima)"
echo ""
echo "💡 Próximos pasos:"
echo "1. Para commits rápidos: git add . && git commit --no-verify -m 'mensaje'"
echo "2. Para autocommit: ./scripts/universal-autocommit.sh"
echo "3. Ver estado: git status"
echo ""
echo "ℹ️  Esta es una configuración mínima para desarrollo inicial."
echo "   Para configuración completa, ejecutar con --full más adelante."
