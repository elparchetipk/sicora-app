from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from fastapi.responses import StreamingResponse
import io

from app.domain.exceptions.evaluation_exceptions import EvaluationNotFoundError
from app.domain.exceptions.period_exceptions import EvaluationPeriodNotFoundError
from app.presentation.dependencies.auth import get_current_user, require_role, CurrentUser
from app.presentation.dependencies.container import (
    get_generate_instructor_report_use_case,
    get_generate_period_report_use_case,
    get_export_report_to_csv_use_case
)
from app.presentation.schemas.report_schemas import (
    InstructorReportSchema,
    PeriodReportSchema,
    ExportRequestSchema
)

from app.application.use_cases.generate_instructor_report_use_case import GenerateInstructorReportUseCase
from app.application.use_cases.generate_period_report_use_case import GeneratePeriodReportUseCase
from app.application.use_cases.export_report_to_csv_use_case import ExportReportToCSVUseCase

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={404: {"description": "Not found"}}
)

@router.get("/instructor/{instructor_id}", response_model=InstructorReportSchema)
async def get_instructor_report(
    instructor_id: UUID,
    period_id: UUID = Query(..., description="Evaluation period ID"),
    current_user: CurrentUser = Depends(get_current_user),
    use_case: GenerateInstructorReportUseCase = Depends(get_generate_instructor_report_use_case)
):
    """
    Generar reporte de evaluaciones para un instructor específico en un período.
    Los administradores y coordinadores pueden generar reportes de cualquier instructor.
    Los instructores solo pueden generar sus propios reportes.
    """
    if current_user.role == "instructor" and instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only view your own evaluation reports"
        )
    elif current_user.role not in ["admin", "coordinator", "instructor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Insufficient permissions to view reports"
        )
    
    try:
        report = use_case.execute(instructor_id, period_id)
        
        return InstructorReportSchema(
            instructor_id=report.instructor_id,
            period_id=report.period_id,
            total_evaluations=report.total_evaluations,
            average_rating=report.average_rating,
            response_rate=report.response_rate,
            question_averages=report.question_averages,
            strengths=report.strengths,
            improvement_areas=report.improvement_areas,
            generated_at=report.generated_at
        )
    
    except EvaluationPeriodNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation period not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/period/{period_id}", response_model=PeriodReportSchema)
async def get_period_report(
    period_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: GeneratePeriodReportUseCase = Depends(get_generate_period_report_use_case)
):
    """
    Generar reporte general de un período de evaluación.
    Solo los administradores y coordinadores pueden generar estos reportes.
    """
    require_role(current_user, ["admin", "coordinator"])
    
    try:
        report = use_case.execute(period_id)
        
        return PeriodReportSchema(
            period_id=report.period_id,
            total_instructors=report.total_instructors,
            total_evaluations=report.total_evaluations,
            completion_rate=report.completion_rate,
            average_rating=report.average_rating,
            instructor_rankings=report.instructor_rankings,
            question_analysis=report.question_analysis,
            department_summary=report.department_summary,
            generated_at=report.generated_at
        )
    
    except EvaluationPeriodNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation period not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/export/csv")
async def export_evaluations_csv(
    export_request: ExportRequestSchema,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: ExportReportToCSVUseCase = Depends(get_export_report_to_csv_use_case)
):
    """
    Exportar evaluaciones a formato CSV.
    Solo los administradores y coordinadores pueden exportar datos.
    """
    require_role(current_user, ["admin", "coordinator"])
    
    try:
        csv_content = use_case.execute(
            period_id=export_request.period_id,
            instructor_id=export_request.instructor_id,
            export_format="csv",
            include_responses=export_request.include_responses,
            include_comments=export_request.include_comments
        )
        
        # Crear un buffer de memoria con el contenido CSV
        output = io.StringIO()
        output.write(csv_content)
        output.seek(0)
        
        # Preparar el nombre del archivo
        filename = f"evaluations_export_{export_request.period_id}"
        if export_request.instructor_id:
            filename += f"_instructor_{export_request.instructor_id}"
        filename += ".csv"
        
        # Crear la respuesta streaming
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
        return response
    
    except EvaluationPeriodNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation period not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/export/excel")
async def export_evaluations_excel(
    export_request: ExportRequestSchema,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: ExportReportToCSVUseCase = Depends(get_export_report_to_csv_use_case)
):
    """
    Exportar evaluaciones a formato Excel.
    Solo los administradores y coordinadores pueden exportar datos.
    """
    require_role(current_user, ["admin", "coordinator"])
    
    try:
        excel_content = use_case.execute(
            period_id=export_request.period_id,
            instructor_id=export_request.instructor_id,
            export_format="excel",
            include_responses=export_request.include_responses,
            include_comments=export_request.include_comments
        )
        
        # Crear un buffer de memoria con el contenido Excel
        output = io.BytesIO()
        output.write(excel_content)
        output.seek(0)
        
        # Preparar el nombre del archivo
        filename = f"evaluations_export_{export_request.period_id}"
        if export_request.instructor_id:
            filename += f"_instructor_{export_request.instructor_id}"
        filename += ".xlsx"
        
        # Crear la respuesta streaming
        response = StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
        return response
    
    except EvaluationPeriodNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation period not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/analytics/instructor/{instructor_id}/trends")
async def get_instructor_trends(
    instructor_id: UUID,
    start_period: UUID = Query(..., description="Start evaluation period ID"),
    end_period: UUID = Query(..., description="End evaluation period ID"),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Obtener tendencias de evaluación para un instructor a lo largo de múltiples períodos.
    Los administradores y coordinadores pueden ver tendencias de cualquier instructor.
    Los instructores solo pueden ver sus propias tendencias.
    """
    if current_user.role == "instructor" and instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only view your own evaluation trends"
        )
    elif current_user.role not in ["admin", "coordinator", "instructor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Insufficient permissions to view trends"
        )
    
    try:
        # TODO: Implement instructor trends analytics
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Instructor trends analytics not implemented yet"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/analytics/period/{period_id}/dashboard")
async def get_period_dashboard(
    period_id: UUID,
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Obtener datos para dashboard de un período de evaluación.
    Solo los administradores y coordinadores pueden acceder al dashboard.
    """
    require_role(current_user, ["admin", "coordinator"])
    
    try:
        # TODO: Implement period dashboard analytics
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Period dashboard analytics not implemented yet"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/analytics/comparative")
async def get_comparative_analysis(
    period_ids: List[UUID] = Query(..., description="List of evaluation period IDs to compare"),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Obtener análisis comparativo entre múltiples períodos de evaluación.
    Solo los administradores y coordinadores pueden realizar análisis comparativos.
    """
    require_role(current_user, ["admin", "coordinator"])
    
    if len(period_ids) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least two periods are required for comparative analysis"
        )
    
    if len(period_ids) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 10 periods allowed for comparative analysis"
        )
    
    try:
        # TODO: Implement comparative analysis
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Comparative analysis not implemented yet"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
