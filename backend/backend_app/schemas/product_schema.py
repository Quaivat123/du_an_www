from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    short_desc: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True   # ✅ Thay cho orm_mode trong Pydantic v2
