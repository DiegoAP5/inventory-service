from datetime import datetime

def create_collections(db):
    if 'status' not in db.list_collection_names():
        db.create_collection('status')
    if 'cloth' not in db.list_collection_names():
        db.create_collection('cloth')
    if 'period' not in db.list_collection_names():
        db.create_collection('period')

def status_model(data):
    return {
        "uuid": data.get("uuid"),
        "status": data.get("status"),
        "created_at": datetime.utcnow()
    }

def cloth_model(data):
    return {
        "uuid": data.get("uuid"),
        "type": data.get("type"),
        "image": data.get("image"),
        "buy": data.get("buy"),
        "price": data.get("price"),
        "sellPrice": data.get("sellPrice"),
        "location": data.get("location"),
        "description": data.get("description"),
        "size": data.get("size"),
        "status": data.get("status"),
        "created_at": datetime.utcnow(),
        "sold_at": None
    }

def period_model(data):
    return {
        "uuid": data.get("uuid"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "status": data.get("status"),
        "cloth_uuid": data.get("cloth_uuid")
    }
