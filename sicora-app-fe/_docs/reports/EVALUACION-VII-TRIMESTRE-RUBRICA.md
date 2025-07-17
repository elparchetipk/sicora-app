# 📊 **RÚBRICA DE EVALUACIÓN DETALLADA - VII TRIMESTRE ADSO**

**Evaluación:** Sistema de Preferencias de Usuario y Comentarios de Evaluación  
**Modalidad:** Práctica individual  
**Duración:** 1 semana  
**Puntuación Total:** 100 puntos + 15 bonus

---

## 🎯 **CRITERIOS GENERALES DE EVALUACIÓN**

### **Escala de Calificación**

- **Excelente (4.6-5.0):** 90-100% de los criterios cumplidos
- **Bueno (4.0-4.5):** 80-89% de los criterios cumplidos
- **Aceptable (3.5-3.9):** 70-79% de los criterios cumplidos
- **Insuficiente (1.0-3.4):** Menos del 70% de los criterios cumplidos

---

## 📋 **PARTE 1: ANÁLISIS Y COMPRENSIÓN (20 PUNTOS)**

### **1.1 Análisis de Arquitectura (10 puntos)**

| Criterio                    | Excelente (9-10 pts)                                                     | Bueno (8-8.9 pts)                               | Aceptable (7-7.9 pts)                                 | Insuficiente (0-6.9 pts)              |
| --------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------- | ----------------------------------------------------- | ------------------------------------- |
| **Identificación de Capas** | Identifica correctamente las 4 capas y sus responsabilidades específicas | Identifica las capas con pequeñas imprecisiones | Identifica las capas principales pero con confusiones | No identifica correctamente las capas |
| **Flujo de Datos**          | Explica claramente el flujo entre capas con ejemplos específicos         | Explica el flujo con pequeños errores           | Explica el flujo básico pero sin detalles             | No comprende el flujo de datos        |
| **Patrones de Diseño**      | Identifica y explica 3+ patrones (Repository, DI, Factory, etc.)         | Identifica 2-3 patrones correctamente           | Identifica 1-2 patrones básicos                       | No identifica patrones de diseño      |
| **Ventajas/Desventajas**    | Análisis profundo con ejemplos reales                                    | Análisis correcto con algunos ejemplos          | Análisis básico sin ejemplos                          | Análisis superficial o incorrecto     |

### **1.2 Análisis de Casos de Uso (10 puntos)**

| Criterio                  | Excelente (9-10 pts)                                     | Bueno (8-8.9 pts)                   | Aceptable (7-7.9 pts)    | Insuficiente (0-6.9 pts)  |
| ------------------------- | -------------------------------------------------------- | ----------------------------------- | ------------------------ | ------------------------- |
| **Selección de Casos**    | Selecciona casos representativos y diversos              | Selecciona casos apropiados         | Selecciona casos básicos | Selección inadecuada      |
| **Análisis de Propósito** | Comprende perfectamente el propósito y contexto          | Comprende el propósito principal    | Comprende parcialmente   | No comprende el propósito |
| **Entradas/Salidas**      | Documenta completamente entradas, salidas y validaciones | Documenta bien con pequeños errores | Documentación básica     | Documentación incompleta  |
| **Flujo de Ejecución**    | Describe paso a paso con manejo de errores               | Describe el flujo principal         | Describe flujo básico    | No describe el flujo      |

---

## 🛠️ **PARTE 2: IMPLEMENTACIÓN PRÁCTICA (50 PUNTOS)**

### **2.1 Sistema de Preferencias de Usuario (25 puntos)**

#### **Domain Layer (6 puntos)**

| Criterio                    | Excelente (5.4-6 pts)                                                 | Bueno (4.8-5.3 pts)                   | Aceptable (4.2-4.7 pts)  | Insuficiente (0-4.1 pts)          |
| --------------------------- | --------------------------------------------------------------------- | ------------------------------------- | ------------------------ | --------------------------------- |
| **Entidad UserPreferences** | Entidad completa con validaciones, métodos de negocio y encapsulación | Entidad correcta con pequeños errores | Entidad básica funcional | Entidad incompleta o no funcional |
| **Validaciones de Dominio** | Validaciones robustas en la entidad                                   | Validaciones básicas                  | Pocas validaciones       | Sin validaciones                  |
| **Métodos de Negocio**      | Métodos como update_language, reset_to_defaults implementados         | Algunos métodos implementados         | Métodos básicos          | Sin métodos de negocio            |

