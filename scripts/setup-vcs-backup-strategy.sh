#!/bin/bash

# 🔒 Script de Implementación Rápida - Estrategia de Respaldo VCS SICORA
# Versión: 1.0
# Fecha: 16 de julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuración
PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"
BACKUP_BASE="/backup/sicora"
SCRIPTS_DIR="$BACKUP_BASE/scripts"
LOG_FILE="/var/log/sicora-backup-setup.log"

# Función para logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

print_header() {
    echo -e "\n${PURPLE}========================================${NC}"
    echo -e "${PURPLE}🔒 $1${NC}"
    echo -e "${PURPLE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar requisitos
check_requirements() {
    print_header "VERIFICANDO REQUISITOS"
    
    # Verificar Git
    if ! command -v git &> /dev/null; then
        print_error "Git no está instalado"
        exit 1
    fi
    print_success "Git disponible: $(git --version)"
    
    # Verificar PostgreSQL tools
    if ! command -v pg_dump &> /dev/null; then
        print_warning "pg_dump no encontrado - instalar postgresql-client"
    else
        print_success "PostgreSQL tools disponibles"
    fi
    
    # Verificar GPG
    if ! command -v gpg &> /dev/null; then
        print_warning "GPG no encontrado - instalar gnupg"
    else
        print_success "GPG disponible para cifrado"
    fi
    
    # Verificar permisos
    if [ ! -w "/backup" ] && [ ! -w "/" ]; then
        print_warning "Permisos limitados - ejecutar como sudo para setup completo"
    fi
}

# Crear estructura de directorios
create_directory_structure() {
    print_header "CREANDO ESTRUCTURA DE DIRECTORIOS"
    
    # Crear directorios base
    sudo mkdir -p "$BACKUP_BASE"/{mirrors,database,configs,postman,cloud-sync,logs}
    sudo mkdir -p "$SCRIPTS_DIR"
    
    # Establecer permisos
    sudo chown -R $USER:$USER "$BACKUP_BASE"
    chmod -R 755 "$BACKUP_BASE"
    
    print_success "Estructura de directorios creada en: $BACKUP_BASE"
}

# Crear script de mirror de repositorios
create_mirror_script() {
    print_header "CREANDO SCRIPT DE MIRROR"
    
    cat > "$SCRIPTS_DIR/mirror-repositories.sh" << 'EOF'
#!/bin/bash
# Mirror automático de repositorios SICORA

BACKUP_BASE="/backup/sicora"
MIRRORS_DIR="$BACKUP_BASE/mirrors"
PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"

# Repositorios a respaldar
REPOS=(
    "sicora-app-fe"
    "sicora-be-go"
    "sicora-be-python"
    "sicora-mcp-server"
    "sicora-infra"
    "sicora-docs"
    "sicora-shared"
    "sicora-data-loader"
)

echo "🔄 Iniciando mirror de repositorios SICORA..."

# Mirror del monorepo principal
echo "📂 Creando mirror del monorepo principal..."
if [ -d "$MIRRORS_DIR/sicora-app/.git" ]; then
    cd "$MIRRORS_DIR/sicora-app"
    git fetch --all
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
else
    mkdir -p "$MIRRORS_DIR"
    cp -r "$PROJECT_ROOT" "$MIRRORS_DIR/sicora-app"
fi

# Mirror de cada componente
for repo in "${REPOS[@]}"; do
    if [ -d "$PROJECT_ROOT/$repo" ]; then
        echo "📦 Procesando $repo..."
        rsync -av --delete "$PROJECT_ROOT/$repo/" "$MIRRORS_DIR/$repo/"
    fi
done

# Crear snapshot comprimido
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_BASE/sicora-complete-$DATE.tar.gz" -C "$MIRRORS_DIR" .

# Limpiar snapshots antiguos (mantener últimos 7 días)
find "$BACKUP_BASE" -name "sicora-complete-*.tar.gz" -mtime +7 -delete

echo "✅ Mirror completado: $DATE"
EOF

    chmod +x "$SCRIPTS_DIR/mirror-repositories.sh"
    print_success "Script de mirror creado"
}

# Crear script de backup de configuraciones
create_config_backup_script() {
    print_header "CREANDO SCRIPT DE BACKUP DE CONFIGURACIONES"
    
    cat > "$SCRIPTS_DIR/backup-configurations.sh" << 'EOF'
#!/bin/bash
# Backup de configuraciones SICORA

BACKUP_BASE="/backup/sicora"
CONFIG_DIR="$BACKUP_BASE/configs/$(date +%Y%m%d)"
PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"

mkdir -p "$CONFIG_DIR"

echo "⚙️ Respaldando configuraciones SICORA..."

cd "$PROJECT_ROOT"

# Variables de entorno (sin secretos)
find . -name ".env.example" -exec cp {} "$CONFIG_DIR/" \;
find . -name "*.env.example" -exec cp {} "$CONFIG_DIR/" \;

# Docker configurations
find . -name "docker-compose*.yml" -exec cp --parents {} "$CONFIG_DIR/" \;
find . -name "Dockerfile*" -exec cp --parents {} "$CONFIG_DIR/" \;

# Package managers
find . -name "package.json" -exec cp --parents {} "$CONFIG_DIR/" \;
find . -name "requirements*.txt" -exec cp --parents {} "$CONFIG_DIR/" \;
find . -name "go.mod" -exec cp --parents {} "$CONFIG_DIR/" \;
find . -name "go.sum" -exec cp --parents {} "$CONFIG_DIR/" \;
find . -name "pyproject.toml" -exec cp --parents {} "$CONFIG_DIR/" \;

# CI/CD configurations
find . -name ".github" -type d -exec cp -r --parents {} "$CONFIG_DIR/" \; 2>/dev/null || true

# Makefiles y scripts
find . -name "Makefile" -exec cp --parents {} "$CONFIG_DIR/" \;
find . -name "*.sh" -exec cp --parents {} "$CONFIG_DIR/" \;

# VS Code settings
find . -name ".vscode" -type d -exec cp -r --parents {} "$CONFIG_DIR/" \; 2>/dev/null || true

# Documentación crítica
cp -r _docs "$CONFIG_DIR/"
cp README.md "$CONFIG_DIR/"
cp sonar-project.properties "$CONFIG_DIR/" 2>/dev/null || true

# Crear inventario
echo "📝 Creando inventario..."
cat > "$CONFIG_DIR/inventory.txt" << INVENTORY
# Inventario de Configuraciones SICORA
# Fecha: $(date)
# Commit: $(git rev-parse HEAD 2>/dev/null || echo "N/A")

$(find "$CONFIG_DIR" -type f | sort)
INVENTORY

echo "✅ Configuraciones respaldadas en: $CONFIG_DIR"
EOF

    chmod +x "$SCRIPTS_DIR/backup-configurations.sh"
    print_success "Script de backup de configuraciones creado"
}

# Crear script de backup de base de datos
create_database_backup_script() {
    print_header "CREANDO SCRIPT DE BACKUP DE BASE DE DATOS"
    
    cat > "$SCRIPTS_DIR/backup-database.sh" << 'EOF'
#!/bin/bash
# Backup de base de datos SICORA

BACKUP_BASE="/backup/sicora"
DB_BACKUP_DIR="$BACKUP_BASE/database/$(date +%Y%m%d)"

mkdir -p "$DB_BACKUP_DIR"

echo "🗄️ Respaldando base de datos SICORA..."

# Configuración de base de datos (ajustar según configuración real)
DB_HOST="localhost"
DB_PORT="5433"  # Puerto según sicora-infra
DB_USER="sicora_user"
DB_NAME="sicora_dev"

# Verificar si PostgreSQL está disponible
if ! command -v pg_dump &> /dev/null; then
    echo "⚠️ pg_dump no disponible - instalar postgresql-client"
    exit 1
fi

# Verificar conexión a la base de datos
if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" 2>/dev/null; then
    echo "⚠️ Base de datos no disponible en $DB_HOST:$DB_PORT"
    echo "ℹ️ Verificar que PostgreSQL esté ejecutándose:"
    echo "   cd sicora-infra && docker compose -f docker/docker-compose.yml up -d postgres"
    exit 1
fi

# Backup completo
echo "📦 Creando backup completo..."
PGPASSWORD="${DB_PASSWORD}" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --verbose --clean --no-owner --no-privileges \
    --format=custom > "$DB_BACKUP_DIR/sicora_full_$(date +%Y%m%d_%H%M%S).dump"

# Backup de esquemas únicamente
echo "📋 Creando backup de esquemas..."
PGPASSWORD="${DB_PASSWORD}" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --schema-only --verbose --clean --no-owner --no-privileges \
    > "$DB_BACKUP_DIR/sicora_schema_$(date +%Y%m%d_%H%M%S).sql"

# Backup de migraciones si existen
PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"
if [ -d "$PROJECT_ROOT/sicora-be-go" ]; then
    find "$PROJECT_ROOT" -path "*/database/migrations" -type d -exec cp -r {} "$DB_BACKUP_DIR/" \; 2>/dev/null || true
fi

# Verificar integridad del backup
DUMP_FILE=$(ls "$DB_BACKUP_DIR"/sicora_full_*.dump | head -1)
if [ -f "$DUMP_FILE" ] && pg_restore --list "$DUMP_FILE" > /dev/null 2>&1; then
    echo "✅ Backup de BD verificado correctamente"
else
    echo "❌ Error en verificación de backup de BD"
fi

echo "✅ Base de datos respaldada en: $DB_BACKUP_DIR"
EOF

    chmod +x "$SCRIPTS_DIR/backup-database.sh"
    print_success "Script de backup de base de datos creado"
}

# Crear script de backup de collections Postman
create_postman_backup_script() {
    print_header "CREANDO SCRIPT DE BACKUP DE POSTMAN"
    
    cat > "$SCRIPTS_DIR/backup-postman-collections.sh" << 'EOF'
#!/bin/bash
# Backup de collections Postman SICORA

BACKUP_BASE="/backup/sicora"
POSTMAN_BACKUP="$BACKUP_BASE/postman/$(date +%Y%m%d)"
PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"
COLLECTIONS_DIR="$PROJECT_ROOT/postman-collections"

mkdir -p "$POSTMAN_BACKUP"

echo "📮 Respaldando colecciones Postman..."

if [ -d "$COLLECTIONS_DIR" ]; then
    # Copiar collections y environments
    cp -r "$COLLECTIONS_DIR"/* "$POSTMAN_BACKUP/" 2>/dev/null || true
    
    # Crear package con timestamp
    cd "$POSTMAN_BACKUP"
    tar -czf "sicora-postman-collections_$(date +%Y%m%d_%H%M%S).tar.gz" . 2>/dev/null || true
    
    # Validar collections si existe el script
    if [ -f "$COLLECTIONS_DIR/validate-collections.sh" ]; then
        echo "🔍 Validando collections..."
        cd "$COLLECTIONS_DIR"
        ./validate-collections.sh || echo "⚠️ Validación de collections con advertencias"
    fi
    
    echo "✅ Collections Postman respaldadas"
else
    echo "⚠️ Directorio de collections no encontrado: $COLLECTIONS_DIR"
fi
EOF

    chmod +x "$SCRIPTS_DIR/backup-postman-collections.sh"
    print_success "Script de backup de Postman creado"
}

# Crear script maestro de backup diario
create_daily_backup_script() {
    print_header "CREANDO SCRIPT MAESTRO DE BACKUP"
    
    cat > "$SCRIPTS_DIR/daily-backup.sh" << 'EOF'
#!/bin/bash
# Script maestro de backup diario SICORA

set -e

BACKUP_BASE="/backup/sicora"
SCRIPTS_DIR="$BACKUP_BASE/scripts"
LOG_FILE="$BACKUP_BASE/logs/sicora-backup-$(date +%Y%m%d).log"

mkdir -p "$BACKUP_BASE/logs"

# Función de logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🚀 Iniciando backup diario SICORA"

# 1. Mirror de repositorios
log "📂 Ejecutando mirror de repositorios..."
if "$SCRIPTS_DIR/mirror-repositories.sh" >> "$LOG_FILE" 2>&1; then
    log "✅ Mirror de repositorios completado"
else
    log "❌ Error en mirror de repositorios"
fi

# 2. Backup de configuraciones
log "⚙️ Respaldando configuraciones..."
if "$SCRIPTS_DIR/backup-configurations.sh" >> "$LOG_FILE" 2>&1; then
    log "✅ Backup de configuraciones completado"
else
    log "❌ Error en backup de configuraciones"
fi

# 3. Backup de base de datos
log "🗄️ Respaldando base de datos..."
if "$SCRIPTS_DIR/backup-database.sh" >> "$LOG_FILE" 2>&1; then
    log "✅ Backup de base de datos completado"
else
    log "⚠️ Backup de base de datos con advertencias"
fi

# 4. Backup de collections Postman
log "📮 Respaldando collections Postman..."
if "$SCRIPTS_DIR/backup-postman-collections.sh" >> "$LOG_FILE" 2>&1; then
    log "✅ Backup de collections completado"
else
    log "⚠️ Backup de collections con advertencias"
fi

# 5. Generar reporte de estado
log "📊 Generando reporte de estado..."
cat > "$BACKUP_BASE/backup-status-$(date +%Y%m%d).txt" << REPORT
# Reporte de Backup SICORA
# Fecha: $(date)

## Resumen de Respaldos
- Repositorios: $(ls $BACKUP_BASE/mirrors/ 2>/dev/null | wc -l) directorios
- Base de datos: $(ls $BACKUP_BASE/database/*/sicora_full_*.dump 2>/dev/null | wc -l) backups
- Configuraciones: $(ls $BACKUP_BASE/configs/ 2>/dev/null | wc -l) sets
- Collections: $(ls $BACKUP_BASE/postman/ 2>/dev/null | wc -l) backups

## Espacio Utilizado
$(du -sh $BACKUP_BASE/* 2>/dev/null | sort -hr)

## Último Log
$(tail -10 "$LOG_FILE")
REPORT

log "🏁 Backup diario SICORA finalizado"

# Mostrar resumen
echo ""
echo "📊 RESUMEN DE BACKUP:"
cat "$BACKUP_BASE/backup-status-$(date +%Y%m%d).txt"
EOF

    chmod +x "$SCRIPTS_DIR/daily-backup.sh"
    print_success "Script maestro de backup creado"
}

# Crear configuración de cron
create_cron_config() {
    print_header "CONFIGURANDO CRON JOBS"
    
    # Crear archivo de cron temporal
    cat > "/tmp/sicora-backup-cron" << EOF
# SICORA Backup Jobs
# Respaldo diario a las 2:00 AM
0 2 * * * $SCRIPTS_DIR/daily-backup.sh

# Mirror de repositorios cada 6 horas
0 */6 * * * $SCRIPTS_DIR/mirror-repositories.sh

# Limpieza de backups antiguos (domingos 4:00 AM)
0 4 * * 0 find $BACKUP_BASE -name "*.tar.gz" -mtime +30 -delete

EOF

    print_warning "Para instalar cron jobs, ejecutar:"
    echo -e "${YELLOW}sudo crontab -u $USER /tmp/sicora-backup-cron${NC}"
    echo -e "${YELLOW}Archivo de configuración creado en: /tmp/sicora-backup-cron${NC}"
}

# Probar la implementación
test_implementation() {
    print_header "PROBANDO IMPLEMENTACIÓN"
    
    log "🧪 Ejecutando prueba de backup..."
    
    # Probar mirror de repositorios
    if "$SCRIPTS_DIR/mirror-repositories.sh"; then
        print_success "Mirror de repositorios: OK"
    else
        print_warning "Mirror de repositorios: Con advertencias"
    fi
    
    # Probar backup de configuraciones
    if "$SCRIPTS_DIR/backup-configurations.sh"; then
        print_success "Backup de configuraciones: OK"
    else
        print_warning "Backup de configuraciones: Con advertencias"
    fi
    
    # Probar backup de Postman
    if "$SCRIPTS_DIR/backup-postman-collections.sh"; then
        print_success "Backup de Postman: OK"
    else
        print_warning "Backup de Postman: Con advertencias"
    fi
    
    # Mostrar estadísticas
    echo ""
    echo "📊 ESTADÍSTICAS DE BACKUP:"
    echo "- Tamaño total: $(du -sh $BACKUP_BASE 2>/dev/null | cut -f1)"
    echo "- Archivos creados: $(find $BACKUP_BASE -type f | wc -l)"
    echo "- Último backup: $(ls -lt $BACKUP_BASE/sicora-complete-*.tar.gz 2>/dev/null | head -1 | awk '{print $6, $7, $8}')"
}

# Función principal
main() {
    clear
    print_header "SETUP DE ESTRATEGIA DE RESPALDO VCS SICORA"
    
    echo -e "${BLUE}Este script configurará automáticamente la estrategia de respaldo para el proyecto SICORA${NC}"
    echo -e "${BLUE}Basado en el documento: _docs/desarrollo/ESTRATEGIA_RESPALDO_VCS.md${NC}"
    echo ""
    
    read -p "¿Continuar con la instalación? [y/N]: " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Instalación cancelada."
        exit 0
    fi
    
    # Ejecutar pasos de instalación
    check_requirements
    create_directory_structure
    create_mirror_script
    create_config_backup_script
    create_database_backup_script
    create_postman_backup_script
    create_daily_backup_script
    create_cron_config
    test_implementation
    
    print_header "INSTALACIÓN COMPLETADA"
    
    echo -e "${GREEN}✅ Estrategia de respaldo VCS instalada exitosamente${NC}"
    echo ""
    echo -e "${BLUE}📁 Ubicación de scripts: $SCRIPTS_DIR${NC}"
    echo -e "${BLUE}📁 Ubicación de backups: $BACKUP_BASE${NC}"
    echo -e "${BLUE}📜 Logs de instalación: $LOG_FILE${NC}"
    echo ""
    echo -e "${YELLOW}📋 PRÓXIMOS PASOS:${NC}"
    echo -e "${YELLOW}1. Revisar configuración de base de datos en backup-database.sh${NC}"
    echo -e "${YELLOW}2. Instalar cron jobs: sudo crontab -u $USER /tmp/sicora-backup-cron${NC}"
    echo -e "${YELLOW}3. Configurar sincronización con la nube (AWS/GitLab/etc.)${NC}"
    echo -e "${YELLOW}4. Probar recuperación: $SCRIPTS_DIR/daily-backup.sh${NC}"
    echo ""
    echo -e "${GREEN}🎉 ¡SICORA está ahora protegido con respaldos automáticos!${NC}"
}

# Ejecutar script principal
main "$@"
