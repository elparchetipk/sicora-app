"""
Adaptadores de infraestructura para servicios externos
"""

from .user_service_adapter import HTTPUserServiceAdapter
from .schedule_service_adapter import HTTPScheduleServiceAdapter
from .file_upload_service import LocalFileUploadService
from .qr_code_service import InMemoryQRCodeService

__all__ = [
    'HTTPUserServiceAdapter',
    'HTTPScheduleServiceAdapter', 
    'LocalFileUploadService',
    'InMemoryQRCodeService'
]
