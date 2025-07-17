"""
Cargador de datos a la base de datos
"""
import pandas as pd
from typing import Dict, List, Any, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import psycopg2
from psycopg2.extras import execute_values
from config.database import db_config

class DatabaseLoader:
    """Cargador de datos a PostgreSQL"""
    
    def __init__(self, schema_name: str, table_name: str):
        """
        Inicializar cargador para una tabla específica
        
        Args:
            schema_name: Nombre del schema
            table_name: Nombre de la tabla
        """
        self.schema_name = schema_name
        self.table_name = table_name
        self.full_table_name = f'"{schema_name}"."{table_name}"'
        self.engine = db_config.get_engine()
    
    def load_data(self, df: pd.DataFrame, column_mapping: Dict[str, str], 
                  mode: str = "insert") -> Dict[str, Any]:
        """
        Cargar datos del DataFrame a la base de datos
        
        Args:
            df: DataFrame con los datos
            column_mapping: Mapeo de columnas DataFrame -> Tabla
            mode: Modo de carga ("insert", "upsert", "replace")
            
        Returns:
            Diccionario con resultados de la carga
        """
        try:
            # Preparar datos
            prepared_df = self._prepare_dataframe(df, column_mapping)
            
            # Ejecutar carga según el modo
            if mode == "insert":
                result = self._insert_data(prepared_df)
            elif mode == "upsert":
                result = self._upsert_data(prepared_df)
            elif mode == "replace":
                result = self._replace_data(prepared_df)
            else:
                raise ValueError(f"Modo de carga no soportado: {mode}")
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "rows_processed": 0,
                "rows_inserted": 0,
                "rows_updated": 0
            }
    
    def _prepare_dataframe(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """Preparar DataFrame para la carga"""
        # Crear copia del DataFrame
        prepared_df = df.copy()
        
        # Renombrar columnas según el mapeo
        reverse_mapping = {v: k for k, v in column_mapping.items()}
        prepared_df = prepared_df.rename(columns=reverse_mapping)
        
        # Seleccionar solo las columnas mapeadas
        mapped_columns = list(column_mapping.values())
        prepared_df = prepared_df[mapped_columns]
        
        # Limpiar datos
        prepared_df = self._clean_data(prepared_df)
        
        return prepared_df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar y preparar datos"""
        cleaned_df = df.copy()
        
        # Convertir fechas
        date_columns = ["created_at", "updated_at", "date", "start_date", "end_date"]
        for col in date_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
        
        # Limpiar strings
        string_columns = cleaned_df.select_dtypes(include=['object']).columns
        for col in string_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
                # Reemplazar 'nan' string con None
                cleaned_df[col] = cleaned_df[col].replace('nan', None)
        
        # Convertir números
        numeric_columns = ["id", "user_id", "group_id", "category_id"]
        for col in numeric_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
        
        return cleaned_df
    
    def _insert_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Insertar datos (solo INSERT)"""
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    # Usar pandas to_sql para inserción
                    df.to_sql(
                        name=self.table_name,
                        con=conn,
                        schema=self.schema_name,
                        if_exists='append',
                        index=False,
                        method='multi'
                    )
                    
                    rows_inserted = len(df)
                    
                    return {
                        "success": True,
                        "rows_processed": len(df),
                        "rows_inserted": rows_inserted,
                        "rows_updated": 0,
                        "message": f"Insertados {rows_inserted} registros exitosamente"
                    }
                    
        except Exception as e:
            raise Exception(f"Error en inserción: {str(e)}")
    
    def _upsert_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Insertar o actualizar datos (UPSERT)"""
        # Para implementar UPSERT necesitamos conocer la clave primaria
        # Por simplicidad, asumimos que existe una columna 'id'
        
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    rows_inserted = 0
                    rows_updated = 0
                    
                    for _, row in df.iterrows():
                        # Construir query de UPSERT
                        columns = list(row.index)
                        values = [row[col] for col in columns]
                        
                        # Si existe ID, intentar UPDATE primero
                        if 'id' in columns and pd.notna(row['id']):
                            update_query = self._build_update_query(columns, row['id'])
                            result = conn.execute(text(update_query), values[:-1])  # Excluir ID del final
                            
                            if result.rowcount > 0:
                                rows_updated += 1
                            else:
                                # Si no se actualizó, hacer INSERT
                                insert_query = self._build_insert_query(columns)
                                conn.execute(text(insert_query), values)
                                rows_inserted += 1
                        else:
                            # Sin ID, hacer INSERT directo
                            insert_query = self._build_insert_query(columns)
                            conn.execute(text(insert_query), values)
                            rows_inserted += 1
                    
                    return {
                        "success": True,
                        "rows_processed": len(df),
                        "rows_inserted": rows_inserted,
                        "rows_updated": rows_updated,
                        "message": f"Procesados {len(df)} registros: {rows_inserted} insertados, {rows_updated} actualizados"
                    }
                    
        except Exception as e:
            raise Exception(f"Error en upsert: {str(e)}")
    
    def _replace_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Reemplazar datos (DELETE + INSERT)"""
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    # Eliminar datos existentes
                    delete_query = f'DELETE FROM {self.full_table_name}'
                    conn.execute(text(delete_query))
                    
                    # Insertar nuevos datos
                    df.to_sql(
                        name=self.table_name,
                        con=conn,
                        schema=self.schema_name,
                        if_exists='append',
                        index=False,
                        method='multi'
                    )
                    
                    return {
                        "success": True,
                        "rows_processed": len(df),
                        "rows_inserted": len(df),
                        "rows_updated": 0,
                        "message": f"Tabla reemplazada con {len(df)} registros"
                    }
                    
        except Exception as e:
            raise Exception(f"Error en reemplazo: {str(e)}")
    
    def _build_insert_query(self, columns: List[str]) -> str:
        """Construir query de INSERT"""
        placeholders = ', '.join([':' + col for col in columns])
        columns_str = ', '.join([f'"{col}"' for col in columns])
        
        return f'''
            INSERT INTO {self.full_table_name} ({columns_str})
            VALUES ({placeholders})
        '''
    
    def _build_update_query(self, columns: List[str], record_id: Any) -> str:
        """Construir query de UPDATE"""
        # Excluir ID de las columnas a actualizar
        update_columns = [col for col in columns if col != 'id']
        set_clause = ', '.join([f'"{col}" = :{col}' for col in update_columns])
        
        return f'''
            UPDATE {self.full_table_name}
            SET {set_clause}
            WHERE id = {record_id}
        '''
    
    def test_connection(self) -> bool:
        """Probar conexión a la base de datos"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                return True
        except:
            return False
    
    def get_table_info(self) -> Dict[str, Any]:
        """Obtener información de la tabla"""
        try:
            with self.engine.connect() as conn:
                # Obtener número de registros
                count_query = f'SELECT COUNT(*) FROM {self.full_table_name}'
                result = conn.execute(text(count_query))
                row_count = result.scalar()
                
                # Obtener información de columnas
                columns_query = f'''
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = '{self.schema_name}'
                    AND table_name = '{self.table_name}'
                    ORDER BY ordinal_position
                '''
                result = conn.execute(text(columns_query))
                columns = [{"name": row[0], "type": row[1], "nullable": row[2] == "YES"} 
                          for row in result.fetchall()]
                
                return {
                    "exists": True,
                    "row_count": row_count,
                    "columns": columns,
                    "schema": self.schema_name,
                    "table": self.table_name
                }
                
        except Exception as e:
            return {
                "exists": False,
                "error": str(e),
                "schema": self.schema_name,
                "table": self.table_name
            }
