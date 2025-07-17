# SICORA - Estrategia Mobile-First con React Vite

## 📱 **Paradigma Web-First: De React Native a React Vite**

### **Contexto del Cambio**

El proyecto SICORA ha migrado de **React Native** a **React Vite** para adoptar un enfoque **Web-First** que mantiene la filosofía mobile-first pero aprovecha las ventajas del desarrollo web moderno.

### **¿Por qué Web-First para SICORA?**

Cuando hablamos de web-first en el contexto de SICORA, estamos adoptando una filosofía donde:

1. **Accesibilidad Universal**: Funciona en cualquier dispositivo con navegador
2. **Distribución Simplificada**: No requiere instalación desde tiendas de aplicaciones
3. **Actualizaciones Instantáneas**: Los cambios se despliegan inmediatamente
4. **Compatibilidad Multiplataforma**: Un solo código base para todos los dispositivos
5. **PWA Capabilities**: Funcionalidades nativas a través de Progressive Web App

### **El Instructor en el Aula: Caso de Uso Principal**

Piensa en el instructor tomando asistencia en un salón de clases:

- Está de pie, posiblemente moviéndose entre escritorios
- Usa un celular o tablet (navegador web)
- Tal vez con una mano ocupada sosteniendo papeles
- Necesita conectividad online/offline
- Requiere interfaz táctil optimizada

Esta es la experiencia más desafiante de SICORA, pero también la más importante. Si diseñamos para este escenario primero, el resto de las experiencias (administrador en escritorio, estudiante consultando horarios) se beneficiarán automáticamente.

## 🎨 **Integración con Identidad SENA**

### **Colores Corporativos Optimizados para Mobile**

Adaptando la paleta oficial del SENA para uso web responsive:

```javascript
// tailwind.config.js - Colores SENA con optimización mobile
export default {
  theme: {
    extend: {
      colors: {
        sena: {
          // Verde oficial SENA - HEX: #39A900
          primary: '#39A900',
          'primary-dark': '#2d7a00',
          'primary-light': '#4bc209',

          // Colores secundarios oficiales
          secondary: {
            'verde-oscuro': '#1a4d1a',
            violeta: '#6b46c1',
            'azul-claro': '#3b82f6',
            'azul-oscuro': '#1e3a8a',
            amarillo: '#fbbf24',
          },

          // Colores neutros oficiales
          neutral: {
            50: '#f9fafb',
            100: '#f3f4f6',
            500: '#6b7280',
            900: '#111827',
          },

          // Estados con alto contraste para mobile
          success: '#059669', // Verde fuerte para acciones positivas
          warning: '#d97706', // Naranja para advertencias
          danger: '#dc2626', // Rojo para errores
          'touch-bg': '#f8fafc', // Fondo para áreas táctiles
        },
      },
    },
  },
};
```

### **Tipografía Corporativa Responsive**

Implementando Work Sans (principal) y Calibri (secundaria) según manual SENA:

```css
/* Tipografía SENA optimizada para web mobile-first */
@import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700&display=swap');

:root {
  /* Work Sans - Tipografía principal SENA */
  --font-primary: 'Work Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  /* Calibri fallback para sistemas que no la tengan */
  --font-secondary: 'Calibri', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Mobile-first: tamaños base más grandes para legibilidad */
.text-base {
  font-size: 16px;
  line-height: 24px;
} /* Base móvil más grande */
.text-lg {
  font-size: 18px;
  line-height: 28px;
} /* Para headers móviles */
.text-xl {
  font-size: 20px;
  line-height: 32px;
} /* Para títulos móviles */

/* Desktop: refinamiento de tamaños */
@media (min-width: 768px) {
  .text-base {
    font-size: 14px;
    line-height: 20px;
  }
  .text-lg {
    font-size: 16px;
    line-height: 24px;
  }
  .text-xl {
    font-size: 18px;
    line-height: 28px;
  }
}
```

## 🏗️ **Configuración Base: Vite + TailwindCSS + SENA**

### **vite.config.ts Actualizado**

