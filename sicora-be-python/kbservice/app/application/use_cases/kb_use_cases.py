"""Use cases for Knowledge Base Service."""

from typing import List, Optional, Dict, Any
from uuid import UUID

from app.domain.entities.kb_entities import (
    KnowledgeItem, Category, SearchQuery, UserRole, ContentType, ContentStatus, TargetAudience
)
from app.domain.value_objects.kb_value_objects import (
    KnowledgeItemId, Title, Content, CategoryName, TagName
)
from app.domain.repositories.kb_repositories import (
    KnowledgeItemRepository, CategoryRepository, SearchQueryRepository
)
from app.domain.services.kb_domain_services import (
    EmbeddingService, SearchService, ContentValidationService, PersonalizationService
)
from app.domain.exceptions.kb_exceptions import (
    KnowledgeItemNotFoundError, InvalidContentError, UnauthorizedAccessError
)
from app.application.dtos.kb_dtos import (
    KnowledgeItemCreateDTO, KnowledgeItemUpdateDTO, KnowledgeItemResponseDTO,
    KnowledgeItemListDTO, SearchRequestDTO, SearchResponseDTO, QueryRequestDTO, QueryResponseDTO
)


class CreateKnowledgeItemUseCase:
    """Use case for creating a knowledge item."""

    def __init__(
        self,
        knowledge_item_repo: KnowledgeItemRepository,
        embedding_service: EmbeddingService,
        validation_service: ContentValidationService
    ):
        self.knowledge_item_repo = knowledge_item_repo
        self.embedding_service = embedding_service
        self.validation_service = validation_service

    async def execute(
        self, 
        dto: KnowledgeItemCreateDTO, 
        author_id: UUID
    ) -> KnowledgeItemResponseDTO:
        """Execute the create knowledge item use case."""
        # Validate content quality
        validation_result = self.validation_service.validate_content_quality(dto.content)
        if not validation_result["is_valid"]:
            raise InvalidContentError(f"Content validation failed: {validation_result['issues']}")

        # Create domain objects
        title = Title(dto.title)
        content = Content(dto.content)
        category = CategoryName(dto.category)
        tags = [TagName(tag) for tag in dto.tags] if dto.tags else []

        # Generate embedding
        embedding = await self.embedding_service.generate_embedding(
            f"{dto.title} {dto.content}"
        )

        # Create knowledge item entity
        knowledge_item = KnowledgeItem(
            title=title,
            content=content,
            content_type=dto.content_type,
            category=category,
            target_audience=dto.target_audience,
            author_id=author_id,
            status=dto.status,
            tags=tags,
            embedding=embedding
        )

        # Save to repository
        created_item = await self.knowledge_item_repo.create(knowledge_item)

        # Return DTO
        return self._to_response_dto(created_item)

    def _to_response_dto(self, item: KnowledgeItem) -> KnowledgeItemResponseDTO:
        """Convert domain entity to response DTO."""
        return KnowledgeItemResponseDTO(
            id=item.id.value,
            title=item.title.value,
            content=item.content.value,
            content_type=item.content_type,
            category=item.category.value,
            target_audience=item.target_audience,
            author_id=item.author_id,
            status=item.status,
            tags=[tag.value for tag in item.tags],
            created_at=item.created_at,
            updated_at=item.updated_at,
            published_at=item.published_at,
            view_count=item.view_count,
            helpful_count=item.helpful_count,
            unhelpful_count=item.unhelpful_count,
            version=item.version
        )


