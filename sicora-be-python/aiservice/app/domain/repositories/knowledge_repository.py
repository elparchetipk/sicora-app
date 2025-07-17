"""Knowledge repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.domain.entities.knowledge_entry import KnowledgeEntry


class KnowledgeRepository(ABC):
    """Abstract repository for knowledge base management."""
    
    @abstractmethod
    async def create(self, entry: KnowledgeEntry) -> KnowledgeEntry:
        """Create a new knowledge entry."""
        pass
    
    @abstractmethod
    async def get_by_id(self, entry_id: UUID) -> Optional[KnowledgeEntry]:
        """Get knowledge entry by ID."""
        pass
    
    @abstractmethod
    async def get_by_category(
        self, 
        category: str, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[KnowledgeEntry]:
        """Get knowledge entries by category."""
        pass
    
    @abstractmethod
    async def search_by_text(
        self, 
        query: str, 
        limit: int = 10,
        category: Optional[str] = None
    ) -> List[KnowledgeEntry]:
        """Search knowledge entries by text."""
        pass
    
    @abstractmethod
    async def search_by_embedding(
        self, 
        embedding: List[float], 
        limit: int = 10,
        similarity_threshold: float = 0.7,
        category: Optional[str] = None
    ) -> List[KnowledgeEntry]:
        """Search knowledge entries by embedding similarity."""
        pass
    
    @abstractmethod
    async def update(self, entry: KnowledgeEntry) -> KnowledgeEntry:
        """Update an existing knowledge entry."""
        pass
    
    @abstractmethod
    async def delete(self, entry_id: UUID) -> bool:
        """Delete a knowledge entry."""
        pass
    
    @abstractmethod
    async def get_by_tags(
        self, 
        tags: List[str], 
        limit: int = 50
    ) -> List[KnowledgeEntry]:
        """Get knowledge entries by tags."""
        pass
    
    @abstractmethod
    async def get_all_categories(self) -> List[str]:
        """Get all available categories."""
        pass
    
    @abstractmethod
    async def get_all_tags(self) -> List[str]:
        """Get all available tags."""
        pass
    
    @abstractmethod
    async def get_entries_without_embeddings(self, limit: int = 100) -> List[KnowledgeEntry]:
        """Get entries that don't have embeddings yet."""
        pass
    
    @abstractmethod
    async def bulk_update_embeddings(
        self, 
        updates: List[Dict[str, Any]]
    ) -> int:
        """Bulk update embeddings for multiple entries."""
        pass
    
    @abstractmethod
    async def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        pass
