"""Service implementations for Knowledge Base Service."""

import httpx
from openai import AsyncOpenAI
from typing import List, Optional, Dict, Any
from uuid import UUID
import hashlib
import asyncio

from app.config import settings
from app.domain.entities.kb_entities import KnowledgeItem, UserRole
from app.domain.value_objects.kb_value_objects import Vector, SearchScore
from app.domain.services.kb_domain_services import (
    EmbeddingService, SearchService, ChatbotIntegrationService
)
from app.domain.repositories.kb_repositories import KnowledgeItemRepository
from app.domain.exceptions.kb_exceptions import EmbeddingError, SearchError


class OpenAIEmbeddingService(EmbeddingService):
    """OpenAI embedding service implementation using OpenAI v1.x API."""
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                timeout=settings.OPENAI_REQUEST_TIMEOUT,
                max_retries=settings.OPENAI_MAX_RETRIES
            )
    
    async def generate_embedding(self, text: str) -> Vector:
        """Generate embedding vector for text using OpenAI v1.x API."""
        try:
            if not self.client:
                # Mock embedding for development/testing
                return self._generate_mock_embedding(text)
            
            # Clean and truncate text
            clean_text = text.replace("\n", " ").strip()[:settings.MAX_CONTENT_LENGTH]
            
            if not clean_text:
                raise EmbeddingError("Empty text provided for embedding")
            
            response = await self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=clean_text,
                encoding_format="float"
            )
            
            embedding_values = response.data[0].embedding
            
            # Validate embedding dimension
            if len(embedding_values) != settings.EMBEDDING_DIMENSION:
                raise EmbeddingError(
                    f"Unexpected embedding dimension: {len(embedding_values)}, "
                    f"expected: {settings.EMBEDDING_DIMENSION}"
                )
            
            return Vector(embedding_values)
            
        except Exception as e:
            if isinstance(e, EmbeddingError):
                raise
            raise EmbeddingError(f"Failed to generate embedding: {str(e)}")
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[Vector]:
        """Generate embedding vectors for multiple texts with batch processing."""
        try:
            if not texts:
                return []
            
            if not self.client:
                # Mock embeddings for development/testing
                return [self._generate_mock_embedding(text) for text in texts]
            
            # Clean and truncate texts
            clean_texts = []
            for text in texts:
                clean_text = text.replace("\n", " ").strip()[:settings.MAX_CONTENT_LENGTH]
                if clean_text:
                    clean_texts.append(clean_text)
                else:
                    clean_texts.append("default text")  # Fallback for empty text
            
            # Process in batches to avoid API limits
            batch_size = getattr(settings, 'OPENAI_BATCH_SIZE', 100)
            all_embeddings = []
            
            for i in range(0, len(clean_texts), batch_size):
                batch_texts = clean_texts[i:i + batch_size]
                
                response = await self.client.embeddings.create(
                    model=settings.EMBEDDING_MODEL,
                    input=batch_texts,
                    encoding_format="float"
                )
                
                batch_embeddings = []
                for item in response.data:
                    embedding_values = item.embedding
                    
                    # Validate embedding dimension
                    if len(embedding_values) != settings.EMBEDDING_DIMENSION:
                        raise EmbeddingError(
                            f"Unexpected embedding dimension: {len(embedding_values)}, "
                            f"expected: {settings.EMBEDDING_DIMENSION}"
                        )
                    
                    batch_embeddings.append(Vector(embedding_values))
                
                all_embeddings.extend(batch_embeddings)
                
                # Add small delay to respect rate limits
                if i + batch_size < len(clean_texts):
                    await asyncio.sleep(0.1)
            
            return all_embeddings
            
        except Exception as e:
            if isinstance(e, EmbeddingError):
                raise
            raise EmbeddingError(f"Failed to generate batch embeddings: {str(e)}")
    
    def _generate_mock_embedding(self, text: str) -> Vector:
        """Generate a mock embedding for development/testing."""
        # Create a deterministic mock embedding based on text hash
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Convert hex to normalized numbers
        values = []
        for i in range(0, len(hash_hex), 2):
            if len(values) >= settings.EMBEDDING_DIMENSION:
                break
            hex_pair = hash_hex[i:i+2]
            normalized_value = (int(hex_pair, 16) / 255.0) * 2.0 - 1.0  # Normalize to [-1, 1]
            values.append(normalized_value)
        
        # Pad to expected dimension
        while len(values) < settings.EMBEDDING_DIMENSION:
            values.append(0.0)
        
        return Vector(values[:settings.EMBEDDING_DIMENSION])


