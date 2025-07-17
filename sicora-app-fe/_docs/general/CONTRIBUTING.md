# Guía de Contribución SICORA Frontend

¡Gracias por tu interés en contribuir al frontend de SICORA! Esta guía te ayudará a comenzar.

## 🚀 Inicio Rápido

### Prerrequisitos

- Node.js >= 18.0.0
- pnpm >= 8.0.0
- Git

### Configuración del Entorno

1. Fork el repositorio
2. Clona tu fork localmente:

   ```bash
   git clone https://github.com/tu-usuario/sicora-frontend.git
   cd sicora-frontend
   ```

3. Instala las dependencias:

   ```bash
   pnpm install
   ```

4. Ejecuta el servidor de desarrollo:
   ```bash
   pnpm dev
   ```

## 📝 Proceso de Contribución

### 1. Crear una Rama

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

### 2. Hacer Cambios

- Asegúrate de seguir las convenciones de código
- Escribe tests para tu código
- Actualiza la documentación si es necesario

### 3. Verificar Calidad de Código

```bash
# Ejecutar linting
pnpm lint

# Verificar formateo
pnpm format:check

# Ejecutar tests
pnpm test

# Verificar tipos
pnpm type-check

# O ejecutar todo junto
pnpm validate
```

### 4. Commit y Push

```bash
git add .
git commit -m "feat: añadir nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

### 5. Crear Pull Request

- Ve a GitHub y crea un Pull Request
- Sigue el template de PR
- Vincula cualquier issue relacionado

## 🎯 Convenciones de Código

### Naming Conventions

- **Componentes**: PascalCase (`Button.tsx`, `UserProfile.tsx`)
- **Hooks**: camelCase con prefijo `use` (`useAuth.ts`, `useLocalStorage.ts`)
- **Utilities**: camelCase (`formatDate.ts`, `validateEmail.ts`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`, `DEFAULT_THEME`)

### Estructura de Archivos

```
src/
├── components/           # Componentes reutilizables
│   ├── ui/              # Componentes base (Button, Input, etc.)
│   └── feature/         # Componentes específicos de funcionalidad
├── pages/               # Páginas/Rutas
├── hooks/               # Custom hooks
├── utils/               # Funciones utilitarias
├── services/            # Servicios API
├── stores/              # Estado global (Zustand)
├── types/               # Definiciones TypeScript
└── assets/              # Recursos estáticos
```

### Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `style:` cambios de formato/estilo
- `refactor:` refactorización de código
- `test:` añadir o modificar tests
- `chore:` tareas de mantenimiento

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests en modo watch
pnpm test

# Tests con coverage
pnpm test:coverage

# Tests UI
pnpm test:ui
```

### Escribir Tests

- Tests unitarios para funciones/hooks
- Tests de componente para UI
- Tests de integración para flujos completos

Ejemplo:

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renderiza correctamente', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });
});
```

## 🎨 Diseño y UI

### Design System

- Usamos TailwindCSS con tokens de diseño SENA
- Componentes base con Radix UI
- Iconos de Lucide React

### Responsive Design

- Mobile-first approach
- Breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px)

## 🚨 Reportar Issues

- Usa los templates de issue
- Incluye información detallada
- Añade capturas de pantalla si es relevante

## 📋 Checklist para Pull Requests

- [ ] Código sigue las convenciones del proyecto
- [ ] Tests añadidos/actualizados
- [ ] Documentación actualizada
- [ ] No hay errores de linting
- [ ] No hay errores de tipo TypeScript
- [ ] PR template completado

## ❓ ¿Necesitas Ayuda?

- Abre un issue con la etiqueta `question`
- Contacta al equipo de desarrollo
- Revisa la documentación existente

¡Gracias por contribuir a SICORA! 🎉
