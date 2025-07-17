"""
Models Router
Router para endpoints de gestión de modelos de IA
"""
from fastapi import APIRouter, HTTPException, Depends, status, Query, Path
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.dependencies import get_ai_model_use_case
from app.application.use_cases.ai_model_use_cases import AIModelManagementUseCase
from app.application.dtos.ai_dtos import (
    AIModelCreateDTO,
    AIModelUpdateDTO,
    AIModelResponseDTO
)
from app.presentation.schemas.model_schemas import (
    AIModelCreate,
    AIModelUpdate,
    AIModelResponse,
    ModelTestRequest,
    ModelTestResponse,
    ModelListQuery,
    ModelListResponse,
    ModelUsageStats,
    ModelAvailabilityCheck,
    ModelAvailabilityResponse
)

router = APIRouter()

@router.get(
    "/",
    response_model=List[AIModelResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar modelos de IA disponibles",
    description="Obtiene una lista de todos los modelos de IA disponibles con filtros opcionales."
)
async def list_models(
    model_type: Optional[str] = Query(None, description="Filtrar por tipo de modelo"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filtrar por estado del modelo"),
    feature: Optional[str] = Query(None, description="Filtrar por característica soportada"),
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Listar modelos de IA disponibles con filtros opcionales."""
    try:
        models = await ai_model_use_case.list_ai_models(
            model_type=model_type,
            status=status_filter,
            feature=feature
        )

        # Convertir DTOs a esquemas de respuesta
        return [
            AIModelResponse(
                id=model.model_id,
                name=model.name,
                model_name=model.model_name,
                provider=model.model_type,
                model_type="chat",  # Asumimos chat por defecto, ajustar según necesidad
                description=model.metadata.get("description", ""),
                max_tokens=model.max_tokens,
                context_window=model.context_window,
                cost_per_token=model.cost_per_token,
                capabilities=model.supported_features,
                config={
                    "temperature": model.temperature,
                    "top_p": model.top_p,
                    "frequency_penalty": model.frequency_penalty,
                    "presence_penalty": model.presence_penalty
                },
                status=model.status,
                is_default=model.metadata.get("is_default", False),
                usage_count=model.metadata.get("usage_count", 0),
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar modelos: {str(e)}"
        )

@router.post(
    "/",
    response_model=AIModelResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo modelo de IA",
    description="Crea un nuevo modelo de IA con la configuración especificada."
)
async def create_model(
    model_data: AIModelCreate,
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Crear un nuevo modelo de IA."""
    try:
        # Convertir esquema a DTO
        model_dto = AIModelCreateDTO(
            name=model_data.name,
            model_type=model_data.provider,
            model_name=model_data.model_name,
            api_endpoint=model_data.config.get("api_endpoint") if model_data.config else None,
            api_key_name=model_data.config.get("api_key_name") if model_data.config else None,
            max_tokens=model_data.max_tokens,
            temperature=model_data.config.get("temperature", 0.7) if model_data.config else 0.7,
            context_window=model_data.context_window,
            cost_per_token=model_data.cost_per_token or 0.0,
            supported_features=model_data.capabilities,
            metadata={
                "description": model_data.description,
                "is_default": model_data.is_default,
                "model_type_specific": model_data.model_type
            }
        )

        # Crear modelo
        created_model = await ai_model_use_case.create_ai_model(model_dto)

        # Convertir DTO a esquema de respuesta
        return AIModelResponse(
            id=created_model.model_id,
            name=created_model.name,
            model_name=created_model.model_name,
            provider=created_model.model_type,
            model_type=model_data.model_type,  # Usamos el valor original
            description=model_data.description,
            max_tokens=created_model.max_tokens,
            context_window=created_model.context_window,
            cost_per_token=created_model.cost_per_token,
            capabilities=created_model.supported_features,
            config={
                "temperature": created_model.temperature,
                "top_p": created_model.top_p,
                "frequency_penalty": created_model.frequency_penalty,
                "presence_penalty": created_model.presence_penalty
            },
            status=created_model.status,
            is_default=model_data.is_default,
            usage_count=0,
            created_at=created_model.created_at,
            updated_at=created_model.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear modelo: {str(e)}"
        )

@router.get(
    "/{model_id}",
    response_model=AIModelResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener información de un modelo específico",
    description="Obtiene información detallada de un modelo de IA específico."
)
async def get_model(
    model_id: UUID = Path(..., description="ID del modelo a consultar"),
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Obtener información de un modelo específico."""
    try:
        model = await ai_model_use_case.get_ai_model(model_id)

        # Extraer información del modelo
        model_type = model.metadata.get("model_type_specific", "chat")
        description = model.metadata.get("description", "")
        is_default = model.metadata.get("is_default", False)
        usage_count = model.metadata.get("usage_count", 0)

        # Convertir DTO a esquema de respuesta
        return AIModelResponse(
            id=model.model_id,
            name=model.name,
            model_name=model.model_name,
            provider=model.model_type,
            model_type=model_type,
            description=description,
            max_tokens=model.max_tokens,
            context_window=model.context_window,
            cost_per_token=model.cost_per_token,
            capabilities=model.supported_features,
            config={
                "temperature": model.temperature,
                "top_p": model.top_p,
                "frequency_penalty": model.frequency_penalty,
                "presence_penalty": model.presence_penalty
            },
            status=model.status,
            is_default=is_default,
            usage_count=usage_count,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Modelo no encontrado: {str(e)}"
        )

@router.put(
    "/{model_id}",
    response_model=AIModelResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un modelo de IA",
    description="Actualiza la configuración de un modelo de IA existente."
)
async def update_model(
    model_id: UUID = Path(..., description="ID del modelo a actualizar"),
    model_data: AIModelUpdate = ...,
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Actualizar un modelo de IA."""
    try:
        # Preparar metadata para actualización
        metadata = {}
        if model_data.description is not None:
            metadata["description"] = model_data.description
        if model_data.is_default is not None:
            metadata["is_default"] = model_data.is_default

        # Convertir esquema a DTO
        update_dto = AIModelUpdateDTO(
            name=model_data.name,
            max_tokens=model_data.max_tokens,
            temperature=model_data.config.get("temperature") if model_data.config else None,
            context_window=model_data.context_window,
            cost_per_token=model_data.cost_per_token,
            status=model_data.status.value if model_data.status else None,
            supported_features=model_data.capabilities,
            metadata=metadata if metadata else None
        )

        # Actualizar modelo
        updated_model = await ai_model_use_case.update_ai_model(model_id, update_dto)

        # Extraer información del modelo
        model_type = updated_model.metadata.get("model_type_specific", "chat")
        description = updated_model.metadata.get("description", "")
        is_default = updated_model.metadata.get("is_default", False)
        usage_count = updated_model.metadata.get("usage_count", 0)

        # Convertir DTO a esquema de respuesta
        return AIModelResponse(
            id=updated_model.model_id,
            name=updated_model.name,
            model_name=updated_model.model_name,
            provider=updated_model.model_type,
            model_type=model_type,
            description=description,
            max_tokens=updated_model.max_tokens,
            context_window=updated_model.context_window,
            cost_per_token=updated_model.cost_per_token,
            capabilities=updated_model.supported_features,
            config={
                "temperature": updated_model.temperature,
                "top_p": updated_model.top_p,
                "frequency_penalty": updated_model.frequency_penalty,
                "presence_penalty": updated_model.presence_penalty
            },
            status=updated_model.status,
            is_default=is_default,
            usage_count=usage_count,
            created_at=updated_model.created_at,
            updated_at=updated_model.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar modelo: {str(e)}"
        )

@router.delete(
    "/{model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un modelo de IA",
    description="Elimina un modelo de IA existente."
)
async def delete_model(
    model_id: UUID = Path(..., description="ID del modelo a eliminar"),
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Eliminar un modelo de IA."""
    try:
        success = await ai_model_use_case.delete_ai_model(model_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Modelo no encontrado o no se pudo eliminar"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar modelo: {str(e)}"
        )

@router.post(
    "/{model_id}/test",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Probar un modelo de IA",
    description="Prueba la disponibilidad y funcionamiento de un modelo de IA."
)
async def test_model(
    model_id: UUID = Path(..., description="ID del modelo a probar"),
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Probar un modelo de IA."""
    try:
        result = await ai_model_use_case.test_model_availability(model_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al probar modelo: {str(e)}"
        )

@router.get(
    "/statistics",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Obtener estadísticas de modelos",
    description="Obtiene estadísticas de uso de los modelos de IA."
)
async def get_model_statistics(
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Obtener estadísticas de uso de modelos."""
    try:
        stats = await ai_model_use_case.get_model_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

@router.get(
    "/available",
    response_model=List[AIModelResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener modelos disponibles",
    description="Obtiene una lista de todos los modelos de IA disponibles y operativos."
)
async def get_available_models(
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Obtener modelos disponibles y operativos."""
    try:
        models = await ai_model_use_case.get_available_models()

        # Convertir DTOs a esquemas de respuesta
        return [
            AIModelResponse(
                id=model.model_id,
                name=model.name,
                model_name=model.model_name,
                provider=model.model_type,
                model_type=model.metadata.get("model_type_specific", "chat"),
                description=model.metadata.get("description", ""),
                max_tokens=model.max_tokens,
                context_window=model.context_window,
                cost_per_token=model.cost_per_token,
                capabilities=model.supported_features,
                config={
                    "temperature": model.temperature,
                    "top_p": model.top_p,
                    "frequency_penalty": model.frequency_penalty,
                    "presence_penalty": model.presence_penalty
                },
                status=model.status,
                is_default=model.metadata.get("is_default", False),
                usage_count=model.metadata.get("usage_count", 0),
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener modelos disponibles: {str(e)}"
        )

@router.get(
    "/by-name/{name}",
    response_model=AIModelResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener modelo por nombre",
    description="Obtiene información detallada de un modelo de IA por su nombre."
)
async def get_model_by_name(
    name: str = Path(..., description="Nombre del modelo a consultar"),
    ai_model_use_case: AIModelManagementUseCase = Depends(get_ai_model_use_case)
):
    """Obtener información de un modelo por su nombre."""
    try:
        model = await ai_model_use_case.get_ai_model_by_name(name)

        # Extraer información del modelo
        model_type = model.metadata.get("model_type_specific", "chat")
        description = model.metadata.get("description", "")
        is_default = model.metadata.get("is_default", False)
        usage_count = model.metadata.get("usage_count", 0)

        # Convertir DTO a esquema de respuesta
        return AIModelResponse(
            id=model.model_id,
            name=model.name,
            model_name=model.model_name,
            provider=model.model_type,
            model_type=model_type,
            description=description,
            max_tokens=model.max_tokens,
            context_window=model.context_window,
            cost_per_token=model.cost_per_token,
            capabilities=model.supported_features,
            config={
                "temperature": model.temperature,
                "top_p": model.top_p,
                "frequency_penalty": model.frequency_penalty,
                "presence_penalty": model.presence_penalty
            },
            status=model.status,
            is_default=is_default,
            usage_count=usage_count,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Modelo no encontrado: {str(e)}"
        )
