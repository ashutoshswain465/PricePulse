import requests
from bs4 import BeautifulSoup


print("Book Price Scraper")
print("==================\n")

URL = "https://books.toscrape.com/"
response = requests.get(URL)

if response.status_code == 200:
    print("Scraping book information...\n")

soup = BeautifulSoup(response.content, "html.parser")


books = soup.find_all("article", class_="product_pod")


counter = 0

for book in books[:3]:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    availability = book.find("p", class_="instock availability").text.strip()

    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Availability: {availability}\n")
    counter += 1


print("\nScraping complete!")
print("Total books found: " + str(counter))
