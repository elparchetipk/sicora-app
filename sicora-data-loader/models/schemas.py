"""
Mapeo de microservicios y esquemas de SICORA
"""
from typing import Dict, List

class SchemaMapping:
    """Mapeo de microservicios a esquemas y tablas principales"""
    
    # Mapeo de microservicios a esquemas
    MICROSERVICE_SCHEMAS = {
        "UserService": "userservice_schema",
        "AttendanceService": "attendanceservice_schema", 
        "ScheduleService": "scheduleservice_schema",
        "KbService": "kbservice_schema",
        "EvalinService": "evalinservice_schema",
        "AIService": "aiservice_schema",
        "MEvalService": "mevalservice_schema",
        "ProjectEvalService": "projectevalservice_schema",
        "SoftwareFactoryService": "softwarefactoryservice_schema"
    }
    
    # Descripción de cada microservicio
    MICROSERVICE_DESCRIPTIONS = {
        "UserService": "Gestión de usuarios, roles y permisos",
        "AttendanceService": "Control de asistencia y justificaciones",
        "ScheduleService": "Gestión de horarios y programación",
        "KbService": "Base de conocimiento y documentación",
        "EvalinService": "Evaluaciones y cuestionarios",
        "AIService": "Servicios de inteligencia artificial",
        "MEvalService": "Evaluaciones de comités",
        "ProjectEvalService": "Evaluación de proyectos",
        "SoftwareFactoryService": "Gestión de fábrica de software"
    }
    
    # Tablas principales esperadas por microservicio
    EXPECTED_TABLES = {
        "UserService": [
            "users", "roles", "permissions", "user_roles", "sessions"
        ],
        "AttendanceService": [
            "attendance_records", "justifications", "attendance_periods"
        ],
        "ScheduleService": [
            "schedules", "groups", "venues", "schedule_assignments"
        ],
        "KbService": [
            "articles", "categories", "faqs", "feedback", "embeddings"
        ],
        "EvalinService": [
            "questions", "questionnaires", "evaluation_periods", 
            "evaluations", "responses"
        ],
        "AIService": [
            "conversations", "chat_sessions", "training_data", "model_configs"
        ],
        "MEvalService": [
            "evaluations", "committees", "committee_members", "evaluation_results"
        ],
        "ProjectEvalService": [
            "projects", "evaluations", "evaluation_criteria", "project_results"
        ],
        "SoftwareFactoryService": [
            "projects", "teams", "team_members", "repositories", "deployments"
        ]
    }
    
    # Campos comunes típicos por tipo de tabla
    COMMON_FIELDS = {
        "users": ["id", "name", "email", "document_number", "created_at"],
        "attendance_records": ["id", "user_id", "date", "check_in", "check_out"],
        "schedules": ["id", "group_id", "venue_id", "start_time", "end_time"],
        "articles": ["id", "title", "content", "category_id", "created_at"],
        "questions": ["id", "text", "type", "options", "questionnaire_id"],
        "projects": ["id", "name", "description", "start_date", "status"]
    }
    
    @classmethod
    def get_schema_for_microservice(cls, microservice: str) -> str:
        """Obtener el schema para un microservicio"""
        return cls.MICROSERVICE_SCHEMAS.get(microservice, "public")
    
    @classmethod
    def get_microservices_list(cls) -> List[str]:
        """Obtener lista de microservicios disponibles"""
        return list(cls.MICROSERVICE_SCHEMAS.keys())
    
    @classmethod
    def get_description(cls, microservice: str) -> str:
        """Obtener descripción de un microservicio"""
        return cls.MICROSERVICE_DESCRIPTIONS.get(microservice, "Sin descripción")
    
    @classmethod
    def get_expected_tables(cls, microservice: str) -> List[str]:
        """Obtener tablas esperadas para un microservicio"""
        return cls.EXPECTED_TABLES.get(microservice, [])
    
    @classmethod
    def get_common_fields(cls, table_name: str) -> List[str]:
        """Obtener campos comunes para un tipo de tabla"""
        return cls.COMMON_FIELDS.get(table_name, [])
