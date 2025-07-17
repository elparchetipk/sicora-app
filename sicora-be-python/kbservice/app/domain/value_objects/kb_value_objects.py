"""Value objects for Knowledge Base Service."""

from typing import List, Union
from uuid import UUID


class KnowledgeItemId:
    """Value object for knowledge item identifier."""
    
    def __init__(self, value: UUID):
        """Initialize knowledge item ID."""
        if not isinstance(value, UUID):
            raise ValueError("Knowledge item ID must be a UUID")
        self._value = value
    
    @property
    def value(self) -> UUID:
        """Get the UUID value."""
        return self._value
    
    def __str__(self) -> str:
        """String representation."""
        return str(self._value)
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, KnowledgeItemId):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        """Hash function."""
        return hash(self._value)


class Title:
    """Value object for knowledge item title."""
    
    def __init__(self, value: str):
        """Initialize title."""
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value.strip()) > 200:
            raise ValueError("Title cannot be longer than 200 characters")
        self._value = value.strip()
    
    @property
    def value(self) -> str:
        """Get the title value."""
        return self._value
    
    def __str__(self) -> str:
        """String representation."""
        return self._value
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Title):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        """Hash function."""
        return hash(self._value)


class Content:
    """Value object for knowledge item content."""
    
    def __init__(self, value: str):
        """Initialize content."""
        if not value or not value.strip():
            raise ValueError("Content cannot be empty")
        if len(value.strip()) > 50000:  # 50KB limit
            raise ValueError("Content cannot be longer than 50000 characters")
        self._value = value.strip()
    
    @property
    def value(self) -> str:
        """Get the content value."""
        return self._value
    
    def __str__(self) -> str:
        """String representation."""
        return self._value
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Content):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        """Hash function."""
        return hash(self._value)
    
    def get_snippet(self, length: int = 200) -> str:
        """Get a content snippet of specified length."""
        if len(self._value) <= length:
            return self._value
        return self._value[:length] + "..."


class CategoryName:
    """Value object for category name."""
    
    def __init__(self, value: str):
        """Initialize category name."""
        if not value or not value.strip():
            raise ValueError("Category name cannot be empty")
        if len(value.strip()) > 100:
            raise ValueError("Category name cannot be longer than 100 characters")
        # Validate format (alphanumeric, spaces, hyphens, underscores)
        cleaned_value = value.strip()
        if not all(c.isalnum() or c in ' -_áéíóúñÁÉÍÓÚÑ' for c in cleaned_value):
            raise ValueError("Category name contains invalid characters")
        self._value = cleaned_value
    
    @property
    def value(self) -> str:
        """Get the category name value."""
        return self._value
    
    def __str__(self) -> str:
        """String representation."""
        return self._value
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, CategoryName):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        """Hash function."""
        return hash(self._value)


class TagName:
    """Value object for tag name."""
    
    def __init__(self, value: str):
        """Initialize tag name."""
        if not value or not value.strip():
            raise ValueError("Tag name cannot be empty")
        if len(value.strip()) > 50:
            raise ValueError("Tag name cannot be longer than 50 characters")
        # Validate format (alphanumeric, hyphens, underscores)
        cleaned_value = value.strip().lower()
        if not all(c.isalnum() or c in '-_áéíóúñ' for c in cleaned_value):
            raise ValueError("Tag name contains invalid characters")
        self._value = cleaned_value
    
    @property
    def value(self) -> str:
        """Get the tag name value."""
        return self._value
    
    def __str__(self) -> str:
        """String representation."""
        return self._value
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, TagName):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        """Hash function."""
        return hash(self._value)


class Vector:
    """Value object for embedding vector."""
    
    def __init__(self, values: List[float]):
        """Initialize vector."""
        if not values:
            raise ValueError("Vector cannot be empty")
        if not all(isinstance(v, (int, float)) for v in values):
            raise ValueError("Vector must contain only numeric values")
        if len(values) > 2000:  # Reasonable limit for embedding dimensions
            raise ValueError("Vector dimension too large")
        self._values = [float(v) for v in values]
    
    @property
    def values(self) -> List[float]:
        """Get the vector values."""
        return self._values.copy()
    
    @property
    def dimension(self) -> int:
        """Get the vector dimension."""
        return len(self._values)
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Vector):
            return False
        return self._values == other._values
    
    def __hash__(self) -> int:
        """Hash function."""
        return hash(tuple(self._values))
    
    def cosine_similarity(self, other: 'Vector') -> float:
        """Calculate cosine similarity with another vector."""
        if self.dimension != other.dimension:
            raise ValueError("Vectors must have the same dimension")
        
        dot_product = sum(a * b for a, b in zip(self._values, other._values))
        magnitude_a = sum(a * a for a in self._values) ** 0.5
        magnitude_b = sum(b * b for b in other._values) ** 0.5
        
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
        
        return dot_product / (magnitude_a * magnitude_b)


class SearchScore:
    """Value object for search result score."""
    
    def __init__(self, value: float):
        """Initialize search score."""
        if not isinstance(value, (int, float)):
            raise ValueError("Search score must be numeric")
        if value < 0.0 or value > 1.0:
            raise ValueError("Search score must be between 0.0 and 1.0")
        self._value = float(value)
    
    @property
    def value(self) -> float:
        """Get the score value."""
        return self._value
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self._value:.3f}"
    
    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, SearchScore):
            return False
        return abs(self._value - other._value) < 1e-9
    
    def __lt__(self, other) -> bool:
        """Less than comparison."""
        if not isinstance(other, SearchScore):
            return NotImplemented
        return self._value < other._value
    
    def __gt__(self, other) -> bool:
        """Greater than comparison."""
        if not isinstance(other, SearchScore):
            return NotImplemented
        return self._value > other._value