#### **Application Layer (6 puntos)**

| Criterio                    | Excelente (5.4-6 pts)                    | Bueno (4.8-5.3 pts)         | Aceptable (4.2-4.7 pts) | Insuficiente (0-4.1 pts) |
| --------------------------- | ---------------------------------------- | --------------------------- | ----------------------- | ------------------------ |
| **Use Cases Implementados** | Los 3 use cases completos y funcionales  | 2-3 use cases implementados | 1-2 use cases básicos   | Use cases incompletos    |
| **Manejo de Errores**       | Excepciones específicas y manejo robusto | Manejo básico de errores    | Poco manejo de errores  | Sin manejo de errores    |
| **Lógica de Negocio**       | Lógica correcta y completa               | Lógica básica correcta      | Lógica simple           | Lógica incorrecta        |

#### **Infrastructure Layer (6 puntos)**

| Criterio                      | Excelente (5.4-6 pts)                           | Bueno (4.8-5.3 pts)                  | Aceptable (4.2-4.7 pts) | Insuficiente (0-4.1 pts)  |
| ----------------------------- | ----------------------------------------------- | ------------------------------------ | ----------------------- | ------------------------- |
| **Repository Implementation** | Implementación completa con queries optimizadas | Implementación correcta              | Implementación básica   | Implementación incompleta |
| **Modelo SQLAlchemy**         | Modelo completo con constraints y relaciones    | Modelo correcto con pequeños errores | Modelo básico           | Modelo incorrecto         |
| **Migraciones**               | Migraciones correctas y versionadas             | Migraciones básicas                  | Migraciones simples     | Sin migraciones           |

#### **Presentation Layer (7 puntos)**

| Criterio                    | Excelente (6.3-7 pts)                                  | Bueno (5.6-6.2 pts)          | Aceptable (4.9-5.5 pts) | Insuficiente (0-4.8 pts) |
| --------------------------- | ------------------------------------------------------ | ---------------------------- | ----------------------- | ------------------------ |
| **Endpoints Implementados** | Los 3 endpoints completos y funcionales                | 2-3 endpoints implementados  | 1-2 endpoints básicos   | Endpoints incompletos    |
| **Validación de Entrada**   | Schemas Pydantic completos con validaciones            | Schemas básicos              | Validaciones simples    | Sin validaciones         |
| **Respuestas HTTP**         | Códigos de estado correctos y respuestas estructuradas | Respuestas básicas correctas | Respuestas simples      | Respuestas incorrectas   |
| **Documentación Swagger**   | Documentación completa con ejemplos                    | Documentación básica         | Documentación mínima    | Sin documentación        |

### **2.2 Sistema de Comentarios en Evaluaciones (25 puntos)**

#### **Domain Layer (6 puntos)**

| Criterio                      | Excelente (5.4-6 pts)                                  | Bueno (4.8-5.3 pts)                  | Aceptable (4.2-4.7 pts) | Insuficiente (0-4.1 pts) |
| ----------------------------- | ------------------------------------------------------ | ------------------------------------ | ----------------------- | ------------------------ |
| **Entidad EvaluationComment** | Entidad completa con validaciones y métodos de negocio | Entidad correcta con errores menores | Entidad básica          | Entidad incompleta       |
| **Reglas de Negocio**         | Implementa reglas como permisos, privacidad, edición   | Implementa algunas reglas            | Reglas básicas          | Sin reglas de negocio    |
| **Validaciones**              | Validaciones robustas (longitud, contenido, etc.)      | Validaciones básicas                 | Pocas validaciones      | Sin validaciones         |

#### **Application Layer (6 puntos)**

| Criterio                     | Excelente (5.4-6 pts)                         | Bueno (4.8-5.3 pts)   | Aceptable (4.2-4.7 pts) | Insuficiente (0-4.1 pts) |
| ---------------------------- | --------------------------------------------- | --------------------- | ----------------------- | ------------------------ |
| **Use Cases CRUD**           | CRUD completo con validaciones de negocio     | CRUD básico funcional | CRUD parcial            | CRUD incompleto          |
| **Integración con Permisos** | Verifica permisos correctamente               | Verificación básica   | Poca verificación       | Sin verificación         |
| **Validación de Estado**     | Valida estado de evaluación antes de comentar | Validación básica     | Poca validación         | Sin validación           |

