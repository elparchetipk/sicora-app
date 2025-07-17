"""ChromaDB adapter implementation for vector store operations."""

import uuid
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings

from app.application.interfaces.vector_store_interface import VectorStoreInterface
from app.domain.entities.knowledge_entry import KnowledgeEntry
from app.domain.exceptions.ai_exceptions import VectorStoreError


class ChromaDBAdapter(VectorStoreInterface):
    """ChromaDB vector store adapter implementation."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        collection_name: str = "knowledge_base",
        persist_directory: Optional[str] = None
    ):
        """Initialize ChromaDB adapter."""
        try:
            if persist_directory:
                # Persistent client
                self.client = chromadb.PersistentClient(
                    path=persist_directory,
                    settings=Settings(anonymized_telemetry=False)
                )
            else:
                # HTTP client for remote ChromaDB
                self.client = chromadb.HttpClient(
                    host=host,
                    port=port,
                    settings=Settings(anonymized_telemetry=False)
                )
            
            self.collection_name = collection_name
            self._collection = None
            
        except Exception as e:
            raise VectorStoreError(f"Failed to initialize ChromaDB: {str(e)}")
    
    async def _get_collection(self):
        """Get or create the collection."""
        if self._collection is None:
            try:
                self._collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"description": "AI Service Knowledge Base"}
                )
            except Exception as e:
                raise VectorStoreError(f"Failed to get collection: {str(e)}")
        return self._collection
    
    async def add_document(
        self,
        entry: KnowledgeEntry,
        embedding: List[float]
    ) -> str:
        """Add a document with its embedding to ChromaDB."""
        try:
            collection = await self._get_collection()
            
            document_id = str(entry.id)
            metadata = {
                "title": entry.title,
                "category": entry.category,
                "tags": ",".join(entry.tags) if entry.tags else "",
                "source": entry.source or "",
                "created_at": entry.created_at.isoformat() if entry.created_at else "",
                "updated_at": entry.updated_at.isoformat() if entry.updated_at else ""
            }
            
            collection.add(
                ids=[document_id],
                embeddings=[embedding],
                documents=[entry.content],
                metadatas=[metadata]
            )
            
            return document_id
            
        except Exception as e:
            raise VectorStoreError(f"Failed to add document to ChromaDB: {str(e)}")
    
    async def search_similar(
        self,
        query_embedding: List[float],
        limit: int = 10,
        similarity_threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[KnowledgeEntry, float]]:
        """Search for similar documents using embedding."""
        try:
            collection = await self._get_collection()
            
            # Build where clause for filters
            where_clause = None
            if filters:
                where_clause = {}
                for key, value in filters.items():
                    if isinstance(value, list):
                        where_clause[key] = {"$in": value}
                    else:
                        where_clause[key] = {"$eq": value}
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            
            entries = []
            if results["ids"] and results["ids"][0]:
                for i, doc_id in enumerate(results["ids"][0]):
                    distance = results["distances"][0][i] if results["distances"] else 0
                    similarity = 1 - distance  # Convert distance to similarity
                    
                    if similarity >= similarity_threshold:
                        metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                        content = results["documents"][0][i] if results["documents"] else ""
                        
                        entry = self._metadata_to_knowledge_entry(
                            doc_id, content, metadata
                        )
                        entries.append((entry, similarity))
            
            return entries
            
        except Exception as e:
            raise VectorStoreError(f"Failed to search ChromaDB: {str(e)}")
    
    async def search_by_text(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[KnowledgeEntry, float]]:
        """Search for documents using text query (requires embedding generation)."""
        # Note: This method requires an embedding service to convert text to embeddings
        # For now, we'll implement a basic text search using ChromaDB's built-in functionality
        try:
            collection = await self._get_collection()
            
            # Build where clause for filters
            where_clause = None
            if filters:
                where_clause = {}
                for key, value in filters.items():
                    if isinstance(value, list):
                        where_clause[key] = {"$in": value}
                    else:
                        where_clause[key] = {"$eq": value}
            
            # Use ChromaDB's query with text (it will generate embeddings internally if configured)
            results = collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            
            entries = []
            if results["ids"] and results["ids"][0]:
                for i, doc_id in enumerate(results["ids"][0]):
                    distance = results["distances"][0][i] if results["distances"] else 0
                    similarity = 1 - distance
                    
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    content = results["documents"][0][i] if results["documents"] else ""
                    
                    entry = self._metadata_to_knowledge_entry(
                        doc_id, content, metadata
                    )
                    entries.append((entry, similarity))
            
            return entries
            
        except Exception as e:
            raise VectorStoreError(f"Failed to text search ChromaDB: {str(e)}")
    
    async def update_document(
        self,
        entry_id: str,
        entry: KnowledgeEntry,
        embedding: List[float]
    ) -> bool:
        """Update a document and its embedding in ChromaDB."""
        try:
            collection = await self._get_collection()
            
            metadata = {
                "title": entry.title,
                "category": entry.category,
                "tags": ",".join(entry.tags) if entry.tags else "",
                "source": entry.source or "",
                "created_at": entry.created_at.isoformat() if entry.created_at else "",
                "updated_at": entry.updated_at.isoformat() if entry.updated_at else ""
            }
            
            collection.update(
                ids=[entry_id],
                embeddings=[embedding],
                documents=[entry.content],
                metadatas=[metadata]
            )
            
            return True
            
        except Exception as e:
            raise VectorStoreError(f"Failed to update document in ChromaDB: {str(e)}")
    
    async def delete_document(self, entry_id: str) -> bool:
        """Delete a document from ChromaDB."""
        try:
            collection = await self._get_collection()
            
            collection.delete(ids=[entry_id])
            return True
            
        except Exception as e:
            raise VectorStoreError(f"Failed to delete document from ChromaDB: {str(e)}")
    
    async def get_document_count(self) -> int:
        """Get the total number of documents in the collection."""
        try:
            collection = await self._get_collection()
            return collection.count()
            
        except Exception as e:
            raise VectorStoreError(f"Failed to get document count: {str(e)}")
    
    async def list_collections(self) -> List[str]:
        """List all collections in ChromaDB."""
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
            
        except Exception as e:
            raise VectorStoreError(f"Failed to list collections: {str(e)}")
    
    async def create_collection(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Create a new collection."""
        try:
            self.client.create_collection(
                name=name,
                metadata=metadata or {}
            )
            return True
            
        except Exception as e:
            raise VectorStoreError(f"Failed to create collection: {str(e)}")
    
    async def delete_collection(self, name: str) -> bool:
        """Delete a collection."""
        try:
            self.client.delete_collection(name=name)
            return True
            
        except Exception as e:
            raise VectorStoreError(f"Failed to delete collection: {str(e)}")
    
    def _metadata_to_knowledge_entry(
        self,
        doc_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> KnowledgeEntry:
        """Convert ChromaDB metadata back to KnowledgeEntry."""
        from datetime import datetime
        
        tags = []
        if metadata.get("tags"):
            tags = metadata["tags"].split(",")
        
        created_at = None
        updated_at = None
        
        if metadata.get("created_at"):
            try:
                created_at = datetime.fromisoformat(metadata["created_at"])
            except:
                pass
                
        if metadata.get("updated_at"):
            try:
                updated_at = datetime.fromisoformat(metadata["updated_at"])
            except:
                pass
        
        return KnowledgeEntry(
            id=uuid.UUID(doc_id),
            title=metadata.get("title", ""),
            content=content,
            category=metadata.get("category", ""),
            tags=tags,
            source=metadata.get("source"),
            created_at=created_at,
            updated_at=updated_at
        )
