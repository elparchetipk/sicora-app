"""SQLAlchemy repository implementations for Knowledge Base Service."""

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_, or_, text
from sqlalchemy.orm import selectinload

from app.domain.entities.kb_entities import (
    KnowledgeItem, Category, SearchQuery, UserRole, ContentType, ContentStatus, TargetAudience, Feedback
)
from app.domain.value_objects.kb_value_objects import (
    KnowledgeItemId, Title, Content, CategoryName, TagName, Vector, SearchScore
)
from app.domain.repositories.kb_repositories import (
    KnowledgeItemRepository, CategoryRepository, SearchQueryRepository, FeedbackRepository
)
from app.infrastructure.models.kb_models import (
    KnowledgeItemModel, CategoryModel, SearchQueryModel, QueryAnalyticsModel, FeedbackModel
)


class SQLAlchemyKnowledgeItemRepository(KnowledgeItemRepository):
    """SQLAlchemy implementation of KnowledgeItemRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, knowledge_item: KnowledgeItem) -> KnowledgeItem:
        """Create a new knowledge item."""
        model = KnowledgeItemModel(
            id=knowledge_item.id.value,
            title=knowledge_item.title.value,
            content=knowledge_item.content.value,
            content_type=knowledge_item.content_type.value,
            category=knowledge_item.category.value,
            target_audience=knowledge_item.target_audience.value,
            author_id=knowledge_item.author_id,
            status=knowledge_item.status.value,
            tags=[tag.value for tag in knowledge_item.tags],
            embedding=knowledge_item.embedding.values if knowledge_item.embedding else None,
            created_at=knowledge_item.created_at,
            updated_at=knowledge_item.updated_at,
            published_at=knowledge_item.published_at,
            view_count=knowledge_item.view_count,
            helpful_count=knowledge_item.helpful_count,
            unhelpful_count=knowledge_item.unhelpful_count,
            version=knowledge_item.version
        )
        
        self.session.add(model)
        await self.session.flush()
        
        return self._to_entity(model)
    
    async def get_by_id(self, item_id: KnowledgeItemId) -> Optional[KnowledgeItem]:
        """Get a knowledge item by ID."""
        stmt = select(KnowledgeItemModel).where(KnowledgeItemModel.id == item_id.value)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._to_entity(model)
        return None
    
    async def update(self, knowledge_item: KnowledgeItem) -> KnowledgeItem:
        """Update an existing knowledge item."""
        stmt = select(KnowledgeItemModel).where(KnowledgeItemModel.id == knowledge_item.id.value)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            model.title = knowledge_item.title.value
            model.content = knowledge_item.content.value
            model.content_type = knowledge_item.content_type.value
            model.category = knowledge_item.category.value
            model.target_audience = knowledge_item.target_audience.value
            model.status = knowledge_item.status.value
            model.tags = [tag.value for tag in knowledge_item.tags]
            model.embedding = knowledge_item.embedding.values if knowledge_item.embedding else None
            model.updated_at = knowledge_item.updated_at
            model.published_at = knowledge_item.published_at
            model.view_count = knowledge_item.view_count
            model.helpful_count = knowledge_item.helpful_count
            model.unhelpful_count = knowledge_item.unhelpful_count
            model.version = knowledge_item.version
            
            await self.session.flush()
            return self._to_entity(model)
        
        return knowledge_item
    
    async def delete(self, item_id: KnowledgeItemId) -> bool:
        """Delete a knowledge item."""
        stmt = select(KnowledgeItemModel).where(KnowledgeItemModel.id == item_id.value)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
    
    async def list_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[KnowledgeItem]:
        """List all knowledge items with optional filters."""
        stmt = select(KnowledgeItemModel)
        
        # Apply filters
        if filters:
            if "status" in filters:
                stmt = stmt.where(KnowledgeItemModel.status == filters["status"])
            if "category" in filters:
                stmt = stmt.where(KnowledgeItemModel.category == filters["category"])
            if "target_audience" in filters:
                stmt = stmt.where(KnowledgeItemModel.target_audience == filters["target_audience"])
            if "content_type" in filters:
                stmt = stmt.where(KnowledgeItemModel.content_type == filters["content_type"])
            if "author_id" in filters:
                stmt = stmt.where(KnowledgeItemModel.author_id == filters["author_id"])
        
        # Order by update date descending
        stmt = stmt.order_by(desc(KnowledgeItemModel.updated_at))
        
        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def list_by_category(
        self, 
        category: CategoryName, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[KnowledgeItem]:
        """List knowledge items by category."""
        stmt = select(KnowledgeItemModel).where(
            KnowledgeItemModel.category == category.value
        ).order_by(desc(KnowledgeItemModel.updated_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def list_by_target_audience(
        self, 
        target_audience: TargetAudience, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[KnowledgeItem]:
        """List knowledge items by target audience."""
        stmt = select(KnowledgeItemModel).where(
            or_(
                KnowledgeItemModel.target_audience == target_audience.value,
                KnowledgeItemModel.target_audience == TargetAudience.ALL.value
            )
        ).order_by(desc(KnowledgeItemModel.updated_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def list_by_status(
        self, 
        status: ContentStatus, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[KnowledgeItem]:
        """List knowledge items by status."""
        stmt = select(KnowledgeItemModel).where(
            KnowledgeItemModel.status == status.value
        ).order_by(desc(KnowledgeItemModel.updated_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def search_by_text(
        self, 
        query: str, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[KnowledgeItem]:
        """Search knowledge items by text content."""
        # Simple text search using LIKE (in production, use full-text search)
        search_term = f"%{query.lower()}%"
        
        stmt = select(KnowledgeItemModel).where(
            or_(
                func.lower(KnowledgeItemModel.title).like(search_term),
                func.lower(KnowledgeItemModel.content).like(search_term)
            )
        )
        
        # Apply filters
        if filters:
            if "status" in filters:
                stmt = stmt.where(KnowledgeItemModel.status == filters["status"])
            if "category" in filters:
                stmt = stmt.where(KnowledgeItemModel.category == filters["category"])
            if "target_audience" in filters:
                stmt = stmt.where(KnowledgeItemModel.target_audience == filters["target_audience"])
        
        # Order by relevance (title matches first, then content matches)
        stmt = stmt.order_by(
            func.lower(KnowledgeItemModel.title).like(search_term).desc(),
            desc(KnowledgeItemModel.view_count)
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def search_by_vector(
        self, 
        vector: Vector, 
        threshold: float = 0.7,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Search knowledge items by vector similarity."""
        # For SQLite, we'll implement a simple cosine similarity
        # In production with PostgreSQL, use pgvector
        stmt = select(KnowledgeItemModel).where(
            KnowledgeItemModel.embedding.isnot(None)
        )
        
        # Apply filters
        if filters:
            if "status" in filters:
                stmt = stmt.where(KnowledgeItemModel.status == filters["status"])
            if "category" in filters:
                stmt = stmt.where(KnowledgeItemModel.category == filters["category"])
            if "target_audience" in filters:
                stmt = stmt.where(KnowledgeItemModel.target_audience == filters["target_audience"])
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        # Calculate similarities
        results = []
        for model in models:
            if model.embedding:
                model_vector = Vector(model.embedding)
                similarity = vector.cosine_similarity(model_vector)
                
                if similarity >= threshold:
                    entity = self._to_entity(model)
                    score = SearchScore(similarity)
                    results.append((entity, score))
        
        # Sort by similarity score
        results.sort(key=lambda x: x[1].value, reverse=True)
        
        return results[:limit]
    
    async def count_total(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count total number of knowledge items."""
        stmt = select(func.count(KnowledgeItemModel.id))
        
        # Apply filters
        if filters:
            if "status" in filters:
                stmt = stmt.where(KnowledgeItemModel.status == filters["status"])
            if "category" in filters:
                stmt = stmt.where(KnowledgeItemModel.category == filters["category"])
            if "target_audience" in filters:
                stmt = stmt.where(KnowledgeItemModel.target_audience == filters["target_audience"])
        
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    async def get_popular_items(self, limit: int = 10) -> List[KnowledgeItem]:
        """Get most popular knowledge items by view count."""
        stmt = select(KnowledgeItemModel).where(
            KnowledgeItemModel.status == ContentStatus.PUBLISHED.value
        ).order_by(desc(KnowledgeItemModel.view_count)).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def get_recent_items(self, limit: int = 10) -> List[KnowledgeItem]:
        """Get most recently updated knowledge items."""
        stmt = select(KnowledgeItemModel).where(
            KnowledgeItemModel.status == ContentStatus.PUBLISHED.value
        ).order_by(desc(KnowledgeItemModel.updated_at)).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def create_backup(self, include_embeddings: bool = False) -> str:
        """Create a backup of the knowledge base."""
        import json
        from datetime import datetime
        
        # TODO: Implement actual backup functionality
        # This is a placeholder implementation
        
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get all knowledge items
        stmt = select(KnowledgeItemModel)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        # Prepare backup data
        backup_data = {
            "backup_id": backup_id,
            "created_at": datetime.utcnow().isoformat(),
            "include_embeddings": include_embeddings,
            "items": []
        }
        
        for model in models:
            item_data = {
                "id": str(model.id),
                "title": model.title,
                "content": model.content,
                "content_type": model.content_type,
                "category": model.category,
                "target_audience": model.target_audience,
                "author_id": str(model.author_id),
                "status": model.status,
                "tags": model.tags,
                "created_at": model.created_at.isoformat() if model.created_at else None,
                "updated_at": model.updated_at.isoformat() if model.updated_at else None,
                "published_at": model.published_at.isoformat() if model.published_at else None,
                "view_count": model.view_count,
                "helpful_count": model.helpful_count,
                "unhelpful_count": model.unhelpful_count,
                "version": model.version
            }
            
            if include_embeddings and model.embedding:
                item_data["embedding"] = model.embedding
            
            backup_data["items"].append(item_data)
        
        # TODO: Save backup to actual storage (file system, S3, etc.)
        # For now, just return the backup ID
        
        return backup_id
    
    async def restore_from_backup(
        self, 
        backup_id: str, 
        overwrite_existing: bool = False
    ) -> Dict[str, Any]:
        """Restore knowledge base from backup."""
        # TODO: Implement actual restore functionality
        # This is a placeholder implementation
        
        # Mock restoration result
        result = {
            "items_count": 0,
            "conflicts": 0,
            "errors": []
        }
        
        # TODO: Load backup data from storage
        # TODO: Validate backup integrity
        # TODO: Process each item in backup
        # TODO: Handle conflicts based on overwrite_existing flag
        # TODO: Track restoration progress and errors
        
        return result

    def _to_entity(self, model: KnowledgeItemModel) -> KnowledgeItem:
        """Convert SQLAlchemy model to domain entity."""
        tags = [TagName(tag) for tag in model.tags] if model.tags else []
        embedding = Vector(model.embedding) if model.embedding else None
        
        return KnowledgeItem(
            id=KnowledgeItemId(model.id),
            title=Title(model.title),
            content=Content(model.content),
            content_type=ContentType(model.content_type),
            category=CategoryName(model.category),
            target_audience=TargetAudience(model.target_audience),
            author_id=model.author_id,
            status=ContentStatus(model.status),
            tags=tags,
            embedding=embedding,
            created_at=model.created_at,
            updated_at=model.updated_at,
            published_at=model.published_at,
            view_count=model.view_count,
            helpful_count=model.helpful_count,
            unhelpful_count=model.unhelpful_count,
            version=model.version
        )


class SQLAlchemyCategoryRepository(CategoryRepository):
    """SQLAlchemy implementation of CategoryRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, category: Category) -> Category:
        """Create a new category."""
        model = CategoryModel(
            id=category.id,
            name=category.name.value,
            description=category.description,
            parent_id=category.parent_id,
            sort_order=category.sort_order,
            is_active=category.is_active,
            created_at=category.created_at
        )
        
        self.session.add(model)
        await self.session.flush()
        
        return self._to_entity(model)
    
    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        """Get a category by ID."""
        stmt = select(CategoryModel).where(CategoryModel.id == category_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._to_entity(model)
        return None
    
    async def get_by_name(self, name: CategoryName) -> Optional[Category]:
        """Get a category by name."""
        stmt = select(CategoryModel).where(CategoryModel.name == name.value)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._to_entity(model)
        return None
    
    async def update(self, category: Category) -> Category:
        """Update an existing category."""
        stmt = select(CategoryModel).where(CategoryModel.id == category.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            model.name = category.name.value
            model.description = category.description
            model.parent_id = category.parent_id
            model.sort_order = category.sort_order
            model.is_active = category.is_active
            
            await self.session.flush()
            return self._to_entity(model)
        
        return category
    
    async def delete(self, category_id: UUID) -> bool:
        """Delete a category."""
        stmt = select(CategoryModel).where(CategoryModel.id == category_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
    
    async def list_all(self, include_inactive: bool = False) -> List[Category]:
        """List all categories."""
        stmt = select(CategoryModel)
        
        if not include_inactive:
            stmt = stmt.where(CategoryModel.is_active == True)
        
        stmt = stmt.order_by(CategoryModel.sort_order, CategoryModel.name)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def list_children(self, parent_id: UUID) -> List[Category]:
        """List child categories of a parent category."""
        stmt = select(CategoryModel).where(
            and_(
                CategoryModel.parent_id == parent_id,
                CategoryModel.is_active == True
            )
        ).order_by(CategoryModel.sort_order, CategoryModel.name)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def list_root_categories(self) -> List[Category]:
        """List root categories (no parent)."""
        stmt = select(CategoryModel).where(
            and_(
                CategoryModel.parent_id.is_(None),
                CategoryModel.is_active == True
            )
        ).order_by(CategoryModel.sort_order, CategoryModel.name)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    def _to_entity(self, model: CategoryModel) -> Category:
        """Convert SQLAlchemy model to domain entity."""
        return Category(
            id=model.id,
            name=CategoryName(model.name),
            description=model.description,
            parent_id=model.parent_id,
            sort_order=model.sort_order,
            is_active=model.is_active,
            created_at=model.created_at
        )


class SQLAlchemySearchQueryRepository(SearchQueryRepository):
    """SQLAlchemy implementation of SearchQueryRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, search_query: SearchQuery) -> SearchQuery:
        """Create a new search query record."""
        model = SearchQueryModel(
            id=search_query.id,
            query_text=search_query.query_text,
            user_id=search_query.user_id,
            user_role=search_query.user_role.value,
            filters=search_query.filters,
            created_at=search_query.created_at
        )
        
        self.session.add(model)
        await self.session.flush()
        
        return self._to_entity(model)
    
    async def get_by_id(self, query_id: UUID) -> Optional[SearchQuery]:
        """Get a search query by ID."""
        stmt = select(SearchQueryModel).where(SearchQueryModel.id == query_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._to_entity(model)
        return None
    
    async def list_by_user(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SearchQuery]:
        """List search queries by user."""
        stmt = select(SearchQueryModel).where(
            SearchQueryModel.user_id == user_id
        ).order_by(desc(SearchQueryModel.created_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def get_frequent_queries(
        self, 
        user_role: Optional[UserRole] = None,
        limit: int = 10
    ) -> List[tuple[str, int]]:
        """Get most frequent search queries."""
        stmt = select(
            SearchQueryModel.query_text,
            func.count(SearchQueryModel.query_text).label('count')
        ).group_by(SearchQueryModel.query_text)
        
        if user_role:
            stmt = stmt.where(SearchQueryModel.user_role == user_role.value)
        
        stmt = stmt.order_by(desc('count')).limit(limit)
        
        result = await self.session.execute(stmt)
        return [(row.query_text, row.count) for row in result]
    
    async def get_query_stats(
        self, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get search query statistics."""
        stmt = select(SearchQueryModel)
        
        if start_date:
            stmt = stmt.where(SearchQueryModel.created_at >= start_date)
        if end_date:
            stmt = stmt.where(SearchQueryModel.created_at <= end_date)
        
        # Total queries
        total_stmt = select(func.count(SearchQueryModel.id)).select_from(stmt.subquery())
        total_result = await self.session.execute(total_stmt)
        total_queries = total_result.scalar() or 0
        
        # Unique users
        users_stmt = select(func.count(func.distinct(SearchQueryModel.user_id))).select_from(stmt.subquery())
        users_result = await self.session.execute(users_stmt)
        unique_users = users_result.scalar() or 0
        
        # Queries by role
        role_stmt = select(
            SearchQueryModel.user_role,
            func.count(SearchQueryModel.id).label('count')
        ).group_by(SearchQueryModel.user_role)
        
        if start_date:
            role_stmt = role_stmt.where(SearchQueryModel.created_at >= start_date)
        if end_date:
            role_stmt = role_stmt.where(SearchQueryModel.created_at <= end_date)
        
        role_result = await self.session.execute(role_stmt)
        queries_by_role = {row.user_role: row.count for row in role_result}
        
        return {
            "total_queries": total_queries,
            "unique_users": unique_users,
            "queries_by_role": queries_by_role
        }
    
    def _to_entity(self, model: SearchQueryModel) -> SearchQuery:
        """Convert SQLAlchemy model to domain entity."""
        return SearchQuery(
            id=model.id,
            query_text=model.query_text,
            user_id=model.user_id,
            user_role=UserRole(model.user_role),
            filters=model.filters or {},
            created_at=model.created_at
        )


class SQLAlchemyFeedbackRepository(FeedbackRepository):
    """SQLAlchemy implementation of FeedbackRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, feedback: Feedback) -> Feedback:
        """Create a new feedback record."""
        model = FeedbackModel(
            id=feedback.id,
            item_id=feedback.item_id,
            user_id=feedback.user_id,
            feedback_type=feedback.feedback_type,
            comment=feedback.comment,
            created_at=feedback.created_at
        )
        
        self.session.add(model)
        await self.session.flush()
        
        return self._to_entity(model)
    
    async def get_by_id(self, feedback_id: UUID) -> Optional[Feedback]:
        """Get a feedback record by ID."""
        stmt = select(FeedbackModel).where(FeedbackModel.id == feedback_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            return self._to_entity(model)
        return None
    
    async def list_by_item(
        self, 
        item_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Feedback]:
        """List feedback for a specific knowledge item."""
        stmt = select(FeedbackModel).where(
            FeedbackModel.item_id == item_id
        ).order_by(desc(FeedbackModel.created_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def list_by_user(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Feedback]:
        """List feedback submitted by a user."""
        stmt = select(FeedbackModel).where(
            FeedbackModel.user_id == user_id
        ).order_by(desc(FeedbackModel.created_at)).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def get_average_rating(self, item_id: UUID) -> float:
        """Get the average rating for a knowledge item (helpful/unhelpful ratio)."""
        # Count helpful vs total feedback
        stmt_helpful = select(func.count(FeedbackModel.id)).where(
            and_(
                FeedbackModel.item_id == item_id,
                FeedbackModel.feedback_type == "helpful"
            )
        )
        stmt_total = select(func.count(FeedbackModel.id)).where(
            FeedbackModel.item_id == item_id
        )
        
        helpful_result = await self.session.execute(stmt_helpful)
        total_result = await self.session.execute(stmt_total)
        
        helpful_count = helpful_result.scalar() or 0
        total_count = total_result.scalar() or 0
        
        return helpful_count / total_count if total_count > 0 else 0.0
    
    def _to_entity(self, model: FeedbackModel) -> Feedback:
        """Convert SQLAlchemy model to domain entity."""
        return Feedback(
            id=model.id,
            item_id=model.item_id,
            user_id=model.user_id,
            feedback_type=model.feedback_type,
            comment=model.comment,
            created_at=model.created_at
        )
