import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyItem
from scrapy.loader import ItemLoader


class EkonomstroySpider(scrapy.Spider):
    name = 'ekonomstroy'
    allowed_domains = ['ekonomstroy.ru']
    start_urls = ['https://www.ekonomstroy.ru/catalog/svetilniki/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@title='Следующая страница']/@href").extract_first()
        goods = response.xpath("//a[@class='bx_catalog_item_images']/@href")
        for good in goods:
            yield response.follow(good, callback=self.parse_goods)
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_goods(self, response: HtmlResponse):
        # print() #остановка для отладки
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@class='span_price']/text()")
        loader.add_xpath('props', "//dl")
        loader.add_xpath('photos', "//span[@class='cnt']")
        yield loader.load_item()


