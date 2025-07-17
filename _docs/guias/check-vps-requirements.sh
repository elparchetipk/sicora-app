#!/bin/bash

# SICORA-APP - Script de Verificación de Requisitos para VPS Hostinger
# Ejecutar ANTES del despliegue para verificar que el servidor está listo

set -e

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
}

print_ok() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_fail() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Variables
MIN_RAM_MB=2048
MIN_DISK_GB=20
MIN_CPU_CORES=2

print_header "🔍 VERIFICACIÓN DE REQUISITOS SICORA-APP VPS"

echo ""
print_info "Verificando servidor VPS para despliegue de SICORA-APP EPTI OneVision..."
echo ""

# 1. Información del sistema
print_header "📋 INFORMACIÓN DEL SISTEMA"

OS_INFO=$(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)
KERNEL=$(uname -r)
ARCHITECTURE=$(uname -m)

echo "🖥️  Sistema Operativo: $OS_INFO"
echo "🔧 Kernel: $KERNEL"
echo "🏗️  Arquitectura: $ARCHITECTURE"

if [[ "$ARCHITECTURE" == "x86_64" ]]; then
    print_ok "Arquitectura compatible (x86_64)"
else
    print_warning "Arquitectura no probada: $ARCHITECTURE"
fi

# 2. Recursos del sistema
print_header "💾 RECURSOS DEL SISTEMA"

# RAM
TOTAL_RAM_MB=$(free -m | awk 'NR==2{printf "%.0f", $2}')
echo "🧠 RAM Total: ${TOTAL_RAM_MB}MB"

if [ $TOTAL_RAM_MB -ge $MIN_RAM_MB ]; then
    print_ok "RAM suficiente (mínimo: ${MIN_RAM_MB}MB)"
else
    print_fail "RAM insuficiente. Disponible: ${TOTAL_RAM_MB}MB, Mínimo: ${MIN_RAM_MB}MB"
fi

# CPU
CPU_CORES=$(nproc)
CPU_INFO=$(lscpu | grep "Model name:" | cut -d':' -f2 | xargs)
echo "⚡ CPU: $CPU_INFO"
echo "🔢 Cores: $CPU_CORES"

if [ $CPU_CORES -ge $MIN_CPU_CORES ]; then
    print_ok "CPU suficiente (mínimo: ${MIN_CPU_CORES} cores)"
else
    print_warning "Pocos cores de CPU. Disponible: $CPU_CORES, Recomendado: $MIN_CPU_CORES"
fi

# Disco
DISK_TOTAL_GB=$(df -BG / | awk 'NR==2 {print $2}' | sed 's/G//')
DISK_USED_GB=$(df -BG / | awk 'NR==2 {print $3}' | sed 's/G//')
DISK_AVAILABLE_GB=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
DISK_USAGE_PERCENT=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

echo "💿 Disco Total: ${DISK_TOTAL_GB}GB"
echo "📊 Disco Usado: ${DISK_USED_GB}GB (${DISK_USAGE_PERCENT}%)"
echo "📁 Disco Disponible: ${DISK_AVAILABLE_GB}GB"

if [ $DISK_AVAILABLE_GB -ge $MIN_DISK_GB ]; then
    print_ok "Espacio en disco suficiente (mínimo: ${MIN_DISK_GB}GB)"
else
    print_fail "Espacio insuficiente. Disponible: ${DISK_AVAILABLE_GB}GB, Mínimo: ${MIN_DISK_GB}GB"
fi

if [ $DISK_USAGE_PERCENT -gt 80 ]; then
    print_warning "Uso de disco alto: ${DISK_USAGE_PERCENT}%"
fi

# 3. Red y conectividad
print_header "🌐 CONECTIVIDAD"

# IP pública
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "No disponible")
echo "🌍 IP Pública: $PUBLIC_IP"

# Verificar conectividad a servicios importantes
services_to_check=(
    "google.com:80"
    "docker.com:443"
    "github.com:443"
    "registry.hub.docker.com:443"
)

for service in "${services_to_check[@]}"; do
    host=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if timeout 5 nc -z $host $port 2>/dev/null; then
        print_ok "Conectividad a $host:$port"
    else
        print_warning "No se pudo conectar a $host:$port"
    fi
done

# 4. Software requerido
print_header "🛠️  SOFTWARE REQUERIDO"

# Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    print_ok "Git instalado: v$GIT_VERSION"
else
    print_fail "Git no está instalado"
fi

# curl
if command -v curl &> /dev/null; then
    print_ok "curl instalado"
else
    print_fail "curl no está instalado"
fi

# Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | sed 's/,//')
    print_ok "Docker instalado: v$DOCKER_VERSION"
    
    # Verificar que Docker está corriendo
    if docker info &> /dev/null; then
        print_ok "Docker daemon está corriendo"
    else
        print_fail "Docker daemon no está corriendo"
    fi
