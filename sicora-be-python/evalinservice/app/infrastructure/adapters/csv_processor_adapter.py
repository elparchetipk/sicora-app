"""CSV Processor adapter."""

import csv
import os
from datetime import datetime
from typing import List
from uuid import uuid4

from ...application.interfaces import CSVProcessorInterface


class CSVProcessorAdapter(CSVProcessorInterface):
    """
    Adaptador para procesamiento de archivos CSV.
    
    Responsabilidades:
    - Implementar interfaz de CSVProcessor
    - Generar archivos CSV desde datos estructurados
    - Procesar archivos CSV para carga masiva
    - Manejar archivos en el sistema de archivos
    """
    
    def __init__(self, upload_directory: str = "/tmp/evalin_exports"):
        self._upload_dir = upload_directory
        os.makedirs(upload_directory, exist_ok=True)
    
    async def generate_csv(
        self, 
        headers: List[str], 
        data: List[List[str]], 
        filename: str
    ) -> dict:
        """
        Generar archivo CSV desde datos estructurados.
        
        Args:
            headers: Lista de encabezados de columnas
            data: Lista de filas de datos
            filename: Nombre base del archivo
            
        Returns:
            dict: Información del archivo generado
        """
        # Generar nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{filename}_{timestamp}.csv"
        file_path = os.path.join(self._upload_dir, unique_filename)
        
        # Escribir archivo CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escribir encabezados
            writer.writerow(headers)
            
            # Escribir datos
            for row in data:
                writer.writerow(row)
        
        # Obtener información del archivo
        file_size = os.path.getsize(file_path)
        
        return {
            "filename": unique_filename,
            "file_path": file_path,
            "file_size": file_size,
            "generated_at": datetime.now(),
            "download_url": f"/api/v1/exports/{unique_filename}"
        }
    
    async def process_csv_upload(self, file_path: str) -> List[dict]:
        """
        Procesar archivo CSV cargado y extraer datos.
        
        Args:
            file_path: Ruta del archivo CSV
            
        Returns:
            List[dict]: Lista de registros procesados
        """
        records = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                # Detectar dialecto del CSV
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                
                reader = csv.DictReader(csvfile, dialect=dialect)
                
                for row_num, row in enumerate(reader, start=2):  # Empezar en 2 por encabezados
                    # Limpiar datos
                    cleaned_row = {}
                    for key, value in row.items():
                        if key:  # Ignorar columnas sin nombre
                            cleaned_row[key.strip()] = value.strip() if value else ""
                    
                    if cleaned_row:  # Solo agregar filas no vacías
                        cleaned_row["_row_number"] = row_num
                        records.append(cleaned_row)
                        
        except Exception as e:
            raise ValueError(f"Error al procesar archivo CSV: {str(e)}")
        
        return records
    
    async def validate_csv_structure(
        self, 
        file_path: str, 
        required_columns: List[str]
    ) -> dict:
        """
        Validar estructura de archivo CSV.
        
        Args:
            file_path: Ruta del archivo CSV
            required_columns: Columnas requeridas
            
        Returns:
            dict: Resultado de validación
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, [])
                
                # Limpiar encabezados
                headers = [h.strip() for h in headers if h.strip()]
                
                # Verificar columnas requeridas
                missing_columns = []
                for col in required_columns:
                    if col not in headers:
                        missing_columns.append(col)
                
                # Contar filas
                row_count = sum(1 for _ in reader)
                
                return {
                    "valid": len(missing_columns) == 0,
                    "headers": headers,
                    "missing_columns": missing_columns,
                    "row_count": row_count,
                    "message": "Estructura válida" if len(missing_columns) == 0 else f"Faltan columnas: {missing_columns}"
                }
                
        except Exception as e:
            return {
                "valid": False,
                "headers": [],
                "missing_columns": required_columns,
                "row_count": 0,
                "message": f"Error al leer archivo: {str(e)}"
            }
    
    async def cleanup_file(self, file_path: str) -> bool:
        """
        Limpiar archivo temporal.
        
        Args:
            file_path: Ruta del archivo a limpiar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error al eliminar archivo: {e}")
        
        return False
