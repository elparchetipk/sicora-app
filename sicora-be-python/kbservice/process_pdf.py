#!/usr/bin/env python3
"""
Script para procesar cualquier PDF del reglamento del aprendiz.
Uso: python process_pdf.py ruta/al/archivo.pdf
"""

import sys
import os
import json
from pathlib import Path
from simple_pdf_processor import SimplePDFProcessor


def process_real_pdf(pdf_path: str):
    """Procesar un PDF real del reglamento."""
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: El archivo {pdf_path} no existe")
        return False
    
    print(f"🔍 Procesando PDF: {pdf_path}")
    print("="*60)
    
    processor = SimplePDFProcessor()
    
    try:
        # 1. Extraer texto
        print("1. Extrayendo texto...")
        text, method = processor.extract_text(pdf_path)
        print(f"   ✅ Método: {method}")
        print(f"   ✅ Caracteres extraídos: {len(text):,}")
        
        # 2. Extraer metadatos
        print("\n2. Extrayendo metadatos...")
        metadata = processor.extract_metadata(pdf_path)
        print(f"   ✅ Archivo: {metadata['file_name']}")
        print(f"   ✅ Tamaño: {metadata['file_size']:,} bytes")
        print(f"   ✅ Páginas: {metadata['pages']}")
        print(f"   ✅ Autor: {metadata.get('author', 'N/A')}")
        print(f"   ✅ Título: {metadata.get('title', 'N/A')}")
        
        # 3. Limpiar texto
        print("\n3. Limpiando texto...")
        clean_text = processor.clean_text(text)
        print(f"   ✅ Caracteres después de limpieza: {len(clean_text):,}")
        
        # 4. Detectar idioma
        language = processor.detect_language(clean_text)
        print(f"   ✅ Idioma detectado: {language}")
        
        # 5. Buscar estructura
        print("\n4. Analizando estructura...")
        import re
        
        # Buscar capítulos
        capitulos = re.findall(r'CAP[ÍI]TULO\s+([IVX\d]+)[^\n]*', clean_text, re.IGNORECASE)
        print(f"   ✅ Capítulos encontrados: {len(capitulos)}")
        
        # Buscar artículos
        articulos = re.findall(r'ART[ÍI]CULO\s+(\d+)[^\n]*', clean_text, re.IGNORECASE)
        print(f"   ✅ Artículos encontrados: {len(articulos)}")
        
        # Buscar secciones importantes
        derechos = len(re.findall(r'derecho[s]?', clean_text, re.IGNORECASE))
        deberes = len(re.findall(r'deber[es]?|obligaci[oó]n[es]?', clean_text, re.IGNORECASE))
        sanciones = len(re.findall(r'sanci[oó]n[es]?|falta[s]?', clean_text, re.IGNORECASE))
        
        print(f"   📊 Menciones de 'derechos': {derechos}")
        print(f"   📊 Menciones de 'deberes': {deberes}")
        print(f"   📊 Menciones de 'sanciones': {sanciones}")
        
        # 6. Segmentar texto
        print("\n5. Segmentando para procesamiento...")
        chunks = processor.segment_text(clean_text, max_chunk_size=1500)
        print(f"   ✅ Chunks creados: {len(chunks)}")
        
        # Mostrar vista previa de chunks
        print("\n6. Vista previa de chunks:")
        for i, chunk in enumerate(chunks[:5]):  # Solo primeros 5
            preview = chunk[:100].replace('\n', ' ')
            print(f"   📝 Chunk {i+1}: {preview}...")
        
        # 7. Guardar resultado
        output_file = pdf_path.replace('.pdf', '_processed.json')
        result = {
            'metadata': metadata,
            'text_stats': {
                'original_length': len(text),
                'clean_length': len(clean_text),
                'language': language,
                'method_used': method
            },
            'structure': {
                'capitulos': len(capitulos),
                'articulos': len(articulos),
                'chunks': len(chunks)
            },
            'content_analysis': {
                'derechos_mentions': derechos,
                'deberes_mentions': deberes,
                'sanciones_mentions': sanciones
            },
            'chunks': chunks[:10]  # Solo primeros 10 para no hacer el archivo muy grande
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n7. ✅ Resultado guardado en: {output_file}")
        
        # 8. Mostrar resumen final
        print("\n" + "="*60)
        print("📊 RESUMEN DEL PROCESAMIENTO")
        print("="*60)
        print(f"📄 Archivo: {os.path.basename(pdf_path)}")
        print(f"📝 Texto extraído: {len(clean_text):,} caracteres")
        print(f"📚 Páginas: {metadata['pages']}")
        print(f"🔧 Método: {method}")
        print(f"🌍 Idioma: {language}")
        print(f"📊 Estructura: {len(capitulos)} capítulos, {len(articulos)} artículos")
        print(f"📦 Chunks: {len(chunks)} secciones para procesamiento")
        print(f"💾 Resultado: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error procesando PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    if len(sys.argv) != 2:
        print("📖 Uso: python process_pdf.py ruta/al/archivo.pdf")
        print("\n📝 Ejemplo:")
        print("   python process_pdf.py reglamento_aprendiz.pdf")
        print("   python process_pdf.py /ruta/completa/al/reglamento.pdf")
        return
    
    pdf_path = sys.argv[1]
    
    print("🚀 PROCESADOR DE PDFs DEL REGLAMENTO DEL APRENDIZ")
    print("=" * 60)
    
    success = process_real_pdf(pdf_path)
    
    if success:
        print("\n🎉 ¡Procesamiento completado exitosamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Revisa el archivo JSON generado")
        print("   2. Los chunks están listos para cargar en la base de conocimiento")
        print("   3. Usa el API para integrar con SICORA")
    else:
        print("\n❌ El procesamiento falló. Revisa el error anterior.")


if __name__ == "__main__":
    main()
