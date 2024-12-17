class Store:
    def __init__(self, id=None, created_at=None, name=None):
        self.id = id
        self.created_at = created_at
        self.name = name

    def __repr__(self):
        return f"Store(id={self.id}, name={self.name}, created_at={self.created_at})"
