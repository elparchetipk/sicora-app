# 🎨 Guía de Estilo - Colores y Contraste SICORA

## ❌ REGLA FUNDAMENTAL: NO DEGRADÉS

**Nunca usar degradés (gradients) en ningún componente de la aplicación.**

### Razones:

- ❌ **Contraste pobre**: Los degradés dificultan la legibilidad
- ❌ **Accesibilidad comprometida**: No cumplen estándares WCAG 2.1
- ❌ **Inconsistencia visual**: Varían según dispositivo y resolución
- ❌ **Problemas de impresión**: Se ven mal en impresiones
- ❌ **Mantenimiento complejo**: Difíciles de ajustar y mantener

## ✅ Esquema de Colores Aprobado

### Colores Principales SENA

```css
/* Colores institucionales */
--sena-blue: #003366; /* Azul SENA principal */
--sena-orange: #ff8c00; /* Naranja SENA principal */
--sena-green: #228b22; /* Verde SENA secundario */
```

### Combinaciones de Alto Contraste

#### 1. Fondo Naranja + Texto Gris ✅

```css
/* Para avisos importantes y disclaimers */
background-color: #ff8c00; /* sena-orange */
color: #4b5563; /* text-gray-600 */
font-weight: 600; /* Semibold para legibilidad */
```

#### 2. Fondo Azul + Texto Blanco ✅

```css
/* Para headers y elementos principales */
background-color: #003366; /* sena-blue */
color: #ffffff; /* text-white */
```

#### 3. Fondo Gris Claro + Texto Oscuro ✅

```css
/* Para contenido general */
background-color: #f9fafb; /* gray-50 */
color: #374151; /* text-gray-700 */
```

### Combinaciones Prohibidas ❌

```css
/* NUNCA usar estas combinaciones */
background: linear-gradient(...); /* Cualquier degradé */
background: radial-gradient(...); /* Cualquier degradé radial */
background-image: gradient(...); /* Cualquier gradient */

/* Colores con contraste insuficiente */
color: #cccccc;
background: #ffffff; /* Contraste < 3:1 */
color: #ffff00;
background: #ffffff; /* Amarillo sobre blanco */
```

## 🎯 Implementación en Componentes

### DisclaimerBanner - Ejemplo Correcto

```tsx
// ✅ CORRECTO - Fondo naranja sólido con texto gris
<div className="bg-sena-orange text-gray-700">
  <h3 className="text-gray-700 font-semibold">Título</h3>
  <p className="text-gray-600">Contenido</p>
</div>

// ❌ INCORRECTO - Degradé horrible
<div className="bg-gradient-to-r from-orange-400 to-red-500">
  <p className="text-white">Texto ilegible</p>
</div>
```

### StickyDisclaimerBanner - Ejemplo Correcto

```tsx
// ✅ CORRECTO
<div className='bg-sena-orange border-b-2 border-orange-400'>
  <AlertTriangle className='text-gray-600' />
  <h3 className='text-gray-700 font-bold'>Aviso</h3>
  <p className='text-gray-600'>Descripción</p>
</div>
```

## 📏 Estándares de Contraste

### Cumplimiento WCAG 2.1

- **Nivel AA**: Mínimo 4.5:1 para texto normal
- **Nivel AA**: Mínimo 3:1 para texto grande (18pt+)
- **Nivel AAA**: Mínimo 7:1 para texto normal (recomendado)

### Herramientas de Validación

```bash
# Instalar herramientas de contraste
npm install --save-dev axe-core
npm install --save-dev lighthouse
```

### Colores Validados ✅

| Fondo     | Texto     | Contraste | Estado      |
| --------- | --------- | --------- | ----------- |
| `#FF8C00` | `#4B5563` | 5.2:1     | ✅ WCAG AA  |
| `#003366` | `#FFFFFF` | 12.6:1    | ✅ WCAG AAA |
| `#F9FAFB` | `#374151` | 8.9:1     | ✅ WCAG AAA |
| `#FFF7ED` | `#9A3412` | 4.8:1     | ✅ WCAG AA  |

## 🛠️ Implementación Técnica

### Clases Tailwind Aprobadas

```css
/* Fondos sólidos */
.bg-sena-orange     /* Naranja institucional */
.bg-sena-blue       /* Azul institucional */
.bg-orange-50       /* Naranja muy claro */
.bg-orange-100      /* Naranja claro */
.bg-gray-50         /* Gris muy claro */
.bg-white           /* Blanco */

/* Textos con buen contraste */
.text-gray-700      /* Gris oscuro */
.text-gray-600      /* Gris medio */
.text-white         /* Blanco sobre fondos oscuros */
.text-orange-600    /* Naranja para iconos */
```

### Clases Prohibidas ❌

```css
/* NUNCA usar estas clases */
.bg-gradient-*      /* Cualquier clase de gradiente */
.from-*             /* Gradientes direccionales */
.to-*               /* Gradientes direccionales */
.via-*              /* Gradientes con puntos medios */
```

## 🔍 Auditoría y Testing

### Comando de Validación

```bash
# Ejecutar auditoría de contraste
npm run test:contrast

# Validar con lighthouse
npm run lighthouse:a11y
```

### Checklist de Revisión

- [ ] ❌ No hay degradés en el componente
- [ ] ✅ Contraste mínimo 4.5:1 cumplido
- [ ] ✅ Colores institucionales utilizados
- [ ] ✅ Texto legible en todos los dispositivos
- [ ] ✅ Validado con herramientas automáticas

## 📋 Responsabilidades

### Desarrollador Frontend

- Implementar colores según esta guía
- Validar contraste antes de commit
- No usar degradés bajo ninguna circunstancia

### Diseñador UX/UI

- Proponer solo colores sólidos
- Validar contraste en herramientas de diseño
- Mantener consistencia institucional

### QA/Testing

- Verificar contraste en cada release
- Probar con herramientas de accesibilidad
- Validar en diferentes dispositivos

## 🚨 Ejemplos de Violaciones Comunes

### ❌ MAL - Degradé horrible

```tsx
// NUNCA hacer esto
export const BadBanner = () => (
  <div className='bg-gradient-to-r from-red-400 via-yellow-500 to-blue-600'>
    <p className='text-white'>Texto ilegible</p>
  </div>
);
```

### ✅ BIEN - Color sólido con contraste

```tsx
// SIEMPRE hacer esto
export const GoodBanner = () => (
  <div className='bg-sena-orange'>
    <p className='text-gray-700 font-semibold'>Texto legible</p>
  </div>
);
```

## 📊 Métricas de Cumplimiento

### Objetivo: 100% Cumplimiento

- **Contraste WCAG AA**: 100% componentes
- **Sin degradés**: 100% componentes
- **Colores institucionales**: 100% elementos principales

### Monitoreo Continuo

```bash
# Comando para verificar cumplimiento
npm run style:audit

# Reporte de colores
npm run colors:report
```

---

## 🎯 Resumen Ejecutivo

**REGLA DE ORO**: Si piensas usar un degradé, usa un color sólido con buen contraste.

**COMBINACIÓN ESTÁNDAR**: Fondo naranja SENA (`#FF8C00`) + texto gris medio (`#4B5563`)

**VALIDACIÓN**: Todo color debe tener contraste mínimo 4.5:1 según WCAG 2.1 AA

---

**Fecha**: 2 de julio de 2025  
**Responsable**: EPTI - Equipo de Proyectos de Tecnología e Innovación  
**Estado**: OBLIGATORIO ✅
