# 📋 Plan de Desarrollo Frontend SICORA

**Sistema de Información de Coordinación Académica - CGMLTI SENA**

---

## 🎯 **OBJETIVO GENERAL**

Desarrollar un frontend completo y robusto para SICORA que integre todos los microservicios del backend (Go + Python FastAPI), proporcionando una experiencia de usuario institucional alineada con el SENA y cubriendo todas las necesidades de gestión académica.

---

## 🏗️ **ARQUITECTURA FRONTEND**

### **Stack Tecnológico**

- **React 19** + **TypeScript 5.7**
- **Vite 7.0** (Build tool)
- **TailwindCSS 3.5** (Estilos)
- **React Router v6** (Navegación)
- **Zustand** (Estado global)
- **React Query/TanStack Query** (Gestión de datos server)
- **React Hook Form** + **Zod** (Formularios y validación)
- **Headless UI** + **Heroicons** (Componentes accesibles)
- **Chart.js/Recharts** (Visualización de datos)
- **pnpm** (Gestión de paquetes)

### **Estructura de Directorios**

```
src/
├── components/
│   ├── atoms/              # Componentes básicos reutilizables
│   ├── molecules/          # Componentes compuestos
│   ├── organisms/          # Componentes complejos
│   ├── templates/          # Layouts y plantillas
│   └── pages/              # Páginas completas
├── hooks/                  # Custom hooks
├── services/               # Servicios para APIs
├── stores/                 # Zustand stores
├── types/                  # Definiciones TypeScript
├── utils/                  # Utilidades y helpers
├── constants/              # Constantes globales
├── assets/                 # Imágenes, iconos, fuentes
└── styles/                 # Estilos globales
```

---

## 📊 **FASE 1: INFRAESTRUCTURA Y CORE** ✅ **COMPLETADA 95%**

**Duración: 2-3 semanas** | **Estado: 🟢 EN PROGRESO - Semana 1 Día 2**

### **🎯 Logros Conseguidos - Julio 2, 2025:**

#### **✅ Paso 1.1 - Setup Inicial y Configuración (COMPLETADO)**

- **React Router v6** configurado con BrowserRouter
- **App.tsx migrado** completamente a nueva arquitectura
- **Zustand store** implementado con gestión de usuarios
- **React Query** configurado para data fetching
- **Commits automáticos** funcionando con Husky + lint-staged
- **Calidad de código** 100% - cero errores ESLint/TypeScript
- **Sistema de rutas** institucionales funcionando
- **Infraestructura Docker** + DevContainer lista

#### **✅ Paso 1.2 - Sistema de Design Tokens (COMPLETADO)**

- [x] ~~Colores institucionales SENA en TailwindCSS~~
- [x] ~~Tipografías Work Sans configuradas~~
- [x] **Tokens de espaciado y sizing** ⭐ **COMPLETADO**
- [x] **Tokens de sombras y borders** ⭐ **COMPLETADO**
- [x] **Variables CSS personalizadas** ⭐ **COMPLETADO**
- [x] **Sistema z-index y animaciones** ⭐ **COMPLETADO**
- [x] **Documentación completa en DESIGN_TOKENS_SENA.md** ⭐ **COMPLETADO**
- [x] **Componente DesignTokensDemo con ejemplos visuales** ⭐ **COMPLETADO**

#### **✅ Paso 1.3 - Guías de UX/UI Institucional (COMPLETADO)**

- [x] **Documentación completa en GUIAS_UX_UI_INSTITUCIONAL_SENA.md** ⭐ **COMPLETADO**
- [x] **Componentes Button y ButtonGroup** con variantes SENA ⭐ **COMPLETADO**
- [x] **Jerarquía visual** (primario → secundario → terciario) ⭐ **COMPLETADO**
- [x] **Espaciado estándar** entre grupos de botones ⭐ **COMPLETADO**
- [x] **Componente UIPatternsDemoPage** con ejemplos visuales ⭐ **COMPLETADO**
- [x] **Separación buttonVariants** para react-refresh ⭐ **COMPLETADO**
- [x] **Commits automáticos activados** 🎯 **CRÍTICO COMPLETADO**

### **1.1 Setup Inicial y Configuración**

- [x] ~~Configuración de Vite + React 19 + TypeScript~~
- [x] ~~Configuración de TailwindCSS con tokens SENA~~
- [x] ~~Configuración de pnpm y estructura de proyecto~~
- [x] ~~**Setup de React Router v6** para rutas dinámicas~~
- [x] ~~**Configuración de Zustand** para estado global~~
- [x] ~~**Setup de React Query** para data fetching~~
- [x] ~~**Commits automáticos** con Husky + lint-staged~~
- [x] ~~**Migración App.tsx** a BrowserRouter + QueryClient~~
- [x] ~~**Sistema de rutas institucionales** con LayoutWrapper~~
- [x] ~~**Resolución errores ESLint/TypeScript** completa~~
- [ ] **Configuración de tests** (Vitest + Testing Library)

### **1.2 Sistema de Design Tokens SENA** ✅ **COMPLETADO**

- [x] ~~Colores institucionales SENA en TailwindCSS~~
- [x] ~~Tipografías Work Sans configuradas~~
- [x] **Tokens de espaciado y sizing** ⭐ **NUEVO**
- [x] **Tokens de sombras y borders** ⭐ **NUEVO**
- [x] **Variables CSS personalizadas** ⭐ **NUEVO**
- [x] **Sistema z-index y animaciones** ⭐ **NUEVO**
- [x] **Documentación completa en DESIGN_TOKENS_SENA.md** ⭐ **NUEVO**
- [x] **Componente DesignTokensDemo con ejemplos visuales** ⭐ **NUEVO**

### **1.3 Guías de UX/UI Institucional** ✅ **COMPLETADO**

#### **📍 REGLA FUNDAMENTAL: Posicionamiento de Botones**

**CRÍTICO**: Los botones que invitan a la acción (Call-to-Action) **SIEMPRE** deben posicionarse a la derecha.

- [x] ~~**Implementar ValidatedInput** con validaciones REGEXP~~
- [x] ~~**Crear componentes de ejemplo** ButtonPositioningDemo~~
- [x] ~~**Crear SecureFormDemo** con validaciones seguras~~
- [x] ~~**Separar hooks y constantes** según buenas prácticas~~
- [x] **Documentación completa en GUIAS_UX_UI_INSTITUCIONAL_SENA.md** ⭐ **NUEVO**
- [x] **Crear componentes Button y ButtonGroup** con posicionamiento correcto ⭐ **NUEVO**
- [x] **Establecer jerarquía visual** (primario → secundario → terciario) ⭐ **NUEVO**
- [x] **Definir espaciado estándar** entre grupos de botones ⭐ **NUEVO**
- [x] **Componente UIPatternsDemoPage** con ejemplos visuales ⭐ **NUEVO**
- [x] **Validación responsive** (mobile mantiene jerarquía) ⭐ **NUEVO**

```typescript
// ✅ PATRÓN CORRECTO - Implementar en todos los componentes
<div className="flex justify-between items-center">
  <button className="btn-secondary">Cancelar</button>
  <div className="flex space-x-3">
    <button className="btn-outline">Guardar Borrador</button>
    <button className="btn-primary">Guardar y Continuar</button>
  </div>
</div>

// ❌ NUNCA HACER - Acción principal a la izquierda
<div className="flex space-x-3">
  <button className="btn-primary">Guardar</button> {/* MAL */}
  <button className="btn-secondary">Cancelar</button>
</div>
```

#### **🎯 Jerarquía de Acciones (de derecha a izquierda)**

1. **Acción Principal** (más a la derecha) - `btn-primary`
2. **Acción Secundaria** (centro) - `btn-outline`
3. **Cancelar/Limpiar** (izquierda) - `btn-secondary`
4. **Destructiva** (separada con espacio extra) - `btn-danger`