#### **Infrastructure y Presentation (13 puntos)**

| Criterio                 | Excelente (11.7-13 pts)                 | Bueno (10.4-11.6 pts)   | Aceptable (9.1-10.3 pts) | Insuficiente (0-9 pts)    |
| ------------------------ | --------------------------------------- | ----------------------- | ------------------------ | ------------------------- |
| **Repository y Modelo**  | Implementación completa y optimizada    | Implementación correcta | Implementación básica    | Implementación incompleta |
| **Endpoints REST**       | 4 endpoints completos y funcionales     | 3-4 endpoints           | 2-3 endpoints            | 1-2 endpoints             |
| **Seguridad y Permisos** | Middleware de autorización implementado | Autorización básica     | Poca seguridad           | Sin seguridad             |

---

## 🔗 **PARTE 3: INTEGRACIÓN ENTRE SERVICIOS (20 PUNTOS)**

### **Comunicación HTTP (20 puntos)**

| Criterio                 | Excelente (18-20 pts)                             | Bueno (16-17.9 pts)                   | Aceptable (14-15.9 pts) | Insuficiente (0-13.9 pts) |
| ------------------------ | ------------------------------------------------- | ------------------------------------- | ----------------------- | ------------------------- |
| **Cliente HTTP**         | Cliente robusto con manejo de errores y timeouts  | Cliente funcional con errores básicos | Cliente simple          | Cliente no funcional      |
| **Endpoint Receptor**    | Endpoint completo con validación y almacenamiento | Endpoint básico funcional             | Endpoint simple         | Endpoint no funcional     |
| **Entidad UserActivity** | Entidad completa con métodos de negocio           | Entidad correcta                      | Entidad básica          | Entidad incompleta        |
| **Integración Async**    | Comunicación no bloqueante con manejo de fallos   | Comunicación básica                   | Comunicación simple     | Comunicación bloqueante   |
| **Manejo de Errores**    | Manejo robusto sin afectar flujo principal        | Manejo básico                         | Poco manejo             | Sin manejo de errores     |

---

## 🧪 **PARTE 4: TESTING Y CALIDAD (10 PUNTOS)**

### **Testing (10 puntos)**

| Criterio                 | Excelente (9-10 pts)                             | Bueno (8-8.9 pts)                   | Aceptable (7-7.9 pts)           | Insuficiente (0-6.9 pts) |
| ------------------------ | ------------------------------------------------ | ----------------------------------- | ------------------------------- | ------------------------ |
| **Tests Unitarios**      | Tests completos para use cases con >90% coverage | Tests básicos con >80% coverage     | Tests simples con >70% coverage | Tests insuficientes      |
| **Tests de Integración** | Tests completos para endpoints con casos edge    | Tests básicos para endpoints        | Tests simples                   | Tests incompletos        |
| **Tests de Errores**     | Tests para manejo de excepciones y casos límite  | Tests básicos de errores            | Pocos tests de error            | Sin tests de error       |
| **Calidad del Código**   | Código limpio, documentado, siguiendo PEP 8      | Código organizado con documentación | Código básico                   | Código desorganizado     |

---

## 🎖️ **EJERCICIOS BONUS (15 PUNTOS)**

### **Optimización de Consultas (5 puntos)**

- **5 pts:** Identifica 2+ consultas y las optimiza con mediciones
- **3-4 pts:** Identifica y optimiza 1 consulta correctamente
- **1-2 pts:** Identifica consultas pero optimización básica
- **0 pts:** No realiza el ejercicio

### **Documentación API Avanzada (5 puntos)**

- **5 pts:** Swagger completo con ejemplos, errores y categorización
- **3-4 pts:** Documentación mejorada con algunos ejemplos
- **1-2 pts:** Documentación básica mejorada
- **0 pts:** No mejora la documentación

### **Análisis de Seguridad (5 puntos)**

