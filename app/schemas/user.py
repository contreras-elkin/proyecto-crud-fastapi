from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from decimal import Decimal
from app.enums.enums_user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, description="La contraseña debe tener al menos 6 caracteres")
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    user_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=1, max_length=20)
    monthly_budget: Decimal = Field(default=Decimal("0.00"), ge=0)
    role: UserRole = Field(default=UserRole.USER)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6)
    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    user_name: str | None = Field(None, min_length=1, max_length=100)
    phone: str | None = Field(None, min_length=1, max_length=20)
    monthly_budget: Decimal | None = Field(None, ge=0)
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    user_name: str
    phone: str
    monthly_budget: Decimal
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
