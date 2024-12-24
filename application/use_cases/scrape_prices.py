class ScrapePrices:
    def __init__(self, product_repo, store_repo, price_repo, scraper):
        self.product_repo = product_repo
        self.store_repo = store_repo
        self.price_repo = price_repo
        self.scraper = scraper

    def execute(self, product_name: str, store_name: str):
        """
        Orchestration du scraping et sauvegarde des informations.
        """
        try:
            # Récupération du magasin
            store = self.store_repo.get_store_by_name(store_name)
            if not store:
                raise ValueError(f"Magasin '{store_name}' introuvable.")

            # Scraping des données
            scraped_data = self.scraper.scrape_metro(product_name)
            print(f"Scraping terminé. Produits récupérés : {len(scraped_data)}")

            # Enregistrement des données dans la base de données
            for data in scraped_data:
                product = self.product_repo.get_product_by_name(data["name"])
                if product:
                    self.product_repo.update_product_by_name(data["name"],{
                        "name": data["name"],
                        "image_url": data["image_url"],
                        "brand": data["brand"],
                        "unit": data["unit"]
                    })
                else:
                    product = self.product_repo.create_product({
                        "name": data["name"],
                        "image_url": data["image_url"],
                        "brand": data["brand"],
                        "unit": data["unit"]
                    })
                
                if self.price_repo.get_prices_by_product_id(product["id"]):
                    self.price_repo.update_price(product["id"], store["id"], {
                        "price": round(data["price"]["price"], 2)
                    })
                else:
                    self.price_repo.create_price({
                        "product_id": product["id"],
                        "store_id": store["id"],
                        "price": round(data["price"]["price"], 2),
                        "unit": data["price"]["unit"]
                    })

            print("Les prix ont été sauvegardés avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'exécution : {e}")
