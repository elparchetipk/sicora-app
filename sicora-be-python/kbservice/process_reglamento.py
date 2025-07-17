#!/usr/bin/env python3
"""
Script especializado para procesar el Reglamento del Aprendiz SENA.
Segmenta el documento por capítulos y crea items estructurados en la KB.
"""

import asyncio
import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import argparse
import logging

# Agregar el directorio de la aplicación al path
sys.path.insert(0, str(Path(__file__).parent))

from app.infrastructure.pdf_processing import PDFProcessor
from app.domain.entities.kb_entities import ContentType, TargetAudience
from app.application.dtos.kb_dtos import KnowledgeItemCreateDTO

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReglamentoProcessor:
    """Procesador especializado para el Reglamento del Aprendiz."""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor(use_ocr=False)
        
        # Patrones para identificar secciones del reglamento
        self.chapter_patterns = [
            r'CAPÍTULO\s+([IVX]+|[0-9]+)[\.\s]*([^\n]+)',
            r'TÍTULO\s+([IVX]+|[0-9]+)[\.\s]*([^\n]+)',
            r'ARTÍCULO\s+([0-9]+)[\.\s]*([^\n]+)',
            r'SECCIÓN\s+([IVX]+|[0-9]+)[\.\s]*([^\n]+)'
        ]
        
        # Categorías por tipo de contenido del reglamento
        self.content_categories = {
            'derechos': ['derecho', 'derechos del aprendiz'],
            'deberes': ['deber', 'deberes', 'obligaciones'],
            'prohibiciones': ['prohibición', 'prohibiciones', 'prohibido'],
            'sanciones': ['sanción', 'sanciones', 'falta', 'faltas'],
            'procedimientos': ['procedimiento', 'proceso', 'trámite'],
            'normatividad': ['norma', 'normativa', 'reglamento']
        }
    
    def extract_and_segment_reglamento(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extrae y segmenta el reglamento en secciones lógicas.
        
        Returns:
            List[Dict]: Lista de secciones con metadata
        """
        try:
            # Extraer texto del PDF
            text, method_used = self.pdf_processor.extract_text(pdf_path)
            cleaned_text = self.pdf_processor.clean_text(text)
            
            logger.info(f"Texto extraído usando: {method_used}")
            logger.info(f"Longitud del texto: {len(cleaned_text)} caracteres")
            
            # Segmentar por secciones
            sections = self._segment_by_structure(cleaned_text)
            
            # Procesar cada sección
            processed_sections = []
            for i, section in enumerate(sections):
                processed_section = self._process_section(
                    section, i + 1, len(sections)
                )
                processed_sections.append(processed_section)
            
            return processed_sections
            
        except Exception as e:
            logger.error(f"Error procesando reglamento: {e}")
            raise
    
    def _segment_by_structure(self, text: str) -> List[Dict[str, str]]:
        """Segmenta el texto por estructura jerárquica del reglamento."""
        sections = []
        
        # Buscar todas las secciones usando patrones
        all_matches = []
        for pattern in self.chapter_patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
            for match in matches:
                all_matches.append({
                    'start': match.start(),
                    'end': match.end(),
                    'type': pattern.split('\\')[0],
                    'title': match.group().strip(),
                    'number': match.group(1) if match.groups() else '',
                    'name': match.group(2) if len(match.groups()) > 1 else ''
                })
        
        # Ordenar por posición en el texto
        all_matches.sort(key=lambda x: x['start'])
        
        # Crear secciones con contenido
        for i, match in enumerate(all_matches):
            start_pos = match['start']
            end_pos = all_matches[i + 1]['start'] if i + 1 < len(all_matches) else len(text)
            
            content = text[start_pos:end_pos].strip()
            
            sections.append({
                'title': match['title'],
                'type': match['type'],
                'number': match['number'],
                'name': match['name'],
                'content': content,
                'start_pos': start_pos,
                'end_pos': end_pos
            })
        
        # Si no se encontraron secciones estructuradas, segmentar por párrafos
        if not sections:
            sections = self._segment_by_paragraphs(text)
        
        return sections
    
    def _segment_by_paragraphs(self, text: str) -> List[Dict[str, str]]:
        """Segmenta por párrafos si no hay estructura clara."""
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 100]
        
        sections = []
        for i, paragraph in enumerate(paragraphs):
            # Intentar extraer título del primer renglón
            lines = paragraph.split('\n')
            title = lines[0] if lines else f"Sección {i + 1}"
            
            sections.append({
                'title': title[:100] + "..." if len(title) > 100 else title,
                'type': 'paragraph',
                'number': str(i + 1),
                'name': '',
                'content': paragraph,
                'start_pos': 0,
                'end_pos': len(paragraph)
            })
        
        return sections
    
    def _process_section(self, section: Dict[str, str], index: int, total: int) -> Dict[str, Any]:
        """Procesa una sección individual."""
        content = section['content']
        title = section['title']
        
        # Auto-categorizar según contenido
        category = self._auto_categorize_content(content)
        
        # Determinar audiencia objetivo
        target_audience = self._determine_target_audience(content)
        
        # Extraer tags relevantes
        tags = self._extract_tags(content)
        
        # Crear metadata enriquecida
        metadata = {
            'source_document': 'Reglamento del Aprendiz SENA',
            'section_type': section['type'],
            'section_number': section['number'],
            'section_name': section['name'],
            'processing_index': index,
            'total_sections': total,
            'word_count': len(content.split()),
            'char_count': len(content),
            'auto_category': category,
            'extracted_tags': tags
        }
        
        return {
            'title': title,
            'content': content,
            'content_type': ContentType.POLICY.value,
            'category': category,
            'target_audience': target_audience,
            'tags': tags,
            'metadata': metadata,
            'status': 'draft'  # Se puede cambiar a published después de revisión
        }
    
    def _auto_categorize_content(self, content: str) -> str:
        """Auto-categoriza el contenido basado en palabras clave."""
        content_lower = content.lower()
        
        # Calcular scores por categoría
        category_scores = {}
        for category, keywords in self.content_categories.items():
            score = 0
            for keyword in keywords:
                score += content_lower.count(keyword)
            if score > 0:
                category_scores[category] = score
        
        # Retornar la categoría con mayor score
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return 'normatividad'  # Default
    
    def _determine_target_audience(self, content: str) -> str:
        """Determina la audiencia objetivo basada en el contenido."""
        content_lower = content.lower()
        
        # Palabras clave por audiencia
        audience_keywords = {
            'aprendices': ['aprendiz', 'aprendices', 'estudiante', 'formación'],
            'instructores': ['instructor', 'docente', 'formador'],
            'administrativos': ['coordinador', 'administrativo', 'director']
        }
        
        for audience, keywords in audience_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return audience
        
        return TargetAudience.ALL.value  # Default
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extrae tags relevantes del contenido."""
        tags = []
        
        # Tags comunes del reglamento
        common_tags = {
            'derechos': ['derechos', 'garantías'],
            'deberes': ['deberes', 'obligaciones', 'responsabilidades'],
            'faltas': ['falta', 'sanción', 'disciplinario'],
            'proceso': ['procedimiento', 'trámite', 'proceso'],
            'formacion': ['formación', 'académico', 'aprendizaje'],
            'convivencia': ['convivencia', 'comportamiento', 'conducta'],
            'evaluacion': ['evaluación', 'seguimiento', 'valoración']
        }
        
        content_lower = content.lower()
        for tag, keywords in common_tags.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag)
        
        return tags[:5]  # Limitar a 5 tags máximo


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description='Procesar Reglamento del Aprendiz SENA'
    )
    parser.add_argument(
        'pdf_path', 
        help='Ruta al archivo PDF del reglamento'
    )
    parser.add_argument(
        '--output', '-o',
        default='reglamento_sections.json',
        help='Archivo de salida (JSON)'
    )
    parser.add_argument(
        '--create-kb-items',
        action='store_true',
        help='Crear items en la base de conocimiento'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Solo mostrar lo que se haría sin ejecutar'
    )
    
    args = parser.parse_args()
    
    # Validar que el archivo existe
    if not os.path.exists(args.pdf_path):
        logger.error(f"Archivo no encontrado: {args.pdf_path}")
        sys.exit(1)
    
    # Procesar reglamento
    processor = ReglamentoProcessor()
    
    try:
        logger.info(f"Procesando: {args.pdf_path}")
        sections = processor.extract_and_segment_reglamento(args.pdf_path)
        
        logger.info(f"Se extrajeron {len(sections)} secciones")
        
        # Mostrar resumen
        for i, section in enumerate(sections):
            print(f"\nSección {i + 1}: {section['title'][:60]}...")
            print(f"  Tipo: {section['metadata']['section_type']}")
            print(f"  Categoría: {section['category']}")
            print(f"  Audiencia: {section['target_audience']}")
            print(f"  Tags: {', '.join(section['tags'])}")
            print(f"  Palabras: {section['metadata']['word_count']}")
        
        # Guardar resultado
        import json
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(sections, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Resultado guardado en: {args.output}")
        
        if args.create_kb_items and not args.dry_run:
            logger.info("Creando items en la base de conocimiento...")
            # TODO: Implementar creación real en KB
            logger.info("Función de creación en KB pendiente de implementar")
        
    except Exception as e:
        logger.error(f"Error procesando reglamento: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
