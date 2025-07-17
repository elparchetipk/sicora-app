"""Dependency injection container for EvalinService."""

from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from ...infrastructure.database.database import SessionLocal
from ...infrastructure.database.session import get_db
from ...infrastructure.repositories import (
    QuestionRepository,
    QuestionnaireRepository,
    EvaluationPeriodRepository,
    EvaluationRepository
)
from ...infrastructure.adapters import (
    UserServiceAdapter,
    ScheduleServiceAdapter,
    NotificationServiceAdapter,
    CSVProcessorAdapter
)
from ...application.use_cases import (
    # Question Use Cases
    CreateQuestionUseCase,
    GetQuestionsUseCase,
    GetQuestionByIdUseCase,
    UpdateQuestionUseCase,
    DeleteQuestionUseCase,
    BulkUploadQuestionsUseCase,

    # Questionnaire Use Cases
    CreateQuestionnaireUseCase,
    GetQuestionnairesUseCase,
    GetQuestionnaireByIdUseCase,
    UpdateQuestionnaireUseCase,
    DeleteQuestionnaireUseCase,
    AddQuestionToQuestionnaireUseCase,
    RemoveQuestionFromQuestionnaireUseCase,

    # Evaluation Period Use Cases
    CreateEvaluationPeriodUseCase,
    GetEvaluationPeriodsUseCase,
    GetEvaluationPeriodByIdUseCase,
    UpdateEvaluationPeriodUseCase,
    CloseEvaluationPeriodUseCase,

    # Evaluation Use Cases
    CreateEvaluationUseCase,
    GetEvaluationByIdUseCase,
    GetEvaluationsUseCase,

    # Report Use Cases
    GenerateInstructorReportUseCase,
    GeneratePeriodReportUseCase,
    ExportReportToCSVUseCase,

    # Config Use Cases
    GetSystemConfigUseCase,

    # Notification Use Cases
    SendEvaluationReminderUseCase
)
import os


