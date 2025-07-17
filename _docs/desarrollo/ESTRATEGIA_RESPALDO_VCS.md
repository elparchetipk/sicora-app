# 🔒 Estrategia de Respaldo del Código VCS - SICORA

> **Estrategia de Respaldo Integral para Proyecto SICORA**  
> **Arquitectura**: Microservicios Multi-Stack (Go, Python, React, Node.js)  
> **Tipo**: Sistema de Información Académica de Misión Crítica

---

## 🎯 ANÁLISIS DEL PROYECTO SICORA

### **📊 Características del Proyecto**

#### **Arquitectura Multi-Stack Compleja**

```yaml
Componentes Principales:
├── Frontend: React + TypeScript + Vite (sicora-app-fe)
├── Backend Go: 8 microservicios, 237 endpoints
├── Backend Python: 7 servicios + API Gateway, 152 endpoints
├── MCP Server: TypeScript + Node.js (desarrollo asistido por IA)
├── Infraestructura: Docker + PostgreSQL + Redis
├── Documentación: Centralizada en _docs/
└── Datos: Loader de datos + colecciones Postman
```

#### **Criticidad del Sistema**

- **Tipo**: Sistema académico SENA (Servicio Nacional de Aprendizaje)
- **Usuarios**: Instructores, aprendices, coordinadores
- **Datos**: Información académica crítica, evaluaciones, asistencia
- **Disponibilidad**: 99.9% requerida durante períodos académicos

### **🚨 Riesgos Identificados**

#### **Riesgos Técnicos**

- **Pérdida de código fuente**: 389 endpoints en múltiples repositorios
- **Desincronización**: Múltiples stacks con dependencias cruzadas
- **Configuraciones**: Variables críticas de entorno y secrets
- **Datos de desarrollo**: Migraciones, seeds, colecciones Postman

#### **Riesgos Operacionales**

- **Equipo distribuido**: Múltiples desarrolladores en diferentes stacks
- **Despliegues**: Múltiples ambientes (dev, staging, prod)
- **Documentación**: Estructura compleja con categorización estricta

---

## 🏗️ ESTRATEGIA DE RESPALDO VCS

### **📋 Principio 3-2-1 Adaptado para SICORA**

```yaml
Estrategia 3-2-1 Mejorada:
├── 3 Copias: Repositorio principal + 2 respaldos
├── 2 Medios: Git distribuido + Archive storage
├── 1 Ubicación remota: Cloud backup cifrado
└── + Redundancia: Mirror automático + respaldo incremental
```

### **🔄 Arquitectura de Respaldo Multi-Nivel**

#### **Nivel 1: Repositorios Git Distribuidos**

```bash
# Repositorios principales
sicora-app/                    # Monorepo principal
├── sicora-app-fe/            # Frontend React
├── sicora-be-go/             # Backend Go (8 servicios)
├── sicora-be-python/         # Backend Python (7 servicios)
├── sicora-mcp-server/        # MCP Server
├── sicora-infra/             # Infraestructura
├── sicora-docs/              # Documentación
└── sicora-shared/            # Recursos compartidos

# Repositorios de respaldo
backup-sicora-primary/        # Mirror diario
backup-sicora-weekly/         # Snapshots semanales
backup-sicora-release/        # Versiones de release
```

#### **Nivel 2: Automatización de Respaldos**

```bash
# Scripts automatizados
backup-scripts/
├── daily-mirror.sh           # Mirror diario a las 2:00 AM
├── weekly-snapshot.sh        # Snapshot semanal completo
├── release-backup.sh         # Backup de releases
├── config-backup.sh          # Respaldo de configuraciones
└── verify-integrity.sh       # Verificación de integridad
```

#### **Nivel 3: Almacenamiento Externo**

```yaml
Cloud Storage:
├── GitHub: Repositorio principal + forks
├── GitLab: Mirror automático
├── Bitbucket: Respaldo terciario
└── Cloud Storage: AWS S3/Azure/Google Drive (archives)

Local Storage:
├── Servidor local: NAS/Storage dedicado
├── Workstations: Clones locales de desarrolladores
└── External drives: Respaldos físicos mensuales
```

