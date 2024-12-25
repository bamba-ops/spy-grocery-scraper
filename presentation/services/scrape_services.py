from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.store_repository import StoreRepository
from infrastructure.repositories.price_repository import PriceRepository
from infrastructure.playwright.scraper import PlaywrightScraper
from infrastructure.beautifulsoup.scraper import ScraperMetro
from application.use_cases.scrape_prices import ScrapePrices
from infrastructure.api.supabase_connexion import SupabaseConnection

class ScrapeService:

    supabase_client = SupabaseConnection.create_connection()
    product_repo = ProductRepository(supabase_client)
    store_repo = StoreRepository(supabase_client)
    price_repo = PriceRepository(supabase_client)

    @staticmethod
    def scrape_product(data: dict):
        product_name = data.get("name")
        product_brand = data.get("brand")
        
        if not product_name and not product_brand:
            return {'error': "Either 'name' or 'brand' is required"}
        
        # Déterminer le type de recherche
        search_type = "name" if product_name else "brand"
        search_value = product_name if product_name else product_brand

        return {"message": f"Scraping completed for {search_type}: {search_value}"}
    
    @staticmethod
    def scrape_product_metro(data: dict):
        product_name = data.get("product_name")
        store_name = data.get("store_name")
        number_of_page = data.get("number_of_page")

        if not product_name and not store_name:
            return {'error': "The both 'product_name' and 'store_name' is required"}

        scraper = ScraperMetro()

        scraper_prices_use_case = ScrapePrices(ScrapeService.product_repo, ScrapeService.store_repo, ScrapeService.price_repo, scraper)

        scraper_prices_use_case.execute(product_name, store_name, number_of_page)

        return {"message": f"Scraping completed for {product_name} in {store_name}"}
