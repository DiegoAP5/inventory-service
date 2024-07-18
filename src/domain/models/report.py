from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from infraestructure.db import Base

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    period_id = Column(Integer, ForeignKey('period.id'), nullable=False)
    total_cloth = Column(Integer, nullable=False)
    cloth_selled = Column(Integer, nullable=False)
    cloth_inSell = Column(Integer, nullable=False)
    invest = Column(Integer, nullable=False)
    earnings = Column(Integer, nullable=False)

    period = relationship("Period", back_populates="reports")
