"""Dependency injection configuration for AttendanceService."""

from functools import lru_cache
from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from uuid import UUID

from .config import settings
from .infrastructure.auth import get_user_id_from_token

# Database setup
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO
)

async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

# Repository imports
from .infrastructure.repositories import (
    SQLAlchemyAttendanceRecordRepository,
    SQLAlchemyJustificationRepository,
    SQLAlchemyAttendanceAlertRepository
)

# Service imports
from .infrastructure.adapters import (
    LocalFileUploadService,
    InMemoryQRCodeService,
    HTTPUserServiceAdapter,
    HTTPScheduleServiceAdapter
)

# Interface imports
from .domain.repositories import (
    AttendanceRecordRepository,
    JustificationRepository,
    AttendanceAlertRepository
)
from .application.interfaces import (
    FileUploadService,
    QRCodeService,
    UserServiceInterface,
    ScheduleServiceInterface
)

# Use case imports
from .application.use_cases import (
    RegisterAttendanceUseCase,
    GetAttendanceSummaryUseCase,
    GetAttendanceHistoryUseCase,
    UploadJustificationUseCase,
    ReviewJustificationUseCase,
    GetJustificationsUseCase,
    DeleteJustificationUseCase,
    GetAttendanceAlertsUseCase,
    GetInstructorNoAttendanceAlertsUseCase,
    AcknowledgeAlertUseCase
)


async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


# Repository dependencies
async def get_attendance_record_repository(
    db: AsyncSession = Depends(get_database)
) -> AttendanceRecordRepository:
    """Get attendance record repository instance."""
    return SQLAlchemyAttendanceRecordRepository(db)


async def get_justification_repository(
    db: AsyncSession = Depends(get_database)
) -> JustificationRepository:
    """Get justification repository instance."""
    return SQLAlchemyJustificationRepository(db)


async def get_attendance_alert_repository(
    db: AsyncSession = Depends(get_database)
) -> AttendanceAlertRepository:
    """Get attendance alert repository instance."""
    return SQLAlchemyAttendanceAlertRepository(db)


# Service dependencies
@lru_cache()
def get_file_upload_service() -> FileUploadService:
    """Get file upload service instance."""
    return LocalFileUploadService(settings.UPLOAD_DIRECTORY)


@lru_cache()
def get_qr_code_service() -> QRCodeService:
    """Get QR code service instance."""
    return InMemoryQRCodeService(
        secret_key=settings.QR_CODE_SECRET,
        refresh_seconds=settings.QR_CODE_REFRESH_SECONDS
    )


@lru_cache()
def get_user_service() -> UserServiceInterface:
    """Get user service instance."""
    return HTTPUserServiceAdapter(
        base_url=settings.USER_SERVICE_URL,
        timeout=30
    )


@lru_cache()
def get_schedule_service() -> ScheduleServiceInterface:
    """Get schedule service instance."""
    return HTTPScheduleServiceAdapter(
        base_url=settings.SCHEDULE_SERVICE_URL,
        timeout=30
    )


# Use case dependencies
async def get_register_attendance_use_case(
    attendance_repo: AttendanceRecordRepository = Depends(get_attendance_record_repository),
    user_service: UserServiceInterface = Depends(get_user_service),
    schedule_service: ScheduleServiceInterface = Depends(get_schedule_service),
    qr_service: QRCodeService = Depends(get_qr_code_service)
) -> RegisterAttendanceUseCase:
    """Get register attendance use case instance."""
    return RegisterAttendanceUseCase(
        attendance_repo, qr_service, user_service, schedule_service
    )


async def get_attendance_summary_use_case(
    attendance_repo: AttendanceRecordRepository = Depends(get_attendance_record_repository),
    user_service: UserServiceInterface = Depends(get_user_service)
) -> GetAttendanceSummaryUseCase:
    """Get attendance summary use case instance."""
    return GetAttendanceSummaryUseCase(attendance_repo, user_service)


async def get_attendance_history_use_case(
    attendance_repo: AttendanceRecordRepository = Depends(get_attendance_record_repository),
    user_service: UserServiceInterface = Depends(get_user_service)
) -> GetAttendanceHistoryUseCase:
    """Get attendance history use case instance."""
    return GetAttendanceHistoryUseCase(attendance_repo, user_service)


async def get_upload_justification_use_case(
    justification_repo: JustificationRepository = Depends(get_justification_repository),
    attendance_repo: AttendanceRecordRepository = Depends(get_attendance_record_repository),
    user_service: UserServiceInterface = Depends(get_user_service),
    file_service: FileUploadService = Depends(get_file_upload_service)
) -> UploadJustificationUseCase:
    """Get upload justification use case instance."""
    return UploadJustificationUseCase(justification_repo, attendance_repo, user_service, file_service)


