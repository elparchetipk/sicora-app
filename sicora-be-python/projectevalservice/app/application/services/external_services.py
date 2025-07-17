from typing import Optional
import httpx
from ...config import settings


class UserServiceClient:
    """Client for communicating with User Service"""

    def __init__(self):
        self.base_url = settings.userservice_url
        self.timeout = 30.0

    async def verify_user_exists(self, user_id: str) -> bool:
        """Verify if a user exists in the user service"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/v1/users/{user_id}")
                return response.status_code == 200
        except Exception:
            return False

    async def get_user_info(self, user_id: str) -> Optional[dict]:
        """Get user information from user service"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/v1/users/{user_id}")
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception:
            return None

    async def verify_instructor_role(self, user_id: str) -> bool:
        """Verify if user has instructor role"""
        user_info = await self.get_user_info(user_id)
        if user_info:
            return user_info.get("role") == "instructor"
        return False

    async def get_group_members(self, group_id: str) -> list:
        """Get members of a group"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/groups/{group_id}/members"
                )
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception:
            return []


class ScheduleServiceClient:
    """Client for communicating with Schedule Service"""

    def __init__(self):
        self.base_url = settings.scheduleservice_url
        self.timeout = 30.0

    async def check_instructor_availability(
        self, instructor_id: str, date_time: str
    ) -> bool:
        """Check if instructor is available at specific time"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/availability/{instructor_id}",
                    params={"datetime": date_time},
                )
                return response.status_code == 200 and response.json().get(
                    "available", False
                )
        except Exception:
            return False

    async def schedule_evaluation_session(
        self, evaluation_data: dict
    ) -> Optional[dict]:
        """Schedule an evaluation session in the schedule service"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/evaluations/schedule", json=evaluation_data
                )
                if response.status_code == 201:
                    return response.json()
                return None
        except Exception:
            return None
