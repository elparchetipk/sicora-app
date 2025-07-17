# 🎓 **EVALUACIÓN VII TRIMESTRE - ÍNDICE EJECUTIVO**

**¡Bienvenido a tu evaluación práctica de Backend con FastAPI!**

---

## 🚀 **¿POR DÓNDE EMPEZAR?**

### **📖 PASO 1: Lee las Instrucciones Detalladas**

👉 **[EVALUACION-VII-TRIMESTRE-INSTRUCCIONES-DETALLADAS.md](EVALUACION-VII-TRIMESTRE-INSTRUCCIONES-DETALLADAS.md)**

**QUÉ ENCONTRARÁS:**

- Plan día a día (7 días)
- QUÉ hacer exactamente cada día
- Comandos específicos para ejecutar
- Checkpoints de verificación
- Estructura de carpetas final

### **💻 PASO 2: Usa las Plantillas de Código**

👉 **[EVALUACION-VII-TRIMESTRE-PLANTILLAS-CODIGO.md](EVALUACION-VII-TRIMESTRE-PLANTILLAS-CODIGO.md)**

**QUÉ ENCONTRARÁS:**

- Código listo para copiar y completar
- TODOs específicos marcados con ✅
- Ejemplos de tests
- Plantillas para cada capa de la arquitectura

### **📊 PASO 3: Verifica con la Rúbrica**

👉 **[EVALUACION-VII-TRIMESTRE-RUBRICA.md](EVALUACION-VII-TRIMESTRE-RUBRICA.md)**

**QUÉ ENCONTRARÁS:**

- Cómo serás evaluado exactamente
- Puntuación por cada parte
- Criterios específicos de calificación
- Lista de verificación antes de entregar

---

## 🎯 **RESUMEN: QUÉ VAS A HACER**

### **📱 Funcionalidad 1: Sistema de Preferencias de Usuario**

**En UserService** - Donde cada usuario puede configurar:

- Idioma (español/inglés)
- Tema visual (claro/oscuro/automático)
- Notificaciones (email/push activadas/desactivadas)
- Zona horaria

**Endpoints a crear:**

```
GET    /api/v1/users/preferences        # Ver mis preferencias
PUT    /api/v1/users/preferences        # Actualizar preferencias
POST   /api/v1/users/preferences/reset  # Volver a defaults
```

### **💬 Funcionalidad 2: Sistema de Comentarios en Evaluaciones**

**En EvalinService** - Donde los usuarios pueden:

- Agregar comentarios a evaluaciones
- Ver comentarios de evaluaciones
- Editar sus propios comentarios
- Marcar comentarios como privados (solo admin)

**Endpoints a crear:**

```
POST   /api/v1/evaluations/{id}/comments      # Agregar comentario
GET    /api/v1/evaluations/{id}/comments      # Ver comentarios
PUT    /api/v1/evaluations/comments/{id}      # Editar comentario
DELETE /api/v1/evaluations/comments/{id}      # Eliminar comentario
```

### **🔗 Funcionalidad 3: Comunicación entre Servicios**

Cuando se complete una evaluación → EvalinService notifica a UserService para registrar la actividad del usuario.

---

## ⏰ **CRONOGRAMA RÁPIDO**

| Día         | Qué Hacer                               | Tiempo Estimado |
| ----------- | --------------------------------------- | --------------- |
| **Día 1**   | Análisis de arquitectura y casos de uso | 4 horas         |
| **Día 2-3** | Implementar Sistema de Preferencias     | 8 horas         |
| **Día 4-5** | Implementar Sistema de Comentarios      | 8 horas         |
| **Día 6**   | Comunicación entre servicios            | 4 horas         |
| **Día 7**   | Testing y documentación                 | 4 horas         |

**Total: ~28 horas** distribuidas en 7 días = **4 horas por día**

---

## ✅ **CHECKLIST RÁPIDO ANTES DE EMPEZAR**

- [ ] Tengo Python 3.13 instalado
- [ ] Puedo clonar/acceder al repositorio
- [ ] Puedo ejecutar `uvicorn` sin errores
- [ ] Veo la documentación en http://localhost:8001/docs
- [ ] Tengo un editor de código configurado
- [ ] Tengo acceso a terminal/línea de comandos

---

## 📋 **ESTRUCTURA DE ENTREGA FINAL**

```
apellido_nombre_evaluacion/
├── README.md                          ← Cómo ejecutar tu código
├── docs/
│   ├── analisis_arquitectura.md       ← Tu análisis (Día 1)
│   ├── analisis_casos_uso.md          ← Tu análisis (Día 1)
│   └── reflexion_personal.md          ← Tu reflexión (Día 7)
├── userservice/                       ← Preferencias de usuario
│   ├── app/domain/entities/user_preferences.py
│   ├── app/application/use_cases/...
│   ├── app/infrastructure/...
│   ├── app/presentation/routers/preferences_router.py
│   └── tests/
├── evalinservice/                     ← Comentarios en evaluaciones
│   ├── app/domain/entities/evaluation_comment.py
│   ├── app/application/use_cases/...
│   ├── app/infrastructure/...
│   ├── app/presentation/routers/comment_router.py
│   └── tests/
└── requirements.txt                   ← Si agregaste dependencias
```

---

## 🆘 **¿TIENES PROBLEMAS?**

### **Errores Comunes:**

1. **"Module not found"** → Verifica imports y PYTHONPATH
2. **"Table doesn't exist"** → Crea migraciones de BD
3. **"401 Unauthorized"** → Verifica headers de autenticación
4. **"Tests fallan"** → Ejecuta un test a la vez

### **Dónde Buscar Ayuda:**

- **Ejemplo de entidad:** `userservice/app/domain/entities/user.py`
- **Ejemplo de caso de uso:** `userservice/app/application/use_cases/`
- **Ejemplo de endpoint:** `userservice/app/presentation/routers/`
- **Ejemplo de test:** `userservice/tests/`

### **Comandos Útiles:**

```bash
# Verificar que funciona
uvicorn main:app --reload --port 8001

# Ejecutar tests
pytest tests/ -v

# Ver documentación
# http://localhost:8001/docs
```

---

## 🏆 **CRITERIOS DE ÉXITO SIMPLES**

**Pregúntate cada día:**

1. ¿Mi código se ejecuta sin errores?
2. ¿Veo mis endpoints en Swagger?
3. ¿Puedo hacer requests y recibir respuestas?
4. ¿Entiendo lo que estoy haciendo?

**Si respondes SÍ → vas bien encaminado** ✅

---

## 📞 **CONTACTO Y SOPORTE**

**Si tienes dudas técnicas específicas:**

- Revisa primero las plantillas de código
- Consulta los ejemplos existentes en el proyecto
- Verifica que hayas seguido todos los pasos

**Recuerda:** Es mejor entregar algo funcional y sencillo que algo complejo que no funciona.

---

**🎯 ¡Ahora sí tienes todo claro! Comienza con las [Instrucciones Detalladas](EVALUACION-VII-TRIMESTRE-INSTRUCCIONES-DETALLADAS.md) y usa las [Plantillas de Código](EVALUACION-VII-TRIMESTRE-PLANTILLAS-CODIGO.md) para implementar.**

**¡Éxito en tu evaluación! 🚀**
