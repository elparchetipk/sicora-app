from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class QRCodeService(ABC):
    """Interfaz para el servicio de códigos QR."""

    @abstractmethod
    async def generate_qr_code(
        self,
        instructor_id: str,
        ficha_id: str,
        block_identifier: str,
        venue_id: str,
        validity_seconds: int = 900  # 15 minutos por defecto
    ) -> str:
        """
        Genera un código QR único para registro de asistencia.
        
        Args:
            instructor_id: ID del instructor que genera el código
            ficha_id: ID de la ficha
            block_identifier: Identificador del bloque de clase
            venue_id: ID del lugar donde se imparte la clase
            validity_seconds: Segundos de validez del código
            
        Returns:
            Código QR único y temporal
        """
        pass

    @abstractmethod
    async def validate_qr_code(
        self,
        qr_code: str,
        student_id: str,
        expected_ficha_id: str
    ) -> dict:
        """
        Valida un código QR para registro de asistencia.
        
        Args:
            qr_code: Código QR a validar
            student_id: ID del estudiante que usa el código
            expected_ficha_id: ID de la ficha esperada
            
        Returns:
            Diccionario con datos del QR si es válido
            
        Raises:
            InvalidQRCodeError: Si el código no es válido o ha expirado
        """
        pass

    @abstractmethod
    async def invalidate_qr_code(self, qr_code: str) -> bool:
        """
        Invalida manualmente un código QR.
        
        Args:
            qr_code: Código QR a invalidar
            
        Returns:
            True si se invalidó correctamente
        """
        pass

    @abstractmethod
    async def get_active_qr_codes(self, instructor_id: str) -> list[dict]:
        """
        Obtiene los códigos QR activos generados por un instructor.
        
        Args:
            instructor_id: ID del instructor
            
        Returns:
            Lista de códigos QR activos con su información
        """
        pass

    @abstractmethod
    async def cleanup_expired_codes(self) -> int:
        """
        Limpia códigos QR expirados del sistema.
        
        Returns:
            Número de códigos eliminados
        """
        pass
