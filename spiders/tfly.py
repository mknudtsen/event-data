from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import Join, MapCompose
from scrapy.http import Request
from datetime import date
from scrapy.shell import inspect_response
from urlparse import urljoin
import scrapy

from build_db.items import EventItem, EventLoader, UrlItem
from build_db.venues import get_scrape_urls, get_venue_id


class Recursive(CrawlSpider):
    name = 'tfly'
    allowed_domains = ['www.ticketfly.com']
    start_urls = get_scrape_urls('ticketfly')

    events_list_xpath = '//div[starts-with(@class, "event-results")]/ul/' \
                        'li[starts-with(@class, "list-view-item vevent")]'


    def parse_event_detail(self, response):
        item = response.meta['item']
        loader = EventLoader(item, response=response)
        loader.add_xpath('age_restriction', './/p[starts-with(@class, "age-restriction")]/text()')
        loader.add_value('age_restriction', 'NA')
        loader.add_xpath('promoter',        './/p[starts-with(@class, "event-sponsor")]/text()')
        loader.add_value('promoter',        'NA')

        # Complete the loader, yielding the completed item
        return loader.load_item()


    def parse(self, response):
        selector = Selector(response)
        venue_id = get_venue_id(response.url)

        #iterate over each event
        for event in selector.xpath(self.events_list_xpath):
            loader = EventLoader(EventItem(), selector=event)
            loader.add_xpath('title',       './/a/img[@class="event-results-image"]/@title')
            loader.add_xpath('event_url',   './/div[starts-with(@class, "event-results-content")]/a/@href')
            loader.add_xpath('artists',     './/div[starts-with(@class, "event-results-titles")]/h3[starts-with(@class, "headliners summary")]/'
                                            'a/text()')
            loader.add_xpath('artists',     './/div[starts-with(@class, "event-results-titles")]/'
                                            'p[starts-with(@class, "event-results-openers description")]/a/text()')
            loader.add_xpath('event_ts',    './/div[starts-with(@class, "event-date dtstart")]/span[starts-with(@class, "value-title")]/@title')
            loader.add_xpath('ticket_price','.//div[starts-with(@class, "event-results-ticket-price")]/'
                                            'p[starts-with(@class, "event-price")]/text()')
            loader.add_value('ticket_price','NA')
            loader.add_xpath('status',      './/div[starts-with(@class, "event-results-ticket-price")]/'
                                            'span[starts-with(@class, "button radius small sold-out")]/text()')
            loader.add_xpath('status',      './/div[starts-with(@class, "event-results-ticket-price")]/'
                                            'span[starts-with(@class, "ticket-link primary-link")]/'
                                            'a[starts-with(@class, "button radius small green tickets")]/text()')
            loader.add_xpath('status',      './/div[starts-with(@class, "event-results-ticket-price")]/'
                                            'span[starts-with(@class, "button radius")]/text()')        
            loader.add_value('status',      'NA')            
            loader.add_xpath('purchase_url','.//div[starts-with(@class, "event-results-ticket-price")]/'
                                            'span[starts-with(@class, "ticket-link primary-link")]/'
                                            'a[starts-with(@class, "button radius small green tickets")]/@href')
            loader.add_value('purchase_url','NA')
            loader.add_value('venue_id',     str(venue_id))
            #loader.add_value('last_update',  str(date.today()))

            event_url = urljoin(response.url,loader.get_output_value('event_url'))   
            item = loader.load_item()
            yield scrapy.Request(url=event_url,
                                 meta={'item': item},
                                 callback=self.parse_event_detail,
                                 dont_filter=True)

