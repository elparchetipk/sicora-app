# 🎨 Assets de SICORA

## 📋 Recursos Visuales

Esta carpeta contiene todos los recursos visuales y assets del proyecto SICORA.

### 🏷️ Logos

#### `logo-sicora.svg` - Logo Principal

- **Dimensiones**: 400x120px
- **Uso**: README principal, documentación destacada
- **Características**:
  - Tema dark con gradientes azul y verde
  - Incluye icono de integración (círculos conectados)
  - Texto completo "SICORA" con subtítulo
  - Badge "OneVision Open Source"

#### `logo-sicora-small.svg` - Logo Compacto

- **Dimensiones**: 200x60px
- **Uso**: Documentación interna, headers de archivos .md
- **Características**:
  - Versión compacta del logo principal
  - Mismo esquema de colores
  - Icono simplificado
  - Badge compacto "Academic System"

### 🖼️ Diagramas

#### `errores-red-docker-sicora.svg` - Diagrama de Errores Docker

- **Dimensiones**: 1200x800px
- **Uso**: Documentación de errores Docker
- **Características**:
  - Diagrama de flujo de diagnóstico
  - 4 tipos principales de errores
  - Scripts automáticos disponibles
  - Tema dark consistente

## 🎨 Guía de Estilo Visual

### Colores Principales

- **Azul Primario**: #4299e1 → #2b6cb0 (gradiente)
- **Verde Acento**: #38a169 → #2f855a (gradiente)
- **Fondo Dark**: #1a202c
- **Texto Claro**: #ffffff → #e2e8f0 (gradiente)
- **Texto Secundario**: #a0aec0

### Tipografía

- **Fuente**: Monospace (para mantener consistencia técnica)
- **Peso**: Bold para títulos, normal para texto
- **Tamaños**: Escalados según uso (32px principal, 18px compacto)

### Elementos Visuales

- **Gradientes**: Sin degradados planos, siempre con transición
- **Bordes**: Redondeados (rx="8" para logos, rx="12" para diagramas)
- **Sombras**: Sutiles con opacidad 0.3
- **Filtros**: Glow para elementos destacados

## 📐 Uso de Assets

### En README Principal

```markdown
![SICORA Logo](./assets/logo-sicora.svg)
```

### En Documentación Interna

```markdown
![SICORA Logo](../../assets/logo-sicora-small.svg)
```

### En Diagramas

```markdown
![Errores Docker](./assets/errores-red-docker-sicora.svg)
```

## 🔧 Creación de Nuevos Assets

### Requisitos para Nuevos SVGs

1. **Tema dark obligatorio** (fondo #1a202c)
2. **Sin degradados planos** (usar gradientes lineales)
3. **Esquema de colores consistente**
4. **Tipografía monospace**
5. **Elementos redondeados**
6. **Optimizados para visualización en GitHub**

### Nomenclatura

- Usar kebab-case: `nombre-asset-sicora.svg`
- Incluir "sicora" en el nombre para identificación
- Ser descriptivo: `diagrama-arquitectura-sicora.svg`

### Dimensiones Recomendadas

- **Logos principales**: 400x120px
- **Logos compactos**: 200x60px
- **Diagramas**: 1200x800px
- **Iconos**: 64x64px

## 📝 Mantenimiento

### Actualización de Logos

- Mantener versión en esquina inferior (formato: v2025.MM)
- Actualizar fecha cuando se modifique contenido
- Conservar esquema de colores existente

### Testing Visual

- Verificar visualización en GitHub (modo dark/light)
- Probar en diferentes tamaños de pantalla
- Validar legibilidad de texto

---

**Última actualización**: Agosto 2025
**Mantenido por**: Equipo SICORA OneVision
**Estilo**: Dark Theme Consistency v1.0
