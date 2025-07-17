# Makefile para SoftwareFactoryService Migrations
# Manejo de migraciones de base de datos usando Alembic

.PHONY: help install clean migrate migrate-auto migrate-history migrate-current migrate-down migrate-reset test-connection

# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
ALEMBIC = $(VENV_DIR)/bin/alembic

# Help
help: ## Mostrar ayuda
	@echo "SoftwareFactoryService Migrations - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Ejemplos de uso:"
	@echo "  make install          # Instalar dependencias"
	@echo "  make migrate          # Ejecutar migraciones"
	@echo "  make migrate-auto     # Crear migración automática"
	@echo "  make migrate-history  # Ver historial de migraciones"

# Instalación
install: ## Instalar dependencias en entorno virtual
	@echo "🔧 Instalando dependencias para SoftwareFactoryService migrations..."
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencias instaladas"

# Limpieza
clean: ## Limpiar entorno virtual
	@echo "🧹 Limpiando entorno virtual..."
	rm -rf $(VENV_DIR)
	@echo "✅ Entorno virtual eliminado"

# Verificar conexión
test-connection: ## Verificar conexión a la base de datos
	@echo "🔌 Verificando conexión a la base de datos..."
	$(PYTHON) -c "import psycopg2; import os; \
		conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
		print('✅ Conexión exitosa'); conn.close()"

# Migraciones
migrate: ## Ejecutar todas las migraciones pendientes
	@echo "📦 Ejecutando migraciones para SoftwareFactoryService..."
	$(ALEMBIC) upgrade head
	@echo "✅ Migraciones completadas"

migrate-auto: ## Crear migración automática (requiere MESSAGE)
	@if [ -z "$(MESSAGE)" ]; then \
		echo "❌ Error: Especifica un mensaje para la migración"; \
		echo "   Uso: make migrate-auto MESSAGE='descripción de la migración'"; \
		exit 1; \
	fi
	@echo "📝 Creando migración automática: $(MESSAGE)"
	$(ALEMBIC) revision --autogenerate -m "$(MESSAGE)"
	@echo "✅ Migración creada"

migrate-manual: ## Crear migración manual (requiere MESSAGE)
	@if [ -z "$(MESSAGE)" ]; then \
		echo "❌ Error: Especifica un mensaje para la migración"; \
		echo "   Uso: make migrate-manual MESSAGE='descripción de la migración'"; \
		exit 1; \
	fi
	@echo "📝 Creando migración manual: $(MESSAGE)"
	$(ALEMBIC) revision -m "$(MESSAGE)"
	@echo "✅ Migración creada"

migrate-history: ## Ver historial de migraciones
	@echo "📋 Historial de migraciones:"
	$(ALEMBIC) history --verbose

migrate-current: ## Ver migración actual
	@echo "📍 Migración actual:"
	$(ALEMBIC) current --verbose

migrate-down: ## Revertir última migración
	@echo "⬇️ Revirtiendo última migración..."
	$(ALEMBIC) downgrade -1
	@echo "✅ Migración revertida"

migrate-reset: ## Resetear todas las migraciones (¡PELIGROSO!)
	@echo "⚠️ ADVERTENCIA: Esto eliminará todas las tablas del esquema softwarefactoryservice_schema"
	@echo "¿Estás seguro? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo "🔄 Reseteando migraciones..."
	$(ALEMBIC) downgrade base
	$(ALEMBIC) upgrade head
	@echo "✅ Migraciones reseteadas"

# Validación
validate-schema: ## Validar que el esquema coincida con las entidades Go
	@echo "🔍 Validando esquema de base de datos..."
	@echo "ℹ️ Verificar manualmente que las tablas coincidan con las entidades Go en:"
	@echo "   sicora-be-go/softwarefactoryservice/internal/domain/entities/"
	$(ALEMBIC) current --verbose

# Información
info: ## Mostrar información del entorno
	@echo "📊 Información de SoftwareFactoryService Migrations:"
	@echo "   Esquema: softwarefactoryservice_schema"
	@echo "   Base de datos: sicora_db"
	@echo "   Usuario: softwarefactoryservice_user"
	@echo "   Tabla de versiones: alembic_version_softwarefactoryservice"
	@echo ""
	@echo "🔗 Integración:"
	@echo "   Microservicio Go: sicora-be-go/softwarefactoryservice"
	@echo "   Inicialización DB: sicora-be-python/database/init/01_init_db_users_schemas.sql"

# Desarrollo
dev-setup: install test-connection ## Configuración completa para desarrollo
	@echo "🚀 Configurando entorno de desarrollo..."
	@echo "✅ Entorno listo para desarrollo"

