"""Interface for CSV processing service."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from io import StringIO


class CSVProcessorInterface(ABC):
    """
    Interface para procesamiento de archivos CSV.
    Define el contrato para validación y procesamiento de cargas masivas.
    """
    
    @abstractmethod
    async def validate_questions_csv(self, csv_content: str) -> Tuple[bool, List[str], List[Dict]]:
        """
        Valida un archivo CSV de preguntas.
        
        Returns:
            Tuple de (es_válido, errores, datos_procesados)
        """
        pass
    
    @abstractmethod
    async def parse_questions_csv(self, csv_content: str) -> List[Dict]:
        """Parsea CSV de preguntas a diccionarios."""
        pass
    
    @abstractmethod
    def get_questions_csv_template(self) -> str:
        """Retorna la plantilla CSV para preguntas."""
        pass
    
    @abstractmethod
    def get_required_columns(self) -> List[str]:
        """Retorna las columnas requeridas para CSV de preguntas."""
        pass
    
    @abstractmethod
    async def generate_sample_csv(self, sample_size: int = 5) -> str:
        """Genera un archivo CSV de ejemplo."""
        pass
    
    @abstractmethod
    async def validate_csv_format(self, csv_content: str) -> Tuple[bool, List[str]]:
        """Valida el formato básico del CSV."""
        pass
