"""Repository interfaces for Knowledge Base Service."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.domain.entities.kb_entities import (
    KnowledgeItem,
    Category,
    SearchQuery,
    UserRole,
    ContentType,
    ContentStatus,
    TargetAudience
)
from app.domain.value_objects.kb_value_objects import (
    KnowledgeItemId,
    CategoryName,
    Vector,
    SearchScore
)


class KnowledgeItemRepository(ABC):
    """Repository interface for knowledge items."""
    
    @abstractmethod
    async def create(self, knowledge_item: KnowledgeItem) -> KnowledgeItem:
        """Create a new knowledge item."""
        pass
    
    @abstractmethod
    async def get_by_id(self, item_id: KnowledgeItemId) -> Optional[KnowledgeItem]:
        """Get a knowledge item by ID."""
        pass
    
    @abstractmethod
    async def update(self, knowledge_item: KnowledgeItem) -> KnowledgeItem:
        """Update an existing knowledge item."""
        pass
    
    @abstractmethod
    async def delete(self, item_id: KnowledgeItemId) -> bool:
        """Delete a knowledge item."""
        pass
    
    @abstractmethod
    async def list_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[KnowledgeItem]:
        """List all knowledge items with optional filters."""
        pass
    
    @abstractmethod
    async def list_by_category(
        self, 
        category: CategoryName, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[KnowledgeItem]:
        """List knowledge items by category."""
        pass
    
    @abstractmethod
    async def list_by_target_audience(
        self, 
        target_audience: TargetAudience, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[KnowledgeItem]:
        """List knowledge items by target audience."""
        pass
    
    @abstractmethod
    async def list_by_status(
        self, 
        status: ContentStatus, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[KnowledgeItem]:
        """List knowledge items by status."""
        pass
    
    @abstractmethod
    async def search_by_text(
        self, 
        query: str, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[KnowledgeItem]:
        """Search knowledge items by text content."""
        pass
    
    @abstractmethod
    async def search_by_vector(
        self, 
        vector: Vector, 
        threshold: float = 0.7,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Search knowledge items by vector similarity."""
        pass
    
    @abstractmethod
    async def count_total(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count total number of knowledge items."""
        pass
    
    @abstractmethod
    async def get_popular_items(self, limit: int = 10) -> List[KnowledgeItem]:
        """Get most popular knowledge items by view count."""
        pass
    
    @abstractmethod
    async def get_recent_items(self, limit: int = 10) -> List[KnowledgeItem]:
        """Get most recently updated knowledge items."""
        pass
    
    @abstractmethod
    async def create_backup(self, include_embeddings: bool = False) -> str:
        """Create a backup of the knowledge base."""
        pass
    
    @abstractmethod
    async def restore_from_backup(
        self, 
        backup_id: str, 
        overwrite_existing: bool = False
    ) -> Dict[str, Any]:
        """Restore knowledge base from backup."""
        pass


class CategoryRepository(ABC):
    """Repository interface for categories."""
    
    @abstractmethod
    async def create(self, category: Category) -> Category:
        """Create a new category."""
        pass
    
    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        """Get a category by ID."""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: CategoryName) -> Optional[Category]:
        """Get a category by name."""
        pass
    
    @abstractmethod
    async def update(self, category: Category) -> Category:
        """Update an existing category."""
        pass
    
    @abstractmethod
    async def delete(self, category_id: UUID) -> bool:
        """Delete a category."""
        pass
    
    @abstractmethod
    async def list_all(self, include_inactive: bool = False) -> List[Category]:
        """List all categories."""
        pass
    
    @abstractmethod
    async def list_children(self, parent_id: UUID) -> List[Category]:
        """List child categories of a parent category."""
        pass
    
    @abstractmethod
    async def list_root_categories(self) -> List[Category]:
        """List root categories (no parent)."""
        pass


class SearchQueryRepository(ABC):
    """Repository interface for search queries."""
    
    @abstractmethod
    async def create(self, search_query: SearchQuery) -> SearchQuery:
        """Create a new search query record."""
        pass
    
    @abstractmethod
    async def get_by_id(self, query_id: UUID) -> Optional[SearchQuery]:
        """Get a search query by ID."""
        pass
    
    @abstractmethod
    async def list_by_user(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[SearchQuery]:
        """List search queries by user."""
        pass
    
    @abstractmethod
    async def get_frequent_queries(
        self, 
        user_role: Optional[UserRole] = None,
        limit: int = 10
    ) -> List[tuple[str, int]]:
        """Get most frequent search queries."""
        pass
    
    @abstractmethod
    async def get_query_stats(
        self, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get search query statistics."""
        pass


class QueryAnalyticsRepository(ABC):
    """Repository interface for query analytics."""
    
    @abstractmethod
    async def get_service_metrics(self, period: str) -> Dict[str, Any]:
        """Get service metrics for analytics."""
        pass
    
    @abstractmethod
    async def get_query_patterns(self, period: str, limit: int) -> List[Dict[str, Any]]:
        """Get query patterns for analysis."""
        pass


class FeedbackRepository(ABC):
    """Repository interface for user feedback."""
    
    @abstractmethod
    async def create(self, feedback: "Feedback") -> "Feedback":
        """Create a new feedback record."""
        pass
    
    @abstractmethod
    async def get_by_id(self, feedback_id: UUID) -> Optional["Feedback"]:
        """Get feedback by ID."""
        pass
    
    @abstractmethod
    async def list_by_item(
        self, 
        item_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List["Feedback"]:
        """List feedback for a knowledge item."""
        pass
    
    @abstractmethod
    async def list_by_user(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List["Feedback"]:
        """List feedback by user."""
        pass
    
    @abstractmethod
    async def get_feedback_stats(self, item_id: UUID) -> Dict[str, int]:
        """Get feedback statistics for an item."""
        pass
