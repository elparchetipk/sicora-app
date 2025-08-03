# Sistema de Configuración Dual EPTI/SENA

## 🎯 Descripción

El sistema permite construir y desplegar la misma aplicación con dos configuraciones diferentes:

- **EPTI/ONEVISION**: Versión para despliegue público/opensource sin logos del SENA
- **SENA**: Versión institucional oficial con branding completo del SENA

## 📁 Estructura del Sistema

```
sicora-app-fe/
├── .env.development     # Configuración desarrollo (EPTI)
├── .env.hostinger      # Configuración producción EPTI
├── .env.sena           # Configuración producción SENA
├── src/config/
│   └── brand.ts        # Configuración centralizada de marca
└── test-brand-config.js # Script verificación configuraciones
```

## 🔧 Variables de Entorno

### Archivos de Configuración

#### `.env.development`

```env
VITE_BUILD_TARGET=development
VITE_BRAND_NAME=EPTI - ONEVISION
VITE_BRAND_SUBTITLE=Sistema de Coordinación Académica
VITE_BRAND_DESCRIPTION=Plataforma integral para la gestión académica
VITE_SHOW_LOGO=false
VITE_ORGANIZATION=EPTI
VITE_ORGANIZATION_FULL=Escuela de Programación y Tecnologías de la Información
VITE_CONTACT_EMAIL=contacto@epti.edu.co
VITE_SUPPORT_URL=http://localhost:5173/soporte
VITE_DOCS_URL=http://localhost:5173/docs
```

#### `.env.hostinger`

```env
VITE_BUILD_TARGET=hostinger
VITE_BRAND_NAME=EPTI - ONEVISION
VITE_BRAND_SUBTITLE=Sistema de Coordinación Académica
VITE_BRAND_DESCRIPTION=Plataforma integral para la gestión académica
VITE_SHOW_LOGO=false
VITE_ORGANIZATION=EPTI
VITE_ORGANIZATION_FULL=Escuela de Programación y Tecnologías de la Información
VITE_CONTACT_EMAIL=contacto@epti.edu.co
VITE_SUPPORT_URL=https://epti.onevision.com.co/soporte
VITE_DOCS_URL=https://epti.onevision.com.co/docs
```

#### `.env.sena`

```env
VITE_BUILD_TARGET=sena
VITE_BRAND_NAME=SENA
VITE_BRAND_SUBTITLE=Sistema de Información de Coordinación Académica
VITE_BRAND_DESCRIPTION=Sistema integral de gestión académica del CGMLTI
VITE_SHOW_LOGO=true
VITE_ORGANIZATION=SENA
VITE_ORGANIZATION_FULL=OneVision Open Source
VITE_CONTACT_EMAIL=cgmlti@sena.edu.co
VITE_SUPPORT_URL=https://sicora.sena.edu.co/soporte
VITE_DOCS_URL=https://sicora.sena.edu.co/docs
```

## 🔄 Scripts de Build

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "dev:hostinger": "cp .env.hostinger .env && vite",
    "dev:sena": "cp .env.sena .env && vite",
    "build": "tsc -b && vite build",
    "build:hostinger": "cp .env.hostinger .env && tsc -b && vite build",
    "build:sena": "cp .env.sena .env && tsc -b && vite build",
    "build:both": "pnpm build:hostinger && pnpm build:sena",
    "preview:hostinger": "cp .env.hostinger .env && vite preview",
    "preview:sena": "cp .env.sena .env && vite preview"
  }
}
```

### Uso de Scripts

```bash
# Desarrollo EPTI
pnpm dev
pnpm dev:hostinger

# Desarrollo SENA
pnpm dev:sena

# Build para producción
pnpm build:hostinger   # Build EPTI/Hostinger
pnpm build:sena        # Build SENA
pnpm build:both        # Ambos builds

# Preview
pnpm preview:hostinger # Preview EPTI
pnpm preview:sena      # Preview SENA
```

## 📄 Configuración Centralizada

### `src/config/brand.ts`

```typescript
export interface BrandConfig {
  name: string;
  subtitle: string;
  description: string;
  showLogo: boolean;
  buildTarget: 'development' | 'hostinger' | 'sena';
  organization: string;
  organizationFull: string;
  contactEmail: string;
  supportUrl: string;
  docsUrl: string;
}

export const BRAND_CONFIG: BrandConfig = {
  name: import.meta.env.VITE_BRAND_NAME || 'EPTI - ONEVISION',
  subtitle:
    import.meta.env.VITE_BRAND_SUBTITLE || 'Sistema de Coordinación Académica',
  // ... más configuraciones
};

// Helpers para identificar entorno
export const IS_SENA_BUILD = BRAND_CONFIG.buildTarget === 'sena';
export const IS_HOSTINGER_BUILD = BRAND_CONFIG.buildTarget === 'hostinger';
export const IS_DEVELOPMENT = BRAND_CONFIG.buildTarget === 'development';

