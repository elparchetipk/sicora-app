#!/usr/bin/env python3
"""
Demo simplificada de procesamiento de PDF sin PyMuPDF.
"""

import os
import sys
import tempfile
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Importar nuestro procesador simplificado
from simple_pdf_processor import SimplePDFProcessor


def create_sample_reglamento_pdf() -> str:
    """Crear un PDF de ejemplo con contenido del reglamento."""
    
    # Contenido de ejemplo del reglamento
    content = """
REGLAMENTO DEL APRENDIZ SENA

CAPÍTULO I
DISPOSICIONES GENERALES

ARTÍCULO 1. OBJETO
El presente reglamento tiene por objeto definir los derechos y deberes de los aprendices del SENA, 
así como las condiciones de matrícula académica, el desarrollo de los procesos formativos, 
la evaluación de los aprendizajes y el reconocimiento de competencias.

ARTÍCULO 2. ÁMBITO DE APLICACIÓN  
Este reglamento se aplica a todos los aprendices matriculados en programas de formación 
profesional integral del SENA en todas sus modalidades: presencial, virtual, a distancia 
y en alternancia.

CAPÍTULO II
DERECHOS DE LOS APRENDICES

ARTÍCULO 3. DERECHOS FUNDAMENTALES
Los aprendices del SENA tienen derecho a:

1. Recibir formación profesional integral de calidad
2. Ser tratados con dignidad y respeto
3. Participar en el mejoramiento continuo de la formación
4. Acceder a los recursos tecnológicos y bibliográficos
5. Obtener certificación de las competencias desarrolladas

ARTÍCULO 4. DERECHO A LA EVALUACIÓN
Todo aprendiz tiene derecho a ser evaluado de manera objetiva, integral y permanente, 
conocer previamente los criterios de evaluación y recibir retroalimentación oportuna.

CAPÍTULO III
DEBERES DE LOS APRENDICES

ARTÍCULO 5. DEBERES GENERALES
Son deberes de los aprendices:

1. Cumplir con el reglamento interno y las normas de convivencia
2. Asistir puntualmente a las actividades de formación
3. Participar activamente en el proceso de aprendizaje
4. Utilizar adecuadamente los recursos institucionales
5. Mantener un comportamiento ético y responsable

ARTÍCULO 6. RESPONSABILIDAD ACADÉMICA
Los aprendices deben cumplir con todas las actividades de formación programadas, 
presentar las evaluaciones en las fechas establecidas y mantener un rendimiento 
académico satisfactorio.

CAPÍTULO IV
PROHIBICIONES Y SANCIONES

ARTÍCULO 7. PROHIBICIONES
Se prohíbe a los aprendices:

1. Portar armas o sustancias psicoactivas
2. Agredir física o verbalmente a compañeros o funcionarios
3. Sustraer bienes institucionales
4. Falsificar documentos
5. Interferir con el desarrollo normal de las actividades

ARTÍCULO 8. TIPOS DE FALTAS
Las faltas se clasifican en:
- Faltas leves: Retrasos, inasistencia injustificada menor a 3 días
- Faltas graves: Irrespeto, daño a equipos, inasistencia prolongada
- Faltas gravísimas: Agresión, hurto, falsificación de documentos

ARTÍCULO 9. SANCIONES APLICABLES
Según la gravedad de la falta se aplicarán:
- Llamado de atención verbal o escrito
- Matrícula condicional
- Cancelación de matrícula con pérdida de cupo
"""

    # Crear archivo temporal
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    
    # Crear el PDF
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Dividir contenido en párrafos
    paragraphs = []
    for line in content.strip().split('\n'):
        if line.strip():
            if line.startswith('CAPÍTULO') or line.startswith('REGLAMENTO'):
                # Título principal
                para = Paragraph(line.strip(), styles['Title'])
            elif line.startswith('ARTÍCULO'):
                # Subtítulo
                para = Paragraph(line.strip(), styles['Heading2'])
            else:
                # Párrafo normal
                para = Paragraph(line.strip(), styles['Normal'])
            
            paragraphs.append(para)
            paragraphs.append(Spacer(1, 6))
    
    # Construir el documento
    doc.build(paragraphs)
    
    return temp_file.name


