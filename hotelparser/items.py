
from itemloaders.processors import MapCompose, TakeFirst
import scrapy

def props_clean(props):
    result = []
    result.append(props.replace('\n', '').replace('\r', '').replace(' ', '').replace('\r\n', '').replace('\ufeff', ''))
    result = list(filter(None, result))

    return result




class HotelparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    props = scrapy.Field(input_processor=MapCompose(props_clean))
    link = scrapy.Field(output_processor=TakeFirst())
    region = scrapy.Field()
    address = scrapy.Field()
    INN = scrapy.Field()
    OGRN = scrapy.Field()
    stars = scrapy.Field()
    type = scrapy.Field()
    room_1 = scrapy.Field()
    room_2 = scrapy.Field()
    room_3 = scrapy.Field()
    room_4 = scrapy.Field()
    room_5 = scrapy.Field()
    _id = scrapy.Field()

