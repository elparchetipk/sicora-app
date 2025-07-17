"""Dependency injection configuration for AI Service - Simplified Version."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.config import get_settings
from app.infrastructure.config.database import get_db_session
from app.infrastructure.repositories.conversation_repository_impl import (
    SQLAlchemyConversationRepository
)
from app.infrastructure.repositories.knowledge_repository_impl import (
    SQLAlchemyKnowledgeRepository
)
from app.infrastructure.repositories.ai_model_repository_impl import (
    SQLAlchemyAIModelRepository
)
from app.domain.repositories.conversation_repository import (
    ConversationRepository
)
from app.domain.repositories.knowledge_repository import KnowledgeRepository
from app.domain.repositories.ai_model_repository import AIModelRepository

from app.application.use_cases.chat_use_cases import (
    ChatUseCase, ConversationManagementUseCase
)
from app.application.use_cases.knowledge_use_cases import (
    KnowledgeManagementUseCase
)
from app.application.use_cases.ai_model_use_cases import (
    AIModelManagementUseCase
)
from app.application.use_cases.analytics_use_cases import AnalyticsUseCase

# Enhanced Chat Service Dependencies
from app.application.services.enhanced_chat_service import EnhancedChatService
from app.infrastructure.integrations.kb_integration import (
    KbServiceIntegration
)
from app.infrastructure.external.simple_openai_client import (
    SimpleOpenAIClient
)


async def get_conversation_repository(
    session: AsyncSession = Depends(get_db_session)
) -> AsyncGenerator[ConversationRepository, None]:
    """Get conversation repository dependency."""
    yield SQLAlchemyConversationRepository(session)


async def get_knowledge_repository(
    session: AsyncSession = Depends(get_db_session)
) -> AsyncGenerator[KnowledgeRepository, None]:
    """Get knowledge repository dependency."""
    yield SQLAlchemyKnowledgeRepository(session)


async def get_ai_model_repository(
    session: AsyncSession = Depends(get_db_session)
) -> AsyncGenerator[AIModelRepository, None]:
    """Get AI model repository dependency."""
    yield SQLAlchemyAIModelRepository(session)


# Use Case Dependencies
async def get_chat_use_case(
    conversation_repo: ConversationRepository = Depends(
        get_conversation_repository
    ),
    ai_model_repo: AIModelRepository = Depends(get_ai_model_repository)
) -> ChatUseCase:
    """Get chat use case dependency."""
    return ChatUseCase(
        conversation_repository=conversation_repo,
        ai_model_repository=ai_model_repo
    )


async def get_conversation_management_use_case(
    conversation_repo: ConversationRepository = Depends(
        get_conversation_repository
    )
) -> ConversationManagementUseCase:
    """Get conversation management use case dependency."""
    return ConversationManagementUseCase(
        conversation_repository=conversation_repo
    )


async def get_knowledge_management_use_case(
    knowledge_repo: KnowledgeRepository = Depends(get_knowledge_repository)
) -> KnowledgeManagementUseCase:
    """Get knowledge management use case dependency."""
    return KnowledgeManagementUseCase(knowledge_repository=knowledge_repo)


async def get_ai_model_management_use_case(
    ai_model_repo: AIModelRepository = Depends(get_ai_model_repository)
) -> AIModelManagementUseCase:
    """Get AI model management use case dependency."""
    return AIModelManagementUseCase(ai_model_repository=ai_model_repo)


async def get_analytics_use_case(
    conversation_repo: ConversationRepository = Depends(
        get_conversation_repository
    )
) -> AnalyticsUseCase:
    """Get analytics use case dependency."""
    return AnalyticsUseCase(conversation_repository=conversation_repo)


# Enhanced Chat Service Dependencies
async def get_kb_integration() -> KbServiceIntegration:
    """Get KbService integration dependency."""
    settings = get_settings()
    kb_service_url = getattr(
        settings, 'KB_SERVICE_URL', 'http://kbservice:8006/api/v1'
    )
    return KbServiceIntegration(kb_service_url=kb_service_url)


async def get_openai_client() -> SimpleOpenAIClient:
    """Get OpenAI client dependency (using simple mock client for testing)."""
    settings = get_settings()
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    organization = getattr(settings, 'OPENAI_ORGANIZATION', None)
    
    # Note: API key no es requerida para el cliente mock
    return SimpleOpenAIClient(api_key=api_key, organization=organization)


async def get_enhanced_chat_service(
    kb_integration: KbServiceIntegration = Depends(get_kb_integration),
    openai_client: SimpleOpenAIClient = Depends(get_openai_client)
) -> EnhancedChatService:
    """Get enhanced chat service dependency."""
    return EnhancedChatService(
        kb_integration=kb_integration,
        openai_client=openai_client
    )
