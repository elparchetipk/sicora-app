#!/bin/bash
# Script para corregir imports en archivos de test movidos a subcarpetas.

# Directorio base
BASE_DIR="/home/epti/Documentos/epti-dev/sicora-app/sicora-be-python/userservice"
cd "$BASE_DIR" || exit 1

# Función para agregar path setup a archivos en subcarpetas
add_path_setup() {
    local file="$1"
    local levels="$2"  # número de niveles hacia arriba (.., ../.., etc)

    # Verificar si ya tiene el setup de path
    if ! grep -q "sys.path.insert" "$file"; then
        # Crear archivo temporal con el nuevo contenido
        {
            # Mantener shebang y docstring
            head -n 1 "$file"
            echo '"""'
            sed -n '2,/"""/p' "$file" | head -n -1
            echo '"""'
            echo
            echo "import sys"
            echo "import os"
            echo "sys.path.insert(0, os.path.join(os.path.dirname(__file__), '$levels'))"
            echo
            # Agregar el resto del archivo, omitiendo shebang y docstring inicial
            sed -n '/"""/,$p' "$file" | tail -n +2
        } > "${file}.tmp"

        mv "${file}.tmp" "$file"
        echo "✅ Corregido: $file"
    else
        echo "⏭️  Ya corregido: $file"
    fi
}

echo "🔧 Corrigiendo imports en archivos de test..."

# Corregir archivos en integration/ (nivel 2: ../..)
find tests/integration/ -name "*.py" -not -name "__*" | while read file; do
    add_path_setup "$file" "../.."
done

# Corregir archivos en debug/ (nivel 2: ../..)
find tests/debug/ -name "*.py" -not -name "__*" | while read file; do
    add_path_setup "$file" "../.."
done

# Corregir archivos en setup/ (nivel 2: ../..)
find tests/setup/ -name "*.py" -not -name "__*" | while read file; do
    add_path_setup "$file" "../.."
done

# Corregir archivos en unit/ (nivel 2: ../..)
find tests/unit/ -name "*.py" -not -name "__*" | while read file; do
    add_path_setup "$file" "../.."
done

# Corregir archivos en e2e/ (nivel 2: ../..)
find tests/e2e/ -name "*.py" -not -name "__*" | while read file; do
    add_path_setup "$file" "../.."
done

echo "✅ Corrección de imports completada"
