<div align="center">

![SICORA Logo](../../assets/logo-sicora-small.svg)

</div>

# 🚨 Errores de Red Comunes en Docker - SICORA

## 📋 Resumen Ejecutivo

Este documento identifica y proporciona soluciones para los errores de red más comunes que ocurren al ejecutar la infraestructura Docker del proyecto SICORA. Incluye diagnósticos automatizados y comandos de resolución.

---

## 🔍 Errores de Red Identificados

### 1. Conflictos de Puerto

#### Error Típico:

```
Error response from daemon: Ports are not available: listen tcp 0.0.0.0:5432: bind: address already in use
```

#### Diagnóstico:

```bash
# Verificar puertos ocupados
netstat -tulpn | grep -E "(5432|5433|27017|6379|3000|8080)"

# Verificar procesos específicos
lsof -i :5432
lsof -i :27017
```

#### Solución:

```bash
# Cambiar puerto en docker-compose.yml
# PostgreSQL: 5432 → 5433
# MongoDB: 27017 (mantener si no hay conflicto)
# Redis: 6379 (mantener si no hay conflicto)

# O detener servicios locales conflictivos
sudo systemctl stop postgresql
sudo systemctl stop redis-server
```

### 2. Problemas de Conectividad Entre Contenedores

#### Error Típico:

```
connection refused to hostname "mongodb"
dial tcp: lookup postgres on 127.0.0.11:53: no such host
```

#### Diagnóstico:

```bash
# Verificar redes Docker
docker network ls | grep sicora

# Inspeccionar red específica
docker network inspect sicora-network

# Verificar contenedores en la red
docker network inspect docker_sicora_network --format "{{json .Containers}}" | jq
```

#### Solución:

```bash
# 1. Asegurar que todos los servicios estén en la misma red
# En docker-compose.yml:
networks:
  default:
    external:
      name: sicora-network

# 2. Usar nombres de servicio correctos en la configuración
# Ejemplo: mongodb (no localhost:27017)
```

### 3. Errores de Resolución DNS

#### Error Típico:

```
getaddrinfo: Name or service not known
temporary failure in name resolution
```

#### Diagnóstico:

```bash
# Probar DNS desde dentro del contenedor
docker exec -it sicora_mongodb nslookup postgres
docker exec -it sicora_postgres nslookup mongodb

# Verificar configuración de red
docker exec -it sicora_mongodb cat /etc/resolv.conf
```

#### Solución:

```bash
# 1. Reiniciar servicios Docker
docker compose down
docker compose up -d

# 2. Recrear red si es necesario
docker network rm sicora-network
docker network create sicora-network
```

### 4. Problemas de Acceso desde Host

#### Error Típico:

```
Connection refused to localhost:27017
ECONNREFUSED 127.0.0.1:5433
```

#### Diagnóstico:

```bash
# Verificar mapeo de puertos
docker compose ps
docker port sicora_mongodb
docker port sicora_postgres

# Probar conectividad
telnet localhost 27017
telnet localhost 5433
```

#### Solución:

```bash
# Verificar configuración de puertos en docker-compose.yml
ports:
  - "27017:27017"  # MongoDB
  - "5433:5432"    # PostgreSQL
  - "6379:6379"    # Redis
```

### 5. Errores de Firewall/Iptables

#### Error Típico:

```
iptables: Operation not permitted
cannot access docker daemon socket
```

#### Diagnóstico:

```bash
# Verificar estado del firewall
sudo ufw status
sudo iptables -L DOCKER-USER

# Verificar daemon Docker
sudo systemctl status docker
```

#### Solución:

```bash
# Reiniciar Docker daemon
sudo systemctl restart docker

# Configurar firewall (si es necesario)
sudo ufw allow 27017
sudo ufw allow 5433
sudo ufw allow 6379
```

---

## 🛠️ Scripts de Diagnóstico Automatizado

### Script Principal de Verificación

```bash
#!/bin/bash
# Archivo: scripts/diagnose-docker-network.sh

echo "🔍 DIAGNÓSTICO DE RED DOCKER - SICORA"
echo "=================================="

# 1. Verificar servicios Docker
echo "📊 Estado de contenedores:"
docker compose ps

# 2. Verificar puertos
echo -e "\n🔌 Puertos ocupados:"
netstat -tulpn | grep -E "(5432|5433|27017|6379)"

# 3. Verificar redes
echo -e "\n🌐 Redes Docker:"
docker network ls | grep sicora

# 4. Probar conectividad
echo -e "\n📡 Pruebas de conectividad:"
for service in sicora_mongodb sicora_postgres sicora_redis; do
    if docker ps --format "table {{.Names}}" | grep -q $service; then
        echo "✅ $service está ejecutándose"
        # Obtener IP del contenedor
        ip=$(docker inspect $service --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
        echo "   IP: $ip"

        # Probar ping
        if ping -c 1 -W 1 $ip > /dev/null 2>&1; then
            echo "   ✅ Ping OK"
        else
            echo "   ❌ Ping falló"
        fi
    else
        echo "❌ $service no está ejecutándose"
    fi
done

# 5. Verificar logs de errores recientes
echo -e "\n📋 Errores recientes en logs:"
docker compose logs --since 5m 2>&1 | grep -i "error\|failed\|connection refused" | tail -5

echo -e "\n✅ Diagnóstico completado"
```

