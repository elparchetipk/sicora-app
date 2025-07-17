"""
Sistema de logging para SICORA Data Loader
"""
import logging
import os
from datetime import datetime
from typing import Any
from loguru import logger
import sys

class DataLoaderLogger:
    """Sistema de logging personalizado"""
    
    def __init__(self, log_file: str = "data_loader.log"):
        """
        Inicializar sistema de logging
        
        Args:
            log_file: Archivo de log
        """
        self.log_file = log_file
        self._setup_logger()
    
    def _setup_logger(self):
        """Configurar loguru logger"""
        # Remover handler por defecto
        logger.remove()
        
        # Formato personalizado
        format_string = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        
        # Handler para consola
        logger.add(
            sys.stdout,
            format=format_string,
            level="INFO",
            colorize=True
        )
        
        # Handler para archivo
        logger.add(
            self.log_file,
            format=format_string,
            level="DEBUG",
            rotation="1 MB",
            retention="7 days",
            compression="zip"
        )
    
    def log_file_upload(self, filename: str, file_size: int, file_type: str):
        """Log de carga de archivo"""
        logger.info(f"📁 Archivo cargado: {filename} ({file_size} bytes, tipo: {file_type})")
    
    def log_validation_start(self, microservice: str, table: str, rows: int):
        """Log inicio de validación"""
        logger.info(f"🔍 Iniciando validación: {microservice}.{table} ({rows} filas)")
    
    def log_validation_result(self, is_valid: bool, errors: int, warnings: int):
        """Log resultado de validación"""
        if is_valid:
            logger.success(f"✅ Validación exitosa: {warnings} advertencias")
        else:
            logger.error(f"❌ Validación fallida: {errors} errores, {warnings} advertencias")
    
    def log_data_load_start(self, microservice: str, table: str, rows: int, mode: str):
        """Log inicio de carga de datos"""
        logger.info(f"📊 Iniciando carga: {microservice}.{table} ({rows} filas, modo: {mode})")
    
    def log_data_load_result(self, success: bool, rows_processed: int, 
                           rows_inserted: int, rows_updated: int, duration: float):
        """Log resultado de carga de datos"""
        if success:
            logger.success(
                f"🎉 Carga exitosa: {rows_processed} procesadas, "
                f"{rows_inserted} insertadas, {rows_updated} actualizadas "
                f"({duration:.2f}s)"
            )
        else:
            logger.error(f"💥 Carga fallida después de {duration:.2f}s")
    
    def log_error(self, error: Exception, context: str = ""):
        """Log de error"""
        logger.error(f"🚨 Error{' en ' + context if context else ''}: {str(error)}")
    
    def log_warning(self, message: str):
        """Log de advertencia"""
        logger.warning(f"⚠️ {message}")
    
    def log_info(self, message: str):
        """Log de información"""
        logger.info(f"ℹ️ {message}")
    
    def log_database_connection(self, success: bool, host: str, database: str):
        """Log de conexión a base de datos"""
        if success:
            logger.success(f"🔗 Conectado a {host}/{database}")
        else:
            logger.error(f"💔 Error conectando a {host}/{database}")
    
    def log_schema_info(self, schema: str, tables_count: int):
        """Log de información de schema"""
        logger.info(f"🗂️ Schema {schema}: {tables_count} tablas disponibles")
    
    def log_table_info(self, schema: str, table: str, columns: int, rows: int):
        """Log de información de tabla"""
        logger.info(f"📋 Tabla {schema}.{table}: {columns} columnas, {rows} filas")
    
    def log_user_action(self, action: str, details: str = ""):
        """Log de acción de usuario"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        logger.info(f"👤 [{timestamp}] {action}{': ' + details if details else ''}")

# Instancia global del logger
data_logger = DataLoaderLogger()