class HybridSearchService(SearchService):
    """Hybrid search service combining text and semantic search."""
    
    def __init__(
        self, 
        knowledge_item_repo: KnowledgeItemRepository,
        embedding_service: EmbeddingService
    ):
        self.knowledge_item_repo = knowledge_item_repo
        self.embedding_service = embedding_service
    
    async def hybrid_search(
        self,
        query: str,
        user_role: UserRole,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Perform hybrid search combining text and semantic search."""
        try:
            # Prepare filters with role-based restrictions
            search_filters = filters or {}
            if user_role != UserRole.ADMIN:
                search_filters["status"] = "published"
            
            # Perform text search
            text_results = await self.knowledge_item_repo.search_by_text(
                query=query,
                skip=0,
                limit=limit * 2,  # Get more results for combining
                filters=search_filters
            )
            
            # Perform semantic search
            query_embedding = await self.embedding_service.generate_embedding(query)
            semantic_results = await self.knowledge_item_repo.search_by_vector(
                vector=query_embedding,
                threshold=settings.VECTOR_SIMILARITY_THRESHOLD,
                limit=limit * 2,
                filters=search_filters
            )
            
            # Combine and rank results
            combined_results = self._combine_search_results(
                text_results, semantic_results, query, user_role
            )
            
            return combined_results[:limit]
            
        except Exception as e:
            raise SearchError(f"Hybrid search failed: {str(e)}")
    
    async def semantic_search(
        self,
        query: str,
        user_role: UserRole,
        threshold: float = 0.7,
        limit: int = 20
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Perform semantic search using embeddings."""
        try:
            # Generate query embedding
            query_embedding = await self.embedding_service.generate_embedding(query)
            
            # Prepare filters
            filters = {}
            if user_role != UserRole.ADMIN:
                filters["status"] = "published"
            
            # Perform vector search
            results = await self.knowledge_item_repo.search_by_vector(
                vector=query_embedding,
                threshold=threshold,
                limit=limit,
                filters=filters
            )
            
            # Filter by user role access
            accessible_results = []
            for item, score in results:
                if item.is_accessible_by(user_role):
                    accessible_results.append((item, score))
            
            return accessible_results
            
        except Exception as e:
            raise SearchError(f"Semantic search failed: {str(e)}")
    
    async def text_search(
        self,
        query: str,
        user_role: UserRole,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Perform traditional text search."""
        try:
            # Prepare filters
            search_filters = filters or {}
            if user_role != UserRole.ADMIN:
                search_filters["status"] = "published"
            
            # Perform text search
            results = await self.knowledge_item_repo.search_by_text(
                query=query,
                skip=0,
                limit=limit,
                filters=search_filters
            )
            
            # Calculate simple text relevance scores
            scored_results = []
            query_lower = query.lower()
            
            for item in results:
                if item.is_accessible_by(user_role):
                    # Simple scoring based on query term frequency
                    title_score = query_lower.count(item.title.value.lower()) * 2
                    content_score = query_lower.count(item.content.value.lower())
                    
                    # Normalize score
                    total_score = min(1.0, (title_score + content_score) / 10.0)
                    if total_score == 0:
                        total_score = 0.1  # Minimum score for matches
                    
                    scored_results.append((item, SearchScore(total_score)))
            
            # Sort by score
            scored_results.sort(key=lambda x: x[1].value, reverse=True)
            
            return scored_results
            
        except Exception as e:
            raise SearchError(f"Text search failed: {str(e)}")
    
    async def get_related_items(
        self,
        item_id: UUID,
        limit: int = 5
    ) -> List[KnowledgeItem]:
        """Get related knowledge items."""
        try:
            # Get the source item
            from app.domain.value_objects.kb_value_objects import KnowledgeItemId
            source_item = await self.knowledge_item_repo.get_by_id(KnowledgeItemId(item_id))
            
            if not source_item or not source_item.embedding:
                return []
            
            # Find similar items by vector similarity
            similar_results = await self.knowledge_item_repo.search_by_vector(
                vector=source_item.embedding,
                threshold=0.6,
                limit=limit + 1,  # +1 to exclude the source item
                filters={"status": "published"}
            )
            
            # Exclude the source item and return related items
            related_items = []
            for item, score in similar_results:
                if item.id.value != item_id:
                    related_items.append(item)
            
            return related_items[:limit]
            
        except Exception as e:
            raise SearchError(f"Failed to get related items: {str(e)}")
    
    def _combine_search_results(
        self,
        text_results: List[KnowledgeItem],
        semantic_results: List[tuple[KnowledgeItem, SearchScore]],
        query: str,
        user_role: UserRole
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Combine and score results from text and semantic search."""
        # Create item score map
        item_scores = {}
        
        # Add semantic scores (higher weight)
        for item, score in semantic_results:
            if item.is_accessible_by(user_role):
                item_scores[item.id.value] = score.value * 0.7
        
        # Add text scores (lower weight)
        query_lower = query.lower()
        for item in text_results:
            if item.is_accessible_by(user_role):
                # Calculate text relevance
                title_matches = item.title.value.lower().count(query_lower)
                content_matches = item.content.value.lower().count(query_lower)
                text_score = min(1.0, (title_matches * 2 + content_matches) / 10.0)
                
                # Combine with existing semantic score or use text score
                if item.id.value in item_scores:
                    item_scores[item.id.value] += text_score * 0.3
                else:
                    item_scores[item.id.value] = text_score * 0.5
        
        # Create final results
        final_results = []
        processed_ids = set()
        
        # Add items from semantic results
        for item, _ in semantic_results:
            if item.id.value in item_scores and item.id.value not in processed_ids:
                final_score = SearchScore(min(1.0, item_scores[item.id.value]))
                final_results.append((item, final_score))
                processed_ids.add(item.id.value)
        
        # Add items from text results that weren't in semantic results
        for item in text_results:
            if item.id.value in item_scores and item.id.value not in processed_ids:
                final_score = SearchScore(min(1.0, item_scores[item.id.value]))
                final_results.append((item, final_score))
                processed_ids.add(item.id.value)
        
        # Sort by combined score
        final_results.sort(key=lambda x: x[1].value, reverse=True)
        
        return final_results


class HTTPChatbotIntegrationService(ChatbotIntegrationService):
    """HTTP-based chatbot integration service."""
    
    def __init__(self):
        self.aiservice_url = settings.AISERVICE_URL
        self.timeout = 30.0
    
    async def should_route_to_chatbot(self, query: str) -> bool:
        """Determine if query should be routed to regulation chatbot."""
        # Keywords that indicate regulation-related queries
        regulation_keywords = [
            "reglamento", "norma", "política", "regla", "sanciones",
            "faltas", "disciplina", "comportamiento", "conducta",
            "prohibido", "permitido", "obligatorio", "debe", "puede"
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in regulation_keywords)
    
    async def query_regulation_chatbot(self, query: str, user_context: Dict[str, Any]) -> str:
        """Query the regulation chatbot."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.aiservice_url}/api/v1/chat/query",
                    json={
                        "message": query,
                        "user_context": user_context
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "Lo siento, no pude obtener una respuesta del chatbot.")
                else:
                    return "El servicio de chatbot no está disponible en este momento."
                    
        except Exception as e:
            return f"Error al consultar el chatbot: {str(e)}"
    
    async def combine_responses(
        self, 
        kb_response: str, 
        chatbot_response: str, 
        query: str
    ) -> str:
        """Combine responses from knowledge base and chatbot."""
        if not kb_response and not chatbot_response:
            return "Lo siento, no encontré información relevante para tu consulta."
        
        if not kb_response:
            return f"**Información del Reglamento:**\n\n{chatbot_response}"
        
        if not chatbot_response:
            return f"**Información de la Base de Conocimiento:**\n\n{kb_response}"
        
        # Combine both responses
        combined = f"""**Información Completa:**

**Base de Conocimiento:**
{kb_response}

**Reglamento Institucional:**
{chatbot_response}

---
*Esta respuesta combina información de nuestra base de conocimiento y el reglamento oficial.*"""
        
        return combined


class QueryAnalyticsService:
    """Service for analyzing query patterns and generating insights."""
    
    def __init__(self, search_query_repo):
        self.search_query_repo = search_query_repo
    
    async def get_service_metrics(self, period: str) -> Dict[str, Any]:
        """Get comprehensive service metrics for a given period."""
        # TODO: Implement actual metrics collection from database
        # This is a placeholder implementation
        
        # Mock metrics based on period
        base_metrics = {
            "total_queries": 1250,
            "avg_response_time": 0.45,
            "search_accuracy": 0.87,
            "error_rate": 0.02,
            "user_satisfaction": 0.91,
            "resource_usage": {
                "cpu_usage": 0.65,
                "memory_usage": 0.78,
                "disk_usage": 0.45,
                "db_connections": 12
            }
        }
        
        # Adjust metrics based on period
        multipliers = {
            "1h": 0.04,
            "24h": 1.0,
            "7d": 7.0,
            "30d": 30.0
        }
        
        multiplier = multipliers.get(period, 1.0)
        base_metrics["total_queries"] = int(base_metrics["total_queries"] * multiplier)
        
        return base_metrics
    
    async def analyze_query_patterns(self, period: str, limit: int) -> List[Dict[str, Any]]:
        """Analyze query patterns and return insights."""
        # TODO: Implement actual pattern analysis from search query logs
        # This is a placeholder implementation
        
        patterns = [
            {
                "pattern": "asistencia registro",
                "frequency": 156,
                "trend": "increasing",
                "success_rate": 0.92,
                "avg_satisfaction": 4.2
            },
            {
                "pattern": "horarios clases",
                "frequency": 134,
                "trend": "stable",
                "success_rate": 0.89,
                "avg_satisfaction": 4.0
            },
            {
                "pattern": "reglamento estudiantes",
                "frequency": 98,
                "trend": "increasing",
                "success_rate": 0.95,
                "avg_satisfaction": 4.5
            },
            {
                "pattern": "evaluaciones fechas",
                "frequency": 87,
                "trend": "seasonal",
                "success_rate": 0.88,
                "avg_satisfaction": 3.9
            },
            {
                "pattern": "certificados obtener",
                "frequency": 76,
                "trend": "stable",
                "success_rate": 0.84,
                "avg_satisfaction": 3.8
            }
        ]
        
        return patterns[:limit]
    
    async def generate_insights(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate insights based on query patterns."""
        insights = []
        
        if patterns:
            # Analyze trends
            increasing_patterns = [p for p in patterns if p["trend"] == "increasing"]
            if increasing_patterns:
                insights.append(
                    f"Se detecta un aumento en consultas sobre: {', '.join([p['pattern'] for p in increasing_patterns[:3]])}"
                )
            
            # Analyze success rates
            low_success = [p for p in patterns if p["success_rate"] < 0.85]
            if low_success:
                insights.append(
                    f"Patrones con baja tasa de éxito que requieren atención: {', '.join([p['pattern'] for p in low_success[:2]])}"
                )
            
            # Analyze satisfaction
            low_satisfaction = [p for p in patterns if p["avg_satisfaction"] < 4.0]
            if low_satisfaction:
                insights.append(
                    f"Áreas con baja satisfacción del usuario: {', '.join([p['pattern'] for p in low_satisfaction[:2]])}"
                )
            
            # General insights
            total_queries = sum(p["frequency"] for p in patterns)
            avg_success_rate = sum(p["success_rate"] for p in patterns) / len(patterns)
            
            insights.append(f"Total de consultas analizadas: {total_queries}")
            insights.append(f"Tasa de éxito promedio: {avg_success_rate:.1%}")
        
        return insights if insights else ["No hay suficientes datos para generar insights."]
