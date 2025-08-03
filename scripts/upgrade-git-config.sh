#!/bin/bash
# Script para habilitar configuración Git completa en SICORA
# Usar cuando el proyecto esté más maduro

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[UPGRADE-GIT]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo -e "${BLUE}🚀 Actualizando a Configuración Git Completa${NC}"
echo "=============================================="

# Verificar que estamos en un repositorio Git
if [ ! -d ".git" ]; then
    echo "❌ No estás en un repositorio Git"
    echo "Ejecuta primero: ./scripts/init-git-sicora.sh"
    exit 1
fi

log "Aplicando configuración Git avanzada..."

# Configuraciones adicionales
git config core.safecrlf warn
git config pull.rebase true
git config rerere.enabled true
git config merge.ours.driver true

# Aliases adicionales
git config alias.co checkout
git config alias.br branch
git config alias.ci commit
git config alias.amend "commit --amend --no-edit"
git config alias.unstage "reset HEAD --"
git config alias.visual "!gitk"
git config alias.tree "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config alias.aliases "config --get-regexp alias"

success "Aliases avanzados configurados"

# Hook de pre-commit más estricto
log "Actualizando hooks a modo estricto..."

cat > .githooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook completo con validaciones estrictas

echo "🔍 Ejecutando validaciones completas..."

# Variables para control de errores
errors=0

# Verificar archivos grandes (bloqueante)
large_files=$(find . -type f -size +50M -not -path "./.git/*" 2>/dev/null || true)
if [ -n "$large_files" ]; then
    echo "❌ Archivos demasiado grandes detectados:"
    echo "$large_files"
    echo "Usa Git LFS o reduce el tamaño del archivo"
    errors=$((errors + 1))
fi

# Verificar credenciales en código (bloqueante)
if git diff --cached --name-only | xargs grep -l "password\|secret\|key\|token" 2>/dev/null; then
    echo "❌ Posibles credenciales detectadas en el código"
    echo "Remueve las credenciales antes del commit"
    errors=$((errors + 1))
fi

# Verificar archivos de configuración sensibles
sensitive_files=(".env" ".env.local" ".env.production" "config/database.yml")
for file in "${sensitive_files[@]}"; do
    if git diff --cached --name-only | grep -q "^$file$"; then
        echo "⚠️  Archivo sensible detectado: $file"
        echo "Asegúrate de que no contiene información confidencial"
    fi
done

# Verificar formato de archivos JavaScript/TypeScript (si existen)
js_files=$(git diff --cached --name-only | grep -E '\.(js|ts|jsx|tsx)$' || true)
if [ -n "$js_files" ] && command -v eslint >/dev/null 2>&1; then
    echo "🔍 Verificando formato JavaScript/TypeScript..."
    if ! echo "$js_files" | xargs eslint --quiet; then
        echo "❌ Errores de ESLint detectados"
        errors=$((errors + 1))
    fi
fi

# Verificar formato de archivos Python (si existen)
py_files=$(git diff --cached --name-only | grep -E '\.py$' || true)
if [ -n "$py_files" ] && command -v black >/dev/null 2>&1; then
    echo "🔍 Verificando formato Python..."
    if ! echo "$py_files" | xargs black --check --quiet; then
        echo "❌ Archivos Python no están formateados correctamente"
        echo "Ejecuta: black $py_files"
        errors=$((errors + 1))
    fi
fi

# Verificar formato de archivos Go (si existen)
go_files=$(git diff --cached --name-only | grep -E '\.go$' || true)
if [ -n "$go_files" ] && command -v gofmt >/dev/null 2>&1; then
    echo "🔍 Verificando formato Go..."
    unformatted=$(echo "$go_files" | xargs gofmt -l)
    if [ -n "$unformatted" ]; then
        echo "❌ Archivos Go no están formateados:"
        echo "$unformatted"
        echo "Ejecuta: gofmt -w $unformatted"
        errors=$((errors + 1))
    fi
fi

# Resultado final
if [ $errors -gt 0 ]; then
    echo ""
    echo "❌ Pre-commit falló con $errors error(es)"
    echo "Corrige los problemas y vuelve a intentar el commit"
    exit 1
else
    echo "✅ Todas las validaciones pasaron"
    exit 0
fi
EOF

# Hook de commit-msg para validar formato
cat > .githooks/commit-msg << 'EOF'
#!/bin/bash
# Validar formato de mensaje de commit

commit_regex='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .{1,50}'
commit_msg=$(head -n 1 "$1")

if ! echo "$commit_msg" | grep -qE "$commit_regex"; then
    echo "❌ Formato de commit inválido"
    echo ""
    echo "Formato esperado:"
    echo "  tipo(scope): descripción"
    echo ""
    echo "Tipos válidos: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert"
    echo ""
    echo "Ejemplos:"
    echo "  feat(auth): add login functionality"
    echo "  fix(ui): resolve button alignment issue"
    echo "  docs: update README"
    echo ""
    exit 1
fi
EOF

chmod +x .githooks/pre-commit
chmod +x .githooks/commit-msg

success "Hooks estrictos configurados"

# .gitignore más completo
log "Actualizando .gitignore..."

cat >> .gitignore << 'EOF'

# === CONFIGURACIÓN COMPLETA ADICIONAL ===

# Logs detallados
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory
coverage/
*.lcov
.nyc_output

# Dependency directories adicionales
bower_components/
jspm_packages/

# IDE adicionales
*.swp
*.swo
*~

# OS adicionales
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db

# Build adicionales
*.tgz
*.tar.gz
.cache/
.parcel-cache/

# Database
*.db
*.sqlite
*.sqlite3

# Python adicional
*.py[cod]
*$py.class
*.so
.Python
env/
ENV/
env.bak/
venv.bak/

# Go adicional
*.exe~
*.dll
*.dylib
*.test
go.work

# Docker adicional
.dockerignore
Dockerfile.dev

# Temporary adicionales
*.temp
*.backup
*.bak
*.old

# SICORA específico adicional
*.sicora.tmp
.sicora-cache/
sicora-logs/
EOF

success ".gitignore actualizado"

echo ""
success "🎉 Configuración Git completa aplicada"
echo ""
echo "🔧 Nuevas características habilitadas:"
echo "  • Hooks estrictos con validaciones de código"
echo "  • Aliases avanzados para Git"
echo "  • Validación de formato de commits"
echo "  • .gitignore más completo"
echo "  • Configuraciones avanzadas de Git"
echo ""
echo "💡 Comandos útiles:"
echo "  git aliases    # Ver todos los aliases"
echo "  git tree       # Ver árbol de commits"
echo "  git amend      # Enmendar último commit"
echo ""
warning "NOTA: Los hooks ahora son más estrictos y pueden bloquear commits"
echo "      Para bypass temporal: git commit --no-verify -m 'mensaje'"
