"""Domain exceptions for Knowledge Base Service."""


class KbDomainException(Exception):
    """Base exception for knowledge base domain."""
    pass


class KnowledgeItemNotFoundError(KbDomainException):
    """Exception raised when a knowledge item is not found."""
    
    def __init__(self, item_id: str):
        """Initialize the exception."""
        super().__init__(f"Knowledge item with ID {item_id} not found")
        self.item_id = item_id


class InvalidContentError(KbDomainException):
    """Exception raised when content is invalid."""
    
    def __init__(self, message: str = "Invalid content provided"):
        """Initialize the exception."""
        super().__init__(message)


class SearchError(KbDomainException):
    """Exception raised when search operation fails."""
    
    def __init__(self, message: str = "Search operation failed"):
        """Initialize the exception."""
        super().__init__(message)


class EmbeddingError(KbDomainException):
    """Exception raised when embedding operation fails."""
    
    def __init__(self, message: str = "Embedding operation failed"):
        """Initialize the exception."""
        super().__init__(message)


class CategoryNotFoundError(KbDomainException):
    """Exception raised when a category is not found."""
    
    def __init__(self, category_id: str):
        """Initialize the exception."""
        super().__init__(f"Category with ID {category_id} not found")
        self.category_id = category_id


class UnauthorizedAccessError(KbDomainException):
    """Exception raised when user doesn't have access to content."""
    
    def __init__(self, message: str = "Unauthorized access to content"):
        """Initialize the exception."""
        super().__init__(message)


class DuplicateContentError(KbDomainException):
    """Exception raised when trying to create duplicate content."""
    
    def __init__(self, message: str = "Content already exists"):
        """Initialize the exception."""
        super().__init__(message)


class InvalidSearchQueryError(KbDomainException):
    """Exception raised when search query is invalid."""
    
    def __init__(self, message: str = "Invalid search query"):
        """Initialize the exception."""
        super().__init__(message)


class VectorDimensionMismatchError(KbDomainException):
    """Exception raised when vector dimensions don't match."""
    
    def __init__(self, expected: int, actual: int):
        """Initialize the exception."""
        super().__init__(f"Vector dimension mismatch: expected {expected}, got {actual}")
        self.expected = expected
        self.actual = actual


class ContentTooLongError(KbDomainException):
    """Exception raised when content exceeds maximum length."""
    
    def __init__(self, max_length: int, actual_length: int):
        """Initialize the exception."""
        super().__init__(f"Content too long: maximum {max_length} characters, got {actual_length}")
        self.max_length = max_length
        self.actual_length = actual_length
