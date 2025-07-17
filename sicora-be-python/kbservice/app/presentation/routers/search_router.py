"""Search router for Knowledge Base Service."""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from app.dependencies import (
    get_current_user,
    get_search_knowledge_use_case
)
from app.presentation.schemas.kb_schemas import (
    SearchRequest,
    SearchResponse,
    QueryRequest,
    QueryResponse
)
from app.application.use_cases.kb_use_cases import SearchKnowledgeUseCase
from app.application.dtos.kb_dtos import SearchRequestDTO
from app.domain.entities.kb_entities import UserRole
from app.domain.exceptions.kb_exceptions import SearchError, InvalidSearchQueryError

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search_knowledge(
    search_request: SearchRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    search_use_case: SearchKnowledgeUseCase = Depends(get_search_knowledge_use_case)
):
    """
    Search knowledge base items.
    
    Performs intelligent search across the knowledge base using multiple strategies:
    
    - **text**: Traditional keyword-based search
    - **semantic**: AI-powered semantic search using embeddings
    - **hybrid**: Combines both text and semantic search (default)
    
    Results are filtered based on user role and access permissions.
    
    **Search filters available:**
    - category: Filter by specific category
    - content_type: Filter by content type (article, faq, guide, etc.)
    - target_audience: Filter by target audience
    
    **Examples:**
    - `"cómo registrar asistencia"` - finds guides about attendance registration
    - `"faltas justificadas"` - finds information about excused absences
    - `"políticas de evaluación"` - finds evaluation policies
    """
    try:
        user_role = UserRole(current_user["role"])
        
        # Convert to DTO
        dto = SearchRequestDTO(
            query=search_request.query,
            filters=search_request.filters,
            limit=search_request.limit,
            offset=search_request.offset
        )
        
        # Add search type to filters
        if hasattr(search_request, 'search_type') and search_request.search_type:
            dto.filters["search_type"] = search_request.search_type
        
        # Execute search
        result = await search_use_case.execute(dto, current_user["user_id"], user_role)
        
        return result
        
    except InvalidSearchQueryError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SearchError as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/query", response_model=QueryResponse)
async def intelligent_query(
    query_request: QueryRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process an intelligent query with potential chatbot integration.
    
    This endpoint provides an AI-powered query processing that:
    
    1. **Analyzes the query** to understand intent and context
    2. **Searches the knowledge base** for relevant information
    3. **Consults the regulation chatbot** if the query is regulation-related
    4. **Generates a comprehensive response** combining multiple sources
    5. **Personalizes the response** based on user role and context
    
    **Features:**
    - Natural language understanding
    - Context-aware responses
    - Role-based personalization
    - Integration with regulation chatbot
    - Source attribution and confidence scoring
    - Related query suggestions
    
    **Example queries:**
    - `"¿Puedo faltar por motivos médicos?"`
    - `"Cómo justifico una inasistencia"`
    - `"Cuál es el porcentaje mínimo de asistencia"`
    - `"Procedimiento para solicitar revisión de notas"`
    
    **Context parameters:**
    - user_role: Automatically determined from token
    - program: User's academic program
    - ficha: User's group/cohort
    - semester: Current semester
    """
    try:
        user_role = UserRole(current_user["role"])
        
        # Add user info to context
        context = query_request.context.copy()
        context.update({
            "user_id": str(current_user["user_id"]),
            "user_role": user_role.value,
            "email": current_user["email"]
        })
        
        # TODO: Implement intelligent query processing
        # This would involve:
        # 1. Query analysis and intent detection
        # 2. Knowledge base search
        # 3. Chatbot integration if needed
        # 4. Response generation and personalization
        
        # For now, return a placeholder response
        response = QueryResponse(
            answer="Esta funcionalidad está en desarrollo. Por favor, usa la búsqueda tradicional por ahora.",
            sources=[],
            confidence=0.0,
            suggestions=[
                "Usar la búsqueda tradicional",
                "Consultar las categorías disponibles",
                "Contactar soporte técnico"
            ],
            chatbot_used=False
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query processing failed: {str(e)}"
        )


@router.get("/suggestions")
async def get_query_suggestions(
    query: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get query suggestions based on partial input.
    
    Provides intelligent suggestions as the user types, based on:
    - Popular queries from other users with the same role
    - Common question patterns
    - Available content topics
    
    **Parameters:**
    - **query**: Partial query text (minimum 2 characters)
    
    **Returns:**
    List of suggested complete queries that the user might want to ask.
    """
    try:
        if len(query.strip()) < 2:
            return {"suggestions": []}
        
        user_role = UserRole(current_user["role"])
        
        # TODO: Implement intelligent suggestions
        # This would involve:
        # 1. Analyzing partial query
        # 2. Looking up frequent queries by role
        # 3. Finding similar content topics
        # 4. Generating contextual suggestions
        
        # For now, return role-based suggestions
        base_suggestions = {
            UserRole.STUDENT: [
                "¿Cómo registro mi asistencia?",
                "¿Cuál es el porcentaje mínimo de asistencia?",
                "¿Cómo justifico una falta?",
                "¿Dónde veo mis calificaciones?",
                "¿Cómo solicito certificados?"
            ],
            UserRole.INSTRUCTOR: [
                "¿Cómo registro asistencia masiva?",
                "¿Cómo genero reportes de asistencia?",
                "¿Cómo gestiono justificaciones?",
                "¿Cómo ingreso calificaciones?",
                "¿Cómo manejo casos disciplinarios?"
            ],
            UserRole.ADMIN: [
                "¿Cómo crear usuarios masivamente?",
                "¿Cómo generar reportes administrativos?",
                "¿Cómo configurar períodos académicos?",
                "¿Cómo gestionar permisos de usuario?",
                "¿Cómo realizar backup del sistema?"
            ]
        }
        
        suggestions = base_suggestions.get(user_role, [])
        
        # Filter suggestions that contain the query text
        query_lower = query.lower()
        filtered_suggestions = [
            s for s in suggestions 
            if query_lower in s.lower()
        ]
        
        return {"suggestions": filtered_suggestions[:5]}
        
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get suggestions: {str(e)}"
        )
