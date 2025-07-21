#!/bin/bash
# Script específico para deployment en Fedora Cloud 42
# Comandos optimizados para Fedora (mismo OS que tu entorno local)

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🚀 SICORA Backend - Deployment en Fedora Cloud 42${NC}"
echo -e "${GREEN}Comandos específicos para Hostinger VPS con Fedora${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} 1. PREPARACIÓN LOCAL (YA COMPLETADA)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ make prepare-deployment${NC} - Paquete listo"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} 2. CONFIGURAR VPS FEDORA CLOUD 42${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${YELLOW}🔑 Conectar SSH:${NC}"
echo -e "   ${GREEN}ssh fedora@TU_IP_VPS${NC}"
echo ""

echo -e "${YELLOW}📦 Setup completo del sistema (copia y pega todo):${NC}"
cat << 'EOF'

# Actualizar Fedora
sudo dnf update -y

# Instalar herramientas
sudo dnf install -y curl wget git htop nano vim

# Instalar Docker y Docker Compose
sudo dnf install -y docker docker-compose

# Configurar Docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# Configurar Firewall
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# Verificar instalación
docker --version
docker-compose --version

# Reiniciar sesión para aplicar cambios
exit

EOF

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} 3. TRANSFERIR Y DESPLEGAR${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${YELLOW}💾 Desde tu máquina local:${NC}"
echo -e "   ${GREEN}scp sicora-backend-deployment-*.tar.gz fedora@TU_IP_VPS:~/${NC}"
echo ""

echo -e "${YELLOW}📂 En el VPS Fedora (copia y pega todo):${NC}"
cat << 'EOF'

# Volver a conectar después del exit anterior
ssh fedora@TU_IP_VPS

# Extraer paquete
mkdir -p ~/sicora-backend
cd ~/sicora-backend
tar -xzf ~/sicora-backend-deployment-*.tar.gz

# Configurar variables de entorno
cp deployment/.env.production.template .env.production

# EDITAR ARCHIVO .env.production
nano .env.production

EOF

echo ""
echo -e "${RED}⚠️  IMPORTANTE - Cambiar en .env.production:${NC}"
echo -e "${YELLOW}   POSTGRES_PASSWORD=CONTRASEÑA_MUY_SEGURA${NC}"
echo -e "${YELLOW}   SECRET_KEY=CLAVE_SECRETA_DE_32_CARACTERES_MINIMO${NC}"
echo -e "${YELLOW}   DATABASE_URL (usar la nueva contraseña)${NC}"
echo ""

echo -e "${YELLOW}🚀 Desplegar servicios:${NC}"
echo -e "   ${GREEN}chmod +x deployment/deploy.sh${NC}"
echo -e "   ${GREEN}./deployment/deploy.sh production${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} 4. CONFIGURAR NGINX${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${YELLOW}🌐 Instalar y configurar Nginx (copia y pega todo):${NC}"
cat << 'EOF'

# Instalar Nginx
sudo dnf install -y nginx

# Configurar virtual host
sudo cp deployment/nginx-sicora.conf /etc/nginx/conf.d/sicora.conf

# Editar configuración si necesitas cambiar el dominio
sudo nano /etc/nginx/conf.d/sicora.conf

# Probar configuración
sudo nginx -t

# Habilitar e iniciar Nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Verificar estado
sudo systemctl status nginx

EOF

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} 5. VALIDACIÓN FINAL${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${YELLOW}🧪 Verificar en el VPS:${NC}"
cat << 'EOF'

# Verificar contenedores
docker ps

# Verificar health checks locales
curl http://localhost:8000/health
curl http://localhost:8001/health

# Verificar a través de Nginx
curl http://localhost/health/api
curl http://localhost/health/notification

EOF

echo -e "${YELLOW}🌐 Desde tu máquina local:${NC}"
echo -e "   ${GREEN}make validate-endpoints-remote DOMAIN=TU_IP_VPS${NC}"
echo ""

echo -e "${YELLOW}🔍 URLs a verificar en el navegador:${NC}"
echo -e "   • ${GREEN}http://TU_IP_VPS/health/api${NC}"
echo -e "   • ${GREEN}http://TU_IP_VPS/health/notification${NC}"
echo -e "   • ${GREEN}http://TU_IP_VPS/api/docs${NC}"
echo -e "   • ${GREEN}http://TU_IP_VPS/notifications/docs${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN} ✅ VENTAJAS DE FEDORA CLOUD 42${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}🔄 Consistencia:${NC} Mismo OS que tu desarrollo local"
echo -e "${GREEN}📦 DNF:${NC} Gestor de paquetes más moderno"
echo -e "${GREEN}🐳 Docker:${NC} Instalación directa desde repos oficiales"
echo -e "${GREEN}🛡️ Firewalld:${NC} Firewall más robusto"
echo -e "${GREEN}🚀 Performance:${NC} Kernel más reciente"
echo -e "${GREEN}🔧 Familiar:${NC} Conoces mejor el sistema"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}🎉 Tiempo estimado: 30-40 minutos${NC}"
echo -e "${PURPLE}🎯 Al finalizar: Backend listo para frontend${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
