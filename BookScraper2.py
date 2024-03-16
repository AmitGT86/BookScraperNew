import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = "http://books.toscrape.com/"

def scrape_book_details(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text
    price = soup.find('p', class_='price_color').text
    stock = soup.find('p', class_='instock availability').text.strip()
    description = soup.find('meta', attrs={'name': 'description'})['content'].strip()
    category = soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()
    rating = soup.find('p', class_='star-rating')['class'][1]
    return {
        'title': title,
        'price': price,
        'stock': stock,
        'description': description,
        'category': category,
        'rating': rating
    }

def get_category_urls():
    url = BASE_URL + "index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return {a.text.strip(): BASE_URL + a['href'] for a in soup.find('div', class_='side_categories').find('ul').find('li').find_all('a')}

def scrape_category(category_name, category_url):
    books = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        book_urls = [BASE_URL + 'catalogue/' + a.find('a')['href'].replace('../', '') for a in soup.find_all('h3')]
        
        for book_url in book_urls:
            books.append(scrape_book_details(book_url))
        
        next_button = soup.find("li", class_="next")
        if next_button:
            next_page_partial_url = next_button.find("a")["href"]
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_page_partial_url
        else:
            category_url = None

    return books


def save_to_csv(books, category_name):
    df = pd.DataFrame(books)
    filename = f'{category_name.replace(" ", "_").lower()}.csv'
    df.to_csv(filename, index=False)

def main():
    categories = get_category_urls()
    for category_name, category_url in categories.items():
        print(f"Processing category: {category_name}")
        books = scrape_category(category_name, category_url)
        save_to_csv(books, category_name)
        print(f"Finished processing {category_name}. Data saved to CSV.")

if __name__ == "__main__":
    main()
