from sqlalchemy.orm import Session
from domain.models.report import Report

class ReportRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, report: Report):
        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        return report

    def get_by_uuid(self, uuid: str):
        return self.session.query(Report).filter_by(uuid=uuid).first()

    def update(self, report: Report):
        self.session.commit()
        self.session.refresh(report)
        return report

    def delete(self, report: Report):
        self.session.delete(report)
        self.session.commit()

    def get_all(self):
        return self.session.query(Report).all()

    def get_by_period_id(self, period_id: int):
        return self.session.query(Report).filter_by(period_id=period_id).all()