#### **📱 Adaptación Mobile**

- [ ] **Stack vertical en mobile** manteniendo orden visual
- [ ] **Botón primario siempre prominente** (parte superior en mobile)
- [ ] **Touch targets mínimo 44px** para accesibilidad

#### **🎨 Aplicación en SICORA**

- [ ] **Formularios**: Submit/Crear siempre a la derecha
- [ ] **Modales**: Confirmar/Aceptar siempre a la derecha
- [ ] **Listas**: Acciones por fila alineadas a la derecha
- [ ] **Dashboards**: CTA principal en esquina superior derecha

### **1.4 Componentes Base Atómicos** 🎯 **PRÓXIMO OBJETIVO**

**Estado: 🔄 EN PROGRESO** | **Prioridad: ALTA**

#### **✅ Componentes Ya Completados:**

- [x] **Button** (primary, secondary, ghost, danger) ⭐ **COMPLETADO**
- [x] **ButtonGroup** (estándar, acciones) ⭐ **COMPLETADO**
- [x] **buttonVariants** (separado para react-refresh) ⭐ **COMPLETADO**
- [x] **Input** (text, email, password, search) ⭐ **COMPLETADO DÍA 1**
- [x] **TextArea** (con contador de caracteres) ⭐ **COMPLETADO DÍA 1**
- [x] **Checkbox** y **Radio** + **RadioGroup** ⭐ **COMPLETADO DÍA 1**
- [x] **Select** (Radix UI, simple/múltiple) ⭐ **COMPLETADO DÍA 2**
- [x] **Badge** (status, roles, variantes) ⭐ **COMPLETADO DÍA 2**
- [x] **Alert** (success, warning, error, info) ⭐ **COMPLETADO DÍA 2**
- [x] **Modal** y **Dialog** (Radix UI, accesible) ⭐ **COMPLETADO DÍA 3**
- [x] **Skeleton** loaders (text, card, table) ⭐ **COMPLETADO DÍA 3**
- [x] **Toast** Notifications (global, variantes) ⭐ **COMPLETADO DÍA 3**
- [x] **Spinner** y **Progress** (5 tipos, todas variantes) ⭐ **COMPLETADO DÍA 4**
- [x] **Tooltip** y **Popover** (Radix UI, accesible) ⭐ **COMPLETADO DÍA 4**
- [x] **Dropdown Menu** (menús contextuales completos) ⭐ **COMPLETADO DÍA 4**

#### **🎯 Componentes Prioritarios por Implementar:**

- [ ] **Tabs** (navegación por pestañas) 🔥 **PRIORIDAD 1**
- [ ] **Accordion** (contenido expansible) 🔥 **PRIORIDAD 1**
- [ ] **Card** (contenedores de información) 🔥 **PRIORIDAD 1**
- [ ] **Table** (tablas de datos) 🔥 **PRIORIDAD 2**
- [ ] **Pagination** (paginación) 🔥 **PRIORIDAD 2**
- [ ] **Breadcrumb** mejorado (navegación) 🔥 **PRIORIDAD 2**
- [ ] **Steps** (wizard/stepper) 🔥 **PRIORIDAD 3**
- [ ] **Calendar/DatePicker** (selección fechas) 🔥 **PRIORIDAD 3**

#### **📋 Componentes Institucionales Legacy (Ya Implementados):**

- [x] ~~LogoSena (múltiples variantes)~~
- [x] ~~**ValidatedInput** (text, email, password con REGEXP)~~
- [x] ~~**UserAvatar** con iniciales y estados~~
- [x] ~~**UserMenu** con navegación contextual~~
- [x] ~~**RoleBadge** para identificación de usuarios~~
- [x] ~~**Breadcrumb** para navegación jerárquica~~
- [x] ~~**InstitutionalHeader** completo~~
- [x] ~~**InstitutionalFooter** con información SENA~~
- [x] ~~**InstitutionalSearchBar** estilo SofiaPlus~~
- [x] ~~**Navigation** contextual por roles~~

#### **🛠️ Plan de Implementación Fase 1.4:**

**DÍA 1 (HOY):** Componentes de Formulario Base

1. **Input Component** con variantes (text, email, password, search)
2. **TextArea Component** con contador de caracteres
3. **Checkbox & Radio Components** con estados

**DÍA 2:** Componentes de Selección y Estado

1. **Select Component** (simple, múltiple, async)
2. **Badge Component** para estados y roles
3. **Alert Component** para mensajes del sistema

**DÍA 3:** Componentes de Feedback y Loading ✅ **COMPLETADO**

1. ✅ **Modal & Dialog Components** - Implementado con Radix UI
   - DialogContent con variantes (default, large, small, destructive)
   - DialogHeader, DialogFooter, DialogTitle, DialogDescription
   - Overlay con blur opcional, close button configurable
   - Accesibilidad completa y keyboard navigation

2. ✅ **Skeleton Loaders** - Estados de carga profesionales
   - Skeleton básico con variantes (default, light, dark, shimmer)
   - SkeletonText con múltiples líneas y espaciado
   - SkeletonCard con avatar e imagen opcionales
   - SkeletonTable para tablas de datos
   - Animación shimmer integrada en Tailwind

3. ✅ **Toast Notifications** - Sistema de notificaciones global
   - ToastProvider con viewport configurable
   - Variantes: default, success, warning, danger, info
   - Hook useToast para gestión global de estados
   - Acciones y auto-dismiss configurables
   - Posicionamiento responsivo (desktop/mobile)

**📋 Demo Integrada:** `/modal-skeleton-toast` - Página de demostración completa con casos de uso reales

**DÍA 4:** Componentes de Navegación e Interacción ✅ **COMPLETADO**

1. ✅ **Spinner Components** - Indicadores de carga variados
   - Spinner básico con variantes (default, primary, secondary, white, dark)
   - ProgressSpinner con porcentaje configurable y SVG circular
   - PulseSpinner con animación de pulso
   - DotsSpinner con múltiples puntos animados
   - SpinnerWithText para contexto adicional
   - Velocidades configurables (slow, default, fast)

2. ✅ **Tooltip Components** - Información contextual accesible
   - Implementado con Radix UI Tooltip para accesibilidad completa
   - SimpleTooltip para casos de uso comunes
   - IconTooltip para iconos con explicaciones
   - HelpTooltip especializado para formularios
   - Variantes: default, light, primary, secondary, success, warning, danger, info
   - Posicionamiento en 4 direcciones con arrow configurable

3. ✅ **Dropdown Menu Components** - Menús contextuales completos
   - DropdownMenu con Radix UI para accesibilidad y keyboard navigation
   - DropdownMenuItem con variantes (default, destructive, success, warning, primary, secondary)
   - DropdownMenuCheckboxItem para opciones múltiples
   - DropdownMenuRadioItem para selección única
   - DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuShortcut
   - Submenús con DropdownMenuSub y DropdownMenuSubContent
   - Variantes de tamaño y tema configurables

**📋 Demo Integrada:** `/spinner-tooltip-dropdown` - Página de demostración interactiva con casos de uso avanzados

### **🎯 FASE 1.4 COMPLETADA AL 100%** ✅

**Componentes Base Atómicos - COMPLETADO**

#### **📋 Estado de Componentes**

**✅ Día 1: Inputs y Formularios (100%)**

- [x] Input (text, email, password, number, search)
- [x] TextArea con redimensionamiento automático
- [x] Checkbox con estados y variantes
- [x] Radio y RadioGroup con validación
- [x] Validaciones REGEXP y accesibilidad

**✅ Día 2: Selects y Notificaciones (100%)**

- [x] Select con Radix UI (@radix-ui/react-select)
- [x] Badge con variantes de estado
- [x] Alert con tipos y iconos
- [x] Demos interactivas y accesibilidad

**✅ Día 3: Modals y Feedback (100%)**