class GetKnowledgeItemUseCase:
    """Use case for getting a knowledge item."""

    def __init__(self, knowledge_item_repo: KnowledgeItemRepository):
        self.knowledge_item_repo = knowledge_item_repo

    async def execute(
        self, 
        item_id: UUID, 
        user_role: UserRole,
        increment_view: bool = True
    ) -> KnowledgeItemResponseDTO:
        """Execute the get knowledge item use case."""
        # Get item from repository
        item = await self.knowledge_item_repo.get_by_id(KnowledgeItemId(item_id))

        if not item:
            raise KnowledgeItemNotFoundError(str(item_id))

        # Check access permissions
        if not item.is_accessible_by(user_role):
            raise UnauthorizedAccessError("User does not have access to this content")

        # Check if item is published (unless user is admin)
        if not item.is_published() and user_role != UserRole.ADMIN:
            raise KnowledgeItemNotFoundError(str(item_id))

        # Increment view count if requested
        if increment_view:
            item.increment_view_count()
            await self.knowledge_item_repo.update(item)

        # Return DTO
        return self._to_response_dto(item)

    def _to_response_dto(self, item: KnowledgeItem) -> KnowledgeItemResponseDTO:
        """Convert domain entity to response DTO."""
        return KnowledgeItemResponseDTO(
            id=item.id.value,
            title=item.title.value,
            content=item.content.value,
            content_type=item.content_type,
            category=item.category.value,
            target_audience=item.target_audience,
            author_id=item.author_id,
            status=item.status,
            tags=[tag.value for tag in item.tags],
            created_at=item.created_at,
            updated_at=item.updated_at,
            published_at=item.published_at,
            view_count=item.view_count,
            helpful_count=item.helpful_count,
            unhelpful_count=item.unhelpful_count,
            version=item.version
        )


class UpdateKnowledgeItemUseCase:
    """Use case for updating a knowledge item."""

    def __init__(
        self,
        knowledge_item_repo: KnowledgeItemRepository,
        embedding_service: EmbeddingService,
        validation_service: ContentValidationService
    ):
        self.knowledge_item_repo = knowledge_item_repo
        self.embedding_service = embedding_service
        self.validation_service = validation_service

    async def execute(
        self, 
        item_id: UUID, 
        dto: KnowledgeItemUpdateDTO, 
        user_id: UUID
    ) -> KnowledgeItemResponseDTO:
        """Execute the update knowledge item use case."""
        # Get existing item
        item = await self.knowledge_item_repo.get_by_id(KnowledgeItemId(item_id))

        if not item:
            raise KnowledgeItemNotFoundError(str(item_id))

        # Update fields if provided
        updated_content = False

        if dto.title or dto.content:
            # Validate content if being updated
            content_to_validate = dto.content or item.content.value
            validation_result = self.validation_service.validate_content_quality(content_to_validate)
            if not validation_result["is_valid"]:
                raise InvalidContentError(f"Content validation failed: {validation_result['issues']}")

            # Update content
            title = Title(dto.title) if dto.title else item.title
            content = Content(dto.content) if dto.content else item.content
            tags = [TagName(tag) for tag in dto.tags] if dto.tags is not None else item.tags

            item.update_content(title, content, tags)
            updated_content = True

        # Update other fields
        if dto.content_type:
            item._content_type = dto.content_type
        if dto.category:
            item._category = CategoryName(dto.category)
        if dto.target_audience:
            item._target_audience = dto.target_audience
        if dto.status:
            if dto.status == ContentStatus.PUBLISHED:
                item.publish()
            elif dto.status == ContentStatus.ARCHIVED:
                item.archive()
            elif dto.status == ContentStatus.UNDER_REVIEW:
                item.set_under_review()
            else:
                item._status = dto.status

        # Regenerate embedding if content was updated
        if updated_content:
            embedding = await self.embedding_service.generate_embedding(
                f"{item.title.value} {item.content.value}"
            )
            item.update_embedding(embedding)

        # Save to repository
        updated_item = await self.knowledge_item_repo.update(item)

        # Return DTO
        return self._to_response_dto(updated_item)

    def _to_response_dto(self, item: KnowledgeItem) -> KnowledgeItemResponseDTO:
        """Convert domain entity to response DTO."""
        return KnowledgeItemResponseDTO(
            id=item.id.value,
            title=item.title.value,
            content=item.content.value,
            content_type=item.content_type,
            category=item.category.value,
            target_audience=item.target_audience,
            author_id=item.author_id,
            status=item.status,
            tags=[tag.value for tag in item.tags],
            created_at=item.created_at,
            updated_at=item.updated_at,
            published_at=item.published_at,
            view_count=item.view_count,
            helpful_count=item.helpful_count,
            unhelpful_count=item.unhelpful_count,
            version=item.version
        )


