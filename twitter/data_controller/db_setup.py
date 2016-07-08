import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

location = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'twitter.db')

engine = create_engine('sqlite:///' + location)
Base = declarative_base()

## need to import all the tables before creating the engine?
from data_controller.tables.tweeter_mapper import Tweeter
from data_controller.tables.tweet_mapper import Tweet
from data_controller.tables.entity_mapper import Entity

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session(session=None):
    """ Convenience function for getting session when necessary."""
    isNewSession = False
    if session is None:
        session = Session()
        isNewSession = True
    return session, isNewSession
