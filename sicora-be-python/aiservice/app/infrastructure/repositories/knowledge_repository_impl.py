"""SQLAlchemy implementation of KnowledgeRepository."""

import logging
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func, and_, or_
from sqlalchemy.dialects.postgresql import insert

from app.domain.entities.knowledge_entry import KnowledgeEntry
from app.domain.repositories.knowledge_repository import KnowledgeRepository
from app.infrastructure.models.knowledge_model import KnowledgeEntryModel

logger = logging.getLogger(__name__)


class SQLAlchemyKnowledgeRepository(KnowledgeRepository):
    """SQLAlchemy implementation of knowledge repository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, entry: KnowledgeEntry) -> KnowledgeEntry:
        """Create a new knowledge entry."""
        try:
            knowledge_model = KnowledgeEntryModel(
                id=entry.entry_id,
                title=entry.title,
                content=entry.content,
                category=entry.category,
                tags=entry.tags,
                source=entry.source,
                embedding=entry.embedding,
                metadata=entry.metadata,
                relevance_score=entry.relevance_score,
                created_at=entry.created_at,
                updated_at=entry.updated_at,
                is_active=entry.is_active
            )
            
            self.session.add(knowledge_model)
            await self.session.commit()
            await self.session.refresh(knowledge_model)
            
            return self._model_to_entity(knowledge_model)
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating knowledge entry: {str(e)}", exc_info=True)
            raise
    
    async def get_by_id(self, entry_id: UUID) -> Optional[KnowledgeEntry]:
        """Get knowledge entry by ID."""
        try:
            stmt = select(KnowledgeEntryModel).where(
                and_(
                    KnowledgeEntryModel.id == entry_id,
                    KnowledgeEntryModel.is_active == True
                )
            )
            
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if not model:
                return None
            
            return self._model_to_entity(model)
            
        except Exception as e:
            logger.error(f"Error getting knowledge entry by ID {entry_id}: {str(e)}", exc_info=True)
            return None
    
    async def get_by_category(
        self, 
        category: str, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[KnowledgeEntry]:
        """Get knowledge entries by category."""
        try:
            conditions = [KnowledgeEntryModel.is_active == True]
            
            if category:
                conditions.append(KnowledgeEntryModel.category == category)
            
            stmt = select(KnowledgeEntryModel).where(
                and_(*conditions)
            ).order_by(
                KnowledgeEntryModel.updated_at.desc()
            ).limit(limit).offset(offset)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            return [self._model_to_entity(model) for model in models]
            
        except Exception as e:
            logger.error(f"Error getting knowledge entries by category: {str(e)}", exc_info=True)
            return []
    
    async def search_by_text(
        self, 
        query: str, 
        limit: int = 10,
        category: Optional[str] = None
    ) -> List[KnowledgeEntry]:
        """Search knowledge entries by text."""
        try:
            conditions = [
                KnowledgeEntryModel.is_active == True,
                or_(
                    KnowledgeEntryModel.title.ilike(f"%{query}%"),
                    KnowledgeEntryModel.content.ilike(f"%{query}%")
                )
            ]
            
            if category:
                conditions.append(KnowledgeEntryModel.category == category)
            
            stmt = select(KnowledgeEntryModel).where(
                and_(*conditions)
            ).order_by(
                KnowledgeEntryModel.updated_at.desc()
            ).limit(limit)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            return [self._model_to_entity(model) for model in models]
            
        except Exception as e:
            logger.error(f"Error searching knowledge entries by text: {str(e)}", exc_info=True)
            return []
    
    async def search_by_embedding(
        self, 
        embedding: List[float], 
        limit: int = 10,
        similarity_threshold: float = 0.7,
        category: Optional[str] = None
    ) -> List[KnowledgeEntry]:
        """Search knowledge entries by embedding similarity."""
        try:
            # Note: This is a simplified implementation
            # In production, you'd want to use vector similarity functions
            # or integrate with a proper vector database
            
            conditions = [
                KnowledgeEntryModel.is_active == True,
                KnowledgeEntryModel.embedding.is_not(None)
            ]
            
            if category:
                conditions.append(KnowledgeEntryModel.category == category)
            
            stmt = select(KnowledgeEntryModel).where(
                and_(*conditions)
            ).limit(limit * 2)  # Get more to filter by similarity
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            # Calculate similarity and filter
            similar_entries = []
            for model in models:
                if model.embedding:
                    similarity = self._calculate_cosine_similarity(embedding, model.embedding)
                    if similarity >= similarity_threshold:
                        entry = self._model_to_entity(model)
                        entry.set_relevance_score(similarity)
                        similar_entries.append(entry)
            
            # Sort by similarity and limit
            similar_entries.sort(key=lambda x: x.relevance_score or 0, reverse=True)
            return similar_entries[:limit]
            
        except Exception as e:
            logger.error(f"Error searching knowledge entries by embedding: {str(e)}", exc_info=True)
            return []
    
    async def update(self, entry: KnowledgeEntry) -> KnowledgeEntry:
        """Update an existing knowledge entry."""
        try:
            stmt = update(KnowledgeEntryModel).where(
                KnowledgeEntryModel.id == entry.entry_id
            ).values(
                title=entry.title,
                content=entry.content,
                category=entry.category,
                tags=entry.tags,
                source=entry.source,
                embedding=entry.embedding,
                metadata=entry.metadata,
                relevance_score=entry.relevance_score,
                updated_at=entry.updated_at,
                is_active=entry.is_active
            )
            
            await self.session.execute(stmt)
            await self.session.commit()
            
            # Return updated entry
            return await self.get_by_id(entry.entry_id)
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating knowledge entry: {str(e)}", exc_info=True)
            raise
    
    async def delete(self, entry_id: UUID) -> bool:
        """Delete a knowledge entry."""
        try:
            # Soft delete by setting is_active to False
            stmt = update(KnowledgeEntryModel).where(
                KnowledgeEntryModel.id == entry_id
            ).values(
                is_active=False,
                updated_at=func.now()
            )
            
            result = await self.session.execute(stmt)
            await self.session.commit()
            
            return result.rowcount > 0
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deleting knowledge entry {entry_id}: {str(e)}", exc_info=True)
            return False
    
    async def get_by_tags(
        self, 
        tags: List[str], 
        limit: int = 50
    ) -> List[KnowledgeEntry]:
        """Get knowledge entries by tags."""
        try:
            # For PostgreSQL, you could use array operations
            # For SQLite, we'll use a workaround with JSON operations
            conditions = [KnowledgeEntryModel.is_active == True]
            
            # Simple approach: search for tags in the JSON array
            tag_conditions = []
            for tag in tags:
                # This is a simplified approach - in production you'd want better JSON querying
                tag_conditions.append(
                    func.json_extract(KnowledgeEntryModel.tags, '$').like(f'%"{tag}"%')
                )
            
            if tag_conditions:
                conditions.append(or_(*tag_conditions))
            
            stmt = select(KnowledgeEntryModel).where(
                and_(*conditions)
            ).order_by(
                KnowledgeEntryModel.updated_at.desc()
            ).limit(limit)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            return [self._model_to_entity(model) for model in models]
            
        except Exception as e:
            logger.error(f"Error getting knowledge entries by tags: {str(e)}", exc_info=True)
            return []
    
    async def get_all_categories(self) -> List[str]:
        """Get all available categories."""
        try:
            stmt = select(KnowledgeEntryModel.category).distinct().where(
                KnowledgeEntryModel.is_active == True
            )
            
            result = await self.session.execute(stmt)
            categories = result.scalars().all()
            
            return [cat for cat in categories if cat]
            
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}", exc_info=True)
            return []
    
    async def get_all_tags(self) -> List[str]:
        """Get all available tags."""
        try:
            stmt = select(KnowledgeEntryModel.tags).where(
                and_(
                    KnowledgeEntryModel.is_active == True,
                    KnowledgeEntryModel.tags.is_not(None)
                )
            )
            
            result = await self.session.execute(stmt)
            tag_lists = result.scalars().all()
            
            # Flatten and deduplicate tags
            all_tags = set()
            for tag_list in tag_lists:
                if tag_list:
                    all_tags.update(tag_list)
            
            return sorted(list(all_tags))
            
        except Exception as e:
            logger.error(f"Error getting tags: {str(e)}", exc_info=True)
            return []
    
    async def get_entries_without_embeddings(self, limit: int = 100) -> List[KnowledgeEntry]:
        """Get entries that don't have embeddings yet."""
        try:
            stmt = select(KnowledgeEntryModel).where(
                and_(
                    KnowledgeEntryModel.is_active == True,
                    or_(
                        KnowledgeEntryModel.embedding.is_(None),
                        func.json_array_length(KnowledgeEntryModel.embedding) == 0
                    )
                )
            ).order_by(
                KnowledgeEntryModel.created_at.asc()
            ).limit(limit)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            return [self._model_to_entity(model) for model in models]
            
        except Exception as e:
            logger.error(f"Error getting entries without embeddings: {str(e)}", exc_info=True)
            return []
    
    async def bulk_update_embeddings(
        self, 
        updates: List[Dict[str, Any]]
    ) -> int:
        """Bulk update embeddings for multiple entries."""
        try:
            updated_count = 0
            
            for update_data in updates:
                entry_id = update_data.get("entry_id")
                embedding = update_data.get("embedding")
                
                if not entry_id or not embedding:
                    continue
                
                stmt = update(KnowledgeEntryModel).where(
                    KnowledgeEntryModel.id == entry_id
                ).values(
                    embedding=embedding,
                    updated_at=func.now()
                )
                
                result = await self.session.execute(stmt)
                if result.rowcount > 0:
                    updated_count += 1
            
            await self.session.commit()
            return updated_count
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error bulk updating embeddings: {str(e)}", exc_info=True)
            return 0
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        try:
            # Total entries
            total_stmt = select(func.count(KnowledgeEntryModel.id)).where(
                KnowledgeEntryModel.is_active == True
            )
            total_result = await self.session.execute(total_stmt)
            total_entries = total_result.scalar() or 0
            
            # Entries with embeddings
            embedded_stmt = select(func.count(KnowledgeEntryModel.id)).where(
                and_(
                    KnowledgeEntryModel.is_active == True,
                    KnowledgeEntryModel.embedding.is_not(None)
                )
            )
            embedded_result = await self.session.execute(embedded_stmt)
            embedded_entries = embedded_result.scalar() or 0
            
            # Categories count
            categories_stmt = select(func.count(func.distinct(KnowledgeEntryModel.category))).where(
                KnowledgeEntryModel.is_active == True
            )
            categories_result = await self.session.execute(categories_stmt)
            categories_count = categories_result.scalar() or 0
            
            return {
                "total_entries": total_entries,
                "embedded_entries": embedded_entries,
                "categories_count": categories_count,
                "embedding_coverage": (embedded_entries / max(total_entries, 1)) * 100
            }
            
        except Exception as e:
            logger.error(f"Error getting knowledge statistics: {str(e)}", exc_info=True)
            return {}
    
    def _model_to_entity(self, model: KnowledgeEntryModel) -> KnowledgeEntry:
        """Convert SQLAlchemy model to domain entity."""
        return KnowledgeEntry(
            entry_id=model.id,
            title=model.title,
            content=model.content,
            category=model.category,
            tags=model.tags or [],
            embedding=model.embedding,
            metadata=model.metadata or {},
            source=model.source,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
            relevance_score=model.relevance_score
        )
    
    def _calculate_cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        try:
            import math
            
            if len(embedding1) != len(embedding2):
                return 0.0
            
            dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
            magnitude1 = math.sqrt(sum(a * a for a in embedding1))
            magnitude2 = math.sqrt(sum(a * a for a in embedding2))
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
            
        except Exception:
            return 0.0
