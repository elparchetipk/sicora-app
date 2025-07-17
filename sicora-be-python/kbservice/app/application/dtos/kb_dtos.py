"""Data Transfer Objects for Knowledge Base Service."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

from app.domain.entities.kb_entities import ContentType, ContentStatus, TargetAudience, UserRole


class KnowledgeItemCreateDTO(BaseModel):
    """DTO for creating a knowledge item."""
    title: str = Field(..., min_length=1, max_length=200, description="Knowledge item title")
    content: str = Field(..., min_length=1, max_length=50000, description="Knowledge item content")
    content_type: ContentType = Field(..., description="Type of content")
    category: str = Field(..., min_length=1, max_length=100, description="Category name")
    target_audience: TargetAudience = Field(..., description="Target audience")
    tags: Optional[List[str]] = Field(default=[], description="List of tags")
    status: ContentStatus = Field(default=ContentStatus.DRAFT, description="Content status")
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if v:
            for tag in v:
                if not tag.strip() or len(tag.strip()) > 50:
                    raise ValueError("Tags must be non-empty and max 50 characters")
        return [tag.strip().lower() for tag in v] if v else []


class KnowledgeItemUpdateDTO(BaseModel):
    """DTO for updating a knowledge item."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Knowledge item title")
    content: Optional[str] = Field(None, min_length=1, max_length=50000, description="Knowledge item content")
    content_type: Optional[ContentType] = Field(None, description="Type of content")
    category: Optional[str] = Field(None, min_length=1, max_length=100, description="Category name")
    target_audience: Optional[TargetAudience] = Field(None, description="Target audience")
    tags: Optional[List[str]] = Field(None, description="List of tags")
    status: Optional[ContentStatus] = Field(None, description="Content status")
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if v is not None:
            for tag in v:
                if not tag.strip() or len(tag.strip()) > 50:
                    raise ValueError("Tags must be non-empty and max 50 characters")
            return [tag.strip().lower() for tag in v]
        return v


class KnowledgeItemResponseDTO(BaseModel):
    """DTO for knowledge item response."""
    id: UUID
    title: str
    content: str
    content_type: ContentType
    category: str
    target_audience: TargetAudience
    author_id: UUID
    status: ContentStatus
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]
    view_count: int
    helpful_count: int
    unhelpful_count: int
    version: int
    
    class Config:
        from_attributes = True


class KnowledgeItemListDTO(BaseModel):
    """DTO for knowledge item list response."""
    id: UUID
    title: str
    content_snippet: str
    content_type: ContentType
    category: str
    target_audience: TargetAudience
    status: ContentStatus
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    view_count: int
    helpful_count: int
    
    class Config:
        from_attributes = True


class CategoryCreateDTO(BaseModel):
    """DTO for creating a category."""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: str = Field(..., min_length=1, max_length=500, description="Category description")
    parent_id: Optional[UUID] = Field(None, description="Parent category ID")
    sort_order: int = Field(default=0, description="Sort order")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not all(c.isalnum() or c in ' -_áéíóúñÁÉÍÓÚÑ' for c in v.strip()):
            raise ValueError("Category name contains invalid characters")
        return v.strip()


class CategoryResponseDTO(BaseModel):
    """DTO for category response."""
    id: UUID
    name: str
    description: str
    parent_id: Optional[UUID]
    sort_order: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class SearchRequestDTO(BaseModel):
    """DTO for search requests."""
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    filters: Optional[Dict[str, Any]] = Field(default={}, description="Search filters")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results")
    offset: int = Field(default=0, ge=0, description="Results offset")


class SearchResultDTO(BaseModel):
    """DTO for search result."""
    item: KnowledgeItemListDTO
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")
    snippet: str = Field(..., description="Content snippet with highlights")
    
    class Config:
        from_attributes = True


class SearchResponseDTO(BaseModel):
    """DTO for search response."""
    results: List[SearchResultDTO]
    total_count: int
    query: str
    filters: Dict[str, Any]
    suggestions: List[str] = Field(default=[], description="Query suggestions")
    
    class Config:
        from_attributes = True


class QueryRequestDTO(BaseModel):
    """DTO for intelligent query requests."""
    query: str = Field(..., min_length=1, max_length=1000, description="User query")
    context: Optional[Dict[str, Any]] = Field(default={}, description="User context")
    include_chatbot: bool = Field(default=True, description="Include chatbot response")
    
    @field_validator('context')
    @classmethod
    def validate_context(cls, v):
        if v is None:
            return {}
        return v


class QueryResponseDTO(BaseModel):
    """DTO for intelligent query response."""
    answer: str = Field(..., description="Generated answer")
    sources: List[KnowledgeItemListDTO] = Field(..., description="Source knowledge items")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence")
    suggestions: List[str] = Field(default=[], description="Related suggestions")
    chatbot_used: bool = Field(default=False, description="Whether chatbot was consulted")
    
    class Config:
        from_attributes = True


class FeedbackDTO(BaseModel):
    """DTO for user feedback."""
    item_id: UUID = Field(..., description="Knowledge item ID")
    feedback_type: str = Field(..., pattern="^(helpful|unhelpful)$", description="Feedback type")
    comment: Optional[str] = Field(None, max_length=500, description="Optional comment")


class FeedbackCreateDTO(BaseModel):
    """DTO for creating feedback."""
    item_id: UUID
    feedback_type: str = Field(..., pattern="^(helpful|unhelpful)$")
    comment: Optional[str] = Field(None, max_length=500)


class FeedbackResponseDTO(BaseModel):
    """DTO for feedback response."""
    id: UUID
    item_id: UUID
    user_id: UUID
    feedback_type: str
    comment: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MetricsResponseDTO(BaseModel):
    """DTO for metrics response."""
    total_items: int
    total_queries: int
    popular_items: List[KnowledgeItemListDTO]
    frequent_queries: List[Dict[str, Any]]
    user_activity: Dict[str, Any]
    performance_stats: Dict[str, Any]
    
    class Config:
        from_attributes = True


class PaginationResponseDTO(BaseModel):
    """DTO for paginated responses."""
    items: List[Any] = Field(..., description="List of items")
    total_count: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_previous: bool = Field(..., description="Whether there are previous pages")
    
    class Config:
        from_attributes = True
