import scrapy
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from booksparser import settings
from booksparser.spiders.labirint import LabirintSpider
from booksparser.spiders.books25 import Books25Spider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpider)
    process.start()

    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]

    process.crawl(Books25Spider)
    process.start()