async def get_review_justification_use_case(
    justification_repo: JustificationRepository = Depends(get_justification_repository),
    attendance_repo: AttendanceRecordRepository = Depends(get_attendance_record_repository),
    user_service: UserServiceInterface = Depends(get_user_service)
) -> ReviewJustificationUseCase:
    """Get review justification use case instance."""
    return ReviewJustificationUseCase(justification_repo, attendance_repo, user_service)


async def get_justifications_use_case(
    justification_repo: JustificationRepository = Depends(get_justification_repository),
    user_service: UserServiceInterface = Depends(get_user_service)
) -> GetJustificationsUseCase:
    """Get justifications use case instance."""
    return GetJustificationsUseCase(justification_repo, user_service)


async def get_delete_justification_use_case(
    justification_repo: JustificationRepository = Depends(get_justification_repository),
    user_service: UserServiceInterface = Depends(get_user_service)
) -> DeleteJustificationUseCase:
    """Get delete justification use case instance."""
    return DeleteJustificationUseCase(justification_repo, user_service)


async def get_attendance_alerts_use_case(
    alert_repo: AttendanceAlertRepository = Depends(get_attendance_alert_repository),
    user_service: UserServiceInterface = Depends(get_user_service)
) -> GetAttendanceAlertsUseCase:
    """Get attendance alerts use case instance."""
    return GetAttendanceAlertsUseCase(alert_repo, user_service)


async def get_instructor_no_attendance_alerts_use_case(
    alert_repo: AttendanceAlertRepository = Depends(get_attendance_alert_repository),
    attendance_repo: AttendanceRecordRepository = Depends(get_attendance_record_repository),
    user_service: UserServiceInterface = Depends(get_user_service),
    schedule_service: ScheduleServiceInterface = Depends(get_schedule_service)
) -> GetInstructorNoAttendanceAlertsUseCase:
    """Get instructor no attendance alerts use case instance."""
    return GetInstructorNoAttendanceAlertsUseCase(alert_repo, attendance_repo, user_service, schedule_service)


async def get_acknowledge_alert_use_case(
    alert_repo: AttendanceAlertRepository = Depends(get_attendance_alert_repository),
    user_service: UserServiceInterface = Depends(get_user_service)
) -> AcknowledgeAlertUseCase:
    """Get acknowledge alert use case instance."""
    return AcknowledgeAlertUseCase(alert_repo, user_service)


# Type aliases for dependency injection
AttendanceRecordRepositoryDep = Annotated[AttendanceRecordRepository, Depends(get_attendance_record_repository)]
JustificationRepositoryDep = Annotated[JustificationRepository, Depends(get_justification_repository)]
AttendanceAlertRepositoryDep = Annotated[AttendanceAlertRepository, Depends(get_attendance_alert_repository)]

FileUploadService = Annotated[FileUploadService, Depends(get_file_upload_service)]
QRCodeService = Annotated[QRCodeService, Depends(get_qr_code_service)]
UserService = Annotated[UserServiceInterface, Depends(get_user_service)]
ScheduleService = Annotated[ScheduleServiceInterface, Depends(get_schedule_service)]

# Authentication dependency
CurrentUser = Annotated[UUID, Depends(get_user_id_from_token)]

RegisterAttendanceUseCaseDep = Annotated[RegisterAttendanceUseCase, Depends(get_register_attendance_use_case)]
GetAttendanceSummaryUseCaseDep = Annotated[GetAttendanceSummaryUseCase, Depends(get_attendance_summary_use_case)]
GetAttendanceHistoryUseCaseDep = Annotated[GetAttendanceHistoryUseCase, Depends(get_attendance_history_use_case)]
UploadJustificationUseCaseDep = Annotated[UploadJustificationUseCase, Depends(get_upload_justification_use_case)]
ReviewJustificationUseCaseDep = Annotated[ReviewJustificationUseCase, Depends(get_review_justification_use_case)]
GetJustificationsUseCaseDep = Annotated[GetJustificationsUseCase, Depends(get_justifications_use_case)]
DeleteJustificationUseCaseDep = Annotated[DeleteJustificationUseCase, Depends(get_delete_justification_use_case)]
GetAttendanceAlertsUseCaseDep = Annotated[GetAttendanceAlertsUseCase, Depends(get_attendance_alerts_use_case)]
GetInstructorNoAttendanceAlertsUseCaseDep = Annotated[GetInstructorNoAttendanceAlertsUseCase, Depends(get_instructor_no_attendance_alerts_use_case)]
AcknowledgeAlertUseCaseDep = Annotated[AcknowledgeAlertUseCase, Depends(get_acknowledge_alert_use_case)]
# def get_register_attendance_use_case(
#     repository: AttendanceRepositoryInterface = Depends(get_attendance_repository)
# ) -> RegisterAttendanceUseCase:
#     """Get register attendance use case instance."""
#     return RegisterAttendanceUseCase(repository)
