from urllib.parse import quote_plus as quote
from typing import NamedTuple

import requests
from lxml import etree


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
        url_template = f'https://mybook.ru/search/books/?q={quote(book_title)}'
        response = requests.get(url_template, headers=headers)
        html = response.text

        def parse_books(_html) -> list[type[Book]]:
            _books = list()
            tree = etree.fromstring(_html, etree.HTMLParser())
            elements = tree.xpath('//h1/../div/div[./div/div/a/p]')
            for element in elements:
                book_title = element.xpath('./div/a/p/text()')[0]
                book_url = element.xpath('./div/a/@href')[0]
                _books.append(Book(book_title, book_url))
            return _books

        cls.books = parse_books(html)




