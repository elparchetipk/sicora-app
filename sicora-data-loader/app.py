"""
SICORA Data Loader - Aplicación Principal
Mini-aplicación para cargar datos desde Excel/PDF a PostgreSQL
"""
import streamlit as st
import pandas as pd
from io import BytesIO
import time
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="SICORA Data Loader",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports locales
from config.database import db_config
from models.schemas import SchemaMapping
from services.file_processor import FileProcessor
from services.data_validator import DataValidator
from services.database_loader import DatabaseLoader
from utils.logger import data_logger

def main():
    """Función principal de la aplicación"""
    
    # Header
    st.title("🚀 SICORA Data Loader")
    st.markdown("**Mini-aplicación para cargar datos desde Excel/PDF a la base de datos SICORA**")
    
    # Sidebar - Configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Test de conexión
        if st.button("🔗 Probar Conexión"):
            test_database_connection()
        
        st.divider()
        
        # Información de la base de datos
        show_database_info()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Cargar Archivo", 
        "🔍 Validar Datos", 
        "📊 Cargar a DB", 
        "📋 Historial"
    ])
    
    with tab1:
        file_upload_tab()
    
    with tab2:
        data_validation_tab()
    
    with tab3:
        database_load_tab()
    
    with tab4:
        history_tab()

def test_database_connection():
    """Probar conexión a la base de datos"""
    with st.spinner("Probando conexión..."):
        success = db_config.test_connection()
        
        if success:
            st.success("✅ Conexión exitosa a PostgreSQL")
            db_info = db_config.get_database_info()
            
            if "error" not in db_info:
                st.info(f"📊 **Base de datos:** {db_info['database']}")
                st.info(f"🏠 **Host:** {db_info['host']}:{db_info['port']}")
                st.info(f"📋 **Schemas encontrados:** {len(db_info['schemas'])}")
                
                data_logger.log_database_connection(True, db_info['host'], db_info['database'])
            else:
                st.error(f"Error obteniendo info de DB: {db_info['error']}")
        else:
            st.error("❌ Error de conexión a la base de datos")
            data_logger.log_database_connection(False, db_config.host, db_config.database)

def show_database_info():
    """Mostrar información de la base de datos"""
    if db_config.test_connection():
        db_info = db_config.get_database_info()
        
        if "error" not in db_info:
            st.success("🟢 DB Conectada")
            st.caption(f"📊 {db_info['database']} ({len(db_info['schemas'])} schemas)")
        else:
            st.error("🔴 Error en DB")
            st.caption(db_info['error'])
    else:
        st.error("🔴 DB Desconectada")
        st.caption("Verificar configuración")

def file_upload_tab():
    """Tab para carga de archivos"""
    st.header("📁 Cargar Archivo de Datos")
    
    # Selección de microservicio
    col1, col2 = st.columns(2)
    
    with col1:
        microservices = SchemaMapping.get_microservices_list()
        selected_microservice = st.selectbox(
            "🎯 Seleccionar Microservicio",
            microservices,
            help="Selecciona el microservicio donde cargar los datos"
        )
        
        if selected_microservice:
            description = SchemaMapping.get_description(selected_microservice)
            st.info(f"📋 **Descripción:** {description}")
    
    with col2:
        if selected_microservice:
            schema_name = SchemaMapping.get_schema_for_microservice(selected_microservice)
            available_tables = db_config.get_schema_tables(schema_name)
            expected_tables = SchemaMapping.get_expected_tables(selected_microservice)
            
            # Mostrar tablas disponibles y esperadas
            all_tables = list(set(available_tables + expected_tables))
            
            selected_table = st.selectbox(
                "📊 Seleccionar Tabla",
                all_tables if all_tables else ["No hay tablas disponibles"],
                help="Selecciona la tabla donde cargar los datos"
            )
            
            if selected_table in available_tables:
                st.success("✅ Tabla existe en la base de datos")
            elif selected_table in expected_tables:
                st.warning("⚠️ Tabla esperada pero no encontrada en DB")
    
    # Upload de archivo
    st.divider()
    uploaded_file = st.file_uploader(
        "📤 Subir Archivo",
        type=['xlsx', 'xls', 'pdf'],
        help="Soporta archivos Excel (.xlsx, .xls) y PDF"
    )
    
    if uploaded_file and selected_microservice and selected_table:
        process_uploaded_file(uploaded_file, selected_microservice, selected_table)

