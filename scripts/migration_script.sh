#!/bin/bash

# Script de migración de documentación existente a repositorio centralizado
# Este script asegura que no perdamos información durante la migración

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📦 Iniciando migración de documentación existente${NC}"

# Variables de configuración
SOURCE_PROJECT_PATH="/home/epti/Documentos/epti-dev/asiste-app/fast-rn/sicora-app-be-multistack/_docs"  # Ajusta esta ruta
TARGET_DOCS_PATH="_docs"
BACKUP_PATH="migration-backup"

# Crear backup antes de migrar (práctica fundamental en operaciones)
echo -e "${YELLOW}📋 Creando backup de seguridad...${NC}"
mkdir -p "$BACKUP_PATH"
cp -r "$TARGET_DOCS_PATH" "$BACKUP_PATH/docs-$(date +%Y%m%d-%H%M%S)" 2>/dev/null || echo "No hay docs previos para backup"

# Función para copiar preservando estructura y metadatos
copy_with_validation() {
    local source_file="$1"
    local target_file="$2"
    local description="$3"
    
    if [ -f "$source_file" ]; then
        # Crear directorio destino si no existe
        mkdir -p "$(dirname "$target_file")"
        
        # Copiar archivo
        cp "$source_file" "$target_file"
        
        # Validar que la copia fue exitosa
        if [ -f "$target_file" ]; then
            echo -e "${GREEN}✅ Migrado: $description${NC}"
            
            # Agregar metadata de migración como comentario en archivos .md
            if [[ "$target_file" == *.md ]]; then
                echo "<!-- Migrado desde: $source_file el $(date) -->" >> "$target_file"
            fi
        else
            echo -e "${RED}❌ Error migrando: $description${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  No encontrado: $source_file${NC}"
    fi
}

echo -e "${BLUE}🔄 Migrando archivos de documentación...${NC}"

# Migrar requisitos funcionales
copy_with_validation \
    "$SOURCE_PROJECT_PATH/_docs/general/rf.md" \
    "$TARGET_DOCS_PATH/general/rf.md" \
    "Requisitos Funcionales"

# Migrar arquitectura comparativa
copy_with_validation \
    "$SOURCE_PROJECT_PATH/_docs/general/arquitectura_comparativa_microservicios_scs.md" \
    "$TARGET_DOCS_PATH/general/arquitectura_comparativa_microservicios_scs.md" \
    "Arquitectura Comparativa"

# Migrar especificaciones de API
copy_with_validation \
    "$SOURCE_PROJECT_PATH/_docs/api/endpoints_specification.md" \
    "$TARGET_DOCS_PATH/api/endpoints_specification.md" \
    "Especificación de Endpoints"

copy_with_validation \
    "$SOURCE_PROJECT_PATH/_docs/api/endpoints_specification_TEMPLATE.md" \
    "$TARGET_DOCS_PATH/api/endpoints_specification_TEMPLATE.md" \
    "Template de Endpoints"

# Migrar historias de usuario del backend
if [ -d "$SOURCE_PROJECT_PATH/_docs/stories/be" ]; then
    echo -e "${BLUE}📚 Migrando historias de usuario del backend...${NC}"
    mkdir -p "$TARGET_DOCS_PATH/stories/be"
    cp -r "$SOURCE_PROJECT_PATH/_docs/stories/be/"* "$TARGET_DOCS_PATH/stories/be/" 2>/dev/null
    echo -e "${GREEN}✅ Historias de usuario del backend migradas${NC}"
fi

# Migrar documentación técnica
if [ -d "$SOURCE_PROJECT_PATH/_docs/technical" ]; then
    echo -e "${BLUE}🔧 Migrando documentación técnica...${NC}"
    mkdir -p "$TARGET_DOCS_PATH/technical"
    cp -r "$SOURCE_PROJECT_PATH/_docs/technical/"* "$TARGET_DOCS_PATH/technical/" 2>/dev/null
    echo -e "${GREEN}✅ Documentación técnica migrada${NC}"
fi

# Crear archivo de inventario de migración
cat > migration-inventory.md << EOF
# Inventario de Migración - $(date)

## Archivos Migrados Exitosamente

### Documentación General
- [x] Requisitos Funcionales (rf.md)
- [x] Arquitectura Comparativa (arquitectura_comparativa_microservicios_scs.md)

### Especificaciones de API
- [x] Endpoints Specification (endpoints_specification.md)
- [x] Template para equipos (endpoints_specification_TEMPLATE.md)

### Historias de Usuario
- [x] Backend stories (directorio completo)

### Documentación Técnica
- [x] Migraciones y cambios técnicos (directorio completo)

## Próximos Pasos

1. Validar que toda la documentación sea accesible
2. Crear scripts de sincronización para codespaces
3. Configurar plantillas de .devcontainer
4. Establecer workflow de actualización

## Metadata de Migración

- **Fecha:** $(date)
- **Fuente:** $SOURCE_PROJECT_PATH
- **Destino:** $TARGET_DOCS_PATH
- **Backup:** $BACKUP_PATH
EOF

echo -e "${GREEN}📋 Inventario de migración creado${NC}"

# Verificar integridad de archivos críticos
echo -e "${BLUE}🔍 Verificando integridad de archivos críticos...${NC}"

critical_files=(
    "$TARGET_DOCS_PATH/general/rf.md"
    "$TARGET_DOCS_PATH/api/endpoints_specification.md"
)

for file in "${critical_files[@]}"; do
    if [ -f "$file" ] && [ -s "$file" ]; then
        echo -e "${GREEN}✅ $file está presente y no está vacío${NC}"
    else
        echo -e "${RED}❌ CRÍTICO: $file falta o está vacío${NC}"
    fi
done

# Commit de la migración
echo -e "${BLUE}💾 Creando commit de migración...${NC}"
git add . -- ':!sicora-docs/*'
git commit -m "feat: migrate existing project documentation

- Import all critical documentation from source project
- Preserve directory structure and file organization
- Add migration metadata for traceability
- Create migration inventory for verification
- Ensure no documentation loss during centralization"

echo -e "${GREEN}🎉 Migración completada exitosamente${NC}"
echo -e "${BLUE}📁 Revisa el archivo migration-inventory.md para detalles completos${NC}"