from sqlalchemy.orm import Session
from domain.models.delivery_date import DeliveryDate

class DeliveryDateRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, delivery_date: DeliveryDate):
        self.session.add(delivery_date)
        self.session.commit()
        self.session.refresh(delivery_date)
        return delivery_date

    def get_by_id(self, delivery_date_id: int):
        return self.session.query(DeliveryDate).filter_by(id=delivery_date_id).first()

    def get_all_by_period(self, period_id: int):
        return self.session.query(DeliveryDate).filter_by(period_id=period_id).all()

    def update(self, delivery_date: DeliveryDate):
        self.session.merge(delivery_date)
        self.session.commit()
        return delivery_date

    def delete(self, delivery_date: DeliveryDate):
        self.session.delete(delivery_date)
        self.session.commit()
