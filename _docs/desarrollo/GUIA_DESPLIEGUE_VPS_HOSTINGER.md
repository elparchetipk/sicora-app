# 🚀 Guía de Despliegue SICORA Backend en VPS Hostinger

## 📋 Resumen

Esta guía proporciona instrucciones paso a paso para desplegar el stack backend FastAPI de SICORA en un VPS de Hostinger, configurar el entorno de producción, y validar que todos los endpoints funcionen correctamente antes de la integración con el frontend.

## 🏗️ Arquitectura de Despliegue

```
VPS Hostinger (Ubuntu 20.04/22.04)
├── Docker & Docker Compose
├── Nginx (Reverse Proxy)
├── Servicios SICORA:
│   ├── PostgreSQL (Puerto 5432)
│   ├── Redis (Puerto 6379)
│   ├── API Gateway (Puerto 8000 → 80/443)
│   └── Notification Service (Puerto 8001 → 80/443)
├── SSL/TLS (Let's Encrypt)
└── Monitoreo y Logs
```

## 🔧 Prerequisitos del VPS

### Especificaciones Mínimas Recomendadas

- **RAM**: 2GB mínimo (4GB recomendado)
- **CPU**: 1 vCore mínimo (2 vCores recomendado)
- **Almacenamiento**: 20GB mínimo (50GB recomendado)
- **SO**: Ubuntu 20.04 LTS o superior
- **Ancho de banda**: Sin límite estricto

### Acceso Requerido

- Acceso SSH con permisos sudo
- Dominio o subdominio configurado (opcional pero recomendado)
- Puertos abiertos: 22 (SSH), 80 (HTTP), 443 (HTTPS)

## 📝 Plan de Despliegue Paso a Paso

### FASE 1: Preparación del Entorno Local

#### 1.1 Verificar Estado Local

```bash
# Ejecutar desde sicora-app/sicora-be-python/
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-be-python

# Verificar que todos los tests pasan
make test-integration

# Validar configuraciones
python scripts/config_manager.py validate-all

# Verificar archivos de deployment
ls -la deployment/
ls -la scripts/prepare-vps-deployment.sh
```

#### 1.2 Preparar Archivos de Deployment

```bash
# Ejecutar script de preparación
chmod +x scripts/prepare-vps-deployment.sh
./scripts/prepare-vps-deployment.sh

# Crear paquete de deployment
tar -czf sicora-backend-deployment.tar.gz \
    deployment/ \
    scripts/ \
    shared/ \
    apigateway/ \
    notificationservice-template/ \
    pyproject.toml \
    requirements-dev.txt \
    .env.production
```

### FASE 2: Configuración del VPS

#### 2.1 Conexión Inicial al VPS

##### Opción A: Fedora Cloud 42 (RECOMENDADO)

```bash
# Conectar via SSH
ssh fedora@TU_IP_VPS
```

##### Opción B: Ubuntu

```bash
# Conectar via SSH
ssh ubuntu@TU_IP_VPS
# O si usas root
ssh root@TU_IP_VPS
```

#### 2.2 Actualización del Sistema

##### Para Fedora Cloud 42:

```bash
# Actualizar paquetes del sistema
sudo dnf update -y

# Instalar herramientas básicas
sudo dnf install -y curl wget git htop nano vim
```

##### Para Ubuntu:

```bash
# Actualizar paquetes del sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas básicas
sudo apt install -y curl wget git htop nano vim
```

#### 2.3 Instalación de Docker

##### Para Fedora Cloud 42:

```bash
# Instalar Docker desde repositorios oficiales
sudo dnf install -y docker docker-compose

# Habilitar y iniciar Docker
sudo systemctl enable docker
sudo systemctl start docker

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Verificar instalación
docker --version
docker-compose --version
```

##### Para Ubuntu:

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version
```

#### 2.4 Configuración de Firewall

##### Para Fedora Cloud 42:

```bash
# Configurar firewalld (firewall de Fedora)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# Verificar estado
sudo firewall-cmd --list-all
```

##### Para Ubuntu:

```bash
# Configurar UFW (firewall de Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Verificar status
sudo ufw status
```

#### 2.5 Reiniciar Sesión

```bash
# Reiniciar sesión para aplicar cambios de grupo docker
exit

# Volver a conectar (Fedora)
ssh fedora@TU_IP_VPS

# O Ubuntu
ssh ubuntu@TU_IP_VPS
docker-compose --version

# Reiniciar sesión para aplicar cambios de grupo
exit
# Volver a conectar via SSH
```

#### 2.4 Configuración de Firewall

```bash
# Configurar UFW (si está disponible)
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Verificar status
sudo ufw status
```

### FASE 3: Despliegue de la Aplicación

#### 3.1 Transferir Archivos al VPS

```bash
# Desde tu máquina local, copiar archivos al VPS
scp sicora-backend-deployment.tar.gz usuario@TU_IP_VPS:~/

