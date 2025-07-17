# 📋 **REQUISITOS FUNCIONALES - EVALPROY SERVICE**

**Módulo:** EvalProy (Evaluación de Proyectos de Formación)  
**Fecha:** 17 de junio de 2025  
**Versión:** 1.0  
**Contexto:** Sistema SICORA - CGMLTI SENA

---

## 🎯 **PROPÓSITO DEL MÓDULO**

El **EvalProy Service** es el sistema de evaluación del **hito más importante** de los programas de formación ADSO (Análisis y Desarrollo de Software) y PSW (Programación de Software). Gestiona el ciclo completo de evaluación de proyectos formativos donde los aprendices desarrollan software real para stakeholders externos, aplicando todos los conocimientos adquiridos desde el segundo trimestre.

---

## 🏗️ **CONTEXTO PEDAGÓGICO**

### **Importancia del Proyecto Formativo**

- **Proyecto principal** de los programas ADSO y PSW
- **Software orientado a web** como preferencia tecnológica
- **Stakeholders reales** en la mayoría de casos
- **Aplicación práctica** de todos los conocimientos del programa
- **Desarrollo incremental** a lo largo de múltiples trimestres

### **Metodología de Evaluación**

- **Sesiones de seguimiento** trimestrales (1-2 por trimestre)
- **Jurados evaluadores** (2 o más instructores)
- **Grupos de trabajo** (3-5 aprendices por grupo). Recomendar número impar.
- **Lista de chequeo** como base de evaluación
- **Presentaciones y desarrollo** de ideas y avances

### **Ciclo de Desarrollo del Proyecto**

1. **Trimestre II:** Presentación de mínimo 3 ideas de proyecto
2. **Trimestre II:** Viabilización y aceptación de 1 idea
3. **Trimestre III-VII:** Desarrollo incremental del software
4. **Cada trimestre:** Evaluación de avances según formación recibida

---

## 👥 **ACTORES DEL SISTEMA**

### **🎓 Aprendices**

- **Responsabilidad:** Desarrollar y presentar proyectos formativos
- **Agrupación:** Grupos de 3-5 estudiantes
- **Actividades:** Proponer ideas, desarrollar software, presentar avances

### **👨‍🏫 Instructores (Jurados)**

- **Responsabilidad:** Evaluar proyectos y dar seguimiento
- **Agrupación:** 2 o más por sesión de evaluación
- **Actividades:** Evaluar ideas, dar feedback, calificar avances

### **🏛️ Administradores/Coordinadores**

- **Responsabilidad:** Gestionar proceso de evaluación
- **Actividades:** Configurar evaluaciones, asignar jurados, generar reportes

### **🏢 Stakeholders Externos**

- **Responsabilidad:** Proporcionar contexto real al proyecto (ROL CONSULTIVO)
- **Actividades:** Definir requisitos iniciales, validar soluciones, dar feedback

---

## ⚖️ **GOBERNANZA Y LIMITACIONES DEL PROYECTO**

### **🏛️ Autoridad Académica vs. Stakeholder**

#### **Decisiones que SOLO pueden tomar Instructores/Equipo Pedagógico:**

- **Cambios en alcance del proyecto** (adición/reducción de funcionalidades)
- **Modificación de cronograma** académico
- **Reasignación de grupos** de trabajo
- **Cambios en metodología** de desarrollo
- **Modificación de tecnologías** a utilizar
- **Extensión de plazos** de entrega
- **Evaluación final** del proyecto

#### **Participación del Stakeholder (NO Decisoria):**

- **Proporcionar requisitos funcionales** iniciales
- **Dar retroalimentación** sobre avances
- **Validar funcionalidades** desarrolladas
- **Sugerir mejoras** dentro del alcance establecido
- **Participar en demostraciones** programadas

### **🔒 Propiedad Intelectual y Derechos**

#### **Propiedad del SENA:**

- **Código fuente completo** desarrollado durante la formación
- **Documentación técnica** generada
- **Metodologías** aplicadas en el desarrollo
- **Innovaciones** técnicas implementadas
- **Bases de datos** y estructuras de información

#### **Derechos del Stakeholder:**

- **Uso del software** desarrollado para sus operaciones
- **Capacitación** en el uso del sistema
- **Soporte básico** durante período formativo
- **Documentación de usuario** del sistema

### **💰 Responsabilidades Financieras**

#### **Costos Asumidos por el SENA:**

