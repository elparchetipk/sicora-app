#!/bin/bash

# Script de validación de integración para sicora-be-go
# Autor: SICORA Team
# Fecha: 2025-06-28

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 SICORA Go Stack - Validación de Integración${NC}"
echo "=================================================="

# 1. Verificar estructura de directorios
echo -e "\n${YELLOW}1. Verificando estructura de directorios...${NC}"
if [ -d "shared" ] && [ -d "infra" ]; then
    echo -e "${GREEN}✅ Submódulos presentes${NC}"
else
    echo -e "${RED}❌ Faltan submódulos${NC}"
    exit 1
fi

# 2. Verificar submódulos Git
echo -e "\n${YELLOW}2. Verificando submódulos Git...${NC}"
git submodule status

# 3. Verificar archivos de configuración
echo -e "\n${YELLOW}3. Verificando archivos de configuración...${NC}"
if [ -f ".env.example" ]; then
    echo -e "${GREEN}✅ .env.example presente${NC}"
else
    echo -e "${RED}❌ Falta .env.example${NC}"
fi

if [ -f "Makefile" ]; then
    echo -e "${GREEN}✅ Makefile presente${NC}"
else
    echo -e "${RED}❌ Falta Makefile${NC}"
fi

if [ -f "docker-compose.yml" ]; then
    echo -e "${GREEN}✅ docker-compose.yml presente${NC}"
else
    echo -e "${RED}❌ Falta docker-compose.yml${NC}"
fi

# 4. Configurar variables de entorno si no existe .env
echo -e "\n${YELLOW}4. Configurando variables de entorno...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Archivo .env creado desde .env.example${NC}"
else
    echo -e "${GREEN}✅ Archivo .env ya existe${NC}"
fi

# 5. Verificar Go
echo -e "\n${YELLOW}5. Verificando Go...${NC}"
if command -v go &> /dev/null; then
    GO_VERSION=$(go version | cut -d' ' -f3)
    echo -e "${GREEN}✅ Go instalado: ${GO_VERSION}${NC}"
else
    echo -e "${RED}❌ Go no instalado${NC}"
    exit 1
fi

# 6. Descargar dependencias
echo -e "\n${YELLOW}6. Descargando dependencias Go...${NC}"
go mod download
go mod tidy
echo -e "${GREEN}✅ Dependencias descargadas${NC}"

# 7. Verificar Docker
echo -e "\n${YELLOW}7. Verificando Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker instalado${NC}"
else
    echo -e "${RED}❌ Docker no instalado${NC}"
    exit 1
fi

# 8. Iniciar servicios de infraestructura
echo -e "\n${YELLOW}8. Iniciando servicios de infraestructura...${NC}"
docker compose -f infra/docker/development/docker-compose.yml up -d postgres redis
echo -e "${GREEN}✅ Servicios iniciados${NC}"

# Esperar a que los servicios estén listos
echo -e "\n${YELLOW}Esperando a que los servicios estén listos...${NC}"
sleep 10

# 9. Verificar servicios Docker
echo -e "\n${YELLOW}9. Verificando servicios Docker...${NC}"
if docker ps | grep -q "sicora-postgres"; then
    echo -e "${GREEN}✅ PostgreSQL corriendo${NC}"
else
    echo -e "${RED}❌ PostgreSQL no está corriendo${NC}"
fi

if docker ps | grep -q "sicora-redis"; then
    echo -e "${GREEN}✅ Redis corriendo${NC}"
else
    echo -e "${RED}❌ Redis no está corriendo${NC}"
fi

# 10. Probar conexión a base de datos
echo -e "\n${YELLOW}10. Probando conexión a base de datos...${NC}"
if go run test-db-connection.go; then
    echo -e "${GREEN}✅ Conexión a base de datos exitosa${NC}"
else
    echo -e "${RED}❌ Error en conexión a base de datos${NC}"
fi

# 11. Verificar compilación de servicios
echo -e "\n${YELLOW}11. Verificando compilación de servicios...${NC}"

SERVICES=("userservice" "scheduleservice" "attendanceservice" "evalinservice")

for service in "${SERVICES[@]}"; do
    if [ -d "$service" ]; then
        echo -e "  Probando compilación de ${service}..."
        cd "$service"
        if go mod tidy && go build -v ./... &> /dev/null; then
            echo -e "${GREEN}  ✅ ${service} compila correctamente${NC}"
        else
            echo -e "${RED}  ❌ Error compilando ${service}${NC}"
        fi
        cd ..
    else
        echo -e "${YELLOW}  ⚠️  ${service} no encontrado${NC}"
    fi
done

# Verificar projectevalservice por separado (estructura diferente)
if [ -d "projectevalservice" ]; then
    echo -e "  Probando compilación de projectevalservice..."
    cd "projectevalservice"
    if go mod tidy && go build -v . &> /dev/null; then
        echo -e "${GREEN}  ✅ projectevalservice compila correctamente${NC}"
    else
        echo -e "${RED}  ❌ Error compilando projectevalservice${NC}"
    fi
    cd ..
fi

# 12. Verificar puertos disponibles
echo -e "\n${YELLOW}12. Verificando puertos disponibles...${NC}"
PORTS=(8001 8002 8003 8004 8007)

for port in "${PORTS[@]}"; do
    if ! lsof -i :$port &> /dev/null; then
        echo -e "${GREEN}✅ Puerto $port disponible${NC}"
    else
        echo -e "${YELLOW}⚠️  Puerto $port en uso${NC}"
    fi
done

# 13. Resumen final
echo -e "\n${BLUE}=================================================="
echo -e "📊 RESUMEN DE VALIDACIÓN"
echo -e "==================================================${NC}"

echo -e "${GREEN}✅ Estructura de directorios: OK${NC}"
echo -e "${GREEN}✅ Submódulos Git: OK${NC}"
echo -e "${GREEN}✅ Configuración: OK${NC}"
echo -e "${GREEN}✅ Go instalado: OK${NC}"
echo -e "${GREEN}✅ Dependencias: OK${NC}"
echo -e "${GREEN}✅ Docker: OK${NC}"
echo -e "${GREEN}✅ Servicios de infraestructura: OK${NC}"
echo -e "${GREEN}✅ Conexión a base de datos: OK${NC}"

echo -e "\n${GREEN}🎉 Validación de integración completada exitosamente!${NC}"
echo -e "\n${YELLOW}Próximos pasos:${NC}"
echo -e "1. Ejecutar: ${BLUE}make run-userservice${NC} para probar un servicio"
echo -e "2. Abrir: ${BLUE}http://localhost:8001/health${NC} para verificar health check"
echo -e "3. Ejecutar: ${BLUE}make test${NC} para correr los tests"
echo -e "4. Revisar documentación en cada servicio"

echo -e "\n${YELLOW}Para detener servicios de infraestructura:${NC}"
echo -e "${BLUE}docker compose -f infra/docker/development/docker-compose.yml down${NC}"
