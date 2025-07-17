#!/usr/bin/env python3
"""
Script CLI para procesamiento de PDFs para SICORA KBService.
Permite procesar PDFs individuales o en batch desde línea de comandos.
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from app.infrastructure.pdf_processing import PDFProcessor, PDFProcessingError

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFProcessorCLI:
    """Interfaz CLI para procesamiento de PDFs."""
    
    def __init__(self):
        self.processor = PDFProcessor(use_ocr=False)
    
    async def process_single_file(
        self,
        file_path: str,
        content_type: str = None,
        category: str = None,
        target_audience: str = "all",
        output_file: str = None
    ) -> Dict[str, Any]:
        """Procesar un archivo PDF individual."""
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        logger.info(f"Procesando archivo: {file_path}")
        
        result = await self.processor.process_pdf_file(
            str(file_path),
            content_type=content_type,
            category=category,
            target_audience=target_audience
        )
        
        if result.get("processing_status") == "success":
            logger.info(f"✅ Archivo procesado exitosamente")
            logger.info(f"   - Título: {result['title']}")
            logger.info(f"   - Tipo: {result['content_type']}")
            logger.info(f"   - Categoría: {result['category']}")
            logger.info(f"   - Páginas: {result['metadata']['pages']}")
            logger.info(f"   - Caracteres: {result['metadata']['text_length']}")
            logger.info(f"   - Método: {result['metadata']['extraction_method']}")
            
            # Guardar resultado si se especifica archivo de salida
            if output_file:
                output_path = Path(output_file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False, default=str)
                logger.info(f"   - Resultado guardado en: {output_path}")
        else:
            logger.error(f"❌ Error procesando archivo: {result.get('error_message')}")
        
        return result
    
    async def process_batch(
        self,
        directory_path: str,
        content_type: str = None,
        category: str = None,
        target_audience: str = "all",
        auto_categorize: bool = True,
        output_dir: str = None
    ) -> Dict[str, List]:
        """Procesar múltiples PDFs en un directorio."""
        
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            raise NotADirectoryError(f"Directorio no encontrado: {directory}")
        
        # Buscar archivos PDF
        pdf_files = list(directory.glob("*.pdf")) + list(directory.glob("*.PDF"))
        
        if not pdf_files:
            logger.warning(f"No se encontraron archivos PDF en: {directory}")
            return {"successful": [], "failed": []}
        
        logger.info(f"Encontrados {len(pdf_files)} archivos PDF")
        
        results = {"successful": [], "failed": []}
        
        # Crear directorio de salida si se especifica
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
        
        for i, pdf_file in enumerate(pdf_files, 1):
            logger.info(f"[{i}/{len(pdf_files)}] Procesando: {pdf_file.name}")
            
            try:
                result = await self.processor.process_pdf_file(
                    str(pdf_file),
                    content_type=content_type if not auto_categorize else None,
                    category=category if not auto_categorize else None,
                    target_audience=target_audience
                )
                
                if result.get("processing_status") == "success":
                    results["successful"].append({
                        "filename": pdf_file.name,
                        "title": result["title"],
                        "content_type": result["content_type"],
                        "category": result["category"],
                        "pages": result["metadata"]["pages"],
                        "text_length": result["metadata"]["text_length"],
                        "extraction_method": result["metadata"]["extraction_method"]
                    })
                    
                    # Guardar resultado individual si se especifica directorio
                    if output_dir:
                        output_file = output_path / f"{pdf_file.stem}_processed.json"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
                    
                    logger.info(f"   ✅ Exitoso - {result['content_type']} en {result['category']}")
                else:
                    results["failed"].append({
                        "filename": pdf_file.name,
                        "error": result.get("error_message", "Error desconocido")
                    })
                    logger.error(f"   ❌ Error: {result.get('error_message')}")
                    
            except Exception as e:
                results["failed"].append({
                    "filename": pdf_file.name,
                    "error": str(e)
                })
                logger.error(f"   ❌ Excepción: {e}")
        
        # Resumen final
        successful_count = len(results["successful"])
        failed_count = len(results["failed"])
        
        logger.info(f"\n📊 Resumen del procesamiento batch:")
        logger.info(f"   ✅ Exitosos: {successful_count}")
        logger.info(f"   ❌ Fallidos: {failed_count}")
        logger.info(f"   📁 Total: {len(pdf_files)}")
        
        if successful_count > 0:
            logger.info(f"\n📈 Tipos de contenido procesados:")
            content_types = {}
            for item in results["successful"]:
                ct = item["content_type"]
                content_types[ct] = content_types.get(ct, 0) + 1
            
            for content_type, count in content_types.items():
                logger.info(f"   - {content_type}: {count} documentos")
        
        # Guardar resumen si se especifica directorio
        if output_dir:
            summary_file = output_path / "batch_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"\n💾 Resumen guardado en: {summary_file}")
        
        return results


def main():
    """Función principal del CLI."""
    parser = argparse.ArgumentParser(
        description="Procesador de PDFs para SICORA KBService",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Procesar un PDF individual
  python pdf_processor.py --file reglamento_aprendiz.pdf --content-type policy

  # Procesamiento en batch con auto-categorización
  python pdf_processor.py --batch-dir documentos_sena/ --auto-categorize

  # Procesar con OCR para documentos escaneados
  python pdf_processor.py --file documento_escaneado.pdf --ocr --content-type procedure

  # Guardar resultados en archivos
  python pdf_processor.py --file manual.pdf --output resultado.json
  python pdf_processor.py --batch-dir docs/ --output-dir resultados/

Tipos de contenido disponibles:
  - article: Artículos informativos
  - faq: Preguntas frecuentes
  - guide: Guías paso a paso
  - procedure: Procedimientos oficiales
  - tutorial: Tutoriales educativos
  - policy: Políticas y reglamentos
        """
    )
    
    # Grupo mutuamente exclusivo para archivo individual vs batch
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file", "-f",
        type=str,
        help="Archivo PDF individual a procesar"
    )
    group.add_argument(
        "--batch-dir", "-b",
        type=str,
        help="Directorio con múltiples PDFs para procesamiento en batch"
    )
    
    # Opciones de contenido
    parser.add_argument(
        "--content-type", "-t",
        type=str,
        choices=["article", "faq", "guide", "procedure", "tutorial", "policy"],
        help="Tipo de contenido (se auto-detecta si no se especifica)"
    )
    parser.add_argument(
        "--category", "-c",
        type=str,
        help="Categoría del documento (se auto-detecta si no se especifica)"
    )
    parser.add_argument(
        "--target-audience", "-a",
        type=str,
        choices=["all", "admin", "instructor", "student", "admin_instructor"],
        default="all",
        help="Audiencia objetivo (default: all)"
    )
    
    # Opciones de procesamiento
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="Usar OCR para documentos escaneados (más lento)"
    )
    parser.add_argument(
        "--auto-categorize",
        action="store_true",
        default=True,
        help="Auto-categorizar basado en contenido (default: activado)"
    )
    parser.add_argument(
        "--no-auto-categorize",
        action="store_false",
        dest="auto_categorize",
        help="Desactivar auto-categorización"
    )
    
    # Opciones de salida
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Archivo de salida para resultado (solo para archivo individual)"
    )
    parser.add_argument(
        "--output-dir", "-d",
        type=str,
        help="Directorio de salida para resultados (solo para batch)"
    )
    
    # Opciones de logging
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Logging detallado"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Solo mostrar errores"
    )
    
    args = parser.parse_args()
    
    # Configurar nivel de logging
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Crear procesador CLI
    cli = PDFProcessorCLI()
    
    # Configurar OCR si se solicita
    if args.ocr:
        cli.processor.use_ocr = True
        logger.info("OCR habilitado para documentos escaneados")
    
    try:
        if args.file:
            # Procesar archivo individual
            result = asyncio.run(cli.process_single_file(
                file_path=args.file,
                content_type=args.content_type,
                category=args.category,
                target_audience=args.target_audience,
                output_file=args.output
            ))
            
            if result.get("processing_status") != "success":
                sys.exit(1)
                
        elif args.batch_dir:
            # Procesamiento en batch
            results = asyncio.run(cli.process_batch(
                directory_path=args.batch_dir,
                content_type=args.content_type,
                category=args.category,
                target_audience=args.target_audience,
                auto_categorize=args.auto_categorize,
                output_dir=args.output_dir
            ))
            
            if len(results["failed"]) > 0:
                logger.warning(f"Algunos archivos fallaron en el procesamiento")
                if len(results["successful"]) == 0:
                    sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
