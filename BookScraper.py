import requests
from bs4 import BeautifulSoup
import pandas as pd

# scrape_book_details function here (as you provided)

def scrape_book_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    title = soup.find('h1').text
    price_incl_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text
    price_excl_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text
    upc = soup.find('th', string='UPC').find_next_sibling('td').text
    quantity = soup.find('th', string='Availability').find_next_sibling('td').text.split('(')[1].split(' ')[0]

    description = soup.find('meta', attrs={'name': 'description'})['content'].strip()
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = soup.find('img')['src'].replace('../../', 'http://books.toscrape.com/')

    book_details = {
        'product_page_url': url,
        'universal_product_code': upc,
        'book_title': title,
        'price_including_tax': price_incl_tax,
        'price_excluding_tax': price_excl_tax,
        'quantity_available': quantity,
        'product_description': description,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url
    }
    return book_details

book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
book_details = scrape_book_details(book_url)

# Writing to CSV
#df = pd.DataFrame([book_details])
#df.to_csv('single_book_details.csv', index=False)







def get_books_in_category(category_url):
    books = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        book_urls = [book.find("a")["href"].replace('../../../', 'http://books.toscrape.com/catalogue/')
                     for book in soup.find_all("h3")]
        
        for book_url in book_urls:
            books.append(scrape_book_details(book_url))
        
        next_button = soup.find("li", class_="next")
        if next_button:
            next_page_partial_url = next_button.find("a")["href"]
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_page_partial_url
        else:
            category_url = None

    return books

# Example usage
category_url = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
books_in_category = get_books_in_category(category_url)

# Writing all books in the category to a single CSV
df = pd.DataFrame(books_in_category)
df.to_csv('category_books_details.csv', index=False)
