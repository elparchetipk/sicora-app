from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID


class FileUploadService(ABC):
    """Interfaz para el servicio de subida de archivos."""

    @abstractmethod
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
            Ruta donde se almacenó el archivo
            
        Raises:
            InvalidJustificationFileError: Si el archivo no es válido
        """
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """
        Elimina un archivo del almacenamiento.
        
        Args:
            file_path: Ruta del archivo a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        pass

    @abstractmethod
    async def get_file_url(self, file_path: str) -> str:
        """
        Obtiene la URL pública para acceder al archivo.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            URL pública del archivo
        """
        pass

    @abstractmethod
    def validate_file(
        self,
        file_content: bytes,
        file_name: str,
        allowed_types: list[str] = None
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
        pass
