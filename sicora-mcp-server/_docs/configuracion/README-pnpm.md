# Servidor MCP SICORA - Guía de uso con pnpm

## 🚀 Configuración inicial

### Prerequisitos

- Node.js >= 18.0.0
- pnpm (se instala automáticamente si no está disponible)

### Instalación rápida

```bash
# Desde el directorio sicora-mcp-server
pnpm install
pnpm run mcp:setup
```

## 📋 Comandos disponibles

### Comandos principales

```bash
# Configurar servidor MCP por primera vez
pnpm run mcp:setup

# Iniciar servidor en producción
pnpm start

# Iniciar en modo desarrollo
pnpm run dev

# Compilar TypeScript
pnpm run build

# Modo desarrollo con recarga automática
pnpm run watch
```

### Comandos de utilidad

```bash
# Mostrar estado del servidor
pnpm run mcp:status

# Limpiar archivos compilados
pnpm run mcp:clean

# Ejecutar pruebas
pnpm test

# Linter
pnpm run lint
```

### Scripts de desarrollo

```bash
# Usar el script de desarrollo
./scripts/dev.sh [comando]

# Ejemplos:
./scripts/dev.sh setup    # Configurar por primera vez
./scripts/dev.sh dev      # Modo desarrollo
./scripts/dev.sh build    # Compilar
./scripts/dev.sh status   # Estado del servidor
```

## 🔧 Configuración VS Code

El servidor MCP se configura automáticamente en VS Code mediante el archivo `.vscode/mcp.json`:

```json
{
  "servers": {
    "sicora-mcp": {
      "command": "pnpm",
      "args": ["--dir", "sicora-mcp-server", "run", "start"],
      "env": {
        "NODE_ENV": "production",
        "SICORA_PROJECT_ROOT": "/ruta/completa/al/proyecto",
        "SICORA_FRONTEND_PATH": "/ruta/al/frontend",
        "SICORA_BACKEND_PATH": "/ruta/al/backend"
      }
    }
  }
}
```

## 🎯 Características del servidor MCP

### Herramientas disponibles

- **sicora-analyze**: Análisis de estructura del proyecto
- **sicora-generate**: Generación de código especializado
- **sicora-integrate**: Integración frontend-backend
- **sicora-test**: Gestión de pruebas
- **sicora-document**: Generación de documentación

### Recursos disponibles

- **project-structure**: Estructura del proyecto SICORA
- **integration-guide**: Guía de integración
- **best-practices**: Mejores prácticas
- **troubleshooting**: Solución de problemas

## 🔄 Flujo de desarrollo

### Configuración inicial

1. Ejecutar `pnpm run mcp:setup`
2. Reiniciar VS Code
3. El servidor MCP estará disponible automáticamente

### Desarrollo diario

1. Iniciar servidor: `pnpm run dev`
2. Usar herramientas MCP en VS Code
3. Compilar para producción: `pnpm run build`

### Integración con otros servicios

- **Frontend**: sicora-app-fe (React + TypeScript)
- **Backend**: sicora-be-go (Go + Gin)
- **Base de datos**: PostgreSQL
- **Gestor de paquetes**: pnpm (preferido)

## 📁 Estructura del proyecto

```
sicora-mcp-server/
├── src/
│   └── index.ts              # Servidor MCP principal
├── dist/                     # Archivos compilados
├── scripts/
│   ├── configure-mcp.sh      # Configuración automática
│   └── dev.sh               # Herramientas de desarrollo
├── package.json             # Configuración pnpm
├── tsconfig.json            # Configuración TypeScript
├── .npmrc                   # Configuración pnpm
└── README-pnpm.md          # Esta guía
```

## 🐛 Solución de problemas

### Servidor no inicia

```bash
# Verificar estado
pnpm run mcp:status

# Limpiar y recompilar
pnpm run mcp:clean
pnpm run build
```

### Errores de dependencias

```bash
# Reinstalar dependencias
rm -rf node_modules
pnpm install
```

### Problemas de compilación

```bash
# Verificar TypeScript
pnpm run build

# Verificar sintaxis
pnpm run lint
```

## 🔗 Integración con VS Code

### Conexión manual

1. Abrir VS Code
2. Ctrl+Shift+P → "MCP: Connect to Server"
3. Seleccionar "sicora-mcp"

### Verificar conexión

- El servidor aparecerá en la barra de estado
- Las herramientas MCP estarán disponibles
- Los recursos serán accesibles

## 📚 Recursos adicionales

- [Documentación MCP](https://modelcontextprotocol.io/)
- [Guía de desarrollo SICORA](../README.md)
- [Integración frontend-backend](../sicora-app-fe/INTEGRACION_FRONTEND_BACKEND_COMPLETADA.md)

## 🤝 Contribución

Para contribuir al servidor MCP:

1. Fork del repositorio
2. Crear rama de feature
3. Desarrollar usando `pnpm run dev`
4. Ejecutar pruebas: `pnpm test`
5. Crear pull request

---

**Nota**: Este servidor está optimizado para el desarrollo de SICORA y usa pnpm como gestor de paquetes preferido para mantener consistencia con el resto del proyecto.