class SearchKnowledgeUseCase:
    """Use case for searching knowledge items."""

    def __init__(
        self,
        knowledge_item_repo: KnowledgeItemRepository,
        search_query_repo: SearchQueryRepository,
        search_service: SearchService,
        personalization_service: PersonalizationService
    ):
        self.knowledge_item_repo = knowledge_item_repo
        self.search_query_repo = search_query_repo
        self.search_service = search_service
        self.personalization_service = personalization_service

    async def execute(
        self, 
        dto: SearchRequestDTO, 
        user_id: UUID, 
        user_role: UserRole
    ) -> SearchResponseDTO:
        """Execute the search knowledge use case."""
        # Log search query
        search_query = SearchQuery(
            query_text=dto.query,
            user_id=user_id,
            user_role=user_role,
            filters=dto.filters
        )
        await self.search_query_repo.create(search_query)

        # Perform search based on query type and filters
        search_results = []

        if dto.filters.get("search_type") == "semantic":
            results = await self.search_service.semantic_search(
                query=dto.query,
                user_role=user_role,
                limit=dto.limit
            )
        elif dto.filters.get("search_type") == "text":
            results = await self.search_service.text_search(
                query=dto.query,
                user_role=user_role,
                filters=dto.filters,
                limit=dto.limit
            )
        else:
            # Default to hybrid search
            results = await self.search_service.hybrid_search(
                query=dto.query,
                user_role=user_role,
                filters=dto.filters,
                limit=dto.limit
            )

        # Convert to DTOs
        search_results = [
            {
                "item": self._to_list_dto(item),
                "score": float(score.value),
                "snippet": item.content.get_snippet(200)
            }
            for item, score in results
        ]

        # Generate suggestions
        suggestions = self.personalization_service.generate_response_suggestions(
            dto.query, user_role
        )

        return SearchResponseDTO(
            results=search_results,
            total_count=len(search_results),
            query=dto.query,
            filters=dto.filters,
            suggestions=suggestions
        )

    def _to_list_dto(self, item: KnowledgeItem) -> KnowledgeItemListDTO:
        """Convert domain entity to list DTO."""
        return KnowledgeItemListDTO(
            id=item.id.value,
            title=item.title.value,
            content_snippet=item.content.get_snippet(200),
            content_type=item.content_type,
            category=item.category.value,
            target_audience=item.target_audience,
            status=item.status,
            tags=[tag.value for tag in item.tags],
            created_at=item.created_at,
            updated_at=item.updated_at,
            view_count=item.view_count,
            helpful_count=item.helpful_count
        )