- **Infraestructura de desarrollo** (servidores, herramientas)
- **Licencias de software** necesarias
- **Horas de instructor** para supervisión
- **Recursos tecnológicos** de aprendices
- **Despliegue inicial** en ambiente de producción

#### **Responsabilidades del Stakeholder:**

- **Hosting y mantenimiento** posterior al período formativo
- **Actualizaciones futuras** del sistema
- **Soporte técnico** post-entrega
- **Infraestructura productiva** propia
- **Respaldos y seguridad** de datos

### **⚠️ Gestión de Expectativas del Stakeholder**

#### **Limitaciones Temporales:**

- **Duración máxima:** Según cronograma académico (no extensible)
- **Horas disponibles:** Limitadas por carga académica de aprendices
- **Revisiones:** Máximo 2 por trimestre según calendario
- **Cambios mayores:** Solo en períodos de transición trimestral

#### **Limitaciones de Alcance:**

- **Funcionalidades:** Deben estar alineadas con competencias del programa
- **Tecnologías:** Restringidas a stack académico definido
- **Integración:** Solo con sistemas accesibles desde ambiente académico
- **Complejidad:** Apropiada para nivel de aprendices por trimestre

#### **Proceso de Gestión de Cambios:**

1. **Solicitud del stakeholder** documentada
2. **Evaluación pedagógica** por instructores
3. **Análisis de viabilidad** técnica y temporal
4. **Decisión final** del equipo pedagógico
5. **Comunicación formal** de la decisión
6. **Documentación** del cambio aprobado/rechazado

### **🎯 Objetivo de Despliegue Post-Formación**

#### **Meta Ideal:**

- El proyecto debe ser **técnicamente desplegable** en el cliente
- **Documentación completa** para facilitar transición
- **Código limpio y mantenible** para evolución futura
- **Capacitación básica** al personal del stakeholder

#### **Condiciones para Despliegue Exitoso:**

- **Cumplimiento de cronograma** académico
- **Calidad técnica** según estándares definidos
- **Documentación completa** de usuario y técnica
- **Pruebas exitosas** en ambiente académico
- **Aceptación formal** por parte del stakeholder

---

## 📋 **REQUISITOS FUNCIONALES**

### **RF-EVALPROY-001: Gestión de Ideas de Proyecto**

**Descripción:** El sistema debe permitir la gestión completa del ciclo de ideas de proyecto desde la propuesta inicial hasta la selección final.

**Funcionalidades:**

- Registro de ideas de proyecto por grupos
- Validación de mínimo 3 ideas por grupo en Trimestre II
- Evaluación y viabilización de ideas por instructores
- Selección de idea definitiva para desarrollo
- Historial de ideas propuestas y rechazadas

### **RF-EVALPROY-002: Gestión de Grupos de Trabajo**

**Descripción:** El sistema debe gestionar la formación y seguimiento de grupos de aprendices.

**Funcionalidades:**

- Formación de grupos (3-5 aprendices)
- Asignación de roles dentro del grupo
- Gestión de cambios en composición de grupos (solo instructores)
- Seguimiento de participación individual
- Evaluación de trabajo colaborativo

### **RF-EVALPROY-003: Configuración de Sesiones de Evaluación**

**Descripción:** El sistema debe permitir la programación y gestión de sesiones de seguimiento trimestral.

**Funcionalidades:**

- Programación de 1-2 sesiones por trimestre
- Asignación de 2 o más instructores como jurados
- Definición de agenda y criterios de evaluación
- Gestión de fechas y horarios
- Notificaciones automáticas a participantes

### **RF-EVALPROY-004: Lista de Chequeo Dinámica**

**Descripción:** El sistema debe proporcionar listas de chequeo configurables para cada trimestre y tipo de evaluación.

**Funcionalidades:**

- Configuración de criterios por trimestre
- Escalamiento de complejidad según avance formativo
- Personalización según tipo de proyecto
- Rúbricas específicas para cada etapa
- Peso diferenciado por criterio

### **RF-EVALPROY-005: Evaluación de Avances Trimestrales**

**Descripción:** El sistema debe permitir la evaluación sistemática de avances del proyecto en cada trimestre.

**Funcionalidades:**

- Registro de avances por trimestre
- Evaluación según conocimientos adquiridos
- Comparación con cronograma planificado
- Identificación de desviaciones
- Recomendaciones de mejora

### **RF-EVALPROY-006: Gestión de Stakeholders**

