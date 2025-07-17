"""
Procesador de archivos Excel y PDF
"""
import pandas as pd
import PyPDF2
import tabula
from typing import Dict, List, Union, Optional
from io import BytesIO
import re

class FileProcessor:
    """Procesador de archivos para carga de datos"""
    
    @staticmethod
    def process_excel(file_content: BytesIO, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Procesar archivo Excel y convertir a DataFrame
        
        Args:
            file_content: Contenido del archivo Excel
            sheet_name: Nombre de la hoja (opcional)
            
        Returns:
            DataFrame con los datos del Excel
        """
        try:
            # Leer Excel
            if sheet_name:
                df = pd.read_excel(file_content, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_content)
            
            # Limpiar nombres de columnas
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Eliminar filas completamente vacías
            df = df.dropna(how='all')
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error procesando Excel: {str(e)}")
    
    @staticmethod
    def get_excel_sheets(file_content: BytesIO) -> List[str]:
        """
        Obtener lista de hojas en un archivo Excel
        
        Args:
            file_content: Contenido del archivo Excel
            
        Returns:
            Lista de nombres de hojas
        """
        try:
            excel_file = pd.ExcelFile(file_content)
            return excel_file.sheet_names
        except Exception:
            return []
    
    @staticmethod
    def process_pdf_tables(file_content: BytesIO, page: int = 1) -> List[pd.DataFrame]:
        """
        Extraer tablas de un archivo PDF
        
        Args:
            file_content: Contenido del archivo PDF
            page: Página a procesar (por defecto la primera)
            
        Returns:
            Lista de DataFrames extraídos del PDF
        """
        try:
            # Guardar temporalmente el contenido
            temp_file = "temp_pdf.pdf"
            with open(temp_file, "wb") as f:
                f.write(file_content.getvalue())
            
            # Extraer tablas con tabula
            tables = tabula.read_pdf(temp_file, pages=page)
            
            # Limpiar DataFrames
            cleaned_tables = []
            for table in tables:
                if not table.empty:
                    # Limpiar nombres de columnas
                    table.columns = table.columns.str.strip().str.lower().str.replace(' ', '_')
                    # Eliminar filas vacías
                    table = table.dropna(how='all')
                    cleaned_tables.append(table)
            
            return cleaned_tables
            
        except Exception as e:
            raise ValueError(f"Error procesando PDF: {str(e)}")
        finally:
            # Limpiar archivo temporal
            try:
                import os
                os.remove(temp_file)
            except:
                pass
    
    @staticmethod
    def extract_pdf_text(file_content: BytesIO) -> str:
        """
        Extraer texto completo de un PDF
        
        Args:
            file_content: Contenido del archivo PDF
            
        Returns:
            Texto extraído del PDF
        """
        try:
            pdf_reader = PyPDF2.PdfReader(file_content)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            raise ValueError(f"Error extrayendo texto del PDF: {str(e)}")
    
    @staticmethod
    def detect_data_types(df: pd.DataFrame) -> Dict[str, str]:
        """
        Detectar tipos de datos en un DataFrame
        
        Args:
            df: DataFrame a analizar
            
        Returns:
            Diccionario con tipos de datos detectados
        """
        type_mapping = {}
        
        for column in df.columns:
            sample_data = df[column].dropna()
            
            if sample_data.empty:
                type_mapping[column] = "unknown"
                continue
            
            # Detectar tipos
            if pd.api.types.is_integer_dtype(sample_data):
                type_mapping[column] = "integer"
            elif pd.api.types.is_float_dtype(sample_data):
                type_mapping[column] = "float"
            elif pd.api.types.is_datetime64_any_dtype(sample_data):
                type_mapping[column] = "datetime"
            elif pd.api.types.is_bool_dtype(sample_data):
                type_mapping[column] = "boolean"
            else:
                # Verificar si puede ser fecha
                if FileProcessor._is_date_column(sample_data):
                    type_mapping[column] = "date"
                # Verificar si puede ser email
                elif FileProcessor._is_email_column(sample_data):
                    type_mapping[column] = "email"
                else:
                    type_mapping[column] = "text"
        
        return type_mapping
    
    @staticmethod
    def _is_date_column(series: pd.Series) -> bool:
        """Detectar si una columna contiene fechas"""
        try:
            sample = series.head(5).astype(str)
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
                r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            ]
            
            for pattern in date_patterns:
                if sample.str.match(pattern).any():
                    return True
            return False
        except:
            return False
    
    @staticmethod
    def _is_email_column(series: pd.Series) -> bool:
        """Detectar si una columna contiene emails"""
        try:
            sample = series.head(5).astype(str)
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return sample.str.match(email_pattern).any()
        except:
            return False
    
    @staticmethod
    def preview_data(df: pd.DataFrame, max_rows: int = 10) -> Dict:
        """
        Generar vista previa de los datos
        
        Args:
            df: DataFrame a previsualizar
            max_rows: Máximo número de filas a mostrar
            
        Returns:
            Diccionario con información de la vista previa
        """
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "data_types": FileProcessor.detect_data_types(df),
            "sample_data": df.head(max_rows),
            "null_counts": df.isnull().sum().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
