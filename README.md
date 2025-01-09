# Grocery Price Scraper

A Python-based web scraper that extracts grocery prices from online stores and stores the data in a Supabase database.

## Project Overview

This project is designed to scrape product data and prices from various grocery stores' websites. The collected data is stored in a Supabase database for easy access and analysis.

## Features

- **Scraping Multiple Stores:** Supports scraping from stores like Metro and IGA.
- **Data Storage:** Integration with Supabase for persistent data storage.
- **FastAPI Integration:** Provides a RESTful API for initiating scrapes and querying results.
- **Scraping Services:** Utilizes ScrapingBee for web scraping.

---

## Project Structure

```
├── application
│   └── use_cases
│       └── scrape_prices.py  # Scraping logic and data storage orchestration
│
├── infrastructure
│   ├── api
│   │   ├── scrapingbee.py          # ScrapingBee integration for web scraping
│   │   └── supabase_connexion.py   # Supabase connection management
│   │
│   ├── beautifulsoup
│   │   └── scraper.py              # Web scraper using BeautifulSoup
│   │
│   ├── playwright
│   │   └── scraper.py              # Web scraper using Playwright (currently unused)
│   │
│   ├── repositories
│       ├── product_repository.py  # Product database operations
│       ├── store_repository.py    # Store database operations
│       └── price_repository.py    # Price database operations
│
├── presentation
│   └── controllers
│       └── scrape_controller.py  # API routes using FastAPI
│
├── services
│   └── scrape_services.py        # Service layer for managing scraping operations
│
├── main.py                       # FastAPI entry point
├── .env                          # Environment variables for API keys and database access
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Supabase account and project setup
- ScrapingBee account with API key

### Installation
```bash
git clone <repository-url>
cd grocery-price-scraper
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scriptsctivate
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the root directory with the following variables:

```plaintext
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_key>
SCRAPINGBEE_KEY=<your_scrapingbee_api_key>
```

Get the key for scrapingbee here : https://www.scrapingbee.com/

---

## Usage

### Running the API Server
```bash
python -m fastapi dev .\main.py
```

### API Endpoints
- **Scrape all products from a store:** `POST /api/v1/scrape/product/all`
- **Scrape Metro store products:** `POST /api/v1/scrape/product/metro`

### Example API Call (Using cURL)
```bash
curl -X POST "http://localhost:8000/api/v1/scrape/product/all" -H "Content-Type: application/json" -d '{"product_name": "banana", "store_name": "metro", "number_of_page": 2}'
```

---

## Technologies Used
- **Python**: Core language
- **FastAPI**: API framework
- **BeautifulSoup**: Web scraping library
- **Playwright**: Alternative web scraper (currently inactive)
- **ScrapingBee**: Third-party scraping service
- **Supabase**: PostgreSQL-based database service

---

## License
This project is licensed under the MIT License.

---

## Contact
For further questions or collaboration, reach out via [https://x.com/bambatheshark].
