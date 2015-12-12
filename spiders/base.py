from scrapy.spiders import Spider
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import Join, MapCompose
from scrapy.http import Request
from datetime import date

from build_db.items import EventItemSpecial, EventLoader, UrlItem
from build_db.venues import get_scrape_urls, get_venue_id

class Ticketfly(Spider):
    name = 'tfly'
    allowed_domains = ['ticketfly.com']
    start_urls = get_scrape_urls('ticketfly')

    events_list_xpath = '//div[starts-with(@class, "event-results")]/ul/' \
                        'li[starts-with(@class, "list-view-item vevent")]'

    def parse(self, response):

        selector = Selector(response)
        venue_id = get_venue_id(response.url)
        #log.start(loglevel='INFO', logstdout=False)

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
            #loader.add_value('detailUrl',    None)
            loader.add_value('venue_id',     str(venue_id))
            loader.add_value('last_update',  str(date.today()))
            loader.add_value('age',          loader.get_output_value('detail_url'))
            #oader.add_value('age',          '21')
            
            yield loader.load_item()