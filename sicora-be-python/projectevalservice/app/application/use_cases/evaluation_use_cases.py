from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime

from ...domain.entities import Evaluation, EvaluationStatus, EvaluationType
from ...domain.repositories import EvaluationRepository
from ...domain.value_objects import EvaluationScore


class CreateEvaluationUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(
        self,
        project_id: UUID,
        evaluation_type: EvaluationType,
        trimester: int,
        academic_year: int,
        scheduled_date: datetime,
        duration_minutes: int,
        location: str,
        created_by: UUID,
    ) -> Evaluation:
        """Create a new evaluation"""

        evaluation = Evaluation(
            id=UUID(),
            project_id=project_id,
            evaluation_type=evaluation_type,
            status=EvaluationStatus.SCHEDULED,
            trimester=trimester,
            academic_year=academic_year,
            scheduled_date=scheduled_date,
            actual_date=None,
            duration_minutes=duration_minutes,
            location=location,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by=created_by,
        )

        return await self.evaluation_repository.create(evaluation)


class StartEvaluationUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(
        self, evaluation_id: UUID, evaluator_id: UUID
    ) -> Optional[Evaluation]:
        """Start an evaluation session"""

        evaluation = await self.evaluation_repository.get_by_id(evaluation_id)
        if not evaluation:
            return None

        if evaluation.status != EvaluationStatus.SCHEDULED:
            raise ValueError("Evaluation is not in scheduled status")

        evaluation.start_evaluation(evaluator_id)

        return await self.evaluation_repository.update(evaluation)


class CompleteEvaluationUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(
        self,
        evaluation_id: UUID,
        technical_score: float,
        presentation_score: float,
        documentation_score: float,
        innovation_score: float,
        collaboration_score: float,
        general_comments: Optional[str] = None,
        technical_feedback: Optional[str] = None,
        presentation_feedback: Optional[str] = None,
        improvement_suggestions: Optional[str] = None,
    ) -> Optional[Evaluation]:
        """Complete an evaluation with scores and feedback"""

        evaluation = await self.evaluation_repository.get_by_id(evaluation_id)
        if not evaluation:
            return None

        if evaluation.status != EvaluationStatus.IN_PROGRESS:
            raise ValueError("Evaluation is not in progress")

        # Validate scores
        scores = {
            "technical": technical_score,
            "presentation": presentation_score,
            "documentation": documentation_score,
            "innovation": innovation_score,
            "collaboration": collaboration_score,
        }

        feedback = {
            "general_comments": general_comments,
            "technical_feedback": technical_feedback,
            "presentation_feedback": presentation_feedback,
            "improvement_suggestions": improvement_suggestions,
        }

        evaluation.complete_evaluation(scores, feedback)

        return await self.evaluation_repository.update(evaluation)


class AddVoiceNotesToEvaluationUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(
        self, evaluation_id: UUID, voice_url: str, transcript: str
    ) -> Optional[Evaluation]:
        """Add voice notes and transcript to evaluation"""

        evaluation = await self.evaluation_repository.get_by_id(evaluation_id)
        if not evaluation:
            return None

        evaluation.add_voice_notes(voice_url, transcript)

        return await self.evaluation_repository.update(evaluation)


class GetEvaluationUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(self, evaluation_id: UUID) -> Optional[Evaluation]:
        """Get evaluation by ID"""
        return await self.evaluation_repository.get_by_id(evaluation_id)


class GetProjectEvaluationsUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(self, project_id: UUID) -> List[Evaluation]:
        """Get all evaluations for a project"""
        return await self.evaluation_repository.get_by_project_id(project_id)


class GetScheduledEvaluationsUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(self, evaluator_id: Optional[UUID] = None) -> List[Evaluation]:
        """Get scheduled evaluations, optionally filtered by evaluator"""
        return await self.evaluation_repository.get_scheduled_evaluations(evaluator_id)


class GetEvaluationsByPeriodUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(self, academic_year: int, trimester: int) -> List[Evaluation]:
        """Get evaluations by academic period"""
        return await self.evaluation_repository.get_evaluations_by_period(
            academic_year, trimester
        )


class RescheduleEvaluationUseCase:
    def __init__(self, evaluation_repository: EvaluationRepository):
        self.evaluation_repository = evaluation_repository

    async def execute(
        self, evaluation_id: UUID, new_date: datetime, reason: str
    ) -> Optional[Evaluation]:
        """Reschedule an evaluation"""

        evaluation = await self.evaluation_repository.get_by_id(evaluation_id)
        if not evaluation:
            return None

        evaluation.reschedule(new_date, reason)

        return await self.evaluation_repository.update(evaluation)