**Descripción:** El sistema debe gestionar la información y participación controlada de stakeholders externos en los proyectos, manteniendo la autoridad académica sobre decisiones del proyecto.

**Funcionalidades:**

- **Participación Limitada del Stakeholder:**
  - Registro de stakeholders externos con rol consultivo
  - Definición inicial de requisitos funcionales
  - Retroalimentación sobre funcionalidades desarrolladas
  - Validación de cumplimiento de expectativas
  - Participación en demostraciones programadas

- **Control de Expectativas:**
  - Documentación clara de limitaciones de alcance
  - Comunicación de restricciones temporales
  - Definición de responsabilidades post-formación
  - Gestión de solicitudes fuera de alcance

- **Comunicación Estructurada:**
  - Canal formal de comunicación stakeholder-instructores
  - Registro de todas las interacciones
  - Filtrado de solicitudes antes de llegar a aprendices
  - Comunicación de decisiones académicas al stakeholder

### **RF-EVALPROY-007: Documentación del Proyecto**

**Descripción:** El sistema debe gestionar toda la documentación generada durante el desarrollo del proyecto.

**Funcionalidades:**

- Gestión de documentos técnicos
- Versionado de entregables
- Plantillas por tipo de documento
- Revisión y aprobación de documentos
- Repositorio centralizado de archivos

### **RF-EVALPROY-008: Calificación y Retroalimentación**

**Descripción:** El sistema debe permitir la calificación integral del proyecto y proporcionar retroalimentación detallada.

**Funcionalidades:**

- Calificación por criterios específicos
- Promedio ponderado de evaluaciones
- Comentarios detallados de jurados(habilitar notas de voz y transcripción)
- Sugerencias de mejora
- Historial de calificaciones

### **RF-EVALPROY-009: Reportes y Analytics**

**Descripción:** El sistema debe generar reportes completos del progreso y resultados de los proyectos formativos.

**Funcionalidades:**

- Reportes de avance por grupo
- Estadísticas de desempeño por trimestre
- Comparativos entre grupos
- Indicadores de éxito del proyecto
- Exportación de resultados

### **RF-EVALPROY-010: Gestión de Entregas**

**Descripción:** El sistema debe gestionar las entregas parciales y finales de los proyectos.

**Funcionalidades:**

- Programación de fechas de entrega
- Carga de archivos y documentos
- Validación de cumplimiento de requisitos
- Historial de entregas
- Notificaciones de vencimientos

### **RF-EVALPROY-011: Gestión de Cambios y Gobernanza del Proyecto**

**Descripción:** El sistema debe gestionar estrictamente los cambios de alcance, cronograma y composición de grupos, manteniendo la autoridad académica por encima de solicitudes de stakeholders.

**Funcionalidades:**

- **Control de Autoridad Académica:**
  - Solo instructores pueden aprobar cambios de alcance
  - Restricción de modificaciones por parte de stakeholders
  - Workflow de aprobación exclusivo para equipo pedagógico
  - Log de decisiones académicas vs. solicitudes de stakeholders

- **Gestión de Solicitudes de Cambio:**
  - Registro formal de solicitudes de stakeholders
  - Evaluación pedagógica de viabilidad
  - Análisis de impacto en cronograma académico
  - Justificación documentada de aprobación/rechazo
  - Comunicación formal de decisiones

- **Limitación de Expectativas:**
  - Definición clara de límites temporales
  - Documentación de restricciones de alcance
  - Validación de alineación con competencias del programa
  - Control de complejidad apropiada por trimestre

- **Gestión de Propiedad Intelectual:**
  - Registro de autoría institucional (SENA)
  - Documentación de derechos de uso del stakeholder
  - Definición de responsabilidades post-formación
  - Gestión de transferencia de conocimiento

### **RF-EVALPROY-012: Preparación para Despliegue Post-Formación**

**Descripción:** El sistema debe facilitar la preparación del proyecto para su eventual despliegue en el cliente, manteniendo la calidad técnica y documentación necesaria.

**Funcionalidades:**

- **Gestión de Entregables Finales:**
  - Código fuente documentado y organizado
  - Manual de usuario completo
  - Documentación técnica para mantenimiento
  - Guías de instalación y configuración

- **Validación de Calidad para Despliegue:**
  - Checklist de preparación para producción
  - Validación de estándares de código
  - Pruebas de funcionalidad completas
  - Documentación de dependencias y requisitos

