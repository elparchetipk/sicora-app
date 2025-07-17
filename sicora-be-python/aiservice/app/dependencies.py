"""Dependency injection configuration for AI Service."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.config import get_settings
from app.infrastructure.config.database import get_db_session
from app.infrastructure.repositories.conversation_repository_impl import SQLAlchemyConversationRepository
from app.infrastructure.repositories.knowledge_repository_impl import SQLAlchemyKnowledgeRepository
from app.infrastructure.repositories.ai_model_repository_impl import SQLAlchemyAIModelRepository
from app.domain.repositories.conversation_repository import ConversationRepository
from app.domain.repositories.knowledge_repository import KnowledgeRepository
from app.domain.repositories.ai_model_repository import AIModelRepository

from app.application.interfaces.ai_provider_interface import AIProviderInterface
from app.application.interfaces.vector_store_interface import VectorStoreInterface
from app.application.interfaces.cache_interface import CacheInterface

from app.application.use_cases.chat_use_cases import ChatUseCase, ConversationManagementUseCase
from app.application.use_cases.knowledge_use_cases import KnowledgeManagementUseCase
from app.application.use_cases.ai_model_use_cases import AIModelManagementUseCase
from app.application.use_cases.analytics_use_cases import AnalyticsUseCase

from app.infrastructure.adapters.factory import (
    ai_service_factory,
    AIProviderType,
    VectorStoreType,
    CacheType
)

# Enhanced Chat Service Dependencies
from app.application.services.enhanced_chat_service import EnhancedChatService
from app.infrastructure.integrations.kb_integration import KbServiceIntegration
from app.infrastructure.external.simple_openai_client import SimpleOpenAIClient


async def get_conversation_repository(
    session: AsyncSession = Depends(get_db_session)
) -> ConversationRepository:
    """Get conversation repository dependency."""
    return SQLAlchemyConversationRepository(session)


async def get_knowledge_repository(
    session: AsyncSession = Depends(get_db_session)
) -> KnowledgeRepository:
    """Get knowledge repository dependency."""
    return SQLAlchemyKnowledgeRepository(session)


async def get_ai_model_repository(
    session: AsyncSession = Depends(get_db_session)
) -> AIModelRepository:
    """Get AI model repository dependency."""
    return SQLAlchemyAIModelRepository(session)


def get_openai_provider() -> AIProviderInterface:
    """Get OpenAI provider dependency."""
    settings = get_settings()

    config = {
        "api_key": getattr(settings, 'OPENAI_API_KEY', None),
        "organization": getattr(settings, 'OPENAI_ORGANIZATION', None)
    }

    return ai_service_factory.create_ai_provider(
        AIProviderType.OPENAI,
        config,
        "default"
    )


def get_anthropic_provider() -> AIProviderInterface:
    """Get Anthropic provider dependency."""
    settings = get_settings()

    config = {
        "api_key": getattr(settings, 'ANTHROPIC_API_KEY', None)
    }

    return ai_service_factory.create_ai_provider(
        AIProviderType.ANTHROPIC,
        config,
        "default"
    )


def get_huggingface_provider() -> AIProviderInterface:
    """Get Hugging Face provider dependency."""
    settings = get_settings()

    config = {
        "device": getattr(settings, 'huggingface_device', 'auto')
    }

    return ai_service_factory.create_ai_provider(
        AIProviderType.HUGGINGFACE,
        config,
        "default"
    )


def get_vector_store() -> VectorStoreInterface:
    """Get vector store dependency."""
    settings = get_settings()

    config = {
        "host": getattr(settings, 'CHROMADB_HOST', 'localhost'),
        "port": getattr(settings, 'CHROMADB_PORT', 8000),
        "collection_name": getattr(settings, 'CHROMADB_COLLECTION', 'knowledge_base'),
        "persist_directory": getattr(settings, 'CHROMADB_PATH', './chromadb')
    }

    return ai_service_factory.create_vector_store(
        VectorStoreType.CHROMADB,
        config,
        "default"
    )


def get_cache() -> CacheInterface:
    """Get cache dependency."""
    settings = get_settings()

    config = {
        "host": getattr(settings, 'REDIS_HOST', 'localhost'),
        "port": getattr(settings, 'REDIS_PORT', 6379),
        "db": getattr(settings, 'REDIS_DB', 0),
        "password": getattr(settings, 'REDIS_PASSWORD', None),
        "max_connections": getattr(settings, 'REDIS_MAX_CONNECTIONS', 10),
        "key_prefix": getattr(settings, 'REDIS_KEY_PREFIX', 'aiservice:')
    }

    return ai_service_factory.create_cache(
        CacheType.REDIS,
        config,
        "default"
    )


# Use Case Dependencies
async def get_chat_use_case(
    conversation_repo: ConversationRepository = Depends(get_conversation_repository),
    ai_model_repo: AIModelRepository = Depends(get_ai_model_repository),
    knowledge_repo: KnowledgeRepository = Depends(get_knowledge_repository),
    ai_provider: AIProviderInterface = Depends(get_openai_provider),
    vector_store: VectorStoreInterface = Depends(get_vector_store),
    cache: CacheInterface = Depends(get_cache)
) -> ChatUseCase:
    """Get chat use case dependency."""
    from app.application.use_cases.chat_use_cases import ChatUseCase
    return ChatUseCase(
        conversation_repo=conversation_repo,
        ai_model_repo=ai_model_repo,
        knowledge_repo=knowledge_repo,
        ai_provider=ai_provider,
        vector_store=vector_store,
        cache=cache
    )


async def get_knowledge_use_case(
    knowledge_repo: KnowledgeRepository = Depends(get_knowledge_repository),
    ai_provider: AIProviderInterface = Depends(get_openai_provider),
    vector_store: VectorStoreInterface = Depends(get_vector_store),
    cache: CacheInterface = Depends(get_cache)
) -> KnowledgeManagementUseCase:
    """Get knowledge use case dependency."""
    return KnowledgeManagementUseCase(
        knowledge_repo=knowledge_repo,
        ai_provider=ai_provider,
        vector_store=vector_store,
        cache=cache
    )


async def get_ai_model_use_case(
    ai_model_repo: AIModelRepository = Depends(get_ai_model_repository),
    ai_provider: AIProviderInterface = Depends(get_openai_provider),
    cache: CacheInterface = Depends(get_cache)
) -> AIModelManagementUseCase:
    """Get AI model use case dependency."""
    return AIModelManagementUseCase(
        ai_model_repo=ai_model_repo,
        ai_provider=ai_provider,
        cache=cache
    )


async def get_analytics_use_case(
    conversation_repo: ConversationRepository = Depends(get_conversation_repository),
    ai_model_repo: AIModelRepository = Depends(get_ai_model_repository),
    knowledge_repo: KnowledgeRepository = Depends(get_knowledge_repository),
    cache: CacheInterface = Depends(get_cache)
) -> AnalyticsUseCase:
    """Get analytics use case dependency."""
    return AnalyticsUseCase(
        conversation_repo=conversation_repo,
        ai_model_repo=ai_model_repo,
        knowledge_repo=knowledge_repo,
        cache=cache
    )


async def get_conversation_management_use_case(
    conversation_repo: ConversationRepository = Depends(get_conversation_repository)
) -> ConversationManagementUseCase:
    """Get conversation management use case dependency."""
    return ConversationManagementUseCase(
        conversation_repo=conversation_repo
    )


async def get_kb_integration() -> KbServiceIntegration:
    """Get KbService integration dependency."""
    settings = get_settings()
    kb_service_url = getattr(settings, 'KB_SERVICE_URL', 'http://kbservice:8006/api/v1')
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


async def get_current_user():
    """Get current user dependency - mock implementation."""
    # TODO: Implement proper authentication
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "username": "test_user",
        "role": "student"
    }
