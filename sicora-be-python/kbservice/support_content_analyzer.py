#!/usr/bin/env python3
"""
Analizador de Información Útil para Soporte Primario de SICORA
Identifica y categoriza la información más valiosa para resolver consultas de usuarios
"""

import json
import re
from typing import List, Dict, Any, Set
from collections import defaultdict, Counter
from pathlib import Path


class SupportContentAnalyzer:
    """Analizador de contenido útil para soporte primario."""
    
    def __init__(self):
        # Tipos de consultas comunes de usuarios
        self.common_user_queries = {
            'authentication': [
                "¿Cómo ingreso al sistema?",
                "Olvidé mi contraseña",
                "No puedo iniciar sesión",
                "¿Cómo cambio mi contraseña?",
                "Mi cuenta está bloqueada"
            ],
            'attendance': [
                "¿Cómo marco asistencia?",
                "¿Qué pasa si llego tarde?",
                "¿Cómo justifico una falta?",
                "¿Dónde veo mi historial de asistencia?",
                "¿Cuántas faltas puedo tener?"
            ],
            'schedules': [
                "¿Dónde veo mi horario?",
                "¿Cómo sé qué ambiente me toca?",
                "Mi horario cambió, ¿dónde lo verifico?",
                "¿Cómo programo una clase?",
                "¿Cómo reservo un ambiente?"
            ],
            'evaluations': [
                "¿Cómo evalúo a un instructor?",
                "¿Dónde veo mis calificaciones?",
                "¿Cómo funciona la evaluación de proyectos?",
                "¿Cuándo son las evaluaciones?",
                "¿Qué criterios se usan para evaluar?"
            ],
            'profiles': [
                "¿Cómo actualizo mi perfil?",
                "¿Cómo cambio mi foto?",
                "¿Dónde veo mis datos personales?",
                "¿Cómo corrijo información incorrecta?",
                "¿Cómo gestiono mis notificaciones?"
            ],
            'reports': [
                "¿Dónde descargo mis reportes?",
                "¿Cómo genero un reporte de asistencia?",
                "¿Cómo exporto mis calificaciones?",
                "¿Qué reportes puedo ver?",
                "¿Cómo interpretar los reportes?"
            ],
            'technical_issues': [
                "La aplicación no carga",
                "No veo mis datos",
                "Error al guardar información",
                "La página está en blanco",
                "¿Cómo reporto un problema?"
            ]
        }
        
        # Información crítica por rol de usuario
        self.critical_info_by_role = {
            'aprendices': {
                'must_know': [
                    'Cómo marcar asistencia',
                    'Cómo consultar horarios',
                    'Cómo iniciar sesión',
                    'Cómo cambiar contraseña',
                    'Cómo consultar calificaciones',
                    'Política de asistencia',
                    'Cómo justificar faltas'
                ],
                'nice_to_know': [
                    'Cómo evaluar instructores',
                    'Cómo actualizar perfil',
                    'Cómo descargar reportes',
                    'Cómo usar el chat de ayuda'
                ]
            },
            'instructores': {
                'must_know': [
                    'Cómo tomar asistencia de estudiantes',
                    'Cómo crear y gestionar horarios',
                    'Cómo evaluar estudiantes',
                    'Cómo generar reportes',
                    'Cómo gestionar ambientes',
                    'Cómo usar el sistema de evaluaciones'
                ],
                'nice_to_know': [
                    'Cómo configurar notificaciones',
                    'Cómo usar herramientas avanzadas',
                    'Cómo exportar datos',
                    'Cómo colaborar en comités'
                ]
            },
            'administrativos': {
                'must_know': [
                    'Cómo gestionar usuarios',
                    'Cómo supervisar asistencia',
                    'Cómo generar reportes institucionales',
                    'Cómo configurar el sistema',
                    'Cómo gestionar comités académicos',
                    'Cómo resolver incidencias'
                ],
                'nice_to_know': [
                    'Cómo optimizar configuraciones',
                    'Cómo usar analytics avanzados',
                    'Cómo hacer backup de datos',
                    'Cómo usar herramientas de monitoreo'
                ]
            }
        }
        
        # Patrones que indican información útil para soporte
        self.useful_patterns = {
            'step_by_step': [
                r'paso\s+\d+',
                r'primero.*segundo.*tercero',
                r'instrucciones\s+para',
                r'procedimiento:'
            ],
            'ui_guidance': [
                r'clic\s+en',
                r'botón\s+de',
                r'pantalla\s+de',
                r'menú\s+de',
                r'formulario\s+de',
                r'ir\s+a.*sección'
            ],
            'problem_solving': [
                r'si.*entonces',
                r'error.*solución',
                r'problema.*resolver',
                r'no\s+funciona.*hacer'
            ],
            'requirements': [
                r'debe.*tener',
                r'necesita.*para',
                r'requisito.*para',
                r'obligatorio.*para'
            ]
        }
    
    def analyze_support_value(self, knowledge_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizar el valor de cada elemento para soporte primario."""
        
        print("🔍 Analizando valor de contenido para soporte primario...")
        
        analyzed_items = []
        
        for item in knowledge_items:
            analysis = self._analyze_item_value(item)
            item.update(analysis)
            analyzed_items.append(item)
        
        # Categorizar por utilidad
        categorized = self._categorize_by_utility(analyzed_items)
        
        # Generar recomendaciones
        recommendations = self._generate_recommendations(categorized)
        
        return {
            'analyzed_items': analyzed_items,
            'categorized_content': categorized,
            'recommendations': recommendations,
            'summary': self._generate_summary(analyzed_items)
        }
    
    def _analyze_item_value(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar el valor individual de un elemento."""
        
        content = item.get('content', '').lower()
        title = item.get('title', '').lower()
        module = item.get('module', 'general')
        target_users = item.get('target_users', [])
        
        analysis = {
            'support_value_score': 0,
            'usefulness_indicators': [],
            'query_matches': [],
            'criticality_level': 'low',
            'actionability': 'low',
            'user_journey_stage': 'unknown'
        }
        
        # 1. Evaluar patrones útiles
        for pattern_type, patterns in self.useful_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content) or re.search(pattern, title):
                    analysis['support_value_score'] += 10
                    analysis['usefulness_indicators'].append(pattern_type)
        
        # 2. Evaluar coincidencias con consultas comunes
        for query_type, queries in self.common_user_queries.items():
            for query in queries:
                if self._text_similarity(content + ' ' + title, query.lower()) > 0.3:
                    analysis['support_value_score'] += 15
                    analysis['query_matches'].append(query_type)
        
        # 3. Evaluar criticidad por rol
        for user_type in target_users:
            if user_type in self.critical_info_by_role:
                critical_topics = self.critical_info_by_role[user_type]['must_know']
                for topic in critical_topics:
                    if self._text_similarity(content + ' ' + title, topic.lower()) > 0.4:
                        analysis['support_value_score'] += 20
                        analysis['criticality_level'] = 'high'
        
        # 4. Evaluar accionabilidad
        action_words = ['cómo', 'paso', 'instrucción', 'procedimiento', 'guía', 'tutorial']
        if any(word in content or word in title for word in action_words):
            analysis['actionability'] = 'high'
            analysis['support_value_score'] += 10
        
        # 5. Determinar etapa del viaje del usuario
        if any(word in content + title for word in ['login', 'sesión', 'contraseña', 'acceso']):
            analysis['user_journey_stage'] = 'onboarding'
            analysis['support_value_score'] += 15
        elif any(word in content + title for word in ['uso', 'gestión', 'administrar', 'crear']):
            analysis['user_journey_stage'] = 'active_use'
            analysis['support_value_score'] += 10
        elif any(word in content + title for word in ['problema', 'error', 'no funciona', 'ayuda']):
            analysis['user_journey_stage'] = 'troubleshooting'
            analysis['support_value_score'] += 25
        
        # Normalizar score
        analysis['support_value_score'] = min(100, analysis['support_value_score'])
        
        return analysis
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calcular similitud simple entre textos."""
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _categorize_by_utility(self, items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorizar elementos por su utilidad para soporte."""
        
        categorized = {
            'critical_support': [],      # Score >= 70
            'high_value': [],           # Score 50-69
            'moderate_value': [],       # Score 30-49
            'low_value': [],           # Score < 30
            'onboarding_essentials': [], # Información para nuevos usuarios
            'troubleshooting_guides': [], # Resolución de problemas
            'advanced_features': []      # Funcionalidades avanzadas
        }
        
        for item in items:
            score = item.get('support_value_score', 0)
            journey_stage = item.get('user_journey_stage', 'unknown')
            
            # Por score
            if score >= 70:
                categorized['critical_support'].append(item)
            elif score >= 50:
                categorized['high_value'].append(item)
            elif score >= 30:
                categorized['moderate_value'].append(item)
            else:
                categorized['low_value'].append(item)
            
            # Por etapa del viaje del usuario
            if journey_stage == 'onboarding':
                categorized['onboarding_essentials'].append(item)
            elif journey_stage == 'troubleshooting':
                categorized['troubleshooting_guides'].append(item)
            elif score >= 40:  # Solo características avanzadas con valor moderado-alto
                categorized['advanced_features'].append(item)
        
        return categorized
    
    def _generate_recommendations(self, categorized: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Generar recomendaciones para mejorar el soporte."""
        
        recommendations = []
        
        # Análisis de cobertura por módulo
        module_coverage = defaultdict(list)
        for category, items in categorized.items():
            for item in items:
                module_coverage[item.get('module', 'general')].append(category)
        
        # Recomendaciones por módulo con baja cobertura
        for module, categories in module_coverage.items():
            critical_count = len([c for c in categories if c == 'critical_support'])
            if critical_count < 2:
                recommendations.append({
                    'type': 'coverage_gap',
                    'module': module,
                    'message': f"El módulo {module} tiene baja cobertura de contenido crítico para soporte",
                    'suggestion': f"Agregar más guías paso a paso y FAQs para {module}",
                    'priority': 'high'
                })
        
        # Recomendaciones por rol de usuario
        user_role_coverage = defaultdict(int)
        for items in categorized.values():
            for item in items:
                for user in item.get('target_users', []):
                    user_role_coverage[user] += 1
        
        for role, count in user_role_coverage.items():
            if count < 5:
                recommendations.append({
                    'type': 'user_role_gap',
                    'role': role,
                    'message': f"Contenido insuficiente para {role}",
                    'suggestion': f"Crear más contenido específico para {role}",
                    'priority': 'medium'
                })
        
        # Recomendaciones de formato
        format_analysis = defaultdict(int)
        for items in categorized.values():
            for item in items:
                if 'step_by_step' in item.get('usefulness_indicators', []):
                    format_analysis['step_by_step'] += 1
                if 'ui_guidance' in item.get('usefulness_indicators', []):
                    format_analysis['ui_guidance'] += 1
        
        if format_analysis['step_by_step'] < 10:
            recommendations.append({
                'type': 'format_enhancement',
                'message': "Insuficientes guías paso a paso",
                'suggestion': "Convertir más contenido en tutoriales detallados con pasos numerados",
                'priority': 'high'
            })
        
        return recommendations
    
    def _generate_summary(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generar resumen del análisis."""
        
        total_items = len(items)
        high_value_items = len([i for i in items if i.get('support_value_score', 0) >= 50])
        
        # Distribución por score
        score_distribution = {
            'critical': len([i for i in items if i.get('support_value_score', 0) >= 70]),
            'high': len([i for i in items if 50 <= i.get('support_value_score', 0) < 70]),
            'moderate': len([i for i in items if 30 <= i.get('support_value_score', 0) < 50]),
            'low': len([i for i in items if i.get('support_value_score', 0) < 30])
        }
        
        # Top indicadores de utilidad
        all_indicators = []
        for item in items:
            all_indicators.extend(item.get('usefulness_indicators', []))
        
        top_indicators = Counter(all_indicators).most_common(5)
        
        # Consultas mejor cubiertas
        all_queries = []
        for item in items:
            all_queries.extend(item.get('query_matches', []))
        
        top_query_coverage = Counter(all_queries).most_common(5)
        
        return {
            'total_items': total_items,
            'high_value_percentage': round((high_value_items / total_items) * 100, 2) if total_items > 0 else 0,
            'score_distribution': score_distribution,
            'top_usefulness_indicators': top_indicators,
            'best_covered_query_types': top_query_coverage,
            'readiness_score': self._calculate_readiness_score(score_distribution, total_items)
        }
    
    def _calculate_readiness_score(self, distribution: Dict[str, int], total: int) -> float:
        """Calcular score de preparación para soporte primario."""
        
        if total == 0:
            return 0.0
        
        # Peso por categoría
        weights = {'critical': 4, 'high': 3, 'moderate': 2, 'low': 1}
        
        weighted_sum = sum(distribution[category] * weight for category, weight in weights.items())
        max_possible = total * 4  # Si todo fuera crítico
        
        return round((weighted_sum / max_possible) * 100, 2)
    
    def extract_most_useful_info(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extraer la información más útil identificada."""
        
        categorized = analysis_result['categorized_content']
        
        # Elementos más críticos para soporte primario
        critical_items = categorized['critical_support']
        onboarding_items = categorized['onboarding_essentials']
        troubleshooting_items = categorized['troubleshooting_guides']
        
        # Crear estructura optimizada para KBService
        optimized_content = {
            'priority_1_critical': self._format_for_kb(critical_items),
            'priority_2_onboarding': self._format_for_kb(onboarding_items),
            'priority_3_troubleshooting': self._format_for_kb(troubleshooting_items),
            'priority_4_general': self._format_for_kb(categorized['high_value'][:10])  # Top 10
        }
        
        # Generar FAQs automáticas
        auto_faqs = self._generate_auto_faqs(critical_items + onboarding_items)
        
        return {
            'optimized_content': optimized_content,
            'auto_generated_faqs': auto_faqs,
            'implementation_guide': self._create_implementation_guide(optimized_content)
        }
    
    def _format_for_kb(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formatear elementos para integración con KBService."""
        
        formatted = []
        
        for item in items:
            formatted_item = {
                'id': item.get('id', ''),
                'title': item['title'],
                'content': item['content'][:800] + '...' if len(item['content']) > 800 else item['content'],
                'category': item.get('module', 'general'),
                'tags': item.get('tags', []),
                'target_audience': item.get('target_users', ['general']),
                'support_score': item.get('support_value_score', 0),
                'content_type': item.get('support_type', 'guide'),
                'actionable': item.get('actionability', 'low') == 'high',
                'user_journey_stage': item.get('user_journey_stage', 'unknown')
            }
            formatted.append(formatted_item)
        
        # Ordenar por score de soporte
        formatted.sort(key=lambda x: x['support_score'], reverse=True)
        
        return formatted
    
    def _generate_auto_faqs(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generar FAQs automáticas basadas en el contenido."""
        
        faqs = []
        
        # Mapear patrones comunes a preguntas
        common_questions = {
            'login': "¿Cómo ingreso al sistema SICORA?",
            'asistencia': "¿Cómo marco mi asistencia?",
            'horario': "¿Dónde puedo ver mi horario?",
            'contraseña': "¿Cómo cambio mi contraseña?",
            'evaluación': "¿Cómo funciona el sistema de evaluaciones?",
            'ambiente': "¿Cómo reservo un ambiente de formación?",
            'reporte': "¿Cómo genero reportes en el sistema?"
        }
        
        for item in items:
            content = item.get('content', '').lower()
            title = item.get('title', '').lower()
            
            for keyword, question in common_questions.items():
                if keyword in content or keyword in title:
                    # Extraer respuesta del contenido
                    answer = self._extract_answer_from_content(item['content'], keyword)
                    if answer:
                        faqs.append({
                            'question': question,
                            'answer': answer,
                            'category': item.get('module', 'general'),
                            'target_users': item.get('target_users', ['general']),
                            'source_item_id': item.get('id', ''),
                            'auto_generated': True
                        })
        
        return faqs[:20]  # Limitar a 20 FAQs principales
    
    def _extract_answer_from_content(self, content: str, keyword: str) -> str:
        """Extraer una respuesta concisa del contenido."""
        
        sentences = content.split('.')
        relevant_sentences = [s.strip() for s in sentences if keyword in s.lower()]
        
        if relevant_sentences:
            # Tomar las primeras 2 oraciones más relevantes
            answer = '. '.join(relevant_sentences[:2])
            return answer[:300] + '...' if len(answer) > 300 else answer
        
        return ""
    
    def _create_implementation_guide(self, optimized_content: Dict[str, Any]) -> Dict[str, Any]:
        """Crear guía de implementación para KBService."""
        
        return {
            'database_structure': {
                'tables_needed': [
                    'kb_articles (contenido principal)',
                    'kb_faqs (preguntas frecuentes)',
                    'kb_categories (categorías)',
                    'kb_tags (etiquetas)',
                    'kb_user_feedback (retroalimentación)',
                    'kb_search_analytics (métricas de búsqueda)'
                ],
                'indexes_recommended': [
                    'Índice full-text en content',
                    'Índice en category y tags',
                    'Índice en target_audience',
                    'Índice en support_score'
                ]
            },
            'api_endpoints': {
                'search': '/api/kb/search?q={query}&category={category}&audience={audience}',
                'browse': '/api/kb/browse/{category}',
                'article': '/api/kb/article/{id}',
                'faqs': '/api/kb/faqs?category={category}',
                'feedback': '/api/kb/feedback/{article_id}'
            },
            'integration_steps': [
                '1. Importar contenido prioritario a la base de datos',
                '2. Configurar búsqueda semántica con vectores',
                '3. Implementar sistema de feedback de usuarios',
                '4. Crear dashboard de analytics para administradores',
                '5. Integrar con AIService para respuestas automáticas',
                '6. Configurar sistema de notificaciones para nuevo contenido'
            ],
            'metrics_to_track': [
                'Consultas más frecuentes',
                'Contenido más útil (por feedback)',
                'Tiempo de resolución de consultas',
                'Cobertura de consultas por módulo',
                'Satisfacción de usuarios por respuesta'
            ]
        }


def main():
    """Función principal."""
    
    print("🎯 Analizador de Información Útil para Soporte Primario")
    print("=" * 60)
    
    # Cargar datos extraídos
    try:
        with open('enhanced_support_knowledge.json', 'r', encoding='utf-8') as f:
            knowledge_items = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró enhanced_support_knowledge.json")
        print("Ejecuta primero enhanced_support_extractor.py")
        return
    
    # Crear analizador
    analyzer = SupportContentAnalyzer()
    
    # Analizar contenido
    analysis_result = analyzer.analyze_support_value(knowledge_items)
    
    # Extraer información más útil
    useful_info = analyzer.extract_most_useful_info(analysis_result)
    
    # Guardar resultados
    with open('support_value_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    with open('most_useful_support_info.json', 'w', encoding='utf-8') as f:
        json.dump(useful_info, f, ensure_ascii=False, indent=2)
    
    # Mostrar estadísticas
    summary = analysis_result['summary']
    categorized = analysis_result['categorized_content']
    
    print(f"\n📊 ANÁLISIS DE VALOR PARA SOPORTE PRIMARIO")
    print(f"Total de elementos analizados: {summary['total_items']}")
    print(f"Contenido de alto valor: {summary['high_value_percentage']}%")
    print(f"Score de preparación: {summary['readiness_score']}%")
    
    print(f"\n🎯 DISTRIBUCIÓN POR VALOR DE SOPORTE:")
    for category, count in summary['score_distribution'].items():
        percentage = (count / summary['total_items']) * 100 if summary['total_items'] > 0 else 0
        print(f"  {category.capitalize()}: {count} elementos ({percentage:.1f}%)")
    
    print(f"\n🏆 CONTENIDO MÁS CRÍTICO PARA SOPORTE:")
    critical_items = categorized['critical_support'][:5]
    for i, item in enumerate(critical_items, 1):
        print(f"  {i}. {item['title'][:60]}... (Score: {item.get('support_value_score', 0)})")
    
    print(f"\n🚀 ELEMENTOS DE ONBOARDING:")
    onboarding_items = categorized['onboarding_essentials'][:3]
    for i, item in enumerate(onboarding_items, 1):
        print(f"  {i}. {item['title'][:60]}...")
    
    print(f"\n🔧 GUÍAS DE RESOLUCIÓN DE PROBLEMAS:")
    troubleshooting_items = categorized['troubleshooting_guides'][:3]
    for i, item in enumerate(troubleshooting_items, 1):
        print(f"  {i}. {item['title'][:60]}...")
    
    print(f"\n💡 RECOMENDACIONES:")
    recommendations = analysis_result['recommendations'][:3]
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['message']}")
        print(f"     Sugerencia: {rec['suggestion']}")
    
    print(f"\n❓ FAQs GENERADAS AUTOMÁTICAMENTE:")
    auto_faqs = useful_info['auto_generated_faqs'][:5]
    for i, faq in enumerate(auto_faqs, 1):
        print(f"  {i}. {faq['question']}")
    
    print(f"\n💾 Archivos generados:")
    print(f"  📊 Análisis completo: support_value_analysis.json")
    print(f"  🎯 Información más útil: most_useful_support_info.json")
    
    print(f"\n✅ Análisis completado!")
    print(f"\n📋 PRÓXIMOS PASOS:")
    print("1. Revisar el contenido crítico identificado")
    print("2. Implementar las FAQs generadas automáticamente")
    print("3. Priorizar la integración del contenido de alto valor")
    print("4. Configurar métricas de seguimiento sugeridas")


if __name__ == "__main__":
    main()
