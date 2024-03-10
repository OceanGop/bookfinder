from urllib.parse import quote_plus as quote
import requests
from typing import NamedTuple


class Book(NamedTuple):
    title: str
    url: str
    # short_description: [None, str]


class Source:
    host: str = ''
    books: list = []
    timeout: int = 10

    @classmethod
    async def get_books(cls):
        pass

    @classmethod
    def search_by_title(cls, book_title):
        pass

    @classmethod
    def search_by_author(cls):
        pass


class MyBookSource(Source):
    host = 'mybook.ru'

    @classmethod
    def search_by_title(cls, book_title):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        url_template = f'https://mybook.ru/search/?q={quote(book_title)}'
        response = requests.get(url_template, headers=headers)
        html = response.text

        def parse_books(_html) -> list[type[Book]]:
            pass

        books = parse_books(html)




