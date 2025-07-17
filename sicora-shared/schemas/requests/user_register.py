from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID
from typing import List, Optional
import re


class UserRegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    document_number: str = Field(...,
                                 min_length=5,
                                 max_length=15,
                                 pattern=r"^\d+$")
    document_type: str = Field(..., min_length=1, max_length=2)
    password: str = Field(..., min_length=10)
    previous_passwords: Optional[
        List[str]] = None  # Lista de hashes de contraseñas anteriores

    @field_validator('password')
    def password_strong(cls, v, values):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Debe contener al menos una mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("Debe contener al menos una minúscula")
        if not re.search(r"\d", v):
            raise ValueError("Debe contener al menos un dígito")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Debe contener al menos un símbolo")
        for field in ['first_name', 'last_name', 'email']:
            if field in values.data and values.data[field].lower() in v.lower(
            ):
                raise ValueError(
                    "La contraseña no debe contener datos personales")
        prev = values.data.get('previous_passwords')
        if prev and v in prev[-5:]:
            raise ValueError("No se permite reusar las últimas 5 contraseñas")
        return v


class BulkUserItem(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    document_number: str
    document_type: str
    role: str


class BulkUserRegisterRequest(BaseModel):
    users: List[BulkUserItem]


class UserRegisterResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    document_number: str
    document_type: str
    role: str
    is_active: bool
    must_change_password: bool


class BulkUserRegisterResponse(BaseModel):
    created: int
    errors: Optional[List[str]] = None
    users: Optional[List[UserRegisterResponse]] = None
