import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class Books25Spider(scrapy.Spider):
    name = 'books25'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='product-card__name smartLink']/@href").extract()
        for link in links:
            yield response.follow(link,callback=self.book_parse)
        for i in range(0, 25):
            next_page = f'https://book24.ru/search/page-{i}/?q=%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F'
            yield response.follow(next_page, callback=self.parse)


    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").extract()
        price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").extract()
        url = response.url
        author = None
        yield BooksparserItem(name=name, price=price, url=url, author=author)