// Textos adaptativos
export const BRAND_TEXTS = {
  welcomeMessage: IS_SENA_BUILD
    ? '¡Bienvenido al Sistema SICORA!'
    : '¡Bienvenido a EPTI - ONEVISION!',
  // ... más textos
};
```

## 🎨 Componentes Adaptativos

### Ejemplo: InstitutionalHeader

```tsx
import { BRAND_CONFIG, IS_SENA_BUILD } from '../config/brand';

export function InstitutionalHeader() {
  return (
    <header>
      {/* Logo condicional */}
      {BRAND_CONFIG.showLogo && <LogoSenaNav size='md' />}

      {/* Título adaptativo */}
      <h1>{IS_SENA_BUILD ? 'Sistema SICORA' : BRAND_CONFIG.name}</h1>

      {/* Subtítulo adaptativo */}
      <p>
        {IS_SENA_BUILD
          ? 'Coordinación Académica - CGMLTI'
          : BRAND_CONFIG.subtitle}
      </p>
    </header>
  );
}
```

## 🧪 Verificación de Configuraciones

### Script de Prueba

```bash
# Verificar todas las configuraciones
node test-brand-config.js

# Verificar builds
pnpm run type-check
pnpm run build:hostinger
pnpm run build:sena
```

### Salida Esperada

```
🔍 Verificando configuraciones de marca...

📋 Development:
   ✅ Variables cargadas:
      🏢 Organización: EPTI
      📛 Nombre: EPTI - ONEVISION
      🎯 Target: development
      🖼️  Logo: false

📋 SENA:
   ✅ Variables cargadas:
      🏢 Organización: SENA
      📛 Nombre: SENA
      🎯 Target: sena
      🖼️  Logo: true
```

## 🚀 Proceso de Deployment

### 1. Deployment EPTI (Hostinger)

```bash
# Build para Hostinger
pnpm build:hostinger

# Deploy a Hostinger
rsync -avz dist/ user@server:/var/www/epti.onevision.com.co/
```

### 2. Deployment SENA (Datacenter)

```bash
# Build para SENA
pnpm build:sena

# Deploy a datacenter SENA
scp -r dist/ sena-server:/var/www/sicora.sena.edu.co/
```

### 3. Deployment Automatizado

```bash
# Build ambas versiones
pnpm build:both

# Deploy automático (requiere configuración CI/CD)
npm run deploy:both
```

## 🔍 Diferencias entre Builds

| Aspecto            | EPTI/Hostinger        | SENA                |
| ------------------ | --------------------- | ------------------- |
| **Logo**           | ❌ Sin logo           | ✅ Logo SENA        |
| **Nombre**         | EPTI - ONEVISION      | SENA                |
| **Colores**        | Neutros               | Verde SENA          |
| **Footer**         | Enlaces EPTI          | Enlaces ministerios |
| **Redes Sociales** | ❌                    | ✅ Redes SENA       |
| **Contacto**       | contacto@epti.edu.co  | cgmlti@sena.edu.co  |
| **URL Base**       | epti.onevision.com.co | sicora.sena.edu.co  |

## 📚 Buenas Prácticas

### ✅ Hacer

- Usar variables de entorno para toda configuración específica de marca
- Centralizar la configuración en `src/config/brand.ts`
- Usar helpers como `IS_SENA_BUILD` para lógica condicional
- Verificar ambos builds antes de deployment
- Mantener funcionalidad idéntica en ambas versiones

### ❌ Evitar

- Hardcodear textos específicos de marca en componentes
- Duplicar código entre versiones
- Usar logos/imágenes del SENA en build público
- Diferencias funcionales entre versiones
- Variables de entorno en código de producción

## 🔧 Troubleshooting

### Error: Variables no se cargan

```bash
# Verificar que el archivo .env existe
ls -la .env*

# Verificar contenido
cat .env

# Limpiar cache de Vite
rm -rf node_modules/.vite
pnpm dev
```

### Error: Build falla

```bash
# Verificar TypeScript
pnpm type-check

# Verificar ESLint
pnpm lint:fix

# Build paso a paso
pnpm build:hostinger
pnpm build:sena
```

### Error: Configuración incorrecta

```bash
# Ejecutar script de verificación
node test-brand-config.js

# Verificar variables en runtime
console.log(BRAND_CONFIG);
```

## 📈 Próximos Pasos

1. **Automatización CI/CD**: Configurar pipelines para deployment automático
2. **Testing E2E**: Verificar ambas configuraciones en tests automatizados
3. **Monitoreo**: Implementar analytics diferenciados por marca
4. **Optimización**: Lazy loading condicional de componentes específicos
5. **Documentación**: Storybook con stories para ambas configuraciones

---

✅ **Sistema completamente funcional y listo para producción**
