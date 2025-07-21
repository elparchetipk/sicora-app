"""Router proxy para AIService en ApiGateway."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, Dict, Any, List

from middleware.auth import get_current_user
from utils.service_discovery import get_service_url

router = APIRouter(tags=["ai"])

# URL del servicio de IA
AI_SERVICE_URL = get_service_url("ai")

async def forward_request_to_ai_service(
    method: str,
    endpoint: str,
    user_data: dict = None,
    json_data: dict = None,
    params: dict = None
):
    """Reenvía solicitudes al AIService."""
    url = f"{AI_SERVICE_URL}{endpoint}"
    
    headers = {}
    if user_data:
        headers["X-User-ID"] = str(user_data.get("user_id"))
        headers["X-User-Role"] = user_data.get("role", "")
        headers["X-User-Email"] = user_data.get("email", "")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, json=json_data, headers=headers)
            elif method.upper() == "PUT":
                response = await client.put(url, json=json_data, headers=headers)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method {method} not allowed"
                )
            
            return JSONResponse(
                status_code=response.status_code,
                content=response.json() if response.content else {}
            )
            
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AIService unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )

# =============================================================================
# ENDPOINTS DE CHAT INTELIGENTE
# =============================================================================

@router.post("/chat")
async def chat_with_ai(
    chat_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Interactuar con el asistente de IA."""
    return await forward_request_to_ai_service(
        method="POST",
        endpoint="/chat",
        json_data=chat_data,
        user_data=current_user
    )

@router.post("/chat/simple")
async def simple_chat(
    message_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Chat simple con el asistente de IA."""
    return await forward_request_to_ai_service(
        method="POST",
        endpoint="/chat/simple",
        json_data=message_data,
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE SESIONES DE CHAT
# =============================================================================

@router.get("/chat/sessions")
async def get_chat_sessions(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Obtener sesiones de chat del usuario."""
    params = {"skip": skip, "limit": limit}
    
    return await forward_request_to_ai_service(
        method="GET",
        endpoint="/chat/sessions",
        params=params,
        user_data=current_user
    )

@router.get("/chat/sessions/{session_id}")
async def get_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener sesión de chat específica."""
    return await forward_request_to_ai_service(
        method="GET",
        endpoint=f"/chat/sessions/{session_id}",
        user_data=current_user
    )

@router.post("/chat/sessions")
async def create_chat_session(
    session_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Crear nueva sesión de chat."""
    return await forward_request_to_ai_service(
        method="POST",
        endpoint="/chat/sessions",
        json_data=session_data,
        user_data=current_user
    )

@router.delete("/chat/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Eliminar sesión de chat."""
    return await forward_request_to_ai_service(
        method="DELETE",
        endpoint=f"/chat/sessions/{session_id}",
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE ANÁLISIS Y RECOMENDACIONES
# =============================================================================

@router.post("/analyze/document")
async def analyze_document(
    document_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Analizar documento con IA."""
    return await forward_request_to_ai_service(
        method="POST",
        endpoint="/analyze/document",
        json_data=document_data,
        user_data=current_user
    )

@router.post("/recommendations/learning")
async def get_learning_recommendations(
    request_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Obtener recomendaciones de aprendizaje personalizadas."""
    return await forward_request_to_ai_service(
        method="POST",
        endpoint="/recommendations/learning",
        json_data=request_data,
        user_data=current_user
    )

@router.post("/generate/summary")
async def generate_summary(
    content_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Generar resumen de contenido."""
    return await forward_request_to_ai_service(
        method="POST",
        endpoint="/generate/summary",
        json_data=content_data,
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE CONFIGURACIÓN
# =============================================================================

@router.get("/config")
async def get_ai_config(
    current_user: dict = Depends(get_current_user)
):
    """Obtener configuración del servicio de IA."""
    return await forward_request_to_ai_service(
        method="GET",
        endpoint="/config",
        user_data=current_user
    )

@router.get("/status")
async def get_ai_status(
    current_user: dict = Depends(get_current_user)
):
    """Obtener estado del servicio de IA."""
    return await forward_request_to_ai_service(
        method="GET",
        endpoint="/status",
        user_data=current_user
    )