- [x] Modal/Dialog (@radix-ui/react-dialog)
- [x] Skeleton Loaders con animaciones
- [x] Toast Notifications (@radix-ui/react-toast)
- [x] Hook useToast y sistema de notificaciones

**✅ Día 4: Spinners y Tooltips (100%)**

- [x] Spinner (basic, progress, pulse, dots, con texto)
- [x] Tooltip (@radix-ui/react-tooltip)
  - [x] SimpleTooltip - Uso básico
  - [x] IconTooltip - Para iconos explicativos
  - [x] HelpTooltip - Para ayuda en formularios
- [x] DropdownMenu (@radix-ui/react-dropdown-menu)
  - [x] Menús contextuales y de acciones
  - [x] Submenús y separadores
  - [x] Variantes e iconos

**🎉 Build Final Exitoso** - Sin errores TypeScript/ESLint
**🎉 Servidor Dev Activo** - http://localhost:5174/
**🎉 Demos Visuales** - Todas las páginas demo funcionando
**🎉 Commit Automatizado** - feat: completa día 4 fase 1.4 (a04bc9f)

### 📊 **RESUMEN FINAL FASE 1.4**

✅ **20+ Componentes UI Implementados**
✅ **4 Páginas Demo Interactivas**  
✅ **Sistemas de Validación REGEXP**
✅ **Infraestructura Radix UI Integrada**
✅ **Design Tokens SENA Aplicados**
✅ **Accesibilidad y UX Institucional**
✅ **Calidad de Código Garantizada**

**🚀 LISTO PARA FASE 2: AUTENTICACIÓN Y USUARIOS**

### 🔐 **PROTECCIÓN DE DATOS COMPLETADA** ✅

**Entorno de Base de Datos Sintético Configurado:**

- ✅ **Esquema EPTI ONEVISION** - Estructura idéntica al SENA pero datos ficticios
- ✅ **Base de Datos Separada** - `epti_onevision_demo` en Hostinger
- ✅ **Datos Sintéticos Generados** - 12 usuarios demo, 8 programas, 4 centros
- ✅ **Validaciones de Seguridad** - 100% emails @epti.edu.co, documentos con prefijo '99'
- ✅ **Credenciales Demo** - Password: 'password123' para todos los usuarios
- ✅ **Scripts de Importación** - SQL listo para Hostinger
- ✅ **Documentación Completa** - Esquemas, configuración y procedimientos

**Archivos Generados:**

- `database/epti_demo_data.sql` - Script de creación completo
- `database/epti_demo_data.json` - Datos estructurados
- `EPTI_DATABASE_SCHEMA.md` - Documentación del esquema
- `HOSTINGER_SETUP.md` - Guía de configuración

---

## 🔐 **FASE 2: AUTENTICACIÓN Y USUARIOS** 🎯 **FASE ACTUAL**

**Duración: 2 semanas** | **Estado: � EN DESARROLLO ACTIVO** | **Prioridad: CRÍTICA**

**📅 Inicio: Julio 2, 2025** | **🎯 Objetivo: Primera interacción real con el backend Go**

### **🚀 IMPORTANCIA ESTRATÉGICA**

Esta fase marca un **hito crítico** en el desarrollo de SICORA:

- **🔗 Primera integración Frontend ↔ Backend Go** (UserService 100% Completado)
- **🛡️ Base de seguridad** para todo el sistema
- **👥 Gestión completa de usuarios** del CGMLTI SENA
- **🗂️ Preparación para despliegue en Hostinger**

### **🏗️ ARQUITECTURA DE AUTENTICACIÓN - BACKEND GO**

#### **Backend Go UserService (100% Completado):**

- ✅ **JWT Service robusto** con claims personalizados
- ✅ **Sistema de permisos granular** (admin, coordinador, instructor, aprendiz)
- ✅ **Middleware de autenticación optimizado V2**
- ✅ **Rate limiting y security headers**
- ✅ **CRUD completo de usuarios** con operaciones masivas
- ✅ **Logging avanzado** con request ID
- ✅ **Suite de tests** (90%+ cobertura)

#### **Stack de Seguridad Frontend:**

- **JWT Tokens** (Access + Refresh) → **Backend Go JWT Service**
- **Zustand Auth Store** (estado global)
- **React Query Auth Hooks** (data fetching)
- **LocalStorage Seguro** (encriptación)
- **Route Guards** (protección de rutas)
- **RBAC** (Role-Based Access Control) → **Backend Go Permissions**

#### **Flujo de Autenticación:**

```
Frontend (React) → Backend Go API → Database (PostgreSQL)
     ↓                    ↓                      ↓
  LoginForm          Auth Middleware V2    User Verification
  JWT Storage        Token Generation      Role/Permission
  Route Guards       Refresh Logic         Session Management
```

#### **🔌 Endpoints Backend Go Disponibles:**

##### **Autenticación:**

- `POST /api/auth/login` ✅ - Login de usuario
- `POST /api/auth/refresh` ✅ - Refresco de token
- `POST /api/auth/logout` ✅ - Cerrar sesión
- `POST /api/auth/forgot-password` ✅ - Solicitar restablecimiento
- `POST /api/auth/reset-password` ✅ - Restablecer contraseña
- `POST /api/auth/change-password` ✅ - Cambio forzado de contraseña

##### **Perfil de Usuario:**

- `GET /api/profile` ✅ - Obtener perfil
- `PUT /api/profile` ✅ - Actualizar perfil
- `PUT /api/profile/password` ✅ - Cambiar contraseña

##### **Administración (Admin/Coordinador):**

- `GET /api/users` ✅ - Listar usuarios con filtros
- `GET /api/users/:id` ✅ - Obtener usuario por ID
- `POST /api/users` ✅ - Crear usuario
- `PUT /api/users/:id` ✅ - Actualizar usuario
- `DELETE /api/users/:id` ✅ - Eliminar usuario
- `PUT /api/users/:id/status` ✅ - Cambiar estado

##### **Operaciones Masivas:**

- `POST /api/users/bulk/create` ✅ - Creación masiva
- `PUT /api/users/bulk/update` ✅ - Actualización masiva
- `DELETE /api/users/bulk/delete` ✅ - Eliminación masiva
- `PUT /api/users/bulk/status` ✅ - Cambio masivo de estado

### **2.1 Sistema de Autenticación Core** 🎯 **PRIORIDAD 1**

**⏱️ Tiempo estimado: 3-4 días**

#### **📋 Componentes de Autenticación:**

- [ ] **🔐 LoginPage** - Formulario institucional SENA
  - Validación de credenciales contra backend
  - Manejo de errores y estados de carga
  - Recordar usuario (opcional)
  - Integración con design tokens SENA

- [ ] **🔑 JWT Token Management** - Manejo seguro de tokens
  - LocalStorage encriptado para Access Token
  - HttpOnly cookies para Refresh Token
  - Auto-refresh antes de expiración
  - Cleanup automático en logout

- [ ] **🛡️ AuthGuard Component** - Protección de rutas
  - HOC para rutas protegidas
  - Redirección automática a login
  - Verificación de tokens válidos
  - Loading states durante verificación

- [ ] **🔄 Token Refresh Logic** - Renovación automática
  - Interceptor para peticiones HTTP
  - Refresh automático en background
  - Manejo de errores de autenticación
  - Logout forzado si refresh falla

- [ ] **📤 Logout System** - Cierre seguro de sesión
  - Cleanup completo de tokens
  - Invalidación en backend
  - Redirección a página pública
  - Notificación de cierre de sesión

#### **🔧 Servicios de Autenticación:**

- [ ] **AuthService** - Servicios de autenticación

  ```typescript
  interface AuthService {
    login(credentials: LoginCredentials): Promise<AuthResponse>;
    logout(): Promise<void>;
    refreshToken(): Promise<string>;
    getCurrentUser(): Promise<User>;
    isAuthenticated(): boolean;
  }
  ```