class DependencyContainer:
    """
    Container de inyección de dependencias para EvalinService.

    Responsabilidades:
    - Configurar y proporcionar todas las dependencias
    - Gestionar el ciclo de vida de las dependencias
    - Mantener configuración centralizada
    """

    def __init__(self):
        self._user_service_adapter = None
        self._schedule_service_adapter = None
        self._notification_service_adapter = None
        self._csv_processor_adapter = None

    # Database Dependencies
    def get_db_session(self) -> Generator[Session, None, None]:
        """Obtener sesión de base de datos."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # External Service Adapters
    def get_user_service_adapter(self) -> UserServiceAdapter:
        """Obtener adaptador de UserService."""
        if self._user_service_adapter is None:
            base_url = os.getenv("USER_SERVICE_URL", "http://userservice:8000")
            self._user_service_adapter = UserServiceAdapter(base_url)
        return self._user_service_adapter

    def get_schedule_service_adapter(self) -> ScheduleServiceAdapter:
        """Obtener adaptador de ScheduleService."""
        if self._schedule_service_adapter is None:
            base_url = os.getenv("SCHEDULE_SERVICE_URL", "http://scheduleservice:8001")
            self._schedule_service_adapter = ScheduleServiceAdapter(base_url)
        return self._schedule_service_adapter

    def get_notification_service_adapter(self) -> NotificationServiceAdapter:
        """Obtener adaptador de NotificationService."""
        if self._notification_service_adapter is None:
            base_url = os.getenv("NOTIFICATION_SERVICE_URL", "http://notificationservice:8005")
            self._notification_service_adapter = NotificationServiceAdapter(base_url)
        return self._notification_service_adapter

    def get_csv_processor_adapter(self) -> CSVProcessorAdapter:
        """Obtener adaptador de procesamiento CSV."""
        if self._csv_processor_adapter is None:
            upload_dir = os.getenv("UPLOAD_DIRECTORY", "/tmp/evalin_exports")
            self._csv_processor_adapter = CSVProcessorAdapter(upload_dir)
        return self._csv_processor_adapter

    # Repository Dependencies
    def get_question_repository(self, db: Session) -> QuestionRepository:
        """Obtener repositorio de preguntas."""
        return QuestionRepository(db)

    def get_questionnaire_repository(self, db: Session) -> QuestionnaireRepository:
        """Obtener repositorio de cuestionarios."""
        return QuestionnaireRepository(db)

    def get_evaluation_period_repository(self, db: Session) -> EvaluationPeriodRepository:
        """Obtener repositorio de períodos de evaluación."""
        return EvaluationPeriodRepository(db)

    def get_evaluation_repository(self, db: Session) -> EvaluationRepository:
        """Obtener repositorio de evaluaciones."""
        return EvaluationRepository(db)

    # Question Use Cases
    def get_create_question_use_case(self, db: Session) -> CreateQuestionUseCase:
        """Obtener caso de uso de crear pregunta."""
        return CreateQuestionUseCase(self.get_question_repository(db))

    def get_get_questions_use_case(self, db: Session) -> GetQuestionsUseCase:
        """Obtener caso de uso de obtener preguntas."""
        return GetQuestionsUseCase(self.get_question_repository(db))

    def get_get_question_by_id_use_case(self, db: Session) -> GetQuestionByIdUseCase:
        """Obtener caso de uso de obtener pregunta por ID."""
        return GetQuestionByIdUseCase(self.get_question_repository(db))

    def get_update_question_use_case(self, db: Session) -> UpdateQuestionUseCase:
        """Obtener caso de uso de actualizar pregunta."""
        return UpdateQuestionUseCase(self.get_question_repository(db))

    def get_delete_question_use_case(self, db: Session) -> DeleteQuestionUseCase:
        """Obtener caso de uso de eliminar pregunta."""
        question_repo = self.get_question_repository(db)
        questionnaire_repo = self.get_questionnaire_repository(db)
        return DeleteQuestionUseCase(question_repo, questionnaire_repo)

    def get_bulk_upload_questions_use_case(self, db: Session) -> BulkUploadQuestionsUseCase:
        """Obtener caso de uso de carga masiva de preguntas."""
        question_repo = self.get_question_repository(db)
        csv_processor = self.get_csv_processor_adapter()
        return BulkUploadQuestionsUseCase(question_repo, csv_processor)

    # Questionnaire Use Cases
    def get_create_questionnaire_use_case(self, db: Session) -> CreateQuestionnaireUseCase:
        """Obtener caso de uso de crear cuestionario."""
        return CreateQuestionnaireUseCase(self.get_questionnaire_repository(db))

    def get_get_questionnaires_use_case(self, db: Session) -> GetQuestionnairesUseCase:
        """Obtener caso de uso de obtener cuestionarios."""
        return GetQuestionnairesUseCase(self.get_questionnaire_repository(db))

    def get_get_questionnaire_by_id_use_case(self, db: Session) -> GetQuestionnaireByIdUseCase:
        """Obtener caso de uso de obtener cuestionario por ID."""
        return GetQuestionnaireByIdUseCase(self.get_questionnaire_repository(db))

    def get_update_questionnaire_use_case(self, db: Session) -> UpdateQuestionnaireUseCase:
        """Obtener caso de uso de actualizar cuestionario."""
        return UpdateQuestionnaireUseCase(self.get_questionnaire_repository(db))

    def get_delete_questionnaire_use_case(self, db: Session) -> DeleteQuestionnaireUseCase:
        """Obtener caso de uso de eliminar cuestionario."""
        questionnaire_repo = self.get_questionnaire_repository(db)
        period_repo = self.get_evaluation_period_repository(db)
        return DeleteQuestionnaireUseCase(questionnaire_repo, period_repo)

    def get_add_question_to_questionnaire_use_case(self, db: Session) -> AddQuestionToQuestionnaireUseCase:
        """Obtener caso de uso de agregar pregunta a cuestionario."""
        questionnaire_repo = self.get_questionnaire_repository(db)
        question_repo = self.get_question_repository(db)
        return AddQuestionToQuestionnaireUseCase(questionnaire_repo, question_repo)

    def get_remove_question_from_questionnaire_use_case(self, db: Session) -> RemoveQuestionFromQuestionnaireUseCase:
        """Obtener caso de uso de remover pregunta de cuestionario."""
        questionnaire_repo = self.get_questionnaire_repository(db)
        question_repo = self.get_question_repository(db)
        return RemoveQuestionFromQuestionnaireUseCase(questionnaire_repo, question_repo)

    # Evaluation Period Use Cases
    def get_create_evaluation_period_use_case(self, db: Session) -> CreateEvaluationPeriodUseCase:
        """Obtener caso de uso de crear período de evaluación."""
        period_repo = self.get_evaluation_period_repository(db)
        questionnaire_repo = self.get_questionnaire_repository(db)
        schedule_service = self.get_schedule_service_adapter()
        return CreateEvaluationPeriodUseCase(period_repo, questionnaire_repo, schedule_service)

    def get_get_evaluation_periods_use_case(self, db: Session) -> GetEvaluationPeriodsUseCase:
        """Obtener caso de uso de obtener períodos de evaluación."""
        return GetEvaluationPeriodsUseCase(self.get_evaluation_period_repository(db))

    def get_get_evaluation_period_by_id_use_case(self, db: Session) -> GetEvaluationPeriodByIdUseCase:
        """Obtener caso de uso de obtener período por ID."""
        return GetEvaluationPeriodByIdUseCase(self.get_evaluation_period_repository(db))

    def get_update_evaluation_period_use_case(self, db: Session) -> UpdateEvaluationPeriodUseCase:
        """Obtener caso de uso de actualizar período."""
        return UpdateEvaluationPeriodUseCase(self.get_evaluation_period_repository(db))

    def get_close_evaluation_period_use_case(self, db: Session) -> CloseEvaluationPeriodUseCase:
        """Obtener caso de uso de cerrar período."""
        period_repo = self.get_evaluation_period_repository(db)
        notification_service = self.get_notification_service_adapter()
        return CloseEvaluationPeriodUseCase(period_repo, notification_service)

    # Evaluation Use Cases
    def get_create_evaluation_use_case(self, db: Session) -> CreateEvaluationUseCase:
        """Obtener caso de uso de crear evaluación."""
        evaluation_repo = self.get_evaluation_repository(db)
        period_repo = self.get_evaluation_period_repository(db)
        questionnaire_repo = self.get_questionnaire_repository(db)
        user_service = self.get_user_service_adapter()
        return CreateEvaluationUseCase(evaluation_repo, period_repo, questionnaire_repo, user_service)

    def get_get_evaluation_by_id_use_case(self, db: Session) -> GetEvaluationByIdUseCase:
        """Obtener caso de uso de obtener evaluación por ID."""
        return GetEvaluationByIdUseCase(self.get_evaluation_repository(db))

    def get_get_evaluations_use_case(self, db: Session) -> GetEvaluationsUseCase:
        """Obtener caso de uso de obtener evaluaciones."""
        return GetEvaluationsUseCase(self.get_evaluation_repository(db))

    # Report Use Cases
    def get_generate_instructor_report_use_case(self, db: Session) -> GenerateInstructorReportUseCase:
        """Obtener caso de uso de generar reporte de instructor."""
        evaluation_repo = self.get_evaluation_repository(db)
        period_repo = self.get_evaluation_period_repository(db)
        question_repo = self.get_question_repository(db)
        user_service = self.get_user_service_adapter()
        return GenerateInstructorReportUseCase(evaluation_repo, period_repo, question_repo, user_service)

    def get_generate_period_report_use_case(self, db: Session) -> GeneratePeriodReportUseCase:
        """Obtener caso de uso de generar reporte de período."""
        evaluation_repo = self.get_evaluation_repository(db)
        period_repo = self.get_evaluation_period_repository(db)
        questionnaire_repo = self.get_questionnaire_repository(db)
        user_service = self.get_user_service_adapter()
        return GeneratePeriodReportUseCase(evaluation_repo, period_repo, questionnaire_repo, user_service)

    def get_export_report_to_csv_use_case(self, db: Session) -> ExportReportToCSVUseCase:
        """Obtener caso de uso de exportar reportes a CSV."""
        evaluation_repo = self.get_evaluation_repository(db)
        period_repo = self.get_evaluation_period_repository(db)
        question_repo = self.get_question_repository(db)
        csv_processor = self.get_csv_processor_adapter()
        user_service = self.get_user_service_adapter()
        return ExportReportToCSVUseCase(evaluation_repo, period_repo, question_repo, csv_processor, user_service)

    # Config Use Cases
    def get_get_system_config_use_case(self) -> GetSystemConfigUseCase:
        """Obtener caso de uso de obtener configuración del sistema."""
        return GetSystemConfigUseCase()

    # Notification Use Cases
    def get_send_evaluation_reminder_use_case(self, db: Session) -> SendEvaluationReminderUseCase:
        """Obtener caso de uso de enviar recordatorios de evaluación."""
        evaluation_repo = self.get_evaluation_repository(db)
        period_repo = self.get_evaluation_period_repository(db)
        user_service = self.get_user_service_adapter()
        notification_service = self.get_notification_service_adapter()
        return SendEvaluationReminderUseCase(evaluation_repo, period_repo, user_service, notification_service)


# Global container instance
container = DependencyContainer()

# Dependency functions for FastAPI
def get_db() -> Generator[Session, None, None]:
    """Dependency function para obtener sesión de base de datos."""
    return container.get_db_session()

# Question use case dependencies
def get_create_question_use_case(db: Session = Depends(get_db)) -> CreateQuestionUseCase:
    return container.get_create_question_use_case(db)

def get_get_questions_use_case(db: Session = Depends(get_db)) -> GetQuestionsUseCase:
    return container.get_get_questions_use_case(db)

def get_get_question_by_id_use_case(db: Session = Depends(get_db)) -> GetQuestionByIdUseCase:
    return container.get_get_question_by_id_use_case(db)

def get_update_question_use_case(db: Session = Depends(get_db)) -> UpdateQuestionUseCase:
    return container.get_update_question_use_case(db)

def get_delete_question_use_case(db: Session = Depends(get_db)) -> DeleteQuestionUseCase:
    return container.get_delete_question_use_case(db)

def get_bulk_upload_questions_use_case(db: Session = Depends(get_db)) -> BulkUploadQuestionsUseCase:
    return container.get_bulk_upload_questions_use_case(db)

# Questionnaire use case dependencies
def get_create_questionnaire_use_case(db: Session = Depends(get_db)) -> CreateQuestionnaireUseCase:
    return container.get_create_questionnaire_use_case(db)

def get_get_questionnaires_use_case(db: Session = Depends(get_db)) -> GetQuestionnairesUseCase:
    return container.get_get_questionnaires_use_case(db)

def get_get_questionnaire_by_id_use_case(db: Session = Depends(get_db)) -> GetQuestionnaireByIdUseCase:
    return container.get_get_questionnaire_by_id_use_case(db)

def get_update_questionnaire_use_case(db: Session = Depends(get_db)) -> UpdateQuestionnaireUseCase:
    return container.get_update_questionnaire_use_case(db)

def get_delete_questionnaire_use_case(db: Session = Depends(get_db)) -> DeleteQuestionnaireUseCase:
    return container.get_delete_questionnaire_use_case(db)

def get_add_question_to_questionnaire_use_case(db: Session = Depends(get_db)) -> AddQuestionToQuestionnaireUseCase:
    return container.get_add_question_to_questionnaire_use_case(db)

def get_remove_question_from_questionnaire_use_case(db: Session = Depends(get_db)) -> RemoveQuestionFromQuestionnaireUseCase:
    return container.get_remove_question_from_questionnaire_use_case(db)

# Evaluation period use case dependencies
def get_create_evaluation_period_use_case(db: Session = Depends(get_db)) -> CreateEvaluationPeriodUseCase:
    return container.get_create_evaluation_period_use_case(db)

def get_get_evaluation_periods_use_case(db: Session = Depends(get_db)) -> GetEvaluationPeriodsUseCase:
    return container.get_get_evaluation_periods_use_case(db)

def get_get_evaluation_period_by_id_use_case(db: Session = Depends(get_db)) -> GetEvaluationPeriodByIdUseCase:
    return container.get_get_evaluation_period_by_id_use_case(db)

def get_update_evaluation_period_use_case(db: Session = Depends(get_db)) -> UpdateEvaluationPeriodUseCase:
    return container.get_update_evaluation_period_use_case(db)

def get_close_evaluation_period_use_case(db: Session = Depends(get_db)) -> CloseEvaluationPeriodUseCase:
    return container.get_close_evaluation_period_use_case(db)

# Evaluation use case dependencies
def get_create_evaluation_use_case(db: Session = Depends(get_db)) -> CreateEvaluationUseCase:
    return container.get_create_evaluation_use_case(db)

def get_get_evaluation_by_id_use_case(db: Session = Depends(get_db)) -> GetEvaluationByIdUseCase:
    return container.get_get_evaluation_by_id_use_case(db)

def get_get_evaluations_use_case(db: Session = Depends(get_db)) -> GetEvaluationsUseCase:
    return container.get_get_evaluations_use_case(db)

# Report use case dependencies
def get_generate_instructor_report_use_case(db: Session = Depends(get_db)) -> GenerateInstructorReportUseCase:
    return container.get_generate_instructor_report_use_case(db)

def get_generate_period_report_use_case(db: Session = Depends(get_db)) -> GeneratePeriodReportUseCase:
    return container.get_generate_period_report_use_case(db)

def get_export_report_to_csv_use_case(db: Session = Depends(get_db)) -> ExportReportToCSVUseCase:
    return container.get_export_report_to_csv_use_case(db)

# Config use case dependencies
def get_get_system_config_use_case() -> GetSystemConfigUseCase:
    return container.get_get_system_config_use_case()

# Notification use case dependencies
def get_send_evaluation_reminder_use_case(db: Session = Depends(get_db)) -> SendEvaluationReminderUseCase:
    return container.get_send_evaluation_reminder_use_case(db)
