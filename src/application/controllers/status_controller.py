from sqlalchemy.orm import Session
from domain.models.status import Status
from infraestructure.repositories.status_repository import StatusRepository
from infraestructure.database import SessionLocal

class StatusController:
    def __init__(self):
        self.session: Session = SessionLocal()
        self.repo = StatusRepository(self.session)

    def create_status(self, data):
        new_status = Status(**data)
        self.repo.add(new_status)
        return new_status

    def get_status(self, uuid):
        return self.repo.get_by_uuid(uuid)

    def get_all_statuses(self):
        return self.repo.get_all()

    def update_status(self, uuid, data):
        status = self.repo.get_by_uuid(uuid)
        if status:
            for key, value in data.items():
                setattr(status, key, value)
            self.repo.update(status)
            return status
        return None

    def delete_status(self, uuid):
        self.repo.delete(uuid)

    def to_dict(self, status: Status):
        return {
            "id": status.id,
            "uuid": status.uuid,
            "status": status.status
        }
