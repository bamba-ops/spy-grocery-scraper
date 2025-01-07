from infrastructure.beautifulsoup.scraper import Scraper
from infrastructure.repositories.price_repository import PriceRepository
from infrastructure.repositories.store_repository import StoreRepository
from infrastructure.repositories.product_repository import ProductRepository


class ScrapePrices:
    def __init__(
        self,
        product_repo: ProductRepository,
        store_repo: StoreRepository,
        price_repo: PriceRepository,
        scraper: Scraper,
    ):
        self.product_repo = product_repo
        self.store_repo = store_repo
        self.price_repo = price_repo
        self.scraper = scraper

    def execute(self, product_name: str, store_name: str, number_of_page: int):
        """
        Orchestration du scraping et sauvegarde des informations.
        """
        try:
            scraped_data_new = []
            # Récupération du magasin
            store = self.store_repo.get_store_by_name(store_name)
            if not store:
                raise ValueError(f"Magasin '{store_name}' introuvable.")

            if store["id"] == "32d6dd89-4216-4588-a096-631bfaf5df56":
                # Scraping des données
                scraped_data_new = self.scraper.scrape_metro(
                    product_name, number_of_page
                )
                # scraped_data = self.scraper.scrape_store(product_name)
                print(f"Scraping terminé. Produits récupérés : {len(scraped_data_new)}")

                # Enregistrement des données dans la base de données
                for data in scraped_data_new:
                    product = self.product_repo.get_product_by_name(data["name"])
                    if product:
                        self.product_repo.update_product_by_name(
                            data["name"],
                            {
                                "name": data["name"],
                                "image_url": data["image_url"],
                                "brand": data["brand"],
                                "unit": data["unit"],
                                "store_id": store["id"],
                            },
                        )

                        self.price_repo.update_price(
                            product["id"],
                            store["id"],
                            {
                                "price": round(data["price"]["price"], 2),
                                "unit": data["price"]["unit"],
                            },
                        )
                    else:
                        product = self.product_repo.create_product(
                            {
                                "name": data["name"],
                                "image_url": data["image_url"],
                                "brand": data["brand"],
                                "unit": data["unit"],
                                "store_id": store["id"],
                            }
                        )

                        self.price_repo.create_price(
                            {
                                "product_id": product["id"],
                                "store_id": store["id"],
                                "price": round(data["price"]["price"], 2),
                                "unit": data["price"]["unit"],
                            }
                        )
            elif store["id"] == "8f719263-a1a0-4f39-b398-29c37ef2c266":
                product = self.product_repo.get_product_by_name(product_name)
                # price_list = []
                if product:

                    scraped_data = self.scraper.scrape_iga(product_name)

                    for data in scraped_data:

                        if product:
                            oneProduct = self.product_repo.create_product(
                                {
                                    "reference_id": product["id"],
                                    "name": data["name"],
                                    "image_url": data["image_url"],
                                    "brand": data["brand"],
                                    "unit": data["unit"],
                                    "store_id": store["id"],
                                }
                            )
                            onePrice = self.price_repo.create_price(
                                {
                                    "product_id": oneProduct["id"],
                                    "store_id": store["id"],
                                    "price": data["price"]["price"],
                                    "unit": data["price"]["unit"],
                                }
                            )
                            onePrice["product"] = oneProduct
                            onePrice["store"] = store
                            scraped_data_new.append(onePrice)

            print("Les prix ont été sauvegardés avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'exécution : {e}")
        finally:
            return scraped_data_new


"""
                    product_by_reference_id = (
                        self.product_repo.get_product_by_reference_id(product["id"])
                    )
                    print(product_by_reference_id)
                    if product_by_reference_id != []:
                        for product_by in product_by_reference_id:
                            print(1)
                            price = self.price_repo.get_price_by_product_and_store(
                                store["id"], product_by["id"]
                            )
                            if isinstance(price, dict):
                                price["product"] = product_by
                                price["store"] = store
                                price_list.append(price)
                            else:
                                print("Le format de `price` est incorrect :", price)
                        scraped_data_new = price_list
                        """


"""
product_iga = self.product_repo.get_product_by_image_url(
                                data["image_url"]
                            )

 if (
                                    product_iga
                                    and product_iga["store_id"]
                                    != "32d6dd89-4216-4588-a096-631bfaf5df56"
                                ):
                                    oneProduct = (
                                        self.product_repo.update_product_by_name(
                                            data["name"],
                                            {
                                                "name": data["name"],
                                                "image_url": data["image_url"],
                                                "brand": data["brand"],
                                                "unit": data["unit"],
                                            },
                                        )
                                    )

                                    onePrice = self.price_repo.update_price(
                                        oneProduct["id"],
                                        store["id"],
                                        {
                                            "product_id": product["id"],
                                            "store_id": store["id"],
                                            "price": data["price"]["price"],
                                            "unit": data["price"]["unit"],
                                        },
                                    )
                                    onePrice["product"] = oneProduct
                                    onePrice["store"] = store

"""
