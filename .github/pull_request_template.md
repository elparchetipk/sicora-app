# Pull Request Template

## 📝 Descripción

Describe brevemente los cambios realizados en este PR.

### Tipo de Cambio

- [ ] 🐛 Bug fix (cambio que arregla un problema)
- [ ] ✨ Nueva característica (cambio que añade funcionalidad)
- [ ] 💥 Breaking change (cambio que causaría que funcionalidad existente no funcione como se esperaba)
- [ ] 📚 Documentación (mejoras o adiciones a la documentación)
- [ ] 🎨 Estilo (formateo, puntos y comas faltantes, etc.; sin cambios de código)
- [ ] ♻️ Refactoring (cambio de código que no arregla bugs ni añade características)
- [ ] ⚡ Performance (cambio que mejora el rendimiento)
- [ ] 🧪 Tests (añadir tests faltantes o corregir tests existentes)
- [ ] 🔧 Configuración (cambios en configuración, CI/CD, etc.)

## 🔗 Issue Relacionado

Fixes #(número del issue)

## 🧪 ¿Cómo se ha Probado?

Describe las pruebas que ejecutaste para verificar tus cambios.

- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Tests manuales
- [ ] Tests E2E

**Comandos de testing ejecutados:**

```bash
# Pega aquí los comandos que ejecutaste
```

## 📷 Screenshots (si aplica)

Agrega screenshots que muestren los cambios visuales.

## ✅ Checklist

### Código

- [ ] Mi código sigue las convenciones de estilo del proyecto
- [ ] He realizado una auto-revisión de mi propio código
- [ ] He comentado mi código, particularmente en áreas difíciles de entender
- [ ] He realizado los cambios correspondientes en la documentación
- [ ] Mis cambios no generan nuevas advertencias
- [ ] He añadido tests que prueban que mi fix es efectivo o que mi característica funciona
- [ ] Tests unitarios nuevos y existentes pasan localmente con mis cambios

### Documentación

- [ ] He actualizado el README si es necesario
- [ ] He actualizado la documentación en `_docs/` si es necesario
- [ ] He creado/actualizado diagramas SVG si es necesario
- [ ] He actualizado los comentarios en el código

### Git & CI/CD

- [ ] Mis commits siguen el formato de conventional commits
- [ ] He hecho rebase de mi rama con la rama principal
- [ ] No hay conflictos de merge
- [ ] Los checks de CI/CD pasan

### Bases de Datos (si aplica)

- [ ] He incluido scripts de migración necesarios
- [ ] He probado la migración en un entorno limpio
- [ ] He documentado cambios en el esquema

### Docker & Infraestructura (si aplica)

- [ ] Los contenedores se construyen correctamente
- [ ] He probado con `docker compose up`
- [ ] He actualizado variables de entorno si es necesario
- [ ] He probado health checks

## 🎓 Impacto Educativo

### ¿Cómo mejora esto la experiencia educativa?

- [ ] Facilita el aprendizaje de conceptos
- [ ] Mejora la documentación educativa
- [ ] Simplifica la configuración para estudiantes
- [ ] Añade ejemplos prácticos
- [ ] Mejora la comprensión del código
- [ ] Otro: ********\_********

### ¿Requiere actualización de materiales educativos?

- [ ] Guías de instalación
- [ ] Tutoriales existentes
- [ ] Diagramas arquitecturales
- [ ] Ejemplos de código
- [ ] Videos explicativos

## 🔧 Componentes Afectados

- [ ] Frontend (sicora-app-fe)
- [ ] Backend Go (sicora-be-go)
- [ ] Backend Python (sicora-be-python)
- [ ] Infraestructura (sicora-infra)
- [ ] MCP Server (sicora-mcp-server)
- [ ] Documentación (sicora-docs)
- [ ] Scripts y herramientas
- [ ] Configuración CI/CD

## 📊 Métricas de Rendimiento

Si es relevante, incluye métricas antes y después:

### Antes

- Tiempo de respuesta:
- Uso de memoria:
- Tamaño del bundle:

### Después

- Tiempo de respuesta:
- Uso de memoria:
- Tamaño del bundle:

## 🔄 Migración (si aplica)

### ¿Requiere pasos de migración?

- [ ] No requiere migración
- [ ] Migración automática
- [ ] Migración manual requerida

### Pasos de migración:

1. Paso 1
2. Paso 2
3. Paso 3

## 🚨 Consideraciones de Deployment

- [ ] Puede desplegarse de manera independiente
- [ ] Requiere deployment coordinado
- [ ] Requiere downtime
- [ ] Requiere feature flags

## 📝 Notas Adicionales

Cualquier información adicional que los revisores deberían saber.

---

## Para Revisores

### 🔍 Qué Revisar

- [ ] Lógica de negocio
- [ ] Seguridad
- [ ] Performance
- [ ] Calidad del código
- [ ] Tests
- [ ] Documentación
- [ ] Compatibilidad
- [ ] Accesibilidad (si aplica)

### 🎓 Para Mentores

Si estás revisando código de un estudiante:

- [ ] ¿El código es educativo y fácil de entender?
- [ ] ¿Hay oportunidades de enseñanza?
- [ ] ¿Los comentarios explican el "por qué" no solo el "qué"?
- [ ] ¿Sigue las mejores prácticas que enseñamos?

---

**¡Gracias por contribuir a SICORA!** 🎉
