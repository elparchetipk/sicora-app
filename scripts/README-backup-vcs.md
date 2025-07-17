# 🔒 Scripts de Respaldo VCS SICORA

Este directorio contiene los scripts para implementar la estrategia de respaldo del código VCS según el documento [ESTRATEGIA_RESPALDO_VCS.md](../_docs/desarrollo/ESTRATEGIA_RESPALDO_VCS.md).

## 🚀 Instalación Rápida

### 1. Ejecutar Setup Automático

```bash
# Desde la raíz del proyecto sicora-app
./scripts/setup-vcs-backup-strategy.sh
```

Este script creará automáticamente:

- ✅ Estructura de directorios de respaldo
- ✅ Scripts de respaldo automático
- ✅ Configuración de cron jobs
- ✅ Pruebas de funcionalidad

### 2. Verificar Instalación

```bash
# Verificar que la estructura fue creada
ls -la /backup/sicora/

# Probar backup manual
/backup/sicora/scripts/daily-backup.sh
```

## 📋 Scripts Disponibles

### Scripts Principales

| Script                          | Descripción                               | Frecuencia     |
| ------------------------------- | ----------------------------------------- | -------------- |
| `setup-vcs-backup-strategy.sh`  | Instalación inicial de toda la estrategia | Una vez        |
| `daily-backup.sh`               | Backup maestro diario                     | Diario 2:00 AM |
| `mirror-repositories.sh`        | Mirror de repositorios Git                | Cada 6 horas   |
| `backup-configurations.sh`      | Respaldo de configuraciones               | Diario         |
| `backup-database.sh`            | Respaldo de PostgreSQL                    | Diario         |
| `backup-postman-collections.sh` | Respaldo de collections Postman           | Diario         |

### Scripts de Soporte

| Script                    | Descripción                                 |
| ------------------------- | ------------------------------------------- |
| `backup-docs.sh`          | Script existente de backup de documentación |
| `verify-doc-structure.sh` | Verificación de estructura de docs          |

## 🗂️ Estructura de Respaldos

```
/backup/sicora/
├── mirrors/                    # Mirrors de repositorios Git
│   ├── sicora-app/            # Monorepo principal
│   ├── sicora-app-fe/         # Frontend React
│   ├── sicora-be-go/          # Backend Go
│   └── sicora-be-python/      # Backend Python
├── database/                   # Backups de PostgreSQL
│   └── YYYYMMDD/
├── configs/                    # Configuraciones y variables
│   └── YYYYMMDD/
├── postman/                    # Collections Postman
│   └── YYYYMMDD/
├── scripts/                    # Scripts de respaldo
├── logs/                       # Logs de operaciones
└── sicora-complete-*.tar.gz   # Snapshots completos
```

## ⚙️ Configuración

### Variables de Entorno

Los scripts utilizan estas configuraciones por defecto:

```bash
# Base de datos
DB_HOST="localhost"
DB_PORT="5433"  # Puerto de sicora-infra
DB_USER="sicora_user"
DB_NAME="sicora_dev"

# Directorios
PROJECT_ROOT="/home/epti/Documentos/epti-dev/sicora-app"
BACKUP_BASE="/backup/sicora"
```

### Personalización

Para personalizar la configuración, editar los scripts en `/backup/sicora/scripts/`:

```bash
# Editar configuración de base de datos
nano /backup/sicora/scripts/backup-database.sh

# Editar repositorios a respaldar
nano /backup/sicora/scripts/mirror-repositories.sh
```

## 🕐 Programación Automática

### Cron Jobs Configurados

```bash
# Respaldo diario a las 2:00 AM
0 2 * * * /backup/sicora/scripts/daily-backup.sh

# Mirror cada 6 horas
0 */6 * * * /backup/sicora/scripts/mirror-repositories.sh

# Limpieza semanal (domingos 4:00 AM)
0 4 * * 0 find /backup/sicora -name "*.tar.gz" -mtime +30 -delete
```

### Activar Cron Jobs

```bash
# Instalar cron jobs
sudo crontab -u $USER /tmp/sicora-backup-cron

# Verificar instalación
crontab -l
```

