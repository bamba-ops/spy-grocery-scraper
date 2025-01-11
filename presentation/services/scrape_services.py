from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.store_repository import StoreRepository
from infrastructure.repositories.price_repository import PriceRepository
from infrastructure.playwright.scraper import PlaywrightScraper
from infrastructure.beautifulsoup.scraper import Scraper
from application.use_cases.scrape_prices import ScrapePrices
from infrastructure.api.supabase_connexion import SupabaseConnection


class ScrapeService:

    supabase_client = SupabaseConnection.create_connection()
    product_repo = ProductRepository(supabase_client)
    store_repo = StoreRepository(supabase_client)
    price_repo = PriceRepository(supabase_client)

    @staticmethod
    def scrape_product(data: dict):
        product_name = data.get("product_name")
        action = data.get("action")

        if not product_name and not action:
            return {"error": "The both 'product_name' and 'action' is required"}

        scraper = Scraper()

        scraper_prices_use_case = ScrapePrices(
            ScrapeService.product_repo,
            ScrapeService.store_repo,
            ScrapeService.price_repo,
            scraper,
        )

        data = scraper_prices_use_case.execute(product_name, action, number_of_page=0)

        if data == []:
            return {"status": "error", "message": "No data scraped"}

        return {
            "status": "success",
            "message": f"Scraping completed for {product_name}",
            "data": data,
        }

    @staticmethod
    def scrape_product_metro(data: dict):
        product_name = data.get("product_name")
        action = data.get("action")
        number_of_page = data.get("number_of_page")

        if not product_name and not action:
            return {"error": "The both 'product_name' and 'action' is required"}

        scraper = Scraper()

        scraper_prices_use_case = ScrapePrices(
            ScrapeService.product_repo,
            ScrapeService.store_repo,
            ScrapeService.price_repo,
            scraper,
        )

        data = scraper_prices_use_case.execute(product_name, action, number_of_page)

        if data == []:
            return {"status": "error", "message": "No data scraped"}

        return {
            "status": "success",
            "message": f"Scraping completed for {product_name} and {action}",
            "data": data,
        }
