# Script para crear el repositorio centralizado de documentación SICORA
# Este script establece la estructura base que servirá como SSOT (Single Source of Truth)

#!/bin/bash

# Colores para output más claro (útil para debugging y logs)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Creando repositorio centralizado SICORA-DOCS${NC}"

# Crear directorio base
mkdir -p sicora-docs
cd sicora-docs

# Inicializar repositorio Git
git init
echo -e "${GREEN}✅ Repositorio Git inicializado${NC}"

# Crear estructura de directorios
# La lógica aquí es separar claramente entre documentación compartida,
# templates reutilizables y herramientas de automatización
mkdir -p {_docs/{general,api,stories/{be,fe},technical,testing},scripts,templates/{devcontainer,docker,github-actions},tools}

echo -e "${GREEN}✅ Estructura de directorios creada${NC}"

# Crear archivos de configuración principales
cat > README.md << 'EOF'
# SICORA - Documentación Centralizada

Este repositorio contiene toda la documentación compartida del proyecto SICORA (Sistema de Información de Coordinación Académica).

## Propósito

Actúa como Single Source of Truth (SSOT) para:
- Requisitos Funcionales (RF's)
- Historias de Usuario
- Especificaciones de API
- Criterios de Aceptación
- Documentación Técnica
- Plantillas de Configuración

## Estructura

```
sicora-docs/
├── _docs/                 # Documentación principal
│   ├── general/          # RF's, arquitectura, etc.
│   ├── api/              # Especificaciones de endpoints
│   ├── stories/          # Historias de usuario
│   ├── technical/        # Documentación técnica
│   └── testing/          # Criterios de aceptación y tests
├── scripts/              # Scripts de sincronización
├── templates/            # Plantillas para codespaces
└── tools/               # Herramientas auxiliares
```

## Uso en Codespaces

Este repositorio se sincroniza automáticamente con todos los codespaces del proyecto mediante scripts automatizados.
EOF

# Crear gitignore específico para documentación
cat > .gitignore << 'EOF'
# Archivos temporales de sincronización
.sync-cache/
*.tmp
*.temp

# Logs de scripts
*.log
sync-logs/

# Archivos de configuración local
.env.local
config.local.*

# Backup automáticos
backups/
*.backup

# IDE específicos
.vscode/settings.json
.idea/
EOF

echo -e "${GREEN}✅ Archivos de configuración creados${NC}"

# Crear estructura inicial de documentación
# Aquí replicamos la estructura que ya tienes en tu proyecto actual
cat > _docs/README.md << 'EOF'
# Documentación del Proyecto SICORA

Esta documentación está organizada siguiendo los principios de Clean Architecture y Domain-Driven Design.

## Navegación

### General
- [Requisitos Funcionales](general/rf.md) - Especificaciones completas del sistema
- [Arquitectura](general/arquitectura_comparativa_microservicios_scs.md) - Decisiones arquitectónicas

### API
- [Especificación de Endpoints](api/endpoints_specification.md) - Contratos de interfaz
- [Plantilla para Equipos](api/endpoints_specification_TEMPLATE.md) - Template para otros stacks

### Historias de Usuario
- [Backend](stories/be/) - Historias específicas del backend
- [Frontend](stories/fe/) - Historias específicas del frontend

### Técnica
- [Migraciones](technical/) - Documentación de cambios técnicos
- [Testing](testing/) - Organización de pruebas
EOF

echo -e "${YELLOW}📝 Estructura de documentación lista${NC}"

# Crear el primer commit
git add .
git commit -m "feat: initial setup of centralized documentation repository

- Create directory structure following SSOT principles
- Add README with clear navigation
- Set up gitignore for documentation-specific files
- Prepare for multi-codespace synchronization"

echo -e "${GREEN}🎉 Repositorio centralizado creado exitosamente${NC}"
echo -e "${BLUE}Siguiente paso: Mover tu documentación existente a este repositorio${NC}"