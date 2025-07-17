"""Knowledge base entry entity for AI Service."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
import uuid


class KnowledgeEntry:
    """Knowledge base entry domain entity."""
    
    def __init__(
        self,
        entry_id: Optional[UUID] = None,
        title: str = "",
        content: str = "",
        category: str = "general",
        tags: Optional[List[str]] = None,
        embedding: Optional[List[float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_active: bool = True,
        relevance_score: Optional[float] = None
    ):
        self.entry_id = entry_id or uuid.uuid4()
        self.title = title
        self.content = content
        self.category = category
        self.tags = tags or []
        self.embedding = embedding
        self.metadata = metadata or {}
        self.source = source
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_active = is_active
        self.relevance_score = relevance_score
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the knowledge entry."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the knowledge entry."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()
    
    def update_content(self, new_content: str) -> None:
        """Update the content of the knowledge entry."""
        self.content = new_content
        self.updated_at = datetime.utcnow()
        # Reset embedding when content changes
        self.embedding = None
    
    def update_embedding(self, embedding: List[float]) -> None:
        """Update the embedding vector."""
        self.embedding = embedding
        self.updated_at = datetime.utcnow()
    
    def set_relevance_score(self, score: float) -> None:
        """Set the relevance score for search results."""
        self.relevance_score = score
    
    def deactivate(self) -> None:
        """Deactivate the knowledge entry."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def get_content_preview(self, max_length: int = 100) -> str:
        """Get a preview of the content."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."
    
    def has_embedding(self) -> bool:
        """Check if the entry has an embedding."""
        return self.embedding is not None and len(self.embedding) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert knowledge entry to dictionary."""
        return {
            "entry_id": str(self.entry_id),
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "metadata": self.metadata,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "relevance_score": self.relevance_score,
            "has_embedding": self.has_embedding(),
            "content_preview": self.get_content_preview()
        }
    
    def __str__(self) -> str:
        return f"KnowledgeEntry(id={self.entry_id}, title='{self.title}', category='{self.category}')"
    
    def __repr__(self) -> str:
        return self.__str__()
