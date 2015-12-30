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
    title = Field()
    status = Field()
    ticket_price = Field()
    event_ts = Field()
    event_url = Field()
    purchase_url = Field()
    artists = Field()
    promoter = Field()
    venue_id = Field()
    age_restriction = Field()


class EventLoader(ItemLoader):

    default_input_processor = MapCompose(remove_entities, unicode.strip)
    default_output_processor = Join(',')

    status_out = TakeFirst()
    ticket_price_out = TakeFirst()
    purchase_url_out = TakeFirst()
    age_restriction_out = TakeFirst()
    promoter_out = TakeFirst()