#!/bin/bash
# Script Universal de Autocommit para SICORA
# Unifica el manejo de commits automáticos en todos los stacks

set -e

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Funciones
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar que estamos en un repositorio Git
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    error "No estás en un repositorio Git"
    exit 1
fi

# Verificar si hay cambios
if git diff --quiet && git diff --staged --quiet; then
    warning "No hay cambios para hacer commit"
    exit 0
fi

log "🚀 Iniciando autocommit universal para SICORA"
log "📁 Branch: $BRANCH"

# Detectar qué stack fue modificado, excluyendo sicora-docs
CHANGED_FILES=$(git diff --name-only --staged -- . ':!sicora-docs/*' 2>/dev/null || git diff --name-only -- . ':!sicora-docs/*')
FRONTEND_CHANGED=$(echo "$CHANGED_FILES" | grep -E "sicora-app-fe/" || true)
BACKEND_GO_CHANGED=$(echo "$CHANGED_FILES" | grep -E "sicora-be-go/" || true)
BACKEND_PYTHON_CHANGED=$(echo "$CHANGED_FILES" | grep -E "sicora-be-python/" || true)
DOCS_CHANGED=$(echo "$CHANGED_FILES" | grep -E "_docs/|\.md$" || true)

# Mostrar qué cambios se detectaron
if [ -n "$FRONTEND_CHANGED" ]; then
    log "📱 Frontend changes detected"
fi
if [ -n "$BACKEND_GO_CHANGED" ]; then
    log "🐹 Go backend changes detected"
fi
if [ -n "$BACKEND_PYTHON_CHANGED" ]; then
    log "🐍 Python backend changes detected"
fi
if [ -n "$DOCS_CHANGED" ]; then
    log "📚 Documentation changes detected"
fi

# Ejecutar verificaciones de calidad por stack
if [ -n "$FRONTEND_CHANGED" ]; then
    log "📱 Verificando frontend..."
    cd "$PROJECT_ROOT/sicora-app-fe"

    # Verificar si pnpm está disponible
    if command -v pnpm &> /dev/null; then
        if pnpm lint && pnpm type-check; then
            success "Frontend checks passed"
        else
            error "Frontend checks failed"
            exit 1
        fi
    else
        warning "pnpm not found, skipping frontend checks"
    fi
    cd "$PROJECT_ROOT"
fi

if [ -n "$BACKEND_GO_CHANGED" ]; then
    log "🐹 Verificando backend Go..."
    cd "$PROJECT_ROOT/sicora-be-go"

    # Verificar si Go está disponible
    if command -v go &> /dev/null; then
        # Verificar si el Makefile existe
        if [ -f "Makefile" ]; then
            if make lint && make test-quick; then
                success "Go backend checks passed"
            else
                error "Go backend checks failed"
                exit 1
            fi
        else
            warning "Makefile not found, running basic go checks"
            if go mod tidy && go build -v ./...; then
                success "Basic Go checks passed"
            else
                error "Basic Go checks failed"
                exit 1
            fi
        fi
    else
        warning "Go not found, skipping Go backend checks"
    fi
    cd "$PROJECT_ROOT"
fi

