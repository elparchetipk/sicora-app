# 📱 **ÍNDICE DE HISTORIAS DE USUARIO - FRONTEND**

**Fecha:** 27 de junio de 2025
**Versión:** 1.0
**Sistema:** SICORA - Aplicación Frontend React

---

## 🎯 **RESUMEN EJECUTIVO**

**Estado consolidado:** 0/95 historias EN DESARROLLO (0%) 🚧

### **📊 Progreso por Área Funcional:**

| Área Funcional          | Historias | Estado           | Completitud | Archivo                                                      |
| ----------------------- | --------- | ---------------- | ----------- | ------------------------------------------------------------ |
| **Core App**            | 0/12      | 🚧 EN DESARROLLO | 0%          | [HU_FE_CoreApp.md](HU_FE_CoreApp.md)                         |
| **Authentication**      | 0/8       | 🚧 EN DESARROLLO | 0%          | [HU_FE_Authentication.md](HU_FE_Authentication.md)           |
| **User Management**     | 0/10      | � EN DESARROLLO  | 0%          | [HU_FE_UserManagement.md](HU_FE_UserManagement.md)           |
| **Schedule**            | 0/12      | � EN DESARROLLO  | 0%          | [HU_FE_Schedule.md](HU_FE_Schedule.md)                       |
| **Attendance**          | 0/10      | � EN DESARROLLO  | 0%          | [HU_FE_Attendance.md](HU_FE_Attendance.md)                   |
| **Evaluations**         | 0/15      | � EN DESARROLLO  | 0%          | [HU_FE_Evaluations.md](HU_FE_Evaluations.md)                 |
| **Knowledge Base**      | 0/8       | � EN DESARROLLO  | 0%          | [HU_FE_KnowledgeBase.md](HU_FE_KnowledgeBase.md)             |
| **MongoDB Integration** | 0/9       | 📋 PLANIFICACIÓN | 0%          | [HU_FE_MongoDB_Integration.md](HU_FE_MongoDB_Integration.md) |
| **AI Assistant**        | 0/6       | � EN DESARROLLO  | 0%          | [HU_FE_AIAssistant.md](HU_FE_AIAssistant.md)                 |
| **Reports/Analytics**   | 0/10      | � EN DESARROLLO  | 0%          | [HU_FE_ReportsAnalytics.md](HU_FE_ReportsAnalytics.md)       |

---

## 📋 **DOCUMENTACIÓN DE REFERENCIA**

### **🎨 Arquitectura Frontend:**

- **Framework:** React + Vite (Mobile First)
- **Compilación:** Web Progressive App
- **Estilización:** TailwindCSS
- **Navegación:** React Router
- **Estado:** Context API + Custom Hooks
- **Testing:** Jest + React Testing Library

### **🔗 Integración Backend:**

- **[RF Backend](../../general/rf.md)** - Arquitectura de microservicios
- **[API Gateway](../be/HU_APIGateway.md)** - Punto de entrada único
- **[User Service](../be/HU_UserService.md)** - Autenticación y usuarios
- **[Schedule Service](../be/HU_ScheduleService.md)** - Horarios y fichas
- **[Attendance Service](../be/HU_AttendanceService.md)** - Control de asistencia
- **[Evalin Service](../be/HU_EvalinService.md)** - Evaluación de instructores
- **[AI Service](../be/HU_AIService.md)** - Asistente virtual
- **[KB Service](../be/HU_KbService.md)** - Base de conocimiento

### **🔧 Documentación Técnica:**

- **[Especificación API](../../api/endpoints_specification.md)** - Contratos RESTful
- **[Runbook Operaciones](../../technical/SICORA-OPERATIONS-RUNBOOK.md)** - Procedimientos
- **[Monitoreo](../../technical/SICORA-MONITORING-SETUP.md)** - Observabilidad

---

## 🏗️ **ARQUITECTURA Y DISEÑO**

### **📱 Estrategia Mobile First**

- **Responsive Design**: TailwindCSS con breakpoints mobile-first
- **Progressive Web App**: PWA capabilities para experiencia nativa
- **Offline Support**: Cache inteligente para funcionalidades críticas
- **Performance**: Lazy loading, code splitting, optimización de bundle

### **🎭 Roles y Experiencias**

#### **👑 Administrador**

- Dashboard ejecutivo con métricas generales
- Gestión completa de usuarios y roles
- Configuración de horarios y ambientes
- Reportes y analytics avanzados
- Administración de evaluaciones

#### **👨‍🏫 Instructor**

- Dashboard personal con agenda del día
- Gestión de asistencia de estudiantes
- Consulta de horarios asignados
- Acceso a recursos de knowledge base
- Evaluación de proyectos estudiantiles

#### **🎓 Aprendiz**

- Dashboard estudiantil personalizado
- Consulta de horarios de clase
- Registro de asistencia (QR/biométrico)
- Acceso a material educativo
- Seguimiento de evaluaciones

### **🔄 Flujos de Navegación**

#### **Flujo Principal**

```
Splash Screen → Login → Dashboard (por rol) → Funcionalidades específicas
```

#### **Flujo de Autenticación**

```
Login → Validación → [Cambio contraseña obligatorio] → Dashboard
```

#### **Flujo de Asistencia**

```
Dashboard → Asistencia → [QR Scanner | Manual] → Confirmación
```

