# backend/backend_app/models/user_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from backend.backend_app.database import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    phone_number = Column(String(10),nullable = False)
    created_at = Column(DateTime, server_default=func.now())
