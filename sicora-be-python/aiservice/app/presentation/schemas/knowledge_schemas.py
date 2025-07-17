"""Pydantic schemas for knowledge base endpoints."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class KnowledgeEntryCreate(BaseModel):
    """Schema for creating a new knowledge entry."""
    title: str = Field(..., min_length=1, max_length=500, description="Knowledge entry title")
    content: str = Field(..., min_length=1, max_length=100000, description="Knowledge entry content")
    category: str = Field(..., min_length=1, max_length=100, description="Knowledge category")
    tags: Optional[List[str]] = Field(default=[], description="Knowledge entry tags")
    source: Optional[str] = Field(default=None, max_length=500, description="Source of the knowledge")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Proceso de Desarrollo de Software",
                "content": "El proceso de desarrollo de software incluye las siguientes fases: análisis, diseño, implementación, pruebas y mantenimiento...",
                "category": "desarrollo",
                "tags": ["desarrollo", "proceso", "metodologia"],
                "source": "Manual interno de desarrollo",
                "metadata": {"author": "equipo_desarrollo", "version": "1.0"}
            }
        }
    )


class KnowledgeEntryUpdate(BaseModel):
    """Schema for updating a knowledge entry."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500, description="New title")
    content: Optional[str] = Field(default=None, min_length=1, max_length=100000, description="New content")
    category: Optional[str] = Field(default=None, min_length=1, max_length=100, description="New category")
    tags: Optional[List[str]] = Field(default=None, description="New tags")
    source: Optional[str] = Field(default=None, max_length=500, description="New source")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="New metadata")


class KnowledgeEntryResponse(BaseModel):
    """Schema for knowledge entry response."""
    id: UUID = Field(..., description="Knowledge entry unique identifier")
    title: str = Field(..., description="Knowledge entry title")
    content: str = Field(..., description="Knowledge entry content")
    category: str = Field(..., description="Knowledge category")
    tags: List[str] = Field(default=[], description="Knowledge entry tags")
    source: Optional[str] = Field(default=None, description="Source of the knowledge")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class KnowledgeSearchRequest(BaseModel):
    """Schema for knowledge search request."""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    category: Optional[str] = Field(default=None, description="Filter by category")
    tags: Optional[List[str]] = Field(default=None, description="Filter by tags")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of results")
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum similarity score")
    include_content: bool = Field(default=True, description="Whether to include full content in results")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "proceso de desarrollo ágil",
                "category": "desarrollo",
                "tags": ["metodologia", "agil"],
                "limit": 10,
                "similarity_threshold": 0.7
            }
        }
    )


class KnowledgeSearchResult(BaseModel):
    """Schema for a single knowledge search result."""
    entry: KnowledgeEntryResponse = Field(..., description="Knowledge entry")
    similarity_score: float = Field(..., description="Similarity score (0.0 to 1.0)")
    highlighted_content: Optional[str] = Field(default=None, description="Content with highlighted matches")


class KnowledgeSearchResponse(BaseModel):
    """Schema for knowledge search response."""
    results: List[KnowledgeSearchResult] = Field(..., description="Search results")
    total_found: int = Field(..., description="Total number of matches found")
    query: str = Field(..., description="Original search query")
    search_time_ms: float = Field(..., description="Search execution time in milliseconds")


class KnowledgeListQuery(BaseModel):
    """Schema for knowledge list query parameters."""
    category: Optional[str] = Field(default=None, description="Filter by category")
    tags: Optional[List[str]] = Field(default=None, description="Filter by tags")
    source: Optional[str] = Field(default=None, description="Filter by source")
    search: Optional[str] = Field(default=None, description="Text search in title and content")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of entries to return")
    offset: int = Field(default=0, ge=0, description="Number of entries to skip")
    order_by: str = Field(default="updated_at", description="Field to order by")
    order_desc: bool = Field(default=True, description="Whether to order in descending order")