#### **Flujo de Evaluaciones**

```
Dashboard → Evaluaciones → Lista → Formulario → Envío → Confirmación
```

---

## 🔗 **INTEGRACIONES FRONTEND-BACKEND**

### **Dependencias Críticas por Área**

| Área Frontend       | Servicios Backend Principales      | Dependencias Secundarias       | Prioridad |
| ------------------- | ---------------------------------- | ------------------------------ | --------- |
| **Authentication**  | APIGateway, UserService            | -                              | CRÍTICA   |
| **Core App**        | UserService                        | Todos (dashboard)              | CRÍTICA   |
| **User Management** | UserService                        | APIGateway                     | ALTA      |
| **Schedule**        | ScheduleService                    | UserService, AttendanceService | ALTA      |
| **Attendance**      | AttendanceService, ScheduleService | UserService                    | ALTA      |
| **Evaluations**     | EvalinService, EvalProyService     | UserService, ScheduleService   | MEDIA     |
| **Knowledge Base**  | KbService                          | AIService, UserService         | MEDIA     |
| **AI Assistant**    | AIService, KbService               | UserService                    | BAJA      |
| **Academic Mgmt**   | AcadService, MevalService          | UserService, ScheduleService   | MEDIA     |
| **Reports**         | Todos los servicios                | UserService                    | BAJA      |

### **🔄 Flujos de Datos Típicos**

#### **Autenticación:**

1. **Frontend** → Envía credenciales a APIGateway
2. **APIGateway** → Valida con UserService
3. **UserService** → Retorna token JWT y perfil
4. **Frontend** → Almacena token y configura contexto de usuario

#### **Dashboard:**

1. **Frontend** → Solicita datos del dashboard por rol
2. **APIGateway** → Valida token y enruta a servicios
3. **Múltiples servicios** → Retornan datos específicos por rol
4. **Frontend** → Renderiza dashboard personalizado

#### **Asistencia:**

1. **Frontend** → Captura datos de asistencia (QR/manual)
2. **APIGateway** → Valida y enruta a AttendanceService
3. **AttendanceService** → Valida con ScheduleService
4. **Frontend** → Muestra confirmación al usuario

---

## 🎯 **CRITERIOS DE CALIDAD FRONTEND**

### **📱 UX/UI**

- **Tiempo de carga inicial**: < 3 segundos
- **Tiempo de navegación**: < 1 segundo entre pantallas
- **Responsive**: Soporte desde 320px hasta 2560px
- **Accesibilidad**: WCAG 2.1 nivel AA
- **Usabilidad**: Máximo 3 clics para funciones principales

### **⚡ Performance**

- **Bundle size**: < 2MB total
- **First Contentful Paint**: < 1.5 segundos
- **Time to Interactive**: < 3 segundos
- **Lighthouse Score**: > 90 en todas las métricas

### **🔒 Seguridad**

- **Token management**: Almacenamiento seguro y rotación automática
- **HTTPS**: Comunicación encriptada obligatoria
- **XSS Protection**: Sanitización de inputs
- **CORS**: Configuración restrictiva

### **🧪 Testing**

- **Unit Tests**: > 80% cobertura de componentes
- **Integration Tests**: Flujos principales cubiertos
- **E2E Tests**: Casos críticos automatizados
- **Visual Regression**: Screenshots automáticos

---

## 📈 **ROADMAP DE DESARROLLO**

### **🚀 Fase 1: Core y Autenticación (Sprint 1-2)**

- ✅ Configuración inicial del proyecto
- 🚧 Core App (splash, navigation, layouts)
- 🚧 Authentication (login, logout, forgot password)
- 📋 User Management básico

### **📅 Fase 2: Funcionalidades Principales (Sprint 3-5)**

- 📋 Schedule Management
- 📋 Attendance Control
- 📋 Basic Dashboards por rol

### **📊 Fase 3: Evaluaciones y Gestión (Sprint 6-8)**

- 📋 Evaluation Systems
- 📋 Academic Management
- 📋 Knowledge Base Integration

### **🤖 Fase 4: IA y Analytics (Sprint 9-10)**

- 📋 AI Assistant Integration
- 📋 Reports & Analytics
- 📋 Advanced Features

---

## 📝 **NOTAS DE IMPLEMENTACIÓN**

### **🔄 Estado de Migración de Documentación Legacy**

Los siguientes archivos legacy han sido consolidados en la nueva estructura:

- ✅ `historias_usuario_fe.md` → Distribuido en archivos HU*FE*\*
- ✅ `criterios_aceptacion_fe.md` → Integrado en cada archivo HU*FE*\*
- ✅ `historias_usuario_fe_evalinservice.md` → HU_FE_Evaluations.md
- ✅ `historias_usuario_fe_kbservice.md` → HU_FE_KnowledgeBase.md

### **📁 Estructura de Archivos**

Cada archivo `HU_FE_*.md` contiene:

- **Historias de usuario** específicas del área
- **Criterios de aceptación** técnicos y funcionales
- **Mockups/Wireframes** de referencia
- **Casos de uso** principales
- **Integraciones** con backend
- **Testing** específico

---

**Notas:** Esta estructura establece la base para el desarrollo incremental del frontend de SICORA, organizando las historias por áreas funcionales coherentes y priorizando según las dependencias del backend y la experiencia del usuario.
