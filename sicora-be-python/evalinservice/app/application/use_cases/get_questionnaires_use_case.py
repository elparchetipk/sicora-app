"""Get Questionnaires use case."""

from typing import List, Optional

from ...domain.repositories import QuestionnaireRepositoryInterface
from ..dtos.questionnaire_dtos import QuestionnaireResponse


class GetQuestionnairesUseCase:
    """
    Caso de uso para obtener cuestionarios con filtros opcionales.
    
    Responsabilidades:
    - Obtener cuestionarios desde el repositorio
    - Aplicar filtros de estado activo si se especifica
    - Convertir entidades a DTOs de respuesta
    """
    
    def __init__(self, questionnaire_repository: QuestionnaireRepositoryInterface):
        self._questionnaire_repository = questionnaire_repository
    
    async def execute(
        self, 
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[QuestionnaireResponse]:
        """
        Ejecuta el caso de uso de obtención de cuestionarios.
        
        Args:
            is_active: Filtro por estado activo (opcional)
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
            
        Returns:
            List[QuestionnaireResponse]: Lista de cuestionarios
        """
        questionnaires = await self._questionnaire_repository.get_all(
            is_active=is_active,
            skip=skip,
            limit=limit
        )
        
        return [
            QuestionnaireResponse(
                id=questionnaire.id,
                name=questionnaire.name,
                description=questionnaire.description,
                is_active=questionnaire.is_active,
                question_count=questionnaire.get_question_count(),
                created_at=questionnaire.created_at,
                updated_at=questionnaire.updated_at,
                question_ids=questionnaire.question_ids
            )
            for questionnaire in questionnaires
        ]
