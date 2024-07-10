from infraestructure.database.repositories import ClothRepository

class ClothService:
    def __init__(self, cloth_repo):
        self.cloth_repo = cloth_repo

    def create(self, data):
        return self.cloth_repo.create(data)

    def get_by_id(self, id):
        return self.cloth_repo.get_by_id(id)

    def update(self, id, data):
        return self.cloth_repo.update(id, data)

    def delete(self, id):
        return self.cloth_repo.delete(id)

    def find_by_type(self, cloth_type):
        return self.cloth_repo.find_by_type(cloth_type)

    def find_by_status(self, status):
        return self.cloth_repo.find_by_status(status)
