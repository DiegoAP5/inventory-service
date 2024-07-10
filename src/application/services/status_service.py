from infraestructure.database.repositories import StatusRepository

class StatusService:
    def __init__(self, status_repo):
        self.status_repo = status_repo

    def create(self, data):
        return self.status_repo.create(data)

    def get_by_id(self, id):
        return self.status_repo.get_by_id(id)

    def update(self, id, data):
        return self.status_repo.update(id, data)

    def delete(self, id):
        return self.status_repo.delete(id)