## 🔍 Monitoreo y Verificación

### Verificar Estado de Respaldos

```bash
# Ver último reporte de estado
cat /backup/sicora/backup-status-$(date +%Y%m%d).txt

# Ver logs de backup
tail -f /backup/sicora/logs/sicora-backup-$(date +%Y%m%d).log

# Verificar espacio utilizado
du -sh /backup/sicora/*
```

### Validar Integridad

```bash
# Verificar último snapshot
tar -tzf /backup/sicora/sicora-complete-*.tar.gz | head -20

# Verificar backup de base de datos
pg_restore --list /backup/sicora/database/*/sicora_full_*.dump

# Verificar mirrors de Git
cd /backup/sicora/mirrors/sicora-app && git fsck
```

## 🔄 Recuperación

### Recuperación Rápida (15 min)

```bash
# Restaurar desde mirror más reciente
cp -r /backup/sicora/mirrors/sicora-app /recovery/sicora-app

# Verificar integridad
cd /recovery/sicora-app && git status
```

### Recuperación Completa (1 hora)

```bash
# Extraer snapshot completo
tar -xzf /backup/sicora/sicora-complete-YYYYMMDD_HHMMSS.tar.gz -C /recovery/

# Restaurar base de datos
createdb sicora_recovered
pg_restore -d sicora_recovered /backup/sicora/database/*/sicora_full_*.dump

# Restaurar configuraciones
cp -r /backup/sicora/configs/latest/* /recovery/sicora-app/
```

## 📊 Métricas y KPIs

### Objetivos de Recuperación

- **RTO (Recovery Time Objective)**: 15 minutos
- **RPO (Recovery Point Objective)**: 6 horas máximo
- **Retención**: 30 días diarios, 12 semanas semanales

### Verificación de Cumplimiento

```bash
# Verificar frecuencia de backups
ls -lt /backup/sicora/sicora-complete-*.tar.gz | head -5

# Verificar tamaño de backups
du -sh /backup/sicora/sicora-complete-*.tar.gz | tail -10

# Verificar logs por errores
grep "ERROR\|FAIL" /backup/sicora/logs/sicora-backup-*.log
```

## 🚨 Troubleshooting

### Problemas Comunes

#### Error: No se puede conectar a la base de datos

```bash
# Verificar que PostgreSQL está ejecutándose
cd sicora-infra
docker compose -f docker/docker-compose.yml ps postgres

# Iniciar PostgreSQL si está detenido
docker compose -f docker/docker-compose.yml up -d postgres
```

#### Error: Permisos insuficientes

```bash
# Cambiar propietario de directorios de backup
sudo chown -R $USER:$USER /backup/sicora

# Hacer scripts ejecutables
chmod +x /backup/sicora/scripts/*.sh
```

#### Error: Espacio insuficiente

```bash
# Limpiar backups antiguos manualmente
find /backup/sicora -name "*.tar.gz" -mtime +7 -delete

# Verificar espacio disponible
df -h /backup
```

### Logs y Diagnóstico

```bash
# Ver logs de instalación
cat /var/log/sicora-backup-setup.log

# Ver logs de operación diaria
tail -50 /backup/sicora/logs/sicora-backup-$(date +%Y%m%d).log

# Verificar configuración de cron
crontab -l | grep sicora
```

## 🔗 Referencias

- [Estrategia de Respaldo VCS](../_docs/desarrollo/ESTRATEGIA_RESPALDO_VCS.md) - Documentación completa
- [Instrucciones de Copilot](../.github/copilot-instructions.md) - Estándares del proyecto
- [Backup de Documentación](./backup-docs.sh) - Script existente

## 📝 Notas Importantes

1. **Seguridad**: Los scripts no respaldan archivos `.env` reales (solo `.env.example`)
2. **Espacio**: Monitorear regularmente el espacio utilizado en `/backup/`
3. **Testing**: Probar recuperación mensualmente
4. **Updates**: Revisar configuración después de cambios importantes en el proyecto

---

**Creado:** 16 de julio de 2025  
**Última actualización:** 16 de julio de 2025  
**Mantenido por:** Equipo SICORA
