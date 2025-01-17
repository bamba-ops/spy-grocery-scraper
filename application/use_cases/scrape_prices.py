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
        print(
            f"[execute] Début de l'exécution avec product_name='{product_name}', action='{action}', number_of_page={number_of_page}"
        )
        try:
            if action == "metro":
                print("[execute] Action = metro")
                store = self.store_repo.get_store_by_name(action)
                if not store:
                    raise ValueError(f"Magasin '{action}' introuvable.")
                scraped_data = self._scrap_metro(product_name, store, number_of_page)
                print(f"[execute] Données scrappées (Metro) : {scraped_data}")
                return scraped_data

            elif action == "all":
                print("[execute] Action = all (scraping iga et superc)")
                product = self.product_repo.get_product_by_name_by_store_id(
                    product_name, "32d6dd89-4216-4588-a096-631bfaf5df56"
                )
                iga = self.store_repo.get_store_by_name("iga")
                superc = self.store_repo.get_store_by_name("superc")

                if not iga and not superc:
                    raise ValueError(f"Magasin '{action}' introuvable.")

                print(f"[execute] Produit correspondant: {product}")
                data_from_iga = self._scrap_iga(product, iga)
                print(f"[execute] Données scrappées (IGA) : {data_from_iga}")
                data_from_superc = self._scrap_superc(product, superc)
                print(f"[execute] Données scrappées (SuperC) : {data_from_superc}")

                oneData = []
                if data_from_iga != [] or data_from_superc != []:
                    oneData.append(data_from_iga)
                    oneData.append(data_from_superc)

                    self.product_repo.update_product_by_name(
                        product["name"], product["store_id"], {"is_scraped": True}
                    )
                    print(
                        f"[execute] Produit mis à jour (is_scraped=True) : {product['name']}"
                    )

                return oneData
            else:
                print("[execute] Erreur - magasin non supporté")
                raise ValueError("Magasin non supporté")

        except Exception as e:
            print(f"[execute] Erreur lors de l'exécution : {e}")
            return []

    def _scrap_metro(self, product_name, store, number_of_page):
        print(
            f"[_scrap_metro] Début avec product_name='{product_name}', store='{store['name']}', number_of_page={number_of_page}"
        )
        scraped_data = self.scraper.scrape_metro(product_name, number_of_page)
        print(f"[_scrap_metro] Données scrappées : {scraped_data}")
        if scraped_data:
            for data in scraped_data:
                self._save_product_and_price_metro(data, store)
            print("[_scrap_metro] Scraping Metro terminé.")
            return scraped_data
        else:
            print("[_scrap_metro] Aucune donnée trouvée pour Metro.")
            return []

    def _scrap_iga(self, product, store):
        print(f"[_scrap_iga] Début avec product='{product}', store='{store['name']}'")
        scraped_data = []
        if product:
            if product["is_scraped"]:
                print(
                    "[_scrap_iga] Produit déjà scrappé, récupération des prix existants."
                )
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
                    print(
                        f"[_scrap_iga] Données retournées (depuis DB) : {scraped_data}"
                    )
                    return scraped_data
            else:
                query_string = product["name"] + " " + product["brand"]
                print(f"[_scrap_iga] Scrap IGA avec requête='{query_string}'")
                scraped_data = self.scraper.scrape_iga(query_string)
                scraped_data_new = []
                if scraped_data:
                    for data in scraped_data:
                        saved_price = self._save_product_and_price_iga(
                            data, product, store
                        )
                        scraped_data_new.append(saved_price)
                    print(
                        f"[_scrap_iga] Nouvelles données scrappées et sauvegardées : {scraped_data_new}"
                    )
                    return scraped_data_new
                else:
                    print("[_scrap_iga] Aucune donnée trouvée lors du scraping IGA.")
                    pass
        else:
            print("[_scrap_iga] Aucun produit valide passé en paramètre.")
        return scraped_data

    def _scrap_superc(self, product, store):
        print(
            f"[_scrap_superc] Début avec product='{product}', store='{store['name']}'"
        )
        scraped_data = []
        if product:
            if product["is_scraped"]:
                print(
                    "[_scrap_superc] Produit déjà scrappé, récupération des prix existants."
                )
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
                    print(
                        f"[_scrap_superc] Données retournées (depuis DB) : {scraped_data}"
                    )
                    return scraped_data
            else:
                query_string = product["name"] + " " + product["brand"]
                print(f"[_scrap_superc] Scrap SuperC avec requête='{query_string}'")
                scraped_data = self.scraper.scrape_superc(query_string)
                scraped_data_new = []
                if scraped_data:
                    for data in scraped_data:
                        saved_price = self._save_product_and_price_superc(
                            data, product, store
                        )
                        scraped_data_new.append(saved_price)
                    print(
                        f"[_scrap_superc] Nouvelles données scrappées et sauvegardées : {scraped_data_new}"
                    )
                    return scraped_data_new
                else:
                    print(
                        "[_scrap_superc] Aucune donnée trouvée lors du scraping SuperC."
                    )
                    pass
        else:
            print("[_scrap_superc] Aucun produit valide passé en paramètre.")
        return scraped_data

    def _save_product_and_price_superc(self, data, product, store):
        print(
            f"[_save_product_and_price_superc] Sauvegarde d'un produit SuperC: {data}"
        )
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

        print(f"[_save_product_and_price_superc] Produit créé: {oneProduct}")
        print(f"[_save_product_and_price_superc] Prix créé: {onePrice}")
        return onePrice

    def _save_product_and_price_iga(self, data, product, store):
        print(f"[_save_product_and_price_iga] Sauvegarde d'un produit IGA: {data}")
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

        print(f"[_save_product_and_price_iga] Produit créé: {oneProduct}")
        print(f"[_save_product_and_price_iga] Prix créé: {onePrice}")
        return onePrice

    def _save_product_and_price_metro(self, data: dict, store):
        """
        Sauvegarde ou mise à jour du produit et du prix pour Metro.
        """
        print(f"[_save_product_and_price_metro] Sauvegarde du produit Metro: {data}")
        if self.product_repo.is_name_exist(data["name"], store["id"]):
            print(
                "[_save_product_and_price_metro] Le produit existe déjà, mise à jour..."
            )
            price = data["price"]
            del data["price"]
            data["store_id"] = store["id"]
            product_update = self.product_repo.update_product_by_name(
                data["name"], data["store_id"], data
            )

            # Mise à jour du prix
            update_data = {
                "store_id": store["id"],
                "price": round(price["price"], 2),
                "unit": price["unit"],
                "price_un": price["price_un"],
                "is_promo": price["is_promo"],
            }
            # Ajout du champ quantity s'il existe et que c'est une promo
            if price.get("is_promo") and "quantity" in price:
                update_data["quantity"] = price["quantity"]

            self.price_repo.update_price(product_update["id"], store["id"], update_data)
            print(f"[_save_product_and_price_metro] Mise à jour du prix: {update_data}")
        else:
            print("[_save_product_and_price_metro] Nouveau produit, création...")
            price = data["price"]
            del data["price"]
            data["store_id"] = store["id"]
            product_created = self.product_repo.create_product(data)

            price_data = {
                "product_id": product_created["id"],
                "store_id": store["id"],
                "price": round(price["price"], 2),
                "unit": price["unit"],
                "price_un": price["price_un"],
                "is_promo": price["is_promo"],
            }
            if price.get("is_promo") and "quantity" in price:
                price_data["quantity"] = price["quantity"]

            self.price_repo.create_price(price_data)
            print(f"[_save_product_and_price_metro] Produit créé: {product_created}")
            print(f"[_save_product_and_price_metro] Prix créé: {price_data}")