def process_uploaded_file(uploaded_file, microservice, table):
    """Procesar archivo cargado"""
    try:
        # Log de carga de archivo
        file_size = len(uploaded_file.getvalue())
        file_type = uploaded_file.type
        data_logger.log_file_upload(uploaded_file.name, file_size, file_type)
        
        st.success(f"✅ Archivo cargado: **{uploaded_file.name}** ({file_size:,} bytes)")
        
        # Procesar según tipo de archivo
        if uploaded_file.name.endswith(('.xlsx', '.xls')):
            process_excel_file(uploaded_file, microservice, table)
        elif uploaded_file.name.endswith('.pdf'):
            process_pdf_file(uploaded_file, microservice, table)
        
    except Exception as e:
        st.error(f"❌ Error procesando archivo: {str(e)}")
        data_logger.log_error(e, "procesamiento de archivo")

def process_excel_file(uploaded_file, microservice, table):
    """Procesar archivo Excel"""
    try:
        file_content = BytesIO(uploaded_file.getvalue())
        
        # Verificar hojas disponibles
        sheets = FileProcessor.get_excel_sheets(file_content)
        
        if len(sheets) > 1:
            selected_sheet = st.selectbox("📋 Seleccionar Hoja", sheets)
        else:
            selected_sheet = sheets[0] if sheets else None
        
        if selected_sheet:
            # Procesar Excel
            with st.spinner("Procesando archivo Excel..."):
                df = FileProcessor.process_excel(file_content, selected_sheet)
            
            # Guardar en session state
            st.session_state['uploaded_data'] = df
            st.session_state['microservice'] = microservice
            st.session_state['table'] = table
            st.session_state['file_name'] = uploaded_file.name
            
            # Mostrar vista previa
            show_data_preview(df)
            
            data_logger.log_info(f"Excel procesado: {len(df)} filas, {len(df.columns)} columnas")
    
    except Exception as e:
        st.error(f"❌ Error procesando Excel: {str(e)}")
        data_logger.log_error(e, "procesamiento de Excel")

def process_pdf_file(uploaded_file, microservice, table):
    """Procesar archivo PDF"""
    try:
        file_content = BytesIO(uploaded_file.getvalue())
        
        with st.spinner("Extrayendo tablas del PDF..."):
            tables = FileProcessor.process_pdf_tables(file_content)
        
        if tables:
            if len(tables) > 1:
                st.info(f"📋 Se encontraron {len(tables)} tablas en el PDF")
                selected_table_idx = st.selectbox(
                    "Seleccionar Tabla", 
                    range(len(tables)),
                    format_func=lambda x: f"Tabla {x+1} ({tables[x].shape[0]} filas, {tables[x].shape[1]} columnas)"
                )
                df = tables[selected_table_idx]
            else:
                df = tables[0]
            
            # Guardar en session state
            st.session_state['uploaded_data'] = df
            st.session_state['microservice'] = microservice
            st.session_state['table'] = table
            st.session_state['file_name'] = uploaded_file.name
            
            # Mostrar vista previa
            show_data_preview(df)
            
            data_logger.log_info(f"PDF procesado: {len(df)} filas, {len(df.columns)} columnas")
        else:
            st.warning("⚠️ No se encontraron tablas en el PDF")
    
    except Exception as e:
        st.error(f"❌ Error procesando PDF: {str(e)}")
        data_logger.log_error(e, "procesamiento de PDF")

