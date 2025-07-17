from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ..schemas import (
    EvaluationCreateSchema,
    EvaluationResponseSchema,
    EvaluationStartSchema,
    EvaluationCompleteSchema,
    EvaluationVoiceNoteSchema,
    EvaluationListResponseSchema,
)
from ...application.use_cases.evaluation_use_cases import (
    CreateEvaluationUseCase,
    StartEvaluationUseCase,
    CompleteEvaluationUseCase,
    AddVoiceNotesToEvaluationUseCase,
    GetEvaluationUseCase,
    GetProjectEvaluationsUseCase,
    GetScheduledEvaluationsUseCase,
    GetEvaluationsByPeriodUseCase,
    RescheduleEvaluationUseCase,
)
from ...infrastructure.database import get_async_db
from ...infrastructure.repositories import SQLAlchemyEvaluationRepository
from sqlalchemy.ext.asyncio import AsyncSession
import math

router = APIRouter(prefix="/api/v1/evaluations", tags=["evaluations"])


# Dependency to get evaluation repository
async def get_evaluation_repository(
    db: AsyncSession = Depends(get_async_db),
) -> SQLAlchemyEvaluationRepository:
    return SQLAlchemyEvaluationRepository(db)


@router.post(
    "/", response_model=EvaluationResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_evaluation(
    evaluation_data: EvaluationCreateSchema,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Create a new evaluation session"""
    try:
        use_case = CreateEvaluationUseCase(evaluation_repo)
        evaluation = await use_case.execute(
            project_id=evaluation_data.project_id,
            evaluation_type=evaluation_data.evaluation_type,
            trimester=evaluation_data.trimester,
            academic_year=evaluation_data.academic_year,
            scheduled_date=evaluation_data.scheduled_date,
            duration_minutes=evaluation_data.duration_minutes,
            location=evaluation_data.location,
            created_by=evaluation_data.created_by,
        )
        return EvaluationResponseSchema.from_orm(evaluation)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating evaluation: {str(e)}",
        )


@router.get("/{evaluation_id}", response_model=EvaluationResponseSchema)
async def get_evaluation(
    evaluation_id: UUID,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Get evaluation by ID"""
    use_case = GetEvaluationUseCase(evaluation_repo)
    evaluation = await use_case.execute(evaluation_id)

    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found"
        )

    return EvaluationResponseSchema.from_orm(evaluation)


@router.post("/{evaluation_id}/start", response_model=EvaluationResponseSchema)
async def start_evaluation(
    evaluation_id: UUID,
    start_data: EvaluationStartSchema,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Start an evaluation session"""
    try:
        use_case = StartEvaluationUseCase(evaluation_repo)
        evaluation = await use_case.execute(evaluation_id, start_data.evaluator_id)

        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found"
            )

        return EvaluationResponseSchema.from_orm(evaluation)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{evaluation_id}/complete", response_model=EvaluationResponseSchema)
async def complete_evaluation(
    evaluation_id: UUID,
    complete_data: EvaluationCompleteSchema,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Complete an evaluation with scores and feedback"""
    try:
        use_case = CompleteEvaluationUseCase(evaluation_repo)
        evaluation = await use_case.execute(
            evaluation_id=evaluation_id,
            technical_score=complete_data.scores.technical_score,
            presentation_score=complete_data.scores.presentation_score,
            documentation_score=complete_data.scores.documentation_score,
            innovation_score=complete_data.scores.innovation_score,
            collaboration_score=complete_data.scores.collaboration_score,
            general_comments=complete_data.feedback.general_comments,
            technical_feedback=complete_data.feedback.technical_feedback,
            presentation_feedback=complete_data.feedback.presentation_feedback,
            improvement_suggestions=complete_data.feedback.improvement_suggestions,
        )

        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found"
            )

        return EvaluationResponseSchema.from_orm(evaluation)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{evaluation_id}/voice-notes", response_model=EvaluationResponseSchema)
async def add_voice_notes(
    evaluation_id: UUID,
    voice_note_data: EvaluationVoiceNoteSchema,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Add voice notes and transcript to evaluation"""
    try:
        use_case = AddVoiceNotesToEvaluationUseCase(evaluation_repo)
        evaluation = await use_case.execute(
            evaluation_id=evaluation_id,
            voice_url=voice_note_data.voice_url,
            transcript=voice_note_data.transcript,
        )

        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found"
            )

        return EvaluationResponseSchema.from_orm(evaluation)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error adding voice notes: {str(e)}",
        )


@router.get("/project/{project_id}", response_model=List[EvaluationResponseSchema])
async def get_project_evaluations(
    project_id: UUID,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Get all evaluations for a project"""
    use_case = GetProjectEvaluationsUseCase(evaluation_repo)
    evaluations = await use_case.execute(project_id)

    return [EvaluationResponseSchema.from_orm(evaluation) for evaluation in evaluations]


@router.get("/scheduled", response_model=List[EvaluationResponseSchema])
async def get_scheduled_evaluations(
    evaluator_id: Optional[UUID] = None,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Get scheduled evaluations, optionally filtered by evaluator"""
    use_case = GetScheduledEvaluationsUseCase(evaluation_repo)
    evaluations = await use_case.execute(evaluator_id)

    return [EvaluationResponseSchema.from_orm(evaluation) for evaluation in evaluations]


@router.get(
    "/period/{academic_year}/{trimester}", response_model=List[EvaluationResponseSchema]
)
async def get_evaluations_by_period(
    academic_year: int,
    trimester: int,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Get evaluations by academic period"""
    use_case = GetEvaluationsByPeriodUseCase(evaluation_repo)
    evaluations = await use_case.execute(academic_year, trimester)

    return [EvaluationResponseSchema.from_orm(evaluation) for evaluation in evaluations]


@router.post("/{evaluation_id}/reschedule", response_model=EvaluationResponseSchema)
async def reschedule_evaluation(
    evaluation_id: UUID,
    new_date: datetime,
    reason: str,
    evaluation_repo: SQLAlchemyEvaluationRepository = Depends(get_evaluation_repository),
):
    """Reschedule an evaluation"""
    try:
        use_case = RescheduleEvaluationUseCase(evaluation_repo)
        evaluation = await use_case.execute(evaluation_id, new_date, reason)

        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found"
            )

        return EvaluationResponseSchema.from_orm(evaluation)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error rescheduling evaluation: {str(e)}",
        )
