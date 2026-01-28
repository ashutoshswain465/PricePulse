import requests
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime

print("Book Price Scraper")
print("==================\n")

URL = "https://books.toscrape.com/"
response = requests.get(URL)

if response.status_code == 200:
    print("Scraping book information...\n")

soup = BeautifulSoup(response.content, "html.parser")

books = soup.find_all("article", class_="product_pod")

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
scraped_data = []

for book in books[:3]:
    title = book.h3.a["title"]
    price_text = book.find("p", class_="price_color").text
    price = float(price_text.replace('£', ''))
    availability = book.find("p", class_="instock availability").text.strip()

    scraped_data.append({
        'timestamp': timestamp,
        'title': title,
        'price': price,
        'availability': availability
    })

print(f"Scarped {len(scraped_data)} books successfully!\n")

filename = 'books_data.csv'
file_exists = os.path.exists(filename)

print(f"Saving to {filename}...")

with open(filename, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['timestamp', 'title', 'price', 'availability'])

    if not file_exists:
        writer.writeheader()

    writer.writerows(scraped_data)

print(f"Data saved with timestamp: {timestamp}\n")

prices = [book['price'] for book in scraped_data]

print("Summary:")
print("--------")
print(f"Total books scraped: {len(scraped_data)}")
print(f"Lowest price: £{min(prices):.2f}")
print(f"Highest price: £{max(prices):.2f}")
print(f"Average price: £{sum(prices)/len(prices):.2f}\n")

print(f"Data saved to: {filename}")
