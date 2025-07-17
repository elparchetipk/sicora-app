"""SQLAlchemy implementation of ConversationRepository."""

import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func, and_, or_
from sqlalchemy.orm import selectinload

from app.domain.entities.conversation import Conversation
from app.domain.value_objects.message import Message, MessageRole, MessageType
from app.domain.value_objects.conversation_metadata import ConversationMetadata
from app.domain.repositories.conversation_repository import ConversationRepository
from app.infrastructure.models.conversation_model import ConversationModel, MessageModel

logger = logging.getLogger(__name__)


class SQLAlchemyConversationRepository(ConversationRepository):
    """SQLAlchemy implementation of conversation repository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, conversation: Conversation) -> Conversation:
        """Create a new conversation."""
        try:
            # Create conversation model
            conversation_model = ConversationModel(
                id=conversation.conversation_id,
                user_id=conversation.user_id,
                title=conversation.title,
                message_count=conversation.get_messages_count(),
                total_tokens=conversation.get_total_tokens(),
                metadata=conversation.metadata.to_dict(),
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
                is_active=conversation.is_active
            )
            
            self.session.add(conversation_model)
            
            # Add messages if any
            for message in conversation.messages:
                message_model = MessageModel(
                    id=message.message_id,
                    conversation_id=conversation.conversation_id,
                    content=message.content,
                    role=message.role.value,
                    message_type=message.message_type.value,
                    tokens=message.tokens,
                    model_used=message.model_used,
                    processing_time=message.processing_time,
                    metadata=message.metadata,
                    created_at=message.timestamp,
                    updated_at=message.timestamp
                )
                self.session.add(message_model)
            
            await self.session.commit()
            await self.session.refresh(conversation_model)
            
            return await self._model_to_entity(conversation_model)
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating conversation: {str(e)}", exc_info=True)
            raise
    
    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get conversation by ID."""
        try:
            stmt = select(ConversationModel).options(
                selectinload(ConversationModel.messages)
            ).where(ConversationModel.id == conversation_id)
            
            result = await self.session.execute(stmt)
            conversation_model = result.scalar_one_or_none()
            
            if not conversation_model:
                return None
            
            return await self._model_to_entity(conversation_model)
            
        except Exception as e:
            logger.error(f"Error getting conversation by ID {conversation_id}: {str(e)}", exc_info=True)
            return None
    
    async def get_by_user_id(
        self, 
        user_id: UUID, 
        limit: int = 10, 
        offset: int = 0,
        include_archived: bool = False
    ) -> List[Conversation]:
        """Get conversations by user ID."""
        try:
            conditions = [ConversationModel.user_id == user_id]
            
            if not include_archived:
                conditions.append(ConversationModel.is_active == True)
            
            stmt = select(ConversationModel).options(
                selectinload(ConversationModel.messages)
            ).where(
                and_(*conditions)
            ).order_by(
                ConversationModel.updated_at.desc()
            ).limit(limit).offset(offset)
            
            result = await self.session.execute(stmt)
            conversation_models = result.scalars().all()
            
            conversations = []
            for model in conversation_models:
                entity = await self._model_to_entity(model)
                conversations.append(entity)
            
            return conversations
            
        except Exception as e:
            logger.error(f"Error getting conversations for user {user_id}: {str(e)}", exc_info=True)
            return []
    
    async def update(self, conversation: Conversation) -> Conversation:
        """Update an existing conversation."""
        try:
            # Update conversation
            stmt = update(ConversationModel).where(
                ConversationModel.id == conversation.conversation_id
            ).values(
                title=conversation.title,
                message_count=conversation.get_messages_count(),
                total_tokens=conversation.get_total_tokens(),
                metadata=conversation.metadata.to_dict(),
                updated_at=conversation.updated_at,
                is_active=conversation.is_active
            )
            
            await self.session.execute(stmt)
            
            # Get existing messages
            existing_messages_stmt = select(MessageModel).where(
                MessageModel.conversation_id == conversation.conversation_id
            )
            result = await self.session.execute(existing_messages_stmt)
            existing_models = result.scalars().all()
            existing_ids = {model.id for model in existing_models}
            
            # Add new messages
            conversation_message_ids = {msg.message_id for msg in conversation.messages}
            
            for message in conversation.messages:
                if message.message_id not in existing_ids:
                    message_model = MessageModel(
                        id=message.message_id,
                        conversation_id=conversation.conversation_id,
                        content=message.content,
                        role=message.role.value,
                        message_type=message.message_type.value,
                        tokens=message.tokens,
                        model_used=message.model_used,
                        processing_time=message.processing_time,
                        metadata=message.metadata,
                        created_at=message.timestamp,
                        updated_at=message.timestamp
                    )
                    self.session.add(message_model)
            
            await self.session.commit()
            
            # Return updated conversation
            return await self.get_by_id(conversation.conversation_id)
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating conversation: {str(e)}", exc_info=True)
            raise
    
    async def delete(self, conversation_id: UUID) -> bool:
        """Delete a conversation."""
        try:
            # Delete messages first (cascade should handle this, but being explicit)
            await self.session.execute(
                delete(MessageModel).where(MessageModel.conversation_id == conversation_id)
            )
            
            # Delete conversation
            result = await self.session.execute(
                delete(ConversationModel).where(ConversationModel.id == conversation_id)
            )
            
            await self.session.commit()
            
            return result.rowcount > 0
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deleting conversation {conversation_id}: {str(e)}", exc_info=True)
            return False
    
    async def get_active_conversations(
        self, 
        user_id: UUID,
        limit: int = 10
    ) -> List[Conversation]:
        """Get active conversations for a user."""
        return await self.get_by_user_id(
            user_id=user_id,
            limit=limit,
            include_archived=False
        )
    
    async def search_conversations(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10
    ) -> List[Conversation]:
        """Search conversations by content."""
        try:
            # Search in conversation titles and message content
            stmt = select(ConversationModel).options(
                selectinload(ConversationModel.messages)
            ).join(MessageModel).where(
                and_(
                    ConversationModel.user_id == user_id,
                    ConversationModel.is_active == True,
                    or_(
                        ConversationModel.title.ilike(f"%{query}%"),
                        MessageModel.content.ilike(f"%{query}%")
                    )
                )
            ).distinct().order_by(
                ConversationModel.updated_at.desc()
            ).limit(limit)
            
            result = await self.session.execute(stmt)
            conversation_models = result.scalars().all()
            
            conversations = []
            for model in conversation_models:
                entity = await self._model_to_entity(model)
                conversations.append(entity)
            
            return conversations
            
        except Exception as e:
            logger.error(f"Error searching conversations: {str(e)}", exc_info=True)
            return []
    
    async def get_conversation_count_by_user(self, user_id: UUID) -> int:
        """Get total conversation count for a user."""
        try:
            stmt = select(func.count(ConversationModel.id)).where(
                and_(
                    ConversationModel.user_id == user_id,
                    ConversationModel.is_active == True
                )
            )
            
            result = await self.session.execute(stmt)
            count = result.scalar()
            
            return count or 0
            
        except Exception as e:
            logger.error(f"Error getting conversation count: {str(e)}", exc_info=True)
            return 0
    
    async def archive_old_conversations(
        self, 
        user_id: UUID, 
        days_old: int = 30
    ) -> int:
        """Archive conversations older than specified days."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            stmt = update(ConversationModel).where(
                and_(
                    ConversationModel.user_id == user_id,
                    ConversationModel.updated_at < cutoff_date,
                    ConversationModel.is_active == True
                )
            ).values(
                is_active=False,
                updated_at=datetime.utcnow()
            )
            
            result = await self.session.execute(stmt)
            await self.session.commit()
            
            return result.rowcount
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error archiving old conversations: {str(e)}", exc_info=True)
            return 0
    
    async def _model_to_entity(self, model: ConversationModel) -> Conversation:
        """Convert SQLAlchemy model to domain entity."""
        try:
            # Convert messages
            messages = []
            for msg_model in model.messages:
                message = Message(
                    message_id=msg_model.id,
                    content=msg_model.content,
                    role=MessageRole(msg_model.role),
                    message_type=MessageType(msg_model.message_type),
                    tokens=msg_model.tokens,
                    metadata=msg_model.metadata or {},
                    timestamp=msg_model.created_at,
                    model_used=msg_model.model_used,
                    processing_time=msg_model.processing_time
                )
                messages.append(message)
            
            # Convert metadata
            metadata = ConversationMetadata(
                message_count=model.message_count,
                total_tokens=model.total_tokens,
                last_activity=model.updated_at,
                **model.metadata
            )
            
            # Create conversation entity
            conversation = Conversation(
                conversation_id=model.id,
                user_id=model.user_id,
                title=model.title,
                messages=messages,
                metadata=metadata,
                created_at=model.created_at,
                updated_at=model.updated_at,
                is_active=model.is_active
            )
            
            return conversation
            
        except Exception as e:
            logger.error(f"Error converting model to entity: {str(e)}", exc_info=True)
            raise
