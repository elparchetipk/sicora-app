# Configuración de Entorno para UserService Go - Middleware Optimizado

## Variables de Entorno Requeridas

### Configuración de Base de Datos
```bash
# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sicora_userservice
DB_USER=postgres
DB_PASSWORD=your_password
DB_SSLMODE=disable

# Database Pool Configuration
DB_MAX_OPEN_CONNS=25
DB_MAX_IDLE_CONNS=5
DB_CONN_MAX_LIFETIME=5m
```

### Configuración JWT y Seguridad
```bash
# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRATION=24h
JWT_REFRESH_EXPIRATION=168h  # 7 days

# Security Configuration
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=1m
REQUEST_TIMEOUT=30s
```

### Configuración del Servidor
```bash
# Server Configuration
PORT=8002
GIN_MODE=release  # Para producción, debug para desarrollo
HOST=0.0.0.0

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4000
CORS_ALLOWED_METHODS=GET,POST,PUT,DELETE,PATCH,OPTIONS
CORS_ALLOWED_HEADERS=Content-Type,Authorization,X-Request-ID
```

### Configuración de Logging
```bash
# Logging Configuration
LOG_LEVEL=info      # debug, info, warn, error
LOG_FORMAT=json     # json, text
LOG_OUTPUT=stdout   # stdout, stderr, file

# Request Logging
LOG_REQUESTS=true
LOG_RESPONSE_BODY=false  # Solo para debugging
LOG_REQUEST_BODY=false   # Solo para debugging
```

### Configuración de Cache y Performance
```bash
# Cache Configuration
AUTH_CACHE_TTL=5m
BLACKLIST_CACHE_TTL=1h

# Compression
COMPRESSION_ENABLED=true
COMPRESSION_LEVEL=6  # 1-9, 6 es balance performance/compression

# Connection Limits
MAX_HEADER_BYTES=1048576  # 1MB
READ_TIMEOUT=30s
WRITE_TIMEOUT=30s
IDLE_TIMEOUT=120s
```

## Archivo .env de Ejemplo

```bash
# UserService Go - Development Environment
# NOTA: En producción usar variables de entorno del sistema o secretos

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sicora_userservice
DB_USER=postgres
DB_PASSWORD=postgres123
DB_SSLMODE=disable

# JWT
JWT_SECRET=dev-secret-key-change-in-production-please
JWT_EXPIRATION=24h
JWT_REFRESH_EXPIRATION=168h

# Server
PORT=8002
GIN_MODE=debug
HOST=0.0.0.0

# Security
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=1m
REQUEST_TIMEOUT=30s

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4000,http://localhost:5173
CORS_ALLOWED_METHODS=GET,POST,PUT,DELETE,PATCH,OPTIONS
CORS_ALLOWED_HEADERS=Content-Type,Authorization,X-Request-ID

# Logging
LOG_LEVEL=debug
LOG_FORMAT=text
LOG_OUTPUT=stdout
LOG_REQUESTS=true
LOG_RESPONSE_BODY=false
LOG_REQUEST_BODY=false

# Cache
AUTH_CACHE_TTL=5m
BLACKLIST_CACHE_TTL=1h

# Performance
COMPRESSION_ENABLED=true
COMPRESSION_LEVEL=6
MAX_HEADER_BYTES=1048576
READ_TIMEOUT=30s
WRITE_TIMEOUT=30s
IDLE_TIMEOUT=120s
```

## Configuración para Diferentes Entornos

### Desarrollo Local
```bash
GIN_MODE=debug
LOG_LEVEL=debug
LOG_FORMAT=text
JWT_SECRET=dev-secret-key
RATE_LIMIT_REQUESTS=1000  # Más permisivo para desarrollo
```

### Testing
```bash
GIN_MODE=test
LOG_LEVEL=error
LOG_OUTPUT=stderr
JWT_SECRET=test-secret-key
RATE_LIMIT_REQUESTS=10000  # Sin límites para tests
DB_NAME=sicora_userservice_test
```

### Staging
```bash
GIN_MODE=release
LOG_LEVEL=info
LOG_FORMAT=json
JWT_SECRET=${JWT_SECRET_FROM_VAULT}
RATE_LIMIT_REQUESTS=200
DB_SSLMODE=require
```

### Producción
```bash
GIN_MODE=release
LOG_LEVEL=warn
LOG_FORMAT=json
LOG_OUTPUT=stdout
JWT_SECRET=${JWT_SECRET_FROM_VAULT}
RATE_LIMIT_REQUESTS=100
DB_SSLMODE=require
COMPRESSION_ENABLED=true
```

## Docker Compose - Variables de Entorno

```yaml
# docker-compose.yml
version: '3.8'
services:
  userservice-go:
    build: ./02-go/userservice
    ports:
      - "8002:8002"
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=sicora_userservice
      - DB_USER=postgres
      - DB_PASSWORD=postgres123
      - JWT_SECRET=docker-secret-key-change-in-production
      - GIN_MODE=release
      - PORT=8002
      - RATE_LIMIT_REQUESTS=100
      - LOG_LEVEL=info
      - LOG_FORMAT=json
    depends_on:
      - postgres
    networks:
      - sicora-network
```

## Configuración de Kubernetes

```yaml
# k8s/userservice-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: userservice-config
data:
  DB_HOST: "postgres-service"
  DB_PORT: "5432"
  DB_NAME: "sicora_userservice"
  GIN_MODE: "release"
  PORT: "8002"
  RATE_LIMIT_REQUESTS: "100"
  LOG_LEVEL: "info"
  LOG_FORMAT: "json"
  COMPRESSION_ENABLED: "true"

---
# k8s/userservice-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: userservice-secrets
type: Opaque
data:
  JWT_SECRET: <base64-encoded-secret>
  DB_PASSWORD: <base64-encoded-password>
```

## Validación de Configuración

### Script de Validación
```bash
#!/bin/bash
# validate-config.sh

echo "🔍 Validando configuración del UserService Go..."

# Verificar variables críticas
if [ -z "$JWT_SECRET" ]; then
    echo "❌ JWT_SECRET no está configurado"
    exit 1
fi

if [ -z "$DB_HOST" ]; then
    echo "❌ DB_HOST no está configurado"
    exit 1
fi

if [ "$GIN_MODE" = "release" ] && [ "$JWT_SECRET" = "dev-secret-key" ]; then
    echo "❌ Usando JWT_SECRET de desarrollo en modo release"
    exit 1
fi

echo "✅ Configuración básica validada"

# Verificar conectividad de base de datos
echo "🔍 Probando conexión a base de datos..."
if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; then
    echo "✅ Base de datos accesible"
else
    echo "❌ No se puede conectar a la base de datos"
    exit 1
fi

echo "🎉 Todas las validaciones pasaron"
```

## Mejores Prácticas

### Seguridad
1. **Nunca** commitear secretos al repositorio
2. Usar **variables de entorno** del sistema en producción
3. Rotar el **JWT_SECRET** regularmente
4. Configurar **SSL/TLS** en producción
5. Usar **secretos de Kubernetes** o **Vault** para secretos

### Performance
1. Ajustar **rate limiting** según la carga esperada
2. Configurar **timeouts** apropiados
3. Activar **compresión** en producción
4. Monitorear **métricas** de middleware

### Observabilidad
1. Usar **logging estructurado** (JSON)
2. Configurar **nivel de log** apropiado por entorno
3. Implementar **health checks**
4. Agregar **métricas** de Prometheus

### Mantenimiento
1. Documentar **cambios** de configuración
2. Probar configuración en **staging** primero
3. Automatizar **validación** de configuración
4. Mantener **coherencia** entre entornos
