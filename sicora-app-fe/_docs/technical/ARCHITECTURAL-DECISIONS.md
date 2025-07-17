# 📋 Decisiones Arquitectónicas - SICORA-APP Multistack

**Fecha**: 16 de junio de 2025  
**Documento**: Registro de decisiones importantes del proyecto

---

## 🎯 **ADR-001: Frontend Único vs Multistack**

### **Decisión**

Implementar **un frontend único** (React Vite) que consume **6 backends diferentes**.

### **Contexto**

Se evaluaron dos opciones:

- A) Un frontend por stack (6 frontends)
- B) Un frontend único para todos los stacks

### **Decisión Tomada: Opción B**

**Razones:**

- ✅ **Comparación directa** entre tecnologías backend
- ✅ **Foco en arquitectura backend** y Clean Architecture
- ✅ **Simplifica testing** y mantenimiento
- ✅ **Valor educativo** más claro para estudiantes
- ✅ **Evaluación objetiva** de rendimiento

### **Consecuencias**

- **Positivas**: Consistencia, simplicidad, comparación directa
- **Negativas**: No demuestra capacidades frontend de cada stack
- **Mitigación**: Documentar características únicas de cada backend

---

## 🚀 **ADR-002: Next.js Backend Only**

### **Decisión**

Implementar **Next.js exclusivamente como backend** usando API Routes, sin componentes frontend.

### **Contexto**

Next.js tiene capacidad full-stack, pero se evaluó:

- A) Next.js full-stack (frontend + backend)
- B) Next.js solo backend (API Routes)

### **Decisión Tomada: Opción B**

**Razones:**

- ✅ **Mantiene consistencia** con ADR-001 (frontend único)
- ✅ **Aprovecha características únicas** (Edge Functions, middleware)
- ✅ **Facilita comparación** con otros stacks backend
- ✅ **Evita conflictos** con React Vite frontend
- ✅ **Foco en diferenciadores** de Next.js como backend

### **Características Únicas Implementadas**

- **Edge Functions** para operaciones ultra-rápidas
- **Middleware nativo** para auth/logging global
- **Streaming APIs** para bulk operations
- **TypeScript zero-config** con inferencia completa

### **Consecuencias**

- **Positivas**: Consistencia arquitectónica, aprovecha ventajas únicas
- **Negativas**: No demuestra SSR/SSG de Next.js
- **Mitigación**: Documentar diferenciadores específicos de backend

---

## 📊 **ADR-003: Shared-Data Centralizada**

### **Decisión**

