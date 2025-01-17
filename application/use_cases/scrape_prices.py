from infrastructure.beautifulsoup.scraper import Scraper
from infrastructure.interfaces.scraper_interface import IScraper
from infrastructure.repositories.price_repository import PriceRepository
from infrastructure.repositories.store_repository import StoreRepository
from infrastructure.repositories.product_repository import ProductRepository
import time


class ScrapePrices:
    def __init__(
        self,
        product_repo: ProductRepository,
        store_repo: StoreRepository,
        price_repo: PriceRepository,
        scraper: IScraper,
    ):
        self.product_repo = product_repo
        self.store_repo = store_repo
        self.price_repo = price_repo
        self.scraper = scraper

    def execute(self, product_name: str, action: str, number_of_page: int):
        """
        Orchestration du scraping et sauvegarde des informations.
        """
        try:

            if action == "metro":
                store = self.store_repo.get_store_by_name(action)
                if not store:
                    raise ValueError(f"Magasin '{action}' introuvable.")
                return self._scrap_metro(product_name, store, number_of_page)
            elif action == "all":
                product = self.product_repo.get_product_by_name_by_store_id(
                    product_name, "32d6dd89-4216-4588-a096-631bfaf5df56"
                )
                iga = self.store_repo.get_store_by_name("iga")
                superc = self.store_repo.get_store_by_name("superc")

                if not iga and not superc:
                    raise ValueError(f"Magasin '{action}' introuvable.")

                data_from_iga = self._scrap_iga(product, iga)

                data_from_superc = self._scrap_superc(product, superc)
                oneData = []

                if data_from_iga != [] or data_from_superc != []:
                    oneData.append(data_from_iga)
                    oneData.append(data_from_superc)

                    self.product_repo.update_product_by_name(
                        product["name"], product["store_id"], {"is_scraped": True}
                    )

                return oneData
            else:
                raise ValueError("Magasin non supporté")

        except Exception as e:
            print(f"Erreur lors de l'exécution : {e}")
            return []

    def _scrap_metro(self, product_name, store, number_of_page):
        scraped_data = self.scraper.scrape_metro(product_name, number_of_page)
        if scraped_data:
            for data in scraped_data:
                self._save_product_and_price_metro(data, store)
            print("Scraping Metro terminé.")
            return scraped_data
        else:
            return []

    def _scrap_iga(self, product, store):
        scraped_data = []
        if product:
            if product["is_scraped"]:
                products_by_reference_id = (
                    self.product_repo.get_product_by_reference_id_and_store_id(
                        product["id"], store["id"]
                    )
                )
                if products_by_reference_id:
                    for _product in products_by_reference_id:
                        price = self.price_repo.get_prices_by_product_id(_product["id"])
                        price[0]["product"] = _product
                        price[0]["store"] = store
                        scraped_data.append(price[0])
                    return scraped_data
            else:
                scraped_data = self.scraper.scrape_iga(
                    product["name"] + " " + product["brand"]
                )
                scraped_data_new = []
                if scraped_data:
                    for data in scraped_data:

                        scraped_data_new.append(
                            self._save_product_and_price_iga(data, product, store)
                        )

                    return scraped_data_new
                else:
                    pass
        return scraped_data

    def _scrap_superc(self, product, store):
        scraped_data = []
        if product:
            if product["is_scraped"]:
                products_by_reference_id = (
                    self.product_repo.get_product_by_reference_id_and_store_id(
                        product["id"], store["id"]
                    )
                )
                if products_by_reference_id:
                    for _product in products_by_reference_id:
                        price = self.price_repo.get_prices_by_product_id(_product["id"])
                        price[0]["product"] = _product
                        price[0]["store"] = store
                        scraped_data.append(price[0])
                    return scraped_data
            else:
                scraped_data = self.scraper.scrape_superc(
                    product["name"] + " " + product["brand"]
                )
                scraped_data_new = []
                if scraped_data:
                    for data in scraped_data:

                        scraped_data_new.append(
                            self._save_product_and_price_superc(data, product, store)
                        )

                    return scraped_data_new
                else:
                    pass
        return scraped_data

    def _save_product_and_price_superc(self, data, product, store):
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

        data["price"]["product_id"] = oneProduct["id"]
        data["price"]["store_id"] = store["id"]

        onePrice = self.price_repo.create_price(data["price"])

        onePrice["product"] = oneProduct
        onePrice["store"] = store
        return onePrice

    def _save_product_and_price_iga(self, data, product, store):
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
                "price_un": data["price"]["price_un"],
                "is_promo": data["price"]["is_promo"],
            }
        )
        onePrice["product"] = oneProduct
        onePrice["store"] = store
        return onePrice

    def _save_product_and_price_metro(self, data: dict, store):
        if self.product_repo.is_name_exist(data["name"], store["id"]):
            print("exist")
            price = data["price"]
            del data["price"]
            data["store_id"] = store["id"]
            product_update = self.product_repo.update_product_by_name(
                data["name"], data["store_id"], data
            )

            if price["is_promo"]:
                self.price_repo.update_price(
                    product_update["id"],
                    store["id"],
                    {
                        "store_id": store["id"],
                        "price": round(price["price"], 2),
                        "unit": price["unit"],
                        "price_un": price["price_un"],
                        "quantity": price["quantity"],
                        "is_promo": price["is_promo"],
                    },
                )
            else:
                self.price_repo.update_price(
                    product_update["id"],
                    store["id"],
                    {
                        "store_id": store["id"],
                        "price": round(price["price"], 2),
                        "unit": price["unit"],
                        "price_un": price["price_un"],
                        "is_promo": price["is_promo"],
                    },
                )
        else:
            price = data["price"]
            del data["price"]
            data["store_id"] = store["id"]
            product_created = self.product_repo.create_product(data)

            if price["is_promo"]:
                self.price_repo.create_price(
                    {
                        "product_id": product_created["id"],
                        "store_id": store["id"],
                        "price": round(price["price"], 2),
                        "unit": price["unit"],
                        "price_un": price["price_un"],
                        "quantity": price["quantity"],
                        "is_promo": price["is_promo"],
                    }
                )
            else:
                self.price_repo.create_price(
                    {
                        "product_id": product_created["id"],
                        "store_id": store["id"],
                        "price": round(price["price"], 2),
                        "unit": price["unit"],
                        "price_un": price["price_un"],
                        "is_promo": price["is_promo"],
                    }
                )
