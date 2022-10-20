import pandas as pd
import requests as re
from bs4 import BeautifulSoup

from File import File


class ProductScrapper:

    def __init__(self):
        self.f = File()

    def scrape_products(self, filename):
        products = []
        product_urls = self.f.read_txt(filename)

        try:
            for url in product_urls:
                soup = self._create_soup(url)
                title = self._get_product_title(soup)
                price = self._get_product_price(soup)

                if title == None or price == None:
                    continue

                products.append({"title": title, "price": price, "url": url})
            return products
        except Exception as e:
            return None

    def create_product_csv(self, filename, products):
        fields = ["title", "price", "url"]
        self.f.create_csv(filename, fields, products)

    def find_potential_buys(self, filename, new_products):
        old_products = pd.read_csv(filename)
        new_products = self._reformat_products(new_products)
        potential_buys = {}
        for url in new_products:
            product_row = old_products.loc[old_products["url"] == url]
            if not product_row.empty:
                old_price = product_row.iloc[0]["price"]
                new_price = new_products[url]["price"]
                price_diff = ((new_price - old_price)/old_price) * 100
                if price_diff < -10:
                    potential_buys[url] = {"title": new_products[url]["title"], "old_price": old_price,
                                           "new_price": new_price, "precentage_decrease": round(price_diff, 2)}

        return potential_buys

    def _create_soup(self, url):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        }

        response = re.get(url, headers=headers)
        return BeautifulSoup(response.content, "html.parser")

    def _get_product_title(self, soup):
        try:
            title = soup.select_one("#productTitle")
            return title.text.strip()
        except Exception as e:
            return None

    def _get_product_price(self, soup):
        try:
            price = soup.select_one(".a-offscreen")
            price = price.text.strip()
            return float(price[1:])
        except Exception as e:
            return None

    def _reformat_products(self, products):
        reformatted_products = {}

        for product in products:
            reformatted_products[product["url"]] = {
                "price": product["price"], "title": product["title"]}

        return reformatted_products
