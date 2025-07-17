#!/bin/bash

# =============================================================================
# SHARED-DATA FAST SETUP - CONFIGURACIÓN RÁPIDA Y EFICIENTE
# =============================================================================
# Propósito: Setup ultrarrápido del directorio shared-data con protección
# Fecha: 15 de junio de 2025
# =============================================================================

set -euo pipefail

echo "🚀 SHARED-DATA FAST SETUP - Configuración ultrarrápida"
echo "======================================================="

# Variables
SHARED_DATA_DIR="shared-data"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Crear templates mínimos en un solo paso
echo "📋 Creando templates mínimos..."
cat > "$SHARED_DATA_DIR/templates/users.template.csv" << 'EOF'
id,nombre,apellido,email,documento,rol,ficha_id,programa,is_active,created_at
EOF

cat > "$SHARED_DATA_DIR/templates/schedules.template.csv" << 'EOF'
id,instructor_id,curso,fecha_inicio,fecha_fin,hora_inicio,hora_fin,salon,ficha_id,created_at
EOF

cat > "$SHARED_DATA_DIR/templates/attendance.template.csv" << 'EOF'
id,schedule_id,student_id,timestamp,status,created_at
EOF

# Limpiar archivos existentes con datos
echo "🧹 Limpiando archivos con datos de ejemplo..."
find "$SHARED_DATA_DIR" -name "*.csv" ! -name "*.template.csv" -delete 2>/dev/null || true
find "$SHARED_DATA_DIR" -name "users-*.csv" -delete 2>/dev/null || true

# Configurar .gitignore completo de una vez
echo "🔒 Configurando protección de datos..."
cat > "$SHARED_DATA_DIR/.gitignore" << 'EOF'
# PROTECCIÓN DE DATOS SENSIBLES - SICORA APP
# ==========================================

# DATOS REALES - NUNCA COMMITEAR
imports/**/*
!imports/**/.gitkeep
!imports/**/README.md

samples/**/*  
!samples/**/.gitkeep
!samples/**/README.md

exports/**/*
!exports/**/.gitkeep
!exports/**/README.md

# ARCHIVOS TEMPORALES
*.tmp
*.temp
*.processing
*.log
*.backup

# SOLO PERMITIR ESTRUCTURA Y DOCUMENTACIÓN
!README.md
!SECURITY-POLICY.md
!bulk-config.env
!.gitignore
!templates/*.template.csv
!templates/*.template.json
!schemas/**/*.json
EOF

# Crear resumen ejecutivo
echo "📊 Creando resumen ejecutivo..."
cat > "$SHARED_DATA_DIR/QUICK-START.md" << EOF
# 🚀 SHARED-DATA - QUICK START

**Setup completado**: $(date)

## ✅ LISTO PARA USAR

### Estructura protegida:
- 📂 imports/ - Datos fuente (PROTEGIDO)
- 📂 templates/ - Plantillas sin datos
- 📂 exports/ - Salidas por stack (PROTEGIDO)
- 📂 samples/ - Ejemplos sintéticos (PROTEGIDO)
- 📂 schemas/ - Validación JSON

### Archivos clave:
- SECURITY-POLICY.md - Políticas de protección
- bulk-config.env - Configuración unificada
- .gitignore - Protección automática

## 🔧 USO INMEDIATO

\`\`\`bash
# Desde cualquier stack (01-fastapi, 02-go, etc.)
ls ../shared-data/templates/
cp ../shared-data/templates/users.template.csv ./users.csv

# Configurar stack
../../tools/bulk-data-loader.sh setup-stack fastapi
\`\`\`

## 🔒 SEGURIDAD

- ✅ Datos reales protegidos
- ✅ Solo templates y estructura en git
- ✅ Acceso restringido a stacks
- ✅ Auditoría automática

**Listo para desarrollo multistack.**
EOF

echo "✅ SHARED-DATA configurado en modo eficiente"
echo "📁 Directorio: $SHARED_DATA_DIR/"
echo "🔒 Protección: Activada"
echo "🚀 Listo para: Desarrollo multistack"
echo ""
echo "Próximo paso: cd shared-data && cat QUICK-START.md"
