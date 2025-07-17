from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

class UserSchema(BaseModel):
    """Esquema para representar un usuario en el sistema."""
    
    id: UUID = Field(..., description="ID único del usuario")
    username: str = Field(..., description="Nombre de usuario")
    email: str = Field(..., description="Correo electrónico del usuario")
    first_name: str = Field(..., description="Nombre del usuario")
    last_name: str = Field(..., description="Apellido del usuario")
    role: str = Field(..., description="Rol del usuario en el sistema")
    is_active: bool = Field(default=True, description="Si el usuario está activo")
    department_id: Optional[UUID] = Field(None, description="ID del departamento del usuario")
    
    class Config:
        from_attributes = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }

class UserCreateSchema(BaseModel):
    """Esquema para crear un nuevo usuario."""
    
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    email: str = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., min_length=8, description="Contraseña del usuario")
    first_name: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")
    last_name: str = Field(..., min_length=1, max_length=100, description="Apellido del usuario")
    role: str = Field(..., description="Rol del usuario en el sistema")
    department_id: Optional[UUID] = Field(None, description="ID del departamento del usuario")

class UserUpdateSchema(BaseModel):
    """Esquema para actualizar un usuario existente."""
    
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre de usuario")
    email: Optional[str] = Field(None, description="Correo electrónico del usuario")
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del usuario")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Apellido del usuario")
    role: Optional[str] = Field(None, description="Rol del usuario en el sistema")
    is_active: Optional[bool] = Field(None, description="Si el usuario está activo")
    department_id: Optional[UUID] = Field(None, description="ID del departamento del usuario")

class UserLoginSchema(BaseModel):
    """Esquema para login de usuario."""
    
    username: str = Field(..., description="Nombre de usuario o email")
    password: str = Field(..., description="Contraseña del usuario")

class UserTokenSchema(BaseModel):
    """Esquema para token de autenticación."""
    
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")
    user: UserSchema = Field(..., description="Información del usuario")

class UserProfileSchema(BaseModel):
    """Esquema para perfil público del usuario."""
    
    id: UUID = Field(..., description="ID único del usuario")
    username: str = Field(..., description="Nombre de usuario")
    first_name: str = Field(..., description="Nombre del usuario")
    last_name: str = Field(..., description="Apellido del usuario")
    role: str = Field(..., description="Rol del usuario en el sistema")
    department_id: Optional[UUID] = Field(None, description="ID del departamento del usuario")
    
    class Config:
        from_attributes = True
        json_encoders = {
            UUID: str
        }
