# 🎨 Sistema de Design Tokens SENA

## 📋 Descripción

Este documento describe el sistema completo de design tokens implementado para SICORA, siguiendo las directrices institucionales del SENA y proporcionando consistencia visual en toda la aplicación.

---

## 🎯 **TOKENS DE ESPACIADO**

### **📏 Espaciado Base (sena-xs a sena-8xl)**

```css
/* Espaciado micro - Para componentes internos */
.space-sena-xs    /* 4px  - Espacios muy pequeños */
.space-sena-sm    /* 8px  - Entre elementos relacionados */
.space-sena-md    /* 12px - Espaciado medio */
.space-sena-lg    /* 16px - Espaciado estándar */
.space-sena-xl    /* 20px - Entre secciones */
.space-sena-2xl   /* 24px - Separación de módulos */
.space-sena-3xl   /* 32px - Separación grande */
.space-sena-4xl   /* 40px - Espaciado muy grande */
.space-sena-5xl   /* 48px - Separación de páginas */
.space-sena-6xl   /* 64px - Separación máxima */
.space-sena-7xl   /* 80px - Espacios especiales */
.space-sena-8xl   /* 96px - Hero sections */
```

### **🏗️ Espaciado Funcional**

```css
/* Layout principal */
.h-sena-header-height      /* 64px - Altura header */
.h-sena-footer-height      /* 48px - Altura footer */
.w-sena-sidebar-width      /* 256px - Ancho sidebar */
.w-sena-sidebar-collapsed  /* 64px - Sidebar colapsado */

/* Contenido */
.p-sena-content-padding    /* 32px - Padding contenido */
.p-sena-container-padding  /* 24px - Padding contenedor */
.gap-sena-section-gap      /* 48px - Gap entre secciones */
.gap-sena-module-gap       /* 24px - Gap entre módulos */

/* Componentes */
.px-sena-button-padding-x  /* 16px - Padding horizontal botones */
.py-sena-button-padding-y  /* 8px  - Padding vertical botones */
.px-sena-input-padding-x   /* 12px - Padding horizontal inputs */
.py-sena-input-padding-y   /* 8px  - Padding vertical inputs */
.p-sena-card-padding       /* 24px - Padding interno cards */
.p-sena-modal-padding      /* 32px - Padding interno modales */
```

### **💡 Ejemplos de Uso**

```tsx
// ✅ Espaciado entre elementos relacionados
<div className="space-y-sena-sm">
  <label>Nombre</label>
  <input />
</div>

// ✅ Separación entre secciones
<div className="space-y-sena-section-gap">
  <section>Información Personal</section>
  <section>Información Académica</section>
</div>

// ✅ Padding estándar en cards
<div className="p-sena-card-padding bg-white rounded-sena-card">
  <h3>Título Card</h3>
  <p>Contenido...</p>
</div>
```

---

## 📐 **TOKENS DE SIZING**

### **📱 Anchos (Width)**

```css
/* Layout */
.w-sena-sidebar            /* 256px - Sidebar estándar */
.w-sena-sidebar-collapsed  /* 64px  - Sidebar colapsado */
.w-sena-sidebar-wide       /* 320px - Sidebar amplio */

/* Contenido */
.w-sena-content-max        /* 1200px - Ancho máximo contenido */
.w-sena-content-narrow     /* 800px  - Contenido estrecho */
.w-sena-content-wide       /* 1400px - Contenido amplio */

/* Formularios */
.w-sena-form-xs            /* 256px - Formularios extra pequeños */
.w-sena-form-sm            /* 320px - Formularios pequeños */
.w-sena-form-md            /* 448px - Formularios medianos */
.w-sena-form-lg            /* 576px - Formularios grandes */
.w-sena-form-xl            /* 768px - Formularios extra grandes */

/* Componentes */
.w-sena-button-sm          /* 96px  - Botones pequeños */
.w-sena-button-md          /* 128px - Botones medianos */
.w-sena-button-lg          /* 192px - Botones grandes */
.w-sena-modal-sm           /* 448px - Modales pequeños */
.w-sena-modal-md           /* 512px - Modales medianos */
.w-sena-modal-lg           /* 768px - Modales grandes */
```

### **📏 Alturas (Height)**

