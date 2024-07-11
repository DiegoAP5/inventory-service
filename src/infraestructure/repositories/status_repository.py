from sqlalchemy.orm import Session
from domain.models.status import Status

class StatusRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, status: Status):
        self.session.add(status)
        self.session.commit()
    
    def get_by_uuid(self, uuid: str) -> Status:
        return self.session.query(Status).filter_by(uuid=uuid).first()
    
    def get_all(self):
        return self.session.query(Status).all()
    
    def update(self, status: Status):
        self.session.commit()
    
    def delete(self, uuid: str):
        status = self.get_by_uuid(uuid)
        if status:
            self.session.delete(status)
            self.session.commit()
