#!/usr/bin/env python3
"""
Script de validación para archivos CSV de programas de formación SICORA
Versión: 1.0
Fecha: 3 de julio de 2025
"""

import pandas as pd
import uuid
import sys
import argparse
import requests
import json
from datetime import datetime
from pathlib import Path


class ProgramCSVValidator:
    """Validador para archivos CSV de programas de formación."""
    
    REQUIRED_FIELDS = ['id', 'name', 'code', 'type', 'duration']
    OPTIONAL_FIELDS = ['description', 'is_active', 'created_at']
    VALID_TYPES = ['TECNICO', 'TECNOLOGO', 'ESPECIALIZACION', 'COMPLEMENTARIO']
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {}
    
    def validate_file(self, file_path):
        """Valida un archivo CSV de programas de formación."""
        print(f"🔍 Validando archivo: {file_path}")
        print("=" * 50)
        
        try:
            # Leer CSV
            df = pd.read_csv(file_path)
            self.stats['total_rows'] = len(df)
            print(f"📊 Total de registros: {self.stats['total_rows']}")
            
            # Ejecutar validaciones
            self._validate_structure(df)
            self._validate_required_fields(df)
            self._validate_data_types(df)
            self._validate_business_rules(df)
            self._validate_uniqueness(df)
            
            # Mostrar resultados
            self._show_results()
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.errors.append(f"Error al leer archivo: {str(e)}")
            self._show_results()
            return False
    
    def _validate_structure(self, df):
        """Valida la estructura básica del CSV."""
        # Verificar campos obligatorios
        missing_fields = set(self.REQUIRED_FIELDS) - set(df.columns)
        if missing_fields:
            self.errors.append(f"Campos obligatorios faltantes: {', '.join(missing_fields)}")
        
        # Verificar campos desconocidos
        all_valid_fields = self.REQUIRED_FIELDS + self.OPTIONAL_FIELDS
        unknown_fields = set(df.columns) - set(all_valid_fields)
        if unknown_fields:
            self.warnings.append(f"Campos no reconocidos (serán ignorados): {', '.join(unknown_fields)}")
    
    def _validate_required_fields(self, df):
        """Valida que los campos obligatorios no estén vacíos."""
        for field in self.REQUIRED_FIELDS:
            if field in df.columns:
                null_count = df[field].isnull().sum()
                empty_count = (df[field] == '').sum() if df[field].dtype == 'object' else 0
                
                if null_count > 0 or empty_count > 0:
                    self.errors.append(f"Campo '{field}' tiene {null_count + empty_count} valores vacíos")
    
    def _validate_data_types(self, df):
        """Valida tipos de datos y formatos."""
        
        # Validar UUIDs
        if 'id' in df.columns:
            for idx, row in df.iterrows():
                try:
                    uuid.UUID(str(row['id']))
                except (ValueError, TypeError):
                    self.errors.append(f"Fila {idx+2}: ID no es un UUID válido: '{row['id']}'")
        
        # Validar tipos de programa
        if 'type' in df.columns:
            invalid_types = df[~df['type'].isin(self.VALID_TYPES)]
            if not invalid_types.empty:
                invalid_values = invalid_types['type'].unique()
                self.errors.append(f"Tipos de programa inválidos: {', '.join(invalid_values)}")
                self.errors.append(f"Valores válidos: {', '.join(self.VALID_TYPES)}")
        
        # Validar duración
        if 'duration' in df.columns:
            try:
                df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
                invalid_duration = df[(df['duration'] < 1) | (df['duration'] > 60) | df['duration'].isnull()]
                if not invalid_duration.empty:
                    self.errors.append(f"Duraciones inválidas encontradas (debe estar entre 1 y 60 meses): {len(invalid_duration)} registros")
            except Exception:
                self.errors.append("Campo 'duration' debe contener valores numéricos")
        
        # Validar booleanos
        if 'is_active' in df.columns:
            invalid_bool = df[~df['is_active'].isin([True, False, 'true', 'false', 'True', 'False', 1, 0])]
            if not invalid_bool.empty:
                self.errors.append(f"Valores inválidos en 'is_active' (usar true/false): {len(invalid_bool)} registros")
    
    def _validate_business_rules(self, df):
        """Valida reglas de negocio específicas del SENA."""
        
        if 'type' in df.columns and 'duration' in df.columns:
            try:
                df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
                
                # Tecnólogos requieren mínimo 18 meses
                tecnologo_short = df[(df['type'] == 'TECNOLOGO') & (df['duration'] < 18)]
                if not tecnologo_short.empty:
                    self.warnings.append(f"Programas TECNOLOGO con duración menor a 18 meses: {len(tecnologo_short)} registros")
                
                # Complementarios máximo 12 meses
                complementario_long = df[(df['type'] == 'COMPLEMENTARIO') & (df['duration'] > 12)]
                if not complementario_long.empty:
                    self.warnings.append(f"Programas COMPLEMENTARIO con duración mayor a 12 meses: {len(complementario_long)} registros")
                
            except Exception:
                pass  # Ya validado en _validate_data_types
        
        # Validar longitud de campos
        if 'name' in df.columns:
            short_names = df[df['name'].str.len() < 5]
            long_names = df[df['name'].str.len() > 200]
            if not short_names.empty:
                self.errors.append(f"Nombres muy cortos (mín. 5 caracteres): {len(short_names)} registros")
            if not long_names.empty:
                self.errors.append(f"Nombres muy largos (máx. 200 caracteres): {len(long_names)} registros")
        
        if 'code' in df.columns:
            short_codes = df[df['code'].str.len() < 2]
            long_codes = df[df['code'].str.len() > 20]
            if not short_codes.empty:
                self.errors.append(f"Códigos muy cortos (mín. 2 caracteres): {len(short_codes)} registros")
            if not long_codes.empty:
                self.errors.append(f"Códigos muy largos (máx. 20 caracteres): {len(long_codes)} registros")
    
    def _validate_uniqueness(self, df):
        """Valida unicidad de campos clave."""
        
        # IDs únicos
        if 'id' in df.columns:
            duplicate_ids = df[df.duplicated(['id'], keep=False)]
            if not duplicate_ids.empty:
                self.errors.append(f"IDs duplicados encontrados: {len(duplicate_ids)} registros")
        
        # Códigos únicos
        if 'code' in df.columns:
            duplicate_codes = df[df.duplicated(['code'], keep=False)]
            if not duplicate_codes.empty:
                self.errors.append(f"Códigos duplicados encontrados: {len(duplicate_codes)} registros")
                duplicate_values = duplicate_codes['code'].unique()
                self.errors.append(f"Códigos duplicados: {', '.join(duplicate_values)}")
    
    def _show_results(self):
        """Muestra los resultados de la validación."""
        print("\n" + "="*50)
        print("📊 RESULTADOS DE VALIDACIÓN")
        print("="*50)
        
        if self.stats:
            print(f"Total de registros procesados: {self.stats.get('total_rows', 0)}")
        
        if self.errors:
            print(f"\n❌ ERRORES ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        if self.warnings:
            print(f"\n⚠️  ADVERTENCIAS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ ¡ARCHIVO VÁLIDO!")
            print("El archivo está listo para ser cargado en SICORA.")
        elif not self.errors:
            print("\n✅ ARCHIVO VÁLIDO CON ADVERTENCIAS")
            print("El archivo puede ser cargado, pero revisa las advertencias.")
        else:
            print("\n❌ ARCHIVO INVÁLIDO")
            print("Corrige los errores antes de cargar el archivo.")
        
        print("\n" + "="*50)
    
    def upload_programs(self, file_path, backend_url="http://localhost:8000", backend_type="python"):
        """Carga los programas del CSV a la API."""
        print(f"\n🚀 INICIANDO CARGA A {backend_type.upper()} BACKEND")
        print(f"URL: {backend_url}")
        print("="*50)
        
        try:
            # Leer CSV
            df = pd.read_csv(file_path)
            
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Preparar payload según el backend
                    if backend_type.lower() == "python":
                        payload = self._prepare_python_payload(row)
                        endpoint = f"{backend_url}/api/v1/admin/programs"
                    else:  # Go backend
                        payload = self._prepare_go_payload(row)
                        endpoint = f"{backend_url}/api/v1/master-data/academic-programs"
                    
                    # Hacer request
                    response = requests.post(
                        endpoint,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    if response.status_code in [200, 201]:
                        success_count += 1
                        print(f"✅ Programa '{row['name']}' cargado exitosamente")
                    else:
                        error_count += 1
                        error_msg = f"Error al cargar '{row['name']}': HTTP {response.status_code}"
                        if response.text:
                            try:
                                error_detail = response.json()
                                error_msg += f" - {error_detail.get('detail', response.text)}"
                            except:
                                error_msg += f" - {response.text[:200]}"
                        errors.append(error_msg)
                        print(f"❌ {error_msg}")
                
                except requests.exceptions.RequestException as e:
                    error_count += 1
                    error_msg = f"Error de conexión al cargar '{row['name']}': {str(e)}"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                
                except Exception as e:
                    error_count += 1
                    error_msg = f"Error inesperado al cargar '{row['name']}': {str(e)}"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
            
            # Mostrar resumen
            print("\n" + "="*50)
            print("📊 RESUMEN DE CARGA")
            print("="*50)
            print(f"✅ Programas cargados exitosamente: {success_count}")
            print(f"❌ Programas con errores: {error_count}")
            print(f"📊 Total procesados: {success_count + error_count}")
            
            if errors:
                print(f"\n❌ ERRORES DETALLADOS:")
                for i, error in enumerate(errors, 1):
                    print(f"  {i}. {error}")
            
            return success_count, error_count, errors
            
        except Exception as e:
            print(f"❌ Error fatal durante la carga: {str(e)}")
            return 0, 1, [str(e)]
    
    def _prepare_python_payload(self, row):
        """Prepara el payload para el backend Python."""
        payload = {
            "name": str(row['name']),
            "code": str(row['code']),
            "program_type": str(row['type']),
            "duration_months": int(row['duration'])
        }
        
        # Campos opcionales
        if pd.notna(row.get('description')):
            payload["description"] = str(row['description'])
        
        if pd.notna(row.get('is_active')):
            payload["is_active"] = bool(row['is_active'])
        
        return payload
    
    def _prepare_go_payload(self, row):
        """Prepara el payload para el backend Go."""
        payload = {
            "name": str(row['name']),
            "code": str(row['code']),
            "type": str(row['type']),
            "duration": int(row['duration'])
        }
        
        # Campos opcionales
        if pd.notna(row.get('description')):
            payload["description"] = str(row['description'])
        
        if pd.notna(row.get('is_active')):
            payload["is_active"] = bool(row['is_active'])
        
        return payload
def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Valida y carga archivos CSV de programas de formación para SICORA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Solo validar
  python validate-programs-csv.py programas.csv
  
  # Validar y cargar a backend Python
  python validate-programs-csv.py programas.csv --upload --backend python --url http://localhost:8000
  
  # Validar y cargar a backend Go  
  python validate-programs-csv.py programas.csv --upload --backend go --url http://localhost:8080
  
Tipos de programa válidos: TECNICO, TECNOLOGO, ESPECIALIZACION, COMPLEMENTARIO
        """
    )
    
    parser.add_argument('file', help='Archivo CSV a validar')
    parser.add_argument('-v', '--verbose', action='store_true', help='Mostrar información detallada')
    parser.add_argument('--upload', action='store_true', help='Cargar programas después de validar')
    parser.add_argument('--backend', choices=['python', 'go'], default='python', 
                       help='Tipo de backend (python o go)')
    parser.add_argument('--url', default='http://localhost:8000', 
                       help='URL base del backend')
    
    args = parser.parse_args()
    
    # Verificar que el archivo existe
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ Error: El archivo '{args.file}' no existe.")
        return 1
    
    # Validar archivo
    validator = ProgramCSVValidator()
    is_valid = validator.validate_file(file_path)
    
    if not is_valid:
        print("\n❌ El archivo no pasó la validación. Corrije los errores antes de intentar la carga.")
        return 1
    
    # Si se solicita upload y el archivo es válido
    if args.upload:
        if args.backend == 'go' and args.url == 'http://localhost:8000':
            # Auto-ajustar URL para Go si no se especificó
            args.url = 'http://localhost:8080'
        
        success_count, error_count, errors = validator.upload_programs(
            file_path, 
            backend_url=args.url, 
            backend_type=args.backend
        )
        
        # Código de salida basado en el resultado de la carga
        return 0 if error_count == 0 else 1
    
    # Solo validación
    return 0


if __name__ == "__main__":
    sys.exit(main())
