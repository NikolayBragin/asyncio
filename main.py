import requests
from bs4 import BeautifulSoup
import time

books_data = []
start_time = time.time()
books_extracted = 0


for page_num in range(1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('h3')
    for book in books:
        book_url = book.find('a')['href']
        book_response = requests.get('https://books.toscrape.com/catalogue/' + book_url)
        book_soup = BeautifulSoup(book_response.content, 'html.parser')
        title = book_soup.find('h1').text
        price = book_soup.find('p', class_='price_color').text
        availability = book_soup.find('p', class_='availability').text.strip()
        image = book_soup.find('img')['src']
        books_data.append([title, price, availability, image])
        print(f'Название: {title}\nЦена: {price}\nНаличие: {availability}\nСсылка на фото: {image}\n')
        books_extracted += 1
        end_time = time.time()
    total_time = (end_time - start_time)
print(f'Мы спарсили {books_extracted} книг за {total_time} сек.\n')
print(books_data)