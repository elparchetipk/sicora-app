"""
Knowledge Base Integration Service
Servicio de integración entre AIService y KbService para el chatbot
"""
import httpx
import asyncio
from typing import List, Dict, Any, Optional
from uuid import UUID
import logging
from datetime import datetime

from app.domain.exceptions.ai_exceptions import KnowledgeBaseError, SearchError
from app.application.dtos.ai_dtos import KnowledgeSearchResult, ChatContext

logger = logging.getLogger(__name__)


class KbServiceIntegration:
    """
    Integración con KbService para búsqueda de conocimiento y contexto del chatbot.
    
    Esta clase maneja la comunicación con el microservicio KbService para:
    - Búsqueda semántica en la base de conocimiento
    - Obtención de contexto relevante para respuestas del chatbot
    - Gestión de resultados de búsqueda y relevancia
    """
    
    def __init__(
        self, 
        kb_service_url: str = "http://kbservice:8000/api/v1",
        timeout: int = 30
    ):
        self.kb_service_url = kb_service_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def search_knowledge(
        self,
        query: str,
        user_id: UUID,
        search_type: str = "hybrid",
        limit: int = 5,
        category_filter: Optional[str] = None
    ) -> List[KnowledgeSearchResult]:
        """
        Buscar conocimiento relevante en KbService.
        
        Args:
            query: Consulta del usuario
            user_id: ID del usuario que realiza la consulta
            search_type: Tipo de búsqueda (text, semantic, hybrid)
            limit: Número máximo de resultados
            category_filter: Filtro por categoría (opcional)
            
        Returns:
            Lista de resultados de búsqueda con contenido relevante
            
        Raises:
            KnowledgeBaseError: Error en comunicación con KbService
            SearchError: Error en la búsqueda
        """
        try:
            search_payload = {
                "query": query,
                "search_type": search_type,
                "limit": limit,
                "filters": {
                    "target_audience": ["all", "student", "instructor"],
                    "content_status": "published"
                }
            }
            
            if category_filter:
                search_payload["filters"]["category"] = category_filter
            
            # Headers con autenticación del usuario
            headers = {
                "User-ID": str(user_id),
                "Content-Type": "application/json"
            }
            
            response = await self.client.post(
                f"{self.kb_service_url}/search/search",
                json=search_payload,
                headers=headers
            )
            
            if response.status_code == 200:
                search_data = response.json()
                return self._parse_search_results(search_data)
            elif response.status_code == 404:
                logger.warning(f"No results found for query: {query}")
                return []
            else:
                raise KnowledgeBaseError(
                    f"KbService search failed: {response.status_code} - {response.text}"
                )
                
        except httpx.TimeoutException:
            raise KnowledgeBaseError("Timeout connecting to KbService")
        except httpx.RequestError as e:
            raise KnowledgeBaseError(f"Error connecting to KbService: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in knowledge search: {str(e)}")
            raise SearchError(f"Failed to search knowledge base: {str(e)}")
    
    async def get_regulatory_context(
        self,
        query: str,
        user_id: UUID
    ) -> List[KnowledgeSearchResult]:
        """
        Obtener contexto específico del Reglamento del Aprendiz SENA.
        
        Args:
            query: Consulta relacionada con el reglamento
            user_id: ID del usuario
            
        Returns:
            Contexto relevante del reglamento para la consulta
        """
        try:
            # Búsqueda específica en contenido de reglamento
            results = await self.search_knowledge(
                query=f"reglamento aprendiz SENA {query}",
                user_id=user_id,
                search_type="semantic",
                limit=3,
                category_filter="reglamento"
            )
            
            # Si no encuentra resultados específicos, buscar de forma más general
            if not results:
                results = await self.search_knowledge(
                    query=query,
                    user_id=user_id,
                    search_type="hybrid",
                    limit=3
                )
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting regulatory context: {str(e)}")
            return []
    
    async def get_chat_context(
        self,
        user_query: str,
        conversation_history: List[Dict[str, Any]],
        user_id: UUID
    ) -> ChatContext:
        """
        Obtener contexto completo para respuesta del chatbot.
        
        Args:
            user_query: Consulta actual del usuario
            conversation_history: Historial de la conversación
            user_id: ID del usuario
            
        Returns:
            Contexto enriquecido para generar respuesta del chatbot
        """
        try:
            # Análizar consulta para determinar categorías relevantes
            query_categories = self._analyze_query_categories(user_query)
            
            # Búsqueda principal
            main_results = await self.search_knowledge(
                query=user_query,
                user_id=user_id,
                search_type="hybrid",
                limit=5
            )
            
            # Búsqueda específica del reglamento si es relevante
            regulatory_results = []
            if self._is_regulatory_query(user_query):
                regulatory_results = await self.get_regulatory_context(
                    user_query, user_id
                )
            
            # Combinar y priorizar resultados
            all_results = self._merge_and_prioritize_results(
                main_results, regulatory_results
            )
            
            return ChatContext(
                query=user_query,
                knowledge_results=all_results,
                conversation_history=conversation_history,
                user_id=user_id,
                timestamp=datetime.utcnow(),
                categories=query_categories
            )
            
        except Exception as e:
            logger.error(f"Error getting chat context: {str(e)}")
            # Retornar contexto básico en caso de error
            return ChatContext(
                query=user_query,
                knowledge_results=[],
                conversation_history=conversation_history,
                user_id=user_id,
                timestamp=datetime.utcnow(),
                categories=[]
            )
    
    def _parse_search_results(self, search_data: Dict[str, Any]) -> List[KnowledgeSearchResult]:
        """Parsear resultados de búsqueda del KbService."""
        results = []
        
        for item in search_data.get("results", []):
            result = KnowledgeSearchResult(
                id=UUID(item["id"]),
                title=item["title"],
                content=item["content"],
                category=item.get("category", "general"),
                content_type=item.get("content_type", "article"),
                relevance_score=item.get("score", 0.0),
                source="kbservice",
                metadata={
                    "target_audience": item.get("target_audience"),
                    "created_at": item.get("created_at"),
                    "updated_at": item.get("updated_at"),
                    "tags": item.get("tags", [])
                }
            )
            results.append(result)
        
        return results
    
    def _analyze_query_categories(self, query: str) -> List[str]:
        """Analizar la consulta para determinar categorías relevantes."""
        categories = []
        query_lower = query.lower()
        
        # Mapeo de términos a categorías
        category_keywords = {
            "reglamento": ["reglamento", "norma", "regla", "sanción", "falta", "disciplinario"],
            "asistencia": ["asistencia", "falta", "inasistencia", "justificar", "ausencia"],
            "evaluación": ["evaluación", "calificación", "nota", "examen", "prueba"],
            "procedimientos": ["procedimiento", "proceso", "trámite", "solicitud"],
            "horarios": ["horario", "cronograma", "calendario", "fecha"],
            "académico": ["académico", "formación", "programa", "competencia"]
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                categories.append(category)
        
        return categories if categories else ["general"]
    
    def _is_regulatory_query(self, query: str) -> bool:
        """Determinar si la consulta está relacionada con el reglamento."""
        regulatory_terms = [
            "reglamento", "norma", "sanción", "falta", "disciplinario",
            "derechos", "deberes", "obligaciones", "prohibido", "permitido"
        ]
        
        query_lower = query.lower()
        return any(term in query_lower for term in regulatory_terms)
    
    def _merge_and_prioritize_results(
        self,
        main_results: List[KnowledgeSearchResult],
        regulatory_results: List[KnowledgeSearchResult]
    ) -> List[KnowledgeSearchResult]:
        """Combinar y priorizar resultados de búsqueda."""
        # Priorizar resultados regulatorios si existen
        if regulatory_results:
            # Aumentar score de resultados regulatorios
            for result in regulatory_results:
                result.relevance_score += 0.2
        
        # Combinar todos los resultados
        all_results = main_results + regulatory_results
        
        # Eliminar duplicados por ID
        seen_ids = set()
        unique_results = []
        for result in all_results:
            if result.id not in seen_ids:
                seen_ids.add(result.id)
                unique_results.append(result)
        
        # Ordenar por relevancia y retornar top 5
        unique_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return unique_results[:5]
    
    async def health_check(self) -> bool:
        """Verificar conectividad con KbService."""
        try:
            response = await self.client.get(f"{self.kb_service_url}/health")
            return response.status_code == 200
        except Exception:
            return False
    
    async def close(self):
        """Cerrar cliente HTTP."""
        await self.client.aclose()
