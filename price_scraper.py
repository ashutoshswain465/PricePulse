"""
THE APP:
Web scraper that extracts book information (title, price, availability)
from books.toscrape.com and displays it in the console.

WHAT TO FIGURE OUT:
- How do you fetch a webpage with Python?
- How do you parse HTML content?
- How do you find specific elements in HTML?
- How do you extract text from HTML elements?
- How do you handle multiple items on a page?

START HERE:
First, just try to fetch the webpage and print the HTML.
Then parse it with BeautifulSoup and find one book.
Finally, loop through multiple books and extract their data.

KEY CONCEPT:
Use requests.get() to fetch webpage content.
BeautifulSoup parses HTML into a searchable structure.
Use .find() for single elements, .find_all() for multiple.
Access element attributes with bracket notation: element['attribute']
Use .text to get the text content of an element.
"""

# ---------------------------------------------
# THE CODE SKELETON

# Import necessary libraries
# (requests for HTTP, BeautifulSoup for HTML parsing)
import requests
from bs4 import BeautifulSoup


# Print header
print("Book Price Scraper")
print("==================")


# Define the URL to scrape
# (books.toscrape.com homepage)
URL = "https://books.toscrape.com/"


# Print status message


# Fetch the webpage
# (use requests.get() to download the page)
response = requests.get(URL)
print(response.status_code)


# Parse the HTML content
# (use BeautifulSoup with 'html.parser')



# Find all book elements on the page
# (each book is in an <article> tag with class 'product_pod')


# Initialize counter


# Loop through the first 3 books
# (slice the list to get only first 3: books[:3])

# Extract the book title
# (title is in h3 > a tag, stored in 'title' attribute)


# Extract the price
# (price is in <p> tag with class 'price_color')


# Extract availability
# (availability is in <p> tag with class 'instock availability')
# (use .strip() to remove extra whitespace)


# Print the book information


# Increment counter


# Print completion message


