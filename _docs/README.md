# 📚 Documentación SICORA - Índice Principal

## 🏛️ Estructura de Documentación

Esta carpeta contiene toda la documentación del proyecto SICORA organizada por temática. El archivo `README.md` principal del proyecto permanece en la raíz para mantener la información general y enlaces a esta documentación.

## 📁 Organización por Carpetas

### 📋 [**integracion/**](./integracion/)

Documentación relacionada con la integración entre servicios y componentes:

- Reportes de integración frontend-backend
- Guías de conexión entre servicios
- Estados de integración y verificaciones
- Resolución de problemas de conectividad

### 🤖 [**mcp/**](./mcp/)

Documentación del servidor MCP (Model Context Protocol):

- Guías para principiantes
- Configuración con pnpm
- Instrucciones de uso
- Checklists y troubleshooting

### ⚙️ [**configuracion/**](./configuracion/)

Documentación de configuración y setup:

- Configuraciones de entorno
- Variables de configuración
- Setup de servicios
- Configuraciones de desarrollo y producción

### 🔧 [**desarrollo/**](./desarrollo/)

Documentación para desarrolladores:

- Guías de desarrollo
- Estándares de código
- Flujos de trabajo
- Herramientas y scripts

### 📊 [**reportes/**](./reportes/)

Reportes y análisis del proyecto:

- Reportes de estado
- Análisis de rendimiento
- Métricas del proyecto
- Auditorías y evaluaciones

### 📖 [**guias/**](./guias/)

Guías generales y tutoriales:

- Guías de usuario
- Tutoriales paso a paso
- Mejores prácticas
- Casos de uso

## 🎯 Principios de Organización

### 1. **Ubicación Única**

- Solo el `README.md` principal permanece en la raíz
- Toda otra documentación se organiza en `_docs/`
- No duplicar documentación entre carpetas

### 2. **Categorización Temática**

- Cada documento va en la carpeta más apropiada
- Usar subcarpetas cuando sea necesario
- Mantener coherencia en la estructura

### 3. **Referencias Actualizadas**

- Todos los enlaces internos usan rutas relativas
- El README principal enlaza a esta documentación
- Mantener índices actualizados

### 4. **Nomenclatura Consistente**

- Usar nombres descriptivos en español
- Formato: `TITULO_DOCUMENTO.md`
- Prefijos por tipo cuando sea necesario

## 🔗 Enlaces Rápidos

### Para Desarrolladores

- [Guía de Desarrollo](./desarrollo/)
- [Configuración MCP](./mcp/)
- [Integración Frontend-Backend](./integracion/)

### Para Administradores

- [Configuración de Servicios](./configuracion/)
- [Reportes de Estado](./reportes/)
- [Guías de Despliegue](./guias/)

### Para Usuarios

- [Guías de Usuario](./guias/)
- [Tutoriales](./guias/)
- [Resolución de Problemas](./integracion/)

## 📝 Instrucciones para Mantenimiento

### Al Crear Nueva Documentación:

1. Determinar la categoría apropiada
2. Crear el archivo en la carpeta correspondiente
3. Actualizar el índice de la carpeta
4. Actualizar referencias en el README principal

### Al Mover Documentación:

1. Mover el archivo a la nueva ubicación
2. Actualizar todas las referencias
3. Verificar que los enlaces funcionen
4. Actualizar índices afectados

### Al Eliminar Documentación:

1. Verificar que no haya enlaces hacia el documento
2. Actualizar índices
3. Considerar crear redirección si es necesario

## 🚨 Nota Importante

Esta estructura debe mantenerse durante todo el desarrollo del proyecto. Los archivos de configuración de herramientas (GitHub Copilot, MCP, etc.) incluyen instrucciones específicas para preservar esta organización.

---

**Última actualización**: 3 de julio de 2025  
**Versión**: 1.0.0  
**Responsable**: Sistema de Documentación SICORA