- **Capacitación y Transferencia:**
  - Registro de sesiones de capacitación realizadas
  - Documentación de conocimiento transferido
  - Validación de comprensión por parte del stakeholder
  - Plan de soporte básico durante transición

---

## 🔧 **REQUISITOS NO FUNCIONALES**

### **RNF-EVALPROY-001: Disponibilidad**

- Disponibilidad 99.5% durante periodos académicos
- Tolerancia a fallos durante sesiones de evaluación
- Backup automático de datos de proyectos

### **RNF-EVALPROY-002: Seguridad**

- Protección de propiedad intelectual de proyectos
- Control de acceso basado en roles
- Trazabilidad de cambios en evaluaciones

### **RNF-EVALPROY-003: Usabilidad**

- Interfaz intuitiva para instructores y aprendices
- Tiempo de respuesta < 3 segundos
- Compatibilidad con dispositivos móviles

### **RNF-EVALPROY-004: Escalabilidad**

- Soporte para 500+ proyectos simultáneos
- Capacidad de crecimiento por semestres
- Optimización para múltiples centros

---

## 🔄 **INTEGRACIÓN CON OTROS SERVICIOS**

### **UserService**

- Autenticación de aprendices e instructores
- Gestión de perfiles y roles
- Información de fichas y programas

### **ScheduleService**

- Programación de sesiones de evaluación
- Coordinación con horarios académicos
- Gestión de disponibilidad de instructores

### **KbService**

- Plantillas de documentos
- Guías de buenas prácticas
- Base de conocimiento de proyectos

### **EvalinService**

- Evaluación de instructores en proceso
- Feedback sobre metodología de evaluación
- Correlación con desempeño docente

---

## 📈 **INDICADORES DE ÉXITO**

### **Indicadores Académicos**

- % de proyectos que completan exitosamente el ciclo
- Nota promedio de proyectos por trimestre
- % de proyectos con stakeholders externos
- Nivel de satisfacción de stakeholders (considerando limitaciones)

### **Indicadores Operativos**

- Tiempo promedio de evaluación por sesión
- % de sesiones realizadas según cronograma
- Número de iteraciones promedio por proyecto
- % de documentos entregados a tiempo

### **Indicadores de Calidad**

- % de proyectos que implementan buenas prácticas
- Nivel de aplicación de conocimientos por trimestre
- % de retroalimentación implementada
- Índice de mejora continua

### **Indicadores de Gobernanza**

- % de solicitudes de cambio de stakeholder aprobadas vs rechazadas
- Tiempo promedio de respuesta a solicitudes de stakeholder
- % de proyectos que mantienen alcance original
- % de proyectos exitosamente desplegables

---

## 🎯 **ALCANCE INICIAL**

### **Fase 1 (Trimestre Actual)**

- Gestión básica de ideas y grupos
- Lista de chequeo configurable
- Evaluación de avances básica
- Control de gobernanza fundamental

### **Fase 2 (Siguiente Trimestre)**

- Integración completa con stakeholders
- Gestión documental avanzada
- Analytics y dashboards
- Notificaciones automáticas

### **Fase 3 (Futuro)**

- Integración con repositorios Git
- Evaluación automática de código
- Machine Learning para recomendaciones
- Portal dedicado para stakeholders externos

---

**Este módulo representa el corazón del proceso formativo de los programas ADSO y PSW, donde los aprendices demuestran la aplicación práctica de todos sus conocimientos en proyectos reales con impacto en stakeholders externos, manteniendo siempre la autoridad académica sobre el proceso de formación.**

---

## 🔧 **REQUISITOS FUNCIONALES AMPLIADOS**

### **RF-13: Gestión de Criterios de Evaluación (CRUD)**

**Descripción:** El sistema debe permitir la gestión completa del ciclo de vida de criterios de evaluación a través de un proceso controlado por equipo pedagógico.

**Especificaciones:**

#### **13.1 Equipo Pedagógico Designado**

- El sistema debe configurar un **comité de revisión** de 3 miembros permanentes
- Roles predefinidos: Coordinador Académico, Instructor Senior, Especialista en Evaluación
- Autoridad completa para aprobar/rechazar modificaciones a criterios

#### **13.2 Operaciones CRUD Controladas**

**Agregación de Criterios:**

- Requiere justificación pedagógica detallada obligatoria
- Aprobación unánime del equipo pedagógico (3/3)
- Documentación de impacto en programas ADSO/PSW
- Prueba obligatoria en grupos piloto antes de implementación general

**Modificación de Criterios:**