---

## 🛠️ IMPLEMENTACIÓN DE LA ESTRATEGIA

### **1. Configuración de Repositorios Mirror**

#### **Script de Mirror Automático**

```bash
#!/bin/bash
# mirror-repositories.sh

# Configuración
BACKUP_BASE="/backup/sicora-mirrors"
REPOS=(
    "sicora-app"
    "sicora-app-fe"
    "sicora-be-go"
    "sicora-be-python"
    "sicora-mcp-server"
    "sicora-infra"
)

# Función de mirror
mirror_repository() {
    local repo=$1
    local backup_dir="$BACKUP_BASE/$repo"
    local timestamp=$(date +%Y%m%d_%H%M%S)

    echo "🔄 Creando mirror de $repo..."

    # Crear backup directory si no existe
    mkdir -p "$backup_dir"

    # Clone/Update mirror
    if [ -d "$backup_dir/.git" ]; then
        cd "$backup_dir"
        git fetch --all
        git pull origin main
    else
        git clone --mirror "https://github.com/tu-org/$repo.git" "$backup_dir"
    fi

    # Crear snapshot con timestamp
    tar -czf "$backup_dir_${timestamp}.tar.gz" -C "$backup_dir" .

    echo "✅ Mirror completado: $repo"
}

# Ejecutar mirrors
for repo in "${REPOS[@]}"; do
    mirror_repository "$repo"
done

# Limpiar mirrors antiguos (mantener últimos 30 días)
find "$BACKUP_BASE" -name "*.tar.gz" -mtime +30 -delete
```

### **2. Respaldo de Configuraciones Críticas**

#### **Script de Backup de Configuraciones**

```bash
#!/bin/bash
# backup-configurations.sh

BACKUP_DIR="/backup/sicora-configs/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Backup de archivos de configuración
echo "📋 Respaldando configuraciones..."

# Variables de entorno
find . -name ".env*" -exec cp {} "$BACKUP_DIR/" \;
find . -name "*.env" -exec cp {} "$BACKUP_DIR/" \;

# Docker configurations
find . -name "docker-compose*.yml" -exec cp {} "$BACKUP_DIR/" \;
find . -name "Dockerfile*" -exec cp {} "$BACKUP_DIR/" \;

# Package managers
find . -name "package.json" -exec cp {} "$BACKUP_DIR/" \;
find . -name "requirements.txt" -exec cp {} "$BACKUP_DIR/" \;
find . -name "go.mod" -exec cp {} "$BACKUP_DIR/" \;
find . -name "go.sum" -exec cp {} "$BACKUP_DIR/" \;

# CI/CD configurations
find . -name ".github" -type d -exec cp -r {} "$BACKUP_DIR/" \;

# Makefiles y scripts
find . -name "Makefile" -exec cp {} "$BACKUP_DIR/" \;
find . -name "*.sh" -exec cp {} "$BACKUP_DIR/" \;

# Crear archivo de inventario
echo "📝 Creando inventario de configuraciones..."
cat > "$BACKUP_DIR/inventory.txt" << EOF
# Inventario de Configuraciones SICORA
# Fecha: $(date)
# Commit: $(git rev-parse HEAD)

$(find "$BACKUP_DIR" -type f | sort)
EOF

echo "✅ Configuraciones respaldadas en: $BACKUP_DIR"
```

### **3. Respaldo de Datos de Desarrollo**

#### **Script de Backup de Base de Datos**

