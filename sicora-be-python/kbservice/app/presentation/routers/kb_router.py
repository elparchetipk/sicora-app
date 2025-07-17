"""Main knowledge base router."""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status

from app.dependencies import (
    get_current_user,
    get_create_knowledge_item_use_case,
    get_get_knowledge_item_use_case,
    get_update_knowledge_item_use_case,
    get_list_knowledge_items_use_case,
    get_create_feedback_use_case,
    get_delete_knowledge_item_use_case
)
from app.presentation.schemas.kb_schemas import (
    KnowledgeItemCreate,
    KnowledgeItemUpdate,
    KnowledgeItemResponse,
    KnowledgeItemList,
    Feedback,
    FeedbackCreateSchema
)
from app.application.use_cases.kb_use_cases import (
    CreateKnowledgeItemUseCase,
    GetKnowledgeItemUseCase,
    UpdateKnowledgeItemUseCase,
    ListKnowledgeItemsUseCase,
    CreateFeedbackUseCase,
    DeleteKnowledgeItemUseCase
)
from app.application.dtos.kb_dtos import (
    KnowledgeItemCreateDTO,
    KnowledgeItemUpdateDTO
)
from app.domain.entities.kb_entities import UserRole, ContentType, ContentStatus, TargetAudience
from app.domain.exceptions.kb_exceptions import (
    KnowledgeItemNotFoundError,
    InvalidContentError,
    UnauthorizedAccessError
)

router = APIRouter()


@router.post("/items", response_model=KnowledgeItemResponse, status_code=http_status.HTTP_201_CREATED)
async def create_knowledge_item(
    item_data: KnowledgeItemCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    create_use_case: CreateKnowledgeItemUseCase = Depends(get_create_knowledge_item_use_case)
):
    """
    Create a new knowledge base item.

    **Required role:** Admin

    Creates a new knowledge base item with the provided content. The system will automatically:
    - Generate embeddings for semantic search
    - Validate content quality
    - Set creation metadata
    """
    # Only admins can create knowledge items
    if current_user["role"] != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create knowledge items"
        )

    try:
        # Convert to DTO
        dto = KnowledgeItemCreateDTO(
            title=item_data.title,
            content=item_data.content,
            content_type=item_data.content_type,
            category=item_data.category,
            target_audience=item_data.target_audience,
            tags=item_data.tags,
            status=item_data.status
        )

        # Execute use case
        result = await create_use_case.execute(dto, current_user["user_id"])

        return result

    except InvalidContentError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create knowledge item: {str(e)}"
        )


@router.get("/items/{item_id}", response_model=KnowledgeItemResponse)
async def get_knowledge_item(
    item_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    get_use_case: GetKnowledgeItemUseCase = Depends(get_get_knowledge_item_use_case)
):
    """
    Get a specific knowledge base item by ID.

    Returns the complete content of a knowledge base item if the user has access to it.
    Access is determined by:
    - Item's target audience
    - User's role
    - Item's publication status
    """
    try:
        user_role = UserRole(current_user["role"])
        result = await get_use_case.execute(item_id, user_role)

        return result

    except KnowledgeItemNotFoundError:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found"
        )
    except UnauthorizedAccessError:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this content"
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get knowledge item: {str(e)}"
        )


@router.put("/items/{item_id}", response_model=KnowledgeItemResponse)
async def update_knowledge_item(
    item_id: UUID,
    item_data: KnowledgeItemUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    update_use_case: UpdateKnowledgeItemUseCase = Depends(get_update_knowledge_item_use_case)
):
    """
    Update an existing knowledge base item.

    **Required role:** Admin

    Updates the specified knowledge base item. If content is modified, embeddings will be regenerated automatically.
    """
    # Only admins can update knowledge items
    if current_user["role"] != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update knowledge items"
        )

    try:
        # Convert to DTO
        dto = KnowledgeItemUpdateDTO(
            title=item_data.title,
            content=item_data.content,
            content_type=item_data.content_type,
            category=item_data.category,
            target_audience=item_data.target_audience,
            tags=item_data.tags,
            status=item_data.status
        )

        # Execute use case
        result = await update_use_case.execute(item_id, dto, current_user["user_id"])

        return result

    except KnowledgeItemNotFoundError:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found"
        )
    except InvalidContentError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update knowledge item: {str(e)}"
        )


