"""Question router for EvalinService API."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from ..dependencies import container, get_admin_user, CurrentUser
from ..schemas import (
    QuestionCreateSchema,
    QuestionUpdateSchema,
    QuestionResponseSchema,
    QuestionListResponseSchema,
    BulkUploadResponseSchema
)
from ...domain.value_objects import QuestionType
from ...domain.exceptions import (
    QuestionNotFoundError,
    QuestionInUseError,
    InvalidQuestionTextError
)

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post(
    "/",
    response_model=QuestionResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva pregunta",
    description="Crea una nueva pregunta para usar en cuestionarios de evaluación"
)
async def create_question(
    question_data: QuestionCreateSchema,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Crear una nueva pregunta.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **text**: Texto de la pregunta (10-1000 caracteres)
    - **question_type**: Tipo de pregunta (likert, text, multiple_choice)
    - **category**: Categoría opcional para agrupar preguntas
    """
    try:
        use_case = container.get_create_question_use_case(db)
        
        from ...application.dtos.question_dtos import CreateQuestionRequest
        request = CreateQuestionRequest(
            text=question_data.text,
            question_type=question_data.question_type,
            category=question_data.category
        )
        
        result = await use_case.execute(request)
        
        return QuestionResponseSchema(
            id=result.id,
            text=result.text,
            question_type=result.question_type,
            category=result.category,
            is_active=result.is_active,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except InvalidQuestionTextError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/",
    response_model=QuestionListResponseSchema,
    summary="Listar preguntas",
    description="Obtiene lista de preguntas con filtros opcionales"
)
async def get_questions(
    question_type: Optional[QuestionType] = None,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Obtener lista de preguntas con filtros.
    
    **Permisos requeridos:** Administrador
    
    **Filtros disponibles:**
    - **question_type**: Filtrar por tipo de pregunta
    - **category**: Filtrar por categoría
    - **is_active**: Filtrar por estado activo
    - **skip**: Número de registros a omitir
    - **limit**: Máximo de registros a retornar
    """
    try:
        use_case = container.get_get_questions_use_case(db)
        
        results = await use_case.execute(
            question_type=question_type,
            category=category,
            is_active=is_active,
            skip=skip,
            limit=limit
        )
        
        questions = [
            QuestionResponseSchema(
                id=q.id,
                text=q.text,
                question_type=q.question_type,
                category=q.category,
                is_active=q.is_active,
                created_at=q.created_at,
                updated_at=q.updated_at
            )
            for q in results
        ]
        
        return QuestionListResponseSchema(
            questions=questions,
            total=len(questions),
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{question_id}",
    response_model=QuestionResponseSchema,
    summary="Obtener pregunta por ID",
    description="Obtiene una pregunta específica por su ID"
)
async def get_question_by_id(
    question_id: UUID,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Obtener pregunta por ID.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **question_id**: ID único de la pregunta
    """
    try:
        use_case = container.get_get_question_by_id_use_case(db)
        result = await use_case.execute(question_id)
        
        return QuestionResponseSchema(
            id=result.id,
            text=result.text,
            question_type=result.question_type,
            category=result.category,
            is_active=result.is_active,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except QuestionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put(
    "/{question_id}",
    response_model=QuestionResponseSchema,
    summary="Actualizar pregunta",
    description="Actualiza una pregunta existente"
)
async def update_question(
    question_id: UUID,
    question_data: QuestionUpdateSchema,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Actualizar pregunta existente.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **question_id**: ID único de la pregunta
    - **text**: Nuevo texto de la pregunta (opcional)
    - **question_type**: Nuevo tipo de pregunta (opcional)
    - **category**: Nueva categoría (opcional)
    - **is_active**: Nuevo estado activo (opcional)
    """
    try:
        use_case = container.get_update_question_use_case(db)
        
        from ...application.dtos.question_dtos import UpdateQuestionRequest
        request = UpdateQuestionRequest(
            text=question_data.text,
            question_type=question_data.question_type,
            category=question_data.category,
            is_active=question_data.is_active
        )
        
        result = await use_case.execute(question_id, request)
        
        return QuestionResponseSchema(
            id=result.id,
            text=result.text,
            question_type=result.question_type,
            category=result.category,
            is_active=result.is_active,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except QuestionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidQuestionTextError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar pregunta",
    description="Elimina una pregunta del sistema"
)
async def delete_question(
    question_id: UUID,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Eliminar pregunta.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **question_id**: ID único de la pregunta
    
    **Nota:** No se puede eliminar una pregunta que esté siendo usada en cuestionarios activos.
    """
    try:
        use_case = container.get_delete_question_use_case(db)
        await use_case.execute(question_id)
        
    except QuestionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except QuestionInUseError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post(
    "/bulk-upload",
    response_model=BulkUploadResponseSchema,
    summary="Carga masiva de preguntas",
    description="Carga múltiples preguntas desde archivo CSV"
)
async def bulk_upload_questions(
    file: UploadFile = File(..., description="Archivo CSV con preguntas"),
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Carga masiva de preguntas desde CSV.
    
    **Permisos requeridos:** Administrador
    
    **Formato del CSV:**
    - **text**: Texto de la pregunta
    - **question_type**: Tipo de pregunta (likert, text, multiple_choice)
    - **category**: Categoría (opcional)
    
    **Ejemplo de archivo CSV:**
    ```
    text,question_type,category
    "¿El instructor explica claramente?",likert,comunicacion
    "¿El instructor domina el tema?",likert,conocimiento
    ```
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe ser de tipo CSV"
            )
        
        # Guardar archivo temporalmente
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            use_case = container.get_bulk_upload_questions_use_case(db)
            result = await use_case.execute(tmp_file_path)
            
            # Convertir resultado a schema
            created_questions = [
                QuestionResponseSchema(
                    id=q.id,
                    text=q.text,
                    question_type=q.question_type,
                    category=q.category,
                    is_active=q.is_active,
                    created_at=q.created_at,
                    updated_at=q.updated_at
                )
                for q in result.created_questions
            ]
            
            return BulkUploadResponseSchema(
                total_processed=result.total_processed,
                successful=result.successful,
                failed=result.failed,
                errors=result.errors,
                created_questions=created_questions
            )
            
        finally:
            # Limpiar archivo temporal
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar archivo: {str(e)}"
        )
