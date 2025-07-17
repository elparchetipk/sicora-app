#!/usr/bin/env python3
"""
Generador de Contenido Implementable para KBService
Crea contenido específico y estructurado listo para implementar como soporte primario
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any


class SupportContentGenerator:
    """Generador de contenido específico para soporte primario."""
    
    def __init__(self):
        # Plantillas de contenido por tipo
        self.content_templates = {
            'step_by_step_guide': {
                'structure': [
                    'Objetivo',
                    'Requisitos previos',
                    'Pasos detallados',
                    'Verificación',
                    'Solución de problemas'
                ]
            },
            'faq_item': {
                'structure': [
                    'Pregunta',
                    'Respuesta corta',
                    'Respuesta detallada',
                    'Enlaces relacionados'
                ]
            },
            'troubleshooting_guide': {
                'structure': [
                    'Síntomas',
                    'Causas posibles',
                    'Soluciones paso a paso',
                    'Prevención'
                ]
            }
        }
    
    def generate_essential_content(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generar contenido esencial para soporte primario."""
        
        content = {
            'critical_faqs': self._generate_critical_faqs(),
            'onboarding_guides': self._generate_onboarding_guides(),
            'troubleshooting_guides': self._generate_troubleshooting_guides(),
            'quick_reference_cards': self._generate_quick_reference_cards()
        }
        
        return content
    
    def _generate_critical_faqs(self) -> List[Dict[str, Any]]:
        """Generar FAQs críticas para cada módulo."""
        
        faqs = []
        
        # AttendanceService FAQs
        attendance_faqs = [
            {
                'question': '¿Cómo marco mi asistencia en SICORA?',
                'short_answer': 'Use la opción "Marcar Asistencia" en la pantalla principal.',
                'detailed_answer': '''
**Pasos para marcar asistencia:**
1. Ingrese al sistema SICORA con sus credenciales
2. En la pantalla principal, seleccione "Marcar Asistencia"
3. Verifique que la ubicación detectada sea correcta
4. Confirme el registro con el botón "Confirmar Asistencia"
5. Espere la confirmación visual del sistema

**Nota importante:** La asistencia debe marcarse durante el horario de clase establecido.
                ''',
                'category': 'attendanceservice',
                'target_audience': ['aprendices'],
                'priority': 'critical'
            },
            {
                'question': '¿Qué pasa si llego tarde a clase?',
                'short_answer': 'El sistema registra tardanzas automáticamente según la hora de llegada.',
                'detailed_answer': '''
**Manejo de tardanzas:**
- **Tardanza menor (1-15 min):** Se registra como tardanza simple
- **Tardanza mayor (16-30 min):** Se registra como tardanza grave
- **Llegada después de 30 min:** Se considera falta

**Cómo justificar una tardanza:**
1. Vaya a "Mi Historial de Asistencia"
2. Seleccione la fecha con tardanza
3. Clic en "Justificar"
4. Adjunte documentos de soporte si es necesario
5. Envíe la justificación

**Documentos válidos:** Incapacidades médicas, emergencias familiares, problemas de transporte público.
                ''',
                'category': 'attendanceservice',
                'target_audience': ['aprendices'],
                'priority': 'high'
            }
        ]
        
        # ScheduleService FAQs
        schedule_faqs = [
            {
                'question': '¿Dónde puedo consultar mi horario de clases?',
                'short_answer': 'En la sección "Mi Horario" del menú principal.',
                'detailed_answer': '''
**Para consultar su horario:**
1. Acceda al sistema SICORA
2. En el menú principal, seleccione "Mi Horario"
3. Use los filtros para ver horario por:
   - Día específico
   - Semana completa
   - Mes completo

**Información disponible:**
- Materia y instructor
- Hora de inicio y fin
- Ambiente asignado
- Tipo de clase (teórica/práctica)
- Estado (confirmada/pendiente)

**Nota:** Los cambios de horario se reflejan automáticamente en el sistema.
                ''',
                'category': 'scheduleservice',
                'target_audience': ['aprendices', 'instructores'],
                'priority': 'critical'
            },
            {
                'question': '¿Cómo reservo un ambiente de formación? (Instructores)',
                'short_answer': 'Use la opción "Gestión de Ambientes" en el menú de instructor.',
                'detailed_answer': '''
**Pasos para reservar un ambiente:**
1. Acceda a "Gestión de Ambientes"
2. Seleccione la fecha deseada en el calendario
3. Verifique disponibilidad por horario
4. Escoja el ambiente que necesite:
   - Aula teórica
   - Laboratorio de sistemas
   - Aula especializada
5. Confirme la reserva

**Restricciones:**
- Máximo 2 horas continuas por reserva
- No se puede reservar con menos de 24h de anticipación
- Cancelaciones deben hacerse con 2h de anticipación

**En caso de problemas:** Contacte a coordinación académica.
                ''',
                'category': 'scheduleservice',
                'target_audience': ['instructores'],
                'priority': 'high'
            }
        ]
        
        # UserService FAQs
        user_faqs = [
            {
                'question': '¿Cómo cambio mi contraseña en SICORA?',
                'short_answer': 'Vaya a "Mi Perfil" > "Cambiar Contraseña".',
                'detailed_answer': '''
**Pasos para cambiar contraseña:**
1. Acceda a su perfil de usuario
2. Seleccione "Configuración de Cuenta"
3. Clic en "Cambiar Contraseña"
4. Ingrese su contraseña actual
5. Escriba la nueva contraseña (2 veces)
6. Confirme el cambio

**Requisitos de contraseña:**
- Mínimo 8 caracteres
- Al menos 1 letra mayúscula
- Al menos 1 número
- Al menos 1 carácter especial (@, #, $, etc.)

**Importante:** Después del cambio, deberá iniciar sesión nuevamente en todos sus dispositivos.
                ''',
                'category': 'userservice',
                'target_audience': ['aprendices', 'instructores', 'administrativos'],
                'priority': 'critical'
            },
            {
                'question': 'Olvidé mi contraseña, ¿qué hago?',
                'short_answer': 'Use la opción "Recuperar Contraseña" en la pantalla de login.',
                'detailed_answer': '''
**Proceso de recuperación:**
1. En la pantalla de login, clic en "¿Olvidó su contraseña?"
2. Ingrese su número de documento
3. Verifique su correo electrónico registrado
4. Clic en el enlace de recuperación recibido
5. Cree una nueva contraseña

**Si no recibe el correo:**
- Verifique la carpeta de spam
- Espere hasta 10 minutos
- Intente nuevamente

**Si persiste el problema:**
- Contacte al administrador del sistema
- Presente su documento de identidad
- Solicite reseteo manual de contraseña
                ''',
                'category': 'userservice',
                'target_audience': ['aprendices', 'instructores', 'administrativos'],
                'priority': 'critical'
            }
        ]
        
        # Compilar todas las FAQs
        all_faqs = attendance_faqs + schedule_faqs + user_faqs
        
        # Agregar metadatos
        for i, faq in enumerate(all_faqs):
            faq.update({
                'id': str(uuid.uuid4())[:12],
                'type': 'faq',
                'status': 'published',
                'created_at': datetime.now().isoformat(),
                'tags': self._generate_tags_for_faq(faq),
                'search_keywords': self._extract_search_keywords(faq)
            })
        
        return all_faqs
    
    def _generate_onboarding_guides(self) -> List[Dict[str, Any]]:
        """Generar guías de onboarding para nuevos usuarios."""
        
        guides = [
            {
                'id': str(uuid.uuid4())[:12],
                'title': 'Guía de Primer Ingreso para Aprendices',
                'type': 'onboarding_guide',
                'target_audience': ['aprendices'],
                'content': '''
# Bienvenido a SICORA - Guía de Primer Ingreso

## 🎯 Objetivo
Esta guía lo ayudará a realizar su primer ingreso al sistema SICORA y conocer las funciones básicas.

## 📋 Requisitos Previos
- Tener sus credenciales de acceso (proporcionadas por coordinación académica)
- Dispositivo con conexión a internet
- Navegador web actualizado

## 🔑 Paso 1: Primer Ingreso
1. **Acceda al sistema:** Vaya a la URL proporcionada por su coordinación
2. **Ingrese credenciales:**
   - Usuario: Su número de documento
   - Contraseña: Contraseña temporal proporcionada
3. **Cambio obligatorio de contraseña:**
   - El sistema le solicitará crear una nueva contraseña
   - Siga los requisitos de seguridad mostrados
4. **Complete su perfil:**
   - Verifique sus datos personales
   - Agregue foto de perfil (opcional)
   - Confirme su información de contacto

## 📱 Paso 2: Conocer la Interfaz Principal
**Elementos principales:**
- **Menú superior:** Navegación principal
- **Dashboard:** Resumen de su actividad académica
- **Notificaciones:** Alertas importantes
- **Mi Perfil:** Configuración personal

## ✅ Paso 3: Funciones Esenciales
### Marcar Asistencia
- Ubicación: Botón principal en el dashboard
- Cuándo usar: Al inicio de cada clase
- Qué verificar: Ubicación y horario correctos

### Consultar Horario
- Ubicación: Menú "Mi Horario"
- Información disponible: Materias, horarios, ambientes
- Filtros: Por día, semana o mes

### Ver Calificaciones
- Ubicación: Menú "Mis Evaluaciones"
- Información: Notas por materia, promedio general
- Exportar: Opción de descarga en PDF

## ✓ Verificación
Después de completar estos pasos, usted debería poder:
- [ ] Ingresar al sistema sin problemas
- [ ] Marcar asistencia correctamente
- [ ] Consultar su horario de clases
- [ ] Ver sus calificaciones actuales
- [ ] Recibir notificaciones del sistema

## 🚨 Solución de Problemas Comunes
**No puedo ingresar:** Verifique credenciales y contacte a coordinación
**No aparece mi horario:** Espere 24h después de matrícula o contacte coordinación
**Error al marcar asistencia:** Verifique conexión a internet y ubicación GPS

## 📞 Soporte
- **Soporte técnico:** Opción "Ayuda" en el menú
- **Coordinación académica:** Horarios de atención presencial
- **Chat de ayuda:** Disponible de 7:00 AM a 6:00 PM
                ''',
                'priority': 'critical',
                'estimated_completion_time': '15 minutos',
                'created_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4())[:12],
                'title': 'Guía de Inicio para Instructores',
                'type': 'onboarding_guide',
                'target_audience': ['instructores'],
                'content': '''
# Guía de Inicio para Instructores - SICORA

## 🎯 Objetivo
Familiarizar a los instructores con las herramientas de gestión académica en SICORA.

## 🔑 Configuración Inicial
### Primer Acceso
1. Use sus credenciales institucionales
2. Complete la verificación de perfil
3. Configure sus preferencias de notificación
4. Revise los grupos de formación asignados

### Configuración del Espacio de Trabajo
- **Dashboard personalizable:** Organice widgets según su preferencia
- **Calendario integrado:** Sincronice con horarios institucionales
- **Notificaciones:** Configure alertas para eventos importantes

## 📚 Gestión de Clases
### Toma de Asistencia
1. Acceda al módulo "Gestión de Grupos"
2. Seleccione el grupo de formación
3. Escoja la fecha y horario de clase
4. Marque presente/ausente para cada aprendiz
5. Agregue observaciones si es necesario

### Programación de Actividades
- **Crear actividades:** Defina objetivos y recursos necesarios
- **Asignar ambientes:** Reserve espacios según tipo de actividad
- **Configurar evaluaciones:** Establezca criterios y fechas

## 📊 Evaluación y Seguimiento
### Sistema de Evaluaciones
- **Criterios predefinidos:** Use las rúbricas institucionales
- **Evaluación continua:** Registre progreso de forma regular
- **Reportes automáticos:** Genere informes de desempeño

### Comunicación con Aprendices
- **Mensajes del sistema:** Envíe comunicaciones oficiales
- **Feedback individual:** Proporcione retroalimentación personalizada
- **Notificaciones grupales:** Informe cambios de horario o actividades

## ⚙️ Herramientas Avanzadas
### Gestión de Ambientes
- Verificar disponibilidad en tiempo real
- Reservar espacios especializados
- Reportar problemas técnicos

### Reportes y Analytics
- Generar reportes de asistencia
- Análisis de desempeño grupal
- Exportar datos para análisis externo

## ✓ Lista de Verificación Semanal
- [ ] Revisar asistencia de todos los grupos
- [ ] Actualizar calificaciones pendientes
- [ ] Verificar reservas de ambientes para la próxima semana
- [ ] Responder mensajes de aprendices
- [ ] Completar observaciones en el sistema

## 📞 Soporte Pedagógico
- **Mesa de ayuda técnica:** Disponible 24/7
- **Coordinación académica:** Soporte pedagógico
- **Comunidad de instructores:** Foro interno de mejores prácticas
                ''',
                'priority': 'high',
                'estimated_completion_time': '30 minutos',
                'created_at': datetime.now().isoformat()
            }
        ]
        
        return guides
    
    def _generate_troubleshooting_guides(self) -> List[Dict[str, Any]]:
        """Generar guías de solución de problemas."""
        
        guides = [
            {
                'id': str(uuid.uuid4())[:12],
                'title': 'Problemas de Acceso al Sistema',
                'type': 'troubleshooting_guide',
                'category': 'authentication',
                'symptoms': [
                    'No puedo iniciar sesión',
                    'El sistema dice que mis credenciales son incorrectas',
                    'La página no carga después del login'
                ],
                'solutions': '''
## 🔍 Diagnóstico Paso a Paso

### Síntoma: No puedo iniciar sesión
**Causas posibles:**
- Credenciales incorrectas
- Cuenta bloqueada temporalmente
- Problemas de conectividad
- Caché del navegador

**Soluciones:**
1. **Verificar credenciales:**
   - Usuario: Número de documento sin puntos ni espacios
   - Contraseña: Distingue mayúsculas de minúsculas
   
2. **Limpiar caché del navegador:**
   - Chrome: Ctrl+Shift+Delete
   - Firefox: Ctrl+Shift+Delete
   - Safari: Cmd+Option+E
   
3. **Probar navegador privado/incógnito:**
   - Esto ayuda a identificar problemas de caché
   
4. **Verificar conexión a internet:**
   - Pruebe con otros sitios web
   - Verifique si está en la red institucional

### Síntoma: Cuenta bloqueada
**Causas:**
- Múltiples intentos fallidos de login
- Violación de políticas de seguridad

**Soluciones:**
1. Espere 15 minutos antes de intentar nuevamente
2. Use la opción "Recuperar contraseña"
3. Contacte al administrador del sistema

### Síntoma: Sistema lento o no responde
**Soluciones inmediatas:**
1. Refrescar la página (F5)
2. Cerrar otras pestañas del navegador
3. Reiniciar el navegador
4. Verificar hora del sistema (debe estar sincronizada)

## 🚨 Cuándo Contactar Soporte
- Después de intentar todas las soluciones básicas
- Si el problema persiste por más de 30 minutos
- Si afecta a múltiples usuarios
- Si involucra información académica crítica
                ''',
                'priority': 'critical',
                'target_audience': ['aprendices', 'instructores', 'administrativos'],
                'created_at': datetime.now().isoformat()
            }
        ]
        
        return guides
    
    def _generate_quick_reference_cards(self) -> List[Dict[str, Any]]:
        """Generar tarjetas de referencia rápida."""
        
        cards = [
            {
                'id': str(uuid.uuid4())[:12],
                'title': 'Referencia Rápida - Asistencia',
                'type': 'quick_reference',
                'category': 'attendanceservice',
                'content': '''
# ⚡ Referencia Rápida - Asistencia

## 🕐 Horarios de Marcación
- **Llegada puntual:** Dentro de los primeros 15 min
- **Tardanza simple:** 16-30 min después del inicio
- **Tardanza grave:** 31-45 min después del inicio
- **Falta:** Más de 45 min o no marcar asistencia

## 📍 Cómo Marcar
1. Dashboard → "Marcar Asistencia"
2. Verificar ubicación GPS
3. Confirmar horario mostrado
4. Clic en "Confirmar"

## 📊 Consultar Historial
- **Ruta:** Menú → "Mi Asistencia"
- **Filtros:** Por fecha, materia, tipo
- **Exportar:** Opción PDF disponible

## ⚠️ Justificar Faltas
- **Plazo:** Máximo 3 días hábiles
- **Documentos:** Incapacidad médica, calamidad familiar
- **Proceso:** Historial → Seleccionar fecha → "Justificar"

## 📞 Contactos
- **Coordinación:** Ext. 101
- **Soporte técnico:** Opción "Ayuda" en el sistema
                ''',
                'target_audience': ['aprendices'],
                'priority': 'high',
                'created_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4())[:12],
                'title': 'Referencia Rápida - Horarios',
                'type': 'quick_reference',
                'category': 'scheduleservice',
                'content': '''
# ⚡ Referencia Rápida - Horarios

## 📅 Consultar Mi Horario
- **Ruta:** Menú → "Mi Horario"
- **Vistas:** Día / Semana / Mes
- **Información:** Materia, instructor, ambiente, hora

## 🏢 Código de Ambientes
- **A101-A120:** Aulas teóricas
- **L201-L210:** Laboratorios de sistemas
- **T301-T305:** Talleres especializados
- **S401-S403:** Salas de reuniones

## 🔄 Cambios de Horario
- **Notificación:** Automática por el sistema
- **Confirmación:** Requerida en 24h
- **Consultas:** Coordinación académica

## 📍 Ubicación de Ambientes
- **Edificio A:** Aulas teóricas (Piso 1-2)
- **Edificio L:** Laboratorios (Piso 2-3)
- **Edificio T:** Talleres (Piso 1)
- **Edificio S:** Salas especiales (Piso 4)

## 🔔 Recordatorios
- **15 min antes:** Notificación automática
- **Cambios:** Alerta inmediata
- **Cancelaciones:** Aviso con 2h de anticipación
                ''',
                'target_audience': ['aprendices', 'instructores'],
                'priority': 'high',
                'created_at': datetime.now().isoformat()
            }
        ]
        
        return cards
    
    def _generate_tags_for_faq(self, faq: Dict[str, Any]) -> List[str]:
        """Generar tags para una FAQ."""
        
        tags = set()
        
        # Tags de categoría
        if faq.get('category'):
            tags.add(faq['category'])
        
        # Tags de audiencia
        for audience in faq.get('target_audience', []):
            tags.add(audience)
        
        # Tags de contenido
        content = (faq.get('question', '') + ' ' + faq.get('short_answer', '')).lower()
        
        keyword_tags = {
            'login': ['acceso', 'ingreso', 'sesión'],
            'password': ['contraseña', 'clave'],
            'attendance': ['asistencia', 'tardanza', 'falta'],
            'schedule': ['horario', 'clase', 'ambiente'],
            'grades': ['calificación', 'nota', 'evaluación'],
            'profile': ['perfil', 'datos', 'información']
        }
        
        for tag, keywords in keyword_tags.items():
            if any(keyword in content for keyword in keywords):
                tags.add(tag)
        
        return list(tags)[:8]  # Limitar a 8 tags
    
    def _extract_search_keywords(self, faq: Dict[str, Any]) -> List[str]:
        """Extraer palabras clave para búsqueda."""
        
        import re
        
        text = (faq.get('question', '') + ' ' + faq.get('short_answer', '')).lower()
        
        # Limpiar y extraer palabras clave
        words = re.findall(r'\b\w{4,}\b', text)  # Palabras de 4+ caracteres
        
        # Filtrar palabras comunes
        stop_words = {'para', 'como', 'donde', 'cuando', 'porque', 'sistema', 'puedo', 'debo'}
        keywords = [word for word in words if word not in stop_words]
        
        # Tomar las más relevantes
        return list(set(keywords))[:10]


