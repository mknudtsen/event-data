from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import mapper, create_session, sessionmaker
from models import db_connect, create_tables, Venue, get_or_create
import csv


CSV_FILE = 'build_db/venues.csv'
engine = db_connect()
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

with open(CSV_FILE) as f:
    cf = csv.DictReader(f, delimiter=',')
    for row in cf:
        v, v_created = get_or_create(session, Venue, **row)
        session.add(v)

session.commit()
session.close()


def get_scrape_urls(ticketing):
    scrape_url = [url[0] for url in session.query(Venue.scrape_url).filter(Venue.ticketing == ticketing).all()]
    return scrape_url


def get_venue_id(response):
    venue_id = session.query(Venue.id).filter(Venue.scrape_url == response).first()[0]
    return venue_id
