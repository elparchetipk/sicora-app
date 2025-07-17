"""
Enhanced Chat Router with KbService Integration
Router mejorado de chat con integración completa al KbService
"""
from fastapi import APIRouter, HTTPException, Depends, status, Query, Path, BackgroundTasks
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging

from app.dependencies import (
    get_chat_use_case, 
    get_conversation_management_use_case,
    get_enhanced_chat_service,
    get_current_user
)
from app.application.use_cases.chat_use_cases import ChatUseCase, ConversationManagementUseCase
from app.application.services.enhanced_chat_service import EnhancedChatService
from app.application.dtos.ai_dtos import (
    EnhancedChatRequestDTO,
    MessageDTO,
    ConversationCreateDTO
)
from app.presentation.schemas.chat_schemas import (
    ChatRequest,
    ChatResponse,
    EnhancedChatRequest,
    EnhancedChatResponse,
    ConversationCreate,
    ConversationResponse,
    ConversationWithMessages,
    MessageResponse,
    QuickAnswerRequest,
    QuickAnswerResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse
)
from app.domain.exceptions.ai_exceptions import (
    ConversationNotFoundError,
    KnowledgeBaseIntegrationError,
    ContextGenerationError,
    ModelNotAvailableError
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/enhanced",
    response_model=EnhancedChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat mejorado con base de conocimiento",
    description="""
    Endpoint principal de chat con integración completa al KbService.
    
    Características:
    - Integración automática con la base de conocimiento
    - Contexto del Reglamento del Aprendiz SENA
    - Búsqueda semántica inteligente
    - Respuestas contextualizadas
    - Historial de conversación
    """
)
async def enhanced_chat(
    request: EnhancedChatRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user),
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """Chat mejorado con integración a la base de conocimiento."""
    try:
        # Validar usuario
        user_id = UUID(current_user["user_id"])
        
        # Crear DTO para el servicio
        chat_request_dto = EnhancedChatRequestDTO(
            message=request.message,
            conversation_id=request.conversation_id,
            user_id=user_id,
            use_knowledge_base=request.use_knowledge_base,
            search_categories=request.search_categories,
            context_limit=request.context_limit,
            model_name=request.model_name,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            metadata=request.metadata
        )
        
        # Obtener historial de conversación si existe
        conversation_history = []
        if request.conversation_id:
            try:
                history = await chat_use_case.get_conversation_messages(
                    conversation_id=request.conversation_id,
                    user_id=user_id,
                    limit=10
                )
                conversation_history = history
            except ConversationNotFoundError:
                logger.warning(f"Conversation {request.conversation_id} not found")
        
        # Generar respuesta mejorada
        response_message = await enhanced_chat_service.generate_enhanced_response(
            request=chat_request_dto,
            conversation_history=conversation_history
        )
        
        # Guardar mensaje del usuario y respuesta en segundo plano
        background_tasks.add_task(
            _save_chat_messages,
            chat_use_case,
            user_id,
            request.conversation_id,
            request.message,
            response_message
        )
        
        return EnhancedChatResponse(
            message=response_message.content,
            conversation_id=request.conversation_id,
            model_used=response_message.model_used,
            tokens_used=response_message.tokens,
            processing_time=response_message.processing_time,
            knowledge_sources_used=response_message.metadata.get("knowledge_sources", 0),
            context_categories=response_message.metadata.get("context_categories", []),
            metadata=response_message.metadata,
            timestamp=response_message.timestamp
        )
        
    except KnowledgeBaseIntegrationError as e:
        logger.error(f"KB integration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Knowledge base integration failed: {str(e)}"
        )
    except ContextGenerationError as e:
        logger.error(f"Context generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to generate context: {str(e)}"
        )
    except ModelNotAvailableError as e:
        logger.error(f"Model not available: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI model not available: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Enhanced chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error in enhanced chat"
        )


