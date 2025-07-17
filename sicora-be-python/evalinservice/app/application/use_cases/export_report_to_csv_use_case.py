"""Export Report to CSV use case."""

from uuid import UUID
from typing import Optional

from ...domain.repositories import (
    EvaluationRepositoryInterface,
    EvaluationPeriodRepositoryInterface,
    QuestionRepositoryInterface
)
from ...domain.exceptions import EvaluationPeriodNotFoundError
from ..dtos.report_dtos import ExportReportRequest, ExportReportResponse
from ..interfaces import CSVProcessorInterface, UserServiceInterface


class ExportReportToCSVUseCase:
    """
    Caso de uso para exportar reportes a formato CSV.
    
    Responsabilidades:
    - Validar que el período existe
    - Obtener datos de evaluaciones según filtros
    - Procesar datos para formato CSV
    - Generar archivo CSV con el procesador
    - Retornar información del archivo generado
    """
    
    def __init__(
        self,
        evaluation_repository: EvaluationRepositoryInterface,
        evaluation_period_repository: EvaluationPeriodRepositoryInterface,
        question_repository: QuestionRepositoryInterface,
        csv_processor: CSVProcessorInterface,
        user_service: UserServiceInterface
    ):
        self._evaluation_repository = evaluation_repository
        self._evaluation_period_repository = evaluation_period_repository
        self._question_repository = question_repository
        self._csv_processor = csv_processor
        self._user_service = user_service
    
    async def execute(self, request: ExportReportRequest) -> ExportReportResponse:
        """
        Ejecuta el caso de uso de exportación de reporte a CSV.
        
        Args:
            request: Parámetros de exportación
            
        Returns:
            ExportReportResponse: Información del archivo generado
            
        Raises:
            EvaluationPeriodNotFoundError: Si el período no existe
        """
        # Verificar que el período existe
        period = await self._evaluation_period_repository.get_by_id(request.evaluation_period_id)
        if not period:
            raise EvaluationPeriodNotFoundError(f"No se encontró el período con ID: {request.evaluation_period_id}")
        
        # Obtener evaluaciones según filtros
        evaluations = await self._evaluation_repository.get_all(
            evaluation_period_id=request.evaluation_period_id,
            instructor_id=request.instructor_id,
            skip=0,
            limit=10000  # Obtener todas las evaluaciones
        )
        
        # Obtener información de preguntas del cuestionario
        questionnaire_id = period.questionnaire_id
        questions = await self._question_repository.get_by_questionnaire_id(questionnaire_id)
        question_map = {q.id: q.text for q in questions}
        
        # Preparar datos para CSV
        csv_data = []
        headers = [
            "evaluation_id",
            "student_id", 
            "instructor_id",
            "instructor_name",
            "submitted_at"
        ]
        
        # Agregar columnas para cada pregunta
        for question in questions:
            headers.append(f"pregunta_{question.id}")
        
        headers.append("comentarios")
        
        # Procesar cada evaluación
        for evaluation in evaluations:
            # Obtener información del instructor
            instructor = await self._user_service.get_user_by_id(evaluation.instructor_id)
            instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown"
            
            row = [
                str(evaluation.id),
                str(evaluation.student_id),
                str(evaluation.instructor_id),
                instructor_name,
                evaluation.submitted_at.isoformat() if evaluation.submitted_at else ""
            ]
            
            # Mapear respuestas por pregunta
            response_map = {resp.question_id: resp.score for resp in evaluation.responses}
            
            # Agregar puntuaciones para cada pregunta
            for question in questions:
                score = response_map.get(question.id, "")
                row.append(str(score) if score else "")
            
            # Agregar comentarios
            row.append(evaluation.comments or "")
            
            csv_data.append(row)
        
        # Generar archivo CSV
        filename = f"evaluaciones_{period.name.replace(' ', '_')}_{request.evaluation_period_id}"
        if request.instructor_id:
            filename += f"_instructor_{request.instructor_id}"
        
        file_info = await self._csv_processor.generate_csv(
            headers=headers,
            data=csv_data,
            filename=filename
        )
        
        return ExportReportResponse(
            filename=file_info.filename,
            file_path=file_info.file_path,
            file_size=file_info.file_size,
            total_records=len(csv_data),
            generated_at=file_info.generated_at,
            download_url=file_info.download_url
        )
