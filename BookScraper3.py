import requests
from bs4 import BeautifulSoup
import csv
import os

# Base URL of the site to scrape
BASE_URL = 'http://books.toscrape.com/'

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
            image_url = BASE_URL + article.find('div', class_='image_container').find('img')['src'].replace('../', '')
            books.append([title, price, availability, image_url])
        
        next_button = soup.find('li', class_='next')
        if next_button:
            url = BASE_URL + 'catalogue/' + next_button.find('a')['href']
        else:
            break
    return books

def download_image(image_url, category, title):
    """Download and save an image to the specified category folder."""
    response = requests.get(image_url)
    response.raise_for_status()
    # Sanitize the title to remove characters not allowed in filenames
    safe_title = ''.join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).rstrip()
    file_path = os.path.join('images', category, f'{safe_title[:50]}.jpg')  # Limit title to 50 chars to avoid too long filenames
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(response.content)

def write_books_to_csv(category, books):
    """Write books of a specific category to a CSV file within 'all_csvs' folder."""
    os.makedirs('all_csvs', exist_ok=True)
    filename = os.path.join('all_csvs', f'{category}.csv')
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Availability', 'Image URL'])
        for book in books:
            writer.writerow(book[:3])  # Write book details excluding the image URL
            download_image(book[3], category, book[0])  # Download image

def main():
    category_links = get_category_links()
    for category, url in category_links.items():
        print(f'Scraping category: {category}')
        books = scrape_books(category, url)
        write_books_to_csv(category, books)

if __name__ == '__main__':
    main()
