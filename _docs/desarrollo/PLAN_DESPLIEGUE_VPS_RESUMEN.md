# 🚀 Plan de Despliegue SICORA Backend - Resumen Ejecutivo

## 📌 Estado Actual

✅ **COMPLETADO:**

- Backend Python-FastAPI totalmente validado
- Tests de integración pasando (19/19 tests)
- Configuraciones validadas para todos los entornos
- Scripts de deployment y monitoreo creados
- Paquete de deployment generado y listo
- Documentación completa de deployment

✅ **LISTO PARA PRODUCCIÓN:**

- API Gateway (puerto 8000)
- Notification Service (puerto 8001)
- Base de datos PostgreSQL configurada
- Redis configurado
- Docker y Docker Compose configurados
- Nginx reverse proxy configurado
- Scripts de monitoreo y backup

## 🎯 Plan Paso a Paso para VPS Hostinger

### FASE 1: Preparación Local ✅ COMPLETADA

```bash
cd sicora-be-python
make prepare-deployment
```

**Resultado:** Paquete `sicora-backend-deployment-YYYYMMDD_HHMMSS.tar.gz` creado

### FASE 2: Configuración del VPS

#### Opción A: Fedora Cloud 42 (RECOMENDADO - igual que tu entorno local)

```bash
# 1. Conectar al VPS
ssh fedora@TU_IP_VPS

# 2. Actualizar sistema Fedora
sudo dnf update -y

# 3. Instalar herramientas básicas
sudo dnf install -y curl wget git htop nano vim

# 4. Instalar Docker
sudo dnf install -y docker docker-compose
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# 5. Verificar Docker
docker --version
docker-compose --version

# 6. Configurar firewall (firewalld en Fedora)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# 7. Reiniciar sesión para aplicar cambios de grupo
exit && ssh fedora@TU_IP_VPS
```

#### Opción B: Ubuntu (alternativa)

```bash
# 1. Conectar al VPS
ssh ubuntu@TU_IP_VPS

# 2. Actualizar sistema Ubuntu
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git htop nano

# 3. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 4. Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 5. Configurar firewall (UFW en Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 6. Reiniciar sesión para aplicar cambios de grupo
exit && ssh ubuntu@TU_IP_VPS
```

#### ✅ **Recomendación: Fedora Cloud 42**

**Ventajas de usar Fedora (mismo que tu entorno local):**

- 🔄 **Consistencia**: Mismo SO que tu desarrollo local
- 📦 **DNF**: Gestor de paquetes más moderno que APT
- 🐳 **Docker**: Instalación más directa desde repos oficiales
- 🛡️ **Firewalld**: Firewall más robusto que UFW
- 🚀 **Performance**: Kernel más reciente y optimizaciones
- 🔧 **Troubleshooting**: Conoces mejor el sistema
  sudo ufw allow 443/tcp
  sudo ufw --force enable

# 6. Reiniciar sesión para aplicar cambios de grupo docker

exit && ssh usuario@TU_IP_VPS

````

### FASE 3: Despliegue de la Aplicación

```bash
# 1. Transferir desde máquina local
scp sicora-backend-deployment-*.tar.gz usuario@TU_IP_VPS:~/

# 2. En el VPS, extraer archivos
mkdir -p ~/sicora-backend
cd ~/sicora-backend
tar -xzf ~/sicora-backend-deployment-*.tar.gz

# 3. Configurar variables de entorno
cp deployment/.env.production.template .env.production
nano .env.production  # Editar con valores reales

# 4. Desplegar servicios
chmod +x deployment/deploy.sh
./deployment/deploy.sh production
````

### FASE 4: Configurar Nginx

```bash
# 1. Instalar Nginx
sudo apt install -y nginx

# 2. Configurar virtual host
sudo cp deployment/nginx-sicora.conf /etc/nginx/sites-available/sicora
sudo ln -s /etc/nginx/sites-available/sicora /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# 3. Probar y reiniciar
sudo nginx -t
sudo systemctl restart nginx
```

### FASE 5: Validación de Endpoints

```bash
# Desde máquina local
make validate-endpoints-remote DOMAIN=TU_IP_O_DOMINIO

# O manualmente
curl http://TU_IP/health/api
curl http://TU_IP/health/notification
curl http://TU_IP/api/docs
curl http://TU_IP/notifications/docs
```

## 🔧 Variables de Entorno Críticas

En `.env.production`, configurar:

```env
# Base de datos - CAMBIAR CONTRASEÑA
DATABASE_URL=postgresql+asyncpg://sicora_user:CONTRASEÑA_SEGURA@postgres:5432/sicora_production
POSTGRES_PASSWORD=CONTRASEÑA_SEGURA

# Seguridad - GENERAR CLAVE SECRETA
SECRET_KEY=CLAVE_SECRETA_DE_32_CARACTERES_O_MAS

# Redis
REDIS_URL=redis://redis:6379/0

# Entorno
ENVIRONMENT=production
```

## 📋 URLs Finales de Validación

Una vez desplegado, estos endpoints deben responder:

- **Health API Gateway**: `http://TU_IP/health/api`
- **Health Notifications**: `http://TU_IP/health/notification`
- **API Documentation**: `http://TU_IP/api/docs`
- **Notifications Documentation**: `http://TU_IP/notifications/docs`
- **Status Page**: `http://TU_IP/status`

## 🚨 Troubleshooting Rápido

### Si los contenedores no arrancan:

```bash
docker ps  # Ver estado
docker logs sicora-backend_apigateway_1
docker logs sicora-backend_notification_1
```

### Si Nginx da error 502:

```bash
curl http://localhost:8000/health  # Verificar backend
curl http://localhost:8001/health
sudo nginx -t  # Verificar configuración
sudo systemctl restart nginx
```

### Si no puede conectar a base de datos:

```bash
docker exec -it sicora-backend_postgres_1 psql -U sicora_user -d sicora_production -c "\l"
```

## 📚 Documentación Completa

**Documentación detallada:** `_docs/desarrollo/GUIA_DESPLIEGUE_VPS_HOSTINGER.md`

**Comandos disponibles:**

```bash
make deployment-help          # Ver ayuda
make prepare-deployment       # Preparar paquete
make validate-endpoints       # Validar local
make validate-endpoints-remote DOMAIN=tu-servidor.com  # Validar remoto
```

## ⏱️ Tiempo Estimado

- **Preparación local**: 5 minutos ✅
- **Setup VPS**: 15-20 minutos
- **Deployment**: 10-15 minutos
- **Configuración Nginx**: 5 minutos
- **Validación**: 5 minutos

**Total**: 40-50 minutos

## 🎉 Resultado Final

Una vez completado tendrás:

- ✅ Backend FastAPI completamente funcional en VPS
- ✅ API Gateway accesible vía HTTP
- ✅ Notification Service funcionando
- ✅ Base de datos PostgreSQL en producción
- ✅ Redis para cache
- ✅ Documentación Swagger accesible
- ✅ Monitoreo y logs configurados
- ✅ Endpoints listos para integración con frontend

**¡SICORA Backend estará listo para que conectes el frontend!**
