import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import CHAR
from .base import Base

class Status(Base):
    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(CHAR(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    status = Column(String(255))