if [ -n "$BACKEND_PYTHON_CHANGED" ]; then
    log "🐍 Verificando backend Python..."
    cd "$PROJECT_ROOT/sicora-be-python"

    # Verificar si Python está disponible
    if command -v python3 &> /dev/null; then
        # Verificar si el Makefile existe
        if [ -f "Makefile" ]; then
            if make lint && make test-quick; then
                success "Python backend checks passed"
            else
                error "Python backend checks failed"
                exit 1
            fi
        else
            warning "Makefile not found, running basic Python checks"
            if python3 -m py_compile **/*.py 2>/dev/null; then
                success "Basic Python checks passed"
            else
                error "Basic Python checks failed"
                exit 1
            fi
        fi
    else
        warning "Python3 not found, skipping Python backend checks"
    fi
    cd "$PROJECT_ROOT"
fi

# Determinar tipo de commit basado en cambios
COMMIT_TYPE=""
COMMIT_SCOPE=""
COMMIT_MESSAGE=""

if [ -n "$FRONTEND_CHANGED" ]; then
    COMMIT_SCOPE="frontend"
    if echo "$CHANGED_FILES" | grep -E "src/.*\.(ts|tsx)$" > /dev/null; then
        COMMIT_TYPE="feat"
        COMMIT_MESSAGE="update frontend components"
    elif echo "$CHANGED_FILES" | grep -E ".*\.test\.(ts|tsx)$" > /dev/null; then
        COMMIT_TYPE="test"
        COMMIT_MESSAGE="add/update frontend tests"
    elif echo "$CHANGED_FILES" | grep -E "tailwind|style|css" > /dev/null; then
        COMMIT_TYPE="style"
        COMMIT_MESSAGE="update frontend styles"
    else
        COMMIT_TYPE="feat"
        COMMIT_MESSAGE="update frontend code"
    fi
elif [ -n "$BACKEND_GO_CHANGED" ]; then
    COMMIT_SCOPE="backend-go"
    if echo "$CHANGED_FILES" | grep -E "handlers|endpoints|routes" > /dev/null; then
        COMMIT_TYPE="feat"
        COMMIT_MESSAGE="update Go API endpoints"
    elif echo "$CHANGED_FILES" | grep -E "entities|models" > /dev/null; then
        COMMIT_TYPE="feat"
        COMMIT_MESSAGE="update Go domain models"
    elif echo "$CHANGED_FILES" | grep -E "test|spec" > /dev/null; then
        COMMIT_TYPE="test"
        COMMIT_MESSAGE="add/update Go tests"
    else
        COMMIT_TYPE="feat"
        COMMIT_MESSAGE="update Go services"
    fi
elif [ -n "$BACKEND_PYTHON_CHANGED" ]; then
    COMMIT_SCOPE="backend-python"
    if echo "$CHANGED_FILES" | grep -E ".*\.py$" > /dev/null; then
        COMMIT_TYPE="feat"
        COMMIT_MESSAGE="update Python services"
    elif echo "$CHANGED_FILES" | grep -E "requirements|pyproject|setup" > /dev/null; then
        COMMIT_TYPE="build"
        COMMIT_MESSAGE="update Python dependencies"
    else
        COMMIT_TYPE="feat"
        COMMIT_MESSAGE="update Python code"
    fi
elif [ -n "$DOCS_CHANGED" ]; then
    COMMIT_TYPE="docs"
    COMMIT_MESSAGE="update documentation"
fi

# Valores por defecto
COMMIT_TYPE=${COMMIT_TYPE:-"chore"}
COMMIT_MESSAGE=${COMMIT_MESSAGE:-"update project files"}

# Construir mensaje de commit
if [ -n "$COMMIT_SCOPE" ]; then
    FULL_MESSAGE="${COMMIT_TYPE}(${COMMIT_SCOPE}): ${COMMIT_MESSAGE}"
else
    FULL_MESSAGE="${COMMIT_TYPE}: ${COMMIT_MESSAGE}"
fi

# Agregar detalles del contexto SICORA
FULL_MESSAGE="${FULL_MESSAGE}

🚀 SICORA Universal Autocommit
Branch: $BRANCH
Stacks affected: $(echo "$FRONTEND_CHANGED $BACKEND_GO_CHANGED $BACKEND_PYTHON_CHANGED $DOCS_CHANGED" | tr ' ' '\n' | grep -v '^$' | wc -l)
Auto-generated commit with quality checks

Co-authored-by: SICORA Development Team <desarrollo@sicora.onevision.edu.co>"

# Staging si no hay nada staged
if git diff --staged --quiet; then
    log "📝 Staging changes..."
    git add .
fi

# Mostrar cambios
log "📤 Changes to commit:"
git diff --staged --name-only | sed 's/^/  /'

# Hacer commit
log "💾 Committing: $FULL_MESSAGE"
if git commit -m "$FULL_MESSAGE"; then
    # Mostrar información del commit
    COMMIT_HASH=$(git rev-parse --short HEAD)
    success "Commit exitoso: $COMMIT_HASH"

    # Mostrar commits recientes
    log "📜 Recent commits:"
    git log --oneline -5

    # Preguntar si hacer push
    echo ""
    read -p "¿Hacer push al remote? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log "🚀 Pushing to remote..."
        if git push origin "$BRANCH"; then
            success "Push completed"
        else
            error "Push failed"
            exit 1
        fi
    fi
else
    error "Commit failed"
    exit 1
fi

log "🎉 Autocommit universal completado exitosamente"
