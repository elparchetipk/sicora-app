#!/usr/bin/env python3
"""
Extractor de Contenido para KBService
Extrae y estructura información de requisitos funcionales e historias de usuario
para alimentar la base de conocimiento de soporte de SICORA.
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import markdown
from bs4 import BeautifulSoup


class KnowledgeExtractor:
    """Extractor de conocimiento desde documentación técnica."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.content_types = {
            'guide': 'Guía de usuario',
            'faq': 'Pregunta frecuente',
            'procedure': 'Procedimiento',
            'tutorial': 'Tutorial paso a paso',
            'article': 'Artículo informativo',
            'policy': 'Política o normativa'
        }
        
        # Categorías por tipo de usuario
        self.user_categories = {
            'aprendices': ['aprendiz', 'estudiante', 'formación', 'asistencia', 'evaluación'],
            'instructores': ['instructor', 'docente', 'clase', 'horario', 'evaluación', 'comité'],
            'administrativos': ['admin', 'coordinador', 'director', 'gestión', 'reportes'],
            'general': ['sistema', 'login', 'sesión', 'autenticación', 'password']
        }
        
    def extract_from_requirements(self, rf_files: List[str]) -> List[Dict[str, Any]]:
        """Extraer información de archivos de requisitos funcionales."""
        
        knowledge_items = []
        
        for rf_file in rf_files:
            file_path = self.base_path / rf_file
            if not file_path.exists():
                continue
                
            print(f"📄 Procesando: {rf_file}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraer información del archivo
                items = self._process_requirements_file(content, rf_file)
                knowledge_items.extend(items)
                
            except Exception as e:
                print(f"❌ Error procesando {rf_file}: {e}")
                
        return knowledge_items
    
    def extract_from_user_stories(self, story_files: List[str]) -> List[Dict[str, Any]]:
        """Extraer información de historias de usuario."""
        
        knowledge_items = []
        
        for story_file in story_files:
            file_path = self.base_path / story_file
            if not file_path.exists():
                continue
                
            print(f"📚 Procesando: {story_file}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraer historias
                items = self._process_user_stories_file(content, story_file)
                knowledge_items.extend(items)
                
            except Exception as e:
                print(f"❌ Error procesando {story_file}: {e}")
                
        return knowledge_items
    
    def _process_requirements_file(self, content: str, filename: str) -> List[Dict[str, Any]]:
        """Procesar archivo de requisitos funcionales."""
        
        items = []
        
        # Extraer el nombre del servicio
        service_name = self._extract_service_name(filename)
        
        # Buscar secciones principales
        sections = self._extract_sections(content)
        
        for section in sections:
            if len(section['content']) < 50:  # Filtrar secciones muy cortas
                continue
                
            # Determinar tipo de contenido
            content_type = self._classify_content_type(section['title'], section['content'])
            
            # Determinar audiencia objetivo
            target_audience = self._determine_target_audience(section['content'])
            
            # Crear item de conocimiento
            item = {
                'title': f"{service_name}: {section['title']}",
                'content': section['content'],
                'content_type': content_type,
                'category': service_name.lower(),
                'target_audience': target_audience,
                'tags': self._extract_tags(section['content'], service_name),
                'source_file': filename,
                'source_type': 'requirements',
                'metadata': {
                    'service': service_name,
                    'section_level': section['level'],
                    'extracted_at': datetime.utcnow().isoformat()
                }
            }
            
            items.append(item)
            
        return items
    
    def _process_user_stories_file(self, content: str, filename: str) -> List[Dict[str, Any]]:
        """Procesar archivo de historias de usuario."""
        
        items = []
        
        # Extraer historias individuales
        stories = self._extract_user_stories(content)
        
        for story in stories:
            if len(story['description']) < 30:
                continue
                
            # Crear guía de usuario basada en la historia
            guide_content = self._convert_story_to_guide(story)
            
            # Determinar audiencia
            target_audience = self._extract_user_role_from_story(story)
            
            item = {
                'title': f"Cómo {story['title']}",
                'content': guide_content,
                'content_type': 'guide',
                'category': story.get('module', 'general'),
                'target_audience': target_audience,
                'tags': self._extract_tags_from_story(story),
                'source_file': filename,
                'source_type': 'user_story',
                'metadata': {
                    'story_id': story.get('id', ''),
                    'status': story.get('status', 'pendiente'),
                    'extracted_at': datetime.utcnow().isoformat()
                }
            }
            
            items.append(item)
            
        return items
    
    def _extract_service_name(self, filename: str) -> str:
        """Extraer nombre del servicio desde el filename."""
        
        service_map = {
            'userservice': 'UserService',
            'attendanceservice': 'AttendanceService', 
            'scheduleservice': 'ScheduleService',
            'evalinservice': 'EvalinService',
            'mevalservice': 'MevalService',
            'projectevalservice': 'ProjectEvalService',
            'kbservice': 'KbService',
            'aiservice': 'AIService',
            'apigateway': 'API Gateway',
            'acadservice': 'AcadService'
        }
        
        for key, value in service_map.items():
            if key in filename.lower():
                return value
                
        return 'SICORA'
    
    def _extract_sections(self, content: str) -> List[Dict[str, Any]]:
        """Extraer secciones del contenido markdown."""
        
        sections = []
        
        # Buscar headers de markdown
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detectar headers (# ## ### etc.)
            if line.startswith('#'):
                # Guardar sección anterior si existe
                if current_section and current_section['content'].strip():
                    sections.append(current_section)
                
                # Iniciar nueva sección
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                
                current_section = {
                    'title': title,
                    'level': level,
                    'content': ''
                }
            elif current_section:
                current_section['content'] += line + '\n'
        
        # Agregar última sección
        if current_section and current_section['content'].strip():
            sections.append(current_section)
            
        return sections
    
    def _extract_user_stories(self, content: str) -> List[Dict[str, Any]]:
        """Extraer historias de usuario individuales."""
        
        stories = []
        
        # Patrón para historias de usuario
        story_pattern = r'\*\*([^*]+)\*\*[^*]*?[\n\r]+(.*?)(?=\*\*|\Z)'
        
        matches = re.findall(story_pattern, content, re.DOTALL | re.MULTILINE)
        
        for i, (title, description) in enumerate(matches):
            # Limpiar contenido
            title = title.strip()
            description = description.strip()
            
            # Extraer ID si existe
            id_match = re.search(r'HU-[A-Z]+-[A-Z]*-?(\d+)', title)
            story_id = id_match.group(0) if id_match else f"STORY-{i+1}"
            
            # Extraer estado
            status = 'pendiente'
            if '✅' in description:
                status = 'completado'
            elif '🚧' in description:
                status = 'en_desarrollo'
            elif '❌' in description:
                status = 'bloqueado'
            
            story = {
                'id': story_id,
                'title': title,
                'description': description,
                'status': status
            }
            
            stories.append(story)
            
        return stories
    
    def _convert_story_to_guide(self, story: Dict[str, Any]) -> str:
        """Convertir historia de usuario en guía práctica."""
        
        description = story['description']
        
        # Extraer componentes de la historia
        como_match = re.search(r'Como\*\*\s+([^*]+)', description, re.IGNORECASE)
        quiero_match = re.search(r'Quiero\*\*\s+([^*]+)', description, re.IGNORECASE)
        para_match = re.search(r'Para\*\*\s+([^*]+)', description, re.IGNORECASE)
        
        guide = f"# {story['title']}\n\n"
        
        if como_match:
            role = como_match.group(1).strip()
            guide += f"**Dirigido a:** {role}\n\n"
        
        if quiero_match and para_match:
            action = quiero_match.group(1).strip()
            purpose = para_match.group(1).strip()
            
            guide += f"**Objetivo:** {purpose}\n\n"
            guide += f"**Acción:** {action}\n\n"
        
        # Agregar estado de implementación
        status_map = {
            'completado': '✅ **Disponible** - Esta funcionalidad está implementada y lista para usar.',
            'en_desarrollo': '🚧 **En desarrollo** - Esta funcionalidad está siendo desarrollada.',
            'pendiente': '📋 **Próximamente** - Esta funcionalidad está planificada para futuras versiones.',
            'bloqueado': '❌ **No disponible** - Esta funcionalidad requiere revisión técnica.'
        }
        
        status_text = status_map.get(story['status'], '📋 Estado desconocido')
        guide += f"**Estado actual:** {status_text}\n\n"
        
        # Agregar información adicional si está disponible
        if story['status'] == 'completado':
            guide += "## Cómo usar esta funcionalidad\n\n"
            guide += "Esta funcionalidad está disponible en la aplicación SICORA. "
            guide += "Consulta con tu instructor o coordinador si necesitas ayuda para acceder.\n\n"
        
        return guide
    
    def _classify_content_type(self, title: str, content: str) -> str:
        """Clasificar tipo de contenido."""
        
        title_lower = title.lower()
        content_lower = content.lower()
        
        if any(word in title_lower for word in ['cómo', 'tutorial', 'guía', 'paso']):
            return 'tutorial'
        elif any(word in title_lower for word in ['procedimiento', 'proceso']):
            return 'procedure'
        elif any(word in title_lower for word in ['política', 'norma', 'reglamento']):
            return 'policy'
        elif any(word in content_lower for word in ['faq', 'pregunta', 'frecuente']):
            return 'faq'
        elif any(word in title_lower for word in ['requisito', 'funcional']):
            return 'article'
        else:
            return 'guide'
    
    def _determine_target_audience(self, content: str) -> str:
        """Determinar audiencia objetivo del contenido."""
        
        content_lower = content.lower()
        
        # Contar menciones por categoría
        scores = {}
        for audience, keywords in self.user_categories.items():
            score = sum(content_lower.count(keyword) for keyword in keywords)
            if score > 0:
                scores[audience] = score
        
        if not scores:
            return 'general'
            
        # Retornar audiencia con mayor score
        return max(scores, key=scores.get)
    
    def _extract_tags(self, content: str, service_name: str) -> List[str]:
        """Extraer tags relevantes del contenido."""
        
        tags = [service_name.lower()]
        
        # Tags comunes por palabras clave
        tag_keywords = {
            'autenticacion': ['login', 'sesión', 'contraseña', 'token'],
            'asistencia': ['asistencia', 'presente', 'ausente', 'tardanza'],
            'evaluacion': ['evaluación', 'calificación', 'nota', 'resultado'],
            'horarios': ['horario', 'clase', 'ambiente', 'programación'],
            'reportes': ['reporte', 'estadística', 'gráfico', 'dashboard'],
            'usuarios': ['usuario', 'perfil', 'rol', 'permiso'],
            'notificaciones': ['notificación', 'alerta', 'mensaje', 'email']
        }
        
        content_lower = content.lower()
        for tag, keywords in tag_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag)
        
        return tags[:8]  # Limitar a 8 tags máximo
    
    def _extract_user_role_from_story(self, story: Dict[str, Any]) -> str:
        """Extraer rol de usuario de la historia."""
        
        description = story['description'].lower()
        
        if any(word in description for word in ['aprendiz', 'estudiante']):
            return 'aprendices'
        elif any(word in description for word in ['instructor', 'docente']):
            return 'instructores'
        elif any(word in description for word in ['admin', 'coordinador']):
            return 'administrativos'
        else:
            return 'general'
    
    def _extract_tags_from_story(self, story: Dict[str, Any]) -> List[str]:
        """Extraer tags de una historia de usuario."""
        
        tags = []
        
        # Tags basados en el ID de la historia
        story_id = story.get('id', '')
        if 'KB' in story_id:
            tags.append('base-conocimiento')
        elif 'FE' in story_id:
            tags.append('frontend')
        elif 'BE' in story_id:
            tags.append('backend')
            
        # Tags basados en el contenido
        content = story['description'].lower()
        
        if 'login' in content or 'sesión' in content:
            tags.append('autenticacion')
        if 'búsqueda' in content or 'buscar' in content:
            tags.append('busqueda')
        if 'dashboard' in content or 'panel' in content:
            tags.append('dashboard')
        if 'asistente' in content or 'chat' in content:
            tags.append('asistente-virtual')
            
        return tags


def main():
    """Función principal."""
    
    if len(sys.argv) < 2:
        print("Uso: python extract_knowledge.py <base_path>")
        return
    
    base_path = sys.argv[1]
    extractor = KnowledgeExtractor(base_path)
    
    print("🚀 EXTRACTOR DE CONOCIMIENTO PARA KBSERVICE")
    print("="*60)
    
    # Archivos de requisitos funcionales
    rf_files = [
        'sicora-docs/_docs/general/rf.md',
        'sicora-docs/_docs/general/rf_kbservice.md',
        'sicora-docs/_docs/general/rf_userservice.md',
        'sicora-docs/_docs/general/rf_attendanceservice.md',
        'sicora-docs/_docs/general/rf_scheduleservice.md',
        'sicora-docs/_docs/general/rf_evalinservice.md',
        'sicora-docs/_docs/general/rf_mevalservice.md',
        'sicora-docs/_docs/general/rf_projectevalservice.md',
        'sicora-docs/_docs/general/rf_aiservice.md',
        'sicora-docs/_docs/general/rf_apigateway.md'
    ]
    
    # Archivos de historias de usuario
    story_files = [
        'sicora-app-web/_docs/stories/fe/historias_usuario_fe.md',
        'sicora-app-web/_docs/stories/fe/historias_usuario_fe_kbservice.md',
        'sicora-app-web/_docs/stories/fe/historias_usuario_fe_userservice.md',
        'sicora-app-web/_docs/stories/fe/historias_usuario_fe_evalinservice.md',
        'sicora-app-web/_docs/stories/be-backend/historias_usuario_be.md',
        'sicora-app-web/_docs/stories/be-backend/historias_usuario_be_kbservice.md',
        'sicora-app-web/_docs/stories/be-backend/historias_usuario_be_evalinservice.md'
    ]
    
    # Extraer conocimiento
    print("\n📄 Procesando requisitos funcionales...")
    rf_items = extractor.extract_from_requirements(rf_files)
    print(f"✅ Extraídos {len(rf_items)} items de requisitos")
    
    print("\n📚 Procesando historias de usuario...")
    story_items = extractor.extract_from_user_stories(story_files)
    print(f"✅ Extraídos {len(story_items)} items de historias")
    
    # Combinar resultados
    all_items = rf_items + story_items
    
    # Estadísticas
    print("\n📊 ESTADÍSTICAS DE EXTRACCIÓN")
    print("="*40)
    print(f"Total de items extraídos: {len(all_items)}")
    
    # Por tipo de contenido
    content_types = {}
    for item in all_items:
        ct = item['content_type']
        content_types[ct] = content_types.get(ct, 0) + 1
    
    print("\nPor tipo de contenido:")
    for ct, count in content_types.items():
        print(f"  {ct}: {count}")
    
    # Por audiencia
    audiences = {}
    for item in all_items:
        aud = item['target_audience']
        audiences[aud] = audiences.get(aud, 0) + 1
    
    print("\nPor audiencia objetivo:")
    for aud, count in audiences.items():
        print(f"  {aud}: {count}")
    
    # Guardar resultado
    output_file = 'knowledge_base_content.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Contenido guardado en: {output_file}")
    print(f"📋 Listo para importar al KBService")
    
    # Mostrar muestra
    print(f"\n📝 Muestra de contenido extraído:")
    for i, item in enumerate(all_items[:3]):
        print(f"\n{i+1}. {item['title']}")
        print(f"   Tipo: {item['content_type']}")
        print(f"   Audiencia: {item['target_audience']}")
        print(f"   Tags: {', '.join(item['tags'])}")
        print(f"   Contenido: {item['content'][:100]}...")


if __name__ == "__main__":
    main()
