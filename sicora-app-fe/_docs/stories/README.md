# Historias de Usuario - SICORA Frontend

Este directorio contiene las historias de usuario para el desarrollo del frontend de SICORA.

## 📁 Estructura

- **`fe/`** - Historias de usuario específicas del frontend
- **`be/`** - Historias de usuario locales del frontend (específicas para componentes)
- **`be-backend/`** - 🔗 **Enlace simbólico** a las historias de usuario del backend

## 🔗 Sincronización con Backend

El directorio `be-backend/` es un **enlace simbólico** que apunta directamente a:

```
/home/epti/Documentos/epti-dev/asiste-app/fast-rn/sicora-app-be-multistack/_docs/stories/be
```

### Ventajas de esta configuración:

1. **Sincronización automática** - Siempre tenemos la información más actualizada del backend
2. **Consistencia** - Evita duplicación y desincronización de documentación
3. **Referencia directa** - Podemos consultar criterios de aceptación y historias de usuario del backend sin cambiar de proyecto
4. **Desarrollo eficiente** - Facilita el mapeo entre funcionalidades backend y frontend

### Archivos principales disponibles:

- `historias_usuario_be.md` - Historias de usuario principales del UserService
- `historias_usuario_be_multistack.md` - Historias de usuario completas del ecosistema
- `criterios_aceptacion_be.md` - Criterios de aceptación detallados
- `criterios_aceptacion_be_multistack.md` - Criterios del ecosistema completo

## 🔄 Mantenimiento

El enlace simbólico se mantiene automáticamente. Si el backend se mueve de ubicación, solo hay que actualizar el enlace:

```bash
cd _docs/stories
rm be-backend
ln -sf "/nueva/ruta/al/backend/_docs/stories/be" ./be-backend
```

## 📋 Uso en Desarrollo

Al desarrollar componentes frontend, siempre consultar:

1. **`be-backend/historias_usuario_be.md`** - Para entender los requisitos del backend
2. **`fe/`** - Para historias específicas de UI/UX
3. **`be/`** - Para componentes que no tienen equivalente directo en backend

---

**Configurado el:** 23 de junio de 2025  
**Última verificación:** ✅ Enlace activo y funcional
