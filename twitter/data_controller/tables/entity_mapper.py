from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, backref

from data_controller.tables.tweet_mapper import Tweet
from data_controller.db_setup import Base

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    entity = Column(String(250))
    starting_index = Column(Integer)
    ending_index = Column(Integer)
    text = Column(String(250))
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship("Tweet", backref=backref('entity'))

