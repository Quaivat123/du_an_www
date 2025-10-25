# backend/backend_app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Optional
from typing import Annotated
from datetime import datetime

# Tạo type riêng cho số điện thoại
PhoneNumber = Annotated[str, StringConstraints(pattern=r'^\d{10}$')]

class ContactBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneNumber] = None
    message: Optional[str] = None

class ContactCreate(ContactBase):
    pass
class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneNumber] = None
    message: Optional[str] = None

class ContactOut(ContactBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
