from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    APPRENTICE = "APPRENTICE"
    INSTRUCTOR = "INSTRUCTOR"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    ADMIN = "ADMIN"

class User(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    document_number: str
    document_type: str
    role: UserRole
    is_active: bool
    must_change_password: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None
