import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem



class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/психология/?stype=0']

    def parse(self, response:HtmlResponse):

        links = response.xpath("//a[@class='product-title-link']/@href").extract()
        next_page = response.xpath("//a[@title='Следующая']/@href").extract_first()
        for link in links:
            yield response.follow(link,callback=self.book_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//div[@id='product-title']/h1/text()").extract()
        price = response.xpath("//div[@class='buying-pricenew-val']/span/text()").extract()
        url = response.url
        author = None
        yield BooksparserItem(name=name, price=price, url=url, author=author)


