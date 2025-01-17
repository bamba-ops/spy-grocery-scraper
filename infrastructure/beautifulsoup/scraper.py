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
    extraire_prix_un_metro,
    extraire_prix_iga,
    extraire_prix_de_liste_superc,
    clean_name_list,
)


class Scraper(IScraper):
    def scrape_superc(self, product_name: str):
        print(f"[scrape_superc] Début du scraping SuperC pour: '{product_name}'")
        scraped_data = []

        # On va boucler tant qu'on ne trouve pas de résultat ou qu'on a plus de mots à enlever
        while True:
            URL_MAIN = "https://www.superc.ca/recherche?filter=" + product_name
            print(f"[scrape_superc] URL: {URL_MAIN}")

            try:
                html_content = ScrapingBee.get_html_content_from_url(
                    URL_MAIN,
                    "#content-temp > div > div.product-page-filter > div:nth-child(3) > div",
                )
            except Exception as e:
                print(f"[scrape_superc] Erreur dans ScrapingBee: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Erreur lors du scrapping : {e}"
                )

            # Si le html_content est vide, on retire le dernier mot du product_name
            if not html_content:
                print(f"[scrape_superc] Aucune donnée retournée pour: '{product_name}'")
                # On scinde le nom du produit en mots
                words = product_name.strip().split()

                # Si on a plus d'un mot, on retire le dernier
                if len(words) > 1:
                    removed_word = words.pop()
                    product_name = " ".join(words)
                    print(
                        f"[scrape_superc] Suppression du mot '{removed_word}'. Nouveau product_name: '{product_name}'"
                    )
                else:
                    # Si on est rendu à un seul mot et qu'on ne trouve toujours rien,
                    # on arrête la recherche.
                    print(
                        "[scrape_superc] Aucun résultat trouvé, même après suppression des mots."
                    )
                    break
            else:
                print(
                    "[scrape_superc] Contenu obtenu, extraction des données en cours..."
                )
                scraped_data.extend(self.extract_info_superc(html_content))
                break  # On sort de la boucle puisqu'on a des résultats

        print(
            f"[scrape_superc] Fin du scraping SuperC. Résultat total : {scraped_data}"
        )
        return scraped_data

    def scrape_iga(self, product_name: str):
        print(f"[scrape_iga] Début du scraping IGA pour: '{product_name}'")
        scraped_data = []

        # On va boucler tant qu'on ne trouve pas de résultat ou qu'on a plus de mots à enlever
        while True:
            URL_MAIN = (
                "https://www.iga.net/fr/search?t={D9CE4CBE-C8C3-4203-A58B-7CF7B830880E}&k="
                + product_name
            )
            print(f"[scrape_iga] URL: {URL_MAIN}")

            try:
                html_content = ScrapingBee.get_html_content_from_url(
                    URL_MAIN,
                    "#body_0_main_1_GrocerySearch_TemplateResult_SearchResultListView_MansoryPanel",
                )
            except Exception as e:
                print(f"[scrape_iga] Erreur dans ScrapingBee: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Erreur lors du scrapping : {e}"
                )

            # Vérification si le contenu est vide
            if not html_content:
                print(f"[scrape_iga] Aucune donnée retournée pour: '{product_name}'")
                # On scinde le nom du produit en mots
                words = product_name.strip().split()

                # Si on a plus d'un mot, on retire le dernier
                if len(words) > 1:
                    removed_word = words.pop()
                    product_name = " ".join(words)
                    print(
                        f"[scrape_iga] Suppression du mot '{removed_word}'. Nouveau product_name: '{product_name}'"
                    )
                else:
                    print(
                        "[scrape_iga] Aucun résultat trouvé, même après suppression des mots."
                    )
                    break
            else:
                print("[scrape_iga] Contenu obtenu, extraction des données en cours...")
                scraped_data.extend(self.extract_info_iga(html_content))
                break

        print(f"[scrape_iga] Fin du scraping IGA. Résultat total : {scraped_data}")
        return scraped_data

    def scrape_metro(self, product_name: str, number_of_page: int):
        print(
            f"[scrape_metro] Début du scraping Metro pour: '{product_name}', sur {number_of_page} page(s)"
        )
        PAGE_NUMBER = number_of_page
        i = 1
        scraped_data = []

        if product_name != "all":
            URL_MAIN = "https://www.metro.ca/epicerie-en-ligne"
            URL_SEARCH_PAGE_1 = "/recherche?filter={product}"
            URL_SEARCH_ALL_PAGE = "/recherche-page-{i}?&filter={product}"
        else:
            URL_MAIN = "https://www.metro.ca/epicerie-en-ligne/recherche-page-{i}"

        while i <= PAGE_NUMBER:
            try:
                if product_name != "all":
                    if i == 1:
                        url = URL_MAIN + URL_SEARCH_PAGE_1.format(product=product_name)
                    else:
                        url = URL_MAIN + URL_SEARCH_ALL_PAGE.format(
                            i=i, product=product_name
                        )
                else:
                    url = URL_MAIN.format(i=i)

                print(f"[scrape_metro] Scraping de la page #{i} : {url}")

                scraped_data.extend(
                    self.extract_info_metro(
                        ScrapingBee.get_html_content_from_url(
                            url,
                            "#content-temp > div:nth-child(1) > div.product-page-filter > div:nth-child(3) > div",
                        )
                    )
                )

            except Exception as e:
                print(f"[scrape_metro] Erreur dans ScrapingBee: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Erreur lors du scrapping : {e}"
                )
            finally:
                print(f"[scrape_metro] Fin de traitement de la page #{i}")
                i += 1

        print(f"[scrape_metro] Fin du scraping Metro. Résultat total : {scraped_data}")
        return scraped_data

    def extract_info_iga(self, html_content):
        print("[extract_info_iga] Extraction des informations depuis le HTML IGA.")
        soup = BeautifulSoup(html_content, "html.parser")

        data = []
        produits = []
        prices = []
        produits_vus = set()  # Pour garder une trace des produits ajoutés

        # Trouver tous les conteneurs de produits
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
                marque = (
                    produit_html.find("div", class_="item-product__brand").get_text(
                        strip=True
                    )
                    if produit_html.find("div", class_="item-product__brand")
                    else ""
                )
                unite = (
                    produit_html.find("div", class_="item-product__info").get_text(
                        strip=True
                    )
                    if produit_html.find("div", class_="item-product__info")
                    else ""
                )
                url_image = (
                    produit_html.find("img", class_="fluid")["src"]
                    if produit_html.find("img", class_="fluid")
                    and produit_html.find("img", class_="fluid").get("src")
                    else ""
                )

                prix_un = (
                    produit_html.find(
                        "span", class_=["price", "text--strong"]
                    ).get_text(strip=True)
                    if produit_html.find("span", class_=["price", "text--strong"])
                    else ""
                )

                if produit_html.find("div", class_="text--small"):
                    prix = produit_html.find("div", class_="text--small").get_text(
                        strip=True
                    )
                else:
                    prix = prix_un + " / " + unite

                produits_vus.add(nom)
                produits.append(
                    {
                        "name": handle_clean_text(nom),
                        "brand": handle_clean_text(marque),
                        "unit": handle_extract_unit_and_value(handle_clean_text(unite)),
                        "image_url": url_image,
                        "price_test": prix,
                        "price_un": extraire_prix_iga(prix_un),
                    }
                )
                prices.append(handle_clean_text(prix))

        new_prices = handle_standardize_units(handle_extract_prices(prices))
        if len(new_prices) == len(produits):
            for produit, price in zip(produits, new_prices):
                if price["price"] is not None:
                    price["price"] = round(price["price"], 2)
                else:
                    price["price"] = None
                price["price_un"] = produit["price_un"]
                price["is_promo"] = False

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
            print(
                "[extract_info_iga] Les longueurs de new_prices et produits ne correspondent pas, aucun data créé."
            )

        print(f"[extract_info_iga] Data final : {data}")
        return data

    def extract_info_superc(self, html_content):
        print(
            "[extract_info_superc] Extraction des informations depuis le HTML SuperC."
        )
        soup = BeautifulSoup(html_content, "html.parser")
        data = []

        container = soup.select_one("div.products-search--grid.searchOnlineResults")
        if not container:
            print("[extract_info_superc] Aucun produit trouvé.")
            return data

        picture_elements = container.select("picture.defaultable-picture")
        name_elements = container.select("div.content__head")
        price_elements = container.select("div.pricing__secondary-price")
        price_un_elements = container.select("div.pricing__sale-price")

        name_value = []
        brand_value = []
        unit_value = []
        img_src = []
        price_value = []
        price_un_value = []

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

        for price_un in price_un_elements:
            price_un_value.append(handle_clean_text(price_un.text))

        if len(price_value) == len(name_value) == len(price_un_value):
            for name, brand, unit, img, price, price_un in zip(
                name_value,
                brand_value,
                unit_value,
                img_src,
                handle_standardize_units_metro(
                    handle_extract_prices_metro(price_value)
                ),
                extraire_prix_de_liste_superc(price_un_value),
            ):
                price["price"] = round(price["price"], 2)
                if isinstance(price_un, list):
                    # On considère que [0] = quantité promo, [1] = prix un promo
                    price["price_un"] = price_un[1]
                    price["quantity"] = price_un[0]
                    price["is_promo"] = True
                else:
                    price["price_un"] = price_un
                    price["is_promo"] = False

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
            print(
                "[extract_info_superc] Les longueurs des listes ne correspondent pas, aucun data créé."
            )

        print(f"[extract_info_superc] Data final : {data}")
        return data

    def extract_info_metro(self, html_content):
        print("[extract_info_metro] Extraction des informations depuis le HTML Metro.")
        soup = BeautifulSoup(html_content, "html.parser")

        data = []
        container = soup.select_one("div.products-search--grid.searchOnlineResults")
        if not container:
            print("[extract_info_metro] Aucun produit trouvé.")
            return data

        picture_elements = container.select("picture.defaultable-picture")
        name_elements = container.select("div.content__head")
        price_elements = container.select("div.pricing__secondary-price")
        price_un_elements = container.select("div.pricing__sale-price")

        name_value = []
        brand_value = []
        unit_value = []
        img_src = []
        price_value = []
        price_un_value = []

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
            price_value.append(price.text if price else "")

        for price_un in price_un_elements:
            price_un_value.append(handle_clean_text(price_un.text))

        price_un_value_extrait = extraire_prix_un_metro(price_un_value)

        # Petit log pour comparer les valeurs extraites
        for price, price_extrait in zip(price_un_value, price_un_value_extrait):
            print(
                f"[extract_info_metro] Price brut: '{price}' | Price extrait: '{price_extrait}'"
            )

        if len(price_value) == len(price_un_value_extrait):
            extracted_prices = handle_extract_prices_metro_2(price_value)
            standardized_prices = handle_standardize_units_2(extracted_prices)

            for name, brand, unit, img, price, price_extrait in zip(
                clean_name_list(name_value),
                brand_value,
                unit_value,
                img_src,
                standardized_prices,
                price_un_value_extrait,
            ):
                if isinstance(price_extrait, list):
                    price["price_un"] = price_extrait[1]
                    price["quantity"] = price_extrait[0]
                    price["is_promo"] = True
                else:
                    price["price_un"] = price_extrait
                    price["is_promo"] = False

                data.append(
                    {
                        "name": name,
                        "image_url": img,
                        "brand": brand,
                        "price": price,
                        "unit": unit,
                    }
                )
            print(f"[extract_info_metro] Données extraites : {data}")
        else:
            print(
                "[extract_info_metro] Les listes price_value et price_un_value_extrait ont des longueurs différentes."
            )

        return data
