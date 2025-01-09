import requests
import os
from dotenv import load_dotenv
from fastapi import HTTPException


class ScrapingBee:

    @staticmethod
    def get_html_content_from_url(url, wait_for=None):
        try:
            API_KEY = os.getenv("SCRAPINGBEE_KEY")

            if not API_KEY:
                raise ValueError(
                    "Les variables SCRAPINGBEE_KEY sont requises dans .env"
                )

            params = {
                "api_key": API_KEY,
                "url": url,
                # "premium_proxy": "true",
                # "country_code": "ca",
                "wait_for": f"{wait_for}",
                "return_page_source": "true",
            }

            if wait_for is not None:
                params["wait_for"] = wait_for

            response = requests.get(
                url="https://app.scrapingbee.com/api/v1",
                params=params,
            )

            # print('Response HTTP Status Code: ', response.status_code)
            # print('Response HTTP Response Body: ', response.content)
            if response.status_code == 200:
                content_str = response.content.decode("utf-8")
                return content_str
            else:
                print(f"Code {response.status_code} pendant la requête")

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erreur lors de la requête à ScrapingBee : {e}"
            )
