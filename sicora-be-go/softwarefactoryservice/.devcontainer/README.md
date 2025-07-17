# 🐳 **DESARROLLO CON DEVCONTAINERS - SOFTWAREFACTORYSERVICE**

Este documento explica cómo configurar y usar el entorno de desarrollo containerizado para el SoftwareFactoryService, optimizado para GitHub Codespaces y VS Code Dev Containers.

---

## 🚀 **CONFIGURACIÓN RÁPIDA**

### **1. Requisitos Previos**

- **Docker Desktop** instalado y funcionando
- **VS Code** con la extensión Dev Containers
- **Git** configurado

### **2. Setup Automático**

```bash
# Clonar el repositorio (si no está clonado)
git clone <repository-url>
cd sicora-app/sicora-be-go/softwarefactoryservice

# Ejecutar setup automático
./setup-dev.sh
```

### **3. Desarrollo en VS Code**

1. Abrir la carpeta en VS Code
2. Ejecutar comando: `Dev Containers: Reopen in Container`
3. Esperar a que el contenedor se configure
4. ¡Empezar a desarrollar!

---

## 🏗️ **ARQUITECTURA DEL ENTORNO**

### **Servicios Configurados**

```yaml
🏭 SoftwareFactory API (Go)     ➜ localhost:8080
🐘 PostgreSQL Database          ➜ localhost:5432
🔴 Redis Cache                  ➜ localhost:6379
🐍 Migration Service (Python)   ➜ (interno)
📊 PgAdmin (opcional)           ➜ localhost:5050
```

### **Volúmenes Persistentes**

- `go_mod_cache` - Cache de módulos Go
- `go_build_cache` - Cache de builds
- `postgres_dev_data` - Datos de PostgreSQL
- `redis_dev_data` - Datos de Redis

---

## 🛠️ **COMANDOS DE DESARROLLO**

### **Gestión del Entorno**

```bash
# Iniciar entorno completo
make docker-dev-up

# Parar entorno
make docker-dev-down

# Reiniciar entorno
make docker-dev-restart

# Reset completo (borra datos)
make docker-dev-reset

# Ver logs en tiempo real
make docker-dev-logs
```

### **Desarrollo Diario**

```bash
# Iniciar con hot reload
make dev-start

# Acceder al shell del contenedor
make dev-shell

# Ver logs del servicio
make dev-logs

# Generar documentación Swagger
make docs

# Ejecutar tests
make test

# Linting del código
make lint
```

### **Base de Datos**

```bash
# Acceder a PostgreSQL
make docker-dev-db-shell

# Acceder a Redis
make docker-dev-redis-shell

# Ejecutar migraciones
cd ../../../sicora-be-python/softwarefactoryservice
make migrate

# Aplicar índices optimizados
make apply-user-story-indexes
```

---

## 📁 **ESTRUCTURA DE ARCHIVOS DEV**

```
.devcontainer/
├── devcontainer.json           # Configuración VS Code Dev Container
├── docker-compose.dev.yml      # Docker Compose para desarrollo
└── README.md                   # Este archivo

# Archivos de configuración Docker
Dockerfile.dev                  # Dockerfile optimizado para desarrollo
.dockerignore                   # Archivos excluidos del build
.env.dev                        # Variables de entorno de desarrollo
.air.toml                       # Configuración de hot reload

# Scripts de utilidad
setup-dev.sh                    # Script de setup automático
```

---

## 🔧 **CONFIGURACIONES ESPECÍFICAS**

### **Hot Reload (Air)**

El entorno está configurado con Air para hot reload automático:

- **Archivos monitoreados**: `*.go`, `*.html`, `*.tmpl`
- **Exclusiones**: `*_test.go`, `vendor/`, `tmp/`
- **Comando de build**: `go build -o ./tmp/main ./cmd/server`
- **Puerto de debug**: `2345` (Delve)

### **Variables de Entorno de Desarrollo**

```bash
# Base de datos
DATABASE_URL=postgresql://softwarefactoryservice_user:dev_password@postgres:5432/sicora_db

# Redis
REDIS_URL=redis://:dev_redis_password@redis:6379

# Configuración del servicio
GO_ENV=development
GIN_MODE=debug
LOG_LEVEL=debug
```

### **Herramientas Pre-instaladas**

- **Go 1.23** con herramientas de desarrollo
- **Air** para hot reload
- **Swag** para documentación
- **GolangCI-Lint** para linting
- **Delve** para debugging
- **PostgreSQL Client** para acceso a DB
- **Redis Tools** para acceso a cache

