from sqlalchemy import create_engine, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.url import URL
from sqlalchemy import Sequence

import datetime
import pytz
import settings

# Create the base class, able to create classes that include directives to describe
# the actual database table they will be mapped to
# returns a new base class from which all mapped classes should inherit
Base = declarative_base()


def db_connect():
    '''
    Performs database connections using database settings from settings.py
    Returns sqlalchemy engine instance
    '''
    engine = create_engine(URL(**settings.DATABASE))
    return engine


def create_tables(engine):
    Base.metadata.create_all(engine)


# association table
event_artists = Table('event_artists', Base.metadata,
                      Column('event_id', Integer, ForeignKey('events.id')),
                      Column('artist_id', Integer, ForeignKey('artists.id')))


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, Sequence('event_id_seq'), primary_key=True)
    event_num = Column(String(100))
    title = Column(String(200))
    status = Column(String(100))
    ticket_price = Column(String(100))
    ticket_price_cleaned = Column(String(100))
    event_ts = Column(String(100))
    event_url = Column(String(200))
    purchase_url = Column(String(200))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    promoter = Column(String(200))
    age_restriction = Column(String(100))
    updated_ts = Column(String(100))
    created_ts = Column(String(100))
    soldout_ts = Column(String(100))

    artists = relationship('Artist',
                           secondary=event_artists)


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    songkick_id = Column(Integer)
    google_id = Column(String(50))
    name = Column(String(200))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    lat = Column(Float)
    lng = Column(Float)
    street = Column(String(100))
    zip = Column(Integer)
    neighborhood = Column(String(100))
    homepage_url = Column(String(200))
    scrape_url = Column(String(200))
    about = Column(String(1000))
    capacity = Column(Integer)
    ticketing = Column(String(50))
    created_ts = Column(String(100))
    updated_ts = Column(String(100))

    events = relationship('Event', backref='venue')


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    created_ts = Column(String(100))
    updated_ts = Column(String(100))
    genre = Column(String(100))
    info = Column(String(100))

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance, True

def utcnow():
    return datetime.datetime.now(tz=pytz.utc)
