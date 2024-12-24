from bs4 import BeautifulSoup
from ..api.scrapingbee import ScrapingBee
from ..playwright.handlers import handle_banner, handle_clean_text, handle_dialog, handle_extract_prices, handle_extract_unit_and_value, handle_standardize_units

class ScraperMetro:

    def scrape_metro(self, product_name: str):
        
        PAGE_NUMBER = 1
        i = 1
        scraped_data = []
        URL_MAIN = "https://www.metro.ca/epicerie-en-ligne"
        URL_SEARCH_PAGE_1 = "/recherche?filter={product}"
        URL_SEARCH_ALL_PAGE = "/recherche-page-{i}?&filter={product}"

        while i <= PAGE_NUMBER:

            try:
                if( i==1 ):
                    scraped_data.extend(self.extract_info_metro(ScrapingBee.get_html_content_from_url(URL_MAIN+URL_SEARCH_PAGE_1.format(product = product_name), '#content-temp > div:nth-child(1) > div.product-page-filter > div:nth-child(3) > div')))
                else:
                    scraped_data.extend(self.extract_info_metro(ScrapingBee.get_html_content_from_url(URL_MAIN+URL_SEARCH_ALL_PAGE.format(i = i, product = product_name), '#content-temp > div:nth-child(1) > div.product-page-filter > div:nth-child(3) > div')))
            
            except Exception as e:
                print(f"Erreur lors du scraping : {e}")
            finally:
                i = i + 1
        
        return scraped_data

    def extract_info_metro(self, html_content):
            soup = BeautifulSoup(html_content, "html.parser")

            name_value=[]
            brand_value = []
            unit_value = []
            img_src = []
            price_value = []
            data = []

            container = soup.select_one('div.products-search--grid.searchOnlineResults')
            if not container:
                print("Aucun produit trouvé.")
                return data
            
            picture_elements = container.select('picture.defaultable-picture')
            name_elements = container.select('div.content__head')
            price_elements = container.select('div.pricing__secondary-price')

            for name in name_elements:
                _title_unit = name.select_one('a')
                _brand = name.select_one('span')
                if _brand or _title_unit:
                    name_value.append(handle_clean_text(_title_unit.text.strip()))
                    brand_value.append(handle_clean_text(_brand.text.strip()))
                    unit_value.append(handle_extract_unit_and_value(handle_clean_text(_title_unit.text.strip())))
            for picture in picture_elements:
                img = picture.select_one('img')
                if img and img.get('src'):
                    img_src.append(img['src'])

            for price in price_elements:
                _price = price.select_one('span')
                if _price:
                    price_value.append(handle_clean_text(_price.text.strip()))

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
