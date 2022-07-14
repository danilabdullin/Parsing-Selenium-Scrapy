from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from marketparser import settings
from marketparser.spiders.chrome import ChromeSpider

if __name__ =='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(ChromeSpider)

    process.start()
