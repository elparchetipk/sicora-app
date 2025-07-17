"""Knowledge base use cases for AI Service."""

import logging
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.domain.entities.knowledge_entry import KnowledgeEntry
from app.domain.repositories.knowledge_repository import KnowledgeRepository
from app.domain.exceptions.ai_exceptions import (
    KnowledgeBaseError,
    EmbeddingError
)
from app.application.interfaces.ai_provider_interface import AIProviderInterface
from app.application.interfaces.vector_store_interface import VectorStoreInterface
from app.application.interfaces.cache_interface import CacheInterface
from app.application.dtos.ai_dtos import (
    KnowledgeEntryCreateDTO,
    KnowledgeEntryUpdateDTO,
    KnowledgeEntryResponseDTO,
    KnowledgeSearchDTO
)

logger = logging.getLogger(__name__)


class KnowledgeManagementUseCase:
    """Use case for knowledge base management."""
    
    def __init__(
        self,
        knowledge_repo: KnowledgeRepository,
        ai_provider: AIProviderInterface,
        vector_store: VectorStoreInterface,
        cache: CacheInterface
    ):
        self.knowledge_repo = knowledge_repo
        self.ai_provider = ai_provider
        self.vector_store = vector_store
        self.cache = cache
    
    async def create_knowledge_entry(self, request: KnowledgeEntryCreateDTO) -> KnowledgeEntryResponseDTO:
        """Create a new knowledge entry."""
        try:
            # Create knowledge entry
            entry = KnowledgeEntry(
                title=request.title,
                content=request.content,
                category=request.category,
                tags=request.tags or [],
                source=request.source,
                metadata=request.metadata or {}
            )
            
            # Save to repository
            saved_entry = await self.knowledge_repo.create(entry)
            
            # Generate and save embedding asynchronously
            await self._generate_and_save_embedding(saved_entry)
            
            return self._to_response_dto(saved_entry)
            
        except Exception as e:
            logger.error(f"Error creating knowledge entry: {str(e)}", exc_info=True)
            raise KnowledgeBaseError(f"Failed to create knowledge entry: {str(e)}")
    
    async def update_knowledge_entry(
        self, 
        entry_id: UUID, 
        request: KnowledgeEntryUpdateDTO
    ) -> KnowledgeEntryResponseDTO:
        """Update an existing knowledge entry."""
        try:
            entry = await self.knowledge_repo.get_by_id(entry_id)
            if not entry:
                raise KnowledgeBaseError(f"Knowledge entry {entry_id} not found")
            
            # Update fields
            if request.title is not None:
                entry.title = request.title
            if request.content is not None:
                entry.update_content(request.content)
            if request.category is not None:
                entry.category = request.category
            if request.tags is not None:
                entry.tags = request.tags
            if request.source is not None:
                entry.source = request.source
            if request.metadata is not None:
                entry.metadata = request.metadata
            if request.is_active is not None:
                entry.is_active = request.is_active
            
            # Save changes
            updated_entry = await self.knowledge_repo.update(entry)
            
            # Regenerate embedding if content changed
            if request.content is not None:
                await self._generate_and_save_embedding(updated_entry)
            
            return self._to_response_dto(updated_entry)
            
        except Exception as e:
            logger.error(f"Error updating knowledge entry: {str(e)}", exc_info=True)
            raise KnowledgeBaseError(f"Failed to update knowledge entry: {str(e)}")
    
    async def get_knowledge_entry(self, entry_id: UUID) -> KnowledgeEntryResponseDTO:
        """Get a knowledge entry by ID."""
        entry = await self.knowledge_repo.get_by_id(entry_id)
        if not entry:
            raise KnowledgeBaseError(f"Knowledge entry {entry_id} not found")
        
        return self._to_response_dto(entry)
    
    async def search_knowledge(self, request: KnowledgeSearchDTO) -> List[KnowledgeEntryResponseDTO]:
        """Search knowledge base."""
        try:
            results = []
            
            if request.use_semantic_search:
                # Generate embedding for semantic search
                query_embedding = await self.ai_provider.generate_embedding(request.query)
                
                # Search using vector similarity
                similar_entries = await self.vector_store.search_similar(
                    query_embedding=query_embedding,
                    limit=request.limit,
                    similarity_threshold=request.similarity_threshold,
                    filters={
                        "category": request.category,
                        "tags": request.tags
                    }
                )
                
                results = [
                    self._to_response_dto(entry, relevance_score=score)
                    for entry, score in similar_entries
                ]
            else:
                # Use text-based search
                entries = await self.knowledge_repo.search_by_text(
                    query=request.query,
                    limit=request.limit,
                    category=request.category
                )
                
                results = [self._to_response_dto(entry) for entry in entries]
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}", exc_info=True)
            raise KnowledgeBaseError(f"Failed to search knowledge base: {str(e)}")
    
    async def list_knowledge_entries(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[KnowledgeEntryResponseDTO]:
        """List knowledge entries with filters."""
        try:
            if category:
                entries = await self.knowledge_repo.get_by_category(
                    category=category,
                    limit=limit,
                    offset=offset
                )
            elif tags:
                entries = await self.knowledge_repo.get_by_tags(
                    tags=tags,
                    limit=limit
                )
            else:
                entries = await self.knowledge_repo.get_by_category(
                    category="",  # Get all
                    limit=limit,
                    offset=offset
                )
            
            return [self._to_response_dto(entry) for entry in entries]
            
        except Exception as e:
            logger.error(f"Error listing knowledge entries: {str(e)}", exc_info=True)
            raise KnowledgeBaseError(f"Failed to list knowledge entries: {str(e)}")
    
    async def delete_knowledge_entry(self, entry_id: UUID) -> bool:
        """Delete a knowledge entry."""
        try:
            # Remove from vector store
            await self.vector_store.delete_document(str(entry_id))
            
            # Remove from repository
            success = await self.knowledge_repo.delete(entry_id)
            
            # Clear cache
            await self.cache.delete(f"knowledge_entry:{entry_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting knowledge entry: {str(e)}", exc_info=True)
            raise KnowledgeBaseError(f"Failed to delete knowledge entry: {str(e)}")
    
    async def get_categories(self) -> List[str]:
        """Get all available categories."""
        return await self.knowledge_repo.get_all_categories()
    
    async def get_tags(self) -> List[str]:
        """Get all available tags."""
        return await self.knowledge_repo.get_all_tags()
    
    async def get_knowledge_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        try:
            repo_stats = await self.knowledge_repo.get_statistics()
            vector_stats = await self.vector_store.get_collection_stats()
            
            return {
                **repo_stats,
                "vector_store": vector_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting knowledge statistics: {str(e)}", exc_info=True)
            return {}
    
    async def bulk_generate_embeddings(self, batch_size: int = 10) -> int:
        """Generate embeddings for entries that don't have them."""
        try:
            entries = await self.knowledge_repo.get_entries_without_embeddings(
                limit=batch_size
            )
            
            processed = 0
            for entry in entries:
                try:
                    await self._generate_and_save_embedding(entry)
                    processed += 1
                except Exception as e:
                    logger.warning(f"Failed to generate embedding for entry {entry.entry_id}: {str(e)}")
            
            return processed
            
        except Exception as e:
            logger.error(f"Error in bulk embedding generation: {str(e)}", exc_info=True)
            raise EmbeddingError(f"Failed to generate embeddings: {str(e)}")
    
    async def _generate_and_save_embedding(self, entry: KnowledgeEntry) -> None:
        """Generate and save embedding for a knowledge entry."""
        try:
            # Generate embedding
            embedding_text = f"{entry.title}\n{entry.content}"
            embedding = await self.ai_provider.generate_embedding(embedding_text)
            
            # Update entry with embedding
            entry.update_embedding(embedding)
            await self.knowledge_repo.update(entry)
            
            # Add to vector store
            await self.vector_store.add_document(entry, embedding)
            
        except Exception as e:
            logger.error(f"Error generating embedding for entry {entry.entry_id}: {str(e)}")
            raise EmbeddingError(f"Failed to generate embedding: {str(e)}")
    
    def _to_response_dto(
        self, 
        entry: KnowledgeEntry, 
        relevance_score: Optional[float] = None
    ) -> KnowledgeEntryResponseDTO:
        """Convert knowledge entry to response DTO."""
        return KnowledgeEntryResponseDTO(
            entry_id=entry.entry_id,
            title=entry.title,
            content=entry.content,
            category=entry.category,
            tags=entry.tags,
            source=entry.source,
            metadata=entry.metadata,
            created_at=entry.created_at,
            updated_at=entry.updated_at,
            is_active=entry.is_active,
            relevance_score=relevance_score or entry.relevance_score,
            has_embedding=entry.has_embedding()
        )
