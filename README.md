
# **Quebec Supermarket Product Scraper**  
**A scalable scraping logic layer for collecting and storing product information from various supermarket websites in Quebec.**

---

## **Project Overview**  
This project is a **scraping logic layer** designed to extract product data (name, price, brand, image, and unit information) from supermarket websites across Quebec. The extracted data is then stored in a **Supabase** database for further use.  

In future iterations, this project will serve as the foundation for a larger system using clean architecture, including:  
1. **API Backend**: An API to provide product information, such as comparing prices across supermarkets.  
2. **Frontend Layer**: A user interface for searching products, viewing comparisons, and finding the cheapest options.

---

## **Key Features**  
- **Dynamic Web Scraping**: Using Playwright for robust and scalable scraping of supermarket websites.  
- **Supabase Integration**: Store extracted product data efficiently in a cloud-hosted database.  
- **Clean Architecture**: The project follows Clean Architecture principles for modularity and maintainability.  
- **Logging System**: Integrated logging to track scraping activity, errors, and progress.  

---

## **How It Works**  

1. **Input**: Provide the product name (e.g., "banana") and the target supermarket (e.g., "metro").  
2. **Scraping**: Playwright navigates the target supermarket's site, handles cookies/banners, and extracts product details:
   - Product Name  
   - Product Price  
   - Brand  
   - Image URL  
   - Units (e.g., kg, L, unit)  
3. **Data Storage**: The extracted data is stored in **Supabase** under structured tables (`products`, `stores`, and `prices`).  
4. **Future Use**: This data can be queried to compare prices across different supermarkets.

---

## **Technology Stack**  

| **Component**       | **Technology**        |  
|----------------------|-----------------------|  
| **Programming Language** | Python            |  
| **Web Scraping**    | Playwright            |  
| **Database**        | Supabase (PostgreSQL) |  
| **Environment Management** | `dotenv`        |  
| **Logging**         | Python Logging Module |  

---

## **Architecture**  

The project is structured as follows:  

```
project-root/
│
├── config/                        # Configuration files (e.g., User Agent list)
├── infrastructure/                
│   ├── playwright/                # Scraping logic
│   │   ├── scraper.py             # Core scraper using Playwright
│   │   └── handlers.py            # Helper functions for handling banners/dialogs
│   ├── repositories/              # Database repositories
│   │   ├── product_repository.py
│   │   ├── store_repository.py
│   │   └── price_repository.py
│   ├── api/                       # Supabase connection setup
│   │   └── supabase_connexion.py
│
├── application/
│   ├── use_cases/
│   │   └── scrape_prices.py       # Use case to scrape prices and store data
│
├── utils/
│   ├── logging_setup.py           # Centralized logging configuration
│   └── user_agents.json           # User agents for scraping
│
├── main.py                        # Entry point for the scraping execution
├── requirements.txt               # Project dependencies
└── .gitignore                     # Ignored files (.env, logs)
```

---

## **Installation Guide**

### **1. Prerequisites**  
Ensure you have the following installed:  
- **Python 3.8+**  
- **Node.js** (required for Playwright installation)  

### **2. Clone the Repository**  
```bash
git clone https://github.com/your-username/quebec-supermarket-scraper.git
cd quebec-supermarket-scraper
```

### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**  
Create a `.env` file in the project root with your Supabase credentials:  
```plaintext
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-api-key
```

### **5. Run the Scraper**  
Example: Scraping "bananas" from "metro":  
```bash
python main.py
```

---

## **Usage Example**  

To scrape data for "bananas" at Metro, call the scraper as follows:  

```python
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.store_repository import StoreRepository
from infrastructure.repositories.price_repository import PriceRepository
from infrastructure.playwright.scraper import PlaywrightScraper
from application.use_cases.scrape_prices import ScrapePrices
from infrastructure.api.supabase_connexion import SupabaseConnection

def main():
    supabase_client = SupabaseConnection.create_connection()
    product_repo = ProductRepository(supabase_client)
    store_repo = StoreRepository(supabase_client)
    price_repo = PriceRepository(supabase_client)
    scraper = PlaywrightScraper()
    scrape_prices_use_case = ScrapePrices(product_repo, store_repo, price_repo, scraper)
    scrape_prices_use_case.execute("banana", "metro")

if __name__ == "__main__":
    main()
```

---

## **Future Enhancements**  
- Add support for additional supermarkets.  
- Schedule automatic scraping using a job scheduler.  
- Implement an API backend for querying and comparing product prices.  
- Build a frontend interface for users to view and interact with the data.  

---

## **Contributing**  
Contributions are welcome! Feel free to fork this repository, open issues, and submit pull requests.  

---

## **License**  
This project is licensed under the MIT License.

---

## **Contact**  
For inquiries or collaboration:  
- **Name**: Your Full Name  
- **Email**: your.email@example.com  
- **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/)  
- **GitHub**: [Your GitHub Profile](https://github.com/your-username)

---