- [ ] **AuthStore (Zustand)** - Estado global de autenticación
  ```typescript
  interface AuthStore {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: LoginCredentials) => Promise<void>;
    logout: () => void;
    checkAuth: () => Promise<void>;
  }
  ```

### **2.2 Gestión de Usuarios (UserService)** 🎯 **PRIORIDAD 2**

**⏱️ Tiempo estimado: 4-5 días**

#### **📋 Estado Actual:**

- [x] ~~**UsuariosPage** - Página base con estructura~~
- [x] ~~**UserAvatar** - Avatar con iniciales~~
- [x] ~~**UserMenu** - Menú desplegable~~

#### **🎯 Componentes por Implementar:**

- [ ] **👥 UserList Component** - Lista paginada de usuarios
  - Tabla responsive con filtros avanzados
  - Paginación server-side
  - Búsqueda en tiempo real
  - Ordenamiento por columnas
  - Acciones bulk (activar/desactivar múltiples)

- [ ] **📝 UserForm Component** - Crear/Editar usuarios
  - Formulario completo con validaciones
  - Subida de foto de perfil
  - Asignación de roles y permisos
  - Validación contra backend
  - Manejo de errores y estados

- [ ] **👤 UserProfile Component** - Perfil detallado
  - Vista completa del usuario
  - Historial de actividad
  - Configuraciones personales
  - Cambio de contraseña
  - Gestión de sesiones activas

- [ ] **🔍 UserSearch Component** - Búsqueda avanzada
  - Filtros por rol, estado, centro
  - Búsqueda semántica
  - Resultados con highlighting
  - Exportación de resultados
  - Guardado de búsquedas frecuentes

- [ ] **📊 UserImport Component** - Importación masiva
  - Carga de archivos CSV/Excel
  - Validación de datos en lote
  - Vista previa antes de importar
  - Manejo de errores y duplicados
  - Reporte de importación

#### **🔧 Servicios de Usuario:**

- [ ] **UserService** - CRUD completo de usuarios
  ```typescript
  interface UserService {
    getUsers(params: UserListParams): Promise<PaginatedUsers>;
    getUser(id: string): Promise<User>;
    createUser(userData: CreateUserData): Promise<User>;
    updateUser(id: string, userData: UpdateUserData): Promise<User>;
    deleteUser(id: string): Promise<void>;
    searchUsers(query: string): Promise<User[]>;
    importUsers(file: File): Promise<ImportResult>;
  }
  ```

### **2.3 Sistema de Roles y Permisos (RBAC)** 🎯 **PRIORIDAD 3**

**⏱️ Tiempo estimado: 3-4 días**

#### **🎯 Componentes de Autorización:**

- [ ] **⚡ RoleManager Component** - CRUD de roles
  - Lista de roles institucionales
  - Crear/editar roles personalizados
  - Asignación de permisos por rol
  - Vista jerárquica de roles
  - Duplicación de roles existentes

- [ ] **🔐 PermissionMatrix** - Matriz de permisos
  - Vista matricial permisos × recursos
  - Edición masiva de permisos
  - Plantillas de permisos comunes
  - Validación de dependencias
  - Exportación de configuración

- [ ] **👨‍💼 RoleAssignment** - Asignación a usuarios
  - Selección múltiple de usuarios
  - Asignación temporal de roles
  - Historial de cambios de roles
  - Notificaciones automáticas
  - Aprobación de cambios críticos

- [ ] **🛡️ PermissionGuard** - Control granular
  - HOC para control de acceso
  - Verificación por recurso y acción
  - Fallbacks personalizables
  - Logging de intentos de acceso
  - Cache de permisos por sesión

#### **🏛️ Roles Institucionales SENA:**

```typescript
enum InstitutionalRoles {
  SUPER_ADMIN = 'super_admin', // Administrador del sistema
  ADMIN_CGMLTI = 'admin_cgmlti', // Admin Centro CGMLTI
  COORDINATOR = 'coordinator', // Coordinador Académico
  INSTRUCTOR = 'instructor', // Instructor
  APPRENTICE = 'apprentice', // Aprendiz
  SECRETARY = 'secretary', // Secretaria
  GUEST = 'guest', // Invitado
}
```

### **2.4 Integración con Backend** 🎯 **PRIMERA INTERACCIÓN REAL**

**⏱️ Tiempo estimado: 2-3 días**

#### **🔗 Endpoints de Autenticación:**

```typescript
// Endpoints del Backend (Go + Python FastAPI)
const AUTH_ENDPOINTS = {
  LOGIN: '/api/auth/login', // POST - Iniciar sesión
  LOGOUT: '/api/auth/logout', // POST - Cerrar sesión
  REFRESH: '/api/auth/refresh', // POST - Renovar token
  ME: '/api/auth/me', // GET - Usuario actual
  FORGOT_PASSWORD: '/api/auth/forgot', // POST - Recuperar contraseña
  RESET_PASSWORD: '/api/auth/reset', // POST - Cambiar contraseña
};

const USER_ENDPOINTS = {
  USERS: '/api/users', // GET, POST - Lista/Crear
  USER_BY_ID: '/api/users/:id', // GET, PUT, DELETE
  USER_ROLES: '/api/users/:id/roles', // GET, PUT - Roles de usuario
  SEARCH_USERS: '/api/users/search', // GET - Búsqueda
  IMPORT_USERS: '/api/users/import', // POST - Importación masiva
};
```

#### **📡 Configuración API Client:**

- [ ] **Axios Configuration** - Cliente HTTP configurado
  - Base URL para diferentes entornos
  - Interceptors para autenticación
  - Manejo centralizado de errores
  - Retry logic para requests fallidos
  - Timeout y cancel tokens

- [ ] **React Query Integration** - Cache y sincronización
  - Queries para data fetching
  - Mutations para escritura
  - Cache invalidation strategies
  - Background refetching
  - Optimistic updates

### **2.5 Testing de Autenticación** 🧪

**⏱️ Tiempo estimado: 1-2 días**

#### **🧪 Estrategia de Testing:**

- [ ] **Unit Tests** - Componentes y servicios
  - AuthService methods
  - AuthStore state management
  - Component rendering
  - Form validations
  - Error handling

- [ ] **Integration Tests** - Flujos completos
  - Login/logout flow
  - Token refresh cycle
  - Route protection
  - Role-based access
  - API integration

- [ ] **E2E Tests** - Casos de uso reales
  - Login completo desde UI
  - Navegación protegida
  - Session timeout
  - Error scenarios
  - Multi-browser testing

### **📋 CRONOGRAMA DETALLADO FASE 2**

#### **🗓️ Semana 1: Core de Autenticación**

**Día 1-2: Sistema de Login**

- [x] LoginPage con formulario institucional
- [x] Validaciones y estados de error
- [x] Integración con AuthStore

**Día 3-4: JWT y Token Management**

- [ ] JWT token handling
- [ ] LocalStorage seguro
- [ ] Auto-refresh logic
- [ ] Logout cleanup

**Día 5: AuthGuard y Route Protection**

- [ ] ProtectedRoute component
- [ ] Redirecciones automáticas
- [ ] Loading states
- [ ] Testing inicial

#### **🗓️ Semana 2: Gestión de Usuarios**

**Día 6-7: UserList y Búsqueda**

- [ ] Tabla de usuarios paginada
- [ ] Filtros y búsqueda
- [ ] Integración con backend
- [ ] Estados de carga

**Día 8-9: UserForm y Profile**

- [ ] Formularios de usuario
- [ ] Vista de perfil detallada
- [ ] Validaciones avanzadas
- [ ] Subida de archivos

**Día 10: Roles y Permisos**

- [ ] Sistema RBAC básico
- [ ] Asignación de roles
- [ ] Permission guards
- [ ] Testing completo

### **🎯 CRITERIOS DE ÉXITO FASE 2**

