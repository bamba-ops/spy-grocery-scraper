from fastapi import HTTPException


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
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de l'insértion du produit : {e}"
            )

    def get_product_by_name(self, name: str):
        """
        Récupère un produit par son nom.
        """
        try:
            response = (
                self.supabase.table("products").select("*").eq("name", name).execute()
            )
            if response.data:
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération du produit par son nom : {e}",
            )

    def get_product_by_name_and_store_id(self, name: str, store_id: str):
        """
        Récupère un produit par son nom.
        """
        try:
            response = (
                self.supabase.table("products")
                .select("*")
                .eq("name", name)
                .eq("store_id", store_id)
                .execute()
            )
            if response.data:
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération du produit par son nom : {e}",
            )

    def get_product_by_image_url(self, image_url: str):

        try:
            response = (
                self.supabase.table("products")
                .select("*")
                .eq("image_url", image_url)
                .execute()
            )
            if response.data:
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération du produit par son image url : {e}",
            )

    def update_product_by_name(self, name: str, updates: dict):
        """
        Met à jour un produit existant en utilisant son nom.
        """
        try:
            response = (
                self.supabase.table("products")
                .update(updates)
                .eq("name", name)
                .execute()
            )
            if response.data:
                print("Produit mis à jour :", response.data)
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la mise à jour du produit par son nom : {e}",
            )

    def delete_product_by_name(self, name: str):
        """
        Supprime un produit par son nom.
        """
        try:
            response = (
                self.supabase.table("products").delete().eq("name", name).execute()
            )
            if response.data:
                print("Produit supprimé :", response.data)
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la suppréssion du produit par son nom : {e}",
            )

    def get_product_by_name_by_store_id(self, name: str, store_id: str):
        """
        Supprime un produit par son nom.
        """
        try:
            response = (
                self.supabase.table("products")
                .select("*")
                .eq("name", name)
                .eq("store_id", store_id)
                .execute()
            )
            if response.data:
                print("Produit supprimé :", response.data)
                return response.data[0]
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la suppréssion du produit par son nom : {e}",
            )

    def get_product_by_reference_id(self, reference_id: str):
        """
        Récupère un produit par son nom.
        """
        try:
            response = (
                self.supabase.table("products")
                .select("*")
                .eq("reference_id", reference_id)
                .execute()
            )
            if response.data:
                return response.data
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération du produit par son reference id : {e}",
            )

    def get_product_by_reference_id_and_store_id(
        self, reference_id: str, store_id: str
    ):
        try:
            response = (
                self.supabase.table("products")
                .select("*")
                .eq("reference_id", reference_id)
                .eq("store_id", store_id)
                .execute()
            )
            if response.data:
                return response.data
            return []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la récupération du produit par son reference id : {e}",
            )

    def lowercase_dict_values(self, data):
        """
        Cette fonction met en minuscule les valeurs des clés spécifiques ('name' et 'brand')
        dans un dictionnaire, y compris les dictionnaires et listes imbriqués.

        :param data: dict | Le dictionnaire à traiter.
        :return: dict | Le dictionnaire avec les valeurs des clés spécifiques en minuscules.
        """
        if isinstance(data, dict):
            return {
                key: (
                    self.lowercase_dict_values(value)
                    if key in ["name", "brand"]
                    else value
                )
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self.lowercase_dict_values(item) for item in data]
        elif isinstance(data, str):
            return data.lower()
        else:
            return data

    def is_name_exist(self, product_name, store_id):
        try:
            response = self.get_product_by_name_and_store_id(product_name, store_id)
            if response:
                return True
            else:
                return False
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la vérification si le nom existe du produit : {e}",
            )