```css
/* Layout */
.h-sena-header             /* 64px  - Altura header estándar */
.h-sena-header-compact     /* 48px  - Header compacto */
.h-sena-footer             /* 48px  - Altura footer */
.h-sena-navbar             /* 56px  - Altura navbar */

/* Secciones */
.h-sena-hero               /* 320px - Sección hero */
.h-sena-hero-sm            /* 256px - Hero pequeño */
.h-sena-hero-lg            /* 384px - Hero grande */

/* Componentes */
.h-sena-button             /* 40px - Botones estándar */
.h-sena-button-sm          /* 32px - Botones pequeños */
.h-sena-button-lg          /* 48px - Botones grandes */
.h-sena-input              /* 40px - Inputs estándar */
.h-sena-card               /* 192px - Cards estándar */
```

### **🔄 Límites (Min/Max)**

```css
/* Anchos mínimos */
.min-w-sena-button         /* 96px  - Ancho mínimo botones */
.min-w-sena-input          /* 192px - Ancho mínimo inputs */
.min-w-sena-card           /* 256px - Ancho mínimo cards */

/* Anchos máximos */
.max-w-sena-container      /* 1200px - Contenedor principal */
.max-w-sena-content        /* 800px  - Contenido de texto */
.max-w-sena-form           /* 600px  - Formularios */
.max-w-sena-modal          /* 90vw   - Modales responsive */

/* Alturas funcionales */
.h-sena-viewport           /* 100vh - Altura completa viewport */
.h-sena-content            /* calc(100vh - 7rem) - Viewport menos header/footer */
.max-h-sena-modal          /* 90vh  - Altura máxima modales */
```

---

## 🎨 **TOKENS DE BORDES Y SOMBRAS**

### **🔲 Border Radius**

```css
.rounded-sena-none         /* 0px   - Sin radius */
.rounded-sena-xs           /* 2px   - Elementos muy pequeños */
.rounded-sena-sm           /* 4px   - Elementos pequeños */
.rounded-sena-md           /* 6px   - Elementos medianos (estándar) */
.rounded-sena-lg           /* 8px   - Elementos grandes */
.rounded-sena-xl           /* 12px  - Elementos extra grandes */
.rounded-sena-2xl          /* 16px  - Elementos muy grandes */

/* Específicos por componente */
.rounded-sena-button       /* 6px   - Botones estándar */
.rounded-sena-input        /* 6px   - Inputs */
.rounded-sena-card         /* 8px   - Cards */
.rounded-sena-modal        /* 12px  - Modales */
.rounded-sena-badge        /* 9999px - Badges circulares */
.rounded-sena-avatar       /* 9999px - Avatares circulares */
```

### **💫 Box Shadow**

```css
/* Sombras sutiles */
.shadow-sena-xs            /* Sombra muy sutil */
.shadow-sena-sm            /* Sombra pequeña */
.shadow-sena-md            /* Sombra mediana */
.shadow-sena-lg            /* Sombra grande */
.shadow-sena-xl            /* Sombra extra grande */

/* Sombras específicas para componentes */
.shadow-sena-card          /* Sombra para cards con tinte verde SENA */
.shadow-sena-header        /* Sombra para headers */
.shadow-sena-modal         /* Sombra para modales */

/* Sombras con color SENA */
.shadow-sena-primary       /* Sombra con color verde SENA */
.shadow-sena-secondary     /* Sombra con color naranja SENA */
```

---

## 🔢 **TOKENS DE Z-INDEX**

```css
.z-sena-base              /* 0    - Nivel base */
.z-sena-dropdown          /* 1000 - Dropdowns */
.z-sena-sticky            /* 1020 - Elementos sticky */
.z-sena-fixed             /* 1030 - Elementos fixed */
.z-sena-modal-backdrop    /* 1040 - Backdrop de modales */
.z-sena-modal             /* 1050 - Modales */
.z-sena-popover           /* 1060 - Popovers */
.z-sena-tooltip           /* 1070 - Tooltips */
.z-sena-toast             /* 1080 - Notificaciones toast */
.z-sena-loading           /* 1090 - Indicadores de carga */
.z-sena-max               /* 9999 - Nivel máximo */
```

---

## 🎭 **TOKENS DE ANIMACIÓN**

```css
/* Animaciones predefinidas */
.animate-sena-fade-in      /* Fade in suave */
.animate-sena-slide-up     /* Slide hacia arriba */
.animate-sena-slide-down   /* Slide hacia abajo */
.animate-sena-scale-in     /* Scale in suave */
.animate-sena-bounce-soft  /* Bounce suave */

/* Duraciones */
.duration-sena-duration-fast    /* 150ms - Transiciones rápidas */
.duration-sena-duration-normal  /* 300ms - Transiciones normales */
.duration-sena-duration-slow    /* 500ms - Transiciones lentas */

/* Timing functions */
.ease-sena-ease-out        /* Cubic bezier para salidas suaves */
.ease-sena-ease-in-out     /* Cubic bezier para transiciones */
```