else
    print_fail "Docker no está instalado"
fi

# Docker Compose
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version --short)
    print_ok "Docker Compose instalado: v$COMPOSE_VERSION"
else
    print_fail "Docker Compose no está instalado"
fi

# 5. Puertos requeridos
print_header "🔌 PUERTOS REQUERIDOS"

ports_to_check=(80 443 22)
blocked_ports=()

for port in "${ports_to_check[@]}"; do
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        print_warning "Puerto $port ya está en uso"
        blocked_ports+=($port)
    else
        print_ok "Puerto $port disponible"
    fi
done

# 6. Seguridad y firewall
print_header "🔒 SEGURIDAD"

# UFW
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(ufw status | head -1 | cut -d: -f2 | xargs)
    echo "🛡️  UFW: $UFW_STATUS"
    if [ "$UFW_STATUS" = "active" ]; then
        print_ok "UFW está activo"
    else
        print_warning "UFW no está activo"
    fi
else
    print_warning "UFW no está instalado"
fi

# SSH
if systemctl is-active --quiet ssh || systemctl is-active --quiet sshd; then
    print_ok "SSH está activo"
else
    print_warning "SSH no está activo"
fi

# 7. Requisitos de Hostinger VPS
print_header "🏢 ESPECÍFICO HOSTINGER VPS"

# Verificar que estamos en un VPS (no en local)
if [ -f /proc/vz/version ] || [ -d /proc/vz ]; then
    print_info "Detectado: OpenVZ/Virtuozzo container"
elif [ -d /proc/xen ]; then
    print_info "Detectado: Xen hypervisor"
elif grep -q "hypervisor" /proc/cpuinfo; then
    print_info "Detectado: Entorno virtualizado"
else
    print_warning "No se detectó virtualización (¿servidor físico?)"
fi

# Verificar acceso root
if [ "$EUID" -eq 0 ]; then
    print_ok "Ejecutándose como root"
else
    print_warning "No se está ejecutando como root (puede requerir sudo)"
fi

# 8. Recomendaciones finales
print_header "📝 RECOMENDACIONES"

recommendations=()

if [ $TOTAL_RAM_MB -lt 4096 ]; then
    recommendations+=("Considerar actualizar a 4GB+ RAM para mejor rendimiento")
fi

if [ $DISK_USAGE_PERCENT -gt 70 ]; then
    recommendations+=("Limpiar espacio en disco antes del despliegue")
fi

if [ ${#blocked_ports[@]} -gt 0 ]; then
    recommendations+=("Liberar puertos bloqueados: ${blocked_ports[*]}")
fi

if ! command -v docker &> /dev/null; then
    recommendations+=("Instalar Docker antes de continuar")
fi

if ! docker compose version &> /dev/null; then
    recommendations+=("Instalar Docker Compose antes de continuar")
fi

if [ ${#recommendations[@]} -eq 0 ]; then
    print_ok "¡Sistema listo para despliegue de SICORA-APP!"
else
    echo "Recomendaciones antes del despliegue:"
    for rec in "${recommendations[@]}"; do
        echo "  • $rec"
    done
fi

# 9. Comandos de instalación rápida
print_header "🚀 COMANDOS DE INSTALACIÓN RÁPIDA"

echo "Si faltan componentes, ejecuta:"
echo ""

if ! command -v docker &> /dev/null; then
    echo "# Instalar Docker:"
    echo "curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "sh get-docker.sh"
    echo ""
fi

if ! docker compose version &> /dev/null; then
    echo "# Instalar Docker Compose:"
    echo "mkdir -p ~/.docker/cli-plugins/"
    echo "curl -SL https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose"
    echo "chmod +x ~/.docker/cli-plugins/docker-compose"
    echo ""
fi

if ! command -v git &> /dev/null; then
    echo "# Instalar Git:"
    echo "apt update && apt install -y git curl"
    echo ""
fi

echo "# Crear directorio y descargar script de despliegue:"
echo "mkdir -p /opt/sicora-app"
echo "cd /opt/sicora-app"
echo "curl -o auto-deploy-sicora.sh https://raw.githubusercontent.com/tu-repo/sicora-app/main/_docs/guias/auto-deploy-sicora.sh"
echo "chmod +x auto-deploy-sicora.sh"
echo "./auto-deploy-sicora.sh deploy"

print_header "✅ VERIFICACIÓN COMPLETADA"

echo ""
print_info "Siguiente paso: Ejecutar el script de despliegue automático"
echo "curl -o auto-deploy-sicora.sh <URL-del-script>"
echo "chmod +x auto-deploy-sicora.sh"
echo "./auto-deploy-sicora.sh deploy"
