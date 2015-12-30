# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from models import Event, Venue, Artist, db_connect, create_tables, event_artists, get_or_create, utcnow

import datetime
import re

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

        # create variables with each of the newly scraped items
        # variables named for the columns in the 'Event' model
        # they will be used to create/return and edit individual events from the db
        title = item['title']
        event_ts = item['event_ts']
        artists = item['artists'].split(',')
        ticket_price = item['ticket_price']
        event_url = item['event_url']
        status = item['status']
        venue_id = int(item['venue_id'])
        purchase_url = item['purchase_url']
        #last_update = item['last_update']
        age_restriction = item['age_restriction']
        promoter = item['promoter']

        # search event_url for set of numbers which are unique to that event
        # then set event_num (a unique id) with the match from event_url (m)
        m = re.search(r'\/(\d+)-', event_url)
        event_num = m.group(1)

        # get_or_create returns an event instance from the db
        # if the event is not found, it then creates the event
        # event_num is unique for an event in the db
        # event_title and other characteristics are likely to change over time
        # need to ensure that we aren't storing multiple records for an event
        e = get_or_create(session, Event, 
                          event_num=event_num)

        # check to see if new scraped status differs from that stored in the db
        # in the case that the scraped event has a status of 'Sold Out'
        # we then check to see if the status in the db is also 'Sold Out'
        # if the db shows that stored status != 'Sold Out'
        # then we can set the soldout_ts (timestamp) to the current utc datetime
        if ('Sold' in status) and (e.status != 'Sold Out'):
            e.soldout_ts = str(utcnow().isoformat())
            e.status = status
        elif (e.status == 'Sold Out'):
            e.soldout_ts = str(utcnow().isoformat())
            e.status = status
        else:
            e.status = status

        e.title = title
        e.event_ts = event_ts
        e.ticket_price = ticket_price
        e.event_url = event_url
        e.purchase_url = purchase_url
        e.age_restriction = age_restriction
        e.promoter = promoter
        e.last_update = str(utcnow().isoformat())

        e.venue = get_or_create(session, Venue, id=venue_id)
        for artist in artists:
            e.artists.append(get_or_create(session, Artist, name=artist))

        session.commit()
        session.close()

        return item