Crear directorio **shared-data/** centralizado para operaciones de carga masiva.

### **Contexto**

Los 6 stacks necesitan acceso a los mismos datos para:

- Importación masiva de usuarios
- Datos de ejemplo para testing
- Templates y esquemas de validación

### **Decisión Tomada: Estructura Centralizada**

**Estructura:**

```
shared-data/
├── imports/     # Datos fuente (PROTEGIDO)
├── templates/   # Plantillas sin datos
├── exports/     # Por stack (PROTEGIDO)
├── samples/     # Ejemplos sintéticos
└── schemas/     # Validación JSON
```

**Razones:**

- ✅ **Consistencia** de datos entre stacks
- ✅ **Reutilización** de assets de datos
- ✅ **Protección** de datos sensibles
- ✅ **Herramientas comunes** para todos los stacks

### **Consecuencias**

- **Positivas**: Consistencia, seguridad, reutilización
- **Negativas**: Dependencia central, posible cuello de botella
- **Mitigación**: Symlinks, herramientas automatizadas

---

## 🏗️ **ADR-004: Clean Architecture Consistente**

### **Decisión**

Aplicar **Clean Architecture idéntica** en los 6 stacks con nomenclatura consistente.

### **Estructura Estándar**

```
{stack}/userservice/
├── domain/          # Entities, business rules
├── application/     # Use cases, DTOs
├── infrastructure/  # Repositories, external services
└── interfaces/      # Controllers, routes
```

### **Razones**

- ✅ **Facilita migración** entre stacks
- ✅ **Patrones consistentes** para equipos
- ✅ **Valor educativo** maximizado
- ✅ **Mantenibilidad** a largo plazo

### **Adaptaciones por Stack**

- **Python**: Módulos + dataclasses
- **Go**: Packages + structs
- **JavaScript**: Classes + modules
- **TypeScript**: Interfaces + classes
- **Java**: Packages + annotations
- **Kotlin**: Data classes + coroutines

---

## 🚢 **ADR-005: Docker Compose Unificado**

### **Decisión**

Un solo **docker-compose.yml** que orquesta todos los stacks + infraestructura.

### **Contexto**

Se evaluó:

- A) Docker compose por stack
- B) Docker compose unificado

### **Decisión Tomada: Opción B**

**Servicios incluidos:**

- PostgreSQL 15 (base de datos común)
- Redis (caché)
- Nginx (proxy reverso)
- 6 servicios backend en paralelo

**Razones:**

- ✅ **Setup simplificado** para desarrollo
- ✅ **Infraestructura compartida** eficiente
- ✅ **Testing integral** del sistema completo
- ✅ **Simulación realista** de producción

---

## 📋 **ADR-006: Puertos Estandarizados**

### **Decisión**

Asignar **puertos fijos** por stack para consistencia.

### **Asignación**

- **8001** - FastAPI (referencia)
- **8002** - Go
- **8003** - Express
- **8004** - Next.js
- **8005** - Java Spring Boot
- **8006** - Kotlin Spring Boot

### **Razones**

- ✅ **Predictibilidad** para desarrollo
- ✅ **Configuración de proxy** simplificada
- ✅ **Testing automatizado** más fácil
- ✅ **Documentación clara** por stack

---

## 🧪 **ADR-007: Estrategia de Testing**

### **Decisión**

**Testing por capas** consistente en todos los stacks.

### **Estructura de Testing**

```
tests/
├── unit/           # Por capa (domain, application)
├── integration/    # Infrastructure + interfaces
└── e2e/           # APIs completas
```

### **Herramientas por Stack**

- **Python**: pytest + FastAPI TestClient
- **Go**: testing package + testify
- **JavaScript**: Jest + supertest
- **TypeScript**: Jest + @types/jest
- **Java**: JUnit 5 + Spring Test
- **Kotlin**: JUnit 5 + Kotest

---

## 📈 **ADR-008: Métricas y Monitoreo**

### **Decisión**

**Métricas consistentes** para comparación objetiva entre stacks.

### **Métricas Clave**

- **Performance**: Throughput, latencia, memoria
- **Funcionales**: Cobertura de tests, bugs por stack
- **Desarrollo**: Velocidad de implementación, complejidad

### **Herramientas**

- Prometheus + Grafana (métricas)
- Logging estructurado por stack
- Benchmarks automatizados

---

## 🧩 **ADR-004: Estrategia Híbrida de Atomic Design**

### **Decisión**

Implementar **Atomic Design selectivo** solo para componentes específicos que requieren alta reutilización, no para toda la aplicación.

### **Contexto**

Se evaluaron dos enfoques para la organización de componentes:

- A) Atomic Design completo para todos los componentes
- B) Atomic Design híbrido solo para componentes críticos
- C) Estructura plana sin metodología específica

### **Decisión Tomada: Opción B - Atomic Design Híbrido**

**Razones:**

- ✅ **Evita overhead innecesario** de full atomic design
- ✅ **Enfoque pragmático** sobre dogmático
- ✅ **Beneficios del 80/20**: máximo valor con mínimo overhead
- ✅ **Facilita aprendizaje** progresivo para estudiantes
- ✅ **Flexibilidad** para ajustar según necesidades reales

### **Componentes Seleccionados para Atomic Design**

#### **Átomos (Nivel 1) - Solo Componentes Críticos**

```
atoms/
├── TouchButton/     # Botón optimizado para mobile
├── TouchInput/      # Input con touch targets
├── StatusBadge/     # Indicadores de estado
└── LoadingSpinner/  # Indicador de carga
```

#### **Moléculas (Nivel 2) - Combinaciones Esenciales**

```
molecules/
├── LoginForm/       # Formulario de autenticación
├── UserCard/        # Tarjeta de usuario reutilizable
├── AttendanceRow/   # Fila de asistencia
└── SearchInput/     # Búsqueda con filtros
```

#### **Organismos (Nivel 3) - Secciones Complejas**

```
organisms/
├── MobileAttendanceList/  # Lista optimizada mobile
├── AdaptiveNavigation/    # Navegación responsive
└── DashboardHeader/       # Header con user info
```

#### **Templates (Nivel 4) - Layouts Base**

```
templates/
├── AdaptiveLayout/        # Layout principal responsive
├── AuthLayout/            # Layout para autenticación
└── EmptyStateLayout/      # Estados vacíos
```

### **Criterios de Selección**

Un componente entra en Atomic Design solo si cumple **AL MENOS 2** de estos criterios:

1. **Reutilización Alta**: Se usa en 3+ pantallas diferentes
2. **Consistencia Crítica**: Variaciones generan problemas UX
3. **Complejidad Mobile**: Requiere optimización táctil específica
4. **Valor Educativo**: Demuestra conceptos importantes para estudiantes
5. **Testing Complejo**: Necesita testing aislado por estados/variantes

### **Componentes EXCLUIDOS de Atomic Design**

- **Páginas específicas** (ProfilePage, SettingsPage)
- **Componentes de una sola vez** (SpecificErrorModal)
- **Wrappers simples** que solo agregan estilos
- **Lógica de negocio específica** del dominio

### **Estructura de Directorios Resultante**

```
src/
├── components/
│   ├── atoms/         # Solo 4-6 componentes críticos
│   ├── molecules/     # Solo 4-8 combinaciones esenciales
│   ├── organisms/     # Solo 3-5 secciones complejas
│   ├── templates/     # Solo 3-4 layouts base
│   ├── pages/         # Páginas específicas (estructura plana)
│   └── features/      # Componentes específicos por funcionalidad
├── hooks/             # Custom hooks reutilizables
├── services/          # Clients API por backend stack
├── utils/             # Funciones utilitarias
├── types/             # Definiciones TypeScript
└── styles/            # CSS global y configuración Tailwind
```

### **Métricas de Éxito**

#### **Señales Positivas (Continuar con Atomic Design)**

- ✅ Nuevas pantallas se ensamblan rápidamente
- ✅ Cambios visuales se propagan automáticamente
- ✅ Componentes se reutilizan sin modificaciones
- ✅ Testing de componentes es natural y útil
- ✅ Nuevos desarrolladores contribuyen sin inconsistencias

#### **Señales de Alerta (Revisar Enfoque)**

- ⚠️ Más tiempo categorizando que implementando
- ⚠️ Creación de wrappers solo por jerarquía
- ⚠️ Cambios simples requieren múltiples niveles
- ⚠️ Desarrolladores evitan reutilizar componentes
- ⚠️ Debates constantes sobre ubicación de componentes

### **Integración con Storybook**

Solo componentes en atomic design tendrán stories en Storybook:

```
.storybook/
├── atoms/           # Stories de átomos
├── molecules/       # Stories de moléculas
├── organisms/       # Stories de organismos
└── templates/       # Stories de layouts
```

**Beneficios:**

- **Documentación automática** de componentes reutilizables
- **Testing visual** de variantes y estados
- **Exploración** fácil para nuevos desarrolladores
- **Playground** para probar props y comportamientos

### **Consecuencias**

#### **Positivas**

- ✅ **Desarrollo ágil**: Overhead mínimo, beneficios máximos
- ✅ **Aprendizaje progresivo**: Estudiantes ven valor inmediato
- ✅ **Flexibilidad**: Fácil adaptación según necesidades reales
- ✅ **Consistencia selectiva**: Solo donde importa
- ✅ **Performance**: Menos abstracciones innecesarias

#### **Negativas**

- ⚠️ **Vigilancia requerida**: Evitar atomic design creep
- ⚠️ **Criterios subjetivos**: Decisiones caso por caso
- ⚠️ **Documentación extra**: Explicar qué va donde

#### **Mitigación**

- **Revisiones regulares** de estructura (cada 2 sprints)
- **Documentación clara** de criterios de selección
- **Ejemplos concretos** de qué incluir/excluir
- **Refactoring periódico** basado en uso real

### **Alineación con Mobile-First y SENA**

Esta estrategia se alinea perfectamente con:

- **Mobile-First**: Componentes críticos optimizados para touch
- **Identidad SENA**: Consistencia visual en elementos corporativos
- **Pragmatismo educativo**: Enseña conceptos sin overhead prohibitivo
- **Escalabilidad**: Permite crecimiento orgánico según necesidades

---

## 🔄 **Proceso de Revisión**

### **Frecuencia**

- **ADRs**: Se revisan cada sprint major
- **Decisiones menores**: En retrospectivas
- **Cambios críticos**: Requieren consenso del equipo

### **Criterios de Cambio**

- Evidencia de que la decisión causa problemas
- Nueva información que invalida supuestos
- Beneficios claros del cambio vs costo

---

## 📚 **Referencias**

- [Clean Architecture - Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Architecture Decision Records](https://adr.github.io/)
- [Microservices Patterns - Chris Richardson](https://microservices.io/)

---

**Este documento se actualiza con cada decisión arquitectónica importante del proyecto.**
