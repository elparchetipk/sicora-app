# 🚀 SHARED-DATA - QUICK START

**Setup completado**: dom 15 jun 2025 23:43:31 -05

## ✅ LISTO PARA USAR

### Estructura protegida:
- 📂 imports/ - Datos fuente (PROTEGIDO)
- 📂 templates/ - Plantillas sin datos
- 📂 exports/ - Salidas por stack (PROTEGIDO)
- 📂 samples/ - Ejemplos sintéticos (PROTEGIDO)
- 📂 schemas/ - Validación JSON

### Archivos clave:
- SECURITY-POLICY.md - Políticas de protección
- bulk-config.env - Configuración unificada
- .gitignore - Protección automática

## 🔧 USO INMEDIATO

```bash
# Desde cualquier stack (01-fastapi, 02-go, etc.)
ls ../shared-data/templates/
cp ../shared-data/templates/users.template.csv ./users.csv

# Configurar stack
../../tools/bulk-data-loader.sh setup-stack fastapi
```

## 🔒 SEGURIDAD

- ✅ Datos reales protegidos
- ✅ Solo templates y estructura en git
- ✅ Acceso restringido a stacks
- ✅ Auditoría automática

**Listo para desarrollo multistack.**