class ListKnowledgeItemsUseCase:
    """Use case for listing knowledge items."""

    def __init__(self, knowledge_item_repo: KnowledgeItemRepository):
        self.knowledge_item_repo = knowledge_item_repo

    async def execute(
        self, 
        user_role: UserRole,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[KnowledgeItemListDTO]:
        """Execute the list knowledge items use case."""
        # Apply role-based filtering
        if filters is None:
            filters = {}

        # Only show published items for non-admin users
        if user_role != UserRole.ADMIN:
            filters["status"] = ContentStatus.PUBLISHED

        # Get items from repository
        items = await self.knowledge_item_repo.list_all(
            skip=skip,
            limit=limit,
            filters=filters
        )

        # Filter by accessibility
        accessible_items = [
            item for item in items 
            if item.is_accessible_by(user_role)
        ]

        # Convert to DTOs
        return [self._to_list_dto(item) for item in accessible_items]

    def _to_list_dto(self, item: KnowledgeItem) -> KnowledgeItemListDTO:
        """Convert domain entity to list DTO."""
        return KnowledgeItemListDTO(
            id=item.id.value,
            title=item.title.value,
            content_snippet=item.content.get_snippet(200),
            content_type=item.content_type,
            category=item.category.value,
            target_audience=item.target_audience,
            status=item.status,
            tags=[tag.value for tag in item.tags],
            created_at=item.created_at,
            updated_at=item.updated_at,
            view_count=item.view_count,
            helpful_count=item.helpful_count
        )


class CreateFeedbackUseCase:
    """Use case for creating user feedback on knowledge items."""

    def __init__(
        self,
        knowledge_item_repo: KnowledgeItemRepository,
        feedback_repo: "FeedbackRepository"
    ):
        self.knowledge_item_repo = knowledge_item_repo
        self.feedback_repo = feedback_repo

    async def execute(
        self, 
        dto: "FeedbackCreateDTO", 
        user_id: UUID
    ) -> "FeedbackResponseDTO":
        """Execute the create feedback use case."""
        # Verify knowledge item exists
        item = await self.knowledge_item_repo.get_by_id(
            KnowledgeItemId(dto.item_id)
        )
        if not item:
            raise KnowledgeItemNotFoundError(f"Knowledge item {dto.item_id} not found")

        # Create feedback entity
        from app.domain.entities.kb_entities import Feedback
        feedback = Feedback(
            item_id=dto.item_id,
            user_id=user_id,
            feedback_type=dto.feedback_type,
            comment=dto.comment
        )

        # Save feedback
        created_feedback = await self.feedback_repo.create(feedback)

        # Update knowledge item counters
        if dto.feedback_type == "helpful":
            item.helpful_count += 1
        elif dto.feedback_type == "unhelpful":
            item.unhelpful_count += 1

        await self.knowledge_item_repo.update(item)

        # Return DTO
        return self._to_response_dto(created_feedback)

    def _to_response_dto(self, feedback: "Feedback") -> "FeedbackResponseDTO":
        """Convert domain entity to response DTO."""
        from app.application.dtos.kb_dtos import FeedbackResponseDTO
        return FeedbackResponseDTO(
            id=feedback.id,
            item_id=feedback.item_id,
            user_id=feedback.user_id,
            feedback_type=feedback.feedback_type,
            comment=feedback.comment,
            created_at=feedback.created_at
        )


class DeleteKnowledgeItemUseCase:
    """Use case for deleting a knowledge item."""

    def __init__(self, knowledge_item_repo: KnowledgeItemRepository):
        self.knowledge_item_repo = knowledge_item_repo

    async def execute(self, item_id: UUID, user_id: UUID) -> bool:
        """Execute the delete knowledge item use case."""
        # Verify knowledge item exists
        item = await self.knowledge_item_repo.get_by_id(KnowledgeItemId(item_id))

        if not item:
            raise KnowledgeItemNotFoundError(str(item_id))

        # Delete knowledge item
        result = await self.knowledge_item_repo.delete(KnowledgeItemId(item_id))

        return result


class IntelligentQueryUseCase:
    """Use case for intelligent query processing with NLP and routing."""

    def __init__(
        self,
        knowledge_item_repo: KnowledgeItemRepository,
        search_service: SearchService,
        chatbot_service: "ChatbotIntegrationService",
        personalization_service: PersonalizationService
    ):
        self.knowledge_item_repo = knowledge_item_repo
        self.search_service = search_service
        self.chatbot_service = chatbot_service
        self.personalization_service = personalization_service

    async def execute(
        self, 
        dto: QueryRequestDTO, 
        user_context: Dict[str, Any]
    ) -> QueryResponseDTO:
        """Execute intelligent query processing."""
        # Analyze query intent and determine routing
        should_route_to_chatbot = await self.chatbot_service.should_route_to_chatbot(
            dto.query
        )

        kb_response = ""
        chatbot_response = ""

        # Search knowledge base
        kb_results = await self.search_service.hybrid_search(
            query=dto.query,
            user_role=UserRole(user_context.get("role", "student")),
            filters=dto.filters,
            limit=5
        )

        if kb_results:
            best_match = kb_results[0][0]  # First result
            kb_response = best_match.content.value

        # Query chatbot if needed
        if should_route_to_chatbot:
            chatbot_response = await self.chatbot_service.query_regulation_chatbot(
                dto.query, user_context
            )

        # Combine responses intelligently
        if chatbot_response and kb_response:
            combined_response = await self.chatbot_service.combine_responses(
                kb_response, chatbot_response, dto.query
            )
        elif chatbot_response:
            combined_response = chatbot_response
        elif kb_response:
            combined_response = kb_response
        else:
            combined_response = "Lo siento, no encontré información relevante para tu consulta."

        # Generate follow-up suggestions
        suggestions = self.personalization_service.generate_response_suggestions(
            dto.query, UserRole(user_context.get("role", "student"))
        )

        return QueryResponseDTO(
            response=combined_response,
            sources=[
                {
                    "type": "knowledge_base" if kb_response else "chatbot",
                    "confidence": 0.9 if kb_results else 0.7,
                    "item_id": kb_results[0][0].id.value if kb_results else None
                }
            ],
            suggestions=suggestions,
            query=dto.query,
            processing_time=0.5  # Placeholder
        )
