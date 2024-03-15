from urllib.parse import quote_plus as quote
from typing import NamedTuple

import requests
from lxml import etree

from . import config


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


# class MyBookSource(Source):
#     host = 'mybook.ru'
#
#     @classmethod
#     def search_by_title(cls, title):
#         headers = {
#             'User-Agent': settings.USER_AGENT,
#         }
#         url_template = f'https://mybook.ru/search/books/?q={quote(title)}'
#         response = requests.get(url_template, headers=headers)
#         html = response.text
#
#         def parse_books(_html) -> list[Book]:
#             _books = list()
#             tree = etree.fromstring(_html, etree.HTMLParser())
#             elements = tree.xpath('//h1/../div/div[./div/div/a/p]')
#             for element in elements:
#                 book_title = element.xpath('./div/a/p/text()')[0]
#                 book_url = element.xpath('./div/a/@href')[0]
#                 _books.append(Book(book_title, book_url))
#             return _books
#
#         cls.books = parse_books(html)

class MyBookSource(Source):
    host = 'mybook.ru'

    @classmethod
    def search_by_title(cls, title):
        url_template = f'https://mybook.ru/search/books/?q={quote(title)}'

    @staticmethod
    def parse_etree(tree) -> list[Book]:
        _books = list()
        elements = tree.xpath('//h1/../div/div[./div/div/a/p]')
        for element in elements:
            book_title = element.xpath('./div/a/p/text()')[0]
            book_url = element.xpath('./div/a/@href')[0]
            _books.append(Book(book_title, book_url))
        return _books

m = MyBookSource.search_by_title(12312)