def demo_simple_pdf_processing():
    """Demostrar las capacidades básicas de procesamiento de PDF."""
    
    print("=== DEMO SIMPLIFICADA DE PROCESAMIENTO DE PDF ===\n")
    
    # Crear PDF de ejemplo
    print("1. Creando PDF de ejemplo del reglamento...")
    pdf_path = create_sample_reglamento_pdf()
    print(f"   ✅ PDF creado: {pdf_path}")
    
    # Procesar con el procesador simplificado
    processor = SimplePDFProcessor(use_ocr=False)
    
    print("\n2. Extrayendo texto del PDF...")
    try:
        text, method = processor.extract_text(pdf_path)
        print(f"   ✅ Método usado: {method}")
        print(f"   ✅ Caracteres extraídos: {len(text)}")
        
        # Mostrar los primeros 300 caracteres
        print(f"\n   📄 Primeras líneas extraídas:")
        print("   " + "="*60)
        preview = text[:400].replace('\n', '\n   ')
        print(f"   {preview}...")
        print("   " + "="*60)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Limpiar texto
    print("\n3. Limpiando y normalizando texto...")
    clean_text = processor.clean_text(text)
    print(f"   ✅ Caracteres después de limpieza: {len(clean_text)}")
    
    # Segmentar texto
    print("\n4. Segmentando texto en chunks...")
    chunks = processor.segment_text(clean_text, max_chunk_size=1000)
    print(f"   ✅ Número de chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks[:3]):  # Mostrar solo los primeros 3
        print(f"\n   📝 Chunk {i + 1} ({len(chunk)} chars):")
        chunk_preview = chunk[:150].replace('\n', ' ')
        print(f"      {chunk_preview}...")
    
    # Extraer metadatos
    print("\n5. Extrayendo metadatos del PDF...")
    metadata = processor.extract_metadata(pdf_path)
    print("   ✅ Metadatos extraídos:")
    for key, value in metadata.items():
        print(f"      📋 {key}: {value}")
    
    # Detectar idioma
    print("\n6. Detectando idioma...")
    language = processor.detect_language(clean_text)
    print(f"   ✅ Idioma detectado: {language}")
    
    print(f"\n7. ✅ Procesamiento completado exitosamente!")
    print(f"   📁 Archivo temporal: {pdf_path}")
    print(f"   🗑️  (Se eliminará automáticamente)")
    
    # Demostrar segmentación por capítulos
    print(f"\n8. 🔍 Analizando estructura del reglamento...")
    
    # Buscar capítulos y artículos
    import re
    capitulos = re.findall(r'CAPÍTULO\s+([IVX]+|[0-9]+)([^\n]*)', clean_text)
    articulos = re.findall(r'ARTÍCULO\s+([0-9]+)\.?\s*([^\n]*)', clean_text)
    
    print(f"   ✅ Capítulos encontrados: {len(capitulos)}")
    for i, (num, titulo) in enumerate(capitulos):
        print(f"      📚 Capítulo {num}: {titulo.strip()}")
    
    print(f"   ✅ Artículos encontrados: {len(articulos)}")
    for i, (num, titulo) in enumerate(articulos[:5]):  # Solo primeros 5
        print(f"      📄 Artículo {num}: {titulo.strip()[:50]}...")
    
    # Limpiar archivo temporal
    try:
        os.unlink(pdf_path)
        print(f"\n   🗑️  Archivo temporal eliminado")
    except:
        pass
    
    return True


def demo_text_categorization():
    """Demostrar categorización automática de texto."""
    
    print("\n=== DEMO DE CATEGORIZACIÓN AUTOMÁTICA ===\n")
    
    # Ejemplos de texto para categorizar
    test_texts = {
        "Derechos": "Los aprendices del SENA tienen derecho a recibir formación integral de calidad y ser tratados con dignidad y respeto.",
        "Deberes": "Son deberes de los aprendices cumplir con el reglamento interno, asistir puntualmente y participar activamente.",
        "Sanciones": "Las faltas graves se sancionarán con matrícula condicional y las gravísimas con cancelación de matrícula.",
        "Procedimientos": "Para presentar una queja debe dirigirse al coordinador académico con los documentos correspondientes."
    }
    
    # Categorías por palabras clave
    categories = {
        'derechos': ['derecho', 'derechos', 'garantía', 'tratado', 'dignidad'],
        'deberes': ['deber', 'deberes', 'obligación', 'responsabilidad', 'cumplir'],
        'sanciones': ['sanción', 'falta', 'cancelación', 'matrícula condicional'],
        'procedimientos': ['procedimiento', 'trámite', 'proceso', 'dirigirse', 'presentar']
    }
    
    def auto_categorize(text: str) -> str:
        """Categorizar texto automáticamente."""
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in categories.items():
            score = sum(text_lower.count(keyword) for keyword in keywords)
            if score > 0:
                scores[category] = score
        
        return max(scores, key=scores.get) if scores else "general"
    
    print("📋 Categorizando automáticamente diferentes tipos de contenido:\n")
    
    for expected_category, text in test_texts.items():
        predicted_category = auto_categorize(text)
        status = "✅" if predicted_category in expected_category.lower() else "⚠️"
        
        print(f"{status} Texto: \"{text[:60]}...\"")
        print(f"   📝 Esperado: {expected_category}")
        print(f"   🤖 Detectado: {predicted_category}")
        print()


if __name__ == "__main__":
    try:
        print("🚀 INICIANDO DEMO DE PROCESAMIENTO DE PDF...\n")
        
        # Demo principal
        success = demo_simple_pdf_processing()
        
        if success:
            # Demo de categorización
            demo_text_categorization()
            
            print("\n" + "="*70)
            print("🎉 DEMO COMPLETADA EXITOSAMENTE")
            print("="*70)
            print("\n📝 Resumen de capacidades demostradas:")
            print("   ✅ Extracción de texto desde PDF")
            print("   ✅ Limpieza y normalización automática")
            print("   ✅ Segmentación inteligente en chunks")
            print("   ✅ Extracción de metadatos")
            print("   ✅ Detección de idioma")
            print("   ✅ Identificación de estructura (capítulos/artículos)")
            print("   ✅ Categorización automática por contenido")
            print("\n🎯 Próximo paso: Usar con tu PDF real del reglamento")
            print("   Comando: python simple_pdf_processor.py tu_reglamento.pdf")
        
    except ImportError as e:
        print(f"❌ Error de dependencias: {e}")
        print("💡 Instala las dependencias con: pip install PyPDF2 pdfplumber reportlab")
    except Exception as e:
        print(f"❌ Error durante la demo: {e}")
        import traceback
        traceback.print_exc()