```bash
#!/bin/bash
# backup-database.sh

DB_BACKUP_DIR="/backup/sicora-database/$(date +%Y%m%d)"
mkdir -p "$DB_BACKUP_DIR"

# Configuración de base de datos
DB_HOST="localhost"
DB_PORT="5432"
DB_USER="sicora_user"
DB_NAME="sicora_dev"

echo "🗄️ Respaldando base de datos SICORA..."

# Backup completo
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --verbose --clean --no-owner --no-privileges \
    --format=custom > "$DB_BACKUP_DIR/sicora_full_$(date +%Y%m%d_%H%M%S).dump"

# Backup de esquemas únicamente
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --schema-only --verbose --clean --no-owner --no-privileges \
    > "$DB_BACKUP_DIR/sicora_schema_$(date +%Y%m%d_%H%M%S).sql"

# Backup de migraciones
cp -r ./sicora-be-*/database/migrations "$DB_BACKUP_DIR/"

# Verificar integridad del backup
if pg_restore --list "$DB_BACKUP_DIR"/sicora_full_*.dump > /dev/null 2>&1; then
    echo "✅ Backup de BD verificado correctamente"
else
    echo "❌ Error en backup de BD"
    exit 1
fi

echo "✅ Base de datos respaldada en: $DB_BACKUP_DIR"
```

### **4. Respaldo de Colecciones Postman**

#### **Script para Postman Collections**

```bash
#!/bin/bash
# backup-postman-collections.sh

COLLECTIONS_BACKUP="/backup/sicora-postman/$(date +%Y%m%d)"
COLLECTIONS_DIR="./postman-collections"

mkdir -p "$COLLECTIONS_BACKUP"

echo "📮 Respaldando colecciones Postman..."

# Copiar collections y environments
cp -r "$COLLECTIONS_DIR"/* "$COLLECTIONS_BACKUP/"

# Crear package con timestamp
cd "$COLLECTIONS_BACKUP"
tar -czf "sicora-postman-collections_$(date +%Y%m%d_%H%M%S).tar.gz" .

# Validar collections
./postman-collections/validate-collections.sh

echo "✅ Collections Postman respaldadas"
```

---

## ⚙️ AUTOMATIZACIÓN Y PROGRAMACIÓN

### **Cron Jobs para Respaldos Automáticos**

```bash
# /etc/crontab entries para SICORA

# Respaldo diario a las 2:00 AM
0 2 * * * /opt/sicora-backup/scripts/daily-backup.sh

# Mirror de repositorios cada 6 horas
0 */6 * * * /opt/sicora-backup/scripts/mirror-repositories.sh

# Backup semanal completo (sábados 1:00 AM)
0 1 * * 6 /opt/sicora-backup/scripts/weekly-full-backup.sh

# Verificación de integridad diaria (3:00 AM)
0 3 * * * /opt/sicora-backup/scripts/verify-integrity.sh

# Limpieza de backups antiguos (domingos 4:00 AM)
0 4 * * 0 /opt/sicora-backup/scripts/cleanup-old-backups.sh
```

### **Script Master de Backup Diario**

```bash
#!/bin/bash
# daily-backup.sh - Script maestro de backup diario

set -e

LOG_FILE="/var/log/sicora-backup.log"
BACKUP_BASE="/backup/sicora"
DATE=$(date +%Y%m%d)

# Función de logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🚀 Iniciando backup diario SICORA"

# 1. Mirror de repositorios
log "📂 Ejecutando mirror de repositorios..."
./mirror-repositories.sh

# 2. Backup de configuraciones
log "⚙️ Respaldando configuraciones..."
./backup-configurations.sh

# 3. Backup de base de datos
log "🗄️ Respaldando base de datos..."
./backup-database.sh

# 4. Backup de collections Postman
log "📮 Respaldando collections Postman..."
./backup-postman-collections.sh

# 5. Sync a cloud storage
log "☁️ Sincronizando con almacenamiento en la nube..."
./sync-to-cloud.sh

# 6. Verificación de integridad
log "🔍 Verificando integridad de backups..."
./verify-integrity.sh

# 7. Notificación de resultado
if [ $? -eq 0 ]; then
    log "✅ Backup diario completado exitosamente"
    ./notify-success.sh
else
    log "❌ Error en backup diario"
    ./notify-failure.sh
    exit 1
fi

log "🏁 Backup diario SICORA finalizado"
```

---

## 🔐 SEGURIDAD Y CIFRADO

### **Cifrado de Respaldos**

