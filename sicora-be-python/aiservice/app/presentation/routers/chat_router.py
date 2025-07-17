"""
Chat Router
Router para endpoints de chat y conversaciones
"""
from fastapi import APIRouter, HTTPException, Depends, status, Query, Path
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.dependencies import get_chat_use_case, get_conversation_management_use_case
from app.application.use_cases.chat_use_cases import ChatUseCase, ConversationManagementUseCase
from app.application.dtos.ai_dtos import (
    ChatRequestDTO,
    ConversationCreateDTO
)
from app.presentation.schemas.chat_schemas import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationWithMessages,
    ConversationListQuery,
    ConversationListResponse,
    MessageCreate,
    MessageResponse
)

router = APIRouter()

@router.get(
    "/",
    response_model=List[ConversationResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar conversaciones",
    description="Obtiene una lista de todas las conversaciones del usuario."
)
async def list_conversations(
    user_id: UUID = Query(..., description="ID del usuario"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de conversaciones a retornar"),
    offset: int = Query(0, ge=0, description="Número de conversaciones a omitir"),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """Listar conversaciones del usuario."""
    try:
        conversations = await chat_use_case.list_conversations(
            user_id=user_id,
            limit=limit,
            offset=offset
        )

        return conversations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar conversaciones: {str(e)}"
        )

@router.post(
    "/",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva conversación",
    description="Crea una nueva conversación para el usuario."
)
async def create_conversation(
    conversation_data: ConversationCreate,
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """Crear nueva conversación."""
    try:
        # Convertir esquema a DTO
        conversation_dto = ConversationCreateDTO(
            user_id=conversation_data.user_id,
            title=conversation_data.title,
            initial_message=conversation_data.system_prompt,
            metadata=conversation_data.metadata
        )

        # Crear conversación
        created_conversation = await chat_use_case.create_conversation(conversation_dto)

        return created_conversation
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear conversación: {str(e)}"
        )

@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener conversación por ID",
    description="Obtiene información detallada de una conversación específica."
)
async def get_conversation(
    conversation_id: UUID = Path(..., description="ID de la conversación"),
    user_id: UUID = Query(..., description="ID del usuario"),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """Obtener conversación por ID."""
    try:
        conversation = await chat_use_case.get_conversation(
            conversation_id=conversation_id,
            user_id=user_id
        )

        return conversation
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversación no encontrada: {str(e)}"
        )

@router.put(
    "/{conversation_id}",
    response_model=ConversationResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar conversación",
    description="Actualiza el título o estado de una conversación existente."
)
async def update_conversation(
    conversation_id: UUID = Path(..., description="ID de la conversación"),
    conversation_data: ConversationUpdate = ...,
    user_id: UUID = Query(..., description="ID del usuario"),
    conversation_mgmt: ConversationManagementUseCase = Depends(get_conversation_management_use_case)
):
    """Actualizar conversación."""
    try:
        if conversation_data.title is not None:
            updated_conversation = await conversation_mgmt.update_conversation_title(
                conversation_id=conversation_id,
                user_id=user_id,
                new_title=conversation_data.title
            )
            return updated_conversation

        if conversation_data.status == "archived":
            success = await conversation_mgmt.archive_conversation(
                conversation_id=conversation_id,
                user_id=user_id
            )
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo archivar la conversación"
                )

            # Obtener la conversación actualizada
            # Nota: Esto requeriría una implementación adicional para obtener la conversación después de archivarla
            # Por ahora, retornamos un mensaje de éxito
            return {"message": "Conversación archivada correctamente"}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere título o estado para actualizar la conversación"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar conversación: {str(e)}"
        )

@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar conversación",
    description="Elimina una conversación existente."
)
async def delete_conversation(
    conversation_id: UUID = Path(..., description="ID de la conversación"),
    user_id: UUID = Query(..., description="ID del usuario"),
    conversation_mgmt: ConversationManagementUseCase = Depends(get_conversation_management_use_case)
):
    """Eliminar conversación."""
    try:
        success = await conversation_mgmt.delete_conversation(
            conversation_id=conversation_id,
            user_id=user_id
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada o no se pudo eliminar"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar conversación: {str(e)}"
        )

@router.post(
    "/message",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Enviar mensaje",
    description="Envía un mensaje y obtiene una respuesta del asistente IA."
)
async def send_message(
    chat_request: ChatRequest,
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """Enviar mensaje y obtener respuesta del asistente IA."""
    try:
        # Convertir esquema a DTO
        request_dto = ChatRequestDTO(
            conversation_id=chat_request.conversation_id,
            user_id=chat_request.conversation_id,  # Esto debería ser el user_id real
            message=chat_request.message,
            model_name=str(chat_request.model_id) if chat_request.model_id else None,
            temperature=chat_request.temperature,
            max_tokens=chat_request.max_tokens,
            use_knowledge_base=True,
            include_context=chat_request.include_context
        )

        # Enviar mensaje
        response = await chat_use_case.send_message(request_dto)

        # Convertir DTO a esquema de respuesta
        return ChatResponse(
            message=MessageResponse(
                id=response.message_id,
                content=response.response,
                message_type="assistant",
                created_at=response.timestamp
            ),
            conversation_id=response.conversation_id,
            usage={
                "tokens": response.tokens_used,
                "processing_time": response.processing_time
            },
            model_info={
                "model": response.model_used,
                "knowledge_sources": response.knowledge_sources
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar mensaje: {str(e)}"
        )
