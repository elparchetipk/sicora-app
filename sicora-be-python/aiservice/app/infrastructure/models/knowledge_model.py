"""Knowledge entry SQLAlchemy model."""

from sqlalchemy import Column, String, Text, JSON, ARRAY, Float
from sqlalchemy.types import TypeDecorator, TEXT
import json
from .base_model import BaseModel


class JSONEncodedList(TypeDecorator):
    """Custom type for storing lists as JSON strings."""
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)


class KnowledgeEntryModel(BaseModel):
    """SQLAlchemy model for knowledge base entries."""
    __tablename__ = "knowledge_entries"
    
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), default="general", nullable=False, index=True)
    tags = Column(JSONEncodedList, default=list, nullable=False)
    source = Column(String(500), nullable=True)
    embedding = Column(JSONEncodedList, nullable=True)  # Store embedding as JSON list
    entry_metadata = Column(JSON, default=dict, nullable=False)
    relevance_score = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<KnowledgeEntry(id={self.id}, title='{self.title}', category='{self.category}')>"
    
    @property
    def has_embedding(self) -> bool:
        """Check if entry has an embedding."""
        return self.embedding is not None and len(self.embedding) > 0
    
    def get_content_preview(self, max_length: int = 100) -> str:
        """Get a preview of the content."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."
