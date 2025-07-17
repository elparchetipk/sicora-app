# Lista de Chequeo: Cobertura Frontend para Microservicios

**Fecha:** 19 de junio de 2025  
**Propósito:** Verificar que un microservicio esté completamente cubierto por su implementación frontend  
**Ejemplo base:** UserService

## 📋 **LISTA DE CHEQUEO COMPLETA**

### 🎯 **FASE 1: ANÁLISIS Y PLANIFICACIÓN**

#### 1.1 Documentación Base

- [ ] **Historias de Usuario definidas** para el microservicio
  - Archivo: `_docs/stories/fe/historias_usuario_fe_{microservice}.md`
  - Criterios de aceptación claros
  - Estados de implementación definidos (✅🚧📋❌)
- [ ] **Mapeo Backend-Frontend** documentado
  - Archivo: `_docs/planning/HU-MAPEO-BE-FE.md`
  - Correspondencia entre endpoints del backend y componentes del frontend
- [ ] **API Endpoints** especificados
  - Archivo: `_docs/api/endpoints_specification_{microservice}.md`
  - Contratos de datos (Request/Response)
  - Códigos de error y manejo de excepciones

#### 1.2 Arquitectura de Información

- [ ] **Modelos de datos TypeScript** definidos
  - Ubicación: `src/types/{microservice}Types.ts`
  - Interfaces para entidades principales
  - Types para DTOs y formularios
- [ ] **Estados de la aplicación** identificados
  - Store management (Zustand/Redux)
  - Estados locales vs globales
  - Flujos de datos entre componentes

### 🛠️ **FASE 2: SERVICIOS Y API**

#### 2.1 Servicios de API

- [ ] **Service client** implementado
  - Archivo: `src/services/{microservice}Service.ts`
  - Todas las operaciones CRUD cubiertas
  - Manejo de errores consistente
  - Tipos TypeScript para requests/responses
- [ ] **Configuración del cliente HTTP**
  - Integración con `apiClient.ts`
  - Headers de autenticación
  - Interceptors para errores globales
  - Timeouts y reintentos

#### 2.2 Hooks Personalizados

- [ ] **Data fetching hooks** implementados
  - Ubicación: `src/hooks/use{Microservice}.ts`
  - React Query / SWR para caché
  - Estados de loading, error, success
  - Invalidación de caché automática
- [ ] **Form management hooks**
  - React Hook Form integrado
  - Validaciones con Zod/Yup
  - Manejo de estados de formulario

### 🎨 **FASE 3: COMPONENTES UI (ATOMIC DESIGN)**

#### 3.1 Átomos (Atoms)

- [ ] **Componentes básicos** específicos del dominio
  - Ubicación: `src/components/atoms/{microservice}/`
  - Botones especializados
  - Inputs con validaciones específicas
  - Labels y badges del dominio

#### 3.2 Moléculas (Molecules)

- [ ] **Grupos de átomos** funcionales
  - Ubicación: `src/components/molecules/{microservice}/`
  - Campos de formulario compuestos
  - Cards de información
  - Filtros y buscadores

#### 3.3 Organismos (Organisms)

- [ ] **Secciones complejas** de la interfaz
  - Ubicación: `src/components/organisms/{microservice}/`
  - Listas con paginación
  - Formularios completos
  - Tablas con acciones
  - Modales específicos del dominio

#### 3.4 Templates y Pages

- [ ] **Layouts** específicos del microservicio
  - Ubicación: `src/components/templates/{microservice}/`
  - Estructura de páginas principales
- [ ] **Páginas completas**
  - Ubicación: `src/components/pages/{microservice}/`
  - Vista de listado principal
  - Vista de detalles
  - Formulario de creación/edición
  - Vista de dashboard específica

### 🔄 **FASE 4: FUNCIONALIDADES PRINCIPALES**

#### 4.1 Operaciones CRUD

- [ ] **CREATE - Crear nuevos registros**
  - Formulario de creación
  - Validaciones frontend
  - Feedback de éxito/error
  - Redirección post-creación
- [ ] **READ - Visualizar datos**
  - Lista con paginación
  - Vista de detalle
  - Filtros y búsqueda
  - Ordenamiento
- [ ] **UPDATE - Actualizar registros**
  - Formulario de edición pre-poblado
  - Validaciones de cambios
  - Confirmación de guardado
  - Manejo de conflictos
- [ ] **DELETE - Eliminar registros**
  - Confirmación de eliminación
  - Eliminación masiva (si aplica)
  - Rollback en caso de error

#### 4.2 Funcionalidades Específicas del Dominio

- [ ] **Workflows del negocio** implementados
  - Procesos específicos del microservicio
  - Estados de transición
  - Validaciones de reglas de negocio
- [ ] **Integraciones** con otros microservicios
  - Llamadas a servicios dependientes
  - Sincronización de datos
  - Manejo de fallos de dependencias

### 🎭 **FASE 5: EXPERIENCIA DE USUARIO**

#### 5.1 Estados de Interfaz

- [ ] **Loading states** implementados
  - Skeletons para carga inicial
  - Spinners para acciones
  - Progress bars para procesos largos
- [ ] **Error states** manejados
  - Páginas de error específicas
  - Mensajes de error contextuales
  - Acciones de recuperación
- [ ] **Empty states** diseñados
  - Estados sin datos
  - Primeros pasos para nuevos usuarios
  - Call-to-action claros

