from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username của user")
    email: EmailStr = Field(..., description="Email của user")


class UserLogin(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                'username': 'admin',
                "email": "admin@mail.com",
                "password": "123456",
            }
        }
    }


class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "123456",
            }
        }
    }


class UserResponse(UserBase):
    id: int = Field(..., description="ID của user")
    is_active: bool = Field(..., description="Trạng thái hoạt động")
    is_superuser: bool = Field(..., description="Quyền superuser")
    created_at: datetime = Field(..., description="Thời gian tạo")
    updated_at: Optional[datetime] = Field(None, description="Thời gian cập nhật")

    # Cho phép tạo model từ ORM object (SQLAlchemy)
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": None
            }
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