#### **✅ Funcionalidades Críticas:**

1. **Autenticación Funcional**
   - Login/logout completo
   - Tokens JWT funcionando
   - Sessions persistentes
   - Route protection activa

2. **Gestión de Usuarios**
   - CRUD completo funcionando
   - Integración backend exitosa
   - Validaciones operativas
   - UX institucional aplicada

3. **Seguridad Implementada**
   - RBAC funcionando
   - Permisos granulares
   - Audit logs básicos
   - Protección contra ataques comunes

4. **Calidad Asegurada**
   - > 85% test coverage
   - Sin errores TypeScript/ESLint
   - Performance optimizada
   - Accesibilidad validada

### **🚀 PREPARACIÓN PARA DESPLIEGUE**

**Al finalizar la Fase 2, el sistema estará listo para:**

- **🌐 Primer despliegue en Hostinger**
- **🔗 Conexión con base de datos real**
- **👥 Usuarios reales del CGMLTI SENA**
- **📊 Métricas de uso iniciales**
- **🔄 Feedback para siguientes fases**

---

## 📅 **FASE 3: GESTIÓN ACADÉMICA**

**Duración: 3-4 semanas**

### **3.1 Horarios (ScheduleService)**

- [x] ~~**HorariosPage** - Página base con estructura~~
- [ ] **ScheduleCalendar** - Vista de calendario interactivo
- [ ] **ScheduleGrid** - Vista en grilla semanal
- [ ] **ScheduleForm** - Crear/Editar horarios
- [ ] **ClassSchedule** - Horario por clase/instructor
- [ ] **RoomSchedule** - Horario por aula
- [ ] **ScheduleConflicts** - Detección de conflictos
- [ ] **ScheduleExport** - Exportar a PDF/Excel

### **3.2 Asistencia (AttendanceService)**

- [ ] **AttendanceMarking** - Marcar asistencia
- [ ] **AttendanceList** - Lista de asistencia por clase
- [ ] **AttendanceReport** - Reportes de asistencia
- [ ] **AttendanceStats** - Estadísticas y gráficos
- [ ] **AttendanceQR** - Generación de códigos QR
- [ ] **AttendanceExceptions** - Manejo de excepciones

### **3.3 Fichas y Programas**

- [ ] **FichasList** - Lista de fichas de formación
- [ ] **FichaDetails** - Detalle de ficha
- [ ] **ProgramsList** - Programas de formación
- [ ] **CompetenciesList** - Competencias y RAP
- [ ] **LearningPathways** - Rutas de aprendizaje

---

## 📊 **FASE 4: EVALUACIONES**

**Duración: 3-4 semanas**

### **4.1 Evaluación de Proyectos (EvalproyService)**

- [x] ~~**EvaluacionesPage** - Página base con tabs completa~~
- [ ] **ProjectsList** - Lista de proyectos
- [ ] **ProjectForm** - Crear/Editar proyecto
- [ ] **ProjectDetails** - Detalle completo
- [ ] **ProjectEvaluation** - Formulario de evaluación
- [ ] **EvaluationCriteria** - Criterios y rúbricas
- [ ] **ProjectProgress** - Seguimiento de progreso
- [ ] **ProjectTeams** - Gestión de equipos

### **4.2 Evaluación Individual (EvalinService)**

- [ ] **EvaluationForm** - Formularios dinámicos
- [ ] **EvaluationHistory** - Historial de evaluaciones
- [ ] **EvaluationResults** - Resultados y calificaciones
- [ ] **CompetencyEvaluation** - Evaluación por competencias
- [ ] **SelfAssessment** - Autoevaluación
- [ ] **PeerEvaluation** - Evaluación entre pares

### **4.3 Reportes de Evaluación**

- [ ] **EvaluationDashboard** - Dashboard principal
- [ ] **StudentReport** - Reporte por estudiante
- [ ] **InstructorReport** - Reporte por instructor
- [ ] **CompetencyReport** - Reporte por competencias
- [ ] **ProgressCharts** - Gráficos de progreso
- [ ] **ExportReports** - Exportación de reportes

---

## 🤖 **FASE 5: IA Y ANÁLISIS**

**Duración: 2-3 semanas**

### **5.1 Servicios de IA (AIService)**

- [ ] **AIChatbot** - Chatbot SICORA integrado
- [ ] **PredictiveAnalytics** - Análisis predictivo
- [ ] **RecommendationEngine** - Sistema de recomendaciones
- [ ] **AutomaticAssessment** - Evaluación automática
- [ ] **LearningAnalytics** - Analíticas de aprendizaje

### **5.2 Base de Conocimientos (KbService)**

- [ ] **KnowledgeSearch** - Búsqueda semántica
- [ ] **DocumentLibrary** - Biblioteca de documentos
- [ ] **FAQSystem** - Sistema de FAQ inteligente
- [ ] **ContentSuggestions** - Sugerencias de contenido
- [ ] **KnowledgeGraph** - Grafos de conocimiento

---

## 💻 **FASE 6: FÁBRICA DE SOFTWARE**

**Duración: 2-3 semanas**

### **6.1 Gestión de Proyectos Software**

- [ ] **ProjectRepository** - Repositorios de código
- [ ] **TechnologyStack** - Stack tecnológico
- [ ] **DevelopmentTeams** - Equipos de desarrollo
- [ ] **CodeReview** - Revisión de código
- [ ] **ProjectMetrics** - Métricas de desarrollo
- [ ] **DeploymentPipeline** - Pipeline de despliegue

### **6.2 Seguimiento y Control**

- [ ] **TaskManager** - Gestión de tareas
- [ ] **TimeTracking** - Seguimiento de tiempo
- [ ] **QualityAssurance** - Control de calidad
- [ ] **DocumentationHub** - Hub de documentación

---

## 📈 **FASE 7: REPORTES Y DASHBOARDS**

**Duración: 2-3 semanas**

### **7.1 Dashboards Interactivos**

- [ ] **AdminDashboard** - Dashboard para administradores
- [ ] **InstructorDashboard** - Dashboard para instructores
- [ ] **StudentDashboard** - Dashboard para aprendices
- [ ] **CoordinatorDashboard** - Dashboard para coordinadores
- [ ] **RealTimeMetrics** - Métricas en tiempo real

### **7.2 Sistema de Reportes**

- [ ] **ReportBuilder** - Constructor de reportes
- [ ] **ScheduledReports** - Reportes programados
- [ ] **CustomReports** - Reportes personalizados
- [ ] **DataVisualization** - Visualización avanzada
- [ ] **ExportOptions** - Múltiples formatos de exportación

---

## 🔧 **FASE 8: CONFIGURACIÓN Y ADMINISTRACIÓN**

**Duración: 2 semanas**

### **8.1 Configuración del Sistema**

- [ ] **SystemSettings** - Configuraciones globales
- [ ] **InstitutionalSettings** - Configuración institucional
- [ ] **NotificationSettings** - Configuración de notificaciones
- [ ] **SecuritySettings** - Configuración de seguridad
- [ ] **BackupSettings** - Configuración de respaldos

### **8.2 Herramientas de Administración**

- [ ] **SystemLogs** - Logs del sistema
- [ ] **UserActivity** - Actividad de usuarios
- [ ] **SystemHealth** - Salud del sistema
- [ ] **DatabaseManagement** - Gestión de BD
- [ ] **CacheManagement** - Gestión de caché

---

## 📱 **FASE 9: EXPERIENCIA MÓVIL Y PWA**

**Duración: 2-3 semanas**

### **9.1 Responsive Design**

- [ ] **Mobile Navigation** - Navegación móvil optimizada
- [ ] **Touch Interactions** - Interacciones táctiles
- [ ] **Mobile Forms** - Formularios para móvil
- [ ] **Mobile Dashboards** - Dashboards móviles

### **9.2 Progressive Web App (PWA)**

