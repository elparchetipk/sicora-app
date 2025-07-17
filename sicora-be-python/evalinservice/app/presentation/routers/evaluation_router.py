from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.domain.exceptions.evaluation_exceptions import (
    EvaluationNotFoundError,
    EvaluationPeriodNotActive,
    DuplicateEvaluation,
    IncompleteEvaluationError,
    InvalidEvaluationData,
    EvaluationNotInProgress
)
from app.presentation.dependencies.auth import get_current_user, require_role, CurrentUser
from app.presentation.dependencies.container import get_create_evaluation_use_case, get_get_evaluation_by_id_use_case, get_get_evaluations_use_case
from app.presentation.schemas.evaluation_schemas import (
    EvaluationCreateSchema,
    EvaluationResponseSchema
)

from app.application.use_cases.create_evaluation_use_case import CreateEvaluationUseCase
from app.application.use_cases.get_evaluation_by_id_use_case import GetEvaluationByIdUseCase
from app.application.use_cases.get_evaluations_use_case import GetEvaluationsUseCase

router = APIRouter(
    prefix="/evaluations",
    tags=["evaluations"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=EvaluationResponseSchema, status_code=status.HTTP_201_CREATED)
async def submit_evaluation(
    evaluation_data: EvaluationCreateSchema,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: CreateEvaluationUseCase = Depends(get_create_evaluation_use_case)
):
    """
    Enviar una evaluación de instructor.
    Solo los estudiantes pueden enviar evaluaciones.
    """
    require_role(current_user, ["student"])
    
    try:
        evaluation = use_case.execute(
            student_id=current_user.user_id,
            instructor_id=evaluation_data.instructor_id,
            period_id=evaluation_data.period_id,
            responses=evaluation_data.responses
        )
        
        return EvaluationResponseSchema(
            id=evaluation.id,
            student_id=evaluation.student_id,
            instructor_id=evaluation.instructor_id,
            period_id=evaluation.period_id,
            responses=evaluation.responses,
            status=evaluation.status.value,
            submitted_at=evaluation.submitted_at,
            created_at=evaluation.created_at,
            updated_at=evaluation.updated_at
        )
    
    except EvaluationPeriodNotActive as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Evaluation period not active: {str(e)}"
        )
    except DuplicateEvaluation as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Duplicate evaluation: {str(e)}"
        )
    except IncompleteEvaluationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incomplete evaluation: {str(e)}"
        )
    except InvalidEvaluationData as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid evaluation data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{evaluation_id}", response_model=EvaluationResponseSchema)
async def get_evaluation(
    evaluation_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: GetEvaluationByIdUseCase = Depends(get_get_evaluation_by_id_use_case)
):
    """
    Obtener una evaluación específica por ID.
    Los administradores pueden ver cualquier evaluación.
    Los estudiantes solo pueden ver sus propias evaluaciones.
    Los instructores pueden ver las evaluaciones que les corresponden.
    """
    try:
        evaluation = use_case.execute(evaluation_id)
        
        if current_user.role not in ["admin", "coordinator"]:
            if current_user.role == "student" and evaluation.student_id != current_user.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You can only view your own evaluations"
                )
            elif current_user.role == "instructor" and evaluation.instructor_id != current_user.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You can only view evaluations about yourself"
                )
        
        return EvaluationResponseSchema(
            id=evaluation.id,
            student_id=evaluation.student_id,
            instructor_id=evaluation.instructor_id,
            period_id=evaluation.period_id,
            responses=evaluation.responses,
            status=evaluation.status.value,
            submitted_at=evaluation.submitted_at,
            created_at=evaluation.created_at,
            updated_at=evaluation.updated_at
        )
    
    except EvaluationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/", response_model=List[EvaluationResponseSchema])