- Requiere mayoría del equipo pedagógico (mínimo 2/3)
- Versionado automático con fechas de vigencia
- Comunicación anticipada (mínimo 1 trimestre)
- Documentación obligatoria de razón pedagógica

**Inactivación de Criterios:**

- Soft delete (marcado como inactivo, no eliminación)
- Mayoría simple requerida (2/3)
- No afecta evaluaciones futuras pero mantiene historial
- Fecha de inactivación y periodo de transición claros

#### **13.3 Trazabilidad y Auditoría**

- Historial completo de cambios con timestamps
- Identificación del miembro que propone/aprueba cambios
- Impacto automático en evaluaciones existentes
- Notificaciones automáticas a instructores afectados

---

### **RF-14: Integración de Notas de Voz y Transcripción**

**Descripción:** El sistema debe capturar, procesar y analizar observaciones de jurados mediante notas de voz con transcripción automática.

**Especificaciones:**

#### **14.1 Captura de Notas de Voz**

- Grabación directa durante sesiones de evaluación
- Asociación automática con criterio específico evaluado
- Identificación segura de evaluador y proyecto
- Controles de privacidad y consentimiento obligatorios

#### **14.2 Transcripción Automática**

- Integración con servicios de speech-to-text (Google Cloud Speech, Azure Speech, AWS Transcribe)
- Edición manual permitida para corrección de errores
- Soporte para múltiples idiomas (español priority)
- Detección automática de puntuación y estructura

#### **14.3 Procesamiento Inteligente**

- Generación automática de resúmenes por categoría de criterios
- Análisis de sentimientos para identificar áreas problemáticas
- Estadísticas de frecuencia de observaciones por criterio
- Identificación de patrones comunes en retroalimentación

#### **14.4 Exportación y Reportes**

- Transcripciones en formatos estándar (PDF, Word, texto plano)
- Reportes consolidados por proyecto/grupo
- Sugerencias automáticas basadas en observaciones históricas
- Dashboard de análisis de retroalimentación por instructor

---

### **RF-15: Control de Versiones para Bases de Datos (Database VCS)**

**Descripción:** El sistema debe implementar control de versiones completo para esquemas de base de datos con migraciones obligatorias.

**Especificaciones:**

#### **15.1 Sistema de Migraciones Obligatorio**

- Integración con herramientas específicas por stack (Alembic/FastAPI, Knex/Express, Flyway/Spring)
- Todas las modificaciones de esquema via archivos de migración versionados
- Scripts de rollback obligatorios para reversión segura
- Numeración secuencial automática de migraciones

#### **15.2 Documentación de Cambios**

- Descripción obligatoria clara del cambio y justificación
- Historial completo de versiones en repositorio Git
- Pruebas obligatorias en desarrollo antes de producción
- Documentación de impacto en datos existentes

#### **15.3 Políticas de Migración**

- Respaldos automáticos obligatorios antes de migraciones destructivas
- Proceso de revisión por pares para migraciones críticas
- Ejecución automática en CI/CD cuando es apropiado
- Sincronización obligatoria entre migraciones y código de aplicación

#### **15.4 Monitoreo y Alertas**

- Validación automática de integridad post-migración
- Alertas en caso de fallos de migración
- Métricas de tiempo de ejecución de migraciones
- Rollback automático en caso de fallos críticos

---

## 📊 **INDICADORES DE ÉXITO AMPLIADOS**

### **Gestión de Criterios**

- 100% de cambios de criterios aprobados por proceso formal
- < 5% de reversiones de criterios en primer año
- > 95% de satisfacción del equipo pedagógico con proceso CRUD
- < 24 horas tiempo promedio de revisión de solicitudes

### **Notas de Voz y Transcripción**

- > 90% precisión en transcripciones automáticas
- < 30 segundos tiempo de procesamiento por minuto de audio
- > 80% adopción de notas de voz por parte de instructores
- > 95% disponibilidad del servicio de transcripción

### **Database VCS**

- 100% de cambios de esquema via migraciones
- 0 pérdidas de datos por migraciones fallidas
- < 2 minutos tiempo promedio de ejecución de migraciones
- > 99.9% éxito en rollbacks cuando se requieren

---

**Versión Ampliada - Fecha: 17 de junio de 2025**  
**Incluye:** Gestión CRUD de Criterios, Notas de Voz con IA, Database VCS\*\*  
**Total de Requisitos Funcionales:** 15 (RF-01 a RF-15)\*\*