# Producción
prod-migrate: ## Ejecutar migraciones en producción (con validaciones)
	@echo "🏭 Ejecutando migraciones en modo producción..."
	@echo "⚠️ Validando entorno de producción..."
	@if [ -z "$(DATABASE_URL)" ]; then \
		echo "❌ Error: DATABASE_URL no está configurada"; \
		exit 1; \
	fi
	$(ALEMBIC) upgrade head
	@echo "✅ Migraciones de producción completadas"

# Performance y Analytics
refresh-analytics: ## Refrescar vistas materializadas para analytics
	@echo "📊 Refrescando vistas de analytics..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	cur = conn.cursor(); \
	cur.execute('SET search_path = softwarefactoryservice_schema, public'); \
	cur.execute('SELECT refresh_softwarefactory_analytics()'); \
	conn.commit(); conn.close(); print('✅ Analytics refrescadas')"

analyze-performance: ## Analizar rendimiento de base de datos e índices
	@echo "🔍 Analizando rendimiento de base de datos..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	cur = conn.cursor(); \
	cur.execute(\"\"\"SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch \
	FROM pg_stat_user_indexes \
	WHERE schemaname = 'softwarefactoryservice_schema' \
	ORDER BY idx_scan DESC LIMIT 20\"\"\"); \
	print('📈 Top 20 índices más utilizados:'); \
	for row in cur.fetchall(): print(f'  {row[2]}: {row[3]} scans'); \
	conn.close()"

check-indexes: ## Verificar estadísticas de uso de índices
	@echo "📈 Verificando uso de índices..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	cur = conn.cursor(); \
	cur.execute(\"\"\"SELECT schemaname, tablename, indexname, idx_scan \
	FROM pg_stat_user_indexes \
	WHERE schemaname = 'softwarefactoryservice_schema' AND idx_scan = 0\"\"\"); \
	unused = cur.fetchall(); \
	if unused: \
		print('⚠️ Índices sin uso encontrados:'); \
		[print(f'  {row[2]}') for row in unused]; \
	else: \
		print('✅ Todos los índices están siendo utilizados'); \
	conn.close()"

analyze-queries: ## Analizar consultas lentas y estadísticas
	@echo "🐌 Analizando consultas lentas..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	cur = conn.cursor(); \
	cur.execute(\"\"\"SELECT query, calls, total_time, mean_time, rows \
	FROM pg_stat_statements \
	WHERE query LIKE '%factory_%' \
	ORDER BY mean_time DESC LIMIT 10\"\"\"); \
	print('🔍 Top 10 consultas más lentas:'); \
	for row in cur.fetchall(): \
		print(f'  Tiempo promedio: {row[3]:.2f}ms - Llamadas: {row[1]}'); \
		print(f'    Query: {row[0][:100]}...'); \
	conn.close()" || echo "ℹ️ pg_stat_statements no disponible"

# Schema y Permisos
setup-schema: ## Configurar esquema y permisos de base de datos
	@echo "🔧 Configurando esquema SoftwareFactoryService..."
	$(PYTHON) -c "import psycopg2; import os; \
	admin_url = os.getenv('ADMIN_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/sicora_db'); \
	conn = psycopg2.connect(admin_url); \
	conn.autocommit = True; \
	cur = conn.cursor(); \
	try: \
		cur.execute('CREATE SCHEMA IF NOT EXISTS softwarefactoryservice_schema'); \
		print('✅ Schema creado/verificado'); \
		cur.execute('CREATE USER softwarefactoryservice_user WITH PASSWORD \\'softwarefactoryservice_password_placeholder\\''); \
		print('✅ Usuario creado'); \
	except psycopg2.errors.DuplicateObject: \
		print('ℹ️ Usuario ya existe'); \
	cur.execute('ALTER SCHEMA softwarefactoryservice_schema OWNER TO softwarefactoryservice_user'); \
	cur.execute('GRANT ALL ON SCHEMA softwarefactoryservice_schema TO softwarefactoryservice_user'); \
	cur.execute('GRANT USAGE ON SCHEMA public TO softwarefactoryservice_user'); \
	cur.execute('ALTER ROLE softwarefactoryservice_user SET search_path = softwarefactoryservice_schema, public'); \
	conn.close(); print('✅ Configuración de esquema completada')"

verify-permissions: ## Verificar permisos del usuario de base de datos
	@echo "🔐 Verificando permisos..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	cur = conn.cursor(); \
	cur.execute('SELECT current_schema(), current_user, session_user'); \
	schema, current, session = cur.fetchone(); \
	print(f'✅ Schema actual: {schema}'); \
	print(f'✅ Usuario actual: {current}'); \
	print(f'✅ Usuario de sesión: {session}'); \
	cur.execute('SHOW search_path'); \
	search_path = cur.fetchone()[0]; \
	print(f'✅ Search path: {search_path}'); \
	conn.close()"

