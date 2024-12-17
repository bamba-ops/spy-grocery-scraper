from supabase import create_client, Client
import os
from dotenv import load_dotenv

class SupabaseConnection:
    """
    Classe responsable de l'initialisation et de la gestion de la connexion à Supabase.
    """
    _instance = None  # Singleton pour éviter de créer plusieurs connexions

    @staticmethod
    def create_connection() -> Client:
        """
        Crée une connexion à Supabase ou retourne l'instance existante.
        """
        if SupabaseConnection._instance is None:
            try:
                # Charger les variables d'environnement
                load_dotenv()

                # Récupérer les variables nécessaires
                supabase_url = os.getenv("SUPABASE_URL")
                supabase_key = os.getenv("SUPABASE_KEY")

                if not supabase_url or not supabase_key:
                    raise ValueError("Les variables SUPABASE_URL et SUPABASE_KEY sont requises dans .env")

                # Créer la connexion à Supabase
                SupabaseConnection._instance = create_client(supabase_url, supabase_key)
                print("Connexion à Supabase réussie.")
            except Exception as e:
                print(f"Erreur lors de la connexion à Supabase : {e}")
                raise

        return SupabaseConnection._instance
