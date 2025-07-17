"""Exceptions package."""

from .kb_exceptions import (
    KbDomainException,
    KnowledgeItemNotFoundError,
    InvalidContentError,
    SearchError,
    EmbeddingError,
    CategoryNotFoundError,
    UnauthorizedAccessError,
    DuplicateContentError,
    InvalidSearchQueryError,
    VectorDimensionMismatchError,
    ContentTooLongError
)

__all__ = [
    "KbDomainException",
    "KnowledgeItemNotFoundError",
    "InvalidContentError",
    "SearchError",
    "EmbeddingError",
    "CategoryNotFoundError",
    "UnauthorizedAccessError",
    "DuplicateContentError",
    "InvalidSearchQueryError",
    "VectorDimensionMismatchError",
    "ContentTooLongError"
]
