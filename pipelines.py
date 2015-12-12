# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from models import Event, Venue, Artist, db_connect, create_tables, event_artists, get_or_create
import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BuildDbPipeline(object):
    ''' pipeline for storing scraped items in the database '''
    def __init__(self):
        '''
        initializes the database connections and sessionmaker
        creates all tables
        '''

        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        '''
        Save events in the database
        this method is called for every item pipeline component
        '''
        session = self.Session()

        name = item['name']
        date = item['date']
        artists = item['artists'].split(',')
        price = item['price']
        url = item['url']
        status = item['status']
        venue_id = float(item['venue_id'])
        detail_url = item['detail_url']
        last_update = item['last_update']
        age = item['age']

        e = get_or_create(session, Event, name=name, date=date, price=price, url=url)
        e.status = status
        e.detail_url = detail_url
        e.age = age
        e.last_update = last_update
        e.venue = get_or_create(session, Venue, id=venue_id)

        for artist in artists:
            e.artists.append(get_or_create(session, Artist, name=artist))

        session.commit()
        session.close()

        return item