---

## 📝 **GUÍAS DE USO**

### **✅ Buenas Prácticas**

1. **Consistencia**: Usar siempre tokens en lugar de valores hardcodeados
2. **Espaciado**: Seguir la escala de espaciado establecida
3. **Componentes**: Usar tokens específicos para cada tipo de componente
4. **Responsive**: Los tokens funcionan en todos los breakpoints

### **📱 Ejemplos Completos**

```tsx
// ✅ Card estándar SENA
<div className="w-sena-card-md h-sena-card p-sena-card-padding rounded-sena-card shadow-sena-card bg-white">
  <h3 className="text-sena-lg font-sena-heading text-sena-primary-700 mb-sena-sm">
    Título de Card
  </h3>
  <p className="text-sena-base text-sena-neutral-600 leading-relaxed">
    Contenido de la card siguiendo el sistema de design tokens SENA.
  </p>
  <div className="flex justify-between items-center mt-sena-lg">
    <button className="px-sena-button-padding-x py-sena-button-padding-y rounded-sena-button bg-sena-neutral-200 text-sena-neutral-700">
      Cancelar
    </button>
    <button className="min-w-sena-button px-sena-button-padding-x py-sena-button-padding-y rounded-sena-button bg-sena-primary-500 text-white shadow-sena-primary">
      Confirmar
    </button>
  </div>
</div>

// ✅ Formulario estándar SENA
<form className="max-w-sena-form mx-auto space-y-sena-lg p-sena-modal-padding">
  <div className="space-y-sena-sm">
    <label className="text-sena-sm font-sena-body text-sena-neutral-700">
      Nombre completo
    </label>
    <input
      className="w-full h-sena-input px-sena-input-padding-x py-sena-input-padding-y rounded-sena-input border border-sena-neutral-300 focus:border-sena-primary-500"
      type="text"
    />
  </div>

  <div className="flex justify-end space-x-sena-md mt-sena-section-gap">
    <button className="px-sena-button-padding-x py-sena-button-padding-y rounded-sena-button border border-sena-neutral-300">
      Cancelar
    </button>
    <button className="min-w-sena-button px-sena-button-padding-x py-sena-button-padding-y rounded-sena-button bg-sena-primary-500 text-white">
      Guardar
    </button>
  </div>
</form>

// ✅ Layout principal con sidebar
<div className="flex h-sena-viewport">
  <aside className="w-sena-sidebar bg-sena-neutral-50 border-r border-sena-neutral-200">
    <nav className="p-sena-content-padding space-y-sena-md">
      {/* Navegación */}
    </nav>
  </aside>

  <main className="flex-1 flex flex-col">
    <header className="h-sena-header bg-white shadow-sena-header px-sena-container-padding flex items-center">
      {/* Header content */}
    </header>

    <div className="flex-1 p-sena-content-padding space-y-sena-section-gap">
      {/* Main content */}
    </div>
  </main>
</div>
```

### **🚫 Evitar**

```tsx
// ❌ NO usar valores hardcodeados
<div className="p-4 m-2 w-64 h-32 rounded-lg shadow-md">

// ✅ SÍ usar tokens
<div className="p-sena-card-padding m-sena-sm w-sena-card-md h-sena-card rounded-sena-card shadow-sena-card">
```

---

## 🔄 **MIGRACIÓN Y COMPATIBILIDAD**

### **Legacy Support**

Los tokens legacy (`sena-space-1`, `sena-space-2`, etc.) se mantienen para compatibilidad pero se recomienda migrar a los nuevos tokens:

```tsx
// ❌ Legacy (funciona pero deprecado)
<div className="p-sena-space-4 m-sena-space-2">

// ✅ Nuevo sistema (recomendado)
<div className="p-sena-lg m-sena-sm">
```

### **Migración Gradual**

1. **Fase 1**: Usar nuevos tokens en componentes nuevos
2. **Fase 2**: Migrar componentes existentes gradualmente
3. **Fase 3**: Eliminar tokens legacy después de migración completa

---

✅ **Sistema de Design Tokens SENA completamente implementado y listo para uso en producción**