def main():
    """Función principal."""
    
    print("🚀 Generador de Contenido Implementable para KBService")
    print("=" * 60)
    
    generator = SupportContentGenerator()
    
    # Generar contenido esencial
    content = generator.generate_essential_content()
    
    # Guardar en archivos separados por tipo
    for content_type, items in content.items():
        filename = f"implementable_{content_type}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        
        print(f"📄 {content_type.replace('_', ' ').title()}: {len(items)} elementos → {filename}")
    
    # Crear resumen de implementación
    implementation_summary = {
        'total_items': sum(len(items) for items in content.values()),
        'by_type': {k: len(v) for k, v in content.items()},
        'priority_distribution': {
            'critical': sum(1 for items in content.values() for item in items if item.get('priority') == 'critical'),
            'high': sum(1 for items in content.values() for item in items if item.get('priority') == 'high'),
            'medium': sum(1 for items in content.values() for item in items if item.get('priority') == 'medium')
        },
        'target_audience_coverage': {},
        'module_coverage': {},
        'implementation_order': [
            'critical_faqs (implementar primero)',
            'onboarding_guides (segunda prioridad)',
            'quick_reference_cards (tercera prioridad)',
            'troubleshooting_guides (cuarta prioridad)'
        ],
        'estimated_implementation_time': '2-3 días para contenido básico',
        'recommended_testing_time': '1 semana con usuarios reales'
    }
    
    # Calcular cobertura de audiencia
    all_audiences = set()
    for items in content.values():
        for item in items:
            audiences = item.get('target_audience', [])
            all_audiences.update(audiences)
    
    for audience in all_audiences:
        count = sum(1 for items in content.values() for item in items 
                   if audience in item.get('target_audience', []))
        implementation_summary['target_audience_coverage'][audience] = count
    
    # Guardar resumen
    with open('implementation_summary.json', 'w', encoding='utf-8') as f:
        json.dump(implementation_summary, f, ensure_ascii=False, indent=2)
    
    # Mostrar estadísticas
    print(f"\n📊 RESUMEN DE CONTENIDO GENERADO:")
    print(f"Total de elementos: {implementation_summary['total_items']}")
    
    print(f"\n🎯 Por tipo de contenido:")
    for content_type, count in implementation_summary['by_type'].items():
        print(f"  {content_type.replace('_', ' ').title()}: {count} elementos")
    
    print(f"\n🔥 Por prioridad:")
    for priority, count in implementation_summary['priority_distribution'].items():
        print(f"  {priority.title()}: {count} elementos")
    
    print(f"\n👥 Cobertura por audiencia:")
    for audience, count in implementation_summary['target_audience_coverage'].items():
        print(f"  {audience.title()}: {count} elementos")
    
    print(f"\n📋 ORDEN DE IMPLEMENTACIÓN RECOMENDADO:")
    for i, step in enumerate(implementation_summary['implementation_order'], 1):
        print(f"  {i}. {step}")
    
    print(f"\n⏱️ ESTIMACIONES:")
    print(f"  Tiempo de implementación: {implementation_summary['estimated_implementation_time']}")
    print(f"  Tiempo de testing: {implementation_summary['recommended_testing_time']}")
    
    print(f"\n💾 Archivos generados:")
    for content_type in content.keys():
        print(f"  📄 implementable_{content_type}.json")
    print(f"  📊 implementation_summary.json")
    
    print(f"\n✅ Contenido listo para implementar en KBService!")


if __name__ == "__main__":
    main()
