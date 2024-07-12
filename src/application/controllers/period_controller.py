from sqlalchemy.orm import Session
from domain.models.period import Period
from infraestructure.repositories.period_repository import PeriodRepository
from infraestructure.db import SessionLocal

class PeriodController:
    def __init__(self):
        self.session: Session = SessionLocal()
        self.repo = PeriodRepository(self.session)

    def create_period(self, data):
        new_period = Period(**data)
        self.repo.add(new_period)
        return new_period

    def get_period(self, uuid):
        return self.repo.get_by_uuid(uuid)

    def get_all_periods(self):
        return self.repo.get_all()

    def update_period(self, uuid, data):
        period = self.repo.get_by_uuid(uuid)
        if period:
            for key, value in data.items():
                setattr(period, key, value)
            self.repo.update(period)
            return period
        return None

    def delete_period(self, uuid):
        self.repo.delete(uuid)
    
    def to_dict(self, period: Period):
        return {
            "id": period.id,
            "uuid": period.uuid,
            "start": period.start,
            "end": period.end,
            "status": period.status,
            "cloth_uuid": period.cloth_uuid
        }
