"""
Validador de datos para carga en base de datos
"""
import pandas as pd
from typing import Dict, List, Tuple, Any
import re
from datetime import datetime

class DataValidator:
    """Validador de datos antes de la carga"""
    
    def __init__(self, table_columns: List[Dict]):
        """
        Inicializar validador con información de columnas de la tabla
        
        Args:
            table_columns: Lista de diccionarios con info de columnas
                          [{"name": "col", "type": "varchar", "nullable": True, "default": None}]
        """
        self.table_columns = {col["name"]: col for col in table_columns}
        self.required_columns = [col["name"] for col in table_columns if not col["nullable"] and col["default"] is None]
        self.all_columns = [col["name"] for col in table_columns]
    
    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validar DataFrame completo
        
        Args:
            df: DataFrame a validar
            
        Returns:
            Diccionario con resultados de validación
        """
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "column_mapping": {},
            "data_issues": {},
            "summary": {}
        }
        
        # 1. Validar estructura de columnas
        column_validation = self._validate_columns(df)
        validation_results.update(column_validation)
        
        # 2. Validar tipos de datos
        type_validation = self._validate_data_types(df)
        validation_results["errors"].extend(type_validation["errors"])
        validation_results["warnings"].extend(type_validation["warnings"])
        
        # 3. Validar datos requeridos
        required_validation = self._validate_required_fields(df)
        validation_results["errors"].extend(required_validation["errors"])
        validation_results["data_issues"].update(required_validation["issues"])
        
        # 4. Validar formatos específicos
        format_validation = self._validate_formats(df)
        validation_results["warnings"].extend(format_validation["warnings"])
        validation_results["data_issues"].update(format_validation["issues"])
        
        # 5. Generar resumen
        validation_results["summary"] = self._generate_summary(df, validation_results)
        
        # Determinar si es válido
        validation_results["is_valid"] = len(validation_results["errors"]) == 0
        
        return validation_results
    
    def _validate_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validar estructura de columnas"""
        result = {
            "column_mapping": {},
            "errors": [],
            "warnings": []
        }
        
        df_columns = list(df.columns)
        
        # Mapeo automático de columnas
        for df_col in df_columns:
            mapped_col = self._find_column_match(df_col)
            if mapped_col:
                result["column_mapping"][df_col] = mapped_col
            else:
                result["warnings"].append(f"Columna '{df_col}' no reconocida en la tabla")
        
        # Verificar columnas requeridas
        mapped_columns = list(result["column_mapping"].values())
        missing_required = [col for col in self.required_columns if col not in mapped_columns]
        
        if missing_required:
            result["errors"].append(f"Faltan columnas requeridas: {', '.join(missing_required)}")
        
        return result
    
    def _find_column_match(self, df_column: str) -> str:
        """Encontrar coincidencia de columna con la tabla"""
        df_col_clean = df_column.lower().strip().replace(' ', '_')
        
        # Coincidencia exacta
        if df_col_clean in self.all_columns:
            return df_col_clean
        
        # Coincidencia parcial
        for table_col in self.all_columns:
            if table_col in df_col_clean or df_col_clean in table_col:
                return table_col
        
        # Mapeos comunes
        common_mappings = {
            "nombre": "name",
            "correo": "email",
            "email": "email",
            "cedula": "document_number",
            "documento": "document_number",
            "fecha": "date",
            "hora": "time",
            "estado": "status",
            "activo": "active",
            "descripcion": "description"
        }
        
        for key, value in common_mappings.items():
            if key in df_col_clean and value in self.all_columns:
                return value
        
        return None
    
    def _validate_data_types(self, df: pd.DataFrame) -> Dict[str, List]:
        """Validar tipos de datos"""
        errors = []
        warnings = []
        
        for df_col, table_col in self.column_mapping.items():
            if table_col not in self.table_columns:
                continue
                
            expected_type = self.table_columns[table_col]["type"]
            series = df[df_col]
            
            # Validar según el tipo esperado
            if "varchar" in expected_type or "text" in expected_type:
                # Verificar longitud si está especificada
                if "(" in expected_type:
                    max_length = int(expected_type.split("(")[1].split(")")[0])
                    long_values = series.str.len() > max_length
                    if long_values.any():
                        warnings.append(f"Columna '{df_col}': {long_values.sum()} valores exceden longitud máxima ({max_length})")
            
            elif "integer" in expected_type or "int" in expected_type:
                non_int = pd.to_numeric(series, errors='coerce').isna() & series.notna()
                if non_int.any():
                    errors.append(f"Columna '{df_col}': {non_int.sum()} valores no son enteros válidos")
            
            elif "timestamp" in expected_type or "date" in expected_type:
                try:
                    pd.to_datetime(series, errors='coerce')
                except:
                    errors.append(f"Columna '{df_col}': contiene fechas en formato inválido")
        
        return {"errors": errors, "warnings": warnings}
    
    def _validate_required_fields(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validar campos requeridos"""
        errors = []
        issues = {}
        
        for df_col, table_col in self.column_mapping.items():
            if table_col in self.required_columns:
                null_count = df[df_col].isna().sum()
                if null_count > 0:
                    errors.append(f"Columna requerida '{df_col}' tiene {null_count} valores nulos")
                    issues[df_col] = f"{null_count} valores nulos"
        
        return {"errors": errors, "issues": issues}
    
    def _validate_formats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validar formatos específicos"""
        warnings = []
        issues = {}
        
        for df_col, table_col in self.column_mapping.items():
            series = df[df_col].dropna()
            
            # Validar emails
            if "email" in table_col.lower():
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                invalid_emails = ~series.str.match(email_pattern, na=False)
                if invalid_emails.any():
                    warnings.append(f"Columna '{df_col}': {invalid_emails.sum()} emails con formato inválido")
                    issues[df_col] = f"{invalid_emails.sum()} emails inválidos"
            
            # Validar números de documento
            if "document" in table_col.lower():
                # Asumir que documentos deben ser numéricos y tener longitud apropiada
                non_numeric = pd.to_numeric(series, errors='coerce').isna()
                if non_numeric.any():
                    warnings.append(f"Columna '{df_col}': {non_numeric.sum()} documentos no numéricos")
        
        return {"warnings": warnings, "issues": issues}
    
    def _generate_summary(self, df: pd.DataFrame, validation_results: Dict) -> Dict:
        """Generar resumen de validación"""
        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "mapped_columns": len(validation_results["column_mapping"]),
            "errors_count": len(validation_results["errors"]),
            "warnings_count": len(validation_results["warnings"]),
            "estimated_load_time": self._estimate_load_time(len(df)),
            "data_quality_score": self._calculate_quality_score(validation_results)
        }
    
    def _estimate_load_time(self, row_count: int) -> str:
        """Estimar tiempo de carga"""
        # Estimación simple: ~1000 registros por segundo
        seconds = max(1, row_count // 1000)
        if seconds < 60:
            return f"~{seconds} segundos"
        else:
            minutes = seconds // 60
            return f"~{minutes} minutos"
    
    def _calculate_quality_score(self, validation_results: Dict) -> int:
        """Calcular puntuación de calidad de datos (0-100)"""
        score = 100
        
        # Penalizar errores más que warnings
        score -= len(validation_results["errors"]) * 20
        score -= len(validation_results["warnings"]) * 5
        
        # Bonificar mapeo completo de columnas
        mapping_ratio = len(validation_results["column_mapping"]) / max(1, len(self.all_columns))
        score += int(mapping_ratio * 10)
        
        return max(0, min(100, score))
