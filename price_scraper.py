import requests
import sqlite3
import time
# import csv
# import os
from bs4 import BeautifulSoup
from datetime import datetime

print("Book Price Tracker")
print("==================\n")

URL = "https://books.toscrape.com/"


def scrape(url):
    response = requests.get(url)

    if response.status_code == 200:
        print("Scraping book information...\n")

    subject = response.content
    return subject


def parse(topic):
    soup = BeautifulSoup(topic, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    scraped_data = []

    for book in books[:20]:
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
    return scraped_data


def store(book_data, retries=5):
    for attempt in range(retries):
        try:
            with sqlite3.connect("books.db", timeout=10) as conn:
                ptr = conn.cursor()
                sql = '''
                    INSERT INTO books (timestamp, title, price, availability) 
                    VALUES (:timestamp, :title, :price, :availability)
                '''

                ptr.executemany(sql, book_data)
                conn.commit()
                print(f"{len(book_data)} records entered successfully!")
        except sqlite3.OperationalError as e:
            print(f"[Retry {attempt + 1}] SQLite error: {e}")
            time.sleep(1)
    raise Exception("Failed to write to database after multiple attempts.")


def summary(db_path, retries=5):
    for attempt in range(retries):
        try:
            with sqlite3.connect(db_path) as conn:
                csr = conn.cursor()

                query = '''
                    SELECT 
                        COUNT(CASE WHEN prev_price IS NULL THEN 1 END) as new_books,
                        COUNT(CASE WHEN price > prev_price THEN 1 END) as increases,
                        COUNT(CASE WHEN price < prev_price THEN 1 END) as decreases,
                        COUNT(CASE WHEN price <> prev_price AND prev_price IS NOT NULL THEN 1 END) as total_changes
                    FROM (
                        SELECT 
                            price,
                            LAG(price) OVER (PARTITION BY book_name ORDER BY timestamp) as prev_price
                        FROM books
                    )
                '''

                csr.execute(query)
                new_books, increased, decreased, total_changes = csr.fetchone()

                print("--- Complete Database Summary ---")
                print(f"New Books Added: {new_books}")
                print(f"Total Price Changes: {total_changes}")
                print(f"Increases: {increased}")
                print(f"Decreases: {decreased}")
        except sqlite3.OperationalError as e:
            print(f"[Retry {attempt + 1}] SQLite error: {e}")
            time.sleep(1)
    raise Exception("Failed to write to database after multiple attempts.")


if __name__ == "__main__":
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            title TEXT NOT NULL,
            price DECIMAL(10, 2),
            availability TEXT
        )""")

    connection.commit()
    connection.close()

    while True:
        content = scrape(URL)
        data = parse(content)
        store(data)
        summary("books.db")
