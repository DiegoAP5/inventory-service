# src/application/controllers/report_controller.py
from marshmallow import ValidationError
from domain.models.report import Report
from infraestructure.repositories.report_repository import ReportRepository
from infraestructure.db import SessionLocal
from application.schemas.report_schema import ReportSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus
from sqlalchemy import func
from domain.models.cloth import Cloth

class ReportController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = ReportRepository(self.session)
        self.schema = ReportSchema()

    def create_report(self, data):
        try:
            validated_data = self.schema.load(data)
            period_id = validated_data['period_id']

            total_cloth = self.session.query(func.count(Cloth.id)).filter_by(period_id=period_id).scalar()
            cloth_selled = self.session.query(func.count(Cloth.id)).filter_by(period_id=period_id, status_id=2).scalar()  # Assuming 2 is the status_id for "selled"
            cloth_inSell = self.session.query(func.count(Cloth.id)).filter_by(period_id=period_id, status_id=1).scalar()  # Assuming 1 is the status_id for "in sell"
            invest = self.session.query(func.sum(Cloth.buy)).filter_by(period_id=period_id).scalar()
            earnings = self.session.query(func.sum(Cloth.sellPrice)).filter_by(period_id=period_id).scalar()

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
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)

    def update_report(self, uuid, data):
        report = self.repo.get_by_uuid(uuid)
        if report:
            try:
                validated_data = self.schema.load(data, partial=True)
                for key, value in validated_data.items():
                    setattr(report, key, value)
                self.repo.update(report)
                return BaseResponse(self.to_dict(report), "Report updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Report not found", False, HTTPStatus.NOT_FOUND)

    def get_report(self, uuid):
        report = self.repo.get_by_uuid(uuid)
        if report:
            return BaseResponse(self.to_dict(report), "Report fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Report not found", False, HTTPStatus.NOT_FOUND)

    def delete_report(self, uuid):
        report = self.repo.get_by_uuid(uuid)
        if report:
            self.repo.delete(report)
            return BaseResponse(None, "Report deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Report not found", False, HTTPStatus.NOT_FOUND)

    def list_reports(self):
        reports = self.repo.get_all()
        return BaseResponse([self.to_dict(report) for report in reports], "Reports fetched successfully", True, HTTPStatus.OK)

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