---

## 🚀 **GITHUB CODESPACES**

### **Configuración Automática**

El entorno está optimizado para Codespaces:

1. **Auto-forward de puertos** configurado
2. **Extensiones VS Code** pre-instaladas
3. **Post-create commands** para setup automático
4. **Secrets** para variables de entorno

### **Puertos Expuestos**

- `8080` - API principal (auto-forward)
- `5432` - PostgreSQL (silencioso)
- `6379` - Redis (silencioso)
- `5050` - PgAdmin (opcional)
- `2345` - Debugger (manual)

### **Uso en Codespaces**

1. Abrir repositorio en GitHub
2. Presionar `.` o `Ctrl+Shift+P` → "Codespaces: Create"
3. Seleccionar configuración de máquina
4. Esperar setup automático (2-3 minutos)
5. ¡Empezar a desarrollar!

---

## 🔍 **DEBUGGING**

### **VS Code Debugging**

Configuración pre-establecida para debugging con Delve:

```json
{
  "name": "Debug SoftwareFactory API",
  "type": "go",
  "request": "launch",
  "mode": "debug",
  "program": "./cmd/server",
  "port": 2345,
  "host": "0.0.0.0"
}
```

### **Debugging Remoto**

```bash
# Iniciar con debugger
dlv debug ./cmd/server --headless --listen=:2345 --api-version=2

# Conectar desde VS Code
# Puerto: 2345
# Host: localhost
```

---

## 📊 **MONITOREO Y LOGS**

### **Logs Estructurados**

```bash
# Logs del API en tiempo real
docker-compose -f .devcontainer/docker-compose.dev.yml logs -f softwarefactory-service

# Logs de base de datos
docker-compose -f .devcontainer/docker-compose.dev.yml logs -f postgres

# Logs de migraciones
docker-compose -f .devcontainer/docker-compose.dev.yml logs migration-service
```

### **Health Checks**

- **API**: `GET http://localhost:8080/health`
- **Swagger**: `http://localhost:8080/swagger/index.html`
- **Base de datos**: Incluido en docker-compose

---

## 🚨 **TROUBLESHOOTING**

### **Problemas Comunes**

#### **El contenedor no inicia**

```bash
# Verificar Docker
docker ps
docker-compose -f .devcontainer/docker-compose.dev.yml ps

# Revisar logs
docker-compose -f .devcontainer/docker-compose.dev.yml logs
```

#### **Base de datos no conecta**

```bash
# Verificar estado de PostgreSQL
docker-compose -f .devcontainer/docker-compose.dev.yml exec postgres pg_isready -U postgres

# Ejecutar migraciones manualmente
cd ../../../sicora-be-python/softwarefactoryservice
make migrate
```

#### **Hot reload no funciona**

```bash
# Verificar Air
docker-compose -f .devcontainer/docker-compose.dev.yml exec softwarefactory-service which air

# Reiniciar con logs
make dev-restart
make dev-logs
```

#### **Reset completo**

```bash
# Parar todo y limpiar
./setup-dev.sh clean

# Iniciar de nuevo
./setup-dev.sh
```

### **Performance**

#### **Optimizar velocidad de build**

- Usar volúmenes para cache de Go modules
- No incluir archivos innecesarios (`.dockerignore`)
- Usar multi-stage builds en producción

#### **Reducir uso de memoria**

```bash
# Limitar recursos en docker-compose.dev.yml
resources:
  limits:
    memory: 512M
    cpus: '0.5'
```

---

## 📚 **RECURSOS ADICIONALES**

- **[Documentación oficial Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)**
- **[GitHub Codespaces Docs](https://docs.github.com/en/codespaces)**
- **[Air Documentation](https://github.com/cosmtrek/air)**
- **[Go in VS Code](https://code.visualstudio.com/docs/languages/go)**

---

## ✅ **CHECKLIST DE SETUP**

- [ ] Docker Desktop instalado y funcionando
- [ ] VS Code con extensión Dev Containers
- [ ] Repositorio clonado localmente
- [ ] Script `setup-dev.sh` ejecutado exitosamente
- [ ] Contenedor abierto en VS Code
- [ ] API respondiendo en `localhost:8080`
- [ ] Swagger accesible en `localhost:8080/swagger/index.html`
- [ ] Hot reload funcionando al editar archivos `.go`
- [ ] Base de datos conectada y migraciones aplicadas

---

**¡Listo para desarrollar! 🚀**
