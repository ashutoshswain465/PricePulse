import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

print("Automated Book Price Monitor")
print("============================\n")

price_targets = {
    'A Light in the Attic': 50.00,
    'Tipping the Velvet': 52.00,
    'Soumission': 52.00
}

print("Loading price targets...")
print(f"Monitoring {len(price_targets)} books for price drops\n")

conn = sqlite3.connect('books.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        title TEXT,
        price REAL,
        availability TEXT
    )
''')
conn.commit()

url = "http://books.toscrape.com/"

print("Running price check...")

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

books = soup.find_all('article', class_='product_pod')

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
scraped_data = []

for book in books[:20]:
    title = book.h3.a['title']
    price_text = book.find('p', class_='price_color').text
    price = float(price_text.replace('£', ''))
    availability = book.find('p', class_='instock availability').text.strip()

    scraped_data.append((timestamp, title, price, availability))

    cursor.execute('''
        INSERT INTO books (timestamp, title, price, availability)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, title, price, availability))

conn.commit()
conn.close()

print(f"Scraped {len(scraped_data)} books successfully!\n")

print("Checking against your targets...\n")

deals_found = []

for timestamp, title, price, availability in scraped_data:
    if title in price_targets:
        target_price = price_targets[title]
        if price <= target_price:
            deals_found.append({
                'title': title,
                'current_price': price,
                'target_price': target_price,
                'savings': target_price - price
            })

if deals_found:
    print("🎯 DEALS FOUND!")
    print("---------------")
    for deal in deals_found:
        print(f"✅ {deal['title']}")
        print(f"   Current: £{deal['current_price']:.2f} | Target: £{deal['target_price']:.2f}")
        print(f"   Status: BELOW TARGET! 🎉\n")

    sender_email = os.getenv('SENDER_EMAIL', 'your_email@gmail.com')
    sender_password = os.getenv('SENDER_PASSWORD', 'your_app_password')
    recipient_email = os.getenv('RECIPIENT_EMAIL', 'your_email@gmail.com')

    print("📧 Sending email alert...")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"🎯 Price Alert: {len(deals_found)} Books Below Target!"

    email_body = "Hello!\n\n"
    email_body += f"Great news - we found {len(deals_found)} books below your target prices:\n\n"

    for i, deal in enumerate(deals_found, 1):
        email_body += f"{i}. {deal['title']}\n"
        email_body += f"   Current Price: £{deal['current_price']:.2f}\n"
        email_body += f"   Your Target: £{deal['target_price']:.2f}\n"
        email_body += f"   Savings: £{deal['savings']:.2f}\n\n"

    email_body += "Happy shopping!"

    msg.attach(MIMEText(email_body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to: {recipient_email}\n")
        email_sent = True
    except Exception as e:
        print(f"Email not sent (configure .env file with credentials)\n")
        email_sent = False

    print("Summary:")
    print("--------")
    print(f"Books monitored: {len(price_targets)}")
    print(f"Deals found: {len(deals_found)}")
    print(f"Email sent: {'✓' if email_sent else '✗'}\n")

else:
    print("No deals found - all prices above targets\n")
    print("Summary:")
    print("--------")
    print(f"Books monitored: {len(price_targets)}")
    print(f"Deals found: 0\n")

next_check = datetime.now() + timedelta(days=1)
print(f"Next check scheduled for: {next_check.strftime('%Y-%m-%d %H:%M:%S')}")
