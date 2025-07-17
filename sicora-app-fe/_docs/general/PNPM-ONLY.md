# SICORA - Configuración pnpm-only

Este proyecto está configurado para usar **exclusivamente pnpm** como package manager.

## ¿Por qué pnpm-only?

- **Seguridad**: Evita dependencias duplicadas y vulnerabilidades
- **Rendimiento**: Instalaciones más rápidas con hard links
- **Consistencia**: Mismo lock file en todo el equipo
- **Espacio**: Menos espacio en disco con store compartido

## Configuración

### 1. `.npmrc`

```ini
auto-install-peers=true
strict-peer-dependencies=false
shamefully-hoist=false
node-linker=isolated
package-import-method=clone
```

### 2. `package.json`

```json
{
  "packageManager": "pnpm@9.0.0",
  "engines": {
    "node": ">=18.0.0",
    "pnpm": ">=8.0.0",
    "npm": "use pnpm",
    "yarn": "use pnpm"
  },
  "scripts": {
    "preinstall": "npx only-allow pnpm"
  }
}
```

## Comandos bloqueados

Si intentas usar npm o yarn:

```bash
npm install  # ❌ Error: Use pnpm
yarn install # ❌ Error: Use pnpm
```

Solo funciona:

```bash
pnpm install # ✅ Correcto
pnpm dev     # ✅ Correcto
pnpm build   # ✅ Correcto
```

## Instalación de pnpm

Si no tienes pnpm instalado:

```bash
# Via npm (una sola vez)
npm install -g pnpm

# Via Homebrew (macOS)
brew install pnpm

# Via script oficial
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

## Comandos principales

```bash
# Desarrollo
pnpm dev

# Build de producción
pnpm build

# Tests
pnpm test

# Linting
pnpm lint

# Type checking
pnpm type-check

# Formato de código
pnpm format
```

## Ventajas en este proyecto

1. **Instalaciones rápidas**: ~50% más rápido que npm
2. **Menos espacio**: Hard links evitan duplicación
3. **Seguridad**: Evita phantom dependencies
4. **Monorepo ready**: Preparado para workspaces futuros
