from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    document_number: str
    document_type: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None