async def get_evaluations(
    current_user: CurrentUser = Depends(get_current_user),
    period_id: UUID = Query(None, description="Filter by evaluation period"),
    instructor_id: UUID = Query(None, description="Filter by instructor"),
    status: str = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0, description="Number of evaluations to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of evaluations to retrieve"),
    use_case: GetEvaluationsUseCase = Depends(get_get_evaluations_use_case)
):
    """
    Obtener lista de evaluaciones.
    Los filtros disponibles dependen del rol del usuario.
    """
    try:
        if current_user.role == "student":
            evaluations = use_case.execute(
                student_id=current_user.user_id,
                period_id=period_id,
                instructor_id=instructor_id,
                status=status
            )
        elif current_user.role == "instructor":
            if instructor_id and instructor_id != current_user.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You can only view evaluations about yourself"
                )
            evaluations = use_case.execute(
                student_id=None,
                period_id=period_id,
                instructor_id=current_user.user_id,
                status=status
            )
        else:
            evaluations = use_case.execute(
                student_id=None,
                period_id=period_id,
                instructor_id=instructor_id,
                status=status
            )
        
        paginated_evaluations = evaluations[skip:skip + limit]
        
        return [
            EvaluationResponseSchema(
                id=evaluation.id,
                student_id=evaluation.student_id,
                instructor_id=evaluation.instructor_id,
                period_id=evaluation.period_id,
                responses=evaluation.responses,
                status=evaluation.status.value,
                submitted_at=evaluation.submitted_at,
                created_at=evaluation.created_at,
                updated_at=evaluation.updated_at
            )
            for evaluation in paginated_evaluations
        ]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{evaluation_id}", response_model=EvaluationResponseSchema)
async def update_evaluation(
    evaluation_id: UUID,
    evaluation_data: EvaluationCreateSchema,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: CreateEvaluationUseCase = Depends(get_create_evaluation_use_case),
    get_evaluation_use_case: GetEvaluationByIdUseCase = Depends(get_get_evaluation_by_id_use_case)
):
    """
    Actualizar una evaluación existente.
    Solo los estudiantes pueden actualizar sus propias evaluaciones en estado draft.
    """
    require_role(current_user, ["student"])
    
    try:
        existing_evaluation = get_evaluation_use_case.execute(evaluation_id)
        
        if existing_evaluation.student_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only update your own evaluations"
            )
        
        if existing_evaluation.status.value != "draft":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update evaluation: Only draft evaluations can be modified"
            )
        
        updated_evaluation = use_case.execute(
            student_id=current_user.user_id,
            instructor_id=existing_evaluation.instructor_id,
            period_id=existing_evaluation.period_id,
            responses=evaluation_data.responses,
            evaluation_id=evaluation_id
        )
        
        return EvaluationResponseSchema(
            id=updated_evaluation.id,
            student_id=updated_evaluation.student_id,
            instructor_id=updated_evaluation.instructor_id,
            period_id=updated_evaluation.period_id,
            responses=updated_evaluation.responses,
            status=updated_evaluation.status.value,
            submitted_at=updated_evaluation.submitted_at,
            created_at=updated_evaluation.created_at,
            updated_at=updated_evaluation.updated_at
        )
    
    except EvaluationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation not found: {str(e)}"
        )
    except EvaluationNotInProgress as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update evaluation: {str(e)}"
        )
    except InvalidEvaluationData as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid evaluation data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete("/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_evaluation(
    evaluation_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    get_evaluation_use_case: GetEvaluationByIdUseCase = Depends(get_get_evaluation_by_id_use_case)
):
    """
    Eliminar una evaluación.
    Solo los administradores pueden eliminar evaluaciones.
    """
    require_role(current_user, ["admin", "coordinator"])
    
    try:
        evaluation = get_evaluation_use_case.execute(evaluation_id)
        
        if evaluation.status.value == "submitted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete submitted evaluation"
            )
        
        # TODO: Implement delete evaluation use case
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Delete evaluation functionality not implemented yet"
        )
    
    except EvaluationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