def show_data_preview(df):
    """Mostrar vista previa de los datos"""
    st.subheader("👀 Vista Previa de Datos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Filas", len(df))
    with col2:
        st.metric("📋 Columnas", len(df.columns))
    with col3:
        st.metric("💾 Memoria", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # Mostrar datos
    st.dataframe(df.head(10), use_container_width=True)
    
    # Información de tipos
    with st.expander("🔍 Información de Columnas"):
        col_info = FileProcessor.detect_data_types(df)
        for col, dtype in col_info.items():
            st.text(f"📋 {col}: {dtype}")

def data_validation_tab():
    """Tab para validación de datos"""
    st.header("🔍 Validar Datos")
    
    if 'uploaded_data' not in st.session_state:
        st.info("📁 Primero carga un archivo en la pestaña 'Cargar Archivo'")
        return
    
    df = st.session_state['uploaded_data']
    microservice = st.session_state['microservice']
    table = st.session_state['table']
    
    st.info(f"🎯 **Microservicio:** {microservice} | **Tabla:** {table}")
    
    # Obtener información de la tabla
    schema_name = SchemaMapping.get_schema_for_microservice(microservice)
    table_columns = db_config.get_table_columns(schema_name, table)
    
    if not table_columns:
        st.error(f"❌ No se pudo obtener información de la tabla {schema_name}.{table}")
        return
    
    # Ejecutar validación
    if st.button("🔍 Ejecutar Validación", type="primary"):
        with st.spinner("Validando datos..."):
            data_logger.log_validation_start(microservice, table, len(df))
            
            validator = DataValidator(table_columns)
            validation_result = validator.validate_dataframe(df)
            
            # Guardar resultado en session state
            st.session_state['validation_result'] = validation_result
            
            data_logger.log_validation_result(
                validation_result['is_valid'],
                len(validation_result['errors']),
                len(validation_result['warnings'])
            )
    
    # Mostrar resultados de validación
    if 'validation_result' in st.session_state:
        show_validation_results(st.session_state['validation_result'])

def show_validation_results(validation_result):
    """Mostrar resultados de validación"""
    st.subheader("📊 Resultados de Validación")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = validation_result['summary']['data_quality_score']
        st.metric("🎯 Calidad", f"{score}%", delta=None)
    
    with col2:
        errors = validation_result['summary']['errors_count']
        st.metric("❌ Errores", errors)
    
    with col3:
        warnings = validation_result['summary']['warnings_count']
        st.metric("⚠️ Advertencias", warnings)
    
    with col4:
        mapped = validation_result['summary']['mapped_columns']
        st.metric("📋 Columnas Mapeadas", mapped)
    
    # Estado general
    if validation_result['is_valid']:
        st.success("✅ Validación Exitosa - Los datos están listos para cargar")
    else:
        st.error("❌ Validación Fallida - Corrige los errores antes de continuar")
    
    # Detalles de errores
    if validation_result['errors']:
        st.subheader("❌ Errores Encontrados")
        for error in validation_result['errors']:
            st.error(error)
    
    # Detalles de advertencias
    if validation_result['warnings']:
        st.subheader("⚠️ Advertencias")
        for warning in validation_result['warnings']:
            st.warning(warning)
    
    # Mapeo de columnas
    if validation_result['column_mapping']:
        st.subheader("📋 Mapeo de Columnas")
        mapping_df = pd.DataFrame([
            {"Columna Archivo": k, "Columna Tabla": v}
            for k, v in validation_result['column_mapping'].items()
        ])
        st.dataframe(mapping_df, use_container_width=True)
    
    # Resumen
    with st.expander("📊 Resumen Detallado"):
        summary = validation_result['summary']
        st.json(summary)

def database_load_tab():
    """Tab para carga a base de datos"""
    st.header("📊 Cargar Datos a Base de Datos")
    
    # Verificar prerrequisitos
    if 'uploaded_data' not in st.session_state:
        st.info("📁 Primero carga un archivo en la pestaña 'Cargar Archivo'")
        return
    
    if 'validation_result' not in st.session_state:
        st.info("🔍 Primero valida los datos en la pestaña 'Validar Datos'")
        return
    
    validation_result = st.session_state['validation_result']
    
    if not validation_result['is_valid']:
        st.error("❌ Los datos no han pasado la validación. Corrige los errores primero.")
        return
    
    # Configuración de carga
    st.subheader("⚙️ Configuración de Carga")
    
    col1, col2 = st.columns(2)
    
    with col1:
        load_mode = st.selectbox(
            "🔄 Modo de Carga",
            ["insert", "upsert", "replace"],
            format_func=lambda x: {
                "insert": "Insertar (solo nuevos registros)",
                "upsert": "Insertar/Actualizar (upsert)",
                "replace": "Reemplazar (eliminar y insertar)"
            }[x],
            help="Selecciona cómo manejar los datos existentes"
        )
    
    with col2:
        confirm_load = st.checkbox(
            "✅ Confirmo que quiero cargar los datos",
            help="Marca esta casilla para habilitar la carga"
        )
    
    # Información de la carga
    df = st.session_state['uploaded_data']
    microservice = st.session_state['microservice']
    table = st.session_state['table']
    
    st.info(f"🎯 **Destino:** {microservice}.{table} | **Registros:** {len(df)} | **Modo:** {load_mode}")
    
    # Estimación de tiempo
    estimated_time = validation_result['summary']['estimated_load_time']
    st.info(f"⏱️ **Tiempo estimado:** {estimated_time}")
    
    # Botón de carga
    if st.button("🚀 Cargar Datos", type="primary", disabled=not confirm_load):
        execute_data_load(df, microservice, table, validation_result['column_mapping'], load_mode)

def execute_data_load(df, microservice, table, column_mapping, mode):
    """Ejecutar carga de datos"""
    try:
        schema_name = SchemaMapping.get_schema_for_microservice(microservice)
        
        # Log inicio
        data_logger.log_data_load_start(microservice, table, len(df), mode)
        
        # Crear loader
        loader = DatabaseLoader(schema_name, table)
        
        # Ejecutar carga con medición de tiempo
        start_time = time.time()
        
        with st.spinner(f"Cargando {len(df)} registros en modo {mode}..."):
            result = loader.load_data(df, column_mapping, mode)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Mostrar resultados
        if result['success']:
            st.success("🎉 ¡Carga de datos exitosa!")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Procesados", result['rows_processed'])
            with col2:
                st.metric("➕ Insertados", result['rows_inserted'])
            with col3:
                st.metric("🔄 Actualizados", result['rows_updated'])
            with col4:
                st.metric("⏱️ Tiempo", f"{duration:.1f}s")
            
            st.info(f"💬 {result['message']}")
            
            # Log resultado exitoso
            data_logger.log_data_load_result(
                True, result['rows_processed'], 
                result['rows_inserted'], result['rows_updated'], 
                duration
            )
            
            # Guardar en historial
            save_to_history(microservice, table, result, duration)
            
        else:
            st.error(f"❌ Error en la carga: {result['error']}")
            data_logger.log_data_load_result(False, 0, 0, 0, duration)
    
    except Exception as e:
        st.error(f"💥 Error inesperado: {str(e)}")
        data_logger.log_error(e, "carga de datos")

def save_to_history(microservice, table, result, duration):
    """Guardar operación en historial"""
    if 'load_history' not in st.session_state:
        st.session_state['load_history'] = []
    
    history_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "microservice": microservice,
        "table": table,
        "file_name": st.session_state.get('file_name', 'Unknown'),
        "rows_processed": result['rows_processed'],
        "rows_inserted": result['rows_inserted'],
        "rows_updated": result['rows_updated'],
        "duration": duration,
        "success": result['success']
    }
    
    st.session_state['load_history'].insert(0, history_entry)