# En el VPS, crear directorio y extraer
mkdir -p ~/sicora-backend
cd ~/sicora-backend
tar -xzf ~/sicora-backend-deployment.tar.gz
```

#### 3.2 Configurar Variables de Entorno

```bash
# En el VPS, crear archivo .env para producción
cd ~/sicora-backend

# Editar archivo .env.production con valores reales
nano .env.production
```

**Contenido de `.env.production`:**

```env
# Entorno
ENVIRONMENT=production

# Base de datos
DATABASE_URL=postgresql+asyncpg://sicora_user:CONTRASEÑA_SEGURA@postgres:5432/sicora_production
POSTGRES_PASSWORD=CONTRASEÑA_SEGURA

# Redis
REDIS_URL=redis://redis:6379/0

# Seguridad
SECRET_KEY=TU_CLAVE_SECRETA_SUPER_SEGURA_DE_32_CARACTERES_O_MAS

# API Gateway
APIGATEWAY_HOST=0.0.0.0
APIGATEWAY_PORT=8000

# Notification Service
NOTIFICATION_HOST=0.0.0.0
NOTIFICATION_PORT=8001

# Logs
LOG_LEVEL=INFO
```

#### 3.3 Construir y Levantar Servicios

```bash
# Hacer ejecutable el script de deployment
chmod +x deployment/deploy.sh

# Ejecutar deployment en producción
./deployment/deploy.sh production
```

### FASE 4: Configuración de Nginx (Reverse Proxy)

#### 4.1 Instalar Nginx

```bash
sudo apt install -y nginx

