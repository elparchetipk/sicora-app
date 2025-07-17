"""Vector store interface for knowledge base operations."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple

from app.domain.entities.knowledge_entry import KnowledgeEntry


class VectorStoreInterface(ABC):
    """Abstract interface for vector store operations."""
    
    @abstractmethod
    async def add_document(
        self,
        entry: KnowledgeEntry,
        embedding: List[float]
    ) -> str:
        """Add a document with its embedding to the vector store."""
        pass
    
    @abstractmethod
    async def search_similar(
        self,
        query_embedding: List[float],
        limit: int = 10,
        similarity_threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[KnowledgeEntry, float]]:
        """Search for similar documents using embedding."""
        pass
    
    @abstractmethod
    async def search_by_text(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[KnowledgeEntry, float]]:
        """Search for documents using text query."""
        pass
    
    @abstractmethod
    async def update_document(
        self,
        entry_id: str,
        entry: KnowledgeEntry,
        embedding: List[float]
    ) -> bool:
        """Update a document and its embedding."""
        pass
    
    @abstractmethod
    async def delete_document(self, entry_id: str) -> bool:
        """Delete a document from the vector store."""
        pass
    
    @abstractmethod
    async def get_document(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Get a document by ID."""
        pass
    
    @abstractmethod
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store collection."""
        pass
    
    @abstractmethod
    async def create_collection(self, collection_name: str) -> bool:
        """Create a new collection."""
        pass
    
    @abstractmethod
    async def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection."""
        pass
    
    @abstractmethod
    async def bulk_add_documents(
        self,
        entries: List[Tuple[KnowledgeEntry, List[float]]]
    ) -> List[str]:
        """Bulk add multiple documents."""
        pass
    
    @abstractmethod
    async def get_documents_by_category(
        self,
        category: str,
        limit: int = 100
    ) -> List[KnowledgeEntry]:
        """Get documents by category."""
        pass
    
    @abstractmethod
    async def backup_collection(self, backup_path: str) -> bool:
        """Backup the collection to a file."""
        pass
    
    @abstractmethod
    async def restore_collection(self, backup_path: str) -> bool:
        """Restore the collection from a backup."""
        pass
