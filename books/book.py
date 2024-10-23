from pprint import pprint

from urllib.parse import quote_plus as quote
from typing import NamedTuple

import requests
from lxml import etree

# from . import config


class Book(NamedTuple):
    title: str
    url: str
    # short_description: [None, str]


class Source:
    host: str = ''
    books: list = []
    timeout: int = 10
    search_by_title_method = 'GET'

    @classmethod
    async def get_books(cls):
        pass

    # classmethod chains with another descriptors was depricated in 3.11!!!
    @classmethod
    def tree(cls, url, method='GET'):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        if cls.search_by_title_method == 'GET':
            response = requests.get(url, headers=headers)
        else:
            raise NotImplementedError
        # print(response)
        _tree = etree.fromstring(response.text, parser=etree.HTMLParser())
        return _tree

    @classmethod
    def parse_tree(cls, *args):
        raise NotImplementedError

    @staticmethod
    def search_by_title_template(title):
        raise NotImplementedError

    @classmethod
    def search_by_title(cls, book_title):
        url_template = cls.search_by_title_template(book_title)
        _tree = cls.tree(url_template)
        result = cls.parse_tree(_tree)
        return result

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

    @staticmethod
    def search_by_title_template(title):
        return f'https://mybook.ru/search/books/?q={quote(title)}'

    @classmethod
    def parse_tree(cls, tree) -> list[Book]:
        _books = list()
        elements = tree.xpath('//h1/../div/div[./div/div/a/p]')
        for element in elements:
            book_title = element.xpath('./div/a/p/text()')[0]
            book_url = f'https://{cls.host}/' + element.xpath('./div/a/@href')[0]
            _books.append(Book(book_title, book_url))
        return _books


class LitnetSource(Source):
    host = 'litnet.com'

    @staticmethod
    def search_by_title_template(title):
        return f'https://litnet.com/ru/search?q={quote(title)}'

    @classmethod
    def parse_tree(cls, tree) -> list[Book]:
        _books = list()
        elements = tree.xpath('//div[contains(@class, "book-item")]')
        for element in elements:
            book_title = element.xpath('./div/h4/a/text()')[0]
            book_url = element.xpath('./div/h4/a/@href')[0]
            book_url = f'https://{cls.host}' + book_url
            _books.append(Book(book_title, book_url))
        return _books


class LivelibSource(Source):
    host = 'livelib.ru'

    @staticmethod
    def search_by_title_template(title):
        return f'https://www.livelib.ru/find/books/{quote(title)}'

    @classmethod
    def parse_tree(cls, tree) -> list[Book]:
        _books = list()
        elements = tree.xpath('//div[@id="objects-block"]/div')
        for element in elements:
            book_title = element.xpath('.//a[@class="title"]/text()')[0]
            book_url = element.xpath('.//a[@class="title"]/@href')[0]
            book_url = f'https://{cls.host}' + book_url
            _books.append(Book(book_title, book_url))
        return _books


if __name__ == '__main__':
    for source in [MyBookSource, LitnetSource, LivelibSource]:
    # for source in [LivelibSource]:
        result = source.search_by_title('Ложная слепота')
        pprint(len(result))
        # pprint(result)

