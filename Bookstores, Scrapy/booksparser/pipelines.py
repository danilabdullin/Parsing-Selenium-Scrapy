import re
from pymongo import MongoClient
class BooksparserPipeline:


    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['author'], item['name'] = self.process_name(item['name'])
        if spider.name == 'labirint':
            item['price'] = int(item['price'][0])
            collection.insert_one(item)
        return item

    def process_name(self, name):

        result = re.split(':', name[0])
        author = result[0]
        name = result[1]
        return author, name

