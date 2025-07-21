#!/bin/bash
# Script de demostración del deployment completo de SICORA Backend
# Este script muestra todos los comandos que necesitas ejecutar para el deployment

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Función para mostrar comandos
show_command() {
    echo -e "${BLUE}➤ $1${NC}"
    echo -e "${YELLOW}   $2${NC}"
    echo ""
}

# Función para mostrar secciones
show_section() {
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN} $1${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

echo -e "${PURPLE}🚀 SICORA Backend - Deployment Demo Script${NC}"
echo -e "${PURPLE}Este script muestra los comandos para desplegar en VPS Hostinger${NC}"
echo ""

show_section "FASE 1: PREPARACIÓN LOCAL (YA COMPLETADA)"

show_command "1. Preparar paquete de deployment:" \
    "make prepare-deployment"

show_command "2. Validar tests locales:" \
    "make test-integration"

show_command "3. Ver archivos generados:" \
    "ls -la sicora-backend-deployment-*.tar.gz && ls -la deployment/"

echo -e "${GREEN}✅ FASE 1 COMPLETADA - Paquete listo para transferir${NC}"
echo ""

show_section "FASE 2: CONFIGURACIÓN DEL VPS"

show_section "FASE 2: CONFIGURACIÓN DEL VPS"

echo -e "${PURPLE}🐧 OPCIÓN A: FEDORA CLOUD 42 (RECOMENDADO - igual que tu entorno local)${NC}"
echo ""

show_command "1. Conectar al VPS Fedora:" \
    "ssh fedora@TU_IP_VPS"

show_command "2. Actualizar sistema Fedora:" \
    "sudo dnf update -y"

show_command "3. Instalar herramientas básicas:" \
    "sudo dnf install -y curl wget git htop nano vim"

show_command "4. Instalar Docker desde repos oficiales:" \
    "sudo dnf install -y docker docker-compose"

show_command "5. Habilitar e iniciar Docker:" \
    "sudo systemctl enable docker && sudo systemctl start docker"

show_command "6. Configurar usuario Docker:" \
    "sudo usermod -aG docker \$USER"

show_command "7. Configurar firewall (firewalld):" \
    "sudo firewall-cmd --permanent --add-service=ssh --add-service=http --add-service=https && sudo firewall-cmd --reload"

show_command "8. Verificar instalaciones:" \
    "docker --version && docker-compose --version"

show_command "9. Reiniciar sesión SSH:" \
    "exit && ssh fedora@TU_IP_VPS"

echo ""
echo -e "${YELLOW}🐧 OPCIÓN B: UBUNTU (alternativa)${NC}"
echo ""

show_command "1. Conectar al VPS Ubuntu:" \
    "ssh ubuntu@TU_IP_VPS"

show_command "2. Actualizar sistema Ubuntu:" \
    "sudo apt update && sudo apt upgrade -y"

show_command "3. Instalar herramientas básicas:" \
    "sudo apt install -y curl wget git htop nano vim"

show_command "4. Instalar Docker:" \
    "curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh"

show_command "5. Configurar usuario Docker:" \
    "sudo usermod -aG docker \$USER"

show_command "6. Instalar Docker Compose:" \
    "sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose"

show_command "7. Hacer Docker Compose ejecutable:" \
    "sudo chmod +x /usr/local/bin/docker-compose"

show_command "8. Configurar firewall (UFW):" \
    "sudo ufw allow ssh && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp && sudo ufw --force enable"

show_command "9. Verificar instalaciones:" \
    "docker --version && docker-compose --version"

show_command "10. Reiniciar sesión SSH:" \
    "exit && ssh ubuntu@TU_IP_VPS"

show_section "FASE 3: TRANSFERIR Y DESPLEGAR"

show_command "1. Desde tu máquina local, transferir paquete:" \
    "scp sicora-backend-deployment-*.tar.gz usuario@TU_IP_VPS:~/"

show_command "2. En el VPS, crear directorio:" \
    "mkdir -p ~/sicora-backend && cd ~/sicora-backend"

show_command "3. Extraer paquete:" \
    "tar -xzf ~/sicora-backend-deployment-*.tar.gz"

show_command "4. Configurar variables de entorno:" \
    "cp deployment/.env.production.template .env.production"

show_command "5. EDITAR VARIABLES (MUY IMPORTANTE):" \
    "nano .env.production"

echo -e "${RED}⚠️  IMPORTANTE: En .env.production, cambiar:${NC}"
echo -e "${YELLOW}   - POSTGRES_PASSWORD=CONTRASEÑA_MUY_SEGURA${NC}"
echo -e "${YELLOW}   - SECRET_KEY=CLAVE_SECRETA_DE_32_CARACTERES_MINIMO${NC}"
echo -e "${YELLOW}   - DATABASE_URL con la nueva contraseña${NC}"
echo ""

show_command "6. Hacer ejecutable el script de deployment:" \
    "chmod +x deployment/deploy.sh"

show_command "7. DESPLEGAR SERVICIOS:" \
    "./deployment/deploy.sh production"

show_section "FASE 4: CONFIGURAR NGINX"

show_command "1. Instalar Nginx:" \
    "sudo apt install -y nginx"

show_command "2. Copiar configuración:" \
    "sudo cp deployment/nginx-sicora.conf /etc/nginx/sites-available/sicora"

show_command "3. Habilitar sitio:" \
    "sudo ln -s /etc/nginx/sites-available/sicora /etc/nginx/sites-enabled/"

show_command "4. Deshabilitar sitio por defecto:" \
    "sudo rm /etc/nginx/sites-enabled/default"

show_command "5. Probar configuración:" \
    "sudo nginx -t"

show_command "6. Reiniciar Nginx:" \
    "sudo systemctl restart nginx"

show_section "FASE 5: VALIDACIÓN"

show_command "1. Verificar contenedores Docker:" \
    "docker ps"

show_command "2. Verificar health checks locales:" \
    "curl http://localhost:8000/health && curl http://localhost:8001/health"

show_command "3. Verificar a través de Nginx:" \
    "curl http://localhost/health/api && curl http://localhost/health/notification"

show_command "4. Desde tu máquina local, validar remotamente:" \
    "make validate-endpoints-remote DOMAIN=TU_IP_VPS"

show_command "5. Verificar documentación Swagger:" \
    "curl http://TU_IP_VPS/api/docs && curl http://TU_IP_VPS/notifications/docs"

show_section "COMANDOS DE MONITOREO Y MANTENIMIENTO"

show_command "Ver logs en tiempo real:" \
    "docker logs -f sicora-backend_apigateway_1"

show_command "Ejecutar script de monitoreo:" \
    "./deployment/monitor-sicora.sh"

show_command "Crear backup:" \
    "./deployment/backup-sicora.sh"

show_command "Reiniciar servicios si es necesario:" \
    "./deployment/deploy.sh production"

show_section "URLs FINALES DE VALIDACIÓN"

echo -e "${GREEN}Una vez completado el deployment, estos endpoints deben funcionar:${NC}"
echo ""
echo -e "${BLUE}🏥 Health Checks:${NC}"
echo -e "   • http://TU_IP/health/api"
echo -e "   • http://TU_IP/health/notification"
echo ""
echo -e "${BLUE}📚 Documentación:${NC}"
echo -e "   • http://TU_IP/api/docs"
echo -e "   • http://TU_IP/notifications/docs"
echo ""
echo -e "${BLUE}🌐 Endpoints principales:${NC}"
echo -e "   • http://TU_IP/api/"
echo -e "   • http://TU_IP/notifications/"
echo ""
echo -e "${BLUE}📊 Status:${NC}"
echo -e "   • http://TU_IP/status"
echo ""

show_section "TROUBLESHOOTING"

echo -e "${YELLOW}Si algo no funciona:${NC}"
echo ""
echo -e "${RED}1. Verificar logs:${NC}"
echo -e "   docker logs sicora-backend_apigateway_1"
echo -e "   docker logs sicora-backend_notification_1"
echo -e "   docker logs sicora-backend_postgres_1"
echo ""
echo -e "${RED}2. Verificar configuración:${NC}"
echo -e "   docker ps"
echo -e "   sudo nginx -t"
echo -e "   sudo systemctl status nginx"
echo ""
echo -e "${RED}3. Verificar variables de entorno:${NC}"
echo -e "   cat .env.production"
echo ""
echo -e "${RED}4. Reiniciar servicios:${NC}"
echo -e "   ./deployment/deploy.sh production"
echo -e "   sudo systemctl restart nginx"
echo ""

show_section "DOCUMENTACIÓN COMPLETA"

echo -e "${PURPLE}📚 Para más detalles, consulta:${NC}"
echo -e "   • _docs/desarrollo/GUIA_DESPLIEGUE_VPS_HOSTINGER.md"
echo -e "   • _docs/desarrollo/PLAN_DESPLIEGUE_VPS_RESUMEN.md"
echo ""
echo -e "${PURPLE}🔧 Comandos Make disponibles:${NC}"
echo -e "   • make deployment-help"
echo -e "   • make prepare-deployment"
echo -e "   • make validate-endpoints-remote DOMAIN=tu-servidor.com"
echo ""

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 ¡SICORA Backend estará listo para integración con frontend!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Tiempo estimado total: 40-50 minutos${NC}"
echo ""
