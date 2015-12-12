# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.utils.markup import remove_entities


class UrlItem(Item):
    start_url = Field()
    url = Field()


class EventItem(Item):
    name = Field()
    status = Field()
    price = Field()
    date = Field()
    url = Field()
    artists = Field()
    venue_id = Field()
    last_update = Field()


class EventItemSpecial(Item):
    name = Field()
    status = Field()
    price = Field()
    date = Field()
    time = Field()
    url = Field()
    detail_url = Field()
    artists = Field()
    venue_id = Field()
    last_update = Field()
    age = Field()


class EventLoader(ItemLoader):

    default_input_processor = MapCompose(remove_entities, unicode.strip)
    default_output_processor = Join(',')

    status_out = TakeFirst()
    price_out = TakeFirst()