"""Evaluation Period router for EvalinService API."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from ..dependencies import container, get_admin_user, get_instructor_user, CurrentUser
from ..schemas import (
    EvaluationPeriodCreateSchema,
    EvaluationPeriodUpdateSchema,
    EvaluationPeriodResponseSchema,
    EvaluationPeriodListResponseSchema
)
from ...domain.value_objects import PeriodStatus
from ...domain.exceptions import (
    EvaluationPeriodNotFoundError,
    EvaluationPeriodOverlapError,
    EvaluationPeriodInvalidStateError,
    QuestionnaireNotFoundError
)

router = APIRouter(prefix="/periods", tags=["Evaluation Periods"])


@router.post(
    "/",
    response_model=EvaluationPeriodResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo período de evaluación",
    description="Crea un nuevo período de evaluación para instructores"
)
async def create_evaluation_period(
    period_data: EvaluationPeriodCreateSchema,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Crear un nuevo período de evaluación.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **name**: Nombre del período (3-200 caracteres)
    - **description**: Descripción opcional del período
    - **start_date**: Fecha y hora de inicio
    - **end_date**: Fecha y hora de finalización
    - **questionnaire_id**: ID del cuestionario a usar
    - **target_groups**: Lista de IDs de grupos objetivo
    - **is_anonymous**: Si las evaluaciones son anónimas
    """
    try:
        use_case = container.get_create_evaluation_period_use_case(db)
        
        from ...application.dtos.period_dtos import CreateEvaluationPeriodRequest
        request = CreateEvaluationPeriodRequest(
            name=period_data.name,
            description=period_data.description,
            start_date=period_data.start_date,
            end_date=period_data.end_date,
            questionnaire_id=period_data.questionnaire_id,
            target_groups=period_data.target_groups,
            is_anonymous=period_data.is_anonymous
        )
        
        result = await use_case.execute(request)
        
        return EvaluationPeriodResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            start_date=result.start_date,
            end_date=result.end_date,
            status=result.status,
            questionnaire_id=result.questionnaire_id,
            target_groups=result.target_groups,
            is_anonymous=result.is_anonymous,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except QuestionnaireNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except EvaluationPeriodOverlapError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
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
    response_model=EvaluationPeriodListResponseSchema,
    summary="Listar períodos de evaluación",
    description="Obtiene lista de períodos de evaluación con filtros opcionales"
)
async def get_evaluation_periods(
    status_filter: Optional[PeriodStatus] = Query(None, alias="status", description="Filtrar por estado"),
    start_date: Optional[datetime] = Query(None, description="Filtrar por fecha de inicio"),
    end_date: Optional[datetime] = Query(None, description="Filtrar por fecha de fin"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros a retornar"),
    current_user: CurrentUser = Depends(get_instructor_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Obtener lista de períodos de evaluación con filtros.
    
    **Permisos requeridos:** Instructor o superior
    
    **Filtros disponibles:**
    - **status**: Filtrar por estado (draft, active, closed)
    - **start_date**: Filtrar por fecha de inicio
    - **end_date**: Filtrar por fecha de fin
    - **skip**: Número de registros a omitir
    - **limit**: Máximo de registros a retornar
    """
    try:
        use_case = container.get_get_evaluation_periods_use_case(db)
        
        results = await use_case.execute(
            status=status_filter,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
        
        periods = [
            EvaluationPeriodResponseSchema(
                id=p.id,
                name=p.name,
                description=p.description,
                start_date=p.start_date,
                end_date=p.end_date,
                status=p.status,
                questionnaire_id=p.questionnaire_id,
                target_groups=p.target_groups,
                is_anonymous=p.is_anonymous,
                created_at=p.created_at,
                updated_at=p.updated_at
            )
            for p in results
        ]
        
        return EvaluationPeriodListResponseSchema(
            periods=periods,
            total=len(periods),
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{period_id}",
    response_model=EvaluationPeriodResponseSchema,
    summary="Obtener período por ID",
    description="Obtiene un período de evaluación específico por su ID"
)
async def get_evaluation_period_by_id(
    period_id: UUID,
    current_user: CurrentUser = Depends(get_instructor_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Obtener período de evaluación por ID.
    
    **Permisos requeridos:** Instructor o superior
    
    **Parámetros:**
    - **period_id**: ID único del período de evaluación
    """
    try:
        use_case = container.get_get_evaluation_period_by_id_use_case(db)
        result = await use_case.execute(period_id)
        
        return EvaluationPeriodResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            start_date=result.start_date,
            end_date=result.end_date,
            status=result.status,
            questionnaire_id=result.questionnaire_id,
            target_groups=result.target_groups,
            is_anonymous=result.is_anonymous,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except EvaluationPeriodNotFoundError as e:
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
    "/{period_id}",
    response_model=EvaluationPeriodResponseSchema,
    summary="Actualizar período de evaluación",
    description="Actualiza un período de evaluación existente"
)
async def update_evaluation_period(
    period_id: UUID,
    period_data: EvaluationPeriodUpdateSchema,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Actualizar período de evaluación existente.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **period_id**: ID único del período
    - **name**: Nuevo nombre del período (opcional)
    - **description**: Nueva descripción (opcional)
    - **start_date**: Nueva fecha de inicio (opcional)
    - **end_date**: Nueva fecha de fin (opcional)
    - **target_groups**: Nuevos grupos objetivo (opcional)
    
    **Nota:** Solo se pueden modificar períodos en estado DRAFT.
    """
    try:
        use_case = container.get_update_evaluation_period_use_case(db)
        
        from ...application.dtos.period_dtos import UpdateEvaluationPeriodRequest
        request = UpdateEvaluationPeriodRequest(
            name=period_data.name,
            description=period_data.description,
            start_date=period_data.start_date,
            end_date=period_data.end_date,
            target_groups=period_data.target_groups
        )
        
        result = await use_case.execute(period_id, request)
        
        return EvaluationPeriodResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            start_date=result.start_date,
            end_date=result.end_date,
            status=result.status,
            questionnaire_id=result.questionnaire_id,
            target_groups=result.target_groups,
            is_anonymous=result.is_anonymous,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except EvaluationPeriodNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except EvaluationPeriodInvalidStateError as e:
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
    "/{period_id}/close",
    response_model=EvaluationPeriodResponseSchema,
    summary="Cerrar período de evaluación",
    description="Cierra un período de evaluación activo"
)
async def close_evaluation_period(
    period_id: UUID,
    current_user: CurrentUser = Depends(get_admin_user),
    db: Session = Depends(container.get_db_session)
):
    """
    Cerrar período de evaluación.
    
    **Permisos requeridos:** Administrador
    
    **Parámetros:**
    - **period_id**: ID único del período a cerrar
    
    **Funcionalidad:**
    - Cambia el estado del período a CLOSED
    - Envía notificaciones a administradores
    - El período no puede ser modificado después del cierre
    """
    try:
        use_case = container.get_close_evaluation_period_use_case(db)
        result = await use_case.execute(period_id)
        
        return EvaluationPeriodResponseSchema(
            id=result.id,
            name=result.name,
            description=result.description,
            start_date=result.start_date,
            end_date=result.end_date,
            status=result.status,
            questionnaire_id=result.questionnaire_id,
            target_groups=result.target_groups,
            is_anonymous=result.is_anonymous,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
    except EvaluationPeriodNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except EvaluationPeriodInvalidStateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
