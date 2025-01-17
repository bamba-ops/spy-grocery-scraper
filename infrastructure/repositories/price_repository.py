from fastapi import HTTPException


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
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de l'insertion du prix : {e}"
            )

    def get_prices_by_product_id(self, product_id: str):
        """
        Récupère les prix associés à un produit spécifique.
        """
        try:
            response = (
                self.supabase.table("prices")
                .select("*")
                .eq("product_id", product_id)
                .execute()
            )
            if response.data:
                return response.data
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la récupération du prix : {e}"
            )

    def update_price(self, product_id: str, store_id: str, price_data: dict):
        """
        Met à jour un prix existant dans la table 'prices'.
        """
        try:
            response = (
                self.supabase.table("prices")
                .update(price_data)
                .eq("product_id", product_id)
                .eq("store_id", store_id)
                .execute()
            )
            if response.data:
                print("Prix mis à jour avec succès :", response.data)
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la mise à jour du prix : {e}"
            )

    def get_price_by_product_and_store(self, store_id: str, product_id: str):
        try:
            response = (
                self.supabase.table("prices")
                .select("*")
                .eq("store_id", store_id)
                .eq("product_id", product_id)
                .execute()
            )
            if response.data:
                print(
                    "Prix par produit id et magasin id récupéré avec success :",
                    response.data,
                )
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération du prix par le produit et le magasin : {e}",
            )