# Verificar que esté corriendo
sudo systemctl status nginx
```

#### 4.2 Configurar Virtual Host

```bash
# Crear configuración para SICORA
sudo nano /etc/nginx/sites-available/sicora
```

**Contenido de `/etc/nginx/sites-available/sicora`:**

```nginx
server {
    listen 80;
    server_name TU_DOMINIO.COM;  # Cambiar por tu dominio o IP

    # API Gateway
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Notification Service
    location /notifications/ {
        proxy_pass http://localhost:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health checks directos (opcional)
    location /health/api {
        proxy_pass http://localhost:8000/health;
    }

    location /health/notification {
        proxy_pass http://localhost:8001/health;
    }
}
```

#### 4.3 Activar Configuración

```bash
# Habilitar el sitio
sudo ln -s /etc/nginx/sites-available/sicora /etc/nginx/sites-enabled/

# Deshabilitar sitio por defecto
sudo rm /etc/nginx/sites-enabled/default

# Probar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### FASE 5: Configuración SSL/TLS (Opcional pero Recomendado)

#### 5.1 Instalar Certbot

```bash
sudo apt install -y snapd
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot

# Crear enlace simbólico
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

#### 5.2 Obtener Certificado SSL

```bash
# Obtener certificado (solo si tienes dominio)
sudo certbot --nginx -d TU_DOMINIO.COM

# Verificar renovación automática
sudo certbot renew --dry-run
```

### FASE 6: Validación y Testing de Endpoints

#### 6.1 Verificar Servicios

```bash
# Verificar que los contenedores estén corriendo
docker ps

# Verificar logs
docker logs sicora-backend_apigateway_1
docker logs sicora-backend_notification_1
docker logs sicora-backend_postgres_1
docker logs sicora-backend_redis_1
```

#### 6.2 Testing de Endpoints Locales

```bash
# Test de health checks directos
curl http://localhost:8000/health
curl http://localhost:8001/health

# Test de health checks via Nginx
curl http://TU_DOMINIO_O_IP/health/api
curl http://TU_DOMINIO_O_IP/health/notification
```

#### 6.3 Testing desde Máquina Externa

```bash
# Desde tu máquina local o Postman
curl http://TU_DOMINIO_O_IP/api/health
curl http://TU_DOMINIO_O_IP/notifications/health

# Si tienes SSL configurado
curl https://TU_DOMINIO.COM/api/health
curl https://TU_DOMINIO.COM/notifications/health
```

### FASE 7: Monitoreo y Mantenimiento

#### 7.1 Scripts de Monitoreo

```bash
# Crear script de monitoreo básico
nano ~/monitor-sicora.sh
```

**Contenido de `monitor-sicora.sh`:**

```bash
#!/bin/bash
echo "=== SICORA Backend Status ==="
echo "Fecha: $(date)"
echo ""

echo "=== Docker Containers ==="
docker ps

echo ""
echo "=== Health Checks ==="
echo "API Gateway: $(curl -s http://localhost:8000/health || echo 'FAILED')"
echo "Notification: $(curl -s http://localhost:8001/health || echo 'FAILED')"

echo ""
echo "=== System Resources ==="
free -h
df -h

echo ""
echo "=== Recent Logs (Last 10 lines) ==="
echo "--- API Gateway ---"
docker logs --tail 10 sicora-backend_apigateway_1
echo "--- Notification ---"
docker logs --tail 10 sicora-backend_notification_1
```

```bash
chmod +x ~/monitor-sicora.sh
```

#### 7.2 Configurar Logs Persistentes

```bash
# Crear directorio para logs
mkdir -p ~/sicora-logs

# Script para backup de logs
nano ~/backup-logs.sh
```

**Contenido de `backup-logs.sh`:**

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
LOG_DIR="~/sicora-logs"

docker logs sicora-backend_apigateway_1 > "$LOG_DIR/apigateway_$DATE.log"
docker logs sicora-backend_notification_1 > "$LOG_DIR/notification_$DATE.log"

# Limpiar logs antiguos (mantener solo 7 días)
find "$LOG_DIR" -name "*.log" -mtime +7 -delete
```

```bash
chmod +x ~/backup-logs.sh

# Agregar a crontab para backup diario
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup-logs.sh") | crontab -
```

## 🧪 Validación Completa de Endpoints

### Checklist de Validación Post-Despliegue

#### ✅ Health Checks

- [ ] `GET /health` en API Gateway (puerto 8000)
- [ ] `GET /health` en Notification Service (puerto 8001)
- [ ] Health checks via Nginx proxy
- [ ] SSL funciona correctamente (si aplicable)

#### ✅ API Gateway Endpoints

- [ ] `GET /` - Página de bienvenida
- [ ] `GET /docs` - Documentación Swagger
- [ ] `GET /redoc` - Documentación ReDoc
- [ ] Endpoints específicos de tu API

#### ✅ Notification Service Endpoints

- [ ] `GET /` - Página de bienvenida
- [ ] `GET /docs` - Documentación Swagger
- [ ] Endpoints de notificaciones

#### ✅ Base de Datos

- [ ] Conexión PostgreSQL funciona
- [ ] Tablas creadas correctamente
- [ ] Migraciones ejecutadas (si aplicable)

#### ✅ Cache/Redis

- [ ] Conexión Redis funciona
- [ ] Cache básico operativo

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. Contenedores no arrancan

```bash
# Verificar logs detallados
docker-compose logs

# Verificar configuración
docker-compose config

# Reiniciar servicios
docker-compose down && docker-compose up -d
```

#### 2. Error de conexión a base de datos

```bash
# Verificar que PostgreSQL esté corriendo
docker exec -it sicora-backend_postgres_1 psql -U sicora_user -d sicora_production -c "\l"

# Verificar variables de entorno
docker exec sicora-backend_apigateway_1 env | grep DATABASE_URL
```

#### 3. Nginx errores 502/503

```bash
# Verificar configuración Nginx
sudo nginx -t

# Verificar que servicios backend respondan
curl http://localhost:8000/health
curl http://localhost:8001/health

# Verificar logs Nginx
sudo tail -f /var/log/nginx/error.log
```

#### 4. Problemas de SSL

```bash
# Verificar certificado
sudo certbot certificates

# Renovar manualmente
sudo certbot renew

# Verificar configuración Nginx SSL
sudo nginx -t
```

## 📚 Recursos Adicionales

### Comandos Útiles de Mantenimiento

```bash
# Actualizar servicios
cd ~/sicora-backend
git pull  # Si conectaste con repositorio
./deployment/deploy.sh production

# Backup de base de datos
docker exec sicora-backend_postgres_1 pg_dump -U sicora_user sicora_production > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker exec -i sicora-backend_postgres_1 psql -U sicora_user sicora_production < backup_FECHA.sql

# Ver uso de recursos
docker stats

# Limpiar contenedores e imágenes no usadas
docker system prune -f
```

### URLs Importantes Post-Despliegue

Una vez completado el despliegue, estos serán tus endpoints principales:

- **API Gateway**: `http://TU_DOMINIO/api/`
- **Notification Service**: `http://TU_DOMINIO/notifications/`
- **Documentación API Gateway**: `http://TU_DOMINIO/api/docs`
- **Documentación Notifications**: `http://TU_DOMINIO/notifications/docs`
- **Health Check API**: `http://TU_DOMINIO/health/api`
- **Health Check Notifications**: `http://TU_DOMINIO/health/notification`

### Próximos Pasos

1. **Validar todos los endpoints** usando Postman o curl
2. **Configurar monitoreo avanzado** (opcional: Prometheus + Grafana)
3. **Configurar backup automático** de base de datos
4. **Preparar frontend** para conectar a estos endpoints
5. **Configurar CI/CD** para deployments automáticos

---

**⚠️ IMPORTANTE**: Antes de continuar con la integración del frontend, asegúrate de que todos los health checks pasen y puedas acceder a la documentación Swagger desde URLs externas.
