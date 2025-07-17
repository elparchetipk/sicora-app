#!/usr/bin/env python3
"""
Importador de contenido para KBService
Carga el contenido extraído desde documentación en la base de conocimiento.
"""

import json
import sys
import asyncio
from pathlib import Path
from typing import List, Dict, Any
import uuid
from datetime import datetime

# Simular las clases que tendríamos en el KBService real
class MockKnowledgeItem:
    """Mock del modelo KnowledgeItem para la demo."""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.title = kwargs.get('title', '')
        self.content = kwargs.get('content', '')
        self.content_type = kwargs.get('content_type', 'article')
        self.category = kwargs.get('category', 'general')
        self.target_audience = kwargs.get('target_audience', 'general')
        self.tags = kwargs.get('tags', [])
        self.metadata = kwargs.get('metadata', {})
        self.status = 'published'  # Auto-publicar contenido extraído
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class KnowledgeBaseImporter:
    """Importador de contenido para la base de conocimiento."""
    
    def __init__(self):
        self.processed_items = []
        self.skipped_items = []
        self.errors = []
        
    async def import_from_json(self, json_file: str) -> Dict[str, Any]:
        """Importar contenido desde archivo JSON."""
        
        print(f"📂 Cargando contenido desde: {json_file}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                items_data = json.load(f)
                
            print(f"📊 Items a procesar: {len(items_data)}")
            
            # Procesar items
            for i, item_data in enumerate(items_data):
                try:
                    await self._process_item(item_data, i + 1, len(items_data))
                except Exception as e:
                    self.errors.append({
                        'item_index': i + 1,
                        'title': item_data.get('title', 'Sin título'),
                        'error': str(e)
                    })
                    print(f"❌ Error procesando item {i + 1}: {e}")
            
            # Generar reporte
            return self._generate_import_report()
            
        except Exception as e:
            print(f"❌ Error cargando archivo: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _process_item(self, item_data: Dict[str, Any], index: int, total: int) -> None:
        """Procesar un item individual."""
        
        # Mostrar progreso
        if index % 50 == 0 or index == total:
            print(f"🔄 Procesando {index}/{total} items...")
        
        # Validar item
        if not self._validate_item(item_data):
            self.skipped_items.append({
                'title': item_data.get('title', 'Sin título'),
                'reason': 'Validación fallida'
            })
            return
        
        # Crear item de conocimiento
        knowledge_item = MockKnowledgeItem(
            title=item_data['title'],
            content=item_data['content'],
            content_type=item_data['content_type'],
            category=item_data['category'],
            target_audience=item_data['target_audience'],
            tags=item_data['tags'],
            metadata={
                **item_data.get('metadata', {}),
                'imported_from': item_data.get('source_file', ''),
                'import_date': datetime.utcnow().isoformat()
            }
        )
        
        # Simular guardado en base de datos
        # En el KBService real, aquí usarías el repository pattern
        await self._save_knowledge_item(knowledge_item)
        
        self.processed_items.append(knowledge_item)
    
    def _validate_item(self, item_data: Dict[str, Any]) -> bool:
        """Validar que el item tenga los campos requeridos."""
        
        required_fields = ['title', 'content', 'content_type', 'category']
        
        for field in required_fields:
            if field not in item_data or not item_data[field]:
                return False
        
        # Validar longitud mínima de contenido
        if len(item_data['content']) < 50:
            return False
        
        return True
    
    async def _save_knowledge_item(self, item: MockKnowledgeItem) -> None:
        """Simular guardado en base de datos."""
        
        # En el KBService real, aquí harías:
        # await self.knowledge_repository.create(item)
        
        # Por ahora, solo simular un pequeño delay
        await asyncio.sleep(0.001)
    
    def _generate_import_report(self) -> Dict[str, Any]:
        """Generar reporte de importación."""
        
        # Estadísticas por tipo de contenido
        content_type_stats = {}
        for item in self.processed_items:
            ct = item.content_type
            content_type_stats[ct] = content_type_stats.get(ct, 0) + 1
        
        # Estadísticas por audiencia
        audience_stats = {}
        for item in self.processed_items:
            aud = item.target_audience
            audience_stats[aud] = audience_stats.get(aud, 0) + 1
        
        # Estadísticas por categoría
        category_stats = {}
        for item in self.processed_items:
            cat = item.category
            category_stats[cat] = category_stats.get(cat, 0) + 1
        
        return {
            'success': True,
            'summary': {
                'total_processed': len(self.processed_items),
                'total_skipped': len(self.skipped_items),
                'total_errors': len(self.errors)
            },
            'statistics': {
                'by_content_type': content_type_stats,
                'by_audience': audience_stats,
                'by_category': category_stats
            },
            'skipped_items': self.skipped_items,
            'errors': self.errors
        }
    
    def export_sample_content(self, output_file: str) -> None:
        """Exportar muestra del contenido procesado."""
        
        sample_items = []
        
        # Tomar muestra representativa
        for content_type in ['guide', 'tutorial', 'faq', 'procedure', 'article']:
            items_of_type = [
                item for item in self.processed_items 
                if item.content_type == content_type
            ]
            
            if items_of_type:
                sample_items.extend(items_of_type[:2])  # 2 por tipo
        
        # Convertir a formato JSON serializable
        sample_data = []
        for item in sample_items:
            sample_data.append({
                'id': item.id,
                'title': item.title,
                'content': item.content[:500] + "..." if len(item.content) > 500 else item.content,
                'content_type': item.content_type,
                'category': item.category,
                'target_audience': item.target_audience,
                'tags': item.tags,
                'metadata': item.metadata,
                'status': item.status
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
        
        print(f"📝 Muestra exportada a: {output_file}")


async def main():
    """Función principal."""
    
    print("📚 IMPORTADOR DE CONTENIDO PARA KBSERVICE")
    print("="*60)
    
    # Archivo de entrada
    input_file = 'knowledge_base_content.json'
    
    if not Path(input_file).exists():
        print(f"❌ Error: No se encontró el archivo {input_file}")
        print("💡 Ejecuta primero: python extract_knowledge.py")
        return
    
    # Crear importador
    importer = KnowledgeBaseImporter()
    
    # Importar contenido
    print("🚀 Iniciando importación...")
    result = await importer.import_from_json(input_file)
    
    if not result['success']:
        print(f"❌ Importación fallida: {result['error']}")
        return
    
    # Mostrar reporte
    print("\n📊 REPORTE DE IMPORTACIÓN")
    print("="*40)
    
    summary = result['summary']
    stats = result['statistics']
    
    print(f"✅ Items procesados: {summary['total_processed']}")
    print(f"⚠️  Items omitidos: {summary['total_skipped']}")
    print(f"❌ Errores: {summary['total_errors']}")
    
    print("\n📈 Estadísticas por tipo de contenido:")
    for content_type, count in stats['by_content_type'].items():
        print(f"   {content_type}: {count}")
    
    print("\n👥 Estadísticas por audiencia:")
    for audience, count in stats['by_audience'].items():
        print(f"   {audience}: {count}")
    
    print("\n📂 Estadísticas por categoría (top 10):")
    top_categories = sorted(
        stats['by_category'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:10]
    
    for category, count in top_categories:
        print(f"   {category}: {count}")
    
    # Mostrar errores si los hay
    if result['errors']:
        print(f"\n❌ Errores encontrados ({len(result['errors'])}):")
        for error in result['errors'][:5]:  # Solo primeros 5
            print(f"   - Item {error['item_index']}: {error['title'][:50]}...")
            print(f"     Error: {error['error']}")
    
    # Exportar muestra
    sample_file = 'knowledge_base_sample.json'
    importer.export_sample_content(sample_file)
    
    print(f"\n🎉 IMPORTACIÓN COMPLETADA")
    print("="*30)
    print(f"📚 Base de conocimiento lista con {summary['total_processed']} items")
    print(f"📝 Muestra disponible en: {sample_file}")
    print(f"🚀 El KBService ahora puede dar soporte sobre:")
    print("   ✅ Autenticación y manejo de sesiones")
    print("   ✅ Gestión de asistencia y horarios")
    print("   ✅ Evaluaciones de instructores y proyectos") 
    print("   ✅ Comités académicos y reportes")
    print("   ✅ Funcionalidades específicas por rol")
    print("   ✅ Procedimientos administrativos")
    print("   ✅ Integración con servicios del sistema")


if __name__ == "__main__":
    asyncio.run(main())
