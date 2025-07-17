#!/usr/bin/env python3
"""
Importador de FAQs Actualizadas al KBService
Importa las FAQs corregidas sobre el sistema de asistencia con códigos QR
"""

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KBFAQImporter:
    """Importador de FAQs al KBService."""
    
    def __init__(self, db_path: str = "kb.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect_db(self):
        """Conectar a la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            logger.info(f"Conectado a la base de datos: {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"Error conectando a la base de datos: {e}")
            return False
    
    def create_tables_if_not_exist(self):
        """Crear tablas necesarias si no existen."""
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS kb_articles (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                content_type TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT DEFAULT 'published',
                priority TEXT DEFAULT 'medium',
                target_audience TEXT,
                tags TEXT,
                search_keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS kb_faqs (
                id TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                short_answer TEXT NOT NULL,
                detailed_answer TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                target_audience TEXT,
                tags TEXT,
                search_keywords TEXT,
                status TEXT DEFAULT 'published',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS kb_categories (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                parent_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS kb_tags (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                category TEXT,
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        try:
            cursor = self.conn.cursor()
            for table_sql in tables_sql:
                cursor.execute(table_sql)
            self.conn.commit()
            logger.info("Tablas verificadas/creadas exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error creando tablas: {e}")
            return False
    
    def load_faqs_from_json(self, json_file: str):
        """Cargar FAQs desde archivo JSON."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                faqs = json.load(f)
            logger.info(f"Cargadas {len(faqs)} FAQs desde {json_file}")
            return faqs
        except Exception as e:
            logger.error(f"Error cargando FAQs desde {json_file}: {e}")
            return []
    
    def import_faq(self, faq_data: dict):
        """Importar una FAQ individual."""
        try:
            cursor = self.conn.cursor()
            
            # Verificar si ya existe
            cursor.execute("SELECT id FROM kb_faqs WHERE id = ?", (faq_data['id'],))
            exists = cursor.fetchone()
            
            # Preparar datos
            target_audience_str = json.dumps(faq_data.get('target_audience', []))
            tags_str = json.dumps(faq_data.get('tags', []))
            keywords_str = json.dumps(faq_data.get('search_keywords', []))
            
            if exists:
                # Actualizar FAQ existente
                update_sql = """
                UPDATE kb_faqs SET
                    question = ?,
                    short_answer = ?,
                    detailed_answer = ?,
                    category = ?,
                    priority = ?,
                    target_audience = ?,
                    tags = ?,
                    search_keywords = ?,
                    status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """
                cursor.execute(update_sql, (
                    faq_data['question'],
                    faq_data['short_answer'],
                    faq_data['detailed_answer'],
                    faq_data['category'],
                    faq_data.get('priority', 'medium'),
                    target_audience_str,
                    tags_str,
                    keywords_str,
                    faq_data.get('status', 'published'),
                    faq_data['id']
                ))
                logger.info(f"FAQ actualizada: {faq_data['id']}")
            else:
                # Insertar nueva FAQ
                insert_sql = """
                INSERT INTO kb_faqs (
                    id, question, short_answer, detailed_answer, category,
                    priority, target_audience, tags, search_keywords, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insert_sql, (
                    faq_data['id'],
                    faq_data['question'],
                    faq_data['short_answer'],
                    faq_data['detailed_answer'],
                    faq_data['category'],
                    faq_data.get('priority', 'medium'),
                    target_audience_str,
                    tags_str,
                    keywords_str,
                    faq_data.get('status', 'published')
                ))
                logger.info(f"FAQ creada: {faq_data['id']}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error importando FAQ {faq_data.get('id', 'unknown')}: {e}")
            return False
    
    def import_category_if_not_exists(self, category_name: str, description: str = None):
        """Importar categoría si no existe."""
        try:
            cursor = self.conn.cursor()
            
            # Verificar si existe
            cursor.execute("SELECT id FROM kb_categories WHERE name = ?", (category_name,))
            exists = cursor.fetchone()
            
            if not exists:
                category_id = str(uuid.uuid4())[:12]
                cursor.execute(
                    "INSERT INTO kb_categories (id, name, description) VALUES (?, ?, ?)",
                    (category_id, category_name, description)
                )
                logger.info(f"Categoría creada: {category_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error importando categoría {category_name}: {e}")
            return False
    
    def import_tags_from_faqs(self, faqs: list):
        """Importar tags únicos desde las FAQs."""
        all_tags = set()
        
        for faq in faqs:
            tags = faq.get('tags', [])
            all_tags.update(tags)
        
        try:
            cursor = self.conn.cursor()
            
            for tag in all_tags:
                # Verificar si existe
                cursor.execute("SELECT id FROM kb_tags WHERE name = ?", (tag,))
                exists = cursor.fetchone()
                
                if not exists:
                    tag_id = str(uuid.uuid4())[:12]
                    cursor.execute(
                        "INSERT INTO kb_tags (id, name, category) VALUES (?, ?, ?)",
                        (tag_id, tag, 'general')
                    )
            
            logger.info(f"Procesados {len(all_tags)} tags únicos")
            return True
            
        except Exception as e:
            logger.error(f"Error importando tags: {e}")
            return False
    
    def update_tag_usage_counts(self):
        """Actualizar contadores de uso de tags."""
        try:
            cursor = self.conn.cursor()
            
            # Contar uso de tags en FAQs
            cursor.execute("""
                SELECT DISTINCT json_each.value as tag_name
                FROM kb_faqs, json_each(kb_faqs.tags)
            """)
            
            tag_counts = {}
            for row in cursor.fetchall():
                tag_name = row[0]
                tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
            
            # Actualizar contadores
            for tag_name, count in tag_counts.items():
                cursor.execute(
                    "UPDATE kb_tags SET usage_count = ? WHERE name = ?",
                    (count, tag_name)
                )
            
            logger.info(f"Actualizados contadores de {len(tag_counts)} tags")
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando contadores de tags: {e}")
            return False
    
    def generate_import_report(self):
        """Generar reporte de importación."""
        try:
            cursor = self.conn.cursor()
            
            # Estadísticas de FAQs
            cursor.execute("SELECT COUNT(*) FROM kb_faqs")
            total_faqs = cursor.fetchone()[0]
            
            cursor.execute("SELECT category, COUNT(*) FROM kb_faqs GROUP BY category")
            faqs_by_category = cursor.fetchall()
            
            cursor.execute("SELECT priority, COUNT(*) FROM kb_faqs GROUP BY priority")
            faqs_by_priority = cursor.fetchall()
            
            # Estadísticas de categorías y tags
            cursor.execute("SELECT COUNT(*) FROM kb_categories")
            total_categories = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM kb_tags")
            total_tags = cursor.fetchone()[0]
            
            report = {
                'total_faqs': total_faqs,
                'faqs_by_category': dict(faqs_by_category),
                'faqs_by_priority': dict(faqs_by_priority),
                'total_categories': total_categories,
                'total_tags': total_tags,
                'import_timestamp': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generando reporte: {e}")
            return {}
    
    def close(self):
        """Cerrar conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            logger.info("Conexión a base de datos cerrada")


def main():
    """Función principal."""
    print("🚀 Importador de FAQs Actualizadas al KBService")
    print("=" * 60)
    
    # Configuración
    faqs_file = "implementable_critical_faqs_updated.json"
    db_path = "kb.db"
    
    # Verificar que existe el archivo de FAQs
    if not Path(faqs_file).exists():
        logger.error(f"No se encontró el archivo de FAQs: {faqs_file}")
        return
    
    # Crear importador
    importer = KBFAQImporter(db_path)
    
    try:
        # Conectar a la base de datos
        if not importer.connect_db():
            return
        
        # Crear tablas si no existen
        if not importer.create_tables_if_not_exist():
            return
        
        # Cargar FAQs
        faqs = importer.load_faqs_from_json(faqs_file)
        if not faqs:
            return
        
        print(f"\n📄 Importando {len(faqs)} FAQs actualizadas...")
        
        # Importar categorías
        categories = set(faq.get('category', 'general') for faq in faqs)
        for category in categories:
            importer.import_category_if_not_exists(
                category, 
                f"Categoría para {category}"
            )
        
        # Importar tags
        importer.import_tags_from_faqs(faqs)
        
        # Importar FAQs
        success_count = 0
        for faq in faqs:
            if importer.import_faq(faq):
                success_count += 1
        
        # Actualizar contadores de tags
        importer.update_tag_usage_counts()
        
        # Confirmar cambios
        importer.conn.commit()
        
        # Generar reporte
        report = importer.generate_import_report()
        
        print(f"\n📊 REPORTE DE IMPORTACIÓN:")
        print(f"✅ FAQs importadas exitosamente: {success_count}/{len(faqs)}")
        print(f"📋 Total de FAQs en sistema: {report.get('total_faqs', 0)}")
        print(f"📂 Categorías: {report.get('total_categories', 0)}")
        print(f"🏷️ Tags: {report.get('total_tags', 0)}")
        
        print(f"\n📈 FAQs por categoría:")
        for category, count in report.get('faqs_by_category', {}).items():
            print(f"  {category}: {count}")
        
        print(f"\n🔥 FAQs por prioridad:")
        for priority, count in report.get('faqs_by_priority', {}).items():
            print(f"  {priority}: {count}")
        
        # Guardar reporte
        report_file = f"faq_import_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Reporte guardado en: {report_file}")
        print(f"\n✅ Importación completada exitosamente!")
        
        # Mostrar próximos pasos
        print(f"\n📋 PRÓXIMOS PASOS:")
        print("1. Verificar las FAQs importadas en el sistema")
        print("2. Probar búsquedas con las nuevas keywords")
        print("3. Configurar respuestas automáticas con IA")
        print("4. Actualizar índices de búsqueda si es necesario")
        
    except Exception as e:
        logger.error(f"Error en el proceso de importación: {e}")
    finally:
        importer.close()


if __name__ == "__main__":
    main()
