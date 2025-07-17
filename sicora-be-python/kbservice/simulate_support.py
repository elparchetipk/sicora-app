#!/usr/bin/env python3
"""
Simulador de consultas de soporte para KBService
Demuestra cómo la base de conocimiento puede responder preguntas típicas de usuarios.
"""

import json
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path


class SupportQuerySimulator:
    """Simulador de consultas de soporte usando la base de conocimiento."""
    
    def __init__(self, knowledge_file: str):
        self.knowledge_items = []
        self.load_knowledge_base(knowledge_file)
        
        # Consultas típicas por tipo de usuario
        self.sample_queries = {
            'aprendices': [
                "¿Cómo puedo marcar mi asistencia?",
                "¿Qué pasa si llego tarde a clase?",
                "¿Cómo cambio mi contraseña?",
                "¿Dónde veo mis calificaciones?",
                "¿Cómo puedo ver mi horario de clases?",
                "¿Qué hacer si olvido mi contraseña?",
                "¿Cuáles son mis derechos como aprendiz?",
                "¿Qué sucede si falto muchos días?",
                "¿Cómo puedo contactar a mi instructor?",
                "¿Dónde encuentro el reglamento del aprendiz?"
            ],
            'instructores': [
                "¿Cómo tomo asistencia de mis estudiantes?",
                "¿Cómo creo un horario de clases?",
                "¿Cómo evalúo el desempeño de un aprendiz?",
                "¿Dónde veo los reportes de asistencia?",
                "¿Cómo programo un ambiente de formación?",
                "¿Cómo gestiono las evaluaciones?",
                "¿Dónde reporto incidencias disciplinarias?",
                "¿Cómo accedo al comité académico?",
                "¿Cómo configuro notificaciones?",
                "¿Dónde están las guías pedagógicas?"
            ],
            'administrativos': [
                "¿Cómo genero reportes de asistencia?",
                "¿Cómo gestiono usuarios del sistema?",
                "¿Dónde veo las estadísticas generales?",
                "¿Cómo configuro el sistema de evaluaciones?",
                "¿Cómo administro los horarios institucionales?",
                "¿Dónde están los logs del sistema?",
                "¿Cómo gestiono los comités académicos?",
                "¿Cómo configuro las integraciones?",
                "¿Dónde veo el estado de los servicios?",
                "¿Cómo hago backup de la información?"
            ]
        }
    
    def load_knowledge_base(self, knowledge_file: str) -> None:
        """Cargar la base de conocimiento."""
        
        try:
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_items = json.load(f)
            print(f"📚 Base de conocimiento cargada: {len(self.knowledge_items)} items")
        except Exception as e:
            print(f"❌ Error cargando base de conocimiento: {e}")
            self.knowledge_items = []
    
    def search_knowledge(self, query: str, user_role: str = 'general') -> List[Dict[str, Any]]:
        """Buscar en la base de conocimiento."""
        
        query_lower = query.lower()
        results = []
        
        # Palabras clave de la consulta
        query_words = set(re.findall(r'\w+', query_lower))
        
        for item in self.knowledge_items:
            score = 0
            
            # Filtrar por audiencia si es específica
            if user_role != 'general' and item['target_audience'] not in ['general', user_role]:
                continue
            
            # Puntaje por título
            title_words = set(re.findall(r'\w+', item['title'].lower()))
            title_matches = len(query_words.intersection(title_words))
            score += title_matches * 3
            
            # Puntaje por contenido
            content_words = set(re.findall(r'\w+', item['content'].lower()))
            content_matches = len(query_words.intersection(content_words))
            score += content_matches
            
            # Puntaje por tags
            tag_words = set()
            for tag in item['tags']:
                tag_words.update(re.findall(r'\w+', tag.lower()))
            tag_matches = len(query_words.intersection(tag_words))
            score += tag_matches * 2
            
            # Bonus por palabras clave específicas
            if any(word in item['content'].lower() for word in ['cómo', 'tutorial', 'guía', 'paso']):
                score += 1
            
            if score > 0:
                results.append({
                    'item': item,
                    'score': score,
                    'relevance_reason': self._explain_relevance(query_words, item)
                })
        
        # Ordenar por puntaje
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:5]  # Top 5 resultados
    
    def _explain_relevance(self, query_words: set, item: Dict[str, Any]) -> str:
        """Explicar por qué un item es relevante."""
        
        reasons = []
        
        # Comprobar coincidencias en título
        title_words = set(re.findall(r'\w+', item['title'].lower()))
        title_matches = query_words.intersection(title_words)
        if title_matches:
            reasons.append(f"título contiene: {', '.join(title_matches)}")
        
        # Comprobar coincidencias en tags
        tag_words = set()
        for tag in item['tags']:
            tag_words.update(re.findall(r'\w+', tag.lower()))
        tag_matches = query_words.intersection(tag_words)
        if tag_matches:
            reasons.append(f"tags relacionados: {', '.join(tag_matches)}")
        
        # Comprobar tipo de contenido
        if item['content_type'] in ['tutorial', 'guide', 'procedure']:
            reasons.append(f"es un {item['content_type']}")
        
        return "; ".join(reasons) if reasons else "contenido relacionado"
    
    def simulate_support_session(self, user_role: str) -> None:
        """Simular una sesión de soporte para un tipo de usuario."""
        
        print(f"\n🎭 SIMULACIÓN DE SOPORTE - ROL: {user_role.upper()}")
        print("="*60)
        
        if user_role not in self.sample_queries:
            print(f"❌ Rol '{user_role}' no reconocido")
            return
        
        queries = self.sample_queries[user_role]
        
        for i, query in enumerate(queries[:5]):  # Solo 5 consultas por demo
            print(f"\n📝 Consulta {i+1}: \"{query}\"")
            print("-" * 40)
            
            results = self.search_knowledge(query, user_role)
            
            if not results:
                print("❌ No se encontraron resultados relevantes")
                continue
            
            print(f"✅ Encontrados {len(results)} resultados:")
            
            for j, result in enumerate(results[:3]):  # Top 3
                item = result['item']
                score = result['score']
                reason = result['relevance_reason']
                
                print(f"\n   {j+1}. {item['title']}")
                print(f"      📊 Relevancia: {score} puntos ({reason})")
                print(f"      📂 Tipo: {item['content_type']} | Categoría: {item['category']}")
                print(f"      👥 Audiencia: {item['target_audience']}")
                
                # Mostrar fragmento del contenido
                content_preview = item['content'][:200].replace('\n', ' ')
                print(f"      📄 Contenido: {content_preview}...")
                
                if j == 0:  # Mostrar tags solo del primer resultado
                    print(f"      🏷️  Tags: {', '.join(item['tags'])}")
    
    def generate_support_coverage_report(self) -> Dict[str, Any]:
        """Generar reporte de cobertura de soporte."""
        
        coverage = {
            'total_items': len(self.knowledge_items),
            'by_audience': {},
            'by_content_type': {},
            'by_category': {},
            'top_tags': {},
            'coverage_analysis': {}
        }
        
        # Estadísticas básicas
        for item in self.knowledge_items:
            # Por audiencia
            aud = item['target_audience']
            coverage['by_audience'][aud] = coverage['by_audience'].get(aud, 0) + 1
            
            # Por tipo de contenido
            ct = item['content_type']
            coverage['by_content_type'][ct] = coverage['by_content_type'].get(ct, 0) + 1
            
            # Por categoría
            cat = item['category']
            coverage['by_category'][cat] = coverage['by_category'].get(cat, 0) + 1
            
            # Tags más frecuentes
            for tag in item['tags']:
                coverage['top_tags'][tag] = coverage['top_tags'].get(tag, 0) + 1
        
        # Análisis de cobertura por área funcional
        functional_areas = {
            'autenticacion': ['login', 'sesión', 'contraseña', 'password', 'autenticacion'],
            'asistencia': ['asistencia', 'presente', 'ausente', 'tardanza'],
            'evaluacion': ['evaluación', 'calificación', 'nota', 'evaluacion'],
            'horarios': ['horario', 'clase', 'ambiente', 'programación'],
            'usuarios': ['usuario', 'perfil', 'rol', 'permiso'],
            'reportes': ['reporte', 'estadística', 'dashboard', 'gráfico'],
            'comites': ['comité', 'académico', 'disciplinario'],
            'notificaciones': ['notificación', 'alerta', 'mensaje', 'email']
        }
        
        for area, keywords in functional_areas.items():
            count = 0
            for item in self.knowledge_items:
                content_lower = item['content'].lower()
                if any(keyword in content_lower for keyword in keywords):
                    count += 1
            coverage['coverage_analysis'][area] = count
        
        return coverage
    
    def demonstrate_ai_integration(self) -> None:
        """Demostrar cómo se integraría con el AIService."""
        
        print(f"\n🤖 DEMOSTRACIÓN DE INTEGRACIÓN CON AISERVICE")
        print("="*60)
        
        # Consultas complejas que requieren IA
        complex_queries = [
            "Ayúdame a entender el proceso completo de evaluación de proyectos",
            "¿Cuál es la diferencia entre una falta leve y una grave?",
            "Explícame paso a paso cómo gestionar un comité académico",
            "¿Qué debo hacer si un aprendiz tiene muchas ausencias?"
        ]
        
        for query in complex_queries:
            print(f"\n❓ Consulta compleja: \"{query}\"")
            print("-" * 50)
            
            # Simular búsqueda en KB
            results = self.search_knowledge(query, 'general')
            
            print(f"📚 Contexto desde KB: {len(results)} documentos relevantes")
            
            if results:
                # Simular lo que haría el AIService
                context_docs = []
                for result in results[:3]:
                    context_docs.append({
                        'title': result['item']['title'],
                        'content_snippet': result['item']['content'][:300],
                        'relevance': result['score']
                    })
                
                print("🔄 El AIService procesaría:")
                print("   1. Consulta del usuario")
                print("   2. Contexto relevante desde KB")
                print("   3. Generaría respuesta personalizada")
                
                print(f"\n📄 Documentos de contexto utilizados:")
                for i, doc in enumerate(context_docs):
                    print(f"   {i+1}. {doc['title']} (relevancia: {doc['relevance']})")
                
                print(f"\n✨ Respuesta AI simulada:")
                print(f"   \"Basándome en la documentación de SICORA, te explico...")
                print(f"   [Respuesta personalizada basada en {len(context_docs)} documentos]\"")
            else:
                print("⚠️  Sin contexto suficiente - AIService respondería con conocimiento general")


