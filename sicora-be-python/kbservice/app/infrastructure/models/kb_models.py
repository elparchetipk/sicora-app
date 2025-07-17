"""SQLAlchemy models for Knowledge Base Service."""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from sqlalchemy import (
    String, Text, Integer, DateTime, Boolean, Float, 
    ForeignKey, JSON, Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.config.database import Base

# Import pgvector for PostgreSQL vector operations
try:
    from pgvector.sqlalchemy import Vector
    VECTOR_AVAILABLE = True
except ImportError:
    VECTOR_AVAILABLE = False


class KnowledgeItemModel(Base):
    """SQLAlchemy model for knowledge items."""
    
    __tablename__ = "knowledge_items"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Content fields
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_audience: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", index=True)
    
    # Metadata
    author_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Embedding vector - use pgvector for PostgreSQL, JSON for SQLite
    if VECTOR_AVAILABLE:
        embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(1536), nullable=True)
    else:
        embedding: Mapped[Optional[List[float]]] = mapped_column(JSON, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Statistics
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    helpful_count: Mapped[int] = mapped_column(Integer, default=0)
    unhelpful_count: Mapped[int] = mapped_column(Integer, default=0)
    version: Mapped[int] = mapped_column(Integer, default=1)
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_knowledge_items_content_gin", "content"),  # For full-text search
        Index("idx_knowledge_items_title_gin", "title"),     # For title search
        Index("idx_knowledge_items_category_status", "category", "status"),
        Index("idx_knowledge_items_target_audience_status", "target_audience", "status"),
        Index("idx_knowledge_items_created_at", "created_at"),
        Index("idx_knowledge_items_view_count", "view_count"),
        # Vector index will be added via migration for PostgreSQL
    )


class CategoryModel(Base):
    """SQLAlchemy model for categories."""
    
    __tablename__ = "categories"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Content fields
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Hierarchy
    parent_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    parent: Mapped[Optional["CategoryModel"]] = relationship("CategoryModel", remote_side=[id], back_populates="children")
    children: Mapped[List["CategoryModel"]] = relationship("CategoryModel", back_populates="parent")


class SearchQueryModel(Base):
    """SQLAlchemy model for search queries."""
    
    __tablename__ = "search_queries"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Query content
    query_text: Mapped[str] = mapped_column(String(1000), nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    user_role: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    
    # Filters and metadata
    filters: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    results_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Indexes
    __table_args__ = (
        Index("idx_search_queries_query_text_gin", "query_text"),
        Index("idx_search_queries_user_created", "user_id", "created_at"),
        Index("idx_search_queries_role_created", "user_role", "created_at"),
    )


class FeedbackModel(Base):
    """SQLAlchemy model for user feedback."""
    
    __tablename__ = "feedback"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Feedback content
    item_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_items.id"), nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    feedback_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # helpful, unhelpful
    comment: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("item_id", "user_id", name="uq_feedback_item_user"),
        Index("idx_feedback_item_type", "item_id", "feedback_type"),
    )


class KnowledgeItemVersionModel(Base):
    """SQLAlchemy model for knowledge item versions."""
    
    __tablename__ = "knowledge_item_versions"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Version tracking
    item_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_items.id"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Content snapshot
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Change metadata
    changed_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    change_comment: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("item_id", "version_number", name="uq_version_item_number"),
        Index("idx_versions_item_version", "item_id", "version_number"),
    )


class QueryAnalyticsModel(Base):
    """SQLAlchemy model for query analytics."""
    
    __tablename__ = "query_analytics"
    
    # Primary key  
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Analytics data
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    query_count: Mapped[int] = mapped_column(Integer, default=0)
    unique_users: Mapped[int] = mapped_column(Integer, default=0)
    avg_response_time: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Popular queries
    top_queries: Mapped[Optional[List[dict]]] = mapped_column(JSON, nullable=True)
    
    # By user role
    student_queries: Mapped[int] = mapped_column(Integer, default=0)
    instructor_queries: Mapped[int] = mapped_column(Integer, default=0)
    admin_queries: Mapped[int] = mapped_column(Integer, default=0)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("date", name="uq_analytics_date"),
    )
