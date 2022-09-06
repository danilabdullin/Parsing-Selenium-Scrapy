from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import sys
from hotelparser import settings
from hotelparser.spiders.hotel import HotelSpider



def run(q):
    if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(HotelSpider, search=q)

    process.start()


