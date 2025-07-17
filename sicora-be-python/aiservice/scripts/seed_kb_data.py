"""
Data Seeder for KbService Integration
Script para inicializar la base de conocimiento con el Reglamento del Aprendiz SENA
"""
import asyncio
import httpx
import json
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class KbDataSeeder:
    """
    Seeder para inicializar datos en KbService.
    
    Carga el Reglamento del Aprendiz SENA como el documento principal
    de la base de conocimiento para el chatbot.
    """
    
    def __init__(self, kb_service_url: str = "http://localhost:8000/api/v1"):
        self.kb_service_url = kb_service_url
        self.client = httpx.AsyncClient(timeout=60)
    
    async def seed_regulatory_content(self):
        """Cargar contenido del Reglamento del Aprendiz SENA."""
        
        # Obtener contenido del reglamento
        regulatory_items = self._get_regulatory_items()
        
        logger.info(f"Seeding {len(regulatory_items)} regulatory items to KbService")
        
        success_count = 0
        error_count = 0
        
        for item in regulatory_items:
            try:
                await self._create_knowledge_item(item)
                success_count += 1
                logger.info(f"Successfully created: {item['title']}")
            except Exception as e:
                error_count += 1
                logger.error(f"Failed to create {item['title']}: {str(e)}")
        
        logger.info(f"Seeding completed: {success_count} success, {error_count} errors")
        return success_count, error_count
    
    def _get_regulatory_items(self) -> List[Dict[str, Any]]:
        """Obtener items del reglamento para cargar en la KB."""
        
        return [
            {
                "title": "Definición de Aprendiz SENA",
                "content": """
                Según el Reglamento del Aprendiz SENA (Acuerdo 9 de 2024), 
                el aprendiz es la persona que se matricula en el SENA para 
                desarrollar un programa de formación profesional integral.
                
                El aprendiz adquiere derechos y deberes específicos que 
                están establecidos en este reglamento.
                """,
                "category": "reglamento",
                "content_type": "article",
                "target_audience": "all",
                "tags": ["definición", "aprendiz", "matrícula"],
                "source": "Acuerdo 9 de 2024 - Reglamento del Aprendiz SENA"
            },
            {
                "title": "Derechos del Aprendiz",
                "content": """
                Los aprendices del SENA tienen derecho a:
                
                1. Recibir formación profesional integral de calidad
                2. Ser tratados con dignidad y respeto
                3. Participar en actividades de bienestar estudiantil
                4. Conocer los contenidos curriculares y metodologías
                5. Recibir certificación según su desempeño
                6. Utilizar los recursos bibliográficos y tecnológicos
                7. Participar en actividades culturales y deportivas
                8. Solicitar traslados y aplazamientos según normativa
                9. Presentar recursos de reposición y apelación
                10. Recibir tratamiento especial en caso de embarazo o lactancia
                """,
                "category": "reglamento",
                "content_type": "article", 
                "target_audience": "all",
                "tags": ["derechos", "formación", "bienestar", "certificación"],
                "source": "Acuerdo 9 de 2024 - Capítulo II - Derechos"
            },
            {
                "title": "Deberes del Aprendiz",
                "content": """
                Los aprendices del SENA tienen los siguientes deberes:
                
                1. Cumplir con las actividades de aprendizaje
                2. Respetar los derechos de los demás miembros de la comunidad
                3. Mantener un comportamiento ético y responsable
                4. Cuidar los recursos y bienes del SENA
                5. Informar irregularidades que afecten el proceso formativo
                6. Cumplir con los horarios establecidos
                7. Portar permanentemente el carné estudiantil
                8. Conservar y mantener los equipos en buen estado
                9. Asumir responsabilidades en actividades complementarias
                10. Informar cambios en datos personales
                """,
                "category": "reglamento",
                "content_type": "article",
                "target_audience": "all", 
                "tags": ["deberes", "responsabilidades", "ética", "horarios"],
                "source": "Acuerdo 9 de 2024 - Capítulo III - Deberes"
            },
            {
                "title": "Faltas Académicas y Disciplinarias",
                "content": """
                El reglamento establece diferentes tipos de faltas:
                
                **FALTAS ACADÉMICAS:**
                - No cumplir con actividades de aprendizaje
                - No presentar evidencias requeridas
                - Fraude en evaluaciones
                - Plagio en trabajos o proyectos
                
                **FALTAS DISCIPLINARIAS:**
                
                *Leves:*
                - Inasistencia sin justificación (hasta 3 días)
                - Incumplimiento del horario
                - No portar carné estudiantil
                
                *Graves:*
                - Inasistencia injustificada mayor a 3 días
                - Irrespeto a compañeros o instructores
                - Daño a recursos institucionales
                
                *Gravísimas:*
                - Agresión física o verbal
                - Fraude o falsificación de documentos
                - Porte o consumo de sustancias prohibidas
                """,
                "category": "reglamento",
                "content_type": "article",
                "target_audience": "all",
                "tags": ["faltas", "académicas", "disciplinarias", "sanciones"],
                "source": "Acuerdo 9 de 2024 - Capítulo IV - Faltas"
            },
            {
                "title": "Proceso Disciplinario y Sanciones",
                "content": """
                El proceso disciplinario garantiza el debido proceso:
                
                **ETAPAS DEL PROCESO:**
                1. Conocimiento de la falta
                2. Formulación de cargos
                3. Descargos del aprendiz
                4. Práctica de pruebas
                5. Decisión administrativa
                
                **MEDIDAS SANCIONATORIAS:**
                
                *Para faltas leves:*
                - Llamado de atención verbal
                - Llamado de atención escrito
                
                *Para faltas graves:*
                - Matrícula condicional
                - Suspensión temporal (hasta 30 días)
                
                *Para faltas gravísimas:*
                - Cancelación de matrícula
                - Exclusión del SENA
                
                **RECURSOS:**
                - Reposición: ante quien profirió la decisión
                - Apelación: ante el superior jerárquico
                """,
                "category": "reglamento", 
                "content_type": "procedure",
                "target_audience": "all",
                "tags": ["proceso", "sanciones", "debido proceso", "recursos"],
                "source": "Acuerdo 9 de 2024 - Capítulo V - Proceso Disciplinario"
            },
            {
                "title": "Control de Asistencia y Justificaciones",
                "content": """
                **CONTROL DE ASISTENCIA:**
                - Es obligatorio asistir al 90% de las actividades programadas
                - La asistencia se controla diariamente
                - Las inasistencias deben ser justificadas oportunamente
                
                **CAUSALES DE JUSTIFICACIÓN:**
                1. Incapacidad médica
                2. Licencia de maternidad/paternidad
                3. Fuerza mayor o caso fortuito
                4. Representación institucional
                5. Actividades académicas autorizadas
                
                **PROCEDIMIENTO PARA JUSTIFICAR:**
                1. Presentar solicitud dentro de los 3 días hábiles siguientes
                2. Adjuntar documentos soportes
                3. Recibir respuesta del coordinador académico
                4. Cumplir con actividades de recuperación si aplica
                
                **CONSECUENCIAS DE INASISTENCIAS:**
                - 1-3 días sin justificar: falta leve
                - Más de 3 días: falta grave
                - Pérdida del 10% de asistencia: cancelación de matrícula
                """,
                "category": "asistencia",
                "content_type": "procedure",
                "target_audience": "all",
                "tags": ["asistencia", "justificaciones", "inasistencias", "procedimiento"],
                "source": "Acuerdo 9 de 2024 - Disposiciones sobre asistencia"
            },
            {
                "title": "Evaluación del Aprendizaje",
                "content": """
                **SISTEMA DE EVALUACIÓN:**
                - La evaluación es integral, continua y permanente
                - Se evalúan conocimientos, desempeños y productos
                - Los juicios evaluativos son: Aprobado, No Aprobado, Aplazado
                
                **TIPOS DE EVALUACIÓN:**
                1. Diagnóstica: al inicio del proceso
                2. Formativa: durante el proceso
                3. Sumativa: al final de cada competencia
                
                **INSTRUMENTOS DE EVALUACIÓN:**
                - Listas de chequeo
                - Cuestionarios
                - Observación directa
                - Proyectos formativos
                - Evidencias de desempeño y producto
                
                **RECUPERACIÓN:**
                - Máximo 3 oportunidades por competencia
                - Plan de mejoramiento obligatorio
                - Acompañamiento del instructor
                
                **CERTIFICACIÓN:**
                - Certificado de competencias laborales
                - Diploma de formación técnica o tecnológica
                - Certificado de curso complementario
                """,
                "category": "evaluación",
                "content_type": "article",
                "target_audience": "all",
                "tags": ["evaluación", "competencias", "certificación", "recuperación"],
                "source": "Acuerdo 9 de 2024 - Sistema de evaluación"
            },
            {
                "title": "Preguntas Frecuentes - Justificación de Faltas",
                "content": """
                **¿Cómo justifico una falta por enfermedad?**
                Presenta incapacidad médica original dentro de los 3 días hábiles siguientes a la falta.
                
                **¿Puedo justificar una falta después de 3 días?**
                Solo en casos excepcionales de fuerza mayor debidamente comprobados.
                
                **¿Qué pasa si no justifico una falta?**
                Se considera falta leve (1-3 días) o grave (más de 3 días) según el caso.
                
                **¿Las citas médicas se justifican?**
                Sí, con la constancia médica que indique fecha, hora y duración de la cita.
                
                **¿Puedo faltar por trabajo?**
                Solo si es para aprendices de modalidad dual y está previamente autorizado.
                """,
                "category": "asistencia",
                "content_type": "faq",
                "target_audience": "student",
                "tags": ["faq", "justificaciones", "faltas", "procedimientos"],
                "source": "Manual de convivencia - Preguntas frecuentes"
            }
        ]
    
    async def _create_knowledge_item(self, item: Dict[str, Any]):
        """Crear un item de conocimiento en KbService."""
        
        payload = {
            "title": item["title"],
            "content": item["content"],
            "category": item["category"],
            "content_type": item["content_type"],
            "target_audience": item["target_audience"],
            "tags": item["tags"],
            "source": item["source"],
            "is_published": True
        }
        
        # Mock de headers de usuario autenticado
        headers = {
            "User-ID": "admin-seeder",
            "Content-Type": "application/json"
        }
        
        response = await self.client.post(
            f"{self.kb_service_url}/kb/items",
            json=payload,
            headers=headers
        )
        
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create item: {response.status_code} - {response.text}")
        
        return response.json()
    
    async def health_check_kb_service(self) -> bool:
        """Verificar que KbService esté disponible."""
        try:
            response = await self.client.get(f"{self.kb_service_url}/health")
            return response.status_code == 200
        except Exception:
            return False
    
    async def close(self):
        """Cerrar cliente HTTP."""
        await self.client.aclose()


async def main():
    """Función principal para ejecutar el seeder."""
    
    logging.basicConfig(level=logging.INFO)
    
    seeder = KbDataSeeder()
    
    try:
        # Verificar conectividad
        if not await seeder.health_check_kb_service():
            logger.error("KbService is not available. Please start KbService first.")
            return
        
        logger.info("KbService is available. Starting data seeding...")
        
        # Cargar datos del reglamento
        success, errors = await seeder.seed_regulatory_content()
        
        logger.info(f"Data seeding completed: {success} items created, {errors} errors")
        
    except Exception as e:
        logger.error(f"Seeding failed: {str(e)}")
    finally:
        await seeder.close()


if __name__ == "__main__":
    asyncio.run(main())
