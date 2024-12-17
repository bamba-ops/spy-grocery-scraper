class Price:
    def __init__(self, id=None, created_at=None, product_id=None, store_id=None, price=None, unit=None):
        self.id = id
        self.created_at = created_at
        self.product_id = product_id
        self.store_id = store_id
        self.price = price
        self.unit = unit
    
    def __repr__(self):
        return (f"Price(id={self.id}, product_id={self.product_id}, "
                f"store_id={self.store_id}, price={self.price}, unit={self.unit} created_at={self.created_at})")
