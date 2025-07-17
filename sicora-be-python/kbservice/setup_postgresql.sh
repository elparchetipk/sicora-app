#!/bin/bash

# 🐘 CONFIGURACIÓN DE POSTGRESQL CON PGVECTOR PARA KBSERVICE
# Script para configurar PostgreSQL con la extensión pgvector en Fedora

echo "🐘 Configurando PostgreSQL con pgvector para KbService..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# Verificar si el usuario quiere instalar PostgreSQL
read -p "¿Deseas instalar y configurar PostgreSQL con pgvector? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    warning "Instalación cancelada. Para usar SQLite, continúa con el desarrollo."
    exit 0
fi

# 1. Instalar PostgreSQL
info "Instalando PostgreSQL..."
sudo dnf install -y postgresql postgresql-server postgresql-contrib postgresql-devel

# 2. Inicializar base de datos
info "Inicializando base de datos PostgreSQL..."
sudo postgresql-setup --initdb

# 3. Iniciar y habilitar PostgreSQL
info "Iniciando PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 4. Verificar que PostgreSQL está corriendo
if ! sudo systemctl is-active --quiet postgresql; then
    error "PostgreSQL no se pudo iniciar correctamente"
    exit 1
fi
success "PostgreSQL está corriendo"

# 5. Instalar dependencias para pgvector
info "Instalando dependencias para pgvector..."
sudo dnf install -y git make gcc postgresql-devel

# 6. Clonar e instalar pgvector
info "Descargando e instalando pgvector..."
cd /tmp
git clone --branch v0.7.4 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install

# 7. Configurar usuario y base de datos
info "Configurando usuario y base de datos..."

# Crear usuario kbservice
sudo -u postgres createuser --interactive --pwprompt kbservice << EOF
n
n
n
EOF

# Crear base de datos
sudo -u postgres createdb kbservice_db -O kbservice

# 8. Configurar autenticación
info "Configurando autenticación PostgreSQL..."
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" /var/lib/pgsql/data/postgresql.conf

# Backup pg_hba.conf
sudo cp /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.backup

# Configurar autenticación md5 para usuario local
sudo bash -c 'cat >> /var/lib/pgsql/data/pg_hba.conf << EOF

# KbService configuration
local   kbservice_db    kbservice                               md5
host    kbservice_db    kbservice    127.0.0.1/32              md5
host    kbservice_db    kbservice    ::1/128                   md5
EOF'

# 9. Reiniciar PostgreSQL para aplicar cambios
info "Reiniciando PostgreSQL..."
sudo systemctl restart postgresql

# 10. Verificar instalación de pgvector
info "Verificando instalación de pgvector..."
sudo -u postgres psql -d kbservice_db -c "CREATE EXTENSION IF NOT EXISTS vector;" || {
    error "No se pudo habilitar la extensión pgvector"
    exit 1
}

success "pgvector instalado y habilitado correctamente"

# 11. Mostrar información de conexión
echo ""
success "🎉 Configuración completada!"
echo ""
info "Configuración de la base de datos:"
echo "  Host: localhost"
echo "  Puerto: 5432"
echo "  Base de datos: kbservice_db"
echo "  Usuario: kbservice"
echo "  Contraseña: [la que configuraste]"
echo ""
info "URL de conexión para .env:"
echo "DATABASE_URL=postgresql+asyncpg://kbservice:TU_PASSWORD@localhost:5432/kbservice_db"
echo ""
warning "IMPORTANTE:"
echo "1. Actualiza el archivo .env con la URL de conexión correcta"
echo "2. Ejecuta las migraciones: python -m alembic upgrade head"
echo "3. La extensión pgvector ya está habilitada en la base de datos"
echo ""

# 12. Verificar que todo funciona
info "Verificando conexión..."
sudo -u postgres psql -d kbservice_db -c "SELECT version();" && success "Conexión exitosa"

echo ""
info "¿Deseas crear un archivo .env con la configuración de PostgreSQL? (y/n)"
read -p "" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Ingresa la contraseña para el usuario kbservice: " -s DBPASS
    echo
    
    cat > .env.postgresql << EOF
# PostgreSQL Configuration for KbService
DATABASE_URL=postgresql+asyncpg://kbservice:${DBPASS}@localhost:5432/kbservice_db
DATABASE_ECHO=false

# Redis (opcional - para caché)
REDIS_URL=redis://localhost:6379

# OpenAI (opcional - para embeddings reales)
OPENAI_API_KEY=your-openai-api-key-here

# JWT Settings
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256

# Application Settings
APP_NAME=SICORA KbService
DEBUG=false
LOG_LEVEL=INFO

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
EOF
    
    success "Archivo .env.postgresql creado"
    info "Copia su contenido a .env o renómbralo: mv .env.postgresql .env"
fi

echo ""
success "🚀 PostgreSQL con pgvector está listo para KbService!"
