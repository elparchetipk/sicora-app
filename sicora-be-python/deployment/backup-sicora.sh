#!/bin/bash
# Script de backup para SICORA Backend

BACKUP_DIR="$HOME/sicora-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio de backups si no existe
mkdir -p "$BACKUP_DIR"

echo "🔄 Iniciando backup de SICORA Backend..."

# Backup de base de datos
echo "📊 Creando backup de base de datos..."
docker exec sicora-backend_postgres_1 pg_dump -U sicora_user sicora_production > "$BACKUP_DIR/db_backup_$DATE.sql"

if [ $? -eq 0 ]; then
    echo "✅ Backup de base de datos completado: db_backup_$DATE.sql"
else
    echo "❌ Error en backup de base de datos"
fi

# Backup de logs
echo "📝 Creando backup de logs..."
mkdir -p "$BACKUP_DIR/logs_$DATE"

docker logs sicora-backend_apigateway_1 > "$BACKUP_DIR/logs_$DATE/apigateway.log" 2>&1
docker logs sicora-backend_notification_1 > "$BACKUP_DIR/logs_$DATE/notification.log" 2>&1
docker logs sicora-backend_postgres_1 > "$BACKUP_DIR/logs_$DATE/postgres.log" 2>&1
docker logs sicora-backend_redis_1 > "$BACKUP_DIR/logs_$DATE/redis.log" 2>&1

# Backup de configuración
echo "⚙️ Creando backup de configuración..."
cp -r ~/sicora-backend/deployment "$BACKUP_DIR/config_$DATE/"
cp ~/sicora-backend/.env.production "$BACKUP_DIR/config_$DATE/" 2>/dev/null || echo "No .env.production found"

# Comprimir backups
echo "🗜️ Comprimiendo backups..."
tar -czf "$BACKUP_DIR/sicora_backup_$DATE.tar.gz" \
    "$BACKUP_DIR/db_backup_$DATE.sql" \
    "$BACKUP_DIR/logs_$DATE/" \
    "$BACKUP_DIR/config_$DATE/"

# Limpiar archivos temporales
rm -f "$BACKUP_DIR/db_backup_$DATE.sql"
rm -rf "$BACKUP_DIR/logs_$DATE/"
rm -rf "$BACKUP_DIR/config_$DATE/"

echo "✅ Backup completado: sicora_backup_$DATE.tar.gz"

# Limpiar backups antiguos (mantener solo 7 días)
find "$BACKUP_DIR" -name "sicora_backup_*.tar.gz" -mtime +7 -delete

echo "🧹 Backups antiguos limpiados"
