class Cloth:
    def __init__(self, uuid, type, image, buy, price, sell_price, location, description, size, status, created_at, sold_at=None):
        self.uuid = uuid
        self.type = type
        self.image = image
        self.buy = buy
        self.price = price
        self.sell_price = sell_price
        self.location = location
        self.description = description
        self.size = size
        self.status = status
        self.created_at = created_at
        self.sold_at = sold_at