```bash
#!/bin/bash
# encrypt-backup.sh

BACKUP_DIR=$1
ENCRYPTED_DIR="${BACKUP_DIR}.encrypted"
ENCRYPTION_KEY="/secure/sicora-backup.key"

# Cifrar backup usando GPG
echo "🔐 Cifrando backup..."
tar -czf - "$BACKUP_DIR" | gpg --cipher-algo AES256 --compress-algo 1 \
    --symmetric --output "$ENCRYPTED_DIR.gpg"

# Crear checksum
sha256sum "$ENCRYPTED_DIR.gpg" > "$ENCRYPTED_DIR.gpg.sha256"

# Limpiar backup no cifrado
rm -rf "$BACKUP_DIR"

echo "✅ Backup cifrado: $ENCRYPTED_DIR.gpg"
```

### **Gestión de Secretos**

```bash
# Backup de secrets (usar con extrema precaución)
# secrets-backup.sh

SECRETS_DIR="/secure/sicora-secrets"
mkdir -p "$SECRETS_DIR"

# Backup de claves JWT
cp sicora-be-*/jwt-secrets.key "$SECRETS_DIR/"

# Backup de certificados SSL
cp ssl-certificates/* "$SECRETS_DIR/"

# Cifrar directorio completo de secrets
gpg --cipher-algo AES256 --compress-algo 1 --symmetric \
    --output "$SECRETS_DIR.gpg" "$SECRETS_DIR"

# Limpiar secrets sin cifrar
rm -rf "$SECRETS_DIR"
```

---

## 📊 MONITOREO Y VERIFICACIÓN

### **Script de Verificación de Integridad**

```bash
#!/bin/bash
# verify-integrity.sh

BACKUP_BASE="/backup/sicora"
REPORT_FILE="/var/log/sicora-backup-verification.log"

echo "🔍 Verificando integridad de respaldos SICORA..."

# Verificar repositorios Git
for repo in $BACKUP_BASE/mirrors/*; do
    if [ -d "$repo/.git" ]; then
        cd "$repo"
        if git fsck --full; then
            echo "✅ $repo: Integridad OK"
        else
            echo "❌ $repo: Error de integridad"
        fi
    fi
done

# Verificar backups de BD
for dump in $BACKUP_BASE/database/*.dump; do
    if pg_restore --list "$dump" > /dev/null 2>&1; then
        echo "✅ $dump: Integridad OK"
    else
        echo "❌ $dump: Error de integridad"
    fi
done

# Verificar checksums
find "$BACKUP_BASE" -name "*.sha256" | while read checksum_file; do
    if sha256sum -c "$checksum_file"; then
        echo "✅ $(basename $checksum_file): Checksum OK"
    else
        echo "❌ $(basename $checksum_file): Checksum ERROR"
    fi
done

echo "🏁 Verificación de integridad completada"
```

### **Dashboard de Estado de Respaldos**

```bash
#!/bin/bash
# backup-status-dashboard.sh

# Generar reporte HTML de estado
cat > /var/www/html/sicora-backup-status.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>SICORA - Estado de Respaldos</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .status-ok { color: green; }
        .status-error { color: red; }
        .status-warning { color: orange; }
    </style>
</head>
<body>
    <h1>🔒 SICORA - Estado de Respaldos</h1>
    <p><strong>Última actualización:</strong> $(date)</p>

    <h2>📊 Resumen de Respaldos</h2>
    <ul>
        <li>Repositorios Git: $(ls /backup/sicora/mirrors/ | wc -l) respaldados</li>
        <li>Base de datos: $(ls /backup/sicora/database/*.dump | wc -l) backups</li>
        <li>Configuraciones: $(ls /backup/sicora/configs/ | wc -l) sets</li>
        <li>Collections Postman: $(ls /backup/sicora/postman/ | wc -l) backups</li>
    </ul>

    <h2>🔍 Último Respaldo</h2>
    <pre>$(tail -20 /var/log/sicora-backup.log)</pre>

    <h2>📈 Espacio Utilizado</h2>
    <pre>$(du -sh /backup/sicora/*)</pre>

</body>
</html>
EOF

echo "📊 Dashboard actualizado: /var/www/html/sicora-backup-status.html"
```

---

## 🚨 PLAN DE RECUPERACIÓN

### **Procedimiento de Recuperación Rápida**

