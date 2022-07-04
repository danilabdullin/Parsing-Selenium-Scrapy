
import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.selector import Selector
import re

def photos_url(value):
    value = Selector(text=value)
    link = value.xpath("//@style").extract()
    result = re.split('\(', link[0])
    result = re.split('\)', result[1])
    result = "".join(result[0])

    def removing(r):
        r = list(r)
        for i in r:
            if i == "'":
                r.remove(i)
            if i == ';':
                r.remove(i)
        return "".join(r)
    final_link = 'https://www.ekonomstroy.ru' + removing(result)
    return final_link



def parse_props(value):
    if value:
        # преобразовываем в selector и вытаскиваем список селекторов со свойствами
        r = Selector(text=value)
        prop_name = r.xpath('//dt/text()').extract()
        prop_value = r.xpath('//dd/text()').extract()


        result = {}
        result2 = {}
        list = dict(zip(prop_name, prop_value))
        for i, j in list.items():
            i = re.sub(' ', '', i)
            j = re.sub(' ', '', j)
            result[i] = j
        for i, j in result.items():
            i = i.replace('\n', '')
            result2[i] = j
        value = result2
    return value

def price_clean(price):
    price = price.replace('\n', '').replace('\t', '').replace(' ', '')


    return price

class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_clean))
    props = scrapy.Field(input_processor=MapCompose(parse_props))
    photos = scrapy.Field(input_processor=MapCompose(photos_url))
    _id = scrapy.Field()



