"""
Enhanced Chat Router - Simplificado
Router para el servicio de chat mejorado con integración KBService
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
import logging
from datetime import datetime
from uuid import UUID

from app.dependencies import get_enhanced_chat_service, get_current_user
from app.application.services.enhanced_chat_service import EnhancedChatService
from app.application.dtos.ai_dtos import EnhancedChatRequestDTO

from app.presentation.schemas.chat_schemas import (
    EnhancedChatRequest,
    EnhancedChatResponse,
    QuickAnswerRequest,
    KnowledgeSearchRequest,
    HealthCheckResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/enhanced",
    response_model=EnhancedChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat Mejorado con Base de Conocimiento",
    description="Generar respuestas inteligentes usando KB."
)
async def enhanced_chat(
    request: EnhancedChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    enhanced_chat_service: EnhancedChatService = Depends(
        get_enhanced_chat_service
    )
) -> EnhancedChatResponse:
    """
    Endpoint principal para chat mejorado con contexto de KB.
    """
    try:
        logger.info(f"Enhanced chat request: {request.message[:50]}...")
        
        # Convertir schema a DTO
        dto_request = EnhancedChatRequestDTO(
            message=request.message,
            conversation_id=request.conversation_id,
            user_id=UUID(current_user["user_id"]),
            use_knowledge_base=request.use_knowledge_base,
            search_categories=request.search_categories,
            context_limit=request.context_limit,
            model_name=request.model_name,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            metadata=request.metadata
        )
        
        # Generar respuesta usando el servicio mejorado
        response_message = await (
            enhanced_chat_service.generate_enhanced_response(
                dto_request,
                []  # Historial vacío por simplicidad
            )
        )
        
        # Construir respuesta
        metadata = response_message.metadata or {}
        
        return EnhancedChatResponse(
            message=response_message.content,
            conversation_id=request.conversation_id,
            model_used=metadata.get("model_used", "mock"),
            tokens_used=metadata.get("tokens_used", 100),
            processing_time=metadata.get("processing_time", 0.5),
            knowledge_sources_used=metadata.get("knowledge_sources", 0),
            context_categories=metadata.get("context_categories", []),
            metadata=metadata,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error in enhanced chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating enhanced response: {str(e)}"
        )


@router.post(
    "/quick-answer",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Respuestas Rápidas FAQ",
    description="Obtener respuestas rápidas para preguntas frecuentes."
)
async def quick_answer(
    request: QuickAnswerRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    enhanced_chat_service: EnhancedChatService = Depends(
        get_enhanced_chat_service
    )
) -> Dict[str, Any]:
    """
    Endpoint para respuestas rápidas a preguntas frecuentes.
    """
    try:
        # Buscar en la base de conocimiento
        results = await enhanced_chat_service.kb_integration.search_knowledge(
            query=request.question,
            user_id=UUID(current_user["user_id"]),
            limit=3
        )
        
        if not results:
            return {
                "answer": "No se encontró información específica.",
                "confidence": 0.0,
                "sources": []
            }
        
        # Tomar la primera respuesta como la más relevante
        best_result = results[0]
        content = best_result.content
        if len(content) > 500:
            content = content[:500] + "..."
        
        return {
            "answer": content,
            "confidence": getattr(best_result, 'relevance_score', 0.8),
            "category": request.category,
            "sources": [
                {
                    "id": best_result.id,
                    "title": best_result.title,
                    "type": best_result.content_type
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in quick answer: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting quick answer: {str(e)}"
        )


@router.post(
    "/search",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Búsqueda en Base de Conocimiento",
    description="Buscar información específica en la base de conocimiento."
)
async def knowledge_search(
    request: KnowledgeSearchRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    enhanced_chat_service: EnhancedChatService = Depends(
        get_enhanced_chat_service
    )
) -> Dict[str, Any]:
    """
    Endpoint para búsqueda directa en la base de conocimiento.
    """
    try:
        results = await enhanced_chat_service.kb_integration.search_knowledge(
            query=request.query,
            user_id=UUID(current_user["user_id"]),
            limit=request.limit
        )
        
        return {
            "query": request.query,
            "total_results": len(results),
            "results": [
                {
                    "id": result.id,
                    "title": result.title,                    "content": (
                        result.content[:300] + "..."
                        if len(result.content) > 300
                        else result.content
                    ),
                    "score": getattr(result, 'relevance_score', 0.8),
                    "type": result.content_type,
                    "category": result.category
                }
                for result in results
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in knowledge search: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching knowledge base: {str(e)}"
        )


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check del Chat Mejorado",
    description="Verificar el estado del servicio de chat mejorado."
)
async def chat_health_check(
    enhanced_chat_service: EnhancedChatService = Depends(
        get_enhanced_chat_service
    )
) -> HealthCheckResponse:
    """
    Health check específico para el servicio de chat mejorado.
    """
    try:
        # Verificar conexión con KBService
        kb_status = await enhanced_chat_service.kb_integration.health_check()
        
        # Verificar cliente OpenAI (mock)
        openai_status = enhanced_chat_service.openai_client.is_available()
        
        status_message = "Enhanced chat service operational"
        if not kb_status:
            status_message += " (KB service warning)"
        if not openai_status:
            status_message += " (OpenAI client warning)"
        
        return HealthCheckResponse(
            status="healthy" if kb_status and openai_status else "degraded",
            message=status_message,
            service="enhanced-chat",
            version="1.0.0"
        )
        
    except Exception as e:
        logger.error(f"Enhanced chat health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Enhanced chat service unhealthy: {str(e)}"
        )