- [ ] **Service Worker** - Cache y offline
- [ ] **App Manifest** - Instalación como app
- [ ] **Push Notifications** - Notificaciones push
- [ ] **Offline Functionality** - Funcionalidad offline

---

## 🧪 **FASE 10: TESTING Y CALIDAD**

**Duración: 2 semanas**

### **10.1 Testing Integral**

- [ ] **Unit Tests** - Tests unitarios (>90% coverage)
- [ ] **Integration Tests** - Tests de integración
- [ ] **E2E Tests** - Tests end-to-end con Playwright
- [ ] **Accessibility Tests** - Tests de accesibilidad
- [ ] **Performance Tests** - Tests de rendimiento

### **10.2 Calidad de Código**

- [ ] **ESLint Rules** - Reglas de linting avanzadas
- [ ] **Prettier Config** - Configuración de formato
- [ ] **Husky Hooks** - Git hooks para calidad
- [ ] **SonarQube** - Análisis de calidad estático

---

## 🚀 **FASE 11: DEPLOYMENT Y CI/CD**

**Duración: 1-2 semanas**

### **11.1 Build y Optimización**

- [ ] **Production Build** - Build optimizado
- [ ] **Bundle Analysis** - Análisis de bundles
- [ ] **Performance Optimization** - Optimización de rendimiento
- [ ] **SEO Optimization** - Optimización SEO

### **11.2 CI/CD Pipeline**

- [ ] **GitHub Actions** - Pipeline automatizado
- [ ] **Automated Testing** - Tests automáticos
- [ ] **Security Scanning** - Escaneo de seguridad
- [ ] **Deployment Strategy** - Estrategia de despliegue

---

## 📚 **DOCUMENTACIÓN Y CAPACITACIÓN**

### **Documentación Técnica**

- [ ] **Component Library** - Storybook con todos los componentes
- [ ] **API Documentation** - Documentación de servicios
- [ ] **User Guide** - Guía de usuario completa
- [ ] **Admin Manual** - Manual de administrador
- [ ] **Developer Guide** - Guía para desarrolladores

### **Capacitación**

- [ ] **Video Tutorials** - Tutoriales en video
- [ ] **Training Materials** - Materiales de capacitación
- [ ] **Support Documentation** - Documentación de soporte

---

## 🎯 **MÉTRICAS DE ÉXITO**

### **Técnicas**

- ✅ **Performance**: Lighthouse Score > 90
- ✅ **Accessibility**: WCAG 2.1 AA compliance
- ✅ **Security**: Zero vulnerabilities críticas
- ✅ **Test Coverage**: > 90% coverage
- ✅ **Bundle Size**: < 500KB inicial

### **Funcionales**

- ✅ **User Experience**: SUS Score > 80
- ✅ **Load Time**: < 3 segundos
- ✅ **Mobile Usability**: 100% responsive
- ✅ **Browser Compatibility**: IE11+, todos los modernos
- ✅ **Offline Capability**: Funcionalidad básica offline

---

## 📋 **CRONOGRAMA ACTUALIZADO - Julio 2025**

| Fase                          | Duración  | Inicio       | Fin          | Estado |
| ----------------------------- | --------- | ------------ | ------------ | ------ |
| **Fase 1**: Infraestructura   | 3 semanas | Jul 1 (✅)   | Jul 21       | 🟢 90% |
| **Fase 2**: Autenticación     | 2 semanas | Jul 22       | Ago 4        | ⚪     |
| **Fase 3**: Gestión Académica | 4 semanas | Ago 5        | Sep 1        | ⚪     |
| **Fase 4**: Evaluaciones      | 4 semanas | Sep 2        | Sep 29       | ⚪     |
| **Fase 5**: IA y Análisis     | 3 semanas | Sep 30       | Oct 20       | ⚪     |
| **Fase 6**: Fábrica Software  | 3 semanas | Oct 21       | Nov 10       | ⚪     |
| **Fase 7**: Reportes          | 3 semanas | Nov 11       | Dic 1        | ⚪     |
| **Fase 8**: Configuración     | 2 semanas | Dic 2        | Dic 15       | ⚪     |
| **Fase 9**: Móvil/PWA         | 3 semanas | Dic 16       | Ene 5, 2026  | ⚪     |
| **Fase 10**: Testing          | 2 semanas | Ene 6, 2026  | Ene 19, 2026 | ⚪     |
| **Fase 11**: Deployment       | 2 semanas | Ene 20, 2026 | Feb 2, 2026  | ⚪     |

**Duración Total**: ~31 semanas (7.5 meses) | **Progreso Global**: 🟢 **22%** ⬆️ **(+4% Design Tokens completados)**

---

## 🏗️ **ESTADO ACTUAL DE IMPLEMENTACIÓN**

### **📦 Componentes Completados (Julio 1, 2025)**

#### **🎨 Layouts Institucionales**

- ✅ `InstitutionalLayout` - Layout principal con header/footer
- ✅ `InstitutionalHeader` - Header responsivo con navegación **[ADAPTATIVO DUAL]**
- ✅ `InstitutionalFooter` - Footer con información organizacional **[ADAPTATIVO DUAL]**
- ✅ `InstitutionalSearchBar` - Búsqueda estilo SofiaPlus
- ✅ `InstitutionalSidebar` - Sidebar contextual por roles
- ✅ `LayoutWrapper` - Wrapper para integración con Router

#### **👤 Gestión de Usuarios**

- ✅ `UserAvatar` - Avatar con iniciales y estados
- ✅ `UserMenu` - Menú desplegable de usuario
- ✅ `RoleBadge` - Badges para identificar roles
- ✅ `Navigation` - Navegación contextual por rol

#### **🧭 Navegación y UX**

- ✅ `Breadcrumb` - Migas de pan automáticas
- ✅ `useBreadcrumb` - Hook para generar breadcrumbs
- ✅ Router configurado con rutas anidadas

#### **🔒 Validación y Seguridad**

- ✅ `ValidatedInput` - Input con validaciones REGEXP
- ✅ `useValidation` - Hook para validaciones
- ✅ `SecureValidator` - Validador con sanitización
- ✅ Sistema anti-XSS y validaciones institucionales

#### **🎨 Sistema de Branding Dual** ⭐ **NUEVO**

- ✅ `src/config/brand.ts` - Configuración centralizada EPTI/SENA
- ✅ `.env.development` - Variables entorno desarrollo
- ✅ `.env.hostinger` - Variables entorno producción EPTI
- ✅ `.env.sena` - Variables entorno producción SENA
- ✅ Scripts duales: `build:hostinger` y `build:sena`
- ✅ Componentes adaptativos automáticos (títulos, logos, textos)
- ✅ Sistema verificación configuraciones
- ✅ Builds diferenciados probados y funcionando

#### **📱 Páginas Base**

- ✅ `Dashboard` - Página principal
- ✅ `DemoPage` - Página de demostración
- ✅ `UsuariosPage` - Gestión de usuarios (estructura)
- ✅ `HorariosPage` - Gestión de horarios (estructura)
- ✅ `EvaluacionesPage` - Sistema de evaluaciones (estructura)
- ✅ `NotFoundPage` - Página 404

#### **🔧 Infraestructura**

- ✅ Zustand store para manejo de estado
- ✅ React Query para data fetching
- ✅ Sistema de commits automáticos
- ✅ DevContainer + Docker configurado
- ✅ Mock backend para desarrollo

#### **🎨 Sistema de Design Tokens SENA** ⭐ **NUEVO**

- ✅ `tailwind.config.ts` - Sistema completo de tokens expandido
- ✅ Tokens de espaciado: 25+ tokens organizados por uso (micro, estándar, funcional)
- ✅ Tokens de sizing: 40+ tokens (width, height, min/max dimensiones)
- ✅ Tokens de border radius: 15+ tokens específicos por componente
- ✅ Tokens de z-index: Sistema de 10 niveles organizados
- ✅ Tokens de animación: 5 animaciones predefinidas con keyframes
- ✅ `DESIGN_TOKENS_SENA.md` - Documentación completa con ejemplos
- ✅ `DesignTokensDemo.tsx` - Componente demostración visual
- ✅ Ruta `/design-tokens` funcional para visualizar tokens

