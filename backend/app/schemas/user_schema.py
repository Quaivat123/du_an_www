# backend/app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    message: str

    class Config:
        orm_mode = True
