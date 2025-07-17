# Archivos de Ejemplo para SICORA Data Loader

Esta carpeta contiene archivos de ejemplo para probar la funcionalidad del Data Loader.

## 📁 Archivos Disponibles

### `users_sample.csv`

Archivo CSV con datos de usuarios de ejemplo:

- **Campos**: name, email, document_number, role, active
- **Registros**: 5 usuarios de muestra
- **Uso**: Probar carga en UserService → users table

### `usuarios_ejemplo.xlsx` (Crear manualmente)

Archivo Excel con datos de usuarios:

- **Hoja**: Usuarios
- **Campos**: Nombre, Correo, Documento, Rol, Activo
- **Uso**: Probar mapeo automático de columnas

### `asistencia_ejemplo.xlsx` (Crear manualmente)

Archivo Excel con datos de asistencia:

- **Hoja**: Asistencia
- **Campos**: user_id, fecha, entrada, salida, estado
- **Uso**: Probar carga en AttendanceService → attendance_records

## 🧪 Cómo Crear Archivos de Prueba

### Excel de Usuarios

```
Nombre              | Correo                    | Documento | Rol        | Activo
Juan Pérez         | juan.perez@sena.edu.co    | 12345678  | instructor | TRUE
María García       | maria.garcia@sena.edu.co  | 87654321  | student    | TRUE
Carlos López       | carlos.lopez@sena.edu.co  | 11223344  | admin      | TRUE
```

### Excel de Asistencia

```
user_id | fecha      | entrada  | salida   | estado
1       | 2025-01-15 | 08:00:00 | 17:00:00 | presente
2       | 2025-01-15 | 08:05:00 | 16:45:00 | presente
3       | 2025-01-15 | 08:10:00 | 17:15:00 | presente
```

## 📋 Casos de Prueba

1. **Carga Normal**: Usar users_sample.csv para UserService
2. **Mapeo de Columnas**: Usar usuarios_ejemplo.xlsx (columnas en español)
3. **Validación de Errores**: Modificar archivos para incluir datos inválidos
4. **Carga Masiva**: Crear archivos con 1000+ registros

## 🚀 Instrucciones de Uso

1. Abrir SICORA Data Loader
2. Seleccionar microservicio apropiado
3. Seleccionar tabla destino
4. Cargar archivo de ejemplo
5. Seguir el flujo de validación y carga

---

_Archivos de ejemplo para facilitar pruebas del Data Loader_
