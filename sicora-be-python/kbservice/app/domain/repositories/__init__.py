"""Repository interfaces package."""

from .kb_repositories import (
    KnowledgeItemRepository,
    CategoryRepository,
    SearchQueryRepository
)

__all__ = [
    "KnowledgeItemRepository",
    "CategoryRepository",
    "SearchQueryRepository"
]
