import type { Config } from 'tailwindcss';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

const config: Config = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      // Colores SENA 2024
      colors: {
        sena: {
          verde: '#39a900',
          'verde-dark': '#2d7a00',
          'verde-light': '#5db025',
          naranja: '#ff7300',
          'naranja-dark': '#cc5c00',
          'naranja-light': '#ff8533',
          violeta: '#8b5fbf',
          'violeta-dark': '#6d4c93',
          'violeta-light': '#a379d1',
          azul: '#0066cc',
          'azul-dark': '#0052a3',
          'azul-light': '#3385d6',
          amarillo: '#fbbf24',
          'amarillo-dark': '#f59e0b',
          'amarillo-light': '#fcd34d',
        },
        'sena-primary': {
          50: '#f0f9e8',
          100: '#d9f0c4',
          200: '#b8e986',
          300: '#8cc73e',
          400: '#5db025',
          500: '#39a900', // Verde SENA Principal
          600: '#2d7a00',
          700: '#1e5200',
          800: '#143d00',
          900: '#0a1f00',
        },
        'sena-secondary': {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#ff7300', // Naranja SENA
          600: '#cc5c00',
          700: '#9a4500',
          800: '#7c3600',
          900: '#632900',
        },
        'sena-neutral': {
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
      // Espaciado SENA - Sistema completo de design tokens
      spacing: {
        // Espaciado micro (componentes internos)
        'sena-xs': '0.25rem', // 4px - Para espacios muy pequeños
        'sena-sm': '0.5rem', // 8px - Entre elementos relacionados
        'sena-md': '0.75rem', // 12px - Espaciado medio
        'sena-lg': '1rem', // 16px - Espaciado estándar
        'sena-xl': '1.25rem', // 20px - Entre secciones
        'sena-2xl': '1.5rem', // 24px - Separación de módulos
        'sena-3xl': '2rem', // 32px - Separación grande
        'sena-4xl': '2.5rem', // 40px - Espaciado muy grande
        'sena-5xl': '3rem', // 48px - Separación de páginas
        'sena-6xl': '4rem', // 64px - Separación máxima
        'sena-7xl': '5rem', // 80px - Espacios especiales
        'sena-8xl': '6rem', // 96px - Hero sections

        // Espaciado funcional específico SENA
        'sena-header-height': '4rem', // 64px - Altura header
        'sena-footer-height': '3rem', // 48px - Altura footer
        'sena-sidebar-width': '16rem', // 256px - Ancho sidebar
        'sena-sidebar-collapsed': '4rem', // 64px - Sidebar colapsado
        'sena-content-padding': '2rem', // 32px - Padding contenido
        'sena-container-padding': '1.5rem', // 24px - Padding contenedor
        'sena-section-gap': '3rem', // 48px - Gap entre secciones
        'sena-module-gap': '1.5rem', // 24px - Gap entre módulos

        // Espaciado de componentes específicos
        'sena-button-padding-x': '1rem', // 16px - Padding horizontal botones
        'sena-button-padding-y': '0.5rem', // 8px - Padding vertical botones
        'sena-input-padding-x': '0.75rem', // 12px - Padding horizontal inputs
        'sena-input-padding-y': '0.5rem', // 8px - Padding vertical inputs
        'sena-card-padding': '1.5rem', // 24px - Padding interno cards
        'sena-modal-padding': '2rem', // 32px - Padding interno modales

        // Legacy (mantener compatibilidad con código existente)
        'sena-space-1': '0.25rem',
        'sena-space-2': '0.5rem',
        'sena-space-3': '0.75rem',
        'sena-space-4': '1rem',
        'sena-space-6': '1.5rem',
        'sena-space-8': '2rem',
        'sena-space-12': '3rem',
        'sena-space-16': '4rem',
      },
      // Radios SENA - Sistema completo de border radius
      borderRadius: {
        'sena-none': '0',
        'sena-xs': '0.125rem', // 2px - Elementos muy pequeños
        'sena-sm': '0.25rem', // 4px - Elementos pequeños
        'sena-md': '0.375rem', // 6px - Elementos medianos (estándar)
        'sena-lg': '0.5rem', // 8px - Elementos grandes
        'sena-xl': '0.75rem', // 12px - Elementos extra grandes
        'sena-2xl': '1rem', // 16px - Elementos muy grandes
        'sena-3xl': '1.5rem', // 24px - Elementos especiales

        // Radios específicos por componente
        'sena-button': '0.375rem', // 6px - Botones estándar
        'sena-input': '0.375rem', // 6px - Inputs
        'sena-card': '0.5rem', // 8px - Cards
        'sena-modal': '0.75rem', // 12px - Modales
        'sena-badge': '9999px', // Circular - Badges
        'sena-avatar': '9999px', // Circular - Avatares

        // Radios especiales
        'sena-pill': '9999px', // Pills y badges circulares
        'sena-rounded': '50%', // Elementos completamente redondos
      },
      // Sombras SENA expandidas
      boxShadow: {
        // Sombras sutiles SENA
        'sena-xs': '0 1px 2px 0 rgb(0 0 0 / 0.03)',
        'sena-sm': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'sena-md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'sena-lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'sena-xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        'sena-2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',

        // Sombras específicas para componentes
        'sena-card': '0 4px 6px -1px rgb(57 169 0 / 0.1), 0 2px 4px -2px rgb(57 169 0 / 0.1)',
        'sena-header': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'sena-modal': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',

        // Sombras con color SENA
        'sena-primary': '0 4px 14px 0 rgb(57 169 0 / 0.15)',
        'sena-secondary': '0 4px 14px 0 rgb(255 115 0 / 0.15)',
      },
      // Dimensiones específicas SENA - Sistema completo de sizing
      width: {
        // Anchos de layout
        'sena-sidebar': '16rem', // 256px - Sidebar estándar
        'sena-sidebar-collapsed': '4rem', // 64px - Sidebar colapsado
        'sena-sidebar-wide': '20rem', // 320px - Sidebar amplio

        // Anchos de contenido
        'sena-content-max': '1200px', // Ancho máximo contenido
        'sena-content-narrow': '800px', // Contenido estrecho
        'sena-content-wide': '1400px', // Contenido amplio

        // Anchos de formularios
        'sena-form-xs': '16rem', // 256px - Formularios pequeños
        'sena-form-sm': '20rem', // 320px - Formularios pequeños
        'sena-form-md': '28rem', // 448px - Formularios medianos
        'sena-form-lg': '36rem', // 576px - Formularios grandes
        'sena-form-xl': '48rem', // 768px - Formularios extra grandes

        // Anchos de componentes
        'sena-button-sm': '6rem', // 96px - Botones pequeños
        'sena-button-md': '8rem', // 128px - Botones medianos
        'sena-button-lg': '12rem', // 192px - Botones grandes
        'sena-input-sm': '12rem', // 192px - Inputs pequeños
        'sena-input-md': '16rem', // 256px - Inputs medianos
        'sena-input-lg': '24rem', // 384px - Inputs grandes
        'sena-card-sm': '16rem', // 256px - Cards pequeñas
        'sena-card-md': '20rem', // 320px - Cards medianas
        'sena-card-lg': '24rem', // 384px - Cards grandes

        // Anchos de modal
        'sena-modal-sm': '28rem', // 448px - Modales pequeños
        'sena-modal-md': '32rem', // 512px - Modales medianos
        'sena-modal-lg': '48rem', // 768px - Modales grandes
        'sena-modal-xl': '64rem', // 1024px - Modales extra grandes
      },

      height: {
        // Alturas de layout
        'sena-header': '4rem', // 64px - Altura header estándar
        'sena-header-compact': '3rem', // 48px - Header compacto
        'sena-footer': '3rem', // 48px - Altura footer
        'sena-navbar': '3.5rem', // 56px - Altura navbar

        // Alturas de contenido
        'sena-hero': '20rem', // 320px - Sección hero
        'sena-hero-sm': '16rem', // 256px - Hero pequeño
        'sena-hero-lg': '24rem', // 384px - Hero grande
        'sena-section': '12rem', // 192px - Secciones estándar

        // Alturas de componentes
        'sena-card': '12rem', // 192px - Cards estándar
        'sena-card-sm': '8rem', // 128px - Cards pequeñas
        'sena-card-lg': '16rem', // 256px - Cards grandes
        'sena-button': '2.5rem', // 40px - Botones estándar
        'sena-button-sm': '2rem', // 32px - Botones pequeños
        'sena-button-lg': '3rem', // 48px - Botones grandes
        'sena-input': '2.5rem', // 40px - Inputs estándar
        'sena-input-sm': '2rem', // 32px - Inputs pequeños
        'sena-input-lg': '3rem', // 48px - Inputs grandes

        // Alturas funcionales
        'sena-viewport': '100vh', // Altura completa viewport
        'sena-content': 'calc(100vh - 7rem)', // Viewport menos header/footer
        'sena-scroll-area': '24rem', // 384px - Áreas con scroll
      },

      minWidth: {
        'sena-button': '6rem', // 96px - Ancho mínimo botones
        'sena-input': '12rem', // 192px - Ancho mínimo inputs
        'sena-card': '16rem', // 256px - Ancho mínimo cards
        'sena-modal': '20rem', // 320px - Ancho mínimo modales
        'sena-sidebar': '4rem', // 64px - Ancho mínimo sidebar
        'sena-content': '320px', // Ancho mínimo contenido
      },

      maxWidth: {
        // Contenedores principales
        'sena-container': '1200px', // Contenedor principal
        'sena-container-wide': '1400px', // Contenedor amplio
        'sena-container-narrow': '800px', // Contenedor estrecho

        // Contenido específico
        'sena-content': '800px', // Contenido de texto
        'sena-form': '600px', // Formularios
        'sena-modal': '90vw', // Modales responsive
        'sena-image': '100%', // Imágenes responsive

        // Breakpoints personalizados
        'sena-mobile': '480px',
        'sena-tablet': '768px',
        'sena-desktop': '1024px',
        'sena-wide': '1200px',
      },

      minHeight: {
        'sena-button': '2rem', // 32px - Altura mínima botones
        'sena-input': '2rem', // 32px - Altura mínima inputs
        'sena-card': '8rem', // 128px - Altura mínima cards
        'sena-section': '4rem', // 64px - Altura mínima secciones
        'sena-hero': '16rem', // 256px - Altura mínima hero
        'sena-content': 'calc(100vh - 7rem)', // Contenido mínimo
      },

      maxHeight: {
        'sena-modal': '90vh', // Altura máxima modales
        'sena-dropdown': '20rem', // 320px - Altura máxima dropdowns
        'sena-scroll': '24rem', // 384px - Altura máxima scroll areas
        'sena-image': '32rem', // 512px - Altura máxima imágenes
      },
      transitionDuration: {
        'sena-duration-fast': '150ms',
        'sena-duration-normal': '300ms',
        'sena-duration-slow': '500ms',
      },
      transitionTimingFunction: {
        'sena-ease-out': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'sena-ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      // Tipografía SENA - Manual de Identidad
      fontFamily: {
        'sena-primary': ['Work Sans', 'system-ui', 'sans-serif'], // Fuente principal SENA
        'sena-heading': ['Work Sans', 'system-ui', 'sans-serif'], // Para títulos
        'sena-body': ['Work Sans', 'system-ui', 'sans-serif'], // Para cuerpo de texto
        'sena-mono': ['Space Mono', 'Courier New', 'monospace'], // Para código
        'work-sans': ['Work Sans', 'system-ui', 'sans-serif'],
        'space-mono': ['Space Mono', 'Courier New', 'monospace'],
      },
      fontSize: {
        'sena-xs': ['0.75rem', { lineHeight: '1rem' }], // 12px
        'sena-sm': ['0.875rem', { lineHeight: '1.25rem' }], // 14px
        'sena-base': ['1rem', { lineHeight: '1.5rem' }], // 16px
        'sena-lg': ['1.125rem', { lineHeight: '1.75rem' }], // 18px
        'sena-xl': ['1.25rem', { lineHeight: '1.75rem' }], // 20px
        'sena-2xl': ['1.5rem', { lineHeight: '2rem' }], // 24px
        'sena-3xl': ['1.875rem', { lineHeight: '2.25rem' }], // 30px
        'sena-4xl': ['2.25rem', { lineHeight: '2.5rem' }], // 36px
      },

      // Z-index SENA - Sistema de capas
      zIndex: {
        'sena-base': '0',
        'sena-dropdown': '1000',
        'sena-sticky': '1020',
        'sena-fixed': '1030',
        'sena-modal-backdrop': '1040',
        'sena-modal': '1050',
        'sena-popover': '1060',
        'sena-tooltip': '1070',
        'sena-toast': '1080',
        'sena-loading': '1090',
        'sena-max': '9999',
      },

      // Animaciones y transiciones SENA
      animation: {
        'sena-fade-in': 'fadeIn 0.3s ease-in-out',
        'sena-slide-up': 'slideUp 0.3s ease-out',
        'sena-slide-down': 'slideDown 0.3s ease-out',
        'sena-scale-in': 'scaleIn 0.2s ease-out',
        'sena-bounce-soft': 'bounce 1s infinite',
        shimmer: 'shimmer 2s ease-in-out infinite',
        'spin-slow': 'spin 3s linear infinite',
        'spin-fast': 'spin 0.5s linear infinite',
      },

      // Keyframes para animaciones
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
  plugins: [forms, typography],
};

export default config;
