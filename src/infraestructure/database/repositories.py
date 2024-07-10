from bson.objectid import ObjectId

class StatusRepository:

    def __init__(self, mongo):
        self.collection = mongo.db.status

    def create(self, data):
        return self.collection.insert_one(data)

    def get_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def update(self, id, data):
        return self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    def delete(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})

class ClothRepository:

    def __init__(self, mongo):
        self.collection = mongo.db.cloth

    def create(self, data):
        return self.collection.insert_one(data)

    def get_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def update(self, id, data):
        return self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    def delete(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})

    def find_by_type(self, cloth_type):
        return self.collection.find({"type": cloth_type})

    def find_by_status(self, status):
        return self.collection.find({"status": status})

class PeriodRepository:

    def __init__(self, mongo):
        self.collection = mongo.db.period

    def create(self, data):
        return self.collection.insert_one(data)

    def get_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def update(self, id, data):
        return self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    def delete(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})

    def get_cloth_count(self, period_id):
        return self.collection.count_documents({"cloth_uuid": period_id})

    def get_cloth_list(self, period_id):
        return self.collection.find({"cloth_uuid": period_id})
