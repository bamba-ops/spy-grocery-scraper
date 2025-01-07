from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from ..services.scrape_services import ScrapeService

router = APIRouter()

@router.post("/scrape/product/all")
def scrape_product(data: dict):
    # Configurer les dépendances
    #product_repo = ProductRepository()
    #store_repo = StoreRepository()
    #price_repo = PriceRepository()
    #scraper = ScrapingBee()

    # Initialiser le cas d'utilisation
    #scrape_use_case = ScrapePrices(product_repo, store_repo, price_repo, scraper)

    # Lancer le scraping
    try:
        return ScrapeService.scrape_product(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/scrape/product/metro")
def scrape_product_metro(data: dict):
    '''
    Scrape all the 'product_name' in the metro supermarket 
    then store all the 'product_name' in supabase database
    related to 'product_name', it's scrape page per page. 
    All search related with 'product_name'
    '''
    try:
        return ScrapeService.scrape_product_metro(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
