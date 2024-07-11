from sqlalchemy.orm import Session
from domain.models.cloth import Cloth

class ClothRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, cloth: Cloth):
        self.session.add(cloth)
        self.session.commit()
    
    def get_by_uuid(self, uuid: str) -> Cloth:
        return self.session.query(Cloth).filter_by(uuid=uuid).first()
    
    def get_all(self):
        return self.session.query(Cloth).all()
    
    def update(self, cloth: Cloth):
        self.session.commit()
    
    def delete(self, uuid: str):
        cloth = self.get_by_uuid(uuid)
        if cloth:
            self.session.delete(cloth)
            self.session.commit()
    
    def search_by_type(self, type: str):
        return self.session.query(Cloth).filter_by(type=type).all()
    
    def list_by_status(self, status: str):
        return self.session.query(Cloth).filter_by(status=status).all()
