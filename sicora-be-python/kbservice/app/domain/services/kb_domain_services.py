"""Domain services for Knowledge Base Service."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.domain.entities.kb_entities import KnowledgeItem, UserRole
from app.domain.value_objects.kb_value_objects import Vector, SearchScore


class EmbeddingService(ABC):
    """Service interface for generating embeddings."""
    
    @abstractmethod
    async def generate_embedding(self, text: str) -> Vector:
        """Generate embedding vector for text."""
        pass
    
    @abstractmethod
    async def generate_embeddings_batch(self, texts: List[str]) -> List[Vector]:
        """Generate embedding vectors for multiple texts."""
        pass


class SearchService(ABC):
    """Service interface for advanced search operations."""
    
    @abstractmethod
    async def hybrid_search(
        self,
        query: str,
        user_role: UserRole,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Perform hybrid search combining text and semantic search."""
        pass
    
    @abstractmethod
    async def semantic_search(
        self,
        query: str,
        user_role: UserRole,
        threshold: float = 0.7,
        limit: int = 20
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Perform semantic search using embeddings."""
        pass
    
    @abstractmethod
    async def text_search(
        self,
        query: str,
        user_role: UserRole,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20
    ) -> List[tuple[KnowledgeItem, SearchScore]]:
        """Perform traditional text search."""
        pass
    
    @abstractmethod
    async def get_related_items(
        self,
        item_id: UUID,
        limit: int = 5
    ) -> List[KnowledgeItem]:
        """Get related knowledge items."""
        pass


class ContentValidationService:
    """Service for validating knowledge content."""
    
    def validate_content_quality(self, content: str) -> Dict[str, Any]:
        """Validate content quality and provide suggestions."""
        issues = []
        suggestions = []
        
        # Check content length
        if len(content) < 100:
            issues.append("Content is too short")
            suggestions.append("Consider adding more detailed information")
        
        # Check for basic structure
        if '\n' not in content and len(content) > 500:
            issues.append("Content lacks structure")
            suggestions.append("Consider adding paragraphs or bullet points")
        
        # Check for questions without answers
        if '?' in content and content.count('?') > content.count('respuesta'):
            issues.append("Questions may lack clear answers")
            suggestions.append("Ensure all questions have clear answers")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions,
            "quality_score": max(0.0, 1.0 - (len(issues) * 0.2))
        }
    
    def extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content."""
        # Simple keyword extraction - in production, use NLP libraries
        import re
        
        # Remove common Spanish stop words
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo',
            'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las',
            'una', 'sus', 'pero', 'como', 'más', 'muy', 'todo', 'ser', 'tiene', 'puede'
        }
        
        # Extract words
        words = re.findall(r'\b[a-záéíóúñ]{3,}\b', content.lower())
        
        # Filter stop words and get unique words
        keywords = list(set(word for word in words if word not in stop_words))
        
        # Sort by frequency in content
        keyword_freq = [(word, content.lower().count(word)) for word in keywords]
        keyword_freq.sort(key=lambda x: x[1], reverse=True)
        
        return [word for word, _ in keyword_freq[:20]]  # Top 20 keywords


class ChatbotIntegrationService(ABC):
    """Service interface for chatbot integration."""
    
    @abstractmethod
    async def should_route_to_chatbot(self, query: str) -> bool:
        """Determine if query should be routed to regulation chatbot."""
        pass
    
    @abstractmethod
    async def query_regulation_chatbot(self, query: str, user_context: Dict[str, Any]) -> str:
        """Query the regulation chatbot."""
        pass
    
    @abstractmethod
    async def combine_responses(
        self, 
        kb_response: str, 
        chatbot_response: str, 
        query: str
    ) -> str:
        """Combine responses from knowledge base and chatbot."""
        pass


class PersonalizationService:
    """Service for personalizing content and responses."""
    
    def personalize_content_for_role(
        self, 
        content: str, 
        user_role: UserRole
    ) -> str:
        """Personalize content based on user role."""
        if user_role == UserRole.STUDENT:
            # Add friendly, explanatory tone for students
            if "procedimiento" in content.lower():
                return f"📚 **Guía para Aprendices:**\n\n{content}\n\n💡 **Tip:** Si tienes dudas, no dudes en contactar a tu instructor."
        
        elif user_role == UserRole.INSTRUCTOR:
            # Add professional context for instructors
            if "gestión" in content.lower() or "administrar" in content.lower():
                return f"👨‍🏫 **Información para Instructores:**\n\n{content}\n\n📋 **Nota:** Recuerda documentar cualquier acción administrativa."
        
        elif user_role == UserRole.ADMIN:
            # Add technical details for admins
            return f"⚙️ **Información Técnica:**\n\n{content}\n\n🔧 **Consideraciones adicionales:** Revisa los logs del sistema para más detalles."
        
        return content
    
    def generate_response_suggestions(
        self, 
        query: str, 
        user_role: UserRole
    ) -> List[str]:
        """Generate response suggestions based on query and user role."""
        suggestions = []
        
        query_lower = query.lower()
        
        if user_role == UserRole.STUDENT:
            if "asistencia" in query_lower:
                suggestions.extend([
                    "¿Cómo justifico una falta?",
                    "¿Cuál es el porcentaje mínimo de asistencia?",
                    "¿Dónde veo mi registro de asistencia?"
                ])
            elif "nota" in query_lower or "calificación" in query_lower:
                suggestions.extend([
                    "¿Cómo consulto mis calificaciones?",
                    "¿Cuáles son los criterios de evaluación?",
                    "¿Cómo solicito revisión de una nota?"
                ])
        
        elif user_role == UserRole.INSTRUCTOR:
            if "registro" in query_lower:
                suggestions.extend([
                    "¿Cómo registro asistencia masiva?",
                    "¿Cómo genero reportes de asistencia?",
                    "¿Cómo manejo justificaciones tardías?"
                ])
        
        elif user_role == UserRole.ADMIN:
            if "usuario" in query_lower:
                suggestions.extend([
                    "¿Cómo crear usuarios masivamente?",
                    "¿Cómo gestionar permisos de usuario?",
                    "¿Cómo realizar backup de usuarios?"
                ])
        
        return suggestions[:5]  # Return top 5 suggestions
