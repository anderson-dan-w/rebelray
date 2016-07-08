from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, backref

from data_controller.db_setup import Base

class Tweeter(Base):
    __tablename__ = 'tweeter'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    twitter_handle = Column(String(250), nullable=False)
    user_id = Column(Integer)
    max_tweet_id = Column(Integer)
    min_tweet_id = Column(Integer)

