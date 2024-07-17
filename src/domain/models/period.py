from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from infraestructure.db import Base

class Period(Base):
    __tablename__ = 'period'
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    start = Column(Date)
    end = Column(Date)
    status_id = Column(Integer, ForeignKey('status.id'))
    
    reports = relationship("Report", back_populates="period", cascade="all, delete-orphan")
    status = relationship("Status", back_populates="periods")
    clothes = relationship("Cloth", back_populates="period", cascade="all, delete-orphan")
