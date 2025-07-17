import os
import uuid
from pathlib import Path
from typing import List
import magic
import asyncio
from concurrent.futures import ThreadPoolExecutor

from ...application.interfaces import FileUploadService
from ...domain.exceptions import InvalidJustificationFileError


class LocalFileUploadService(FileUploadService):
    """
    Implementación local del servicio de subida de archivos.
    
    Almacena archivos en el sistema de archivos local con validaciones
    de tipo, tamaño y estructura de directorios organizadas.
    """

    def __init__(self, upload_base_path: str = "uploads/justifications"):
        self.upload_base_path = Path(upload_base_path)
        self.upload_base_path.mkdir(parents=True, exist_ok=True)
        self.allowed_mime_types = ["application/pdf"]
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        
        # ThreadPoolExecutor para operaciones de archivo
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def upload_file(
        self,
        file_content: bytes,
        file_name: str,
        file_type: str,
        max_size_mb: int = 5
    ) -> str:
        """
        Sube un archivo y retorna la ruta donde se almacenó.
        
        Args:
            file_content: Contenido binario del archivo
            file_name: Nombre original del archivo
            file_type: Tipo MIME del archivo
            max_size_mb: Tamaño máximo permitido en MB
            
        Returns:
            Ruta relativa donde se almacenó el archivo
            
        Raises:
            InvalidJustificationFileError: Si el archivo no es válido
        """
        # Validar tamaño
        max_size_bytes = max_size_mb * 1024 * 1024
        if len(file_content) > max_size_bytes:
            raise InvalidJustificationFileError(
                f"File size {len(file_content)} bytes exceeds maximum of {max_size_bytes} bytes"
            )

        # Validar tipo de archivo
        if not self.validate_file(file_content, file_name, self.allowed_mime_types):
            raise InvalidJustificationFileError(
                f"Invalid file type. Only PDF files are allowed."
            )

        # Generar nombre único para el archivo
        file_extension = Path(file_name).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Crear estructura de directorios por año/mes
        from datetime import datetime
        now = datetime.now()
        year_month_path = self.upload_base_path / str(now.year) / f"{now.month:02d}"
        year_month_path.mkdir(parents=True, exist_ok=True)
        
        # Ruta completa del archivo
        file_path = year_month_path / unique_filename
        
        # Guardar archivo de forma asíncrona
        await self._save_file_async(file_path, file_content)
        
        # Retornar ruta relativa desde la base
        return str(file_path.relative_to(self.upload_base_path))

    async def delete_file(self, file_path: str) -> bool:
        """
        Elimina un archivo del almacenamiento.
        
        Args:
            file_path: Ruta relativa del archivo a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        try:
            full_path = self.upload_base_path / file_path
            if full_path.exists() and full_path.is_file():
                await self._delete_file_async(full_path)
                return True
            return False
        except Exception:
            return False

    async def get_file_url(self, file_path: str) -> str:
        """
        Obtiene la URL pública para acceder al archivo.
        
        Args:
            file_path: Ruta relativa del archivo
            
        Returns:
            URL pública del archivo (en este caso, ruta del sistema de archivos)
        """
        full_path = self.upload_base_path / file_path
        if full_path.exists():
            return str(full_path.absolute())
        raise InvalidJustificationFileError(f"File not found: {file_path}")

    def validate_file(
        self,
        file_content: bytes,
        file_name: str,
        allowed_types: List[str] = None
    ) -> bool:
        """
        Valida que un archivo cumple con los requisitos.
        
        Args:
            file_content: Contenido binario del archivo
            file_name: Nombre del archivo
            allowed_types: Tipos MIME permitidos
            
        Returns:
            True si el archivo es válido
        """
        if allowed_types is None:
            allowed_types = self.allowed_mime_types

        try:
            # Validar extensión
            file_extension = Path(file_name).suffix.lower()
            if file_extension != '.pdf':
                return False

            # Validar contenido usando python-magic
            mime_type = magic.from_buffer(file_content, mime=True)
            if mime_type not in allowed_types:
                return False

            # Validar que el contenido es realmente un PDF
            if not file_content.startswith(b'%PDF-'):
                return False

            # Validar que no esté vacío
            if len(file_content) < 100:  # Un PDF mínimo tiene más de 100 bytes
                return False

            return True

        except Exception:
            return False

    async def _save_file_async(self, file_path: Path, content: bytes) -> None:
        """Guarda un archivo de forma asíncrona."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.executor,
            self._save_file_sync,
            file_path,
            content
        )

    def _save_file_sync(self, file_path: Path, content: bytes) -> None:
        """Guarda un archivo de forma síncrona."""
        with open(file_path, 'wb') as f:
            f.write(content)

    async def _delete_file_async(self, file_path: Path) -> None:
        """Elimina un archivo de forma asíncrona."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.executor,
            self._delete_file_sync,
            file_path
        )

    def _delete_file_sync(self, file_path: Path) -> None:
        """Elimina un archivo de forma síncrona."""
        file_path.unlink()

    def __del__(self):
        """Limpia el executor al destruir el objeto."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
