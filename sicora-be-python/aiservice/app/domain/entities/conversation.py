"""Conversation entity for AI Service."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
import uuid

from app.domain.value_objects.message import Message
from app.domain.value_objects.conversation_metadata import ConversationMetadata


class Conversation:
    """Conversation domain entity representing a chat session."""
    
    def __init__(
        self,
        conversation_id: Optional[UUID] = None,
        user_id: UUID = None,
        title: str = "Nueva Conversación",
        messages: Optional[List[Message]] = None,
        metadata: Optional[ConversationMetadata] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_active: bool = True
    ):
        self.conversation_id = conversation_id or uuid.uuid4()
        self.user_id = user_id
        self.title = title
        self.messages = messages or []
        self.metadata = metadata or ConversationMetadata()
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_active = is_active
    
    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
        self.metadata.increment_message_count()
    
    def get_messages_count(self) -> int:
        """Get the total number of messages in the conversation."""
        return len(self.messages)
    
    def get_last_message(self) -> Optional[Message]:
        """Get the last message in the conversation."""
        return self.messages[-1] if self.messages else None
    
    def get_messages_by_role(self, role: str) -> List[Message]:
        """Get all messages by role (user, assistant, system)."""
        return [msg for msg in self.messages if msg.role == role]
    
    def get_context_window(self, max_messages: int = 10) -> List[Message]:
        """Get the last N messages for context window."""
        return self.messages[-max_messages:] if self.messages else []
    
    def archive(self) -> None:
        """Archive the conversation."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def update_title(self, new_title: str) -> None:
        """Update conversation title."""
        self.title = new_title
        self.updated_at = datetime.utcnow()
    
    def get_total_tokens(self) -> int:
        """Get total tokens used in the conversation."""
        return sum(msg.tokens for msg in self.messages if msg.tokens)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert conversation to dictionary."""
        return {
            "conversation_id": str(self.conversation_id),
            "user_id": str(self.user_id),
            "title": self.title,
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": self.metadata.to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "message_count": self.get_messages_count(),
            "total_tokens": self.get_total_tokens()
        }
    
    def __str__(self) -> str:
        return f"Conversation(id={self.conversation_id}, title='{self.title}', messages={len(self.messages)})"
    
    def __repr__(self) -> str:
        return self.__str__()
