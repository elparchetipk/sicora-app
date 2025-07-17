#!/bin/bash

# =============================================================================
# POSTGRESQL 15 ENFORCEMENT SCRIPT
# =============================================================================
# Actualiza todas las referencias a PostgreSQL para garantizar versión 15
# =============================================================================

echo "🔧 Enforcing PostgreSQL 15 across the project..."

# Función para actualizar archivos
update_postgres_refs() {
    local file="$1"
    if [ -f "$file" ]; then
        # Reemplazar referencias genéricas
        sed -i 's/PostgreSQL/PostgreSQL 15/g' "$file" 2>/dev/null || true
        sed -i 's/postgresql/postgresql-15/g' "$file" 2>/dev/null || true
        sed -i 's/postgres:/postgres:15/g' "$file" 2>/dev/null || true
        
        # Evitar duplicados
        sed -i 's/PostgreSQL 15 15/PostgreSQL 15/g' "$file" 2>/dev/null || true
        sed -i 's/postgresql-15-15/postgresql-15/g' "$file" 2>/dev/null || true
        sed -i 's/postgres:15:15/postgres:15/g' "$file" 2>/dev/null || true
        
        echo "✅ Updated: $file"
    fi
}

# Archivos críticos a actualizar
files=(
    "README.md"
    "01-fastapi/README.md"
    "02-go/README.md" 
    "03-express/README.md"
    "04-nextjs/README.md"
    "05-springboot-java/README.md"
    "06-springboot-kotlin/README.md"
    "_docs/technical/ARCHITECTURAL-DECISIONS.md"
    "_docs/stories/be/historias_usuario_be_multistack.md"
    "tools/MULTISTACK-GUIDE.md"
    "CLEAN-ARCHITECTURE.md"
)

# Actualizar archivos
for file in "${files[@]}"; do
    update_postgres_refs "$file"
done

# Buscar y actualizar archivos .md adicionales
find . -name "*.md" -not -path "./.git/*" -not -path "./venv*/*" | while read file; do
    if grep -l "PostgreSQL\|postgresql\|postgres:" "$file" 2>/dev/null; then
        update_postgres_refs "$file"
    fi
done

echo ""
echo "✅ PostgreSQL 15 enforcement completed!"
echo "🔍 Verifying docker-compose.yml..."

# Verificar docker-compose.yml
if grep -q "postgres:15" docker-compose.yml; then
    echo "✅ docker-compose.yml already uses postgres:15"
else
    echo "⚠️  WARNING: docker-compose.yml needs manual verification"
fi

echo ""
echo "📊 Summary:"
echo "- All documentation updated to PostgreSQL 15"
echo "- README files standardized"
echo "- Technical docs aligned"
echo ""
echo "🚀 Ready to proceed with Next.js implementation!"
