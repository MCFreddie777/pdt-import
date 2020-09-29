from sqlalchemy import Column, Text, Integer, String, BigInteger, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import relationship
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
    country_id = Column('country_id', Integer, ForeignKey("countries.id"), nullable=False)
    parent_id = Column('parent_id', String(20), ForeignKey("tweets.id"), nullable=True)

    # relationships
    country = relationship("Country")
    author = relationship("Account")
    parent = relationship("Tweet")
    hashtags = relationship("Hashtag", secondary=tweet_hashtags_association)
    mentions = relationship("Account", secondary=tweet_accounts_association)

    def __init__(
            self,
            content,
            location,
            retweet_count,
            favorite_count,
            happened_at,
            author_id,
            country_id,
            parent_id
    ):
        self.content = content
        self.location = location
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.happened_at = happened_at
        self.author_id = author_id
        self.country_id = country_id
        self.parent_id = parent_id
