"""
Versión simplificada del procesador de PDF sin PyMuPDF para la demostración.
"""

import os
import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import hashlib
from datetime import datetime

# PDF Processing (solo las librerías disponibles)
import PyPDF2
import pdfplumber
from PIL import Image
import io

# Text Processing
try:
    from langdetect import detect
except ImportError:
    def detect(text):
        return "es"  # Default español

# FastAPI
from fastapi import UploadFile

logger = logging.getLogger(__name__)


class PDFProcessingError(Exception):
    """Excepción para errores de procesamiento de PDF."""
    pass


class SimplePDFProcessor:
    """Procesador simplificado de documentos PDF."""
    
    def __init__(self, use_ocr: bool = False):
        """
        Inicializar el procesador de PDF.
        
        Args:
            use_ocr: Si usar OCR para PDFs escaneados (deshabilitado en esta versión)
        """
        self.use_ocr = False  # Deshabilitado para esta demo
        self.supported_mime_types = [
            'application/pdf',
            'application/x-pdf',
            'application/x-bzpdf',
            'application/x-gzpdf'
        ]
    
    def is_pdf_file(self, file_path: str) -> bool:
        """Verificar si el archivo es un PDF válido."""
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
    
    def extract_text(self, file_path: str) -> Tuple[str, str]:
        """
        Extraer texto de PDF usando métodos disponibles.
        
        Returns:
            Tuple[str, str]: (texto_extraído, método_usado)
        """
        if not self.is_pdf_file(file_path):
            raise PDFProcessingError(f"El archivo {file_path} no es un PDF válido")
        
        # Intentar múltiples métodos de extracción
        methods = [
            ("pdfplumber", self.extract_text_pdfplumber),
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
        if len(paragraphs) > 1:
            chunks = []
            current_chunk = ""
            
            for paragraph in paragraphs:
                if len(current_chunk) + len(paragraph) <= max_chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph + "\n\n"
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            return chunks
        
        # Si no hay párrafos, segmentar por oraciones
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text]


# Instancia global para usar en la demo
pdf_processor = SimplePDFProcessor()
