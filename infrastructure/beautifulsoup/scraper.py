from bs4 import BeautifulSoup
from infrastructure.interfaces.scraper_interface import IScraper
from fastapi import HTTPException
from ..api.scrapingbee import ScrapingBee
from ..playwright.handlers import (
    handle_banner,
    handle_clean_text,
    handle_dialog,
    handle_extract_prices,
    handle_extract_unit_and_value,
    handle_standardize_units,
    handle_extract_prices_metro,
    handle_standardize_units_metro,
    handle_extract_prices_metro_2,
    handle_standardize_units_2,
)


class Scraper(IScraper):

    def scrape_superc(self, product_name: str):
        URL_MAIN = "https://www.superc.ca/recherche?filter=" + product_name
        print(URL_MAIN)
        scraped_data = []
        try:
            scraped_data.extend(
                self.extract_info_superc(
                    ScrapingBee.get_html_content_from_url(
                        URL_MAIN,
                        "#content-temp > div > div.product-page-filter > div:nth-child(3) > div",
                    )
                )
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erreur lors du scrapping : {e}"
            )

        return scraped_data

    def scrape_iga(self, product_name: str):

        URL_MAIN = (
            "https://www.iga.net/fr/search?t={D9CE4CBE-C8C3-4203-A58B-7CF7B830880E}&k="
            + product_name
        )
        print(URL_MAIN)
        scraped_data = []
        try:
            scraped_data.extend(
                self.extract_info_iga(
                    ScrapingBee.get_html_content_from_url(
                        URL_MAIN,
                        "#body_0_main_1_GrocerySearch_TemplateResult_SearchResultListView_ctrl0_ItemTemplatePanel_0 > div > div.item-product > div > div:nth-child(1) > div",
                    )
                )
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erreur lors du scrapping : {e}"
            )

        return scraped_data

    def scrape_metro(self, product_name: str, number_of_page: int):

        PAGE_NUMBER = number_of_page
        i = 1
        scraped_data = []
        URL_MAIN = "https://www.metro.ca/epicerie-en-ligne"
        URL_SEARCH_PAGE_1 = "/recherche?filter={product}"
        URL_SEARCH_ALL_PAGE = "/recherche-page-{i}?&filter={product}"

        while i <= PAGE_NUMBER:

            try:
                if i == 1:
                    scraped_data.extend(
                        self.extract_info_metro(
                            ScrapingBee.get_html_content_from_url(
                                URL_MAIN
                                + URL_SEARCH_PAGE_1.format(product=product_name),
                                "#content-temp > div:nth-child(1) > div.product-page-filter > div:nth-child(3) > div",
                            )
                        )
                    )
                else:
                    scraped_data.extend(
                        self.extract_info_metro(
                            ScrapingBee.get_html_content_from_url(
                                URL_MAIN
                                + URL_SEARCH_ALL_PAGE.format(i=i, product=product_name),
                                "#content-temp > div:nth-child(1) > div.product-page-filter > div:nth-child(3) > div",
                            )
                        )
                    )

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur lors du scrapping : {e}"
                )
            finally:
                i = i + 1

        return scraped_data

    def extract_info_iga(self, html_content):
        # Initialiser BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        print(html_content)

        # Liste pour stocker les informations des produits
        data = []
        produits = []
        prices = []
        produits_vus = set()  # Pour garder une trace des produits ajoutés

        # Trouver tous les conteneurs de produits (adapter le sélecteur en fonction de la structure HTML)
        produits_html = soup.find_all(
            "div",
            class_=[
                "item-product",
                "js-product",
                "js-equalized",
                "js-addtolist-container",
                "js-ga",
            ],
        )

        for produit_html in produits_html:
            nom = (
                produit_html.find("h3", class_=["h4-like", "text--brand"]).get_text(
                    strip=True
                )
                if produit_html.find("h3", class_=["h4-like", "text--brand"])
                else ""
            )
            if nom not in produits_vus:
                # Extraire les informations individuelles
                marque = (
                    produit_html.find("div", class_="item-product__brand").get_text(
                        strip=True
                    )
                    if produit_html.find("div", class_="item-product__brand")
                    else ""
                )
                # Nettoyer le texte de la marque pour retirer les informations supplémentaires
                # marque = marque.replace(nom, '').strip()
                unite = (
                    produit_html.find("div", class_="item-product__info").get_text(
                        strip=True
                    )
                    if produit_html.find("div", class_="item-product__info")
                    else ""
                )
                url_image = (
                    produit_html.find("img", class_="fluid")["src"]
                    if produit_html.find("img", class_="fluid")["src"]
                    else ""
                )
                # prix = produit_html.find('div', class_='text--small').get_text(strip=True)
                if produit_html.find("div", class_="text--small"):
                    prix = produit_html.find("div", class_="text--small").get_text(
                        strip=True
                    )
                else:  # produit_html.find('span', class_=['price', 'text--strong']):
                    prix = produit_html.find(
                        "span", class_=["price", "text--strong"]
                    ).get_text(strip=True)
                    prix = prix + " / " + unite

                produits_vus.add(
                    nom
                )  # Ajoute le produit au set pour éviter les doublons
                # Ajouter les informations dans la liste
                produits.append(
                    {
                        "name": handle_clean_text(nom),
                        "brand": handle_clean_text(marque),
                        "unit": handle_extract_unit_and_value(handle_clean_text(unite)),
                        "image_url": url_image,
                        "price_test": prix,
                    }
                )
                prices.append(handle_clean_text(prix))

        new_prices = handle_standardize_units(handle_extract_prices(prices))
        if len(new_prices) == len(produits):
            for produit, price in zip(produits, new_prices):
                price["price"] = round(price["price"], 2)
                data.append(
                    {
                        "name": produit["name"],
                        "image_url": produit["image_url"],
                        "brand": produit["brand"],
                        "price": price,
                        "unit": produit["unit"],
                    }
                )
        else:
            pass
        return data

    def extract_info_superc(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        print(html_content)
        name_value = []
        brand_value = []
        unit_value = []
        img_src = []
        price_value = []
        data = []

        container = soup.select_one("div.products-search--grid.searchOnlineResults")
        if not container:
            print("Auncu produit trouvé")
            return data

        picture_elements = container.select("picture.defaultable-picture")
        name_elements = container.select("div.content__head")
        price_elements = container.select("div.pricing__secondary-price")

        for name in name_elements:
            _title_unit = name.select_one("a")
            _brand = name.select_one("span")
            if _brand or _title_unit:
                name_value.append(handle_clean_text(_title_unit.text.strip()))
                brand_value.append(handle_clean_text(_brand.text.strip()))
                unit_value.append(
                    handle_extract_unit_and_value(
                        handle_clean_text(_title_unit.text.strip())
                    )
                )
        for picture in picture_elements:
            img = picture.select_one("img")
            if img and img.get("src"):
                img_src.append(img["src"])

        for price in price_elements:
            _price = price.select_one("span")
            if _price:
                price_value.append(handle_clean_text(_price.text.strip()))
        if len(price_value) == len(name_value):
            for name, brand, unit, img, price in zip(
                name_value,
                brand_value,
                unit_value,
                img_src,
                handle_standardize_units_metro(
                    handle_extract_prices_metro(price_value)
                ),
            ):
                price["price"] = round(price["price"], 2)
                data.append(
                    {
                        "name": name,
                        "image_url": img,
                        "brand": brand,
                        "price": price,
                        "unit": unit,
                    }
                )
        else:
            pass
        # print(data)
        return data

    def extract_info_metro(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        name_value = []
        brand_value = []
        unit_value = []
        img_src = []
        price_value = []
        data = []

        container = soup.select_one("div.products-search--grid.searchOnlineResults")
        if not container:
            print("Aucun produit trouvé.")
            return data

        picture_elements = container.select("picture.defaultable-picture")
        name_elements = container.select("div.content__head")
        price_elements = container.select("div.pricing__secondary-price")

        for name in name_elements:
            _title_unit = name.select_one("a")
            _brand = name.select_one("span")
            if _brand or _title_unit:
                name_value.append(handle_clean_text(_title_unit.text.strip()))
                brand_value.append(handle_clean_text(_brand.text.strip()))
                unit_value.append(
                    handle_extract_unit_and_value(
                        handle_clean_text(_title_unit.text.strip())
                    )
                )
        for picture in picture_elements:
            img = picture.select_one("img")
            if img and img.get("src"):
                img_src.append(img["src"])

        for price in price_elements:
            # print(price.text)
            _price = price.select_one("span")
            # print(_price.text.strip())
            price_value.append(price.text)

        print(handle_standardize_units_2(handle_extract_prices_metro_2(price_value)))

        for name, brand, unit, img, price in zip(
            name_value,
            brand_value,
            unit_value,
            img_src,
            handle_standardize_units_2(handle_extract_prices_metro_2(price_value)),
        ):
            print(
                {
                    "name": name,
                    "brand": brand,
                    "unit": unit,
                    "image_url": img,
                    "price": price["price"],
                    "unit_price": price["unit"],
                }
            )
            data.append(
                {
                    "name": name,
                    "image_url": img,
                    "brand": brand,
                    "price": price,
                    "unit": unit,
                }
            )
        # print(data)
        return data