#### **1. Recuperación de Repositorios**

```bash
#!/bin/bash
# recover-repositories.sh

BACKUP_SOURCE="/backup/sicora/mirrors"
RECOVERY_TARGET="/recovery/sicora"

echo "🔄 Iniciando recuperación de repositorios..."

# Crear directorio de recuperación
mkdir -p "$RECOVERY_TARGET"

# Restaurar cada repositorio
for repo in $BACKUP_SOURCE/*; do
    repo_name=$(basename "$repo")
    echo "📂 Restaurando $repo_name..."

    git clone "$repo" "$RECOVERY_TARGET/$repo_name"

    # Verificar integridad
    cd "$RECOVERY_TARGET/$repo_name"
    if git fsck; then
        echo "✅ $repo_name restaurado correctamente"
    else
        echo "❌ Error en restauración de $repo_name"
    fi
done

echo "🏁 Recuperación de repositorios completada"
```

#### **2. Recuperación de Base de Datos**

```bash
#!/bin/bash
# recover-database.sh

BACKUP_FILE=$1
DB_NAME="sicora_recovered"

if [ -z "$BACKUP_FILE" ]; then
    echo "Uso: $0 <archivo_backup.dump>"
    exit 1
fi

echo "🗄️ Recuperando base de datos desde: $BACKUP_FILE"

# Crear nueva base de datos
createdb "$DB_NAME"

# Restaurar desde backup
pg_restore -d "$DB_NAME" "$BACKUP_FILE"

# Verificar datos críticos
psql -d "$DB_NAME" -c "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM schedules;"

echo "✅ Base de datos recuperada: $DB_NAME"
```

### **Procedimiento de Recuperación por Niveles**

#### **Nivel 1: Recuperación Rápida (15 minutos)**

- Restaurar repositorio principal desde mirror más reciente
- Desplegar configuración de desarrollo
- Validar funcionamiento básico

#### **Nivel 2: Recuperación Completa (1 hora)**

- Restaurar todos los repositorios
- Recuperar base de datos desde último backup completo
- Restablecer configuraciones de producción
- Ejecutar tests de integración

#### **Nivel 3: Recuperación Total (4 horas)**

- Recuperación desde backups externos
- Reconstrucción de infraestructura
- Migración de datos desde múltiples fuentes
- Validación completa del sistema

---

## 🎯 MEJORES PRÁCTICAS ESPECÍFICAS PARA SICORA

### **1. Gestión de Branches Críticas**

```bash
# Proteger branches principales
git config branch.main.pushRemote origin
git config branch.develop.pushRemote origin
git config branch.production.pushRemote origin

# Backup automático antes de merges importantes
git hook pre-merge-commit "./scripts/pre-merge-backup.sh"
```

### **2. Respaldo de Documentación Estructurada**

```bash
#!/bin/bash
# backup-structured-docs.sh

# Respetar estructura de documentación SICORA
DOCS_BACKUP="/backup/sicora/docs/$(date +%Y%m%d)"
mkdir -p "$DOCS_BACKUP"

# Backup manteniendo estructura _docs/
cp -r ./_docs "$DOCS_BACKUP/"
cp README.md "$DOCS_BACKUP/"

# Validar estructura después del backup
./scripts/verify-docs-structure-strict.sh "$DOCS_BACKUP"

echo "📚 Documentación respaldada con estructura validada"
```

### **3. Sincronización Multi-Stack**

```bash
#!/bin/bash
# sync-multistack.sh

# Sincronizar todos los stacks antes del backup
echo "🔄 Sincronizando stacks SICORA..."

# Frontend React
cd sicora-app-fe && npm run build && cd ..

# Backend Go
cd sicora-be-go && make build-all && cd ..

# Backend Python
cd sicora-be-python && python -m pytest && cd ..

# MCP Server
cd sicora-mcp-server && pnpm build && cd ..

echo "✅ Todos los stacks sincronizados"
```

### **4. Backup de Configuraciones de Desarrollo**

