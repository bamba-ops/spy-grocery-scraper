class ManageProducts:
    def __init__(self, product_repo):
        self.product_repo = product_repo

    def create_product(self, product_data: dict):
        """
        Crée un nouveau produit dans la base de données.
        """
        try:
            return self.product_repo.create_product(product_data)
        except Exception as e:
            print(f"Erreur lors de la création du produit : {e}")

    def get_product_by_name(self, name: str):
        """
        Récupère un produit par son nom.
        """
        try:
            return self.product_repo.get_product_by_name(name)
        except Exception as e:
            print(f"Erreur lors de la récupération du produit : {e}")

    def update_product(self, name: str, updates: dict):
        """
        Met à jour un produit par son nom.
        """
        try:
            return self.product_repo.update_product_by_name(name, updates)
        except Exception as e:
            print(f"Erreur lors de la mise à jour du produit : {e}")

    def delete_product(self, name: str):
        """
        Supprime un produit par son nom.
        """
        try:
            return self.product_repo.delete_product_by_name(name)
        except Exception as e:
            print(f"Erreur lors de la suppression du produit : {e}")
