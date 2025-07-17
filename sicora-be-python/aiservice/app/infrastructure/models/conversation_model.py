"""Conversation SQLAlchemy model."""

from sqlalchemy import Column, String, Text, JSON, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .base_model import BaseModel


class ConversationModel(BaseModel):
    """SQLAlchemy model for conversations."""
    __tablename__ = "conversations"
    
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    title = Column(String(200), nullable=False, default="Nueva Conversación")
    message_count = Column(Integer, default=0, nullable=False)
    total_tokens = Column(Integer, default=0, nullable=False)
    conversation_metadata = Column(JSON, default=dict, nullable=False)
    
    # Relationship to messages
    messages = relationship("MessageModel", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, title='{self.title}', messages={self.message_count})>"


class MessageModel(BaseModel):
    """SQLAlchemy model for messages."""
    __tablename__ = "messages"
    
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    message_type = Column(String(20), default="text", nullable=False)  # text, image, file, code
    tokens = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    processing_time = Column(Float, nullable=True)
    message_metadata = Column(JSON, default=dict, nullable=False)
    
    # Relationship to conversation
    conversation = relationship("ConversationModel", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', content_preview='{self.content[:50]}...')>"
