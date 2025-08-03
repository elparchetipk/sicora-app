# SICORA Frontend

Sistema de Información de Coordinación Académica - Frontend moderno construido con React 19 + Vite + TailwindCSS.

## 🚀 Stack Tecnológico

- **Framework**: React 19 con TypeScript
- **Build Tool**: Vite 7.0
- **Styling**: TailwindCSS + Design Tokens SENA
- **Package Manager**: pnpm (exclusivo)
- **Testing**: Vitest + React Testing Library
- **Linting**: ESLint + Prettier
- **Git Hooks**: Husky + lint-staged + Commitlint

## 📋 Requisitos Previos

- Node.js ≥ 18.0.0
- pnpm ≥ 8.0.0

## 🛠️ Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd sicora-frontend

# Instalar dependencias (solo pnpm permitido)
pnpm install
```

## 🎯 Scripts Disponibles

```bash
# Desarrollo
pnpm dev                    # Servidor de desarrollo
pnpm build                  # Build de producción
pnpm preview               # Preview del build

# Calidad de código
pnpm lint                  # Verificar código con ESLint
pnpm lint:fix              # Corregir errores de ESLint
pnpm format                # Formatear código con Prettier
pnpm format:check          # Verificar formato de código
pnpm type-check            # Verificar tipos de TypeScript

# Testing
pnpm test                  # Ejecutar tests
pnpm test:ui               # Ejecutar tests con UI
pnpm test:coverage         # Tests con coverage

# Validación completa
pnpm validate              # Ejecutar todas las verificaciones
```

## 🔧 Configuración pnpm-only

Este proyecto está configurado para usar **exclusivamente pnpm** como package manager.

### ¿Por qué pnpm-only?

- **Seguridad**: Evita dependencias duplicadas y vulnerabilidades
- **Rendimiento**: Instalaciones más rápidas con hard links
- **Consistencia**: Mismo lock file en todo el equipo
- **Espacio**: Menos espacio en disco con store compartido

Ver [PNPM-ONLY.md](./PNPM-ONLY.md) para más detalles.

## 🎨 Design System SENA

El proyecto implementa el design system oficial SENA 2024:

- **Colores**: Paleta institucional (verde, naranja, violeta, azul)
- **Tipografía**: Inter + Poppins según especificaciones
- **Espaciado**: Sistema basado en 4px
- **Componentes**: Biblioteca siguiendo atomic design

## 🛡️ Calidad de Código

### Git Hooks Automáticos

- **pre-commit**: Ejecuta lint-staged (ESLint + Prettier + TypeScript)
- **commit-msg**: Valida formato de commit con Commitlint

### Convenciones de Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: agregar nuevo componente Button
fix: corregir problema de responsive en Header
docs: actualizar documentación de API
style: formatear código según Prettier
refactor: reestructurar componentes de layout
test: agregar tests para utilidades
chore: actualizar dependencias
```

### Lint-staged

Ejecuta automáticamente en cada commit:

- ESLint con auto-fix
- Prettier para formateo
- Type checking incremental

## 📁 Estructura del Proyecto

```
sicora-frontend/
├── src/
│   ├── components/          # Componentes React
│   │   ├── atoms/          # Componentes básicos
│   │   ├── molecules/      # Componentes compuestos
│   │   └── organisms/      # Componentes complejos
│   ├── pages/              # Páginas principales
│   ├── utils/              # Utilidades
│   ├── styles/             # Estilos globales
│   └── types/              # Tipos TypeScript
├── public/                 # Assets estáticos
├── .husky/                 # Git hooks
└── docs/                   # Documentación
```

## 🚦 Estados del Proyecto

- ✅ **Configuración base**: React 19 + Vite + TailwindCSS
- ✅ **pnpm-only**: Package manager exclusivo configurado
- ✅ **Git hooks**: Husky + lint-staged + commitlint
- ✅ **Calidad de código**: ESLint + Prettier + TypeScript
- 🚧 **Design System**: Componentes base SENA
- 🚧 **Testing**: Configuración de tests
- 📋 **CI/CD**: GitHub Actions / GitLab CI

## 👥 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feat/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feat/nueva-funcionalidad`)
5. Abre un Pull Request

Los Git hooks se ejecutarán automáticamente para validar calidad de código.

## 📄 Licencia

Este proyecto es propiedad de OneVision Open Source - Educational Platform.

---

**SICORA** - Sistema de Información de Coordinación Académica
SENA 2024 - Construido con ❤️ y las mejores prácticas de desarrollo
