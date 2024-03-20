import requests
from bs4 import BeautifulSoup
import csv
import os

def get_soup(url):
    """Return a BeautifulSoup object for a given URL."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_books_urls(category_url):
    """Retrieve all book URLs within a given category, handling pagination."""
    books_urls = []
    while category_url:
        soup = get_soup(category_url)
        for book in soup.select('h3 a'):
            book_url = 'http://books.toscrape.com/catalogue/' + book['href'].replace('../../..', '')
            books_urls.append(book_url)
        
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_partial_url = next_button.find('a')['href']
            category_url = os.path.join(category_url.rsplit('/', 2)[0], next_page_partial_url)
        else:
            category_url = None
    return books_urls

def scrape_book_data(book_url):
    """Scrape details of a book given its product page URL."""
    soup = get_soup(book_url)
    title = soup.find('div', class_='product_main').find('h1').text
    price = soup.find('p', class_='price_color').text[1:]  # Remove currency symbol
    availability = soup.find('p', class_='instock availability').text.strip()
    image_url = 'http://books.toscrape.com/' + soup.find('div', class_='item active').find('img')['src'].replace('../../', '')
    return [title, price, availability, image_url]

def write_books_to_csv(category_name, books_data):
    """Write book details to a CSV file."""
    filename = f'{category_name}.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Availability', 'Image URL'])
        writer.writerows(books_data)
    print(f'Saved {len(books_data)} books in {filename}')

def main():
    # URL of the "Science" category, replace this with your desired category URL
    category_url = 'http://books.toscrape.com/catalogue/category/books/science_22/index.html'
    category_name = 'Science'
    
    books_urls = get_books_urls(category_url)
    books_data = []
    for book_url in books_urls:
        book_data = scrape_book_data(book_url)
        books_data.append(book_data)
    
    write_books_to_csv(category_name, books_data)

if __name__ == '__main__':
    main()