---

### **📊 Métricas de Calidad**

- **Errores ESLint**: 0 ❌➡️✅
- **Errores TypeScript**: 0 ❌➡️✅
- **Test Coverage**: 0% (pendiente)
- **Performance**: 95+ (Lighthouse)
- **Accessibility**: WCAG 2.1 AA (en progreso)

---

## 🛠️ **HERRAMIENTAS Y RECURSOS**

### **Desarrollo**

- **IDE**: VSCode + extensiones React/TypeScript
- **Version Control**: Git + GitHub
- **Package Manager**: pnpm
- **API Testing**: Postman/Insomnia
- **Database Tools**: pgAdmin, Redis Insight

### **Design y UX**

- **Design System**: Storybook
- **Prototyping**: Figma
- **Icons**: Heroicons, Lucide
- **Illustrations**: Undraw, Storyset

### **Monitoreo y Analytics**

- **Error Tracking**: Sentry
- **Analytics**: Google Analytics 4
- **Performance**: Web Vitals, Lighthouse CI
- **Uptime**: Uptime Robot

---

## ⚠️ **RIESGOS Y MITIGACIONES**

### **Riesgos Técnicos**

- **Integración Backend**: Tests de integración tempranos
- **Performance**: Profiling continuo y optimización
- **Compatibility**: Testing en múltiples browsers
- **Security**: Auditorías de seguridad regulares

### **Riesgos de Proyecto**

- **Scope Creep**: Documentación clara de requerimientos
- **Resource Availability**: Plan de contingencia para desarrolladores
- **Timeline Delays**: Buffer de tiempo en fases críticas

---

## 🎉 **ENTREGABLES FINALES**

1. **Aplicación Web Completa** - Frontend production-ready
2. **Component Library** - Storybook con documentación
3. **Documentation Suite** - Documentación técnica y usuario
4. **Testing Suite** - Suite completa de tests
5. **Deployment Guide** - Guía de despliegue y mantenimiento
6. **Training Materials** - Materiales de capacitación
7. **Support Documentation** - Documentación de soporte

---

**Este plan cubre todas las necesidades de interfaz gráfica para el backend de SICORA, asegurando una experiencia de usuario completa, robusta y alineada con los estándares institucionales del SENA.**

---

## 📋 **PLAN PASO A PASO - ESTADO ACTUAL**

### **🎯 SITUACIÓN ACTUAL (Julio 1, 2025) - ✅ COMPLETADO**

**✅ COMPLETADO - Paso 1.1 Setup Inicial:**

- ✅ Configuración Docker completa y funcionando
- ✅ DevContainer operativo para desarrollo en equipo
- ✅ React Router v6 configurado con BrowserRouter
- ✅ App.tsx migrado completamente a nueva arquitectura
- ✅ Zustand store implementado con gestión de usuarios
- ✅ React Query configurado para data fetching
- ✅ Commits automáticos funcionando con Husky + lint-staged
- ✅ Todos los errores ESLint y TypeScript resueltos
- ✅ Sistema de validaciones REGEXP implementado
- ✅ Componentes institucionales base completados
- ✅ Páginas base funcionando con navegación
- ✅ Mock backend sirviendo datos de prueba

**📍 PRÓXIMOS PASOS CRÍTICOS:**

---

### **SEMANA 1 (Julio 1-7): ✅ COMPLETADA - CONSOLIDACIÓN Y DOCKER**

#### **✅ Día 1 (Julio 1): Setup Docker Completo - COMPLETADO**

- ✅ DevContainer funcionando 100%
- ✅ Stack Docker completo operativo
- ✅ Mock backend sirviendo datos
- ✅ Documentación setup para equipo

#### **✅ Día 1 (Julio 1): Integración Validaciones - COMPLETADO**

- ✅ Todos los inputs existentes con validación REGEXP
- ✅ Formularios siguiendo UX/UI (botones a la derecha)
- ✅ ValidatedInput implementado y funcionando
- ✅ Demo funcional SecureFormDemo

#### **✅ Día 1 (Julio 1): React Router + Rutas - COMPLETADO**

- ✅ Routing completo configurado
- ✅ Navegación funcional entre páginas
- ✅ Breadcrumbs dinámicos
- ✅ URLs amigables y limpias

**🎉 RESULTADO: Paso 1.1 completado exitosamente en 1 día vs 7 días planificados**

---

### **SEMANA 1 (Julio 2-7): 🔄 EN PROGRESO - DESIGN TOKENS**

#### **🎯 Próximo: Día 2 (Julio 2): Tokens de Espaciado y Sizing**

```typescript
// Implementar en tailwind.config.js:
spacing: {
  'sena-xs': '0.5rem',    // 8px
  'sena-sm': '1rem',      // 16px
  'sena-md': '1.5rem',    // 24px
  'sena-lg': '2rem',      // 32px
  'sena-xl': '3rem',      // 48px
  'sena-2xl': '4rem',     // 64px
}
```

**Tareas pendientes:**

- [ ] Implementar tokens de espaciado SENA
- [ ] Implementar tokens de sombras
- [ ] Crear variables CSS personalizadas
- [ ] Documentar en Storybook

---

### **SEMANA 2 (Julio 8-14): MÓDULOS CORE**

#### **Día 1-3: Módulo Usuarios**

```typescript
// Estructura a crear:
src/
├── pages/
│   └── usuarios/
│       ├── UsuariosListPage.tsx
│       ├── UsuarioCreatePage.tsx
│       ├── UsuarioEditPage.tsx
│       └── UsuarioDetailPage.tsx
├── components/
│   └── usuarios/
│       ├── UsuarioForm.tsx
│       ├── UsuarioCard.tsx
│       └── UsuarioFilters.tsx
└── services/
    └── usuariosService.ts
```

**Implementación paso a paso:**

1. **UsuariosListPage**: Lista con filtros, búsqueda y paginación
2. **UsuarioForm**: Formulario con ValidatedInput para cedula, email @sena.edu.co, etc.
3. **Integración API**: Conectar con backend real (Go/Python)
4. **Testing**: Tests E2E para flujo completo

**Entregables:**

- [ ] CRUD usuarios completo y funcional
- [ ] Validaciones institucionales (email @sena.edu.co, cedula)
- [ ] Integración con backend real
- [ ] Tests E2E para usuarios

#### **Día 4-7: Módulo Horarios**

```typescript
// Componentes a crear:
-HorarioCalendar.tsx - // Vista calendario mensual/semanal
  HorarioForm.tsx - // Crear/editar horario
  HorarioConflicts.tsx - // Detección conflictos
  InstructorSchedule.tsx - // Vista por instructor
  FichaSchedule.tsx; // Vista por ficha
```

**Funcionalidades críticas:**

1. **Calendario visual** con drag & drop
2. **Detección automática de conflictos**
3. **Asignación instructor-ficha-ambiente**
4. **Exportación PDF/Excel**

**Entregables:**

- [ ] Calendario funcional con todas las vistas
- [ ] Sistema anti-conflictos operativo
- [ ] Integración completa con backend
- [ ] Exportación de horarios

---

### **SEMANA 3 (Julio 15-21): EVALUACIONES + IA**

#### **Día 1-4: Sistema Evaluaciones**

```typescript
// Módulos principales:
1. EvaluacionForm.tsx       // Crear evaluación
2. EvaluacionRubrica.tsx    // Sistema de rúbricas
3. EvaluacionCalificacion.tsx // Calificar evaluación
4. EvaluacionReportes.tsx   // Reportes por ficha/instructor
```

