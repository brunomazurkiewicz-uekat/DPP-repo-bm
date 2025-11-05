from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime
from auth_app.models.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default= datetime.now)
