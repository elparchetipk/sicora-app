#!/bin/bash

# SICORA-APP EPTI OneVision - Script de Despliegue Automático para Hostinger VPS
# Versión: 1.0
# Fecha: 4 de julio de 2025

set -e

# Configuración de colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuración de logging
LOG_FILE="/var/log/sicora-deployment.log"
touch $LOG_FILE

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  $1${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
    log "SUCCESS: $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    log "WARNING: $1"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    log "ERROR: $1"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
    log "INFO: $1"
}

# Variables de configuración
SICORA_DIR="/opt/sicora-app"
BACKUP_DIR="$SICORA_DIR/backup"
LOG_DIR="$SICORA_DIR/logs"

# Función para verificar requisitos
check_requirements() {
    print_header "🔍 VERIFICANDO REQUISITOS DEL SISTEMA"
    
    # Verificar Docker
    if command -v docker &> /dev/null; then
        print_status "Docker instalado: $(docker --version)"
    else
        print_error "Docker no está instalado"
        exit 1
    fi
    
    # Verificar Docker Compose
    if docker compose version &> /dev/null; then
        print_status "Docker Compose instalado: $(docker compose version --short)"
    else
        print_error "Docker Compose no está instalado"
        exit 1
    fi
    
    # Verificar espacio en disco
    available_space=$(df / | awk 'NR==2 {print $4}')
    if [ $available_space -gt 10485760 ]; then  # 10GB en KB
        print_status "Espacio en disco suficiente: $(df -h / | awk 'NR==2 {print $4}') disponible"
    else
        print_warning "Poco espacio en disco: $(df -h / | awk 'NR==2 {print $4}') disponible"
    fi
    
    # Verificar memoria
    total_mem=$(free -m | awk 'NR==2{print $2}')
    if [ $total_mem -gt 2048 ]; then
        print_status "Memoria suficiente: ${total_mem}MB RAM"
    else
        print_warning "Poca memoria RAM: ${total_mem}MB (recomendado: >2GB)"
    fi
}

