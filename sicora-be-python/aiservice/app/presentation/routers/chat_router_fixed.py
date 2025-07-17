"""Chat and conversation router for AI Service - Fixed version."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from fastapi import status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.presentation.schemas.chat_schemas import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationResponse,
    ConversationWithMessages,
    ConversationListResponse,
    ConversationStatusEnum,
    MessageResponse,
    MessageTypeEnum
)
from app.application.use_cases.chat_use_cases import ChatUseCase
from app.application.dtos.ai_dtos import ChatRequestDTO, ConversationCreateDTO
from app.domain.exceptions.ai_exceptions import (
    ConversationNotFoundError,
    ModelNotAvailableError,
    InvalidPromptError,
    TokenLimitExceededError
)
from app.dependencies import get_chat_use_case
from app.infrastructure.config.database import get_db_session

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatRequest,
    user_id: UUID = Query(..., description="User ID for the request"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Send a message and get AI response.
    
    - **message**: The user message to send
    - **conversation_id**: Optional existing conversation ID
    - **temperature**: Response creativity level (0.0 to 2.0)
    - **max_tokens**: Maximum tokens in response
    - **include_context**: Whether to include conversation context
    """
    try:
        # Convert Pydantic request to DTO
        chat_request_dto = ChatRequestDTO(
            conversation_id=request.conversation_id,
            user_id=user_id,
            message=request.message,
            model_name=None,  # Use default model if not specified
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            use_knowledge_base=request.include_context,
            include_context=request.include_context
        )
        
        # Use the chat use case to process the request
        response_dto = await chat_use_case.send_message(chat_request_dto)
        
        # Convert DTO back to Pydantic response
        return ChatResponse(
            message=MessageResponse(
                id=response_dto.message_id,
                content=response_dto.response,
                message_type=MessageTypeEnum.ASSISTANT,
                metadata={
                    "model_used": response_dto.model_used,
                    "tokens_used": response_dto.tokens_used,
                    "processing_time": response_dto.processing_time,
                    "knowledge_sources": response_dto.knowledge_sources or []
                },
                created_at=response_dto.timestamp
            ),
            conversation_id=response_dto.conversation_id,
            usage={
                "prompt_tokens": 0,  # Will be calculated properly in the use case
                "completion_tokens": response_dto.tokens_used,
                "total_tokens": response_dto.tokens_used
            },
            model_info={
                "model": response_dto.model_used,
                "provider": "ai_service"
            }
        )
        
    except ConversationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ModelNotAvailableError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except TokenLimitExceededError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.post("/stream", response_class=StreamingResponse)
async def chat_stream(
    request: ChatRequest,
    user_id: UUID = Query(..., description="User ID for the request"),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """
    Send a message and get streaming AI response.
    
    Returns a streaming response with Server-Sent Events format.
    """
    try:
        async def generate_stream():
            # Convert request to DTO
            chat_request_dto = ChatRequestDTO(
                conversation_id=request.conversation_id,
                user_id=user_id,
                message=request.message,
                model_name=None,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                use_knowledge_base=request.include_context,
                include_context=request.include_context
            )
            
            # For now, just get the response and simulate streaming
            response_dto = await chat_use_case.send_message(chat_request_dto)
            
            # Split response into words for streaming simulation
            words = response_dto.response.split()
            
            for word in words:
                yield f"data: {{'content': '{word} ', 'type': 'content'}}\n\n"
                # Small delay to simulate streaming
                import asyncio
                await asyncio.sleep(0.05)
            
            # Send final message
            yield f"data: {{'type': 'done', 'conversation_id': '{response_dto.conversation_id}', 'message_id': '{response_dto.message_id}'}}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing streaming chat request: {str(e)}"
        )


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation: ConversationCreate,
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """
    Create a new conversation.
    
    - **title**: Optional conversation title
    - **user_id**: User ID who owns the conversation
    - **model_id**: Optional AI model to use
    - **system_prompt**: Optional system prompt for the conversation
    - **metadata**: Optional additional metadata
    """
    try:
        # Convert to DTO
        conversation_dto = ConversationCreateDTO(
            user_id=conversation.user_id,
            title=conversation.title,
            initial_message=None,  # No initial message for conversation creation
            metadata=conversation.metadata
        )
        
        # Use the chat use case to create the conversation
        response_dto = await chat_use_case.create_conversation(conversation_dto)
        
        # Convert back to Pydantic response
        return ConversationResponse(
            id=response_dto.conversation_id,
            title=response_dto.title,
            user_id=response_dto.user_id,
            model_id=conversation.model_id,
            system_prompt=conversation.system_prompt,
            status=ConversationStatusEnum.ACTIVE,
            message_count=response_dto.message_count,
            metadata=response_dto.metadata,
            created_at=response_dto.created_at,
            updated_at=response_dto.updated_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating conversation: {str(e)}"
        )


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    user_id: UUID = Query(..., description="User ID to filter conversations"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of conversations to return"),
    offset: int = Query(0, ge=0, description="Number of conversations to skip"),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """
    List conversations with optional filtering and pagination.
    
    - **user_id**: Filter by user ID
    - **limit**: Maximum number of conversations to return (1-100)
    - **offset**: Number of conversations to skip
    """
    try:
        # Use chat use case to list conversations
        conversation_dtos = await chat_use_case.list_conversations(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        # Convert DTOs to response format
        conversation_responses = []
        for dto in conversation_dtos:
            conversation_responses.append(ConversationResponse(
                id=dto.conversation_id,
                title=dto.title,
                user_id=dto.user_id,
                model_id=None,  # TODO: Add to DTO
                system_prompt=None,  # TODO: Add to DTO
                status=ConversationStatusEnum.ACTIVE if dto.is_active else ConversationStatusEnum.ARCHIVED,
                message_count=dto.message_count,
                metadata=dto.metadata,
                created_at=dto.created_at,
                updated_at=dto.updated_at
            ))
        
        # TODO: Get total count from use case
        total = len(conversation_responses) + offset  # Approximate for now
        
        return ConversationListResponse(
            conversations=conversation_responses,
            total=total,
            limit=limit,
            offset=offset,
            has_more=len(conversation_responses) == limit  # Simplified logic
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing conversations: {str(e)}"
        )


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: UUID,
    user_id: UUID = Query(..., description="User ID for authorization"),
    include_messages: bool = Query(True, description="Whether to include messages in the response"),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    """
    Get a specific conversation by ID.
    
    - **conversation_id**: The conversation ID to retrieve
    - **user_id**: User ID for authorization
    - **include_messages**: Whether to include messages in the response
    """
    try:
        # Use chat use case to get conversation
        conversation_dto = await chat_use_case.get_conversation(conversation_id, user_id)
        
        # Convert to response format with messages if requested
        messages = []
        if include_messages:
            # TODO: Add get_conversation_messages method to use case
            # For now, return empty messages list
            pass
        
        return ConversationWithMessages(
            id=conversation_dto.conversation_id,
            title=conversation_dto.title,
            user_id=conversation_dto.user_id,
            model_id=None,  # TODO: Add to DTO
            system_prompt=None,  # TODO: Add to DTO
            status=ConversationStatusEnum.ACTIVE if conversation_dto.is_active else ConversationStatusEnum.ARCHIVED,
            message_count=conversation_dto.message_count,
            metadata=conversation_dto.metadata,
            created_at=conversation_dto.created_at,
            updated_at=conversation_dto.updated_at,
            messages=messages
        )
        
    except ConversationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversation: {str(e)}"
        )
