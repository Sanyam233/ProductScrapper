import os.path as path

from ProductScrapper import ProductScrapper


# Variables to change
txt_file = "product_urls.txt"
csv_file = "amazon_products.csv"

scrapper = ProductScrapper()

# scrape products
products = scrapper.scrape_products(txt_file)

if not path.isfile("./" + csv_file):
    scrapper.create_product_csv(csv_file, products)
else:
    potential_buys = scrapper.find_potential_buys(
        csv_file, products)
    print(potential_buys)
    scrapper.create_product_csv(csv_file, products)