### Script de Reparación Automática

```bash
#!/bin/bash
# Archivo: scripts/repair-docker-network.sh

echo "🔧 REPARACIÓN AUTOMÁTICA DE RED DOCKER"
echo "===================================="

# 1. Detener todos los servicios
echo "🛑 Deteniendo servicios..."
docker compose down

# 2. Limpiar redes huérfanas
echo "🧹 Limpiando redes huérfanas..."
docker network prune -f

# 3. Recrear red principal
echo "🌐 Recreando red sicora-network..."
docker network rm sicora-network 2>/dev/null || true
docker network create sicora-network

# 4. Reiniciar servicios
echo "🚀 Reiniciando servicios..."
docker compose up -d

# 5. Esperar inicialización
echo "⏳ Esperando inicialización..."
sleep 10

# 6. Verificar estado
echo "✅ Verificando estado final:"
docker compose ps
```

---

## 📊 Monitoring de Red en Tiempo Real

### Comando de Monitoreo Continuo

```bash
# Monitorear logs de red en tiempo real
docker compose logs -f | grep -E "(connection|network|port|bind|refused)"

# Monitor específico por servicio
docker logs -f sicora_mongodb | grep -i network
docker logs -f sicora_postgres | grep -i connection
```

### Verificación de Salud Automática

```bash
#!/bin/bash
# Health check automático para servicios SICORA

check_service() {
    local service=$1
    local port=$2
    local host=${3:-localhost}

    if nc -z $host $port 2>/dev/null; then
        echo "✅ $service ($host:$port) - OK"
        return 0
    else
        echo "❌ $service ($host:$port) - FALLO"
        return 1
    fi
}

echo "🏥 VERIFICACIÓN DE SALUD - SERVICIOS SICORA"
echo "=========================================="

# Verificar servicios principales
check_service "MongoDB" 27017
check_service "PostgreSQL" 5433
check_service "Redis" 6379

# Verificar desde dentro de la red Docker
if docker ps --format "{{.Names}}" | grep -q sicora_mongodb; then
    echo -e "\n🔍 Verificación interna (red Docker):"
    docker exec sicora_mongodb sh -c "nc -z postgres 5432" && echo "✅ MongoDB → PostgreSQL" || echo "❌ MongoDB → PostgreSQL"
fi
```

---

## 🚀 Comandos de Recuperación Rápida

### Reinicio Completo

```bash
# Reinicio completo del entorno Docker
cd /home/epti/Documentos/epti-dev/sicora-app/sicora-infra/docker
docker compose down --volumes --remove-orphans
docker compose up -d
```

### Reinicio Selectivo por Servicio

```bash
# Solo MongoDB
docker compose restart mongodb

# Solo PostgreSQL
docker compose restart postgres

# Solo Redis
docker compose restart redis
```

### Limpieza Profunda (Último Recurso)

```bash
# ⚠️ CUIDADO: Esto elimina TODOS los datos
docker compose down --volumes
docker system prune -f
docker volume prune -f
docker network prune -f

# Recrear desde cero
docker compose up -d
```

---

## 📈 Métricas de Red

### Verificar Ancho de Banda

```bash
# Instalar iftop si no está disponible
# sudo apt install iftop

# Monitorear tráfico de red Docker
iftop -i docker0

# Estadísticas por contenedor
docker stats --format "table {{.Container}}\t{{.NetIO}}"
```

### Latencia Entre Servicios

```bash
# Medir latencia entre contenedores
docker exec sicora_mongodb sh -c "time nc -z postgres 5432"
docker exec sicora_postgres sh -c "time nc -z mongodb 27017"
```

---

## 🔧 Configuración Optimizada

### Variables de Entorno Recomendadas

```bash
# En .env file
COMPOSE_HTTP_TIMEOUT=120
DOCKER_CLIENT_TIMEOUT=120
COMPOSE_PROJECT_NAME=sicora
```

### Configuración Docker Daemon

```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-address-pools": [
    {
      "base": "172.17.0.0/16",
      "size": 24
    }
  ]
}
```

---

## 📝 Checklist de Resolución

### Antes de Reportar un Error:

- [ ] Ejecutar diagnóstico automático
- [ ] Verificar logs de los últimos 5 minutos
- [ ] Probar reinicio de servicio específico
- [ ] Verificar configuración de puertos
- [ ] Comprobar espacio en disco
- [ ] Verificar memoria disponible

### Pasos de Escalamiento:

1. **Nivel 1**: Reinicio de servicio individual
2. **Nivel 2**: Reinicio completo del stack
3. **Nivel 3**: Limpieza de redes y volúmenes
4. **Nivel 4**: Recreación completa del entorno

---

## 🆘 Contacto y Soporte

Para errores persistentes que no se resuelven con esta guía:

1. Ejecutar el script de diagnóstico completo
2. Capturar logs relevantes
3. Documentar pasos realizados
4. Crear issue en el repositorio con la información completa

---

**Fecha de última actualización**: Agosto 2025
**Versión**: 1.0
**Mantenido por**: Equipo SICORA OneVision
