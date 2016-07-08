from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, backref

from data_controller.tables.tweeter_mapper import Tweeter
from data_controller.db_setup import Base

class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    text = Column(String(250))
    created_at = Column(DateTime)
    favorite_counts = Column(Integer)
    retweet_counts = Column(Integer)
    tweeter_id = Column(Integer, ForeignKey('tweeter.id'))
    tweeter = relationship("Tweeter", backref=backref('tweet'))

