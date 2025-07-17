#!/usr/bin/env python3
"""
Script de demostración para mostrar capacidades de procesamiento de PDFs.
Crea un PDF de ejemplo con contenido del reglamento y lo procesa.
"""

import os
import sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# Agregar el directorio de la aplicación al path
sys.path.insert(0, str(Path(__file__).parent))

from app.infrastructure.pdf_processing import PDFProcessor


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

CAPÍTULO V
PROCEDIMIENTOS DISCIPLINARIOS

ARTÍCULO 10. DEBIDO PROCESO
Todo proceso disciplinario debe garantizar el derecho a la defensa, 
la presunción de inocencia y el derecho a ser escuchado.

ARTÍCULO 11. COMITÉ DE EVALUACIÓN Y SEGUIMIENTO
El Comité será el encargado de estudiar los casos disciplinarios y 
recomendar las sanciones correspondientes.
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


def demo_pdf_processing():
    """Demostrar las capacidades de procesamiento de PDF."""
    
    print("=== DEMOSTRACIÓN DE PROCESAMIENTO DE PDF ===\n")
    
    # Crear PDF de ejemplo
    print("1. Creando PDF de ejemplo del reglamento...")
    pdf_path = create_sample_reglamento_pdf()
    print(f"   PDF creado: {pdf_path}")
    
    # Procesar con diferentes métodos
    processor = PDFProcessor(use_ocr=False)
    
    print("\n2. Extrayendo texto del PDF...")
    try:
        text, method = processor.extract_text(pdf_path)
        print(f"   Método usado: {method}")
        print(f"   Caracteres extraídos: {len(text)}")
        
        # Mostrar los primeros 300 caracteres
        print(f"\n   Primeras líneas extraídas:")
        print("   " + "="*50)
        print("   " + text[:300] + "...")
        print("   " + "="*50)
        
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Limpiar texto
    print("\n3. Limpiando y normalizando texto...")
    clean_text = processor.clean_text(text)
    print(f"   Caracteres después de limpieza: {len(clean_text)}")
    
    # Segmentar texto
    print("\n4. Segmentando texto en chunks...")
    chunks = processor.segment_text(clean_text, max_chunk_size=1000)
    print(f"   Número de chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks[:3]):  # Mostrar solo los primeros 3
        print(f"\n   Chunk {i + 1} ({len(chunk)} chars):")
        print(f"   {chunk[:150]}...")
    
    # Extraer metadatos
    print("\n5. Extrayendo metadatos del PDF...")
    metadata = processor.extract_metadata(pdf_path)
    print("   Metadatos extraídos:")
    for key, value in metadata.items():
        print(f"     {key}: {value}")
    
    # Detectar idioma
    print("\n6. Detectando idioma...")
    language = processor.detect_language(clean_text)
    print(f"   Idioma detectado: {language}")
    
    print(f"\n7. Procesamiento completado exitosamente!")
    print(f"   Archivo temporal: {pdf_path}")
    print(f"   (Puedes eliminar el archivo cuando termines de probarlo)")


def demo_reglamento_processing():
    """Demostrar el procesamiento especializado del reglamento."""
    
    print("\n=== DEMOSTRACIÓN DE PROCESAMIENTO ESPECIALIZADO ===\n")
    
    # Importar el procesador especializado
    try:
        from process_reglamento import ReglamentoProcessor
    except ImportError:
        print("Error: No se pudo importar el procesador del reglamento")
        return
    
    # Crear PDF de ejemplo
    pdf_path = create_sample_reglamento_pdf()
    
    # Procesar con el procesador especializado
    processor = ReglamentoProcessor()
    
    print("1. Procesando reglamento con segmentación inteligente...")
    try:
        sections = processor.extract_and_segment_reglamento(pdf_path)
        
        print(f"   Secciones encontradas: {len(sections)}")
        
        print("\n2. Resumen de secciones procesadas:")
        print("   " + "="*80)
        
        for i, section in enumerate(sections):
            print(f"\n   Sección {i + 1}:")
            print(f"     Título: {section['title'][:60]}...")
            print(f"     Categoría: {section['category']}")
            print(f"     Audiencia: {section['target_audience']}")
            print(f"     Tags: {', '.join(section['tags'])}")
            print(f"     Palabras: {section['metadata']['word_count']}")
            print(f"     Tipo: {section['metadata']['section_type']}")
            
            # Mostrar fragmento del contenido
            content_preview = section['content'][:200] + "..."
            print(f"     Contenido: {content_preview}")
            
        print("\n3. El reglamento ha sido segmentado y categorizado automáticamente!")
        print("   Cada sección puede ser importada individualmente a la base de conocimiento.")
        
    except Exception as e:
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Limpiar archivo temporal
    try:
        os.unlink(pdf_path)
    except:
        pass


if __name__ == "__main__":
    # Verificar dependencias
    try:
        import reportlab
        print("Dependencias encontradas. Iniciando demostración...\n")
    except ImportError:
        print("Error: Se requiere reportlab para crear PDFs de ejemplo.")
        print("Instalar con: pip install reportlab")
        sys.exit(1)
    
    try:
        demo_pdf_processing()
        demo_reglamento_processing()
        
        print("\n" + "="*60)
        print("DEMOSTRACIÓN COMPLETADA")
        print("="*60)
        print("\nPróximos pasos para usar con PDFs reales:")
        print("1. Coloca tu PDF del reglamento en el directorio actual")
        print("2. Ejecuta: python process_reglamento.py tu_reglamento.pdf")
        print("3. Revisa el archivo de salida JSON con las secciones")
        print("4. Usa el endpoint /api/pdf/upload-pdf para subir desde la web")
        
    except Exception as e:
        print(f"\nError durante la demostración: {e}")
        import traceback
        traceback.print_exc()