# Monitoreo y Mantenimiento
analyze-indexes: ## Analizar uso y rendimiento de índices
	@echo "📊 Analizando rendimiento de índices..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	cur = conn.cursor(); \
	print('=== ÍNDICES MÁS UTILIZADOS ==='); \
	cur.execute('SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch FROM pg_stat_user_indexes WHERE schemaname = %s ORDER BY idx_tup_read DESC LIMIT 10', ('softwarefactoryservice_schema',)); \
	for row in cur.fetchall(): print(f'{row[0]}.{row[1]}.{row[2]}: reads={row[3]}, fetches={row[4]}'); \
	print('\\n=== TAMAÑO DE ÍNDICES ==='); \
	cur.execute('SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass)) as size FROM pg_indexes WHERE schemaname = %s ORDER BY pg_relation_size(indexname::regclass) DESC LIMIT 10', ('softwarefactoryservice_schema',)); \
	for row in cur.fetchall(): print(f'{row[0]}: {row[1]}'); \
	conn.close()"

apply-user-story-indexes: ## Aplicar índices optimizados basados en historias de usuario
	@echo "🚀 Aplicando índices optimizados para historias de usuario..."
	$(PYTHON) -m alembic upgrade 004_user_stories_optimized_indexes
	@echo "✅ Índices de historias de usuario aplicados"

analyze-user-story-performance: ## Analizar rendimiento específico de consultas de historias de usuario
	@echo "📈 Analizando rendimiento de consultas de historias de usuario..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	cur = conn.cursor(); \
	print('=== ÍNDICES DE USER STORIES ==='); \
	cur.execute(\"SELECT indexname, idx_tup_read, idx_tup_fetch FROM pg_stat_user_indexes WHERE tablename = 'factory_user_stories' AND schemaname = 'softwarefactoryservice_schema' ORDER BY idx_tup_read DESC\"); \
	for row in cur.fetchall(): print(f'{row[0]}: reads={row[1]}, fetches={row[2]}'); \
	print('\\n=== CONSULTAS MÁS LENTAS (USER STORIES) ==='); \
	cur.execute(\"SELECT query, mean_time, calls FROM pg_stat_statements WHERE query LIKE '%factory_user_stories%' ORDER BY mean_time DESC LIMIT 5\"); \
	for row in cur.fetchall(): print(f'Query: {row[0][:80]}... | Tiempo medio: {row[1]:.2f}ms | Llamadas: {row[2]}'); \
	conn.close()"

validate-index-usage: ## Validar que los índices críticos están siendo utilizados
	@echo "✅ Validando uso de índices críticos..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	cur = conn.cursor(); \
	critical_indexes = ['idx_factory_user_stories_backlog_management', 'idx_factory_user_stories_personal_tasks', 'idx_factory_projects_instructor_dashboard']; \
	print('=== VALIDACIÓN DE ÍNDICES CRÍTICOS ==='); \
	for idx in critical_indexes: \
	    cur.execute('SELECT idx_tup_read, idx_tup_fetch FROM pg_stat_user_indexes WHERE indexname = %s', (idx,)); \
	    result = cur.fetchone(); \
	    if result: print(f'✅ {idx}: reads={result[0]}, fetches={result[1]}'); \
	    else: print(f'❌ {idx}: NO ENCONTRADO'); \
	conn.close()"

vacuum-analyze: ## Ejecutar VACUUM ANALYZE en todas las tablas
	@echo "🧹 Ejecutando VACUUM ANALYZE..."
	$(PYTHON) -c "import psycopg2; import os; \
	conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://softwarefactoryservice_user:softwarefactoryservice_password_placeholder@localhost:5432/sicora_db')); \
	conn.autocommit = True; \
	cur = conn.cursor(); \
	cur.execute('SET search_path = softwarefactoryservice_schema, public'); \
	tables = ['factory_projects', 'factory_teams', 'factory_team_members', 'factory_sprints', 'factory_user_stories', 'factory_evaluations', 'factory_technologies', 'factory_improvement_plans']; \
	for table in tables: \
		try: \
			cur.execute(f'VACUUM ANALYZE {table}'); \
			print(f'✅ {table} optimizada'); \
		except Exception as e: \
			print(f'⚠️ Error en {table}: {e}'); \
	conn.close()"

# Default target
.DEFAULT_GOAL := help
