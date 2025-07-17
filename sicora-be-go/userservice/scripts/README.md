# Scripts de Utilidades - UserService Go

Este directorio contiene scripts útiles para desarrollo, testing y validación del UserService.

## Scripts Disponibles

### `validate-middleware.sh`
Script de validación del middleware optimizado que verifica:
- Estado del servidor
- Headers de seguridad
- Rate limiting
- Rutas públicas y protegidas
- CORS
- Logging y Request ID
- Compresión
- Documentación
- Estructura de errores

**Uso:**
```bash
# Asegurar que el servidor esté ejecutándose
cd 02-go/userservice
go run main.go &

# En otra terminal, ejecutar la validación
chmod +x scripts/validate-middleware.sh
./scripts/validate-middleware.sh
```

**Prerrequisitos:**
- Servidor UserService ejecutándose en puerto 8002
- curl instalado
- Base de datos PostgreSQL configurada

## Ejecución de Scripts

### Hacer ejecutables
```bash
chmod +x scripts/*.sh
```

### Ejecutar validación completa
```bash
# Desde el directorio userservice
./scripts/validate-middleware.sh
```

## Próximos Scripts Planificados

### `performance-test.sh`
- Load testing del middleware
- Métricas de rate limiting
- Análisis de throughput

### `security-scan.sh`
- Escaneo de vulnerabilidades
- Validación de headers de seguridad
- Verificación de configuraciones

### `integration-test.sh`
- Tests de integración completos
- Validación de flujos end-to-end
- Testing de autenticación real

### `monitor-logs.sh`
- Análisis de logs en tiempo real
- Detección de anomalías
- Métricas de uso

## Contribución

Para agregar nuevos scripts:
1. Crear el archivo `.sh` en este directorio
2. Hacerlo ejecutable con `chmod +x`
3. Documentar su uso en este README
4. Seguir el estilo de logging y colores de `validate-middleware.sh`
