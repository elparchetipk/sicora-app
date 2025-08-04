# SICORA Frontend - React + TypeScript + Vite

## 🏛️ Sistema de Información de Coordinación Académica

Frontend del proyecto SICORA desarrollado para OneVision Open Source, construido con React 18, TypeScript y Vite para una experiencia de desarrollo moderna y eficiente.

## 🚀 Tecnologías Principales

- **React 18** - Biblioteca de interfaz de usuario
- **TypeScript** - Tipado estático para JavaScript
- **Vite** - Herramienta de build rápida
- **TailwindCSS** - Framework de CSS utilitario
- **Zustand** - Gestión de estado ligera
- **React Hook Form** - Gestión de formularios
- **Zod** - Validación de esquemas

## 📁 Estructura del Proyecto

```
sicora-app-fe/
├── src/
│   ├── components/     # Componentes reutilizables
│   ├── pages/         # Páginas de la aplicación
│   ├── hooks/         # Hooks personalizados
│   ├── store/         # Gestión de estado (Zustand)
│   ├── types/         # Definiciones de tipos
│   ├── utils/         # Utilidades
│   └── assets/        # Recursos estáticos
├── public/            # Archivos públicos
├── _docs/             # Documentación organizada
├── scripts/           # Scripts de automatización
└── README.md          # Este archivo
```

## 🔧 Desarrollo

### Prerrequisitos

- Node.js >= 18
- pnpm (recomendado)

### Instalación

```bash
# Instalar dependencias
pnpm install

# Desarrollo
pnpm dev

# Build
pnpm build

# Preview
pnpm preview
```

### Scripts Disponibles

```bash
# Desarrollo con hot reload
pnpm dev

# Build para producción
pnpm build

# Preview del build
pnpm preview

# Linting
pnpm lint

# Tests
pnpm test

# Verificar estructura de documentación
./scripts/verify-doc-structure.sh
```

## 🎨 Design System

El proyecto utiliza un sistema de diseño basado en los lineamientos institucionales de OneVision:

- **Branding dual**: Soporte para OneVision y EPTI
- **Design tokens**: Variables de diseño consistentes
- **Componentes**: Biblioteca de componentes reutilizables
- **Accesibilidad**: Cumplimiento de estándares WCAG

## 🔗 Integración Backend

Integración completa con el backend en Go:

- **Autenticación**: JWT con refresh automático
- **API REST**: Comunicación con microservicios
- **Estado**: Sincronización con Zustand
- **Validación**: Esquemas Zod para datos

## 📚 Documentación

Para documentación detallada, consulta la [documentación organizada](./_docs/):

- [📋 Integración](./_docs/integracion/) - Integración frontend-backend
- [⚙️ Configuración](./_docs/configuracion/) - Setup y configuración
- [🔧 Desarrollo](./_docs/desarrollo/) - Guías de desarrollo
- [📊 Reportes](./_docs/reportes/) - Reportes de estado
- [📖 Guías](./_docs/guias/) - Guías de implementación
- [🎨 Diseño](./_docs/diseno/) - Design tokens y UI/UX
- [📄 General](./_docs/general/) - Documentación general

## 🛠️ Configuración de Entorno

### Variables de Entorno

```bash
# .env.development
VITE_API_URL=http://localhost:8002
VITE_APP_ENV=development

# .env.production
VITE_API_URL=https://api.sicora.onevision.edu.co
VITE_APP_ENV=production
```

### Configuración de VS Code

El proyecto incluye configuración específica para VS Code con:

- Extensiones recomendadas
- Configuración de linting
- Snippets personalizados
- Configuración de debugger

## 🚀 Despliegue

### Build para Producción

```bash
# Build
pnpm build

# El directorio dist/ contiene los archivos estáticos
```

### Despliegue en Hostinger

Ver [Configuración de Hostinger](./_docs/configuracion/HOSTINGER_SETUP.md)

## 🧪 Testing

```bash
# Ejecutar tests
pnpm test

# Tests con cobertura
pnpm test:coverage

# Tests en modo watch
pnpm test:watch
```

## 🔍 Verificación de Calidad

```bash
# Linting
pnpm lint

# Verificar tipos
pnpm type-check

# Verificar estructura de documentación
./scripts/verify-doc-structure.sh
```

## 📈 Estado del Proyecto

### ✅ Completado

- ✅ Configuración base con Vite + React + TypeScript
- ✅ Sistema de design tokens OneVision
- ✅ Integración con backend Go
- ✅ Autenticación JWT
- ✅ Gestión de estado con Zustand
- ✅ Componentes base institucionales
- ✅ Responsive design
- ✅ Documentación organizada

### 🔄 En Desarrollo

- 🔄 Módulos específicos de gestión académica
- 🔄 Dashboard de reportes
- 🔄 Internacionalización
- 🔄 Tests unitarios completos

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

Ver [Guía de Contribución](./_docs/general/CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [CODE_OF_CONDUCT.md](./_docs/general/CODE_OF_CONDUCT.md) para más detalles.

## 🔧 Mantenimiento

### Estructura de Documentación

- **Solo README.md** en la raíz
- **Toda documentación** en `_docs/` por categorías
- **Scripts** en `scripts/`
- **Verificación automática** con `./scripts/verify-doc-structure.sh`

### Actualizaciones

- Mantener dependencias actualizadas
- Ejecutar verificaciones de estructura regularmente
- Actualizar documentación con nuevas funcionalidades

---

_Desarrollado con ❤️ para OneVision Open Source por el equipo EPTI_
