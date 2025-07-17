#!/usr/bin/env python3
"""
Extractor Mejorado de Contenido de Soporte para KBService
Enfocado específicamente en extraer información útil para soporte primario 
de usuarios sobre cómo interactuar con los diferentes módulos de SICORA.
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
import markdown
from bs4 import BeautifulSoup


class SupportKnowledgeExtractor:
    """Extractor especializado en información de soporte para usuarios."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        
        # Patrones específicos para identificar información de soporte
        self.support_patterns = {
            'how_to': [
                r'como\s+.*?(?:hacer|usar|acceder|configurar|gestionar)',
                r'pasos\s+para',
                r'procedimiento\s+para',
                r'instrucciones\s+para',
                r'guía\s+para'
            ],
            'troubleshooting': [
                r'problema.*?solución',
                r'error.*?resolución',
                r'no\s+funciona',
                r'fallo.*?corrección',
                r'troubleshooting'
            ],
            'faq': [
                r'pregunta.*?frecuente',
                r'qué\s+es',
                r'cómo\s+se',
                r'cuándo\s+se',
                r'por\s+qué',
                r'FAQ'
            ],
            'user_interface': [
                r'pantalla\s+de',
                r'interfaz\s+de',
                r'formulario\s+de',
                r'ventana\s+de',
                r'botón\s+de',
                r'menú\s+de'
            ],
            'workflows': [
                r'flujo\s+de\s+trabajo',
                r'proceso\s+de',
                r'secuencia\s+de',
                r'workflow',
                r'procedimiento\s+estándar'
            ]
        }
        
        # Módulos de SICORA para categorización
        self.sicora_modules = {
            'attendanceservice': {
                'name': 'Asiste (Control de Asistencia)',
                'keywords': ['asistencia', 'tardanza', 'falta', 'excusa', 'presencia'],
                'user_actions': [
                    'marcar asistencia',
                    'consultar historial de asistencia',
                    'registrar tardanza',
                    'justificar falta',
                    'revisar política de asistencia'
                ]
            },
            'scheduleservice': {
                'name': 'Horarios (Gestión de Horarios y Ambientes)',
                'keywords': ['horario', 'ambiente', 'aula', 'programación', 'calendario'],
                'user_actions': [
                    'consultar horario personal',
                    'ver disponibilidad de ambientes',
                    'programar clases',
                    'modificar horarios',
                    'gestionar ambientes de formación'
                ]
            },
            'evalinservice': {
                'name': 'Evaluación de Instructores',
                'keywords': ['evaluación', 'instructor', 'desempeño', 'calificación'],
                'user_actions': [
                    'evaluar instructor',
                    'consultar resultados de evaluación',
                    'participar en evaluación docente',
                    'revisar criterios de evaluación'
                ]
            },
            'mevalservice': {
                'name': 'Comité (Gestión de Comités Académicos)',
                'keywords': ['comité', 'reunión', 'decisión', 'académico', 'evaluación'],
                'user_actions': [
                    'participar en comité',
                    'consultar actas de comité',
                    'programar reuniones',
                    'revisar decisiones académicas'
                ]
            },
            'projectevalservice': {
                'name': 'Evaluación de Proyectos',
                'keywords': ['proyecto', 'evaluación', 'formativo', 'práctica'],
                'user_actions': [
                    'evaluar proyecto formativo',
                    'consultar criterios de evaluación',
                    'revisar proyectos asignados',
                    'calificar entregables'
                ]
            },
            'userservice': {
                'name': 'Gestión de Usuarios',
                'keywords': ['usuario', 'perfil', 'cuenta', 'autenticación', 'sesión'],
                'user_actions': [
                    'iniciar sesión',
                    'cambiar contraseña',
                    'actualizar perfil',
                    'recuperar contraseña',
                    'gestionar roles'
                ]
            },
            'kbservice': {
                'name': 'Base de Conocimiento',
                'keywords': ['ayuda', 'documentación', 'soporte', 'FAQ', 'tutorial'],
                'user_actions': [
                    'buscar información',
                    'acceder a tutoriales',
                    'consultar FAQs',
                    'obtener ayuda',
                    'reportar problemas'
                ]
            }
        }
        
        # Tipos de usuarios con necesidades específicas
        self.user_profiles = {
            'aprendices': {
                'needs': [
                    'procedimientos básicos',
                    'acceso a funciones estudiantiles',
                    'consulta de información personal',
                    'cumplimiento de requisitos',
                    'resolución de problemas comunes'
                ],
                'priority_modules': ['attendanceservice', 'scheduleservice', 'userservice', 'evalinservice']
            },
            'instructores': {
                'needs': [
                    'gestión de clases',
                    'evaluación de estudiantes',
                    'administración de horarios',
                    'generación de reportes',
                    'uso de herramientas pedagógicas'
                ],
                'priority_modules': ['scheduleservice', 'attendanceservice', 'evalinservice', 'projectevalservice']
            },
            'administrativos': {
                'needs': [
                    'supervisión de procesos',
                    'generación de reportes',
                    'gestión de usuarios',
                    'configuración del sistema',
                    'resolución de incidencias'
                ],
                'priority_modules': ['userservice', 'mevalservice', 'scheduleservice', 'kbservice']
            }
        }
    
    def extract_support_content(self) -> List[Dict[str, Any]]:
        """Extraer contenido específico de soporte de usuarios."""
        
        print("🔍 Iniciando extracción de contenido de soporte...")
        
        # Buscar archivos de documentación
        rf_files = list(self.base_path.glob("**/rf*.md"))
        story_files = list(self.base_path.glob("**/historias*.md"))
        
        print(f"📄 Encontrados {len(rf_files)} archivos de requisitos funcionales")
        print(f"📚 Encontrados {len(story_files)} archivos de historias de usuario")
        
        support_items = []
        
        # Procesar requisitos funcionales
        for rf_file in rf_files:
            items = self._extract_from_requirements(rf_file)
            support_items.extend(items)
            
        # Procesar historias de usuario
        for story_file in story_files:
            items = self._extract_from_stories(story_file)
            support_items.extend(items)
        
        # Post-procesar y enriquecer
        enriched_items = self._enrich_support_content(support_items)
        
        print(f"✅ Extraídos {len(enriched_items)} elementos de soporte")
        return enriched_items
    
    def _extract_from_requirements(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extraer información de soporte de requisitos funcionales."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")
            return []
        
        items = []
        
        # Determinar módulo por nombre de archivo
        module = self._identify_module(file_path.name)
        
        # Buscar secciones de funcionalidades
        sections = self._extract_functional_sections(content)
        
        for section in sections:
            # Extraer información específica de soporte
            support_info = self._extract_support_info(section, module)
            if support_info:
                support_info['source_file'] = str(file_path.relative_to(self.base_path))
                support_info['source_type'] = 'requirements'
                items.append(support_info)
        
        return items
    
    def _extract_from_stories(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extraer información de soporte de historias de usuario."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")
            return []
        
        items = []
        
        # Determinar módulo y tipo de frontend/backend
        module = self._identify_module(file_path.name)
        ui_type = 'frontend' if 'fe' in file_path.name else 'backend'
        
        # Extraer historias individuales
        stories = self._extract_user_stories(content)
        
        for story in stories:
            # Convertir historia en información de soporte
            support_info = self._story_to_support(story, module, ui_type)
            if support_info:
                support_info['source_file'] = str(file_path.relative_to(self.base_path))
                support_info['source_type'] = 'user_story'
                items.append(support_info)
        
        return items
    
    def _identify_module(self, filename: str) -> str:
        """Identificar el módulo de SICORA basado en el nombre del archivo."""
        
        filename_lower = filename.lower()
        
        for module_key in self.sicora_modules.keys():
            if module_key in filename_lower:
                return module_key
        
        # Mapeos adicionales
        module_mappings = {
            'asiste': 'attendanceservice',
            'horario': 'scheduleservice',
            'evalin': 'evalinservice',
            'comite': 'mevalservice',
            'proyecto': 'projectevalservice',
            'user': 'userservice',
            'kb': 'kbservice'
        }
        
        for key, module in module_mappings.items():
            if key in filename_lower:
                return module
        
        return 'general'
    
    def _extract_functional_sections(self, content: str) -> List[Dict[str, Any]]:
        """Extraer secciones funcionales de un documento."""
        
        sections = []
        
        # Dividir por encabezados
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Detectar encabezados
            if re.match(r'^#+\s+', line):
                # Guardar sección anterior si existe
                if current_section and current_content:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content),
                        'level': len(re.match(r'^(#+)', line).group(1))
                    })
                
                # Iniciar nueva sección
                current_section = re.sub(r'^#+\s+', '', line).strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Agregar última sección
        if current_section and current_content:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content),
                'level': len(re.match(r'^(#+)', current_section).group(1)) if re.match(r'^#+', current_section) else 2
            })
        
        return sections
    
    def _extract_user_stories(self, content: str) -> List[Dict[str, Any]]:
        """Extraer historias de usuario individuales."""
        
        stories = []
        
        # Patrón para historias de usuario
        story_pattern = r'\*\*HU-.*?\*\*:?\s*(.*?)(?=\*\*HU-|\*\*Como|\Z)'
        
        matches = re.finditer(story_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            story_content = match.group(1).strip()
            
            # Extraer componentes de la historia
            story_data = self._parse_user_story(story_content)
            if story_data:
                stories.append(story_data)
        
        return stories
    
    def _parse_user_story(self, content: str) -> Optional[Dict[str, Any]]:
        """Parsear una historia de usuario individual."""
        
        # Buscar patrones de historia de usuario
        como_match = re.search(r'\*\*Como\*\*\s+(.*?)(?:\n|\*\*)', content, re.IGNORECASE)
        quiero_match = re.search(r'\*\*Quiero\*\*\s+(.*?)(?:\n|\*\*)', content, re.IGNORECASE)
        para_match = re.search(r'\*\*Para\*\*\s+(.*?)(?:\n|\*\*)', content, re.IGNORECASE)
        
        if not (como_match and quiero_match and para_match):
            return None
        
        return {
            'role': como_match.group(1).strip(),
            'action': quiero_match.group(1).strip(),
            'benefit': para_match.group(1).strip(),
            'full_content': content
        }
    
    def _extract_support_info(self, section: Dict[str, Any], module: str) -> Optional[Dict[str, Any]]:
        """Extraer información específica de soporte de una sección."""
        
        content = section['content']
        title = section['title']
        
        # Verificar si la sección contiene información de soporte
        support_score = 0
        support_type = None
        
        for pattern_type, patterns in self.support_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    support_score += 1
                    support_type = pattern_type
        
        if support_score == 0:
            return None
        
        # Extraer información útil
        return {
            'title': f"{self.sicora_modules.get(module, {}).get('name', module.upper())}: {title}",
            'content': content[:1000],  # Limitar contenido
            'support_type': support_type,
            'module': module,
            'target_users': self._identify_target_users(content),
            'keywords': self._extract_keywords(content, module),
            'priority': self._calculate_priority(content, module),
            'extracted_at': datetime.utcnow().isoformat()
        }
    
    def _story_to_support(self, story: Dict[str, Any], module: str, ui_type: str) -> Optional[Dict[str, Any]]:
        """Convertir una historia de usuario en información de soporte."""
        
        if not story.get('action'):
            return None
        
        # Crear título descriptivo
        title = f"Cómo {story['action']}"
        
        # Crear contenido de soporte
        content = f"""
**Objetivo:** {story['action']}

**Beneficio:** {story['benefit']}

**Tipo de usuario:** {story['role']}

**Interfaz:** {ui_type}

**Procedimiento:** Para {story['action']}, el usuario debe {story['benefit']}.
"""
        
        return {
            'title': title,
            'content': content,
            'support_type': 'procedure',
            'module': module,
            'ui_type': ui_type,
            'target_users': [self._normalize_user_role(story['role'])],
            'keywords': self._extract_keywords(story['action'], module),
            'priority': 'high' if any(keyword in story['action'].lower() for keyword in ['login', 'sesión', 'contraseña', 'asistencia']) else 'medium',
            'extracted_at': datetime.utcnow().isoformat()
        }
    
    def _identify_target_users(self, content: str) -> List[str]:
        """Identificar usuarios objetivo basado en el contenido."""
        
        users = []
        content_lower = content.lower()
        
        user_keywords = {
            'aprendices': ['aprendiz', 'estudiante', 'formación', 'alumno'],
            'instructores': ['instructor', 'docente', 'profesor', 'facilitador'],
            'administrativos': ['admin', 'coordinador', 'director', 'administrativo']
        }
        
        for user_type, keywords in user_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                users.append(user_type)
        
        return users if users else ['general']
    
    def _normalize_user_role(self, role: str) -> str:
        """Normalizar rol de usuario."""
        
        role_lower = role.lower()
        
        if any(keyword in role_lower for keyword in ['aprendiz', 'estudiante', 'alumno']):
            return 'aprendices'
        elif any(keyword in role_lower for keyword in ['instructor', 'docente', 'profesor']):
            return 'instructores'
        elif any(keyword in role_lower for keyword in ['admin', 'coordinador', 'director']):
            return 'administrativos'
        else:
            return 'general'
    
    def _extract_keywords(self, content: str, module: str) -> List[str]:
        """Extraer palabras clave relevantes."""
        
        keywords = set()
        content_lower = content.lower()
        
        # Agregar palabras clave del módulo
        if module in self.sicora_modules:
            keywords.update(self.sicora_modules[module]['keywords'])
        
        # Extraer palabras clave técnicas
        tech_keywords = [
            'login', 'sesión', 'contraseña', 'autenticación',
            'horario', 'ambiente', 'aula', 'programación',
            'asistencia', 'tardanza', 'falta', 'excusa',
            'evaluación', 'calificación', 'desempeño',
            'comité', 'reunión', 'acta', 'decisión',
            'proyecto', 'formativo', 'práctica', 'entregable',
            'usuario', 'perfil', 'cuenta', 'rol',
            'ayuda', 'soporte', 'documentación', 'tutorial'
        ]
        
        for keyword in tech_keywords:
            if keyword in content_lower:
                keywords.add(keyword)
        
        return list(keywords)[:10]  # Limitar a 10 keywords
    
    def _calculate_priority(self, content: str, module: str) -> str:
        """Calcular prioridad basada en contenido y módulo."""
        
        content_lower = content.lower()
        
        # Alta prioridad para funciones críticas
        high_priority_keywords = [
            'login', 'sesión', 'contraseña', 'autenticación',
            'asistencia', 'tardanza', 'horario', 'evaluación'
        ]
        
        if any(keyword in content_lower for keyword in high_priority_keywords):
            return 'high'
        
        # Prioridad media para módulos importantes
        if module in ['userservice', 'attendanceservice', 'scheduleservice']:
            return 'medium'
        
        return 'low'
    
    def _enrich_support_content(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enriquecer contenido con información adicional."""
        
        enriched_items = []
        
        for item in items:
            # Agregar información del módulo
            module = item.get('module', 'general')
            if module in self.sicora_modules:
                module_info = self.sicora_modules[module]
                item['module_name'] = module_info['name']
                item['related_actions'] = module_info['user_actions']
            
            # Agregar tags mejorados
            item['tags'] = self._generate_enhanced_tags(item)
            
            # Agregar ID único
            item['id'] = self._generate_id(item)
            
            # Agregar categoría
            item['category'] = module
            
            # Agregar estado
            item['status'] = 'published'
            
            enriched_items.append(item)
        
        return enriched_items
    
    def _generate_enhanced_tags(self, item: Dict[str, Any]) -> List[str]:
        """Generar tags mejorados para búsqueda."""
        
        tags = set()
        
        # Tags del módulo
        module = item.get('module', 'general')
        tags.add(module)
        
        # Tags de keywords
        keywords = item.get('keywords', [])
        tags.update(keywords)
        
        # Tags de tipo de soporte
        support_type = item.get('support_type')
        if support_type:
            tags.add(support_type)
        
        # Tags de usuarios objetivo
        target_users = item.get('target_users', [])
        tags.update(target_users)
        
        # Tags de UI
        ui_type = item.get('ui_type')
        if ui_type:
            tags.add(ui_type)
        
        return list(tags)[:15]  # Limitar tags
    
    def _generate_id(self, item: Dict[str, Any]) -> str:
        """Generar ID único para el item."""
        
        import hashlib
        
        content = f"{item.get('title', '')}{item.get('module', '')}{item.get('support_type', '')}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def generate_support_statistics(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generar estadísticas del contenido de soporte."""
        
        stats = {
            'total_items': len(items),
            'by_module': {},
            'by_support_type': {},
            'by_target_user': {},
            'by_priority': {},
            'coverage_analysis': {}
        }
        
        for item in items:
            # Por módulo
            module = item.get('module', 'general')
            stats['by_module'][module] = stats['by_module'].get(module, 0) + 1
            
            # Por tipo de soporte
            support_type = item.get('support_type', 'other')
            stats['by_support_type'][support_type] = stats['by_support_type'].get(support_type, 0) + 1
            
            # Por usuario objetivo
            target_users = item.get('target_users', ['general'])
            for user in target_users:
                stats['by_target_user'][user] = stats['by_target_user'].get(user, 0) + 1
            
            # Por prioridad
            priority = item.get('priority', 'low')
            stats['by_priority'][priority] = stats['by_priority'].get(priority, 0) + 1
        
        # Análisis de cobertura
        for module, module_info in self.sicora_modules.items():
            module_items = stats['by_module'].get(module, 0)
            total_actions = len(module_info['user_actions'])
            coverage = (module_items / max(total_actions, 1)) * 100
            
            stats['coverage_analysis'][module] = {
                'items': module_items,
                'expected_actions': total_actions,
                'coverage_percentage': round(coverage, 2)
            }
        
        return stats


def main():
    """Función principal."""
    
    print("🚀 Extractor Mejorado de Contenido de Soporte para KBService")
    print("=" * 60)
    
    # Configurar rutas
    base_path = Path("/home/epti/Documentos/epti-dev/sicora-app")
    
    # Crear extractor
    extractor = SupportKnowledgeExtractor(str(base_path))
    
    # Extraer contenido
    support_items = extractor.extract_support_content()
    
    # Generar estadísticas
    stats = extractor.generate_support_statistics(support_items)
    
    # Guardar resultados
    output_file = "enhanced_support_knowledge.json"
    stats_file = "support_statistics.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(support_items, f, ensure_ascii=False, indent=2)
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 ESTADÍSTICAS DE CONTENIDO DE SOPORTE")
    print(f"Total de elementos: {stats['total_items']}")
    print(f"\n📱 Por módulo:")
    for module, count in stats['by_module'].items():
        print(f"  {module}: {count} elementos")
    
    print(f"\n🛠️ Por tipo de soporte:")
    for support_type, count in stats['by_support_type'].items():
        print(f"  {support_type}: {count} elementos")
    
    print(f"\n👥 Por usuario objetivo:")
    for user_type, count in stats['by_target_user'].items():
        print(f"  {user_type}: {count} elementos")
    
    print(f"\n📈 Análisis de cobertura:")
    for module, analysis in stats['coverage_analysis'].items():
        print(f"  {module}: {analysis['coverage_percentage']}% de cobertura ({analysis['items']}/{analysis['expected_actions']})")
    
    print(f"\n💾 Resultados guardados en:")
    print(f"  📄 Contenido: {output_file}")
    print(f"  📊 Estadísticas: {stats_file}")
    
    print(f"\n✅ Extracción completada exitosamente!")


if __name__ == "__main__":
    main()
