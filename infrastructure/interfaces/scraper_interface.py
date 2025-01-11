from abc import ABC, abstractmethod


class IScraper(ABC):
    @abstractmethod
    def scrape_metro(self, product_name: str, number_of_page: int):
        pass

    @abstractmethod
    def scrape_iga(self, product_name: str):
        pass

    @abstractmethod
    def scrape_superc(self, product_name: str):
        pass