@router.post(
    "/quick-answer",
    response_model=QuickAnswerResponse,
    status_code=status.HTTP_200_OK,
    summary="Respuesta rápida para FAQs",
    description="Obtener respuestas rápidas para preguntas frecuentes desde la base de conocimiento."
)
async def get_quick_answer(
    request: QuickAnswerRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Obtener respuesta rápida para preguntas frecuentes."""
    try:
        user_id = UUID(current_user["user_id"])
        
        quick_answer = await enhanced_chat_service.get_quick_answer(
            question=request.question,
            user_id=user_id,
            category=request.category
        )
        
        return QuickAnswerResponse(
            question=request.question,
            answer=quick_answer,
            category=request.category,
            found=quick_answer is not None,
            source="knowledge_base" if quick_answer else None
        )
        
    except Exception as e:
        logger.error(f"Quick answer error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get quick answer"
        )


@router.post(
    "/search-knowledge",
    response_model=KnowledgeSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar en la base de conocimiento",
    description="Buscar información específica en la base de conocimiento del sistema."
)
async def search_knowledge(
    request: KnowledgeSearchRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Buscar contenido específico en la base de conocimiento."""
    try:
        user_id = UUID(current_user["user_id"])
        
        if request.search_regulatory:
            # Búsqueda específica en reglamento
            results = await enhanced_chat_service.search_regulatory_content(
                query=request.query,
                user_id=user_id
            )
        else:
            # Búsqueda general
            results = await enhanced_chat_service.kb_integration.search_knowledge(
                query=request.query,
                user_id=user_id,
                search_type=request.search_type,
                limit=request.limit,
                category_filter=request.category
            )
        
        return KnowledgeSearchResponse(
            query=request.query,
            results=[
                {
                    "id": str(result.id),
                    "title": result.title,
                    "content": result.content[:500] + "..." if len(result.content) > 500 else result.content,
                    "category": result.category,
                    "content_type": result.content_type,
                    "relevance_score": result.relevance_score,
                    "source": result.source
                }
                for result in results
            ],
            total_results=len(results),
            search_type=request.search_type
        )
        
    except Exception as e:
        logger.error(f"Knowledge search error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search knowledge base"
        )


@router.get(
    "/health/enhanced",
    status_code=status.HTTP_200_OK,
    summary="Estado del chat mejorado",
    description="Verificar el estado del servicio de chat mejorado y sus integraciones."
)
async def enhanced_chat_health(
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Verificar estado del servicio de chat mejorado."""
    try:
        health_status = await enhanced_chat_service.health_check()
        
        if all(health_status.values()):
            return {
                "status": "healthy",
                "enhanced_chat": True,
                "integrations": health_status,
                "message": "Enhanced chat service is fully operational"
            }
        else:
            return {
                "status": "degraded",
                "enhanced_chat": True,
                "integrations": health_status,
                "message": "Some integrations are not available"
            }
            
    except Exception as e:
        logger.error(f"Enhanced chat health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Enhanced chat service health check failed"
        )


# Función auxiliar para guardar mensajes en segundo plano
async def _save_chat_messages(
    chat_use_case: ChatUseCase,
    user_id: UUID,
    conversation_id: Optional[UUID],
    user_message: str,
    assistant_message: MessageDTO
):
    """Guardar mensajes de la conversación en segundo plano."""
    try:
        # Crear conversación si no existe
        if not conversation_id:
            conversation_dto = ConversationCreateDTO(
                user_id=user_id,
                title=user_message[:50] + "..." if len(user_message) > 50 else user_message,
                initial_message=user_message
            )
            conversation = await chat_use_case.create_conversation(conversation_dto)
            conversation_id = conversation.conversation_id
        
        # Guardar mensaje del usuario
        await chat_use_case.add_message_to_conversation(
            conversation_id=conversation_id,
            message=MessageDTO(
                content=user_message,
                role="user",
                message_type="text",
                timestamp=assistant_message.timestamp
            ),
            user_id=user_id
        )
        
        # Guardar respuesta del asistente
        await chat_use_case.add_message_to_conversation(
            conversation_id=conversation_id,
            message=assistant_message,
            user_id=user_id
        )
        
    except Exception as e:
        logger.error(f"Failed to save chat messages: {str(e)}")
        # No lanzar excepción para no afectar la respuesta principal
