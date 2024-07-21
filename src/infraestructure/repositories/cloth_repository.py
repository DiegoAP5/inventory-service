from sqlalchemy.orm import Session
from domain.models.cloth import Cloth
from domain.models.period import Period
from sqlalchemy.orm import joinedload

class ClothRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, cloth: Cloth):
        self.session.add(cloth)
        self.session.commit()
        self.session.refresh(cloth)
        return cloth

    def get_by_uuid(self, id):
        return self.session.query(Cloth).filter(Cloth.id == id).first()

    def get_all(self):
        return self.session.query(Cloth).all()

    def update(self, cloth: Cloth):
        self.session.commit()

    def delete(self, id):
        cloth = self.get_by_uuid(id)
        if cloth:
            self.session.delete(cloth)
            self.session.commit()

    def search_by_type_and_period(self, type, period_id):
        return self.session.query(Cloth).filter(Cloth.type == type, Cloth.period_id == period_id).all()
    
    def get_all_by_status_and_type(self, type, status_id):
        return self.session.query(Cloth).filter(Cloth.type == type, Cloth.status_id == status_id).all()

    def get_all_by_status(self, status_id):
        return self.session.query(Cloth).filter(Cloth.status_id == status_id).all()
    
    def get_all_by_period(self, period_id):
        return self.session.query(Cloth).filter(Cloth.period_id == period_id).all()
    
    def get_cloth_and_user_id(self, cloth_id):
        return self.session.query(Cloth, Period.user_id).join(Period).filter(Cloth.id == cloth_id).first()
    
    def get_to_statics(self, user_id):
        return self.session.query(Cloth).join(Period).filter(Period.user_id == user_id).options(joinedload(Cloth.period)).all()

    def list_by_status_and_period(self, status_id, period_id):
        return self.session.query(Cloth).filter(Cloth.status_id == status_id, Cloth.period_id == period_id).all()
