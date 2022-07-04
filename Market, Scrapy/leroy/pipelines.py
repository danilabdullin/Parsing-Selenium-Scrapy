
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from pymongo import MongoClient


class LeroyPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy

    def process_item(self, item, spider):
        item['price'] = item['price'][0]
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item


class LeroyPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        img_folder = item['name']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        result = f'/{img_folder}/{image_guid}.jpg'
        return result