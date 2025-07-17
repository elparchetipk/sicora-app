"""DTOs for AI Service application layer."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class MessageDTO(BaseModel):
    """Data transfer object for messages."""
    message_id: Optional[UUID] = None
    content: str = Field(..., min_length=1, max_length=10000)
    role: str = Field(..., pattern="^(user|assistant|system)$")
    message_type: str = Field(default="text", pattern="^(text|image|file|code|function_call)$")
    tokens: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    model_used: Optional[str] = None
    processing_time: Optional[float] = None


class ConversationCreateDTO(BaseModel):
    """DTO for creating a new conversation."""
    user_id: UUID = Field(..., description="ID of the user creating the conversation")
    title: Optional[str] = Field(default="Nueva Conversación", max_length=200)
    initial_message: Optional[str] = Field(None, max_length=10000)
    metadata: Optional[Dict[str, Any]] = None


class ConversationUpdateDTO(BaseModel):
    """DTO for updating a conversation."""
    title: Optional[str] = Field(None, max_length=200)
    metadata: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ConversationResponseDTO(BaseModel):
    """DTO for conversation responses."""
    conversation_id: UUID
    user_id: UUID
    title: str
    message_count: int
    total_tokens: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    last_message: Optional[MessageDTO] = None
    metadata: Optional[Dict[str, Any]] = None


class ChatRequestDTO(BaseModel):
    """DTO for chat requests."""
    conversation_id: Optional[UUID] = None
    user_id: UUID
    message: str = Field(..., min_length=1, max_length=10000)
    model_name: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0, le=8000)
    use_knowledge_base: bool = Field(default=True)
    include_context: bool = Field(default=True)


class ChatResponseDTO(BaseModel):
    """DTO for chat responses."""
    conversation_id: UUID
    message_id: UUID
    response: str
    model_used: str
    tokens_used: int
    processing_time: float
    knowledge_sources: Optional[List[str]] = None
    timestamp: datetime


class KnowledgeEntryCreateDTO(BaseModel):
    """DTO for creating knowledge entries."""
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1, max_length=50000)
    category: str = Field(default="general", max_length=100)
    tags: Optional[List[str]] = Field(default_factory=list)
    source: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeEntryUpdateDTO(BaseModel):
    """DTO for updating knowledge entries."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=1, max_length=50000)
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    source: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class KnowledgeEntryResponseDTO(BaseModel):
    """DTO for knowledge entry responses."""
    entry_id: UUID
    title: str
    content: str
    category: str
    tags: List[str]
    source: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    relevance_score: Optional[float] = None
    has_embedding: bool


class KnowledgeSearchDTO(BaseModel):
    """DTO for knowledge search requests."""
    query: str = Field(..., min_length=1, max_length=1000)
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    limit: int = Field(default=10, ge=1, le=50)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    use_semantic_search: bool = Field(default=True)


class AIModelCreateDTO(BaseModel):
    """DTO for creating AI model configurations."""
    name: str = Field(..., min_length=1, max_length=100)
    model_type: str = Field(..., pattern="^(openai_gpt|anthropic_claude|huggingface|local)$")
    model_name: str = Field(..., min_length=1, max_length=200)
    api_endpoint: Optional[str] = None
    api_key_name: Optional[str] = None
    max_tokens: int = Field(default=4096, gt=0, le=32000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    context_window: int = Field(default=4096, gt=0, le=200000)
    cost_per_token: float = Field(default=0.0, ge=0.0)
    supported_features: Optional[List[str]] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None


class AIModelUpdateDTO(BaseModel):
    """DTO for updating AI model configurations."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    api_endpoint: Optional[str] = None
    max_tokens: Optional[int] = Field(None, gt=0, le=32000)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    context_window: Optional[int] = Field(None, gt=0, le=200000)
    cost_per_token: Optional[float] = Field(None, ge=0.0)
    status: Optional[str] = Field(None, pattern="^(active|inactive|maintenance|error)$")
    supported_features: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class AIModelResponseDTO(BaseModel):
    """DTO for AI model responses."""
    model_id: UUID
    name: str
    model_type: str
    model_name: str
    api_endpoint: Optional[str]
    max_tokens: int
    temperature: float
    context_window: int
    cost_per_token: float
    status: str
    supported_features: List[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    is_available: bool


class AnalyticsRequestDTO(BaseModel):
    """DTO for analytics requests."""
    user_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metric_types: Optional[List[str]] = Field(default_factory=list)
    group_by: Optional[str] = Field(None, pattern="^(day|week|month|user|model)$")


class AnalyticsResponseDTO(BaseModel):
    """DTO for analytics responses."""
    total_conversations: int
    total_messages: int
    total_tokens: int
    avg_response_time: float
    most_used_models: Dict[str, int]
    user_activity: Dict[str, Any]
    time_period: Dict[str, datetime]
    detailed_metrics: Optional[Dict[str, Any]] = None


class KnowledgeSearchResult(BaseModel):
    """DTO for knowledge search results from KbService."""
    id: UUID
    title: str
    content: str
    category: str
    content_type: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    source: str = "kbservice"
    metadata: Optional[Dict[str, Any]] = None


class ChatContext(BaseModel):
    """DTO for chat context with knowledge base integration."""
    query: str
    knowledge_results: List[KnowledgeSearchResult]
    conversation_history: List[Dict[str, Any]]
    user_id: UUID
    timestamp: datetime
    categories: List[str] = Field(default_factory=list)


class EnhancedChatRequestDTO(BaseModel):
    """Enhanced DTO for chat requests with KB integration."""
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[UUID] = None
    user_id: UUID
    use_knowledge_base: bool = Field(default=True)
    search_categories: Optional[List[str]] = None
    context_limit: int = Field(default=5, ge=1, le=10)
    model_name: Optional[str] = None
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=1000, ge=1, le=4000)
    metadata: Optional[Dict[str, Any]] = None