**Implementación:**

1. **Tipos de evaluación**: Proyecto, quiz, presentación, práctica
2. **Sistema de rúbricas**: Configurable por competencia
3. **Calificación masiva**: Importar/exportar Excel
4. **Reportes automáticos**: Progreso por aprendiz/ficha

#### **Día 5-7: Integración IA**

```typescript
// Componentes IA:
1. AIAssistant.tsx          // Chat con IA
2. AIEvaluationHelper.tsx   // Sugerencias evaluación
3. AIContentGenerator.tsx   // Generar contenido
4. AIAnalytics.tsx          // Análisis inteligente
```

**Entregables:**

- [ ] Sistema evaluaciones completo
- [ ] IA Assistant funcionando
- [ ] Generación automática de contenido
- [ ] Análisis inteligente de datos

---

### **SEMANA 4 (Julio 22-28): OPTIMIZACIÓN + TESTING**

#### **Día 1-3: Performance + PWA**

```bash
# Optimizaciones críticas:
1. Code splitting por rutas
2. Lazy loading componentes
3. Service Worker para PWA
4. Optimización imágenes
5. Bundle analysis y reducción
```

#### **Día 4-7: Testing Completo**

```typescript
// Suite de testing:
1. Unit tests (Jest + Testing Library)
2. Integration tests (API mocking)
3. E2E tests (Playwright)
4. Visual regression tests
5. Performance tests (Lighthouse CI)
```

**Entregables:**

- [ ] PWA completamente funcional
- [ ] Performance Score > 90
- [ ] Coverage de tests > 90%
- [ ] Suite E2E completa

---

## 🔄 **FLUJO DE TRABAJO DIARIO**

### **Rutina Matutina (9:00-10:00 AM)**

```bash
# 1. Actualizar repositorio
git pull origin main

# 2. Levantar entorno desarrollo
make dev-docker  # o docker-compose up

# 3. Verificar tests
pnpm test

# 4. Review tareas del día
```

### **Desarrollo (10:00 AM - 5:00 PM)**

```bash
# Ciclo por funcionalidad:
1. Crear rama feature: git checkout -b feature/usuarios-crud
2. Implementar componente con ValidatedInput
3. Escribir tests unitarios
4. Integrar con backend
5. Test manual + E2E
6. Code review + merge
```

### **Cierre Diario (5:00-6:00 PM)**

```bash
# 1. Ejecutar suite completa tests
pnpm test:full

# 2. Build verificación
pnpm build

# 3. Commit y push
git add . && git commit -m "feat: implement users CRUD"
git push origin feature/usuarios-crud

# 4. Actualizar documentación
```

---

## 📊 **MÉTRICAS DIARIAS DE PROGRESO**

### **Checklist Diario:**

- [ ] ¿Nuevos componentes usan ValidatedInput?
- [ ] ¿Botones siguen UX/UI (derecha para acciones)?
- [ ] ¿Tests unitarios escritos y pasando?
- [ ] ¿Integración backend funciona?
- [ ] ¿Performance mantiene > 90?
- [ ] ¿Documentación actualizada?

### **Reportes Semanales:**

- **Funcionalidades completadas vs. planificadas**
- **Coverage de tests actual**
- **Performance metrics (Lighthouse)**
- **Issues de seguridad detectados**
- **Feedback de usuario (si aplica)**

---

## 🚨 **PUNTOS DE CONTROL CRÍTICOS**

### **Semana 1 - Checkpoint Docker + Validaciones**

**Criterios de éxito:**

- ✅ Docker funcionando en todo el equipo
- ✅ Validaciones REGEXP implementadas
- ✅ Router funcionando
- ✅ Demo completo operativo

### **Semana 2 - Checkpoint Módulos Core**

**Criterios de éxito:**

- ✅ CRUD usuarios 100% funcional
- ✅ Sistema horarios operativo
- ✅ Integración backend estable
- ✅ Tests E2E usuarios + horarios

### **Semana 3 - Checkpoint Evaluaciones + IA**

**Criterios de éxito:**

- ✅ Sistema evaluaciones completo
- ✅ IA Assistant operativo
- ✅ Reportes automáticos funcionando
- ✅ Performance mantenida

### **Semana 4 - Checkpoint Final**

**Criterios de éxito:**

- ✅ PWA completa y funcionando
- ✅ Suite testing > 90% coverage
- ✅ Documentación completa
- ✅ Lista para producción

---

## 📞 **ESCALACIÓN DE PROBLEMAS**

### **Blockers Técnicos:**

1. **Primero**: Consultar documentación técnica
2. **Segundo**: Review código en equipo
3. **Tercero**: Consultar con arquitecto backend
4. **Último**: Escalación a lead técnico

### **Problemas de Integración:**

1. **Mock data** para continuar desarrollo
2. **Coordinación** con equipo backend
3. **Testing** con datos reales cuando esté listo

---

**🎯 OBJETIVO**: Al final de estas 4 semanas tener un frontend completamente funcional, seguro, optimizado y listo para producción, siguiendo todos los estándares institucionales SENA.\*\*

---

### **🔧 CONFIGURACIÓN TÉCNICA - INTEGRACIÓN GO**

#### **⚙️ Configuración del Cliente HTTP:**

```typescript
// src/lib/api-client.ts
const API_BASE_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8080';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

#### **🏃‍♂️ PASOS INMEDIATOS PARA INICIAR LA INTEGRACIÓN:**

##### **1. Configuración del Backend Go (LISTO)** ✅

- ✅ UserService 100% implementado y tested
- ✅ JWT middleware optimizado V2 funcionando
- ✅ Base de datos PostgreSQL configurada
- ✅ Todos los endpoints de autenticación disponibles
- ✅ Documentación completa generada

##### **2. Configuración del Frontend (PRÓXIMO PASO)** 🔄

- [ ] **Instalar dependencias HTTP**: `axios`, `@tanstack/react-query`
- [ ] **Configurar variables de entorno**: `.env.local` con URL del backend Go
- [ ] **Crear cliente HTTP**: interceptors para JWT y manejo de errores
- [ ] **Configurar stores Zustand**: AuthStore con integración Go API
- [ ] **Implementar hooks React Query**: mutaciones y queries para auth

##### **3. Variables de Entorno Requeridas:**

```bash
# .env.local
VITE_API_BASE_URL=http://localhost:8080
VITE_API_TIMEOUT=10000
VITE_JWT_REFRESH_THRESHOLD=300000  # 5 minutos antes de expirar
```

##### **4. Estructura de Archivos a Crear:**

```
src/
├── lib/
│   ├── api-client.ts           # Cliente HTTP con interceptors
│   ├── auth-api.ts            # Endpoints específicos de auth
│   └── users-api.ts           # Endpoints de gestión de usuarios
├── stores/
│   └── auth-store.ts          # Zustand store para autenticación
├── hooks/
│   ├── use-auth.ts            # Hook personalizado de auth
│   ├── use-auth-query.ts      # React Query hooks para auth
│   └── use-users-query.ts     # React Query hooks para users
└── types/
    ├── auth.types.ts          # Tipos TypeScript para auth
    └── user.types.ts          # Tipos TypeScript para users
```

#### **📡 SERVIDOR BACKEND GO - ESTADO DE PREPARACIÓN:**

##### **🚀 Listo para Conexión:**

- **Puerto**: `8080` (configuración por defecto)
- **Base URL**: `http://localhost:8080`
- **Documentación**: Swagger UI disponible
- **Health Check**: `GET /health` endpoint disponible
- **CORS**: Configurado para desarrollo local
- **Rate Limiting**: 100 requests/minuto por IP

##### **🔐 Autenticación JWT:**

- **Algorithm**: HS256
- **Access Token TTL**: 15 minutos
- **Refresh Token TTL**: 7 días
- **Custom Claims**: `user_id`, `email`, `role`, `permissions`
