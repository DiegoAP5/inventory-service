# src/domain/models/report.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    period_id = Column(Integer, ForeignKey('periods.id'), nullable=False)
    total_cloth = Column(Integer, nullable=False, default=0)
    cloth_selled = Column(Integer, nullable=False, default=0)
    cloth_inSell = Column(Integer, nullable=False, default=0)
    invest = Column(Float, nullable=False, default=0.0)
    earnings = Column(Float, nullable=False, default=0.0)

    period = relationship("Period", back_populates="report")