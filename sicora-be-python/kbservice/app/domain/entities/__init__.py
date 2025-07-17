"""Domain entities package."""

from .kb_entities import (
    KnowledgeItem,
    Category,
    SearchQuery,
    UserRole,
    ContentType,
    ContentStatus,
    TargetAudience
)

__all__ = [
    "KnowledgeItem",
    "Category", 
    "SearchQuery",
    "UserRole",
    "ContentType",
    "ContentStatus",
    "TargetAudience"
]
