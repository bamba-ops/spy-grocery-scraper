class Product:
    def __init__(self, id=None, created_at=None, name=None, image_url=None, brand=None, unit=None):
        self.id = id
        self.created_at = created_at
        self.name = name
        self.image_url = image_url
        self.brand = brand
        self.unit = unit
    
    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, image_url={self.image_url}, brand={self.brand}, created_at={self.created_at})"
