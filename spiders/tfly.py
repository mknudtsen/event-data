from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import Join, MapCompose
from scrapy.http import Request
from datetime import date
from scrapy.shell import inspect_response
from urlparse import urljoin
import scrapy
#from scrapy.utils.response import open_in_browser

from build_db.items import EventItemSpecial, EventLoader, UrlItem
from build_db.venues import get_scrape_urls, get_venue_id


class Recursive(CrawlSpider):
    name = 'tfly'
    allowed_domains = ['www.ticketfly.com']
    start_urls = get_scrape_urls('ticketfly')

    events_list_xpath = '//div[starts-with(@class, "event-results")]/ul/' \
                        'li[starts-with(@class, "list-view-item vevent")]'


    def parse_ticket_detail(self, response):

        loader = response.meta['loader']
        loader.add_value('age', '500')

        # Complete the loader, yielding the completed item
        return loader.load_item()


    def parse(self, response):
        selector = Selector(response)
        venue_id = get_venue_id(response.url)
        #log.start(loglevel='DEBUG', logstdout=True)

        #iterate over each event
        for event in selector.xpath(self.events_list_xpath):
            loader = EventLoader(EventItemSpecial(), selector=event)
            loader.add_xpath('name',        './a/img[@class="event-results-image"]/@title')
            loader.add_xpath('url',         './a/@href')
            loader.add_xpath('artists',     './/div[@class="event-results-titles"]/h3[@class="headliners summary"]/'
                                            'a/text()')
            loader.add_xpath('artists',     './/div[@class="event-results-titles"]/'
                                            'p[@class="event-results-openers description"]/a/text()')
            loader.add_xpath('date',        './/div[@class="event-date dtstart"]/span[@class="value-title"]/@title')
            loader.add_xpath('time',        './/div[@class="event-results-ticket-price"]/p[@class="event-time"]/text()')
            loader.add_xpath('price',       './/div[@class="event-results-ticket-price"]/'
                                            'p[@class="event-price"]/text()')
            loader.add_value('price',       'NA')
            loader.add_xpath('status',      './/div[@class="event-results-ticket-price"]/'
                                            'span[@class="button radius small sold-out"]/text()')
            loader.add_xpath('status',      './/div[@class="event-results-ticket-price"]/'
                                            'span[@class="ticket-link primary-link"]/'
                                            'a[@class="button radius small green tickets"]/text()')
            loader.add_xpath('detail_url',   './/div[@class="event-results-ticket-price"]/'
                                            'span[@class="ticket-link primary-link"]/'
                                            'a[@class="button radius small green tickets"]/@href')
            #loader.add_xpath('url',         None)
            loader.add_value('venue_id',     str(venue_id))
            loader.add_value('last_update',  str(date.today()))

            event_url = urljoin(response.url,loader.get_output_value('url'))
            
            yield scrapy.Request(url=event_url,
                                 meta={'loader': loader},
                                 callback=self.parse_ticket_detail,
                                 dont_filter=True)

