"""Simple database models import for Alembic."""

import os
from sqlalchemy import Column, String, Text, JSON, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid

# Create a simple base for migrations
Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields."""
    __abstract__ = True
    
    # Use String for UUID compatibility with SQLite
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class ConversationModel(BaseModel):
    """SQLAlchemy model for conversations."""
    __tablename__ = "conversations"
    
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(200), nullable=False, default="Nueva Conversación")
    message_count = Column(Integer, default=0, nullable=False)
    total_tokens = Column(Integer, default=0, nullable=False)
    conversation_metadata = Column(JSON, default=dict, nullable=False)
    
    # Relationship to messages
    messages = relationship("MessageModel", back_populates="conversation", cascade="all, delete-orphan")


class MessageModel(BaseModel):
    """SQLAlchemy model for messages."""
    __tablename__ = "messages"
    
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    message_type = Column(String(20), default="text", nullable=False)  # text, image, file, code
    tokens = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    processing_time = Column(Float, nullable=True)
    message_metadata = Column(JSON, default=dict, nullable=False)
    
    # Relationship to conversation
    conversation = relationship("ConversationModel", back_populates="messages")


class KnowledgeEntryModel(BaseModel):
    """SQLAlchemy model for knowledge base entries."""
    __tablename__ = "knowledge_entries"
    
    title = Column(String(300), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), default="general", nullable=False, index=True)
    tags = Column(JSON, default=list, nullable=False)
    source = Column(String(500), nullable=True)
    embedding = Column(JSON, nullable=True)  # Store embedding as JSON list
    entry_metadata = Column(JSON, default=dict, nullable=False)
    relevance_score = Column(Float, nullable=True)


class AIModelModel(BaseModel):
    """SQLAlchemy model for AI model configurations."""
    __tablename__ = "ai_models"
    
    name = Column(String(100), nullable=False, unique=True, index=True)
    provider = Column(String(50), nullable=False, index=True)  # openai, anthropic, huggingface, etc.
    model_type = Column(String(50), nullable=False)  # chat, completion, embedding, etc.
    version = Column(String(50), nullable=True)
    
    # Model configuration
    context_window = Column(Integer, default=4096, nullable=False)
    max_tokens = Column(Integer, default=1000, nullable=False)
    temperature = Column(Float, default=0.7, nullable=False)
    top_p = Column(Float, default=1.0, nullable=False)
    frequency_penalty = Column(Float, default=0.0, nullable=False)
    presence_penalty = Column(Float, default=0.0, nullable=False)
    
    # Cost and performance
    input_cost_per_token = Column(Float, nullable=True)
    output_cost_per_token = Column(Float, nullable=True)
    requests_per_minute = Column(Integer, default=60, nullable=False)
    tokens_per_minute = Column(Integer, default=60000, nullable=False)
    
    # Status and metadata
    status = Column(String(20), default="active", nullable=False)  # active, inactive, maintenance, error
    supported_features = Column(JSON, default=list, nullable=False)  # chat, completion, embedding, etc.
    model_metadata = Column(JSON, default=dict, nullable=False)
