class ProductRepository:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def create_product(self, product_data: dict):
        """
        Insère un nouveau produit dans la table 'products'.
        """
        try:
            response = self.supabase.table("products").insert(product_data).execute()
            if response.data:
                print("Produit inséré avec succès :", response.data)
                return response.data[0]
            else:
                print("Erreur d'insertion :", response.errors)
        except Exception as e:
            print(f"Erreur lors de l'insertion du produit : {e}")
            raise

    def get_product_by_name(self, name: str):
        """
        Récupère un produit par son nom.
        """
        try:
            response = self.supabase.table("products").select("*").eq("name", name).execute()
            if response.data:
                return response.data[0]
            else:
                print(f"Produit '{name}' non trouvé.")
        except Exception as e:
            print(f"Erreur lors de la récupération du produit : {e}")
            raise

    def update_product_by_name(self, name: str, updates: dict):
        """
        Met à jour un produit existant en utilisant son nom.
        """
        try:
            response = self.supabase.table("products").update(updates).eq("name", name).execute()
            print("Produit mis à jour :", response.data)
            return response.data
        except Exception as e:
            print(f"Erreur lors de la mise à jour du produit : {e}")
            raise

    def delete_product_by_name(self, name: str):
        """
        Supprime un produit par son nom.
        """
        try:
            response = self.supabase.table("products").delete().eq("name", name).execute()
            print("Produit supprimé :", response.data)
            return response.data
        except Exception as e:
            print(f"Erreur lors de la suppression du produit : {e}")
            raise
