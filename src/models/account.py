from sqlalchemy import Column, String, Integer, BigInteger, Text
from sqlalchemy.orm import relationship
from base import Base


class Account(Base):
    __tablename__ = 'accounts'

    # properties
    id = Column('id', BigInteger, primary_key=True)
    screen_name = Column('screen_name', String(200))
    name = Column('name', String(200))
    description = Column('description', Text)
    followers_count = Column('followers_count', Integer)
    friends_count = Column('friends_count', Integer)
    statuses_count = Column('statuses_count', Integer)

    # relationships
    tweets = relationship("Tweet")

    def __init__(self, screen_name, name, description, followers_count, friends_count, statuses_count):
        self.screen_name = screen_name
        self.name = name
        self.description = description
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count
