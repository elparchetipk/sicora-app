"""Conversation repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.conversation import Conversation


class ConversationRepository(ABC):
    """Abstract repository for conversation management."""
    
    @abstractmethod
    async def create(self, conversation: Conversation) -> Conversation:
        """Create a new conversation."""
        pass
    
    @abstractmethod
    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get conversation by ID."""
        pass
    
    @abstractmethod
    async def get_by_user_id(
        self, 
        user_id: UUID, 
        limit: int = 10, 
        offset: int = 0,
        include_archived: bool = False
    ) -> List[Conversation]:
        """Get conversations by user ID."""
        pass
    
    @abstractmethod
    async def update(self, conversation: Conversation) -> Conversation:
        """Update an existing conversation."""
        pass
    
    @abstractmethod
    async def delete(self, conversation_id: UUID) -> bool:
        """Delete a conversation."""
        pass
    
    @abstractmethod
    async def get_active_conversations(
        self, 
        user_id: UUID,
        limit: int = 10
    ) -> List[Conversation]:
        """Get active conversations for a user."""
        pass
    
    @abstractmethod
    async def search_conversations(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10
    ) -> List[Conversation]:
        """Search conversations by content."""
        pass
    
    @abstractmethod
    async def get_conversation_count_by_user(self, user_id: UUID) -> int:
        """Get total conversation count for a user."""
        pass
    
    @abstractmethod
    async def archive_old_conversations(
        self, 
        user_id: UUID, 
        days_old: int = 30
    ) -> int:
        """Archive conversations older than specified days."""
        pass
