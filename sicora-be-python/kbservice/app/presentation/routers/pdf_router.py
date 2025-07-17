"""Router para procesamiento de documentos PDF en KBService."""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi import status as http_status

from app.dependencies import get_current_user, get_kb_use_cases
from app.infrastructure.pdf_processing import pdf_upload_handler, PDFProcessingError
from app.presentation.schemas.kb_schemas import KnowledgeItemResponse
from app.domain.entities.kb_entities import ContentType, TargetAudience, ContentStatus
from app.application.use_cases.kb_use_cases import CreateKnowledgeItemUseCase
from app.application.dtos.kb_dtos import KnowledgeItemCreateDTO
import uuid
from datetime import datetime

router = APIRouter()


@router.post("/upload-pdf", response_model=KnowledgeItemResponse)
async def upload_pdf_document(
    file: UploadFile = File(..., description="Archivo PDF a procesar"),
    content_type: Optional[ContentType] = Form(
        None, description="Tipo de contenido"
    ),
    category: Optional[str] = Form(
        None, description="Categoría del documento"
    ),
    target_audience: Optional[TargetAudience] = Form(
        TargetAudience.ALL, description="Audiencia objetivo"
    ),
    auto_categorize: bool = Form(
        True, description="Auto-categorizar basado en contenido"
    ),
    create_chunks: bool = Form(
        True, description="Crear chunks para documentos largos"
    ),
    current_user: Dict[str, Any] = Depends(get_current_user),
    create_use_case: CreateKnowledgeItemUseCase = Depends(
        lambda: None  # TODO: Implementar dependency real
    )
):
    """
    Subir y procesar un documento PDF.
    
    El endpoint:
    1. Valida el archivo PDF
    2. Extrae el texto usando múltiples métodos
    3. Auto-categoriza el contenido (opcional)
    4. Limpia y procesa el texto
    5. Crea el item en la base de conocimiento
    6. Opcionalmente crea chunks para documentos largos
    """
    try:
        # Validar usuario
        user_role = current_user.get("role", "").lower()
        if user_role not in ["admin", "instructor", "coordinador"]:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Solo administradores e instructores pueden subir docs"
            )
        
        # Procesar PDF
        result = await pdf_upload_handler.handle_upload(
            file=file,
            content_type=content_type.value if content_type else None,
            category=category,
            target_audience=target_audience.value if target_audience else "all"
        )
        
        if result.get("processing_status") != "success":
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail=f"Error procesando PDF: {result.get('error_message')}"
            )
        
        # TODO: Crear item real en la base de conocimiento
        # cuando tengamos el dependency injection configurado
        # dto = KnowledgeItemCreateDTO(
        #     title=result["title"],
        #     content=result["content"],
        #     content_type=result["content_type"],
        #     category=result["category"],
        #     target_audience=result["target_audience"],
        #     tags=result.get("tags", []),
        #     metadata=result["metadata"]
        # )
        # knowledge_item = await create_use_case.execute(
        #     dto, UUID(current_user["id"])
        # )
        
        # Por ahora, retornar información del procesamiento
        processed_content = result["content"]
        if len(processed_content) > 500:
            display_content = processed_content[:500] + "..."
        else:
            display_content = processed_content
            
        return {
            "id": "temp-id",  # TODO: ID real del item creado
            "title": result["title"],
            "content": display_content,
            "content_type": result["content_type"],
            "category": result["category"],
            "target_audience": result["target_audience"],
            "status": "published",
            "metadata": result["metadata"],
            "created_at": result["metadata"]["processed_at"],
            "updated_at": result["metadata"]["processed_at"]
        }
        
    except PDFProcessingError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno procesando PDF: {str(e)}"
        )


@router.post("/batch-upload-pdf")
async def batch_upload_pdf_documents(
    files: List[UploadFile] = File(..., description="Lista de archivos PDF"),
    content_type: Optional[ContentType] = Form(None, description="Tipo de contenido para todos"),
    category: Optional[str] = Form(None, description="Categoría para todos"),
    target_audience: Optional[TargetAudience] = Form(TargetAudience.ALL, description="Audiencia objetivo"),
    auto_categorize: bool = Form(True, description="Auto-categorizar cada documento"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Subir y procesar múltiples documentos PDF en batch.
    
    Procesa cada PDF individualmente y retorna un resumen
    de los resultados exitosos y fallidos.
    """
    try:
        # Validar usuario
        user_role = current_user.get("role", "").lower()
        if user_role not in ["admin", "instructor", "coordinador"]:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Solo administradores e instructores pueden subir documentos"
            )
        
        # Validar número de archivos
        if len(files) > 10:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Máximo 10 archivos por batch"
            )
        
        results = {
            "successful": [],
            "failed": [],
            "total_processed": len(files)
        }
        
        for file in files:
            try:
                result = await pdf_upload_handler.handle_upload(
                    file=file,
                    content_type=content_type.value if content_type else None,
                    category=category,
                    target_audience=target_audience.value if target_audience else "all"
                )
                
                if result.get("processing_status") == "success":
                    results["successful"].append({
                        "filename": file.filename,
                        "title": result["title"],
                        "content_type": result["content_type"],
                        "category": result["category"],
                        "text_length": result["metadata"]["text_length"],
                        "pages": result["metadata"]["pages"]
                    })
                else:
                    results["failed"].append({
                        "filename": file.filename,
                        "error": result.get("error_message", "Error desconocido")
                    })
                    
            except Exception as e:
                results["failed"].append({
                    "filename": file.filename,
                    "error": str(e)
                })
        
        return {
            "message": f"Procesamiento completado: {len(results['successful'])} exitosos, {len(results['failed'])} fallidos",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en procesamiento batch: {str(e)}"
        )


@router.get("/pdf-processing-info")
async def get_pdf_processing_info():
    """Obtener información sobre las capacidades de procesamiento de PDF."""
    return {
        "supported_formats": ["PDF"],
        "supported_mime_types": [
            "application/pdf",
            "application/x-pdf",
            "application/x-bzpdf",
            "application/x-gzpdf"
        ],
        "extraction_methods": [
            {
                "name": "pdfplumber",
                "description": "Mejor para documentos con tablas y layout complejo",
                "best_for": ["tablas", "formularios", "layout estructurado"]
            },
            {
                "name": "pymupdf",
                "description": "Excelente para documentos con formato complejo",
                "best_for": ["documentos oficiales", "layout complejo", "metadatos"]
            },
            {
                "name": "pypdf2",
                "description": "Método básico y confiable",
                "best_for": ["documentos simples", "texto plano"]
            },
            {
                "name": "ocr",
                "description": "Para documentos escaneados (requiere configuración)",
                "best_for": ["documentos escaneados", "imágenes con texto"]
            }
        ],
        "auto_categorization": {
            "enabled": True,
            "rules": {
                "policy": ["reglamento", "norma", "política", "decreto"],
                "procedure": ["procedimiento", "proceso", "instrucciones"],
                "guide": ["tutorial", "guía", "manual", "como"],
                "faq": ["pregunta", "faq", "consulta"]
            }
        },
        "text_processing": {
            "cleaning": "Automática",
            "segmentation": "Automática para documentos > 2000 caracteres",
            "language_detection": "Automática (español por defecto)",
            "max_file_size": "50MB",
            "batch_limit": 10
        }
    }
