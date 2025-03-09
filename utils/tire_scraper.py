import requests
from bs4 import BeautifulSoup
from utils.tire import Tire

class TireScraper:
    def __init__(self, width, profile, size):
        self.width = width
        self.profile = profile
        self.size = size
        self.tires = []

    def scrape_tire_stock(self):
        BASE_URL = "https://www.alphatires.ca/?post_type=product&ad_search=1&width={}&profile={}&wheel-size={}"
        search_url = BASE_URL.format(self.width, self.profile, self.size)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            return {"error": "Failed to fetch data from Alpha Tires."}

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("li", class_="wc-block-product")

        for result in results:
            name_tag = result.find("h3")
            price_tag = result.find("span", class_="woocommerce-Price-amount")
            stock_tag = result.find("span", class_="stock-badge")

            name = name_tag.text.strip() if name_tag else "Unknown Tire"
            price = price_tag.text.strip() if price_tag else "Price unavailable"
            low_stock = "Low stock" in stock_tag.text if stock_tag else False

            self.tires.append(Tire(name, low_stock, price))

        return self.tires