# Función para configurar el entorno
setup_environment() {
    print_header "🏗️ CONFIGURANDO ENTORNO"
    
    # Crear directorios necesarios
    mkdir -p $SICORA_DIR/{database/init,logs,backup,certs,config,monitoring/{prometheus,grafana},nginx/{conf.d,ssl}}
    mkdir -p $SICORA_DIR/production/{frontend,backend-go,backend-python}
    mkdir -p $SICORA_DIR/scripts
    
    print_status "Estructura de directorios creada"
    
    # Crear red Docker
    docker network create sicora_network 2>/dev/null || print_status "Red Docker ya existe"
    
    # Configurar permisos
    chown -R $USER:$USER $SICORA_DIR
    chmod +x $SICORA_DIR/scripts/*.sh 2>/dev/null || true
    
    print_status "Permisos configurados"
}

# Función para configurar variables de entorno
setup_env_vars() {
    print_header "⚙️ CONFIGURANDO VARIABLES DE ENTORNO"
    
    if [ ! -f "$SICORA_DIR/.env" ]; then
        print_info "Creando archivo de variables de entorno..."
        
        # Generar passwords seguros
        POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        REDIS_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        JWT_SECRET=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-50)
        SECRET_KEY=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        
        cat > $SICORA_DIR/.env << EOF
# SICORA-APP Producción - Variables de Entorno
# Generado automáticamente el $(date)

# Base de Datos PostgreSQL
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=sicora_prod
POSTGRES_USER=sicora_prod_user
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_PASSWORD=$REDIS_PASSWORD
REDIS_HOST=redis
REDIS_PORT=6379

# Seguridad
JWT_SECRET=$JWT_SECRET
SECRET_KEY=$SECRET_KEY

# Aplicación
ENV=production
LOG_LEVEL=INFO

# Dominio (CAMBIAR POR TU DOMINIO)
DOMAIN=tu-dominio.com
API_URL=https://tu-dominio.com/api

# Monitoreo
GRAFANA_PASSWORD=admin123
PROMETHEUS_RETENTION=15d
EOF
        
        print_status "Variables de entorno generadas"
        print_warning "⚠️  IMPORTANTE: Cambiar DOMAIN en $SICORA_DIR/.env por tu dominio real"
        print_warning "⚠️  IMPORTANTE: Guardar las contraseñas generadas en lugar seguro"
    else
        print_status "Archivo .env ya existe"
    fi
}

# Función para descargar/preparar código fuente
prepare_source_code() {
    print_header "📥 PREPARANDO CÓDIGO FUENTE"
    
    print_info "Por favor, asegúrate de que el código fuente esté disponible en:"
    print_info "- $SICORA_DIR/production/backend-go/ (código del backend Go)"
    print_info "- $SICORA_DIR/production/backend-python/aiservice/ (código del AIService)"
    print_info "- $SICORA_DIR/production/frontend/ (código del frontend React)"
    
    echo ""
    echo -e "${YELLOW}¿Está el código fuente ya disponible en las ubicaciones correctas? [y/N]${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Código fuente confirmado"
    else
        print_info "Manual: Copiar el código fuente a las ubicaciones especificadas"
        print_info "Ejemplo con Git:"
        echo "  cd $SICORA_DIR/production/backend-go && git clone <tu-repo-go> ."
        echo "  cd $SICORA_DIR/production/backend-python && git clone <tu-repo-python> ."
        echo "  cd $SICORA_DIR/production/frontend && git clone <tu-repo-frontend> ."
        echo ""
        print_info "¿Continuar después de copiar el código? [y/N]"
        read -r response2
        if [[ ! "$response2" =~ ^[Yy]$ ]]; then
            print_error "Despliegue cancelado. Preparar código fuente primero."
            exit 1
        fi
    fi
}

# Función para crear configuraciones de Docker Compose
create_docker_configs() {
    print_header "🐳 CREANDO CONFIGURACIONES DOCKER"
    
    # Docker Compose principal
    cat > $SICORA_DIR/docker-compose.yml << 'EOF'
version: '3.9'

services:
  # Base de datos PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: sicora_postgres_prod
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8"
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
      - ./logs/postgres:/var/log/postgresql
    networks:
      - sicora_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    container_name: sicora_redis_prod
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD} --appendonly yes
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - sicora_network
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Servicios Go
  userservice-go:
    build:
      context: ./production/backend-go/userservice
      dockerfile: Dockerfile
    container_name: sicora_userservice_go_prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - JWT_SECRET=${JWT_SECRET}
      - PORT=8001
      - ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - sicora_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  scheduleservice-go:
    build:
      context: ./production/backend-go/scheduleservice
      dockerfile: Dockerfile
    container_name: sicora_scheduleservice_go_prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - PORT=8002
      - ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - sicora_network

  attendanceservice-go:
    build:
      context: ./production/backend-go/attendanceservice
      dockerfile: Dockerfile
    container_name: sicora_attendanceservice_go_prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - PORT=8003
      - ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - sicora_network

  evalinservice-go:
    build:
      context: ./production/backend-go/evalinservice
      dockerfile: Dockerfile
    container_name: sicora_evalinservice_go_prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - PORT=8004
      - ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - sicora_network

  kbservice-go:
    build:
      context: ./production/backend-go/kbservice
      dockerfile: Dockerfile
    container_name: sicora_kbservice_go_prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - PORT=8005
      - ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - sicora_network

  projectevalservice-go:
    build:
      context: ./production/backend-go/projectevalservice
      dockerfile: Dockerfile
    container_name: sicora_projectevalservice_go_prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - PORT=8007
      - ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - sicora_network

  # AIService Python
  aiservice:
    build:
      context: ./production/backend-python/aiservice
      dockerfile: Dockerfile
    container_name: sicora_aiservice_prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - SECRET_KEY=${SECRET_KEY}
      - ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - sicora_network

  # Nginx
  nginx:
    image: nginx:alpine
    container_name: sicora_nginx_prod
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./certs:/etc/nginx/certs:ro
      - frontend_dist:/var/www/sicora-frontend:ro
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - userservice-go
      - scheduleservice-go
      - attendanceservice-go
      - evalinservice-go
      - kbservice-go
      - projectevalservice-go
      - aiservice
    networks:
      - sicora_network

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  frontend_dist:
    driver: local

networks:
  sicora_network:
    driver: bridge
EOF

    print_status "Archivo docker-compose.yml creado"
    
    # Crear configuración básica de Nginx
    create_nginx_config
    
    # Crear script de inicialización de base de datos
    create_database_init
}

create_nginx_config() {
    # Nginx principal
    cat > $SICORA_DIR/nginx/nginx.conf << 'EOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log notice;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    gzip on;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    include /etc/nginx/conf.d/*.conf;
}
EOF

    # Configuración del sitio
    cat > $SICORA_DIR/nginx/conf.d/sicora.conf << 'EOF'
# Upstream para servicios Go
upstream userservice {
    server userservice-go:8001;
}

upstream scheduleservice {
    server scheduleservice-go:8002;
}

upstream attendanceservice {
    server attendanceservice-go:8003;
}

upstream evalinservice {
    server evalinservice-go:8004;
}

upstream kbservice {
    server kbservice-go:8005;
}

upstream projectevalservice {
    server projectevalservice-go:8007;
}

upstream aiservice {
    server aiservice:8004;
}

server {
    listen 80;
    server_name _;

    # Headers de seguridad
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Servir frontend estático
    location / {
        root /var/www/sicora-frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API Routes
    location /api/users/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://userservice/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/schedules/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://scheduleservice/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/attendance/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://attendanceservice/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/evaluations/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://evalinservice/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/knowledge/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://kbservice/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/projects/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://projectevalservice/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ai/ {
        limit_req zone=api burst=10 nodelay;
        proxy_pass http://aiservice/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Archivos estáticos con caché
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        root /var/www/sicora-frontend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    print_status "Configuración de Nginx creada"
}

create_database_init() {
    cat > $SICORA_DIR/database/init/01-init-sicora.sql << 'EOF'
-- Crear base de datos principal
CREATE DATABASE sicora_prod;

-- Crear usuario específico para producción
CREATE USER sicora_prod_user WITH ENCRYPTED PASSWORD 'POSTGRES_PASSWORD_PLACEHOLDER';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE sicora_prod TO sicora_prod_user;

-- Conectar a la base de datos
\c sicora_prod

-- Crear esquemas para microservicios
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS schedules;
CREATE SCHEMA IF NOT EXISTS attendance;
CREATE SCHEMA IF NOT EXISTS evaluations;
CREATE SCHEMA IF NOT EXISTS knowledge_base;
CREATE SCHEMA IF NOT EXISTS ai_service;
CREATE SCHEMA IF NOT EXISTS projects;

-- Otorgar permisos en esquemas
GRANT ALL ON SCHEMA users TO sicora_prod_user;
GRANT ALL ON SCHEMA schedules TO sicora_prod_user;
GRANT ALL ON SCHEMA attendance TO sicora_prod_user;
GRANT ALL ON SCHEMA evaluations TO sicora_prod_user;
GRANT ALL ON SCHEMA knowledge_base TO sicora_prod_user;
GRANT ALL ON SCHEMA ai_service TO sicora_prod_user;
GRANT ALL ON SCHEMA projects TO sicora_prod_user;

-- Configurar permisos por defecto
ALTER DEFAULT PRIVILEGES IN SCHEMA users GRANT ALL ON TABLES TO sicora_prod_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA schedules GRANT ALL ON TABLES TO sicora_prod_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA attendance GRANT ALL ON TABLES TO sicora_prod_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA evaluations GRANT ALL ON TABLES TO sicora_prod_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA knowledge_base GRANT ALL ON TABLES TO sicora_prod_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ai_service GRANT ALL ON TABLES TO sicora_prod_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA projects GRANT ALL ON TABLES TO sicora_prod_user;
EOF

    print_status "Script de inicialización de base de datos creado"
}

# Función para construir frontend
build_frontend() {
    print_header "🎨 CONSTRUYENDO FRONTEND EPTI ONEVISION"
    
    if [ ! -d "$SICORA_DIR/production/frontend" ]; then
        print_error "Directorio del frontend no encontrado: $SICORA_DIR/production/frontend"
        exit 1
    fi
    
    # Crear configuración de build del frontend
    cat > $SICORA_DIR/docker-compose.frontend-build.yml << 'EOF'
version: '3.9'

services:
  frontend-builder:
    image: node:18-alpine
    container_name: sicora_frontend_builder
    working_dir: /app
    volumes:
      - ./production/frontend:/app
      - frontend_dist:/app/dist
    environment:
      - NODE_ENV=production
    command: >
      sh -c "
        echo 'Instalando dependencias...' &&
        npm install -g pnpm &&
        pnpm install &&
        echo 'Configurando ambiente EPTI OneVision...' &&
        if [ -f .env.hostinger ]; then
          cp .env.hostinger .env
        else
          echo 'VITE_BUILD_TARGET=hostinger' > .env
          echo 'VITE_BRAND_CONFIG=epti' >> .env
          echo 'VITE_API_URL=http://localhost/api' >> .env
        fi &&
        echo 'Construyendo para producción...' &&
        if npm run | grep -q 'build:hostinger'; then
          pnpm build:hostinger
        else
          pnpm build
        fi &&
        echo 'Copiando archivos al volumen...' &&
        cp -r dist/* /app/dist/ &&
        echo 'Build completado!'
      "

volumes:
  frontend_dist:
    driver: local
EOF
    
    print_info "Construyendo frontend..."
    docker compose -f $SICORA_DIR/docker-compose.frontend-build.yml run --rm frontend-builder
    
    if [ $? -eq 0 ]; then
        print_status "Frontend construido exitosamente"
    else
        print_error "Error al construir frontend"
        exit 1
    fi
}

# Función para ejecutar despliegue
deploy_application() {
    print_header "🚀 DESPLEGANDO APLICACIÓN"
    
    cd $SICORA_DIR
    
    # Detener servicios existentes
    print_info "Deteniendo servicios existentes..."
    docker compose down --remove-orphans 2>/dev/null || true
    
    # Construir imágenes
    print_info "Construyendo imágenes Docker..."
    docker compose build --parallel
    
    # Iniciar servicios de base de datos primero
    print_info "Iniciando servicios de base de datos..."
    docker compose up -d postgres redis
    
    # Esperar a que estén listos
    print_info "Esperando a que PostgreSQL esté listo..."
    timeout=60
    counter=0
    until docker exec sicora_postgres_prod pg_isready -U sicora_prod_user -d sicora_prod >/dev/null 2>&1; do
        sleep 2
        counter=$((counter + 2))
        if [ $counter -ge $timeout ]; then
            print_error "Timeout esperando PostgreSQL"
            exit 1
        fi
    done
    print_status "PostgreSQL listo"
    
    print_info "Esperando a que Redis esté listo..."
    counter=0
    until docker exec sicora_redis_prod redis-cli -a "$(grep REDIS_PASSWORD $SICORA_DIR/.env | cut -d= -f2)" ping >/dev/null 2>&1; do
        sleep 2
        counter=$((counter + 2))
        if [ $counter -ge $timeout ]; then
            print_error "Timeout esperando Redis"
            exit 1
        fi
    done
    print_status "Redis listo"
    
    # Iniciar servicios backend
    print_info "Iniciando servicios backend..."
    docker compose up -d \
        userservice-go \
        scheduleservice-go \
        attendanceservice-go \
        evalinservice-go \
        kbservice-go \
        projectevalservice-go \
        aiservice
    
    # Esperar a que los servicios estén listos
    print_info "Esperando a que los servicios backend estén listos..."
    sleep 30
    
    # Iniciar Nginx
    print_info "Iniciando Nginx..."
    docker compose up -d nginx
    
    print_status "Despliegue completado"
}

# Función para verificar despliegue
verify_deployment() {
    print_header "🔍 VERIFICANDO DESPLIEGUE"
    
    # Verificar contenedores
    print_info "Estado de contenedores:"
    docker compose ps
    
    # Verificar servicios
    services=(
        "userservice-go:8001"
        "scheduleservice-go:8002"
        "attendanceservice-go:8003"
        "evalinservice-go:8004"
        "kbservice-go:8005"
        "projectevalservice-go:8007"
    )
    
    healthy_services=0
    total_services=${#services[@]}
    
    for service in "${services[@]}"; do
        name=$(echo $service | cut -d: -f1)
        port=$(echo $service | cut -d: -f2)
        
        if timeout 10 docker exec $name curl -f -s http://localhost:$port/health >/dev/null 2>&1; then
            print_status "$name está saludable"
            healthy_services=$((healthy_services + 1))
        else
            print_warning "$name no responde en health check"
        fi
    done
    
    # Verificar frontend
    if curl -f -s http://localhost/ >/dev/null 2>&1; then
        print_status "Frontend accesible"
    else
        print_warning "Frontend no accesible"
    fi
    
    # Resumen
    echo ""
    print_header "📊 RESUMEN DEL DESPLIEGUE"
    echo "✅ Servicios saludables: $healthy_services/$total_services"
    echo "🌐 Frontend: $(curl -s -o /dev/null -w "%{http_code}" http://localhost/)"
    echo "🗄️  PostgreSQL: $(docker exec sicora_postgres_prod pg_isready -U sicora_prod_user -d sicora_prod >/dev/null 2>&1 && echo "OK" || echo "FAIL")"
    echo "🔴 Redis: $(docker exec sicora_redis_prod redis-cli -a "$(grep REDIS_PASSWORD $SICORA_DIR/.env | cut -d= -f2)" ping 2>/dev/null | tr -d '\r')"
    
    if [ $healthy_services -eq $total_services ]; then
        print_status "🎉 DESPLIEGUE EXITOSO - Todos los servicios están corriendo"
        echo ""
        echo "🌐 Acceso a la aplicación:"
        echo "   Frontend: http://$(curl -s ifconfig.me)"
        echo "   API: http://$(curl -s ifconfig.me)/api"
        echo ""
        echo "🔧 Comandos útiles:"
        echo "   Ver logs: docker compose logs -f [servicio]"
        echo "   Reiniciar: docker compose restart [servicio]"
        echo "   Estado: docker compose ps"
    else
        print_error "DESPLIEGUE INCOMPLETO - Algunos servicios no están funcionando"
        echo ""
        echo "🔍 Para diagnosticar:"
        echo "   docker compose ps"
        echo "   docker compose logs [servicio-fallido]"
    fi
}

# Función para mostrar información post-despliegue
show_post_deployment_info() {
    print_header "📋 INFORMACIÓN POST-DESPLIEGUE"
    
    echo -e "${CYAN}🔐 Credenciales generadas:${NC}"
    echo "   PostgreSQL: sicora_prod_user / [ver en $SICORA_DIR/.env]"
    echo "   Redis: [ver REDIS_PASSWORD en $SICORA_DIR/.env]"
    echo ""
    
    echo -e "${CYAN}📁 Directorios importantes:${NC}"
    echo "   Aplicación: $SICORA_DIR"
    echo "   Logs: $SICORA_DIR/logs"
    echo "   Backup: $SICORA_DIR/backup"
    echo "   Configuración: $SICORA_DIR/.env"
    echo ""
    
    echo -e "${CYAN}🛠️  Scripts útiles:${NC}"
    echo "   Estado: docker compose ps"
    echo "   Logs: docker compose logs -f [servicio]"
    echo "   Reiniciar: docker compose restart"
    echo "   Parar: docker compose down"
    echo ""
    
    echo -e "${CYAN}⚠️  Tareas pendientes:${NC}"
    echo "   1. Cambiar DOMAIN en $SICORA_DIR/.env por tu dominio real"
    echo "   2. Configurar SSL/TLS para HTTPS"
    echo "   3. Configurar backup automático"
    echo "   4. Configurar monitoreo"
    echo "   5. Configurar firewall del VPS"
    echo ""
    
    echo -e "${YELLOW}📚 Documentación completa disponible en:${NC}"
    echo "   _docs/guias/DESPLIEGUE_HOSTINGER_VPS_PRODUCCION.md"
}

# Función principal
main() {
    print_header "🚀 SICORA-APP EPTI ONEVISION - DESPLIEGUE AUTOMÁTICO"
    echo -e "${CYAN}Iniciando despliegue en VPS Hostinger...${NC}"
    echo ""
    
    # Verificar que se está ejecutando como root
    if [ "$EUID" -ne 0 ]; then
        print_error "Este script debe ejecutarse como root (sudo)"
        exit 1
    fi
    
    # Verificar argumentos
    case "${1:-deploy}" in
        "check")
            check_requirements
            ;;
        "setup")
            check_requirements
            setup_environment
            setup_env_vars
            create_docker_configs
            print_status "Setup completado"
            ;;
        "build")
            cd $SICORA_DIR
            build_frontend
            ;;
        "deploy")
            check_requirements
            setup_environment
            setup_env_vars
            prepare_source_code
            create_docker_configs
            build_frontend
            deploy_application
            verify_deployment
            show_post_deployment_info
            ;;
        "verify")
            cd $SICORA_DIR
            verify_deployment
            ;;
        *)
            echo "Uso: $0 [check|setup|build|deploy|verify]"
            echo ""
            echo "Comandos:"
            echo "  check   - Verificar requisitos del sistema"
            echo "  setup   - Configurar entorno (sin desplegar)"
            echo "  build   - Construir solo el frontend"
            echo "  deploy  - Despliegue completo (por defecto)"
            echo "  verify  - Verificar despliegue existente"
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