```typescript
// vite.config.ts - Optimizado para PWA y mobile-first
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/sicora\.api\.sena\.edu\.co\/api\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'sicora-api-cache',
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24, // 24 horas
              },
            },
          },
        ],
      },
      manifest: {
        name: 'SICORA - Sistema de Control de Asistencia SENA',
        short_name: 'SICORA',
        description:
          'Control de asistencia para instructores y estudiantes SENA',
        theme_color: '#39A900', // Verde oficial SENA
        background_color: '#ffffff',
        display: 'standalone',
        orientation: 'portrait-primary',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
    }),
  ],
  resolve: {
    alias: {
      '@': './src',
      '@components': './src/components',
      '@hooks': './src/hooks',
      '@utils': './src/utils',
      '@types': './src/types',
    },
  },
});
```

### **tailwind.config.js Completo**

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    // Mobile-first: definimos primero para móviles, luego expandimos
    screens: {
      sm: '640px', // tablet pequeña
      md: '768px', // tablet
      lg: '1024px', // laptop
      xl: '1280px', // desktop
      '2xl': '1536px', // desktop grande
    },
    // Fuentes oficiales SENA
    fontFamily: {
      sans: ['Work Sans', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      secondary: [
        'Calibri',
        '-apple-system',
        'BlinkMacSystemFont',
        'sans-serif',
      ],
    },
    extend: {
      // Espaciado optimizado para touch según estándares móviles
      spacing: {
        touch: '44px', // Tamaño mínimo iOS/Android guidelines
        'safe-top': 'env(safe-area-inset-top)',
        'safe-bottom': 'env(safe-area-inset-bottom)',
      },
      // Tipografía escalable mobile-first
      fontSize: {
        xs: ['12px', { lineHeight: '16px' }],
        sm: ['14px', { lineHeight: '20px' }],
        base: ['16px', { lineHeight: '24px' }], // Base móvil más grande
        lg: ['18px', { lineHeight: '28px' }],
        xl: ['20px', { lineHeight: '32px' }],
        '2xl': ['24px', { lineHeight: '36px' }],
      },
      // Colores oficiales SENA + optimizaciones mobile
      colors: {
        sena: {
          // Verde oficial SENA - HEX: #39A900
          primary: '#39A900',
          'primary-dark': '#2d7a00',
          'primary-light': '#4bc209',

          // Colores secundarios oficiales del manual
          secondary: {
            'verde-oscuro': '#1a4d1a',
            violeta: '#6b46c1',
            'azul-claro': '#3b82f6',
            'azul-oscuro': '#1e3a8a',
            amarillo: '#fbbf24',
          },

          // Estados con alto contraste para mobile
          success: '#059669',
          warning: '#d97706',
          danger: '#dc2626',
          'touch-bg': '#f8fafc',

          // Grises neutros del manual
          neutral: {
            50: '#f9fafb',
            100: '#f3f4f6',
            200: '#e5e7eb',
            300: '#d1d5db',
            400: '#9ca3af',
            500: '#6b7280',
            600: '#4b5563',
            700: '#374151',
            800: '#1f2937',
            900: '#111827',
          },
        },
      },
      // Animaciones optimizadas para mobile
      transitionProperty: {
        touch: 'transform, background-color, border-color, opacity',
      },
      // Sombras con mejor performance en mobile
      boxShadow: {
        touch: '0 2px 8px rgba(0, 0, 0, 0.1)',
        elevated: '0 4px 16px rgba(0, 0, 0, 0.15)',
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
};
```

// ============================================================================
// 2. HOOK PERSONALIZADO: DETECCIÓN Y GESTIÓN DE VIEWPORT
// ============================================================================

// src/hooks/useViewport.js
import { useState, useEffect } from 'react';

/\*\*

- Hook para gestionar responsive behavior y adaptarse al contexto de uso
- Especialmente importante para SICORA donde el contexto cambia dramáticamente
- entre instructor-en-aula vs admin-en-oficina
  \*/
  export const useViewport = () => {
  const [viewport, setViewport] = useState({
  width: window.innerWidth,
  height: window.innerHeight,
  isMobile: window.innerWidth < 768,
  isTablet: window.innerWidth >= 768 && window.innerWidth < 1024,
  isDesktop: window.innerWidth >= 1024,
  orientation: window.innerWidth > window.innerHeight ? 'landscape' : 'portrait'
  });

useEffect(() => {
const handleResize = () => {
const width = window.innerWidth;
const height = window.innerHeight;

      setViewport({
        width,
        height,
        isMobile: width < 768,
        isTablet: width >= 768 && width < 1024,
        isDesktop: width >= 1024,
        orientation: width > height ? 'landscape' : 'portrait'
      });
    };

    // Throttle resize events para performance
    let timeoutId;
    const throttledResize = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(handleResize, 100);
    };

    window.addEventListener('resize', throttledResize);
    return () => {
      window.removeEventListener('resize', throttledResize);
      clearTimeout(timeoutId);
    };

}, []);

// Métodos de utilidad para diferentes contextos de SICORA
const getOptimalColumns = () => {
if (viewport.isMobile) return 1;
if (viewport.isTablet) return 2;
return 3;
};

const getAttendanceCardSize = () => {
// Para mobile: tarjetas más grandes, fáciles de tocar
if (viewport.isMobile) return 'large';
if (viewport.isTablet) return 'medium';
return 'compact';
};

const shouldUseDrawerNavigation = () => {
// En móvil, usamos drawer. En desktop, sidebar fijo
return viewport.isMobile || viewport.isTablet;
};

return {
...viewport,
getOptimalColumns,
getAttendanceCardSize,
shouldUseDrawerNavigation
};
};

// ============================================================================
// 3. COMPONENTE BASE: TOUCH-OPTIMIZED BUTTON
// ============================================================================

// src/components/atoms/TouchButton/TouchButton.jsx
import React from 'react';
import { cn } from '../../../utils/classNames';

/\*\*

- Botón optimizado para interacción táctil
- Diseñado primero para el instructor usando celular en el aula
  \*/
  export const TouchButton = ({
  children,
  variant = 'primary',
  size = 'touch', // Por defecto: tamaño táctil
  disabled = false,
  loading = false,
  onClick,
  className,
  ...props
  }) => {

const baseStyles = cn(
// Base: Optimizado para touch desde el inicio
'inline-flex items-center justify-center rounded-lg font-medium',
'transition-all duration-200 ease-in-out',
// Touch feedback crucial para mobile
'active:scale-95 active:transition-none',
// Accessibility para keyboard navigation
'focus:outline-none focus:ring-2 focus:ring-offset-2',
// Estados disabled
'disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100'
);

// Variantes con colores de alto contraste para uso móvil
const variants = {
primary: cn(
'bg-sicora-primary text-white shadow-lg',
'hover:bg-blue-700 active:bg-blue-800',
'focus:ring-blue-500'
),
success: cn(
'bg-sicora-success text-white shadow-lg',
'hover:bg-green-700 active:bg-green-800',
'focus:ring-green-500'
),
danger: cn(
'bg-sicora-danger text-white shadow-lg',
'hover:bg-red-700 active:bg-red-800',
'focus:ring-red-500'
),
secondary: cn(
'bg-white text-gray-700 border-2 border-gray-300 shadow-sm',
'hover:bg-gray-50 active:bg-gray-100',
'focus:ring-gray-500'
)
};

// Tamaños optimizados para diferentes contextos
const sizes = {
// Touch: Tamaño mínimo 44px como recomienda Apple/Google
touch: 'min-h-touch px-6 py-3 text-base min-w-touch',
// Large: Para acciones primarias en móvil
large: 'min-h-12 px-8 py-4 text-lg min-w-32',
// Medium: Para tablets y acciones secundarias
medium: 'min-h-10 px-4 py-2 text-base min-w-24',
// Small: Solo para desktop y acciones terciarias
small: 'min-h-8 px-3 py-1.5 text-sm min-w-16',
// Full width: Para formularios móviles
full: 'w-full min-h-touch px-6 py-3 text-base'
};

return (
<button
type="button"
disabled={disabled || loading}
onClick={onClick}
className={cn(
baseStyles,
variants[variant],
sizes[size],
className
)}
// Asegurar que el área táctil sea suficiente
style={{ minHeight: '44px', minWidth: '44px' }}
{...props} >
{loading && (
<svg 
          className="animate-spin -ml-1 mr-2 h-5 w-5" 
          fill="none" 
          viewBox="0 0 24 24"
        >
<circle 
            className="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4"
          />
<path 
            className="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
</svg>
)}
{children}
</button>
);
};

// ============================================================================
// 4. COMPONENTE: MOBILE-FIRST INPUT CON VALIDACIÓN VISUAL
// ============================================================================

// src/components/atoms/TouchInput/TouchInput.jsx
export const TouchInput = ({
label,
error,
helper,
required = false,
type = 'text',
className,
...props
}) => {
const inputId = `input-${Math.random().toString(36).substr(2, 9)}`;

return (

<div className={cn('space-y-2', className)}>
{label && (
<label 
          htmlFor={inputId}
          className="block text-base font-medium text-gray-900"
        >
{label}
{required && <span className="text-red-500 ml-1">\*</span>}
</label>
)}

      <input
        id={inputId}
        type={type}
        className={cn(
          // Base: Optimizado para touch desde móvil
          'block w-full rounded-lg shadow-sm',
          // Tamaño mínimo para mobile touch
          'min-h-touch px-4 py-3',
          // Tipografía legible en móvil
          'text-base placeholder-gray-400',
          // Bordes y estados
          'border-2 border-gray-300',
          'focus:border-sicora-primary focus:ring-2 focus:ring-sicora-primary focus:ring-opacity-20',
          // Estados de error con alta visibilidad
          error && 'border-red-500 focus:border-red-500 focus:ring-red-500 focus:ring-opacity-20',
          // Estados disabled
          'disabled:bg-gray-50 disabled:text-gray-500 disabled:border-gray-200'
        )}
        {...props}
      />

      {helper && !error && (
        <p className="text-sm text-gray-600">{helper}</p>
      )}

      {error && (
        <p className="text-sm text-red-600 font-medium">{error}</p>
      )}
    </div>

);
};

// ============================================================================
// 5. ORGANISMO: LISTA DE ASISTENCIA MOBILE-FIRST
// ============================================================================

// src/components/organisms/MobileAttendanceList/MobileAttendanceList.jsx
import { useState } from 'react';
import { useViewport } from '../../../hooks/useViewport';

export const MobileAttendanceList = ({
students,
onToggleAttendance,
readonly = false
}) => {
const { isMobile, isTablet, getAttendanceCardSize } = useViewport();
const [searchTerm, setSearchTerm] = useState('');

// Filtrar estudiantes basado en búsqueda
const filteredStudents = students.filter(student =>
`${student.firstName} ${student.lastName} ${student.document}`
.toLowerCase()
.includes(searchTerm.toLowerCase())
);

// Componente de tarjeta de estudiante optimizado para mobile
const StudentCard = ({ student, onToggle }) => (

<div className={cn(
'bg-white rounded-lg border-2 border-gray-200 shadow-sm',
// Mobile-first: más padding, elementos más grandes
'p-4 space-y-3',
// Responsive: ajustar en pantallas más grandes
'md:p-3 md:space-y-2'
)}>
<div className="flex items-start justify-between">
{/_ Info del estudiante _/}
<div className="flex-1 min-w-0">
<h3 className="font-semibold text-gray-900 text-base leading-tight">
{student.firstName} {student.lastName}
</h3>
<p className="text-sm text-gray-600 mt-1">
Doc: {student.document}
</p>
{student.email && (
<p className="text-xs text-gray-500 mt-1 truncate">
{student.email}
</p>
)}
</div>

        {/* Avatar */}
        <div className="flex-shrink-0 ml-3">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-sm">
              {student.firstName?.[0]}{student.lastName?.[0]}
            </span>
          </div>
        </div>
      </div>

      {/* Controles de asistencia */}
      {!readonly && (
        <div className="flex gap-2 pt-2 border-t border-gray-100">
          <TouchButton
            variant="success"
            size={isMobile ? "touch" : "medium"}
            onClick={() => onToggle(student.id, true)}
            className="flex-1"
          >
            ✓ Presente
          </TouchButton>
          <TouchButton
            variant="danger"
            size={isMobile ? "touch" : "medium"}
            onClick={() => onToggle(student.id, false)}
            className="flex-1"
          >
            ✗ Ausente
          </TouchButton>
        </div>
      )}

      {/* Estado de asistencia (solo lectura) */}
      {readonly && student.attendance && (
        <div className="pt-2 border-t border-gray-100">
          <span className={cn(
            'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium',
            student.attendance.present
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          )}>
            {student.attendance.present ? '✓ Presente' : '✗ Ausente'}
          </span>
        </div>
      )}
    </div>

);

return (

<div className="space-y-4">
{/_ Header con búsqueda - Mobile optimized _/}
<div className="space-y-3">
<h2 className="text-xl font-bold text-gray-900">
Lista de Asistencia
</h2>

        {/* Búsqueda con tamaño touch-friendly */}
        <TouchInput
          type="search"
          placeholder="Buscar por nombre o documento..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full"
        />

        {/* Stats rápidas */}
        <div className="flex justify-between text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
          <span>Total: {filteredStudents.length}</span>
          <span>Mostrando: {filteredStudents.length} estudiantes</span>
        </div>
      </div>

      {/* Lista de estudiantes */}
      <div className={cn(
        'space-y-3',
        // En tablet/desktop: grid para aprovechar espacio
        'md:grid md:gap-4 md:space-y-0',
        'md:grid-cols-2 lg:grid-cols-3'
      )}>
        {filteredStudents.map(student => (
          <StudentCard
            key={student.id}
            student={student}
            onToggle={onToggleAttendance}
          />
        ))}
      </div>

      {/* Empty state */}
      {filteredStudents.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 text-4xl mb-4">🔍</div>
          <p className="text-gray-600">
            No se encontraron estudiantes con "{searchTerm}"
          </p>
        </div>
      )}
    </div>

);
};

// ============================================================================
// 6. LAYOUT: ADAPTIVE NAVIGATION
// ============================================================================

// src/components/templates/AdaptiveLayout/AdaptiveLayout.jsx
import { useState } from 'react';

export const AdaptiveLayout = ({ children, title, user }) => {
const { shouldUseDrawerNavigation, isMobile } = useViewport();
const [isDrawerOpen, setIsDrawerOpen] = useState(false);

// Componente de navegación que se adapta al viewport
const Navigation = () => (

<nav className={cn(
'bg-white border-r border-gray-200',
// Mobile: drawer overlay
shouldUseDrawerNavigation && [
'fixed inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 ease-in-out',
isDrawerOpen ? 'translate-x-0' : '-translate-x-full'
],
// Desktop: sidebar fijo
!shouldUseDrawerNavigation && 'w-64 flex-shrink-0'
)}>
<div className="h-full flex flex-col">
{/_ Header de navegación _/}
<div className="p-4 border-b border-gray-200">
<h2 className="font-bold text-lg text-gray-900">SICORA</h2>
<p className="text-sm text-gray-600">{user?.role}</p>
</div>

        {/* Enlaces de navegación optimizados para touch */}
        <div className="flex-1 p-4 space-y-2">
          {[
            { label: 'Dashboard', icon: '🏠', href: '/dashboard' },
            { label: 'Asistencia', icon: '✓', href: '/attendance' },
            { label: 'Horarios', icon: '📅', href: '/schedule' },
            { label: 'Perfil', icon: '👤', href: '/profile' }
          ].map(item => (
            <a
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center space-x-3 px-3 py-3 rounded-lg',
                'text-gray-700 hover:bg-gray-100 active:bg-gray-200',
                'transition-colors duration-150',
                // Touch-friendly sizing
                'min-h-touch'
              )}
              onClick={() => setIsDrawerOpen(false)}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </a>
          ))}
        </div>
      </div>
    </nav>

);

return (

<div className="flex h-screen bg-gray-50">
{/_ Overlay para mobile drawer _/}
{shouldUseDrawerNavigation && isDrawerOpen && (
<div
className="fixed inset-0 z-40 bg-black bg-opacity-50"
onClick={() => setIsDrawerOpen(false)}
/>
)}

      {/* Navegación */}
      <Navigation />

      {/* Contenido principal */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header móvil */}
        <header className={cn(
          'bg-white border-b border-gray-200 p-4',
          'flex items-center justify-between'
        )}>
          {/* Menu button para mobile */}
          {shouldUseDrawerNavigation && (
            <TouchButton
              variant="secondary"
              size="touch"
              onClick={() => setIsDrawerOpen(true)}
              className="mr-3"
            >
              ☰
            </TouchButton>
          )}

          <h1 className="text-lg font-semibold text-gray-900 truncate">
            {title}
          </h1>

          {/* User info */}
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600 hidden sm:block">
              {user?.firstName}
            </span>
            <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-medium">
                {user?.firstName?.[0]}
              </span>
            </div>
          </div>
        </header>

        {/* Contenido con scroll */}
        <main className="flex-1 overflow-auto">
          <div className={cn(
            'p-4 max-w-full',
            // Desktop: más padding y ancho máximo
            'lg:p-6 lg:max-w-6xl lg:mx-auto'
          )}>
            {children}
          </div>
        </main>
      </div>
    </div>

);
};

// ============================================================================
// 7. PÁGINA COMPLETA: REGISTRO DE ASISTENCIA MOBILE-FIRST
// ============================================================================

// src/pages/AttendancePage.jsx
export const AttendancePage = () => {
const { user } = useAuth();
const { isMobile } = useViewport();
const [students, setStudents] = useState([]);
const [loading, setLoading] = useState(true);
const [saving, setSaving] = useState(false);

const handleToggleAttendance = async (studentId, isPresent) => {
try {
// Optimistic update para mejor UX móvil
setStudents(prev => prev.map(student =>
student.id === studentId
? { ...student, attendance: { present: isPresent } }
: student
));

      // Llamada a API
      await attendanceService.toggleAttendance(studentId, isPresent);
    } catch (error) {
      console.error('Error toggling attendance:', error);
      // Revertir en caso de error
      loadStudents();
    }

};

const handleSaveAll = async () => {
setSaving(true);
try {
const attendanceData = students
.filter(s => s.attendance)
.map(s => ({
studentId: s.id,
present: s.attendance.present,
timestamp: new Date().toISOString()
}));

      await attendanceService.saveAttendance(attendanceData);

      // Feedback táctil en móvil
      if (navigator.vibrate) {
        navigator.vibrate(100);
      }
    } catch (error) {
      console.error('Error saving attendance:', error);
    } finally {
      setSaving(false);
    }

};

return (
<AdaptiveLayout title="Registro de Asistencia" user={user}>

<div className="space-y-4">
{/_ Actions header _/}
<div className={cn(
'flex gap-3',
// Mobile: stack buttons
'flex-col sm:flex-row sm:justify-between sm:items-center'
)}>
<div>
<h2 className="text-lg font-semibold text-gray-900">
Ficha 2826503 - ADSO
</h2>
<p className="text-sm text-gray-600">
{new Date().toLocaleDateString('es-CO', {
weekday: 'long',
year: 'numeric',
month: 'long',
day: 'numeric'
})}
</p>
</div>

          <TouchButton
            variant="primary"
            size={isMobile ? "full" : "touch"}
            onClick={handleSaveAll}
            loading={saving}
          >
            {saving ? 'Guardando...' : 'Guardar Asistencia'}
          </TouchButton>
        </div>

        {/* Lista de estudiantes */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-gray-500">Cargando estudiantes...</div>
          </div>
        ) : (
          <MobileAttendanceList
            students={students}
            onToggleAttendance={handleToggleAttendance}
          />
        )}
      </div>
    </AdaptiveLayout>

);
};

// ============================================================================
// 8. CONFIGURACIÓN: SERVICE WORKER PARA PWA
// ============================================================================

// public/sw.js - Service Worker para funcionalidad offline
self.addEventListener('install', event => {
event.waitUntil(
caches.open('sicora-v1').then(cache => {
return cache.addAll([
'/',
'/static/css/main.css',
'/static/js/main.js',
'/manifest.json'
]);
})
);
});

self.addEventListener('fetch', event => {
// Cache-first strategy para assets estáticos
if (event.request.destination === 'style' ||
event.request.destination === 'script') {
event.respondWith(
caches.match(event.request).then(response => {
return response || fetch(event.request);
})
);
}

// Network-first para API calls
if (event.request.url.includes('/api/')) {
event.respondWith(
fetch(event.request).catch(() => {
return caches.match(event.request);
})
);
}
});

// ============================================================================
// BENEFICIOS DE ESTE ENFOQUE MOBILE-FIRST PARA SICORA
// ============================================================================

/\*

1. EXPERIENCIA ÓPTIMA PARA EL CASO DE USO CRÍTICO:
   - Instructores pueden tomar asistencia eficientemente en móvil
   - Touch targets de tamaño adecuado (44px mínimo)
   - Contraste alto para visibilidad exterior
   - Feedback táctil y visual inmediato

2. PROGRESSIVE ENHANCEMENT:
   - La experiencia básica funciona en cualquier dispositivo
   - Features adicionales se agregan en pantallas más grandes
   - No hay funcionalidad "perdida" en móvil

3. PERFORMANCE OPTIMIZADA:
   - CSS mobile-first es más eficiente
   - Menos overrides y especificidad
   - Carga más rápida en dispositivos móviles

4. ACCESIBILIDAD MEJORADA:
   - Tamaños touch-friendly benefician a todos
   - Contraste alto ayuda en múltiples contextos
   - Navegación simplificada es más intuitiva

5. DESARROLLO SIMPLIFICADO:
   - Una sola base de código para todos los dispositivos
   - Testing más directo (empezar por móvil)
   - Menos bugs de responsive design

6. VALOR EDUCATIVO:
   - Demuestra mejores prácticas modernas
   - Enseña pensamiento mobile-first
   - Muestra cómo construir PWAs efectivas
     \*/

---

## 🏗️ **Integración con Estrategia Híbrida de Atomic Design**

### **Alineación Perfecta: Mobile-First + Atomic Design Selectivo**

La estrategia móvil-primero de SICORA se alinea perfectamente con la **estrategia híbrida de Atomic Design** documentada en [ADR-004](../technical/ARCHITECTURAL-DECISIONS.md#adr-004-estrategia-híbrida-de-atomic-design):

#### **Átomos Mobile-Optimized**

```typescript
// Los átomos DEBEN ser touch-friendly desde el diseño inicial
TouchButton:  min-height: 44px, optimized feedback
TouchInput:   min-height: 44px, large tap targets
StatusBadge:  high contrast colors, large text
LoadingSpinner: visible on all backgrounds
```

#### **Moléculas Responsive**

```typescript
// Las moléculas adaptan su layout según viewport
UserCard:     vertical en mobile, horizontal en desktop
LoginForm:    full-width en mobile, constrained en desktop
SearchInput:  overlay en mobile, inline en desktop
```

#### **Organismos Context-Aware**

```typescript
// Los organismos conocen su contexto de uso
MobileAttendanceList: optimized para instructor-en-aula
AdaptiveNavigation:   drawer en mobile, sidebar en desktop
DashboardHeader:      collapsed en mobile, full en desktop
```

### **Componentes NO-Atomic que Siguen Mobile-First**

Los componentes que NO están en atomic design (en `/features/` y `/pages/`) **también** deben seguir mobile-first:

```typescript
// features/attendance/AttendanceFilters.tsx
export const AttendanceFilters = () => {
  const { isMobile } = useViewport();

  return (
    <div className={cn(
      // Mobile-first: stack filters vertically
      'space-y-3',
      // Desktop: horizontal layout
      'md:flex md:space-y-0 md:space-x-4'
    )}>
      {/* Filters content */}
    </div>
  );
};
```

### **Criterios Duales: Mobile-First + Reutilización**

Un componente entra en Atomic Design si cumple:

1. **Criterios de Reutilización** (del ADR-004), Y
2. **Criterios Mobile-First**:
   - ✅ Requiere optimización táctil específica
   - ✅ Necesita comportamiento adaptivo móvil/desktop
   - ✅ Tiene interacciones complejas en mobile
   - ✅ Maneja estados críticos para UX móvil

### **Exclusiones Específicas Mobile-First**

Componentes que NO entran en Atomic Design aunque sean mobile-friendly:

❌ **Gestos específicos** de una pantalla (SwipeToRefresh específico)  
❌ **Overlays únicos** (OnboardingOverlay)  
❌ **Animaciones específicas** de transición entre pantallas  
❌ **Funcionalidades PWA** específicas (InstallPrompt)

---

## 📱 **Cumplimiento Estricto: Manual de Identidad SENA 2024**

### **Integración Obligatoria con Identidad Corporativa**

Todo el desarrollo frontend de SICORA cumple **estrictamente** con el [Manual de Identidad Visual SENA 2024](../general/manual_imagen_corporativa_sena.md):

#### **Paleta de Colores Obligatoria**

```css
/* Variables CSS que DEBEN usarse en todos los componentes */
:root {
  /* Verde institucional SENA - USO OBLIGATORIO para acciones primarias */
  --sena-verde-principal: #39a900;
  --sena-verde-oscuro: #2d7a00;
  --sena-verde-claro: #4bc209;

  /* Colores secundarios oficiales del manual */
  --sena-violeta: #6b46c1;
  --sena-azul-claro: #3b82f6;
  --sena-azul-oscuro: #1e3a8a;
  --sena-amarillo: #fbbf24;
}
```

#### **Tipografía Corporativa Obligatoria**

```css
/* Fuentes oficiales SENA según manual 2024 */
.font-sena-primary {
  font-family:
    'Work Sans',
    -apple-system,
    BlinkMacSystemFont,
    sans-serif;
  /* USO: Títulos, botones, elementos importantes */
}

.font-sena-secondary {
  font-family:
    'Calibri',
    -apple-system,
    BlinkMacSystemFont,
    sans-serif;
  /* USO: Texto corrido, descripciones, contenido general */
}
```

#### **Aplicación en Componentes Atomic Design**

```typescript
// Átomos DEBEN usar colores SENA obligatorios
const TouchButton = ({ variant = 'primary' }) => {
  const baseStyles = 'font-sena-primary font-medium';

  const variants = {
    primary: 'bg-sena-verde-principal text-white', // OBLIGATORIO
    secondary: 'border-2 border-sena-verde-principal text-sena-verde-principal',
    danger: 'bg-red-600 text-white', // Permitido para errores
  };

  return (
    <button className={cn(baseStyles, variants[variant])}>
      {children}
    </button>
  );
};
```

#### **Restricciones del Manual Aplicadas**

##### **✅ PERMITIDO**

- Verde #39A900 para acciones primarias y navegación
- Colores secundarios oficiales para categorización
- Work Sans para elementos interactivos
- Calibri para contenido textual
- Logo SENA en header (posición superior izquierda)

##### **❌ PROHIBIDO**

- Modificar el verde institucional (#39A900)
- Usar logos no oficiales o versiones alteradas
- Combinar Work Sans con otras fuentes no autorizadas
- Usar el logo SENA sobre fondos de bajo contraste
- Aplicar efectos (sombras, degradados) al logo oficial

#### **Validación Automática de Identidad**

```typescript
// utils/senaCompliance.ts - Validación automática
export const validateSenaCompliance = (component: React.ComponentType) => {
  const issues = [];

  // Verificar colores permitidos
  if (usesUnauthorizedColors(component)) {
    issues.push('Uses colors not approved in SENA manual 2024');
  }

  // Verificar tipografía
  if (usesUnauthorizedFonts(component)) {
    issues.push('Uses fonts not specified in SENA manual 2024');
  }

  // Verificar uso correcto del logo
  if (misusesLogo(component)) {
    issues.push('Incorrect logo usage according to SENA guidelines');
  }

  return { compliant: issues.length === 0, issues };
};
```

### **Documentación de Cumplimiento**

Cada componente en Atomic Design incluye:

```typescript
/**
 * TouchButton - Botón optimizado para mobile con identidad SENA
 *
 * CUMPLIMIENTO SENA 2024:
 * ✅ Verde institucional #39A900 para variant="primary"
 * ✅ Tipografía Work Sans según manual
 * ✅ Contraste mínimo 4.5:1 para accesibilidad
 * ✅ Respeta restricciones de uso de colores corporativos
 *
 * @see /docs/general/manual_imagen_corporativa_sena.md
 */
export const TouchButton = ({ variant = 'primary', ...props }) => {
  // Implementation with SENA compliance
};
```

---

## 🎯 **Resumen Ejecutivo: Triple Alineación**

SICORA implementa una **triple alineación** estratégica:

### **1. Mobile-First (ADR Base)**

- Diseño desde móvil hacia desktop
- Touch targets de 44px mínimo
- Optimización para instructor-en-aula

### **2. Atomic Design Híbrido (ADR-004)**

- Solo componentes que justifican la abstracción
- Máximo valor, mínimo overhead
- Enfoque pragmático sobre dogmático

### **3. Identidad SENA Estricta (Manual 2024)**

- Cumplimiento obligatorio de colores corporativos
- Tipografía oficial Work Sans + Calibri
- Restricciones de logo y aplicaciones digitales

### **Resultado: Sistema Cohesivo y Escalable**

Esta triple alineación produce:

- ✅ **Experiencia móvil óptima** para el caso de uso crítico
- ✅ **Consistencia visual** a través de componentes reutilizables
- ✅ **Identidad corporativa** coherente con estándares SENA
- ✅ **Desarrollo eficiente** sin overhead innecesario
- ✅ **Escalabilidad** orgánica según necesidades reales

---

## 📄 **Referencias y Documentación Relacionada**

- **[ADR-004: Estrategia Híbrida de Atomic Design](../technical/ARCHITECTURAL-DECISIONS.md#adr-004)**
- **[Guía de Implementación Atomic Design Híbrido](../technical/atomic-design-hybrid-guide.md)**
- **[Manual de Identidad Visual SENA 2024](../general/manual_imagen_corporativa_sena.md)**
- **[Configuración Vite + TailwindCSS + PWA](../../vite.config.ts)**

---

**✋ IMPORTANTE: No crear componentes hasta recibir "next->"**

La documentación está completa y el proyecto configurado. Los componentes se implementarán siguiendo esta estrategia una vez se reciba la instrucción específica para proceder con la fase de implementación.
