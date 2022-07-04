import scrapy

class BooksparserItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    _id = scrapy.Field()

