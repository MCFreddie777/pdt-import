from sqlalchemy import Column, Text, Integer, String, BigInteger, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import relationship, backref
from geoalchemy2 import Geometry
from base import Base

tweet_hashtags_association = Table(
    'tweet_hashtags', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('hashtag_id', Integer, ForeignKey("hashtags.id"), nullable=False),
    Column('tweet_id', String(20), ForeignKey("tweets.id"), nullable=False),
)

tweet_accounts_association = Table(
    'tweet_mentions',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('account_id', BigInteger, ForeignKey("accounts.id"), nullable=False),
    Column('tweet_id', String(20), ForeignKey("tweets.id"), nullable=False),
)


class Tweet(Base):
    __tablename__ = 'tweets'

    # properties
    id = Column('id', String(20), primary_key=True)
    content = Column('content', Text)
    location = Column('location', Geometry(geometry_type='POINT', srid=4326))
    retweet_count = Column('retweet_count', Integer)
    favorite_count = Column('favorite_count', Integer)
    happened_at = Column('happened_at', TIMESTAMP(timezone=True))
    author_id = Column('author_id', BigInteger, ForeignKey("accounts.id"), nullable=False)
    country_id = Column('country_id', Integer, ForeignKey("countries.id"), nullable=True)
    parent_id = Column('parent_id', String(20), ForeignKey("tweets.id"), nullable=True)

    # relationships
    country = relationship("Country")
    author = relationship("Account")
    parent = relationship("Tweet", remote_side=[id])
    hashtags = relationship("Hashtag", secondary=tweet_hashtags_association)
    mentions = relationship("Account", secondary=tweet_accounts_association)

    def __init__(
            self,
            id,
            content,
            location,
            retweet_count,
            favorite_count,
            happened_at,
    ):
        self.id = id
        self.content = content
        self.location = location
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.happened_at = happened_at

    def __str__(self):
        return f"id: {self.id}\ncontent: {self.content}\nlocation: {self.location}\nretweet_count: {self.retweet_count}\nfavorite_count: {self.favorite_count}\nhappened_at: {self.happened_at}\n"
