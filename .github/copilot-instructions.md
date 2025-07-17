# Instrucciones para GitHub Copilot - Organización de Documentación SICORA

## � REGLAS CRÍTICAS - CUMPLIMIENTO OBLIGATORIO

### ❌ PROHIBIDO ABSOLUTO:

- **NUNCA** crear archivos `.md` en la raíz de `/sicora-app/` (excepto README.md)
- **NUNCA** crear documentación fuera de la estructura `_docs/`
- **NUNCA** duplicar documentos entre la raíz y `_docs/`
- **NUNCA** ignorar la estructura de carpetas establecida

### ✅ OBLIGATORIO ANTES DE CREAR DOCUMENTACIÓN:

1. **VERIFICAR** que no existe en la raíz un archivo similar
2. **DETERMINAR** la categoría correcta (integracion/, mcp/, configuracion/, desarrollo/, reportes/, guias/)
3. **USAR** únicamente rutas dentro de `_docs/[categoria]/`
4. **ACTUALIZAR** el índice correspondiente después de crear

### 🔍 VERIFICACIÓN AUTOMÁTICA:

Antes de crear cualquier archivo `.md`, SIEMPRE ejecutar:

```bash
# Verificar que no hay archivos .md incorrectos en la raíz
ls -la /sicora-app/*.md | grep -v README.md
# Si este comando devuelve algo, HAY UN PROBLEMA que debe corregirse
```

## �📚 Estructura de Documentación

### Ubicación de Documentos

- **README.md principal**: Permanece en la raíz del proyecto (`/sicora-app/README.md`)
- **Toda otra documentación**: Debe organizarse en `/sicora-app/_docs/` según temática
- **Prohibido**: Crear documentos `.md` adicionales en la raíz del proyecto

### Estructura de Carpetas

```
sicora-app/
├── README.md (ÚNICO archivo .md en la raíz)
└── _docs/
    ├── README.md (índice principal)
    ├── integracion/     # Documentación de integración
    ├── mcp/            # Documentación MCP
    ├── configuracion/   # Documentación de configuración
    ├── desarrollo/      # Documentación de desarrollo
    ├── reportes/       # Reportes y análisis
    └── guias/          # Guías y tutoriales
```

## 🎯 Reglas de Organización

### Al Crear Nueva Documentación:

1. **Determinar categoría**: Integración, MCP, Configuración, Desarrollo, Reportes, o Guías
2. **Crear en carpeta apropiada**: `/sicora-app/_docs/[categoria]/`
3. **Usar nomenclatura**: `TITULO_DOCUMENTO.md` en mayúsculas
4. **Actualizar índice**: Añadir referencia en el README de la carpeta correspondiente

### Categorías Específicas:

#### `/integracion/`

- Reportes de integración frontend-backend
- Verificaciones de conectividad
- Estados de integración entre servicios
- Troubleshooting de comunicación

#### `/mcp/`

- Configuración del servidor MCP
- Guías de uso de Model Context Protocol
- Scripts y herramientas MCP
- Documentación para principiantes

#### `/configuracion/`

- Configuración de entornos
- Variables de configuración
- Setup de servicios
- Configuración de herramientas

#### `/desarrollo/`

- Guías de desarrollo
- Estándares de código
- Flujos de trabajo
- Herramientas de desarrollo

#### `/reportes/`

- Reportes de estado del proyecto
- Análisis de rendimiento
- Métricas y evaluaciones
- Auditorías

#### `/guias/`

- Guías de usuario
- Tutoriales paso a paso
- Mejores prácticas
- Casos de uso

## 🔧 Comandos para Organización

### Crear Documentación Nueva:

```bash
# Crear en carpeta apropiada
touch /sicora-app/_docs/[categoria]/NUEVO_DOCUMENTO.md

# Actualizar índice de carpeta
echo "- [Nuevo Documento](./NUEVO_DOCUMENTO.md)" >> /sicora-app/_docs/[categoria]/README.md
```

### Mover Documentación Existente:

```bash
# Mover archivo
mv /sicora-app/DOCUMENTO.md /sicora-app/_docs/[categoria]/

# Actualizar referencias en README principal
# Cambiar enlaces de ./DOCUMENTO.md a ./_docs/[categoria]/DOCUMENTO.md
```

## 📝 Instrucciones Específicas para GitHub Copilot

### Cuando generes documentación:

