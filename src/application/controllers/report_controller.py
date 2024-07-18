from marshmallow import ValidationError
from domain.models.report import Report
from domain.models.cloth import Cloth
from infraestructure.repositories.report_repository import ReportRepository
from infraestructure.db import SessionLocal
from application.schemas.report_schema import ReportSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus
from sqlalchemy.sql import func

class ReportController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = ReportRepository(self.session)
        self.schema = ReportSchema()

    def create_or_update_report(self, data):
        period_id = data.get("period_id")
        if not period_id:
            return BaseResponse(None, "Period ID is required", False, HTTPStatus.BAD_REQUEST)

        existing_report = self.repo.get_by_period(period_id)
        if existing_report:
            return self.update_report(existing_report)
        else:
            return self.create_report(period_id)

    def create_report(self, period_id):
        total_cloth = self.session.query(func.count()).select_from(Cloth).filter_by(period_id=period_id).scalar()
        cloth_selled = self.session.query(func.count()).select_from(Cloth).filter_by(period_id=period_id, status_id=2).scalar()
        cloth_inSell = self.session.query(func.count()).select_from(Cloth).filter_by(period_id=period_id, status_id=1).scalar()
        invest = self.session.query(func.sum(Cloth.buy)).filter_by(period_id=period_id).scalar() or 0
        earnings = self.session.query(func.sum(Cloth.sellPrice)).filter_by(period_id=period_id).scalar() or 0

        new_report = Report(
            period_id=period_id,
            total_cloth=total_cloth,
            cloth_selled=cloth_selled,
            cloth_inSell=cloth_inSell,
            invest=invest,
            earnings=earnings
        )
        self.repo.add(new_report)
        return BaseResponse(self.to_dict(new_report), "Report created successfully", True, HTTPStatus.CREATED)

    def update_report(self, report):
        report.total_cloth = self.session.query(func.count()).select_from(Cloth).filter_by(period_id=report.period_id).scalar()
        report.cloth_selled = self.session.query(func.count()).select_from(Cloth).filter_by(period_id=report.period_id, status_id=2).scalar()
        report.cloth_inSell = self.session.query(func.count()).select_from(Cloth).filter_by(period_id=report.period_id, status_id=1).scalar()
        report.invest = self.session.query(func.sum(Cloth.buy)).filter_by(period_id=report.period_id).scalar() or 0
        report.earnings = self.session.query(func.sum(Cloth.sellPrice)).filter_by(period_id=report.period_id).scalar() or 0

        self.repo.update(report)
        return BaseResponse(self.to_dict(report), "Report updated successfully", True, HTTPStatus.OK)

    def get_report_by_period(self, period_id):
        report = self.repo.get_by_period(period_id)
        if report:
            return BaseResponse(self.to_dict(report), "Report fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Report not found", False, HTTPStatus.NOT_FOUND)

    def to_dict(self, report: Report):
        return {
            "id": report.id,
            "uuid": report.uuid,
            "period_id": report.period_id,
            "total_cloth": report.total_cloth,
            "cloth_selled": report.cloth_selled,
            "cloth_inSell": report.cloth_inSell,
            "invest": report.invest,
            "earnings": report.earnings
        }
