from pymongo import MongoClient


class HotelparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.hotels

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        try:
            props_list = item['props']
            vid_idx = props_list.index("Вид:")
            item['type'] = props_list[vid_idx + 1]
            region_idx = props_list.index("Регион:")
            item['region'] = props_list[region_idx + 1]
            address_idx = props_list.index("Адресместанахождения:")
            item['address'] = props_list[address_idx + 1]
            OGRN_idx = props_list.index("ОГРН/ОГРНИП:")
            item['OGRN'] = props_list[OGRN_idx + 1]
            INN_idx = props_list.index("ИНН:")
            item['INN'] = props_list[INN_idx + 1]
            stars_idx = props_list.index("Присвоеннаякатегория:")
            item['stars'] = props_list[stars_idx + 1]
            rooms_idx = props_list.index('Количестводоп.мест')
            rooms = props_list[rooms_idx + 1:]
            rms_idx = []
            for i in rooms:
                if i.isdigit() == False:
                    rms_idx.append(rooms.index(i))

            if len(rms_idx) == 1:
                item['room_1'] = ':'.join(rooms[1:2])
            elif len(rms_idx) == 2:
                item['room_1'] = ':'.join(rooms[1:2])
                item['room_2'] = ':'.join(rooms[5:6])
            elif len(rms_idx) == 3:
                item['room_1'] = ':'.join(rooms[1:2])
                item['room_2'] = ':'.join(rooms[5:6])
                item['room_3'] = ':'.join(rooms[9:10])
            elif len(rms_idx) == 4:
                item['room_1'] = ':'.join(rooms[1:2])
                item['room_2'] = ':'.join(rooms[5:6])
                item['room_3'] = ':'.join(rooms[9:10])
                item['room_4'] = ':'.join(rooms[13:14])
            elif len(rms_idx) == 5:
                item['room_1'] = ':'.join(rooms[1:2])
                item['room_2'] = ':'.join(rooms[5:6])
                item['room_3'] = ':'.join(rooms[9:10])
                item['room_4'] = ':'.join(rooms[13:14])
                item['room_5'] = ':'.join(rooms[17:18])
        except:
            pass

        collection.insert_one(item)
        return item