1. **NUNCA crear archivos .md en la raíz** (excepto README.md principal)
2. **SIEMPRE preguntar la categoría** antes de crear documentación
3. **USAR rutas relativas** para enlaces internos
4. **ACTUALIZAR índices** después de crear documentación

### Patrones de nomenclatura:

- `REPORTE_[TEMA].md` para reportes
- `GUIA_[TEMA].md` para guías
- `CONFIGURACION_[TEMA].md` para configuración
- `INTEGRACION_[TEMA].md` para integración

### Enlaces en README principal:

```markdown
## 📚 Documentación

Para documentación detallada, consulta:

- [📋 Integración](./_docs/integracion/)
- [🤖 MCP](./_docs/mcp/)
- [⚙️ Configuración](./_docs/configuracion/)
- [🔧 Desarrollo](./_docs/desarrollo/)
- [📊 Reportes](./_docs/reportes/)
- [📖 Guías](./_docs/guias/)
```

## 🚨 Reglas Estrictas

### PROHIBIDO:

- Crear archivos `.md` en la raíz (excepto README.md)
- Duplicar documentación entre carpetas
- Crear carpetas adicionales sin consultar

### REQUERIDO:

- Usar la estructura de carpetas establecida
- Actualizar índices cuando se cree documentación
- Mantener enlaces relativos funcionales
- Seguir nomenclatura establecida

## 🔄 Mantenimiento

### 🛡️ Prevención de Errores Comunes

#### Error: Documentos en la Raíz

**NUNCA** crear archivos `.md` en `/sicora-app/` excepto `README.md`. Si encuentras documentos en la raíz:

```bash
# Verificar archivos problemáticos
ls -la /sicora-app/*.md | grep -v README.md

# Si hay archivos, moverlos a la ubicación correcta
mv /sicora-app/DOCUMENTO_INCORRECTO.md /sicora-app/_docs/[categoria]/
```

#### Error: Duplicación de Documentación

Antes de crear documentación, SIEMPRE verificar:

```bash
# Buscar documentos similares existentes
find /sicora-app/_docs/ -name "*TEMA*" -type f
```

#### Error: Índices Desactualizados

Después de crear/mover documentación:

```bash
# Actualizar README de la categoría
echo "- [Nuevo Documento](./DOCUMENTO.md)" >> /sicora-app/_docs/[categoria]/README.md
```

### Revisión Regular:

- Verificar que no hay archivos .md en la raíz
- Comprobar que los enlaces funcionan
- Actualizar índices cuando sea necesario
- Mantener estructura coherente

### Al Refactorizar:

- Mover archivos manteniendo referencias
- Actualizar todos los enlaces afectados
- Verificar que los índices estén actualizados
- Probar que la navegación funcione

---

## 🛠️ Herramientas y Comandos del Entorno Local

### Docker y Contenedores

#### Comando Docker Compose Correcto

**IMPORTANTE**: En este entorno local se debe usar `docker compose` (con espacio, NO `docker-compose` con guión).

```bash
# ✅ CORRECTO - Usar este comando
docker compose up -d

# ❌ INCORRECTO - NO usar este comando
docker-compose up -d
```

#### Gestión de Contenedores PostgreSQL

```bash
# Iniciar PostgreSQL (infraestructura completa)
cd sicora-infra
docker compose -f docker/docker-compose.yml up -d postgres

# Verificar estado de contenedores
docker compose -f docker/docker-compose.yml ps postgres

# Ver logs de PostgreSQL
docker compose -f docker/docker-compose.yml logs postgres

# Detener servicios
docker compose -f docker/docker-compose.yml down

# Conectar a PostgreSQL (puerto 5433 para evitar conflictos con instalación local)
psql -h localhost -p 5433 -U sicora_user -d sicora_dev
```

#### Otros Servicios de Infraestructura

```bash
# Backend Python
cd sicora-be-python
docker compose up -d

# Backend Go
cd sicora-be-go
docker compose up -d

# Frontend
cd sicora-app-fe
docker compose -f docker-compose.dev.yml up -d
```

### Verificación de Herramientas

Antes de ejecutar comandos Docker, siempre usar la sintaxis correcta para este entorno:

- **Docker Compose**: `docker compose` (V2, con espacio)
- **Python**: `python3`
- **Node.js**: Verificar versión con `node --version`
- **Zsh Shell**: Comandos optimizados para zsh

---

**Estas instrucciones deben seguirse SIEMPRE al trabajar con documentación en el proyecto SICORA.**
