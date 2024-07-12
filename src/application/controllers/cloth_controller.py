from sqlalchemy.orm import Session
from domain.models.cloth import Cloth
from infraestructure.repositories.cloth_repository import ClothRepository
from infraestructure.db import SessionLocal

class ClothController:
    def __init__(self):
        self.session: Session = SessionLocal()
        self.repo = ClothRepository(self.session)

    def create_cloth(self, data):
        new_cloth = Cloth(**data)
        self.repo.add(new_cloth)
        return new_cloth

    def get_cloth(self, uuid):
        return self.repo.get_by_uuid(uuid)

    def get_all_clothes(self):
        return self.repo.get_all()

    def update_cloth(self, uuid, data):
        cloth = self.repo.get_by_uuid(uuid)
        if cloth:
            for key, value in data.items():
                setattr(cloth, key, value)
            self.repo.update(cloth)
            return cloth
        return None

    def delete_cloth(self, uuid):
        self.repo.delete(uuid)

    def search_cloth_by_type(self, type):
        return self.repo.search_by_type(type)

    def list_cloth_by_status(self, status_id):
        return self.repo.list_by_status(status_id)
    
    def to_dict(self, cloth: Cloth):
        return {
            "id": cloth.id,
            "uuid": cloth.uuid,
            "type": cloth.type,
            "image": cloth.image,
            "buy": cloth.buy,
            "price": cloth.price,
            "sellPrice": cloth.sellPrice,
            "location": cloth.location,
            "description": cloth.description,
            "size": cloth.size,
            "status_id": cloth.status_id,
            "created_at": cloth.created_at,
            "sold_at": cloth.sold_at
        }
