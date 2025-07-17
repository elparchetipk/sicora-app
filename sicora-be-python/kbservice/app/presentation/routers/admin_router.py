"""Admin router for Knowledge Base Service administration endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from app.presentation.schemas.kb_schemas import (
    AdminMetricsResponse,
    AdminConfigResponse,
    AdminConfigRequest,
    HealthCheckResponse
)
from app.dependencies import (
    get_current_user,
    get_query_analytics_service
)
from app.infrastructure.services.kb_services_impl import QueryAnalyticsService

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse)
async def admin_health_check():
    """Health check endpoint for admin."""
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        service="kbservice-admin",
        version="1.0.0"
    )

@router.get("/metrics", response_model=AdminMetricsResponse)
async def get_admin_metrics(
    current_user: Dict[str, Any] = Depends(get_current_user),
    analytics_service: QueryAnalyticsService = Depends(get_query_analytics_service)
):
    """Get administration metrics."""
    # Basic implementation - can be enhanced later
    try:
        return AdminMetricsResponse(
            period="daily",
            total_queries=0,
            average_response_time=0.0,
            search_accuracy=0.0,
            error_rate=0.0,
            user_satisfaction=0.0,
            resource_usage={},
            timestamp=datetime.now(timezone.utc)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics: {str(e)}"
        )
