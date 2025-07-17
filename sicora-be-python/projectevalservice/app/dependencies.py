from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .infrastructure.database import get_async_db
from .application.services import UserServiceClient, ScheduleServiceClient


# Global service instances
user_service = UserServiceClient()
schedule_service = ScheduleServiceClient()


async def get_user_service() -> UserServiceClient:
    """Dependency for getting user service client"""
    return user_service


async def get_schedule_service() -> ScheduleServiceClient:
    """Dependency for getting schedule service client"""
    return schedule_service


async def get_current_user_id() -> str:
    """
    Dependency for getting current user ID from JWT token
    This is a placeholder - implement with actual JWT validation
    """
    # TODO: Implement JWT token validation
    # For now, return a dummy user ID
    return "123e4567-e89b-12d3-a456-426614174000"


async def get_current_instructor_id() -> str:
    """
    Dependency for getting current instructor ID
    Validates that current user is an instructor
    """
    user_id = await get_current_user_id()

    # TODO: Validate instructor role with user service
    # user_info = await user_service.get_user_info(user_id)
    # if not user_info or user_info.get("role") != "instructor":
    #     raise HTTPException(status_code=403, detail="Instructor access required")

    return user_id