@router.get("/items", response_model=List[KnowledgeItemList])
async def list_knowledge_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of items to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    content_type: Optional[ContentType] = Query(None, description="Filter by content type"),
    content_status: Optional[ContentStatus] = Query(None, description="Filter by status (admin only)"),
    target_audience: Optional[TargetAudience] = Query(None, description="Filter by target audience"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    list_use_case: ListKnowledgeItemsUseCase = Depends(get_list_knowledge_items_use_case)
):
    """
    List knowledge base items with optional filtering.

    Returns a paginated list of knowledge base items accessible to the current user.
    Filters available:
    - **category**: Filter by category name
    - **content_type**: Filter by content type (article, faq, guide, etc.)
    - **status**: Filter by status (admin only)
    - **target_audience**: Filter by target audience
    """
    try:
        user_role = UserRole(current_user["role"])

        # Build filters
        filters = {}
        if category:
            filters["category"] = category
        if content_type:
            filters["content_type"] = content_type.value
        if target_audience:
            filters["target_audience"] = target_audience.value
        if content_status and user_role == UserRole.ADMIN:
            filters["status"] = content_status.value

        # Execute use case
        result = await list_use_case.execute(
            user_role=user_role,
            skip=skip,
            limit=limit,
            filters=filters
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list knowledge items: {str(e)}"
        )


@router.post("/feedback", status_code=http_status.HTTP_201_CREATED)
async def create_feedback(
    feedback_data: FeedbackCreateSchema,
    current_user: Dict[str, Any] = Depends(get_current_user),
    create_feedback_use_case: CreateFeedbackUseCase = Depends(get_create_feedback_use_case)
):
    """
    Submit feedback for a knowledge base item.

    Allows users to provide helpful/unhelpful feedback and optional comments
    to improve the quality of the knowledge base.
    """
    try:
        # Convert to DTO
        from app.application.dtos.kb_dtos import FeedbackCreateDTO
        dto = FeedbackCreateDTO(
            item_id=feedback_data.item_id,
            feedback_type=feedback_data.feedback_type,
            comment=feedback_data.comment
        )

        # Execute use case
        result = await create_feedback_use_case.execute(dto, current_user["user_id"])

        return result

    except KnowledgeItemNotFoundError as e:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )


@router.get("/items/{item_id}/suggestions", response_model=List[str])
async def get_suggestions(
    item_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get related suggestions for a knowledge item.

    Returns a list of related topics, common questions, or follow-up actions
    based on the current item and user context.
    """
    try:
        # TODO: Implement intelligent suggestions based on:
        # - Related items by category/tags
        # - User role and common patterns
        # - Content analysis and NLP

        suggestions = [
            "¿Cómo registrar la asistencia manualmente?",
            "Procedimiento para justificar faltas",
            "Consultar mi historial de asistencia",
            "Reportar problemas técnicos",
            "Contactar coordinación académica"
        ]

        return suggestions

    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get suggestions: {str(e)}"
        )


@router.delete("/items/{item_id}", status_code=http_status.HTTP_200_OK)
async def delete_knowledge_item(
    item_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    delete_use_case: DeleteKnowledgeItemUseCase = Depends(get_delete_knowledge_item_use_case)
):
    """
    Delete a knowledge base item.

    **Required role:** Admin

    Removes a knowledge item from the system. This operation cannot be undone.
    """
    # Only admins can delete knowledge items
    if current_user["role"] != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete knowledge items"
        )

    try:
        # Execute use case
        result = await delete_use_case.execute(item_id, current_user["user_id"])

        if not result:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Knowledge item not found"
            )

        return {"message": "Knowledge item deleted successfully"}

    except KnowledgeItemNotFoundError:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete knowledge item: {str(e)}"
        )


@router.get("/categories", response_model=List[str])
async def list_categories(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get list of available categories.

    Returns all active categories that contain published content accessible to the current user.
    """
    try:
        # TODO: Implement category listing
        # For now, return common categories
        categories = [
            "Asistencia",
            "Evaluación", 
            "Procedimientos",
            "Guías Técnicas",
            "Políticas",
            "Reglamento",
            "Soporte Técnico"
        ]

        return categories

    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list categories: {str(e)}"
        )
