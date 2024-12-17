from utils import setup_logging, logger
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.store_repository import StoreRepository
from infrastructure.repositories.price_repository import PriceRepository
from infrastructure.playwright.scraper import PlaywrightScraper
from application.use_cases.scrape_prices import ScrapePrices
from infrastructure.api.supabase_connexion import SupabaseConnection

def main():
    setup_logging()
    
    logger.info("Application startup")
    
    try:
        # Initialize Supabase connection
        logger.info("Connecting to Supabase...")
        supabase_client = SupabaseConnection.create_connection()
        logger.info("Successfully connected to Supabase.")
        
        # Initialize repositories
        if not supabase_client:
            raise ValueError("Invalid Supabase connection.")
        
        product_repo = ProductRepository(supabase_client)
        store_repo = StoreRepository(supabase_client)
        price_repo = PriceRepository(supabase_client)
        
        logger.info("Repositories initialized successfully.")
        
        # Initialize scraper
        scraper = PlaywrightScraper()
        logger.info("Playwright scraper initialized.")
        
        # Use case: scrape prices
        scrape_prices_use_case = ScrapePrices(product_repo, store_repo, price_repo, scraper)
        logger.info("Executing price scraping use case for 'banana' at 'metro'.")
        
        scrape_prices_use_case.execute("banana", "metro")
        logger.info("Scraping completed successfully.")
    
    except ValueError as ve:
        logger.error(f"Validation error: {ve}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        logger.info("Application shutdown")

if __name__ == "__main__":
    main()
