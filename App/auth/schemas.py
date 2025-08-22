from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username của user")
    email: EmailStr = Field(..., description="Email của user")
    full_name: Optional[str] = Field(None, max_length=100, description="Tên đầy đủ của user")

class UserCreate(UserBase):
    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe"
            }
        }

class UserResponse(UserBase):
    id: int = Field(..., description="ID của user")
    is_active: bool = Field(..., description="Trạng thái hoạt động")
    is_superuser: bool = Field(..., description="Quyền superuser")
    created_at: datetime = Field(..., description="Thời gian tạo")
    updated_at: Optional[datetime] = Field(None, description="Thời gian cập nhật")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": None
            }
        }
