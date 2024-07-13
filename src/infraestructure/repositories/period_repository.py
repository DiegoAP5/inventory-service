from sqlalchemy.orm import Session
from domain.models.period import Period

class PeriodRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, period: Period):
        self.session.add(period)
        self.session.commit()
        self.session.refresh(period)
        return period

    def get_by_uuid(self, uuid):
        return self.session.query(Period).filter(Period.uuid == uuid).first()

    def get_all(self):
        return self.session.query(Period).all()

    def update(self, period: Period):
        self.session.commit()

    def delete(self, uuid):
        period = self.get_by_uuid(uuid)
        if period:
            self.session.delete(period)
            self.session.commit()

    def search_by_status(self, status_id):
        return self.session.query(Period).filter(Period.status_id == status_id).all()
