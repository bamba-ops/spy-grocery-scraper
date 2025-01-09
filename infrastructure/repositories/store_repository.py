from fastapi import HTTPException


class StoreRepository:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def get_store_by_name(self, name: str):
        """
        Récupère un magasin par son nom.
        """
        try:
            response = (
                self.supabase.table("stores").select("*").eq("name", name).execute()
            )
            if response.data:
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération du magasin par son nom : {e}",
            )

    def create_store(self, store_data: dict):
        """
        Insère un nouveau magasin dans la table 'stores'.
        """
        try:
            response = self.supabase.table("stores").insert(store_data).execute()
            if response.data:
                print("Magasin inséré avec succès :", response.data)
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la création du magasin : {e}"
            )
