from playwright.sync_api import sync_playwright
from .handlers import handle_dialog, handle_banner, wait_for_element, handle_clean_text, handle_extract_unit_and_value, handle_standardize_units, handle_extract_prices
from utils import load_user_agents
import json

class PlaywrightScraper:
    def __init__(self, user_agent_file="config/user_agents.json", headless: bool = False):
        self.user_agents = load_user_agents(user_agent_file)
        self.headless = headless

    def scrape_store(self, store_name: str, product_name: str):
        """
        Lance le scraping pour un magasin donné avec Playwright.
        """
        PAGE_NUMBER = 2
        i = 1
        scraped_data = []
        URL_MAIN = "https://www.metro.ca/epicerie-en-ligne"
        URL_SEARCH_PAGE_1 = "/recherche?filter={product}"
        URL_SEARCH_ALL_PAGE = "/recherche-page-{i}?&filter={product}"

        while i <= PAGE_NUMBER:
            for user_agent in self.user_agents:
                with sync_playwright() as p:
                    print(f"Utilisation de User-Agent : {user_agent}")
                    browser = p.chromium.launch(headless=self.headless)
                    context = browser.new_context(user_agent=user_agent)
                    page = context.new_page()

                    page.on("dialog", handle_dialog)

                    try:
                        if(i == 1):
                            page.goto(URL_MAIN+URL_SEARCH_PAGE_1.format(product = product_name))
                            print(URL_MAIN+URL_SEARCH_PAGE_1.format(product = product_name))
                        else:
                            page.goto(URL_MAIN+URL_SEARCH_ALL_PAGE.format(i = i, product = product_name))
                            print(URL_MAIN+URL_SEARCH_ALL_PAGE.format(i = i, product = product_name))

                        handle_banner(page)
                        wait_for_element(page, "#content-temp > div:nth-child(1) > div.product-page-filter > div:nth-child(3)")

                        # Extraction des données
                        data = self.extract_product_info(page)
                        scraped_data.extend(data)

                    except Exception as e:
                        print(f"Erreur lors du scraping : {e}")
                    finally:
                        i = i + 1
                        browser.close()
                        if(i > PAGE_NUMBER):
                            break
        return scraped_data

    def extract_product_info(self, page):
        """
        Extrait les informations des produits sur la page actuelle.
        """
        name_value=[]
        brand_value = []
        unit_value = []
        img_src = []
        price_value = []
        data = []
        container = page.query_selector('div.products-search--grid.searchOnlineResults')
        if not container:
            print("Aucun produit trouvé.")
            return data
        
        picture_elements = container.query_selector_all('picture.defaultable-picture')
        name_elements = container.query_selector_all('div.content__head')
        price_elements = container.query_selector_all('div.pricing__secondary-price')


        for name in name_elements:
            _title_unit = name.query_selector('a')
            _brand = name.query_selector('span')
            if _brand or _title_unit:
                name_value.append(handle_clean_text(_title_unit.text_content()))
                brand_value.append(handle_clean_text(_brand.text_content()))
                unit_value.append(handle_extract_unit_and_value(handle_clean_text(_title_unit.text_content())))
        for picture in picture_elements:
            img = picture.query_selector('img')
            if img:
                img_src.append(img.get_attribute('src'))

        for price in price_elements:
            _price = price.query_selector('span')
            if _price:
                price_value.append(handle_clean_text(_price.text_content()))

        for name, brand, unit, img, price in zip(name_value, brand_value, unit_value, img_src, handle_standardize_units(handle_extract_prices(price_value))):
            print({"name": name, "brand": brand, "unit":unit, img: "img", "price": price["price"], "unit_price": price["unit"]})
            data.append({
                "name": name,
                "image_url": img,
                "brand": brand,
                "price": price,
                "unit": unit
                })

        return data
