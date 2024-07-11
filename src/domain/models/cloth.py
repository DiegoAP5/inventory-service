import uuid
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Cloth(Base):
    __tablename__ = 'cloth'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(CHAR(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    type = Column(String(255))
    image = Column(String(255))
    buy = Column(Float)
    price = Column(Float)
    sellPrice = Column(Float)
    location = Column(String(255))
    description = Column(String(255))
    size = Column(String(255))
    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship("Status")
    created_at = Column(Date, default=datetime.utcnow)
    sold_at = Column(Date, nullable=True)
