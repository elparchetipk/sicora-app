"""Domain package."""

from .entities import *
from .value_objects import *
from .exceptions import *
from .repositories import *
from .services import *

__all__ = [
    # Entities
    "KnowledgeItem",
    "Category",
    "SearchQuery",
    "UserRole",
    "ContentType",
    "ContentStatus",
    "TargetAudience",
    
    # Value objects
    "KnowledgeItemId",
    "Title",
    "Content",
    "CategoryName",
    "TagName",
    "Vector",
    "SearchScore",
    
    # Exceptions
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
    "ContentTooLongError",
    
    # Repositories
    "KnowledgeItemRepository",
    "CategoryRepository",
    "SearchQueryRepository",
    
    # Services
    "EmbeddingService",
    "SearchService",
    "ContentValidationService",
    "ChatbotIntegrationService",
    "PersonalizationService"
]
