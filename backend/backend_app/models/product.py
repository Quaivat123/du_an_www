from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, UTC
from backend.backend_app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    short_desc = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)  # ví dụ: "banhang", "doanhnghiep"
    created_at = Column(DateTime, default=datetime.now(UTC))
