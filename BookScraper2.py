import requests
from bs4 import BeautifulSoup
import csv
import os

# Base URL of the site to scrape
BASE_URL = 'http://books.toscrape.com/'

# Ensure the directory for CSVs exists
CSV_DIR = 'all_csvs'
os.makedirs(CSV_DIR, exist_ok=True)

def get_soup(url):
    """Return a BeautifulSoup object for a given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response was an error
    return BeautifulSoup(response.text, 'html.parser')

def get_category_links():
    """Retrieve a dictionary of book categories and their URLs."""
    soup = get_soup(BASE_URL)
    category_links = {}
    for category in soup.find('div', class_='side_categories').find_all('a')[1:]:  # Skip the first one as it's 'Books'
        name = category.get_text().strip()
        link = BASE_URL + category['href']
        category_links[name] = link
    return category_links

def scrape_books(category, url):
    """Scrape book details from a given category page."""
    books = []
    while True:
        soup = get_soup(url)
        for article in soup.find_all('article', class_='product_pod'):
            title = article.find('h3').find('a')['title']
            price = article.find('p', class_='price_color').text[1:]  # Remove currency symbol
            availability = article.find('p', class_='instock availability').text.strip()
            books.append([title, price, availability])
        
        next_button = soup.find('li', class_='next')
        if next_button:
            url = BASE_URL + 'catalogue/' + next_button.find('a')['href']
        else:
            break
    return books

def write_books_to_csv(category, books):
    """Write books of a specific category to a CSV file."""
    filename = os.path.join(CSV_DIR, f'{category}.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Availability'])
        writer.writerows(books)
    print(f'Saved {len(books)} books in {filename}')

def main():
    category_links = get_category_links()
    for category, url in category_links.items():
        print(f'Scraping category: {category}')
        books = scrape_books(category, url)
        write_books_to_csv(category, books)

if __name__ == '__main__':
    main()
