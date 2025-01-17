from utils import setup_logging, logger
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.store_repository import StoreRepository
from infrastructure.repositories.price_repository import PriceRepository

# from infrastructure.playwright.scraper import PlaywrightScraper
# from infrastructure.beautifulsoup.scraper import Scraper
# from application.use_cases.scrape_prices import ScrapePrices
# from infrastructure.api.supabase_connexion import SupabaseConnection
from fastapi import FastAPI
from presentation.controllers.scrape_controller import router as scrape_router

app = FastAPI()

# Inclure les routes
app.include_router(scrape_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Scraper API is running!"}


"""
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
        
        # Test
        #response = supabase_client.table("prices").select("*").eq("id", "bba875c1-9b9a-4413-b489-cd79e4ada79f").execute()
        #if response.data:
        #    print(response.data[0])
        #else:
        #    print("Erreur")

        product_repo = ProductRepository(supabase_client)
        store_repo = StoreRepository(supabase_client)
        price_repo = PriceRepository(supabase_client)
        
        logger.info("Repositories initialized successfully.")
        
        # Initialize scraper
        #scraper = ScraperMetro()
        logger.info("Scraper initialized.")
        
        # Use case: scrape prices
        #scrape_prices_use_case = ScrapePrices(product_repo, store_repo, price_repo, scraper)
        logger.info("Executing price scraping use case for 'banana' at 'metro'.")
        
        #scrape_prices_use_case.execute("banana", "metro")
        logger.info("Scraping completed successfully.")
    
    except ValueError as ve:
        logger.error(f"Validation error: {ve}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        logger.info("Application shutdown")

if __name__ == "__main__":
    main()

"""
