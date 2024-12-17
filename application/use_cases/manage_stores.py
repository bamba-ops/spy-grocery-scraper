class ManageStores:
    def __init__(self, store_repo):
        self.store_repo = store_repo

    def get_store_by_name(self, name: str):
        """
        Récupère un magasin par son nom.
        """
        try:
            store = self.store_repo.get_store_by_name(name)
            if store:
                print(f"Magasin trouvé : {store}")
                return store
            else:
                print(f"Magasin '{name}' non trouvé.")
                return None
        except Exception as e:
            print(f"Erreur lors de la récupération du magasin : {e}")
    
    def create_store(self, store_data: dict):
        """
        Crée un nouveau magasin dans la base de données.
        """
        try:
            return self.store_repo.create_store(store_data)
        except Exception as e:
            print(f"Erreur lors de la création du magasin : {e}")
