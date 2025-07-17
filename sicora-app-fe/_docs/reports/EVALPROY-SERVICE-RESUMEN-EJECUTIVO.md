# 📊 **EVALPROY SERVICE - RESUMEN EJECUTIVO**

**Módulo:** EvalProy (Evaluación de Proyectos de Formación)  
**Fecha:** 17 de junio de 2025  
**Estado:** 📋 **DOCUMENTACIÓN COMPLETA**  
**Prioridad:** 🔥 **CRÍTICA** - Proceso central de formación ADSO/PSW

---

## 🎯 **DESCRIPCIÓN EJECUTIVA**

El **EvalProy Service** es el sistema de evaluación del **hito más importante** de los programas ADSO y PSW: el desarrollo de proyectos formativos reales. Gestiona el ciclo completo desde la propuesta de ideas hasta la entrega final, involucrando stakeholders externos y aplicando metodologías de evaluación profesional.

### **🔥 Valor de Negocio**

- **Centraliza** el proceso de evaluación más crítico del SENA
- **Estandariza** metodologías de seguimiento entre instructores
- **Mejora** la calidad de proyectos mediante evaluación sistemática
- **Vincula** aprendizaje académico con necesidades reales del mercado
- **Mantiene control académico** sobre alcance y cronograma del proyecto
- **Gestiona expectativas** de stakeholders externos de manera sistemática
- **Protege propiedad intelectual** institucional del SENA

---

## 📚 **DOCUMENTACIÓN CREADA**

| Documento                                                                | Descripción                                     | Estado      |
| ------------------------------------------------------------------------ | ----------------------------------------------- | ----------- |
| **[rf_evalproy.md](../general/rf_evalproy.md)**                          | Requisitos funcionales completos con gobernanza | ✅ Completo |
| **[historias_usuario_evalproy.md](historias_usuario_evalproy.md)**       | 50 historias de usuario detalladas              | ✅ Completo |
| **[criterios_aceptacion_evalproy.md](criterios_aceptacion_evalproy.md)** | Criterios específicos por HU                    | ✅ Completo |

---

## 📊 **ESTADÍSTICAS DEL PROYECTO**

### **Alcance Funcional**

- **50 Historias de Usuario** distribuidas entre 4 actores
- **12 Requisitos Funcionales** principales (incluyendo gobernanza)
- **3 Fases de implementación** planificadas
- **4 Integraciones** con otros servicios
- **Controles de gobernanza** para gestión de stakeholders

### **Distribución por Actor**

| Actor               | Historias | % del Total | Prioridad |
| ------------------- | --------- | ----------- | --------- |
| **Instructores**    | 23        | 46%         | Crítica   |
| **Aprendices**      | 15        | 30%         | Alta      |
| **Administradores** | 10        | 20%         | Media     |
| **Stakeholders**    | 4         | 4%          | Baja      |

---

## 🔒 **ASPECTOS CRÍTICOS DE GOBERNANZA**

### **Control Académico Absoluto**

- **Solo instructores** pueden modificar alcance, cronograma y grupos
- **Stakeholders** tienen rol **consultivo**, no decisorio
- **Todas las decisiones** deben tener justificación pedagógica
- **Sistema bloquea** automáticamente modificaciones no autorizadas

### **Gestión de Expectativas de Stakeholders**

- **Limitaciones claras** de tiempo y recursos comunicadas desde inicio
- **Proceso formal** para solicitudes de cambio con evaluación académica
- **Comunicación automática** de decisiones con justificación
- **Alertas de riesgo** cuando stakeholder excede límites razonables

### **Protección de Propiedad Intelectual**

- **Propiedad del SENA** sobre todo código y documentación generada
- **Derechos de uso** del stakeholder claramente definidos
- **Responsabilidades post-formación** documentadas
- **Transferencia controlada** de conocimiento y sistemas

### **Preparación para Despliegue Real**

- **Objetivo:** Proyecto técnicamente desplegable en cliente
- **Documentación completa** para transición
- **Capacitación básica** incluida en proceso formativo
- **Calidad profesional** según estándares institucionales

---

## 🏗️ **ARQUITECTURA Y DISEÑO**

### **Patrón Arquitectónico**

- **Clean Architecture** (siguiendo estándar del proyecto)
- **Domain-Driven Design** para modelar proceso académico
- **CQRS** para separar lecturas/escrituras complejas
- **Event Sourcing** para auditoría completa

### **Integraciones Requeridas**

```
EvalProy --> UserService (Autenticación y roles)
EvalProy --> ScheduleService (Programación de sesiones)
EvalProy --> KbService (Plantillas y documentación)
EvalProy --> EvalinService (Evaluación de instructores)
```

### **Tecnologías Principales**

