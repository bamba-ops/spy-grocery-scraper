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
            print(f"Erreur lors de l'insertion du produit : {e}")
            raise

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
            print(f"Erreur lors de la récupération du produit : {e}")
            raise

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
            print(f"Erreur lors de la récupération du produit : {e}")
            raise

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
            print(f"Erreur lors de la mise à jour du produit : {e}")
            raise

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
            print(f"Erreur lors de la suppression du produit : {e}")
            raise

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
            print(f"Erreur lors de la récupération du produit : {e}")
            raise

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
