from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

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
    name: str = Field(..., min_length=2, max_length=120)
    description: str | None = None
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    stock: int = Field(default=0, ge=0, description="Stock cannot be negative")
    category_id: int = Field(..., gt=0)
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
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: int | None = Field(default=None, gt=0)
    image_url: str | None = None

class CartItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(default=1, gt=0, le=50)
class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True
        orm_mode = True

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str
    payment_method: str = "UPI / ZapPay"

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    delivery_address: str
    payment_method: str
    total_amount: float
    items_summary: str
    status: str

    class Config:
        from_attributes = True
        orm_mode = True