def history_tab():
    """Tab para historial de cargas"""
    st.header("📋 Historial de Cargas")
    
    if 'load_history' not in st.session_state or not st.session_state['load_history']:
        st.info("📊 No hay cargas registradas aún")
        return
    
    history = st.session_state['load_history']
    
    # Convertir a DataFrame
    history_df = pd.DataFrame(history)
    
    # Métricas generales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_loads = len(history_df)
        st.metric("📊 Total Cargas", total_loads)
    
    with col2:
        successful_loads = len(history_df[history_df['success']])
        st.metric("✅ Exitosas", successful_loads)
    
    with col3:
        total_rows = history_df['rows_processed'].sum()
        st.metric("📋 Total Filas", f"{total_rows:,}")
    
    with col4:
        avg_duration = history_df['duration'].mean()
        st.metric("⏱️ Tiempo Promedio", f"{avg_duration:.1f}s")
    
    # Tabla de historial
    st.subheader("📊 Detalle de Cargas")
    
    # Formatear DataFrame para mostrar
    display_df = history_df.copy()
    display_df['Status'] = display_df['success'].apply(lambda x: "✅ Exitosa" if x else "❌ Fallida")
    display_df['Duración'] = display_df['duration'].apply(lambda x: f"{x:.1f}s")
    
    columns_to_show = [
        'timestamp', 'microservice', 'table', 'file_name',
        'rows_processed', 'rows_inserted', 'rows_updated', 
        'Duración', 'Status'
    ]
    
    st.dataframe(
        display_df[columns_to_show],
        use_container_width=True,
        hide_index=True
    )
    
    # Opción para limpiar historial
    if st.button("🗑️ Limpiar Historial"):
        st.session_state['load_history'] = []
        st.rerun()

if __name__ == "__main__":
    main()
