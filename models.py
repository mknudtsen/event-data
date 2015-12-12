from sqlalchemy import create_engine, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.url import URL

import settings

# Create the base class, able to create classes that include directives to describe
# the actual database table they will be mapped to
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

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    status = Column(String(100))
    price = Column(String(100))
    date = Column(String(100))
    url = Column(String(200))
    detail_url = Column(String(200))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    last_update = Column(String(100))
    age = Column(String(100))
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

    events = relationship('Event', backref='venue')


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    genre = Column(String(100))
    familiarity = Column(Float)
    hot = Column(Float)
    terms = Column(String(1000))
    twitter = Column(String(100))
    songs = Column(String(1000))


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance






