from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="CUSTOMER", pattern="^(CUSTOMER|ADMIN)$")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        orm_mode = True
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    category_id: int
    image_url: str | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int
    category_id: int
    image_url: str | None = None

    class Config:
        from_attributes = True
        orm_mode = True

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    category_id: int | None = None
    image_url: str | None = None