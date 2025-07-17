"""
Configuración de base de datos para SICORA Data Loader
"""
import os
from typing import Dict, List
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DatabaseConfig:
    """Configuración de conexión a PostgreSQL SICORA"""
    
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.database = os.getenv("DB_NAME", "sicora_dev")
        self.username = os.getenv("DB_USER", "sicora_user")
        self.password = os.getenv("DB_PASSWORD", "sicora_password")
        
        # URL de conexión para SQLAlchemy
        self.database_url = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_engine(self) -> Engine:
        """Crear engine de SQLAlchemy"""
        return create_engine(self.database_url, echo=False)
    
    def get_connection(self):
        """Obtener conexión directa a PostgreSQL"""
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.username,
            password=self.password
        )
    
    def test_connection(self) -> bool:
        """Probar conexión a la base de datos"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    return True
        except Exception:
            return False
    
    def get_database_info(self) -> Dict:
        """Obtener información de la base de datos"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Versión de PostgreSQL
                    cursor.execute("SELECT version()")
                    version = cursor.fetchone()[0]
                    
                    # Schemas disponibles
                    cursor.execute("""
                        SELECT schema_name 
                        FROM information_schema.schemata 
                        WHERE schema_name LIKE '%service%_schema'
                        ORDER BY schema_name
                    """)
                    schemas = [row[0] for row in cursor.fetchall()]
                    
                    return {
                        "version": version,
                        "schemas": schemas,
                        "host": self.host,
                        "port": self.port,
                        "database": self.database
                    }
        except Exception as e:
            return {"error": str(e)}
    
    def get_schema_tables(self, schema_name: str) -> List[str]:
        """Obtener tablas de un schema específico"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = %s 
                        AND table_type = 'BASE TABLE'
                        ORDER BY table_name
                    """, (schema_name,))
                    return [row[0] for row in cursor.fetchall()]
        except Exception:
            return []
    
    def get_table_columns(self, schema_name: str, table_name: str) -> List[Dict]:
        """Obtener información de columnas de una tabla"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            column_name,
                            data_type,
                            is_nullable,
                            column_default
                        FROM information_schema.columns 
                        WHERE table_schema = %s 
                        AND table_name = %s
                        ORDER BY ordinal_position
                    """, (schema_name, table_name))
                    
                    columns = []
                    for row in cursor.fetchall():
                        columns.append({
                            "name": row[0],
                            "type": row[1],
                            "nullable": row[2] == "YES",
                            "default": row[3]
                        })
                    return columns
        except Exception:
            return []

# Instancia global de configuración
db_config = DatabaseConfig()