- **5 pts:** Análisis completo con recomendaciones implementadas
- **3-4 pts:** Análisis correcto con algunas recomendaciones
- **1-2 pts:** Análisis básico
- **0 pts:** No realiza análisis

---

## 📝 **CRITERIOS TRANSVERSALES**

### **Criterios Aplicables a Todas las Partes**

| Aspecto                     | Descripción                                            | Impacto en Calificación           |
| --------------------------- | ------------------------------------------------------ | --------------------------------- |
| **Seguimiento de Patrones** | Respeta los patrones arquitectónicos establecidos      | -10% si no sigue patrones         |
| **Nomenclatura**            | Usa convenciones PEP 8 y nomenclatura consistente      | -5% por inconsistencias           |
| **Git y Commits**           | Commits descriptivos y estructura de proyecto ordenada | +2% por buenas prácticas          |
| **Documentación**           | README completo con instrucciones claras               | -5% si documentación insuficiente |
| **Entrega Puntual**         | Entrega dentro del plazo establecido                   | -10% por cada día de retraso      |

---

## 🎓 **EVALUACIÓN DE LA REFLEXIÓN FINAL**

### **Reflexión Personal (Incluida en las partes principales)**

| Criterio              | Excelente                                     | Bueno                           | Aceptable             | Insuficiente               |
| --------------------- | --------------------------------------------- | ------------------------------- | --------------------- | -------------------------- |
| **Profundidad**       | Reflexión profunda con conexiones claras      | Reflexión correcta con ejemplos | Reflexión básica      | Reflexión superficial      |
| **Autocrítica**       | Identifica fortalezas y áreas de mejora       | Identifica algunos aspectos     | Identificación básica | Sin autocrítica            |
| **Aprendizaje**       | Articula claramente el aprendizaje obtenido   | Describe el aprendizaje         | Menciona aprendizajes | No identifica aprendizajes |
| **Aplicación Futura** | Conecta con aplicaciones profesionales reales | Algunas conexiones              | Conexiones básicas    | Sin conexiones             |

---

## 📊 **TABLA DE CALIFICACIÓN FINAL**

### **Conversión de Puntos a Nota**

| Puntos Obtenidos | Nota (Escala 1.0-5.0) | Calificación      |
| ---------------- | --------------------- | ----------------- |
| 95-115           | 4.8-5.0               | Excelente         |
| 90-94            | 4.6-4.7               | Muy Bueno         |
| 85-89            | 4.3-4.5               | Bueno             |
| 80-84            | 4.0-4.2               | Aceptable Alto    |
| 75-79            | 3.7-3.9               | Aceptable         |
| 70-74            | 3.5-3.6               | Aceptable Bajo    |
| 60-69            | 3.0-3.4               | Insuficiente Alto |
| 50-59            | 2.0-2.9               | Insuficiente      |
| <50              | 1.0-1.9               | Deficiente        |

---

## 💡 **RECOMENDACIONES PARA LA EVALUACIÓN**

### **Para el Instructor**

1. **Revisión por Partes:** Evaluar cada parte independientemente antes de la nota final
2. **Ejecución de Código:** Verificar que el código se ejecute sin errores
3. **Testing:** Ejecutar tests proporcionados por el estudiante
4. **Feedback Constructivo:** Proporcionar comentarios específicos para cada criterio
5. **Revisión de Arquitectura:** Verificar que se respete la Clean Architecture

### **Comandos de Verificación**

```bash
# Verificar que el código se ejecute
cd userservice && python -m pytest tests/ -v

# Verificar coverage
pytest --cov=app --cov-report=html

# Verificar linting
flake8 . --max-line-length=88

# Verificar documentación
cd userservice && uvicorn main:app --reload
# Visitar http://localhost:8000/docs
```

### **Aspectos Críticos a Revisar**

- [ ] **Funcionalidad:** El código cumple los requerimientos
- [ ] **Arquitectura:** Respeta Clean Architecture
- [ ] **Testing:** Tests ejecutan sin errores
- [ ] **Seguridad:** Validaciones y permisos implementados
- [ ] **Comunicación:** Integración entre servicios funciona
- [ ] **Documentación:** README e instrucciones claras

---

**Esta rúbrica garantiza una evaluación justa, objetiva y formativa que prepare a los estudiantes para desafíos profesionales reales en desarrollo de software.**
