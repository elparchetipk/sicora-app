"""
Enhanced Chat Service with Knowledge Base Integration
Servicio de chat mejorado con integración completa a la base de conocimiento
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.infrastructure.integrations.kb_integration import KbServiceIntegration
from app.application.dtos.ai_dtos import (
    EnhancedChatRequestDTO,
    ChatContext,
    KnowledgeSearchResult,
    MessageDTO
)
from app.domain.exceptions.ai_exceptions import (
    KnowledgeBaseIntegrationError,
    ContextGenerationError,
    ModelNotAvailableError
)
from app.infrastructure.external.simple_openai_client import SimpleOpenAIClient

logger = logging.getLogger(__name__)


class EnhancedChatService:
    """
    Servicio de chat mejorado con integración completa al KbService.
    
    Proporciona respuestas inteligentes basadas en:
    - Consulta del usuario
    - Contexto de la conversación
    - Conocimiento relevante de la base de datos
    - Reglamento del Aprendiz SENA (documento principal)
    """
    
    def __init__(
        self,
        kb_integration: KbServiceIntegration,
        openai_client: SimpleOpenAIClient
    ):
        self.kb_integration = kb_integration
        self.openai_client = openai_client
        self.regulatory_context_cache: Dict[str, List[KnowledgeSearchResult]] = {}
    
    async def generate_enhanced_response(
        self,
        request: EnhancedChatRequestDTO,
        conversation_history: List[MessageDTO]
    ) -> MessageDTO:
        """
        Generar respuesta mejorada con contexto de la base de conocimiento.
        
        Args:
            request: Solicitud de chat mejorada
            conversation_history: Historial de la conversación
            
        Returns:
            Respuesta del asistente con contexto enriquecido
            
        Raises:
            KnowledgeBaseIntegrationError: Error en integración con KB
            ContextGenerationError: Error generando contexto
            ModelNotAvailableError: Modelo de IA no disponible
        """
        try:
            start_time = datetime.utcnow()
            
            # 1. Obtener contexto enriquecido de la base de conocimiento
            chat_context = None
            if request.use_knowledge_base:
                chat_context = await self._get_enhanced_context(
                    request, conversation_history
                )
            
            # 2. Construir prompt contextualizado
            system_prompt = self._build_contextual_system_prompt(
                chat_context, request.search_categories
            )
            
            # 3. Preparar historial de conversación
            conversation_messages = self._prepare_conversation_messages(
                conversation_history, system_prompt
            )
            
            # 4. Agregar mensaje del usuario
            conversation_messages.append({
                "role": "user",
                "content": request.message
            })
            
            # 5. Generar respuesta con OpenAI
            ai_response = await self.openai_client.chat_completion(
                messages=conversation_messages,
                model=request.model_name or "gpt-4",
                temperature=request.temperature or 0.7,
                max_tokens=request.max_tokens or 1000
            )
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # 6. Crear mensaje de respuesta
            response_message = MessageDTO(
                content=ai_response["choices"][0]["message"]["content"],
                role="assistant",
                message_type="text",
                tokens=ai_response.get("usage", {}).get("total_tokens"),
                metadata={
                    "model_used": ai_response.get("model"),
                    "processing_time": processing_time,
                    "knowledge_sources": len(chat_context.knowledge_results) if chat_context else 0,
                    "context_categories": chat_context.categories if chat_context else [],
                    "kb_integration_used": request.use_knowledge_base
                },
                timestamp=datetime.utcnow(),
                model_used=ai_response.get("model"),
                processing_time=processing_time
            )
            
            return response_message
            
        except Exception as e:
            logger.error(f"Error generating enhanced response: {str(e)}")
            if "knowledge" in str(e).lower():
                raise KnowledgeBaseIntegrationError(f"KB integration failed: {str(e)}")
            elif "context" in str(e).lower():
                raise ContextGenerationError(f"Context generation failed: {str(e)}")
            elif "model" in str(e).lower():
                raise ModelNotAvailableError(f"AI model error: {str(e)}")
            else:
                raise
    
    async def _get_enhanced_context(
        self,
        request: EnhancedChatRequestDTO,
        conversation_history: List[MessageDTO]
    ) -> ChatContext:
        """Obtener contexto enriquecido para la respuesta."""
        try:
            # Convertir historial de MessageDTO a dict para la integración
            history_dicts = [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
                }
                for msg in conversation_history[-5:]  # Últimos 5 mensajes
            ]
            
            # Obtener contexto completo del KbService
            context = await self.kb_integration.get_chat_context(
                user_query=request.message,
                conversation_history=history_dicts,
                user_id=request.user_id
            )
            
            return context
            
        except Exception as e:
            logger.warning(f"Failed to get enhanced context: {str(e)}")
            # Retornar contexto básico en caso de error
            return ChatContext(
                query=request.message,
                knowledge_results=[],
                conversation_history=[],
                user_id=request.user_id,
                timestamp=datetime.utcnow(),
                categories=request.search_categories or []
            )
    
    def _build_contextual_system_prompt(
        self,
        context: Optional[ChatContext],
        user_categories: Optional[List[str]] = None
    ) -> str:
        """Construir prompt del sistema con contexto de la base de conocimiento."""
        
        base_prompt = """Eres un asistente especializado en el Sistema de Información de Coordinación Académica (SICORA) del SENA.

