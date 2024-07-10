from infraestructure.database.repositories import PeriodRepository

class PeriodService:
    def __init__(self, period_repo):
        self.period_repo = period_repo

    def create(self, data):
        return self.period_repo.create(data)

    def get_by_id(self, id):
        return self.period_repo.get_by_id(id)

    def update(self, id, data):
        return self.period_repo.update(id, data)

    def delete(self, id):
        return self.period_repo.delete(id)

    def get_cloth_count(self, period_id):
        return self.period_repo.get_cloth_count(period_id)

    def get_cloth_list(self, period_id):
        return self.period_repo.get_cloth_list(period_id)
