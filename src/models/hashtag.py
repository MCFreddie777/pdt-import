from sqlalchemy import Column, Text, Integer, Table, ForeignKey, String
from sqlalchemy.orm import relationship
from base import Base
from models.tweet import tweet_hashtags_association


class Hashtag(Base):
    __tablename__ = 'hashtags'

    # properties
    id = Column('id', Integer, primary_key=True)
    value = Column('value', Text, unique=True)

    # relationships
    tweets = relationship("Tweet", secondary=tweet_hashtags_association)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"id: {self.id}\nvalue: {self.value}\n"

    def __repr__(self):
        return str(self)

