"""Questionnaire router for EvalinService API."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies import container, get_admin_user, CurrentUser
from ..schemas import (
    QuestionnaireCreateSchema,
    QuestionnaireUpdateSchema,
    QuestionnaireResponseSchema,
    QuestionnaireListResponseSchema,
    AddQuestionToQuestionnaireSchema,
    RemoveQuestionFromQuestionnaireSchema
)
from ...domain.exceptions import (
    QuestionnaireNotFoundError,
    QuestionnaireAlreadyExistsError,
    QuestionnaireInUseError,
    QuestionNotFoundError,
    DuplicateQuestionError,
    QuestionNotInQuestionnaireError
)

router = APIRouter(prefix="/questionnaires", tags=["Questionnaires"])


@router.post(
    "/",
    response_model=QuestionnaireResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo cuestionario",
    description="Crea un nuevo cuestionario para evaluaciones de instructores"
)
async def create_questionnaire(
    questionnaire_data: QuestionnaireCreateSchema,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Crear un nuevo cuestionario.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **name**: Nombre único del cuestionario (3-200 caracteres)
    - **description**: Descripción opcional del cuestionario
    """
    try:
        use_case = container.get_create_questionnaire_use_case(db)
        
        from ...application.dtos.questionnaire_dtos import CreateQuestionnaireRequest
        request = CreateQuestionnaireRequest(
            name=questionnaire_data.name,
            description=questionnaire_data.description
        )
        
        result = await use_case.execute(request)
        
        return QuestionnaireResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            is_active=result.is_active,
            question_count=result.question_count,
            question_ids=result.question_ids,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except QuestionnaireAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/",
    response_model=QuestionnaireListResponseSchema,
    summary="Listar cuestionarios",
    description="Obtiene lista de cuestionarios con filtros opcionales"
)
async def get_questionnaires(
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Obtener lista de cuestionarios con filtros.
    
    **Permisos requeridos:** Administrador
    
    **Filtros disponibles:**
    - **is_active**: Filtrar por estado activo
    - **skip**: Número de registros a omitir
    - **limit**: Máximo de registros a retornar
    """
    try:
        use_case = container.get_get_questionnaires_use_case(db)
        
        results = await use_case.execute(
            is_active=is_active,
            skip=skip,
            limit=limit
        )
        
        questionnaires = [
            QuestionnaireResponseSchema(
                id=q.id,
                name=q.name,
                description=q.description,
                is_active=q.is_active,
                question_count=q.question_count,
                question_ids=q.question_ids,
                created_at=q.created_at,
                updated_at=q.updated_at
            )
            for q in results
        ]
        
        return QuestionnaireListResponseSchema(
            questionnaires=questionnaires,
            total=len(questionnaires),
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{questionnaire_id}",
    response_model=QuestionnaireResponseSchema,
    summary="Obtener cuestionario por ID",
    description="Obtiene un cuestionario específico por su ID"
)
async def get_questionnaire_by_id(
    questionnaire_id: UUID,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Obtener cuestionario por ID.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **questionnaire_id**: ID único del cuestionario
    """
    try:
        use_case = container.get_get_questionnaire_by_id_use_case(db)
        result = await use_case.execute(questionnaire_id)
        
        return QuestionnaireResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            is_active=result.is_active,
            question_count=result.question_count,
            question_ids=result.question_ids,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except QuestionnaireNotFoundError as e:
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
    "/{questionnaire_id}",
    response_model=QuestionnaireResponseSchema,
    summary="Actualizar cuestionario",
    description="Actualiza un cuestionario existente"
)
async def update_questionnaire(
    questionnaire_id: UUID,
    questionnaire_data: QuestionnaireUpdateSchema,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Actualizar cuestionario existente.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **questionnaire_id**: ID único del cuestionario
    - **name**: Nuevo nombre del cuestionario (opcional)
    - **description**: Nueva descripción (opcional)
    - **is_active**: Nuevo estado activo (opcional)
    """
    try:
        use_case = container.get_update_questionnaire_use_case(db)
        
        from ...application.dtos.questionnaire_dtos import UpdateQuestionnaireRequest
        request = UpdateQuestionnaireRequest(
            name=questionnaire_data.name,
            description=questionnaire_data.description,
            is_active=questionnaire_data.is_active
        )
        
        result = await use_case.execute(questionnaire_id, request)
        
        return QuestionnaireResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            is_active=result.is_active,
            question_count=result.question_count,
            question_ids=result.question_ids,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except QuestionnaireNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except QuestionnaireAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete(
    "/{questionnaire_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar cuestionario",
    description="Elimina un cuestionario del sistema"
)
async def delete_questionnaire(
    questionnaire_id: UUID,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Eliminar cuestionario.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **questionnaire_id**: ID único del cuestionario
    
    **Nota:** No se puede eliminar un cuestionario que esté siendo usado en períodos de evaluación.
    """
    try:
        use_case = container.get_delete_questionnaire_use_case(db)
        await use_case.execute(questionnaire_id)
        
    except QuestionnaireNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except QuestionnaireInUseError as e:
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
    "/{questionnaire_id}/questions",
    response_model=QuestionnaireResponseSchema,
    summary="Agregar pregunta al cuestionario",
    description="Agrega una pregunta existente al cuestionario"
)
async def add_question_to_questionnaire(
    questionnaire_id: UUID,
    question_data: AddQuestionToQuestionnaireSchema,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Agregar pregunta a cuestionario.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **questionnaire_id**: ID único del cuestionario
    - **question_id**: ID de la pregunta a agregar
    """
    try:
        use_case = container.get_add_question_to_questionnaire_use_case(db)
        
        result = await use_case.execute(questionnaire_id, question_data.question_id)
        
        return QuestionnaireResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            is_active=result.is_active,
            question_count=result.question_count,
            question_ids=result.question_ids,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except QuestionnaireNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except QuestionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateQuestionError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete(
    "/{questionnaire_id}/questions/{question_id}",
    response_model=QuestionnaireResponseSchema,
    summary="Remover pregunta del cuestionario",
    description="Remueve una pregunta del cuestionario"
)
async def remove_question_from_questionnaire(
    questionnaire_id: UUID,
    question_id: UUID,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Remover pregunta de cuestionario.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **questionnaire_id**: ID único del cuestionario
    - **question_id**: ID de la pregunta a remover
    """
    try:
        use_case = container.get_remove_question_from_questionnaire_use_case(db)
        
        result = await use_case.execute(questionnaire_id, question_id)
        
        return QuestionnaireResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            is_active=result.is_active,
            question_count=result.question_count,
            question_ids=result.question_ids,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except QuestionnaireNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except QuestionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except QuestionNotInQuestionnaireError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