Tu propósito principal es ayudar a estudiantes, instructores y administrativos con:
- Consultas sobre el Reglamento del Aprendiz SENA
- Procedimientos académicos y administrativos
- Información sobre asistencia, evaluaciones y horarios
- Políticas y normativas institucionales

IMPORTANTE:
- Siempre mantén un tono profesional y amigable
- Proporciona información precisa basada en la documentación oficial
- Si no tienes información específica, indícalo claramente
- Sugiere contactar con la coordinación académica para casos específicos"""

        if not context or not context.knowledge_results:
            return base_prompt

        # Agregar contexto de la base de conocimiento
        knowledge_context = "\n\nCONTEXTO RELEVANTE DE LA BASE DE CONOCIMIENTO:\n"
        
        for i, result in enumerate(context.knowledge_results[:3], 1):
            knowledge_context += f"\n{i}. {result.title} ({result.category})\n"
            knowledge_context += f"   {result.content[:300]}...\n"
        
        # Agregar categorías específicas si están disponibles
        if context.categories:
            knowledge_context += f"\nCategorías relevantes: {', '.join(context.categories)}\n"
        
        knowledge_context += "\nUsa esta información para proporcionar respuestas precisas y contextualizadas."
        
        return base_prompt + knowledge_context
    
    def _prepare_conversation_messages(
        self,
        conversation_history: List[MessageDTO],
        system_prompt: str
    ) -> List[Dict[str, str]]:
        """Preparar mensajes de conversación para la API de OpenAI."""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Agregar historial reciente (últimos 8 mensajes para mantener contexto)
        recent_history = conversation_history[-8:] if conversation_history else []
        
        for msg in recent_history:
            if msg.role in ["user", "assistant"]:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        return messages
    
    async def search_regulatory_content(
        self,
        query: str,
        user_id: UUID
    ) -> List[KnowledgeSearchResult]:
        """
        Búsqueda específica en el Reglamento del Aprendiz SENA.
        
        Args:
            query: Consulta específica sobre el reglamento
            user_id: ID del usuario que consulta
            
        Returns:
            Resultados específicos del reglamento
        """
        try:
            # Usar caché para consultas frecuentes
            cache_key = f"{query.lower().strip()[:50]}"
            if cache_key in self.regulatory_context_cache:
                return self.regulatory_context_cache[cache_key]
            
            # Búsqueda en contenido regulatorio
            results = await self.kb_integration.get_regulatory_context(
                query=query,
                user_id=user_id
            )
            
            # Guardar en caché (máximo 100 entradas)
            if len(self.regulatory_context_cache) < 100:
                self.regulatory_context_cache[cache_key] = results
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching regulatory content: {str(e)}")
            return []
    
    async def get_quick_answer(
        self,
        question: str,
        user_id: UUID,
        category: Optional[str] = None
    ) -> Optional[str]:
        """
        Obtener respuesta rápida para preguntas frecuentes.
        
        Args:
            question: Pregunta del usuario
            user_id: ID del usuario
            category: Categoría específica (opcional)
            
        Returns:
            Respuesta rápida si está disponible
        """
        try:
            # Búsqueda específica para FAQs
            results = await self.kb_integration.search_knowledge(
                query=question,
                user_id=user_id,
                search_type="semantic",
                limit=1,
                category_filter=category
            )
            
            if results and results[0].content_type == "faq":
                return results[0].content
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting quick answer: {str(e)}")
            return None
    
    async def health_check(self) -> Dict[str, Any]:
        """Verificar estado del servicio de chat mejorado."""
        try:
            kb_healthy = await self.kb_integration.health_check()
            openai_healthy = await self.openai_client.health_check()
            
            return {
                "enhanced_chat_service": True,
                "kb_integration": kb_healthy,
                "openai_client": openai_healthy,
                "cache_size": len(self.regulatory_context_cache)
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "enhanced_chat_service": False,
                "error": str(e)
            }
