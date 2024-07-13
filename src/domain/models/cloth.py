from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4
import datetime
from infraestructure.db import Base

class Cloth(Base):
    __tablename__ = 'cloth'
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    type = Column(String(36), index=True)
    image = Column(String(255))
    buy = Column(Float)
    price = Column(Float)
    sellPrice = Column(Float)
    location = Column(String(255))
    description = Column(String(255))
    size = Column(String(10))
    status_id = Column(Integer, ForeignKey('status.id'))
    period_id = Column(Integer, ForeignKey('period.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    sold_at = Column(DateTime, nullable=True)
    
    status = relationship("Status", back_populates="clothes")
    period = relationship("Period", back_populates="clothes")
