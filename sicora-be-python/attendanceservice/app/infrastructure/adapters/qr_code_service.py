import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

from ...application.interfaces import QRCodeService
from ...domain.exceptions import InvalidQRCodeError


class InMemoryQRCodeService(QRCodeService):
    """
    Implementación en memoria del servicio de códigos QR.
    
    Genera códigos QR únicos y temporales para registro de asistencia
    con validación de tiempo y contexto académico.
    """

    def __init__(self):
        # Almacén en memoria para códigos QR activos
        self._active_codes: Dict[str, Dict] = {}
        self._executor = ThreadPoolExecutor(max_workers=2)
        
        # Configuración por defecto
        self.default_validity_seconds = 900  # 15 minutos
        self.max_validity_seconds = 3600     # 1 hora máximo

    async def generate_qr_code(
        self,
        instructor_id: str,
        ficha_id: str,
        block_identifier: str,
        venue_id: str,
        validity_seconds: int = 900
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
        # Validar tiempo de validez
        if validity_seconds > self.max_validity_seconds:
            validity_seconds = self.max_validity_seconds
        elif validity_seconds < 60:  # Mínimo 1 minuto
            validity_seconds = 60

        # Generar código único
        timestamp = datetime.now().isoformat()
        random_component = secrets.token_hex(16)
        
        # Crear payload del código QR
        payload = {
            "instructor_id": instructor_id,
            "ficha_id": ficha_id,
            "block_identifier": block_identifier,
            "venue_id": venue_id,
            "timestamp": timestamp,
            "random": random_component
        }

        # Generar hash del payload
        payload_str = json.dumps(payload, sort_keys=True)
        qr_code = hashlib.sha256(payload_str.encode()).hexdigest()[:32]

        # Calcular tiempo de expiración
        expires_at = datetime.now() + timedelta(seconds=validity_seconds)

        # Almacenar código activo
        self._active_codes[qr_code] = {
            "instructor_id": instructor_id,
            "ficha_id": ficha_id,
            "block_identifier": block_identifier,
            "venue_id": venue_id,
            "schedule_id": f"schedule_{ficha_id}_{block_identifier}",  # Temporal
            "created_at": datetime.now(),
            "expires_at": expires_at,
            "validity_seconds": validity_seconds,
            "is_active": True,
            "usage_count": 0
        }

        # Programar limpieza automática
        asyncio.create_task(self._schedule_cleanup(qr_code, validity_seconds))

        return qr_code

    async def validate_qr_code(
        self,
        qr_code: str,
        student_id: str,
        expected_ficha_id: str
    ) -> Dict:
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
        # Verificar que el código existe
        if qr_code not in self._active_codes:
            raise InvalidQRCodeError("QR code not found or has expired")

        code_data = self._active_codes[qr_code]

        # Verificar que el código está activo
        if not code_data["is_active"]:
            raise InvalidQRCodeError("QR code has been deactivated")

        # Verificar que no ha expirado
        if datetime.now() > code_data["expires_at"]:
            # Remover código expirado
            del self._active_codes[qr_code]
            raise InvalidQRCodeError("QR code has expired")

        # Verificar que la ficha coincide
        if code_data["ficha_id"] != expected_ficha_id:
            raise InvalidQRCodeError(
                f"QR code is for ficha {code_data['ficha_id']}, but student is in ficha {expected_ficha_id}"
            )

        # Incrementar contador de uso
        code_data["usage_count"] += 1

        # Retornar datos válidos del código
        return {
            "instructor_id": code_data["instructor_id"],
            "ficha_id": code_data["ficha_id"],
            "block_identifier": code_data["block_identifier"],
            "venue_id": code_data["venue_id"],
            "schedule_id": code_data["schedule_id"],
            "created_at": code_data["created_at"],
            "expires_at": code_data["expires_at"],
            "remaining_seconds": int((code_data["expires_at"] - datetime.now()).total_seconds()),
            "usage_count": code_data["usage_count"]
        }

    async def invalidate_qr_code(self, qr_code: str) -> bool:
        """
        Invalida manualmente un código QR.
        
        Args:
            qr_code: Código QR a invalidar
            
        Returns:
            True si se invalidó correctamente
        """
        if qr_code in self._active_codes:
            self._active_codes[qr_code]["is_active"] = False
            return True
        return False

    async def get_active_qr_codes(self, instructor_id: str) -> List[Dict]:
        """
        Obtiene los códigos QR activos generados por un instructor.
        
        Args:
            instructor_id: ID del instructor
            
        Returns:
            Lista de códigos QR activos con su información
        """
        active_codes = []
        current_time = datetime.now()

        for qr_code, data in self._active_codes.items():
            # Filtrar por instructor y códigos activos no expirados
            if (data["instructor_id"] == instructor_id and 
                data["is_active"] and 
                current_time <= data["expires_at"]):
                
                active_codes.append({
                    "qr_code": qr_code,
                    "ficha_id": data["ficha_id"],
                    "block_identifier": data["block_identifier"],
                    "venue_id": data["venue_id"],
                    "created_at": data["created_at"],
                    "expires_at": data["expires_at"],
                    "remaining_seconds": int((data["expires_at"] - current_time).total_seconds()),
                    "usage_count": data["usage_count"]
                })

        # Ordenar por fecha de creación descendente
        active_codes.sort(key=lambda x: x["created_at"], reverse=True)
        return active_codes

    async def cleanup_expired_codes(self) -> int:
        """
        Limpia códigos QR expirados del sistema.
        
        Returns:
            Número de códigos eliminados
        """
        current_time = datetime.now()
        expired_codes = []

        # Identificar códigos expirados
        for qr_code, data in self._active_codes.items():
            if current_time > data["expires_at"]:
                expired_codes.append(qr_code)

        # Remover códigos expirados
        for qr_code in expired_codes:
            del self._active_codes[qr_code]

        return len(expired_codes)

    async def _schedule_cleanup(self, qr_code: str, delay_seconds: int) -> None:
        """
        Programa la limpieza automática de un código QR.
        
        Args:
            qr_code: Código QR a limpiar
            delay_seconds: Segundos a esperar antes de limpiar
        """
        await asyncio.sleep(delay_seconds + 60)  # +60 segundos de gracia
        
        # Verificar si el código todavía existe y ha expirado
        if qr_code in self._active_codes:
            data = self._active_codes[qr_code]
            if datetime.now() > data["expires_at"]:
                del self._active_codes[qr_code]

    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas de uso de códigos QR.
        
        Returns:
            Diccionario con estadísticas del servicio
        """
        current_time = datetime.now()
        total_codes = len(self._active_codes)
        active_codes = 0
        expired_codes = 0
        total_usage = 0

        for data in self._active_codes.values():
            total_usage += data["usage_count"]
            
            if data["is_active"] and current_time <= data["expires_at"]:
                active_codes += 1
            else:
                expired_codes += 1

        return {
            "total_codes": total_codes,
            "active_codes": active_codes,
            "expired_codes": expired_codes,
            "total_usage": total_usage,
            "average_usage_per_code": total_usage / total_codes if total_codes > 0 else 0
        }

    def __del__(self):
        """Limpia el executor al destruir el objeto."""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=False)