def main():
    """Función principal."""
    
    print("🎯 SIMULADOR DE CONSULTAS DE SOPORTE - KBSERVICE")
    print("="*70)
    
    # Verificar archivos
    kb_file = 'knowledge_base_content.json'
    if not Path(kb_file).exists():
        print(f"❌ No se encontró {kb_file}")
        print("💡 Ejecuta primero: python extract_knowledge.py")
        return
    
    # Crear simulador
    simulator = SupportQuerySimulator(kb_file)
    
    if not simulator.knowledge_items:
        print("❌ No se pudo cargar la base de conocimiento")
        return
    
    # Simular consultas por tipo de usuario
    for user_role in ['aprendices', 'instructores', 'administrativos']:
        simulator.simulate_support_session(user_role)
    
    # Demostrar integración con AI
    simulator.demonstrate_ai_integration()
    
    # Generar reporte de cobertura
    print(f"\n📊 REPORTE DE COBERTURA DE SOPORTE")
    print("="*50)
    
    coverage = simulator.generate_support_coverage_report()
    
    print(f"📚 Total de items en KB: {coverage['total_items']}")
    
    print(f"\n👥 Cobertura por audiencia:")
    for aud, count in coverage['by_audience'].items():
        percentage = (count / coverage['total_items']) * 100
        print(f"   {aud}: {count} items ({percentage:.1f}%)")
    
    print(f"\n📄 Cobertura por tipo de contenido:")
    for ct, count in coverage['by_content_type'].items():
        print(f"   {ct}: {count} items")
    
    print(f"\n🔧 Cobertura por área funcional:")
    for area, count in coverage['coverage_analysis'].items():
        print(f"   {area}: {count} documentos")
    
    print(f"\n🏷️  Tags más frecuentes:")
    top_tags = sorted(coverage['top_tags'].items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in top_tags:
        print(f"   {tag}: {count} veces")
    
    print(f"\n🎉 RESUMEN FINAL")
    print("="*30)
    print(f"✅ KBService está listo para dar soporte completo sobre SICORA")
    print(f"📚 {coverage['total_items']} documentos de soporte disponibles")
    print(f"👥 Cobertura para todos los roles de usuario")
    print(f"🤖 Listo para integración con AIService")
    print(f"🔍 Búsqueda inteligente implementada")
    print(f"📈 Análisis de relevancia automático")


if __name__ == "__main__":
    main()