```bash
#!/bin/bash
# backup-dev-configs.sh

DEV_BACKUP="/backup/sicora/dev-configs/$(date +%Y%m%d)"
mkdir -p "$DEV_BACKUP"

# VS Code settings
cp -r .vscode "$DEV_BACKUP/"

# Docker configurations
find . -name "docker-compose*.yml" -exec cp {} "$DEV_BACKUP/" \;

# Environment files (sin secretos)
find . -name ".env.example" -exec cp {} "$DEV_BACKUP/" \;

# MCP configurations
cp sicora-mcp-server/.mcprc "$DEV_BACKUP/" 2>/dev/null || true

echo "🛠️ Configuraciones de desarrollo respaldadas"
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### **Fase 1: Setup Inicial (1 día)**

- [ ] Configurar repositorios mirror
- [ ] Crear estructura de directorios de backup
- [ ] Instalar dependencias (git, pg_dump, gpg)
- [ ] Configurar claves de cifrado
- [ ] Probar scripts básicos

### **Fase 2: Automatización (2 días)**

- [ ] Configurar cron jobs
- [ ] Implementar scripts de verificación
- [ ] Configurar notificaciones
- [ ] Probar recuperación básica
- [ ] Documentar procedimientos

### **Fase 3: Integración Completa (3 días)**

- [ ] Integrar con CI/CD
- [ ] Configurar backup en la nube
- [ ] Implementar monitoreo
- [ ] Probar recuperación completa
- [ ] Capacitar al equipo

### **Fase 4: Optimización (1 día)**

- [ ] Optimizar rendimiento
- [ ] Configurar alertas avanzadas
- [ ] Implementar métricas
- [ ] Ajustar políticas de retención
- [ ] Documentación final

---

## 📊 MÉTRICAS Y KPIs

### **Indicadores de Respaldo**

- **RTO (Recovery Time Objective)**: 15 minutos para recuperación rápida
- **RPO (Recovery Point Objective)**: Máximo 6 horas de pérdida de datos
- **Frecuencia**: Diaria para código, continua para commits críticos
- **Retención**: 30 días diarios, 12 semanas semanales, 24 meses anuales

### **Métricas de Calidad**

- **Integridad**: 100% de respaldos verificados
- **Disponibilidad**: 99.9% de acceso a respaldos
- **Tiempo de backup**: < 30 minutos para backup completo
- **Compresión**: > 70% de reducción de espacio

---

## 🔗 RECURSOS Y HERRAMIENTAS

### **Herramientas Recomendadas**

- **Git**: Control de versiones distribuido
- **rsync**: Sincronización eficiente de archivos
- **pg_dump/pg_restore**: Backup de PostgreSQL
- **GPG**: Cifrado de respaldos
- **AWS CLI/rclone**: Sincronización con la nube

### **Scripts de Referencia**

- `./scripts/backup-docs.sh` - Backup existente de documentación
- `./scripts/verify-doc-structure.sh` - Verificación de estructura
- `postman-collections/validate-collections.sh` - Validación de collections

---

## 💡 CONCLUSIONES Y RECOMENDACIONES

### **Implementación Prioritaria**

1. **Inmediato**: Mirror diario de repositorios principales
2. **Semana 1**: Backup automático de base de datos
3. **Semana 2**: Respaldo de configuraciones y secrets
4. **Semana 3**: Integración con almacenamiento en la nube
5. **Semana 4**: Sistema completo de monitoreo y alertas

### **Adaptaciones Específicas para SICORA**

- **Multi-stack**: Scripts especializados para Go, Python, React, Node.js
- **Microservicios**: Backup coordinado de 389 endpoints
- **Documentación**: Respeto estricto a estructura `_docs/`
- **Educativo**: Consideración de períodos académicos críticos

### **Beneficios Esperados**

- **Seguridad**: Protección total del código fuente y datos
- **Continuidad**: Recuperación rápida ante incidentes
- **Compliance**: Cumplimiento de estándares académicos
- **Confianza**: Respaldo robusto para sistema de misión crítica

---

**Documento creado:** 16 de julio de 2025  
**Versión:** 1.0  
**Estado:** Propuesta para implementación  
**Próxima revisión:** 30 días post-implementación
