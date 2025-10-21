# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    message = Column(Text)
