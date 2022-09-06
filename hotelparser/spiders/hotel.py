import scrapy
from scrapy.http import HtmlResponse
from hotelparser.items import HotelparserItem
from scrapy.loader import ItemLoader
import time


main_link = 'http://классификация-туризм.рф'
additional_link = 'http://классификация-туризм.рф/displayAccommodation/index'
class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = ['классификация-туризм.рф', 'xn----7sba3acabbldhv3chawrl5bzn.xn--p1ai']

    def __init__(self, search):
        self.start_urls = [search]

    def parse(self, response:HtmlResponse):
        links = response.xpath("//div[@class='object']/a/@href").extract()
        next_page = response.xpath("//li[@class='next']/a/@href").extract_first()
        for link in links:
            yield response.follow(link, callback=self.hotel_parse)
            time.sleep(1)

        if next_page:
            yield response.follow(next_page, callback=self.parse)



    def hotel_parse(self, response:HtmlResponse):
        loader = ItemLoader(item=HotelparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('props', "//div[@class='detail-fields']//text()")
        loader.add_value('link', response.url)
        yield loader.load_item()