class KnowledgeListResponse(BaseModel):
    """Schema for knowledge list response."""
    entries: List[KnowledgeEntryResponse] = Field(..., description="List of knowledge entries")
    total: int = Field(..., description="Total number of entries")
    limit: int = Field(..., description="Limit used for pagination")
    offset: int = Field(..., description="Offset used for pagination")
    has_more: bool = Field(..., description="Whether there are more entries available")


class KnowledgeBulkCreate(BaseModel):
    """Schema for bulk creating knowledge entries."""
    entries: List[KnowledgeEntryCreate] = Field(..., min_length=1, max_length=100, description="Knowledge entries to create")
    skip_duplicates: bool = Field(default=True, description="Whether to skip duplicate entries")
    update_existing: bool = Field(default=False, description="Whether to update existing entries with same title")


class KnowledgeBulkCreateResponse(BaseModel):
    """Schema for bulk create response."""
    created_count: int = Field(..., description="Number of entries created")
    updated_count: int = Field(..., description="Number of entries updated")
    skipped_count: int = Field(..., description="Number of entries skipped")
    errors: List[str] = Field(default=[], description="List of error messages")
    created_ids: List[UUID] = Field(default=[], description="IDs of created entries")


class KnowledgeStats(BaseModel):
    """Schema for knowledge base statistics."""
    total_entries: int = Field(..., description="Total number of knowledge entries")
    categories: Dict[str, int] = Field(..., description="Number of entries per category")
    top_tags: List[Dict[str, Any]] = Field(..., description="Most used tags with counts")
    sources: Dict[str, int] = Field(..., description="Number of entries per source")
    entries_today: int = Field(..., description="Entries created today")
    entries_this_week: int = Field(..., description="Entries created this week")
    entries_this_month: int = Field(..., description="Entries created this month")
    avg_content_length: float = Field(..., description="Average content length in characters")


class KnowledgeEmbeddingRequest(BaseModel):
    """Schema for generating embeddings for knowledge entries."""
    entry_ids: Optional[List[UUID]] = Field(default=None, description="Specific entry IDs to process")
    category: Optional[str] = Field(default=None, description="Process entries from specific category")
    force_regenerate: bool = Field(default=False, description="Whether to regenerate existing embeddings")
    batch_size: int = Field(default=10, ge=1, le=50, description="Batch size for processing")


class KnowledgeEmbeddingResponse(BaseModel):
    """Schema for embedding generation response."""
    processed_count: int = Field(..., description="Number of entries processed")
    success_count: int = Field(..., description="Number of successful embeddings generated")
    error_count: int = Field(..., description="Number of failed embeddings")
    errors: List[str] = Field(default=[], description="List of error messages")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")


class KnowledgeAnalysisRequest(BaseModel):
    """Schema for knowledge analysis request."""
    entry_id: UUID = Field(..., description="Knowledge entry ID to analyze")
    analysis_types: List[str] = Field(..., description="Types of analysis to perform")
    model_id: Optional[UUID] = Field(default=None, description="AI model to use for analysis")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "entry_id": "123e4567-e89b-12d3-a456-426614174000",
                "analysis_types": ["sentiment", "keywords", "summary", "classification"],
                "model_id": "456e7890-e89b-12d3-a456-426614174001"
            }
        }
    )


class KnowledgeAnalysisResponse(BaseModel):
    """Schema for knowledge analysis response."""
    entry_id: UUID = Field(..., description="Knowledge entry ID")
    analysis_results: Dict[str, Any] = Field(..., description="Analysis results by type")
    model_used: Optional[str] = Field(default=None, description="AI model used for analysis")
    analysis_time_ms: float = Field(..., description="Analysis execution time in milliseconds")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "entry_id": "123e4567-e89b-12d3-a456-426614174000",
                "analysis_results": {
                    "sentiment": {"sentiment": "positive", "confidence": 0.85},
                    "keywords": ["desarrollo", "software", "metodología"],
                    "summary": "Resumen del proceso de desarrollo...",
                    "classification": {"tecnico": 0.9, "proceso": 0.8}
                },
                "analysis_time_ms": 1250.5
            }
        }
    )
