import uuid
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from .base import Base

class Period(Base):
    __tablename__ = 'period'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(CHAR(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    start = Column(Date)
    end = Column(Date)
    status_id = Column(Integer, ForeignKey('status.id'))
    cloth_uuid = Column(CHAR(36), ForeignKey('cloth.uuid'))
    cloth = relationship("Cloth")
