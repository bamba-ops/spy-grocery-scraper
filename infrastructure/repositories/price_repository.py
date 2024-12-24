class PriceRepository:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def create_price(self, price_data: dict):
        """
        Insère un nouveau prix dans la table 'prices'.
        """
        try:
            response = self.supabase.table("prices").insert(price_data).execute()
            if response.data:
                print("Prix inséré avec succès :", response.data)
                return response.data[0]
            else:
                print("Erreur d'insertion :", response.errors)
        except Exception as e:
            print(f"Erreur lors de l'insertion du prix : {e}")
            raise

    def get_prices_by_product_id(self, product_id: str):
        """
        Récupère les prix associés à un produit spécifique.
        """
        try:
            response = self.supabase.table("prices").select("*").eq("product_id", product_id).execute()
            return response.data
        except Exception as e:
            print(f"Erreur lors de la récupération des prix : {e}")
            raise
    
    def update_price(self, product_id: str, store_id: str, price_data: dict):
        """
        Met à jour un prix existant dans la table 'prices'.
        """
        try:
            response = self.supabase.table("prices") \
                .update(price_data) \
                .eq("product_id", product_id) \
                .eq("store_id", store_id) \
                .execute()
            if response.data:
                print("Prix mis à jour avec succès :", response.data)
                return response.data[0]
            else:
                print("Erreur lors de la mise à jour :", response.errors)
        except Exception as e:
            print(f"Erreur lors de la mise à jour du prix : {e}")
            raise
