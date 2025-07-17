# 🎨 Guías de UX/UI Institucional SENA

**Sistema de Información de Coordinación Académica - CGMLTI SENA**

---

## 🎯 **OBJETIVO**

Establecer las pautas de experiencia de usuario y interfaz que garantizan coherencia visual y usabilidad alineadas con la identidad institucional del SENA, asegurando una experiencia profesional y accesible.

---

## 🔲 **PATRONES DE BOTONES**

### **Jerarquía Visual**

#### **Botón Primario**

- **Color**: `bg-sena-primary` (Verde institucional #39A900)
- **Uso**: Acción principal de cada contexto
- **Posición**: Siempre a la derecha en formularios
- **Máximo**: Un botón primario por pantalla

```tsx
<Button variant='primary' size='default'>
  Guardar Usuario
</Button>
```

#### **Botón Secundario**

- **Color**: `bg-sena-secondary` (Naranja institucional #FF8C00)
- **Uso**: Acciones importantes pero no principales
- **Posición**: A la izquierda del botón primario

```tsx
<Button variant='secondary' size='default'>
  Vista Previa
</Button>
```

#### **Botón Terciario/Outline**

- **Color**: `border-sena-primary` con texto `text-sena-primary`
- **Uso**: Acciones alternativas (Cancelar, Volver)
- **Posición**: Extrema izquierda

```tsx
<Button variant='outline' size='default'>
  Cancelar
</Button>
```

#### **Botones de Estado**

- **Success**: Verde para confirmaciones
- **Warning**: Ámbar para advertencias
- **Danger**: Rojo para acciones destructivas

### **Tamaños Estandarizados**

| Tamaño    | Altura | Padding | Uso                          |
| --------- | ------ | ------- | ---------------------------- |
| `sm`      | 32px   | 12px    | Acciones en listas, toolbars |
| `default` | 40px   | 16px    | Formularios estándar         |
| `lg`      | 48px   | 32px    | CTAs principales             |
| `xl`      | 56px   | 40px    | Landing pages, dashboards    |

### **Espaciado Entre Botones**

- **Horizontal**: `gap-sena-spacing-sm` (8px) entre botones relacionados
- **Grupos**: `gap-sena-spacing-md` (16px) entre grupos de botones
- **Separación**: `gap-sena-spacing-lg` (24px) para botones no relacionados

---

## 📋 **PATRONES DE FORMULARIOS**

### **Estructura Estándar**

```
[Título del Formulario]
[Breadcrumb Navigation]

[Campo 1]
[Campo 2]
...
[Campo N]

[Botón Cancelar]    [Botón Guardar]
                    (siempre a la derecha)
```

### **Validaciones Visuales**

#### **Estados de Campo**

- **Normal**: `border-gray-300`
- **Focus**: `border-sena-primary ring-sena-primary/20`
- **Error**: `border-red-500 ring-red-500/20`
- **Success**: `border-green-500 ring-green-500/20`
- **Disabled**: `bg-gray-50 border-gray-200`

#### **Mensajes de Validación**

- **Error**: Texto rojo debajo del campo con ícono
- **Ayuda**: Texto gris claro debajo del campo
- **Requerido**: Asterisco rojo en el label

### **Agrupación de Campos**

```tsx
<fieldset className='space-y-6'>
  <legend className='text-lg font-semibold text-gray-900'>
    Información Personal
  </legend>

  <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
    {/* Campos del grupo */}
  </div>
</fieldset>
```

---

## 📊 **PATRONES DE LISTAS Y TABLAS**

### **Estructura de Lista**

```
[Título + Contador]     [Botón Crear Nuevo]
[Filtros y Búsqueda]
[------------------]
[Lista/Tabla de Datos]
[Paginación]
```

### **Acciones por Fila**

- **Posición**: Siempre en la columna más a la derecha
- **Orden**: Ver, Editar, Eliminar (de izquierda a derecha)
- **Espaciado**: `gap-2` entre acciones

```tsx
<ButtonGroupActions>
  <Button variant='ghost' size='sm'>
    <EyeIcon className='h-4 w-4' />
  </Button>
  <Button variant='ghost' size='sm'>
    <PencilIcon className='h-4 w-4' />
  </Button>
  <Button variant='ghost' size='sm'>
    <TrashIcon className='h-4 w-4' />
  </Button>
</ButtonGroupActions>
```

### **Estados de Fila**

- **Normal**: `bg-white`
- **Hover**: `hover:bg-gray-50`
- **Seleccionada**: `bg-sena-light/20`
- **Deshabilitada**: `opacity-50`

---

## 🎯 **PATRONES DE NAVEGACIÓN**

### **Breadcrumb Institucional**

- **Separador**: `/` o `>` en color `text-gray-400`
- **Página actual**: Sin enlace, `text-gray-900 font-medium`
- **Enlaces**: `text-sena-primary hover:text-sena-primary/80`

### **Menú de Usuario**

- **Posición**: Esquina superior derecha
- **Elementos**: Avatar + Nombre + Rol + Dropdown
- **Orden del dropdown**: Perfil, Configuración, Cerrar Sesión

### **Navegación Principal**

- **Logo**: Esquina superior izquierda
- **Menú**: Horizontal debajo del header
- **Indicador activo**: `border-b-2 border-sena-primary`

---

## 🎨 **JERARQUÍA VISUAL**

### **Tipografía**

| Elemento         | Clase                                 | Uso                     |
| ---------------- | ------------------------------------- | ----------------------- |
| Título Principal | `text-3xl font-bold text-gray-900`    | H1 de páginas           |
| Título Sección   | `text-xl font-semibold text-gray-900` | H2 de secciones         |
| Subtítulo        | `text-lg font-medium text-gray-700`   | H3, campos de grupo     |
| Texto Normal     | `text-base text-gray-600`             | Párrafos, descripciones |
| Texto Pequeño    | `text-sm text-gray-500`               | Metadatos, ayudas       |

### **Espaciado Vertical**

```tsx
// Entre secciones principales
className = 'space-y-8';

// Entre elementos relacionados
className = 'space-y-4';

// Entre elementos del mismo grupo
className = 'space-y-2';
```

### **Colores de Estado**

| Estado      | Color            | Uso            |
| ----------- | ---------------- | -------------- |
| Éxito       | `text-green-600` | Confirmaciones |
| Advertencia | `text-amber-600` | Alertas        |
| Error       | `text-red-600`   | Errores        |
| Información | `text-blue-600`  | Tips, ayudas   |
| Neutral     | `text-gray-600`  | Texto general  |

---

## 📱 **RESPONSIVIDAD**

### **Breakpoints SENA**

```tsx
// Mobile First
'sm': '640px',   // Tabletas pequeñas
'md': '768px',   // Tabletas
'lg': '1024px',  // Laptops
'xl': '1280px',  // Escritorio
'2xl': '1536px'  // Pantallas grandes
```

### **Patrones Responsive**

#### **Formularios**

```tsx
// Móvil: 1 columna
// Tablet+: 2 columnas
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
```

#### **Botones**

```tsx
// Móvil: Stack vertical con botón primario arriba
// Desktop: Horizontal con botón primario a la derecha
<div className="flex flex-col-reverse sm:flex-row sm:justify-between gap-4">
```

#### **Navegación**

```tsx
// Móvil: Menú hamburguesa
// Desktop: Menú horizontal
<nav className="hidden md:flex space-x-8">
```

---

## ♿ **ACCESIBILIDAD**

### **Requisitos Mínimos**

1. **Contraste**: Mínimo 4.5:1 para texto normal
2. **Focus**: Indicadores visibles en todos los elementos interactivos
3. **Keyboard**: Navegación completa por teclado
4. **Screen Readers**: ARIAq labels y roles apropiados
5. **Tamaños**: Mínimo 44px para elementos táctiles

### **Implementación**

```tsx
// Botones accesibles
<Button
  aria-label="Editar usuario Juan Pérez"
  className="focus:ring-2 focus:ring-sena-primary"
>

// Formularios accesibles
<label htmlFor="email" className="sr-only">
  Correo electrónico
</label>
<input
  id="email"
  aria-describedby="email-help"
  aria-invalid={hasError}
/>
```

---

## 🔍 **CASOS DE USO ESPECÍFICOS**

### **Página de Login**

- Logo centrado
- Formulario simple (2 campos + botón)
- Enlace "Olvidé mi contraseña" debajo
- Footer con información institucional

### **Dashboard**

- Saludo personalizado arriba izquierda
- Estadísticas en cards
- Acceso rápido a funciones principales
- Botón de acción principal esquina superior derecha

### **CRUD de Usuarios**

- Lista con filtros superiores
- Botón "Crear Usuario" esquina superior derecha
- Acciones por fila alineadas a la derecha
- Modal/página para crear/editar

### **Formularios Complejos**

- Dividir en secciones lógicas
- Progress stepper para formularios largos
- Guardar progreso automáticamente
- Validación en tiempo real

---

## ✅ **CHECKLIST DE IMPLEMENTACIÓN**

### **Antes de Desarrollar**

- [ ] Definir la jerarquía de botones en la pantalla
- [ ] Identificar estados posibles de cada elemento
- [ ] Planear el comportamiento responsive
- [ ] Revisar requisitos de accesibilidad

### **Durante el Desarrollo**

- [ ] Usar componentes base establecidos
- [ ] Aplicar design tokens consistentemente
- [ ] Implementar estados de loading/error
- [ ] Validar en diferentes tamaños de pantalla

### **Antes de Deploy**

- [ ] Test de contraste de colores
- [ ] Test de navegación por teclado
- [ ] Test en screen readers
- [ ] Test responsive en dispositivos reales

---

_Documento actualizado: Julio 2025_  
_Versión: 1.0_  
_Estado: Implementado en Fase 1.3_
