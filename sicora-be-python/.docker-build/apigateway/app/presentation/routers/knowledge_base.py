"""Router proxy para KBService en ApiGateway."""

from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, Dict, Any, List

from middleware.auth import get_current_user, get_instructor_user, get_admin_user
from utils.service_discovery import get_service_url

router = APIRouter(tags=["knowledge-base"])

# URL del servicio de base de conocimiento
KB_SERVICE_URL = get_service_url("kb")

async def forward_request_to_kb_service(
    method: str,
    endpoint: str,
    user_data: dict = None,
    json_data: dict = None,
    params: dict = None,
    files: dict = None,
    form_data: dict = None
):
    """Reenvía solicitudes al KBService."""
    url = f"{KB_SERVICE_URL}{endpoint}"
    
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
                if files or form_data:
                    response = await client.post(url, data=form_data, files=files, headers=headers)
                else:
                    response = await client.post(url, json=json_data, headers=headers)
            elif method.upper() == "PUT":
                if files or form_data:
                    response = await client.put(url, data=form_data, files=files, headers=headers)
                else:
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
                detail=f"KBService unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )

# =============================================================================
# ENDPOINTS DE DOCUMENTOS
# =============================================================================

@router.get("/documents")
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Obtener documentos de la base de conocimiento."""
    params = {"skip": skip, "limit": limit}
    if category:
        params["category"] = category
    if search:
        params["search"] = search
        
    return await forward_request_to_kb_service(
        method="GET",
        endpoint="/documents",
        params=params,
        user_data=current_user
    )

@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener documento por ID."""
    return await forward_request_to_kb_service(
        method="GET",
        endpoint=f"/documents/{document_id}",
        user_data=current_user
    )

@router.post("/documents")
async def create_document(
    document_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Crear nuevo documento (solo instructores)."""
    return await forward_request_to_kb_service(
        method="POST",
        endpoint="/documents",
        json_data=document_data,
        user_data=current_user
    )

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    category: str = "general",
    description: str = None,
    current_user: dict = Depends(get_instructor_user)
):
    """Subir archivo de documento."""
    form_data = {
        "category": category
    }
    if title:
        form_data["title"] = title
    if description:
        form_data["description"] = description
        
    files = {"file": (file.filename, file.file, file.content_type)}
    
    return await forward_request_to_kb_service(
        method="POST",
        endpoint="/documents/upload",
        files=files,
        form_data=form_data,
        user_data=current_user
    )

@router.put("/documents/{document_id}")
async def update_document(
    document_id: str,
    document_data: Dict[str, Any],
    current_user: dict = Depends(get_instructor_user)
):
    """Actualizar documento."""
    return await forward_request_to_kb_service(
        method="PUT",
        endpoint=f"/documents/{document_id}",
        json_data=document_data,
        user_data=current_user
    )

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: dict = Depends(get_instructor_user)
):
    """Eliminar documento."""
    return await forward_request_to_kb_service(
        method="DELETE",
        endpoint=f"/documents/{document_id}",
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE BÚSQUEDA Y CONSULTA
# =============================================================================

@router.post("/search")
async def search_knowledge_base(
    search_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Buscar en la base de conocimiento."""
    return await forward_request_to_kb_service(
        method="POST",
        endpoint="/search",
        json_data=search_data,
        user_data=current_user
    )

@router.post("/query")
async def query_knowledge_base(
    query_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Consultar la base de conocimiento con procesamiento avanzado."""
    return await forward_request_to_kb_service(
        method="POST",
        endpoint="/query",
        json_data=query_data,
        user_data=current_user
    )

@router.get("/categories")
async def get_categories(
    current_user: dict = Depends(get_current_user)
):
    """Obtener categorías disponibles."""
    return await forward_request_to_kb_service(
        method="GET",
        endpoint="/categories",
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE PROCESAMIENTO DE PDF
# =============================================================================

@router.post("/upload-pdf")
async def upload_pdf_document(
    file: UploadFile = File(..., description="Archivo PDF a procesar"),
    content_type: Optional[str] = None,
    category: Optional[str] = None,
    target_audience: Optional[str] = "all",
    auto_categorize: bool = True,
    create_chunks: bool = True,
    current_user: dict = Depends(get_instructor_user)
):
    """
    Subir y procesar un documento PDF.
    
    - Requiere permisos de instructor o superior
    - Procesa automáticamente el PDF y lo agrega a la base de conocimiento
    - Soporta auto-categorización y segmentación inteligente
    """
    try:
        # Preparar datos del formulario
        form_data = {
            "content_type": content_type,
            "category": category,
            "target_audience": target_audience,
            "auto_categorize": str(auto_categorize).lower(),
            "create_chunks": str(create_chunks).lower()
        }
        
        # Preparar archivo
        file_content = await file.read()
        files = {
            "file": (file.filename, file_content, file.content_type)
        }
        
        return await forward_request_to_kb_service(
            method="POST",
            endpoint="/api/v1/pdf/upload-pdf",
            user_data=current_user,
            form_data=form_data,
            files=files
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando PDF: {str(e)}"
        )

@router.post("/batch-upload-pdf")
async def batch_upload_pdf_documents(
    files: List[UploadFile] = File(..., description="Lista de archivos PDF"),
    content_type: Optional[str] = None,
    category: Optional[str] = None,
    target_audience: Optional[str] = "all",
    auto_categorize: bool = True,
    current_user: dict = Depends(get_instructor_user)
):
    """
    Subir y procesar múltiples documentos PDF en lote.
    
    - Requiere permisos de instructor o superior
    - Procesa cada PDF individualmente
    - Retorna resultados por archivo
    """
    try:
        # Validar número de archivos
        if len(files) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Máximo 10 archivos por lote"
            )
        
        # Preparar datos del formulario
        form_data = {
            "content_type": content_type,
            "category": category,
            "target_audience": target_audience,
            "auto_categorize": str(auto_categorize).lower()
        }
        
        # Preparar archivos
        files_data = {}
        for i, file in enumerate(files):
            file_content = await file.read()
            files_data[f"files_{i}"] = (file.filename, file_content, file.content_type)
        
        return await forward_request_to_kb_service(
            method="POST",
            endpoint="/api/v1/pdf/batch-upload-pdf",
            user_data=current_user,
            form_data=form_data,
            files=files_data
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando PDFs en lote: {str(e)}"
        )

@router.get("/pdf-processing-status/{task_id}")
async def get_pdf_processing_status(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener estado de procesamiento de un PDF.
    
    - Útil para procesos largos o en background
    """
    return await forward_request_to_kb_service(
        method="GET",
        endpoint=f"/api/v1/pdf/processing-status/{task_id}",
        user_data=current_user
    )

# =============================================================================
# ENDPOINTS DE ADMINISTRACIÓN
# =============================================================================

@router.post("/reindex")
async def reindex_knowledge_base(
    current_user: dict = Depends(get_admin_user)
):
    """Reindexar la base de conocimiento (solo admins)."""
    return await forward_request_to_kb_service(
        method="POST",
        endpoint="/reindex",
        user_data=current_user
    )

@router.get("/stats")
async def get_knowledge_base_stats(
    current_user: dict = Depends(get_instructor_user)
):
    """Obtener estadísticas de la base de conocimiento."""
    return await forward_request_to_kb_service(
        method="GET",
        endpoint="/stats",
        user_data=current_user
    )