#### 5.2 Navegación y Routing

- [ ] **Rutas** definidas y protegidas
  - Estructura de URLs clara
  - Protección por roles
  - Breadcrumbs donde aplique
- [ ] **Navegación** intuitiva
  - Menús contextuales
  - Enlaces internos consistentes
  - Back navigation

### 🔐 **FASE 6: SEGURIDAD Y PERMISOS**

#### 6.1 Autorización

- [ ] **Permisos por rol** implementados
  - Guards de componentes
  - Ocultación de funcionalidades no permitidas
  - Validación en cliente y servidor
- [ ] **Contextos de seguridad**
  - Manejo de sesiones
  - Refresh de tokens
  - Logout automático por inactividad

### 📱 **FASE 7: RESPONSIVIDAD Y ACCESIBILIDAD**

#### 7.1 Diseño Responsivo

- [ ] **Mobile-first** implementado
  - Breakpoints definidos
  - Componentes adaptables
  - Touch interactions
- [ ] **Cross-browser** compatibility
  - Testing en navegadores principales
  - Polyfills necesarios
  - Graceful degradation

#### 7.2 Accesibilidad (a11y)

- [ ] **ARIA labels** implementados
  - Screen reader support
  - Keyboard navigation
  - Color contrast apropiado
- [ ] **Semantic HTML** utilizado
  - Elementos apropiados para cada función
  - Estructura lógica de headings

### 🧪 **FASE 8: TESTING**

#### 8.1 Unit Tests

- [ ] **Componentes** testados
  - Ubicación: `src/test/components/{microservice}/`
  - Jest + Testing Library
  - Coverage > 80%
- [ ] **Hooks y servicios** testados
  - Ubicación: `src/test/hooks/` y `src/test/services/`
  - Mocking de APIs
  - Edge cases cubiertos

#### 8.2 Integration Tests

- [ ] **Flujos completos** testados
  - End-to-end con Playwright/Cypress
  - User journeys principales
  - Escenarios de error

### 🎨 **FASE 9: CUMPLIMIENTO DE ESTÁNDARES**

#### 9.1 Imagen Corporativa SENA

- [ ] **Colores institucionales** aplicados
  - Verde SENA: #39A900
  - Naranja SENA: #FF8C00
  - Escala de grises definida
- [ ] **Tipografía** consistente
  - Fuentes institucionales
  - Jerarquía tipográfica
  - Legibilidad asegurada
- [ ] **Elementos visuales** apropiados
  - Logos en tamaños correctos
  - Iconografía consistente
  - Spacing y layout estandarizado

#### 9.2 Mejores Prácticas de Desarrollo

- [ ] **Clean Code** aplicado
  - Nomenclatura consistente
  - Componentes reutilizables
  - Separación de responsabilidades
- [ ] **Performance** optimizado
  - Lazy loading implementado
  - Bundle splitting
  - Memoización donde aplique

### 📊 **FASE 10: DOCUMENTACIÓN Y DEPLOYMENT**

#### 10.1 Documentación

- [ ] **Storybook** configurado
  - Componentes documentados
  - Variaciones y estados
  - Props tables actualizadas
- [ ] **README** específico del microservicio
  - Instrucciones de uso
  - Configuración necesaria
  - Troubleshooting

#### 10.2 CI/CD

- [ ] **Build process** configurado
  - Linting y formateo automático
  - Tests en pipeline
  - Build optimization
- [ ] **Deployment** automatizado
  - Environment variables
  - Health checks
  - Rollback procedures

---

## 🎯 **CHECKLIST RÁPIDO POR MICROSERVICIO**

### ✅ **UserService** - Status: 🚧 En desarrollo

- [x] Documentación base definida
- [x] Servicios API implementados
- [ ] Componentes UI completos (50%)
- [ ] Funcionalidades CRUD (70%)
- [ ] Tests implementados (30%)
- [ ] Cumplimiento SENA (80%)

### ✅ **ScheduleService** - Status: ✅ Completado (95%)

- [x] Documentación base definida
- [x] Servicios API implementados
- [x] Componentes UI completos (95%)
- [x] Funcionalidades CRUD (95%)
- [ ] Tests implementados (0%)
- [x] Cumplimiento SENA (95%)

### 📋 **AttendanceService** - Status: 📋 Pendiente

- [ ] Documentación base definida
- [ ] Servicios API implementados
- [ ] Componentes UI completos
- [ ] Funcionalidades CRUD
- [ ] Tests implementados
- [ ] Cumplimiento SENA

---

## 🔧 **COMANDOS ÚTILES PARA VERIFICACIÓN**

```bash
# Verificar estructura de archivos
find src -name "*{microservice}*" -type f

# Verificar imports y exports
grep -r "{microservice}" src/ --include="*.ts" --include="*.tsx"

# Verificar tests
npm run test -- --testPathPattern="{microservice}"

# Verificar build
npm run build

# Verificar linting
npm run lint src/components/**/{microservice}/**
```

---

## 📈 **MÉTRICAS DE COMPLETITUD**

- **Completitud de funcionalidades**: X/Y historias implementadas
- **Cobertura de tests**: X% de code coverage
- **Performance**: Lighthouse score > 90
- **Accesibilidad**: a11y score > 95
- **Cumplimiento corporativo**: Lista de verificación SENA

---

**Nota:** Esta lista debe ser actualizada conforme evolucionan los estándares del proyecto y las necesidades específicas de cada microservicio.
