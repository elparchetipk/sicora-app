# 📚 Documentación Frontend SICORA

## 🎯 Organización de Documentación

Esta carpeta contiene toda la documentación específica del frontend SICORA, organizada por temáticas para facilitar la navegación y mantenimiento.

### 📁 Estructura de Carpetas

```
_docs/
├── README.md (este archivo)
├── integracion/     # Integración frontend-backend
├── configuracion/   # Configuración y setup
├── desarrollo/      # Planes y guías de desarrollo
├── reportes/        # Reportes y análisis
├── guias/          # Guías de implementación
├── diseno/         # Design tokens y UI/UX
├── general/        # Documentación general
├── api/            # Documentación de API
├── charts/         # Gráficos y visualizaciones
├── comparisons/    # Comparaciones técnicas
├── planning/       # Planificación del proyecto
├── progress/       # Progreso de desarrollo
├── reports/        # Reportes técnicos
├── stories/        # Historias de usuario
├── technical/      # Documentación técnica
└── tmp/            # Archivos temporales
```

## 📋 Categorías de Documentación

### 🔗 [Integración](./integracion/)

Documentación relacionada con la integración frontend-backend:

- Configuración de APIs
- Protocolos de comunicación
- Estados de integración
- Troubleshooting de conectividad

### ⚙️ [Configuración](./configuracion/)

Setup y configuración del entorno:

- Configuración de desarrollo
- Variables de entorno
- Setup de Hostinger
- Configuración de despliegue

### 🔧 [Desarrollo](./desarrollo/)

Guías y planes de desarrollo:

- Planes de desarrollo frontend
- Estándares de código
- Flujos de trabajo
- Herramientas de desarrollo

### 📊 [Reportes](./reportes/)

Reportes de estado y análisis:

- Estados de implementación
- Resúmenes ejecutivos
- Análisis de progreso
- Reportes de verificación

### 📖 [Guías](./guias/)

Guías de implementación y correcciones:

- Implementaciones completadas
- Guías de UI/UX
- Correcciones aplicadas
- Tutoriales paso a paso

### 🎨 [Diseño](./diseno/)

Design tokens, branding y UI/UX:

- Design tokens SENA
- Sistema de branding dual
- Guías de colores
- Patrones de UI/UX institucional

### 📄 [General](./general/)

Documentación general y miscelánea:

- Códigos de conducta
- Contribución
- Esquemas de base de datos
- Generadores de datos

## 🔍 Documentación Técnica Especializada

### 📡 [API](./api/)

Documentación de interfaces de programación

### 📈 [Charts](./charts/)

Gráficos y visualizaciones de datos

### ⚖️ [Comparisons](./comparisons/)

Comparaciones técnicas y análisis

### 📅 [Planning](./planning/)

Planificación y roadmaps del proyecto

### 🏃 [Progress](./progress/)

Seguimiento del progreso de desarrollo

### 📋 [Reports](./reports/)

Reportes técnicos y de estado

### 👥 [Stories](./stories/)

Historias de usuario y casos de uso

### 🔧 [Technical](./technical/)

Documentación técnica avanzada

## 🚀 Cómo Usar Esta Documentación

### 📖 Para Desarrolladores

1. **Empezar aquí**: Lee este README.md
2. **Configuración**: Revisa [Configuración](./configuracion/)
3. **Desarrollo**: Consulta [Desarrollo](./desarrollo/)
4. **Integración**: Verifica [Integración](./integracion/)

### 👨‍💼 Para Managers

1. **Estado general**: Revisa [Reportes](./reportes/)
2. **Progreso**: Consulta [Progress](./progress/)
3. **Planificación**: Verifica [Planning](./planning/)

### 🎨 Para Diseñadores

1. **Design system**: Revisa [Diseño](./diseno/)
2. **Guías UI/UX**: Consulta [Guías](./guias/)
3. **Branding**: Verifica tokens y patrones

## 📝 Convenciones de Documentación

### 📏 Nomenclatura

- **Archivos**: `TITULO_DOCUMENTO.md` (mayúsculas con guiones bajos)
- **Prefijos por tipo**:
  - `INTEGRACION_` - Documentación de integración
  - `CONFIGURACION_` - Configuración y setup
  - `IMPLEMENTACION_` - Implementaciones completadas
  - `GUIA_` - Guías y tutoriales
  - `REPORTE_` - Reportes y análisis
  - `ESTADO_` - Estados y resúmenes

### 📚 Estructura de Documento

```markdown
# Título del Documento

## 🎯 Objetivo

Descripción clara del propósito

## 📋 Contenido

Desarrollo del contenido

## ✅ Conclusiones

Resumen y siguientes pasos

## 📚 Referencias

Enlaces y recursos relacionados
```

### 🔗 Enlaces Internos

Usar rutas relativas:

- `[Otro documento](./categoria/DOCUMENTO.md)`
- `[Carpeta](./categoria/)`

## 🔄 Mantenimiento

### ✅ Reglas de Organización

1. **Solo README.md en la raíz** del frontend
2. **Toda documentación en `_docs/`** por categorías
3. **Actualizar índices** cuando se agregue documentación
4. **Usar nomenclatura consistente**

### 🛠️ Herramientas de Verificación

```bash
# Verificar estructura
./scripts/verify-doc-structure.sh

# Organizar archivos automáticamente
./scripts/verify-doc-structure.sh organize
```

### 📈 Actualización Regular

- Revisar enlaces rotos mensualmente
- Actualizar índices cuando sea necesario
- Archivar documentación obsoleta en `tmp/`

## 🚨 Alertas Importantes

### ⚠️ Estructura Requerida

- **PROHIBIDO**: Archivos `.md` en la raíz (excepto README.md)
- **REQUERIDO**: Toda documentación en `_docs/`
- **OBLIGATORIO**: README.md en cada subcarpeta

### 🔒 Preservación de Estructura

Esta organización se mantiene automáticamente mediante:

- Scripts de verificación
- Configuración de VS Code
- Instrucciones de Copilot
- Verificaciones de CI/CD

---

## 📊 Estadísticas de Documentación

### 📁 Archivos Organizados (Julio 2025)

- **Total archivos .md organizados**: 25+
- **Categorías creadas**: 7
- **Archivos de configuración**: 4
- **Guías de implementación**: 8
- **Reportes de integración**: 3

### 🎯 Cobertura por Categoría

| Categoría     | Archivos | Estado      |
| ------------- | -------- | ----------- |
| Integración   | 3        | ✅ Completa |
| Configuración | 2        | ✅ Completa |
| Desarrollo    | 1        | ✅ Completa |
| Reportes      | 3        | ✅ Completa |
| Guías         | 8        | ✅ Completa |
| Diseño        | 3        | ✅ Completa |
| General       | 5        | ✅ Completa |

---

_Esta documentación se actualiza automáticamente. Última actualización: Julio 2025_
