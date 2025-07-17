"""Bulk Upload Questions use case."""

import csv
from io import StringIO
from typing import List

from ...domain.entities import Question
from ...domain.repositories import QuestionRepositoryInterface
from ...domain.value_objects import QuestionType
from ...domain.exceptions import InvalidQuestionTextError, InvalidQuestionTypeError
from ..interfaces import CSVProcessorInterface
from ..dtos.question_dtos import BulkQuestionUploadRequest, BulkQuestionUploadResult, QuestionResponse


class BulkUploadQuestionsUseCase:
    """
    Caso de uso para carga masiva de preguntas desde CSV.
    
    Responsabilidades:
    - Validar formato del archivo CSV
    - Procesar preguntas en lotes
    - Manejar errores de validación por fila
    - Crear preguntas válidas en el repositorio
    - Generar reporte de resultados
    """
    
    def __init__(
        self, 
        question_repository: QuestionRepositoryInterface,
        csv_processor: CSVProcessorInterface
    ):
        self._question_repository = question_repository
        self._csv_processor = csv_processor
    
    async def execute(self, request: BulkQuestionUploadRequest) -> BulkQuestionUploadResult:
        """
        Ejecuta el caso de uso de carga masiva de preguntas.
        
        Args:
            request: Datos de la carga masiva
            
        Returns:
            BulkQuestionUploadResult: Resultado de la operación
        """
        errors = []
        created_questions = []
        successful_count = 0
        failed_count = 0
        
        try:
            # Validar formato CSV
            is_valid, validation_errors = await self._csv_processor.validate_csv_format(request.csv_content)
            
            if not is_valid:
                errors.extend(validation_errors)
                return BulkQuestionUploadResult(
                    successful_count=0,
                    failed_count=0,
                    errors=errors,
                    created_questions=[]
                )
            
            # Parsear CSV
            questions_data = await self._csv_processor.parse_questions_csv(request.csv_content)
            
            # Si es solo validación, no crear las preguntas
            if request.validate_only:
                validated_questions = []
                for i, question_data in enumerate(questions_data, 1):
                    try:
                        # Intentar crear entidad para validar
                        self._validate_question_data(question_data, i)
                        validated_questions.append(question_data)
                        successful_count += 1
                    except Exception as e:
                        errors.append(f"Fila {i}: {str(e)}")
                        failed_count += 1
                
                return BulkQuestionUploadResult(
                    successful_count=successful_count,
                    failed_count=failed_count,
                    errors=errors,
                    created_questions=[]
                )
            
            # Procesar y crear preguntas
            questions_to_create = []
            
            for i, question_data in enumerate(questions_data, 1):
                try:
                    # Validar datos
                    self._validate_question_data(question_data, i)
                    
                    # Verificar que no exista pregunta con el mismo texto
                    if await self._question_repository.exists_by_text(question_data["text"]):
                        errors.append(f"Fila {i}: Ya existe una pregunta con el texto '{question_data['text']}'")
                        failed_count += 1
                        continue
                    
                    # Crear entidad
                    question = Question.create(
                        text=question_data["text"],
                        question_type=QuestionType(question_data["question_type"]),
                        category=question_data["category"],
                        is_required=question_data.get("is_required", True),
                        order_index=question_data.get("order_index", 0),
                        options=question_data.get("options")
                    )
                    
                    questions_to_create.append(question)
                    
                except Exception as e:
                    errors.append(f"Fila {i}: {str(e)}")
                    failed_count += 1
            
            # Crear preguntas en lote
            if questions_to_create:
                created_entities = await self._question_repository.bulk_create(questions_to_create)
                successful_count = len(created_entities)
                
                # Convertir a DTOs de respuesta
                created_questions = [
                    QuestionResponse(
                        id=question.id,
                        text=question.text,
                        question_type=question.question_type,
                        category=question.category,
                        is_required=question.is_required,
                        order_index=question.order_index,
                        is_active=question.is_active,
                        options=question.options,
                        created_at=question.created_at,
                        updated_at=question.updated_at
                    )
                    for question in created_entities
                ]
            
        except Exception as e:
            errors.append(f"Error general: {str(e)}")
            failed_count = len(questions_data) if 'questions_data' in locals() else 1
        
        return BulkQuestionUploadResult(
            successful_count=successful_count,
            failed_count=failed_count,
            errors=errors,
            created_questions=created_questions
        )
    
    def _validate_question_data(self, question_data: dict, row_number: int) -> None:
        """Valida los datos de una pregunta."""
        required_fields = ["text", "question_type", "category"]
        
        for field in required_fields:
            if field not in question_data or not question_data[field]:
                raise ValueError(f"Campo requerido '{field}' faltante o vacío")
        
        # Validar tipo de pregunta
        try:
            question_type = QuestionType(question_data["question_type"])
        except ValueError:
            valid_types = [t.value for t in QuestionType]
            raise ValueError(f"Tipo de pregunta inválido. Tipos válidos: {', '.join(valid_types)}")
        
        # Validar que preguntas de opción múltiple tengan opciones
        if question_type == QuestionType.MULTIPLE_CHOICE:
            if not question_data.get("options"):
                raise ValueError("Preguntas de opción múltiple deben tener opciones definidas")
        
        # Validar longitud del texto
        if len(question_data["text"].strip()) < 10:
            raise ValueError("El texto de la pregunta debe tener al menos 10 caracteres")
        
        if len(question_data["text"].strip()) > 500:
            raise ValueError("El texto de la pregunta no puede exceder 500 caracteres")
