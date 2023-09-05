from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp

url = "https://books.toscrape.com/"

async def parser(page_num: int) -> None:
    books_data = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}/catalogue/page-{page_num}.html") as response:
            response = await response.text()
            soup = BeautifulSoup(response, "html.parser")
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
            print(books_data)

async def main():
    async_list = []
    for page_num in range(1, 51):
        task = asyncio.create_task(parser(page_num=page_num))
        async_list.append(task)
    await asyncio.gather(*async_list)

asyncio.run(main())
