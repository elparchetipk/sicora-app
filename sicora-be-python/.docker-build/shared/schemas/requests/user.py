from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    document_number: str
    document_type: str
    role: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    document_number: str
    document_type: str
    role: str
    is_active: bool
