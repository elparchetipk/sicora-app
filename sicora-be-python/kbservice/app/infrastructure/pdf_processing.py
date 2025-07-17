"""
Utilidades para procesamiento de documentos PDF para KBService.
Extrae texto, metadatos y procesa documentos para la base de conocimiento.
"""

import os
import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import hashlib
from datetime import datetime

# PDF Processing
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Text Processing
import chardet
from langdetect import detect
import magic

# FastAPI
from fastapi import UploadFile

logger = logging.getLogger(__name__)


class PDFProcessingError(Exception):
    """Excepción para errores de procesamiento de PDF."""
    pass


class PDFProcessor:
    """Procesador principal de documentos PDF."""
    
    def __init__(self, use_ocr: bool = False):
        """
        Inicializar el procesador de PDF.
        
        Args:
            use_ocr: Si usar OCR para PDFs escaneados
        """
        self.use_ocr = use_ocr
        self.supported_mime_types = [
            'application/pdf',
            'application/x-pdf',
            'application/x-bzpdf',
            'application/x-gzpdf'
        ]
        
    def is_pdf_file(self, file_path: str) -> bool:
        """Verificar si el archivo es un PDF válido."""
        try:
            mime_type = magic.from_file(file_path, mime=True)
            return mime_type in self.supported_mime_types
        except Exception as e:
            logger.warning(f"Error verificando tipo MIME: {e}")
            return file_path.lower().endswith('.pdf')
    
    def extract_text_pypdf2(self, file_path: str) -> str:
        """Extraer texto usando PyPDF2."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Error con PyPDF2: {e}")
            return ""
    
    def extract_text_pdfplumber(self, file_path: str) -> str:
        """Extraer texto usando pdfplumber (mejor para tablas)."""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error con pdfplumber: {e}")
            return ""
    
    def extract_text_pymupdf(self, file_path: str) -> str:
        """Extraer texto usando PyMuPDF (mejor para layout complejo)."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error con PyMuPDF: {e}")
            return ""
    
    def extract_text_with_ocr(self, file_path: str) -> str:
        """Extraer texto usando OCR para PDFs escaneados."""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # OCR con tesseract
                page_text = pytesseract.image_to_string(
                    img, 
                    lang='spa',  # Español
                    config='--psm 6'
                )
                text += page_text + "\n"
            
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error con OCR: {e}")
            return ""
    
    def extract_text(self, file_path: str) -> Tuple[str, str]:
        """
        Extraer texto de PDF usando múltiples métodos.
        
        Returns:
            Tuple[str, str]: (texto_extraído, método_usado)
        """
        if not self.is_pdf_file(file_path):
            raise PDFProcessingError(f"El archivo {file_path} no es un PDF válido")
        
        # Intentar múltiples métodos de extracción
        methods = [
            ("pdfplumber", self.extract_text_pdfplumber),
            ("pymupdf", self.extract_text_pymupdf),
            ("pypdf2", self.extract_text_pypdf2)
        ]
        
        best_text = ""
        method_used = "none"
        
        for method_name, method_func in methods:
            try:
                text = method_func(file_path)
                if len(text) > len(best_text):
                    best_text = text
                    method_used = method_name
            except Exception as e:
                logger.warning(f"Método {method_name} falló: {e}")
                continue
        
        # Si no se extrajo texto suficiente y OCR está habilitado
        if len(best_text) < 100 and self.use_ocr:
            logger.info("Texto insuficiente, intentando con OCR...")
            ocr_text = self.extract_text_with_ocr(file_path)
            if len(ocr_text) > len(best_text):
                best_text = ocr_text
                method_used = "ocr"
        
        if not best_text.strip():
            raise PDFProcessingError("No se pudo extraer texto del PDF")
        
        return best_text, method_used
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extraer metadatos del PDF."""
        metadata = {
            "file_name": os.path.basename(file_path),
            "file_size": os.path.getsize(file_path),
            "file_hash": self._calculate_file_hash(file_path),
            "processed_at": datetime.utcnow().isoformat()
        }
        
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                info = reader.metadata
                
                if info:
                    metadata.update({
                        "title": info.get("/Title", ""),
                        "author": info.get("/Author", ""),
                        "subject": info.get("/Subject", ""),
                        "creator": info.get("/Creator", ""),
                        "producer": info.get("/Producer", ""),
                        "creation_date": str(info.get("/CreationDate", "")),
                        "modification_date": str(info.get("/ModDate", "")),
                        "pages": len(reader.pages)
                    })
        except Exception as e:
            logger.warning(f"Error extrayendo metadatos: {e}")
            metadata["pages"] = 0
        
        return metadata
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calcular hash SHA256 del archivo."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def clean_text(self, text: str) -> str:
        """Limpiar y normalizar el texto extraído."""
        if not text:
            return ""
        
        # Remover caracteres de control
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', text)
        
        # Normalizar espacios en blanco
        text = re.sub(r'\s+', ' ', text)
        
        # Remover líneas muy cortas (probablemente headers/footers)
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 10]
        
        # Unir líneas cortadas
        text = ' '.join(cleaned_lines)
        
        # Remover múltiples espacios
        text = re.sub(r' {2,}', ' ', text)
        
        return text.strip()
    
    def detect_language(self, text: str) -> str:
        """Detectar idioma del texto."""
        try:
            # Usar una muestra del texto para detección
            sample = text[:1000] if len(text) > 1000 else text
            return detect(sample)
        except Exception:
            return "es"  # Default a español
    
    def segment_text(self, text: str, max_chunk_size: int = 2000) -> List[str]:
        """Segmentar texto en chunks más pequeños para procesamiento."""
        if len(text) <= max_chunk_size:
            return [text]
        
        # Intentar segmentar por párrafos primero
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Si el párrafo es muy largo, dividirlo por oraciones
                if len(paragraph) > max_chunk_size:
                    sentences = re.split(r'[.!?]+', paragraph)
                    temp_chunk = ""
                    for sentence in sentences:
                        if len(temp_chunk) + len(sentence) <= max_chunk_size:
                            temp_chunk += sentence + ". "
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk.strip())
                            temp_chunk = sentence + ". "
                    if temp_chunk:
                        current_chunk = temp_chunk
                else:
                    current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def auto_categorize(self, text: str, filename: str) -> Tuple[str, str]:
        """Auto-categorizar documento basado en contenido y nombre."""
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # Reglas de categorización
        if any(word in text_lower for word in ['reglamento', 'norma', 'política', 'decreto']):
            return "policy", "reglamentos"
        elif any(word in text_lower for word in ['procedimiento', 'proceso', 'instrucciones']):
            return "procedure", "procedimientos"
        elif any(word in text_lower for word in ['tutorial', 'guía', 'manual', 'como']):
            return "guide", "guias"
        elif any(word in text_lower for word in ['pregunta', 'faq', 'consulta']):
            return "faq", "preguntas-frecuentes"
        elif any(word in filename_lower for word in ['reglamento', 'politica']):
            return "policy", "reglamentos"
        else:
            return "article", "general"
    
    async def process_pdf_file(
        self,
        file_path: str,
        content_type: Optional[str] = None,
        category: Optional[str] = None,
        target_audience: str = "all"
    ) -> Dict[str, Any]:
        """
        Procesar un archivo PDF completo.
        
        Returns:
            Dict con la información procesada lista para KBService
        """
        try:
            # Extraer texto y metadatos
            text, method_used = self.extract_text(file_path)
            metadata = self.extract_metadata(file_path)
            
            # Limpiar texto
            cleaned_text = self.clean_text(text)
            
            # Auto-categorizar si no se especifica
            if not content_type or not category:
                auto_type, auto_category = self.auto_categorize(cleaned_text, metadata["file_name"])
                content_type = content_type or auto_type
                category = category or auto_category
            
            # Detectar idioma
            language = self.detect_language(cleaned_text)
            
            # Segmentar texto si es muy largo
            text_chunks = self.segment_text(cleaned_text)
            
            result = {
                "title": metadata.get("title") or Path(file_path).stem,
                "content": cleaned_text,
                "content_type": content_type,
                "category": category,
                "target_audience": target_audience,
                "metadata": {
                    **metadata,
                    "extraction_method": method_used,
                    "language": language,
                    "text_length": len(cleaned_text),
                    "chunks_count": len(text_chunks)
                },
                "chunks": text_chunks if len(text_chunks) > 1 else None,
                "processing_status": "success"
            }
            
            logger.info(f"PDF procesado exitosamente: {metadata['file_name']}")
            return result
            
        except Exception as e:
            logger.error(f"Error procesando PDF {file_path}: {e}")
            return {
                "file_path": file_path,
                "processing_status": "error",
                "error_message": str(e)
            }


class PDFUploadHandler:
    """Manejador para uploads de PDF via FastAPI."""
    
    def __init__(self, processor: PDFProcessor):
        self.processor = processor
        self.upload_dir = Path("temp_uploads")
        self.upload_dir.mkdir(exist_ok=True)
    
    async def handle_upload(
        self,
        file: UploadFile,
        content_type: Optional[str] = None,
        category: Optional[str] = None,
        target_audience: str = "all"
    ) -> Dict[str, Any]:
        """Manejar upload de archivo PDF."""
        
        # Validar tipo de archivo
        if not file.content_type or "pdf" not in file.content_type.lower():
            raise PDFProcessingError("Solo se permiten archivos PDF")
        
        # Guardar archivo temporalmente
        temp_file_path = self.upload_dir / f"temp_{file.filename}"
        
        try:
            # Escribir archivo
            content = await file.read()
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(content)
            
            # Procesar PDF
            result = await self.processor.process_pdf_file(
                str(temp_file_path),
                content_type=content_type,
                category=category,
                target_audience=target_audience
            )
            
            return result
            
        finally:
            # Limpiar archivo temporal
            if temp_file_path.exists():
                temp_file_path.unlink()
    
    def cleanup_temp_files(self):
        """Limpiar archivos temporales."""
        for file_path in self.upload_dir.glob("temp_*"):
            try:
                file_path.unlink()
            except Exception as e:
                logger.warning(f"Error limpiando archivo temporal {file_path}: {e}")


# Instancia global del procesador
pdf_processor = PDFProcessor(use_ocr=False)
pdf_upload_handler = PDFUploadHandler(pdf_processor)
