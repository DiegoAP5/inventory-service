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

    def get_by_period(self, period_id: int):
        return self.session.query(Report).filter_by(period_id=period_id).first()

    def update(self, report: Report):
        self.session.merge(report)
        self.session.commit()
        return report