- **Backend:** FastAPI + Python 3.13
- **Base de Datos:** PostgreSQL 15
- **Autenticación:** JWT tokens
- **Documentación:** OpenAPI/Swagger
- **Testing:** Pytest + Coverage

---

## 🚀 **ROADMAP DE IMPLEMENTACIÓN**

### **📅 Fase 1: Core Functionality (4 semanas)**

**Prioridad:** Crítica

**Sprint 1 (Semana 1-2): Gestión de Ideas y Gobernanza**

- [ ] HU-EVALPROY-APR-001: Registrar Idea de Proyecto
- [ ] HU-EVALPROY-APR-002: Ver Mis Ideas Registradas
- [ ] HU-EVALPROY-INS-001: Evaluar Ideas de Proyecto
- [ ] HU-EVALPROY-INS-020: Controlar Modificaciones de Alcance

**Sprint 2 (Semana 3-4): Sesiones de Evaluación**

- [ ] HU-EVALPROY-INS-004: Programar Sesión de Evaluación
- [ ] HU-EVALPROY-APR-006: Ver Próximas Sesiones de Evaluación
- [ ] HU-EVALPROY-INS-010: Calificar Avances Trimestrales
- [ ] HU-EVALPROY-INS-019: Gestionar Solicitudes de Cambio de Stakeholder

### **📅 Fase 2: Advanced Features (3 semanas)**

**Prioridad:** Alta

- [ ] Gestión completa de stakeholders con limitaciones
- [ ] Reportes y analytics avanzados
- [ ] Preparación para despliegue
- [ ] Notificaciones automáticas

### **📅 Fase 3: Optimization (2 semanas)**

**Prioridad:** Media

- [ ] Integración con repositorios Git
- [ ] Machine Learning para recomendaciones
- [ ] Portal dedicado para stakeholders
- [ ] Métricas predictivas de éxito

---

## 🎯 **ENTIDADES PRINCIPALES**

### **Domain Entities**

```
Project (Proyecto)
├── project_id: UUID
├── group_id: UUID
├── title: str
├── description: str
├── stakeholder_info: dict
├── status: ProjectStatus
├── selected_idea_id: UUID
├── intellectual_property_owner: "SENA"
└── created_at: datetime

ProjectIdea (Idea de Proyecto)
├── idea_id: UUID
├── group_id: UUID
├── title: str
├── description: str
├── technologies: List[str]
├── feasibility_score: float
├── is_selected: bool
└── evaluation_status: IdeaStatus

EvaluationSession (Sesión de Evaluación)
├── session_id: UUID
├── session_date: datetime
├── trimester: int
├── evaluators: List[UUID]
├── groups: List[UUID]
├── checklist_template_id: UUID
└── status: SessionStatus

ChangeRequest (Solicitud de Cambio)
├── request_id: UUID
├── project_id: UUID
├── stakeholder_id: UUID
├── requested_change: str
├── academic_evaluation: str
├── approval_status: RequestStatus
├── instructor_decision: str
└── created_at: datetime

ProjectProgress (Avance de Proyecto)
├── progress_id: UUID
├── project_id: UUID
├── trimester: int
├── description: str
├── deliverables: List[File]
├── completion_percentage: float
└── submitted_at: datetime
```

---

## 📈 **MÉTRICAS Y KPIS**

### **Indicadores Académicos**

- **Tasa de Finalización:** >85% de proyectos completados exitosamente
- **Satisfacción Stakeholder:** >3.5/5.0 (considerando limitaciones)
- **Calidad de Entregas:** >80% cumplen criterios mínimos
- **Aplicación de Conocimientos:** >90% aplican tecnologías del programa

### **Indicadores Operativos**

- **Cumplimiento Cronograma:** >95% sesiones realizadas a tiempo
- **Eficiencia Evaluación:** <30 min promedio por evaluación
- **Adopción Sistema:** >90% instructores usando vs. método manual
- **Disponibilidad Sistema:** >99.5% durante períodos académicos

### **Indicadores de Gobernanza**

- **Control de Cambios:** <30% solicitudes de stakeholder rechazadas
- **Tiempo de Respuesta:** <48h para solicitudes de stakeholder
- **Mantenimiento de Alcance:** >70% proyectos mantienen alcance original
- **Preparación para Despliegue:** >80% proyectos técnicamente desplegables

### **Indicadores de Calidad**

- **Consistencia Evaluación:** <15% variación entre jurados
- **Tiempo Retroalimentación:** <48 horas post-evaluación
- **Precisión Datos:** <1% errores en calificaciones
- **Satisfacción Usuario:** >4.2/5.0 en encuestas de usabilidad

---

## 🔧 **CONSIDERACIONES TÉCNICAS**

