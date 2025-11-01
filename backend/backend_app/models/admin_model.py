from sqlalchemy import Column, Integer, String
from backend.backend_app.database import Base
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # lưu hash