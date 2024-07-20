from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from infraestructure.db import Base

class DeliveryDate(Base):
    __tablename__ = "delivery_dates"

    id = Column(Integer, primary_key=True, index=True)
    period_id = Column(Integer, ForeignKey("period.id"), nullable=False)
    date = Column(Date)

    period = relationship("Period", back_populates="delivery_dates")