### **Escalabilidad**

- **Capacidad:** 500+ proyectos simultáneos
- **Usuarios Concurrentes:** 200+ sin degradación
- **Almacenamiento:** 10GB+ por semestre académico
- **Integración:** API REST con rate limiting

### **Seguridad**

- **Autenticación:** JWT con refresh tokens
- **Autorización:** RBAC granular por funcionalidad
- **Auditoría:** Log completo de cambios críticos y decisiones de gobernanza
- **Privacidad:** Encriptación de datos sensibles y protección IP

### **Mantenimiento**

- **Backup:** Diario automático con retención 2 años
- **Monitoreo:** Alertas automáticas de problemas y violaciones de gobernanza
- **Actualización:** Rolling updates sin downtime
- **Soporte:** Documentación técnica completa

---

## 🏆 **CRITERIOS DE ÉXITO**

### **Criterios Técnicos**

- [ ] ✅ API RESTful completamente funcional
- [ ] ✅ Tests unitarios >90% coverage
- [ ] ✅ Tests de integración completos
- [ ] ✅ Documentación Swagger actualizada
- [ ] ✅ Performance cumple SLAs definidos

### **Criterios de Negocio**

- [ ] ✅ Todas las HU prioritarias implementadas
- [ ] ✅ Flujo de evaluación end-to-end funcional
- [ ] ✅ Sistema de gobernanza operativo
- [ ] ✅ Integración con UserService operativa
- [ ] ✅ Reportes básicos disponibles

### **Criterios de Gobernanza**

- [ ] ✅ Control de autoridad académica funcional
- [ ] ✅ Gestión de stakeholders con limitaciones operativa
- [ ] ✅ Proceso de solicitud de cambios implementado
- [ ] ✅ Protección de propiedad intelectual asegurada
- [ ] ✅ Preparación para despliegue validada

### **Criterios de Adopción**

- [ ] ✅ Capacitación a instructores completada
- [ ] ✅ Migración de datos históricos exitosa
- [ ] ✅ Piloto con 2+ programas ejecutado
- [ ] ✅ Feedback positivo de usuarios finales
- [ ] ✅ Proceso de soporte establecido

---

## 🔄 **SIGUIENTES PASOS**

### **Inmediatos (Esta Semana)**

1. **Análisis Técnico Detallado**
   - Definir esquemas de base de datos
   - Diseñar APIs principales
   - Establecer estructura de proyectos

2. **Setup de Desarrollo**
   - Crear estructura FastAPI base
   - Configurar CI/CD pipeline
   - Establecer entorno de testing

### **Corto Plazo (Próximo Mes)**

1. **Desarrollo Sprint 1**
   - Implementar gestión de ideas
   - Crear interfaces de evaluación
   - Establecer controles de gobernanza

2. **Validación con Usuarios**
   - Demos con instructores clave
   - Feedback de coordinadores académicos
   - Ajustes basados en retroalimentación

---

## 📞 **EQUIPO Y CONTACTOS**

### **Stakeholders Clave**

- **Coordinación Académica:** Validación de procesos y gobernanza
- **Instructores ADSO/PSW:** Usuarios finales principales
- **Desarrollo de Software:** Implementación técnica
- **QA/Testing:** Validación de calidad y criterios de aceptación

### **Cronograma de Revisiones**

- **Semanal:** Progreso técnico con equipo desarrollo
- **Quincenal:** Validación funcional con instructores
- **Mensual:** Revisión ejecutiva con coordinación
- **Por fase:** Validación de criterios de gobernanza

---

## ⚠️ **CONSIDERACIONES ESPECIALES**

### **Gestión de Stakeholders Problemáticos**

- **Protocolo definido** para stakeholders que exceden límites
- **Escalamiento automático** a coordinación académica
- **Documentación completa** de interacciones problemáticas
- **Sesiones de clarificación** de expectativas cuando sea necesario

### **Protección de Propiedad Intelectual**

- **Avisos legales** claros en toda la documentación
- **Acuerdos firmados** con stakeholders sobre derechos
- **Registro automático** de autoría institucional
- **Proceso de transferencia** controlado y documentado

### **Preparación para Auditoria**

- **Trazabilidad completa** de todas las decisiones
- **Justificación pedagógica** de cambios de alcance
- **Evidencia documentada** de control académico
- **Métricas de cumplimiento** de políticas institucionales

---

**🎯 El EvalProy Service representa la digitalización del proceso más crítico de formación en los programas ADSO y PSW, conectando el aprendizaje académico con las necesidades reales del mercado laboral a través de proyectos formativos con stakeholders externos, mientras mantiene firmemente la autoridad académica sobre todas las decisiones del proyecto.**
