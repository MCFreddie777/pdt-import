from sqlalchemy import MetaData, Table, Column, String, Integer, BigInteger, Text, ForeignKey, TIMESTAMP
from geoalchemy2 import Geometry

meta = MetaData()

countries = Table(
    'countries',
    meta,
    Column('id', Integer, primary_key=True),
    Column('code', String(2)),
    Column('name', String(200))
)

accounts = Table(
    'accounts',
    meta,
    Column('id', BigInteger, primary_key=True),
    Column('screen_name', String(200)),
    Column('name', String(200)),
    Column('description', Text),
    Column('followers_count', Integer),
    Column('friends_count', Integer),
    Column('statuses_count', Integer),
)

hashtags = Table(
    'hashtags',
    meta,
    Column('id', Integer, primary_key=True),
    Column('value', Text, unique=True),
)

tweets = Table(
    'tweets',
    meta,
    Column('id', String(20), primary_key=True),
    Column('content', Text),
    Column('location', Geometry(geometry_type='POINT', srid=4326)),
    Column('retweet_count', Integer),
    Column('favorite_count', Integer),
    Column('happened_at', TIMESTAMP(timezone=True)),
    Column('author_id', BigInteger, ForeignKey("accounts.id"), nullable=False),
    Column('country_id', Integer, ForeignKey("countries.id"), nullable=False),
    Column('parent_id', String(20), ForeignKey("tweets.id"), nullable=True),
)

tweet_mentions = Table(
    'tweet_mentions',
    meta,
    Column('id', Integer, primary_key=True),
    Column('account_id', BigInteger, ForeignKey("accounts.id"), nullable=False),
    Column('tweet_id', String(20), ForeignKey("tweets.id"), nullable=False),
)

tweet_hashtags = Table(
    'tweet_hashtags',
    meta,
    Column('id', Integer, primary_key=True),
    Column('hashtag_id', Integer, ForeignKey("hashtags.id"), nullable=False),
    Column('tweet_id', String(20), ForeignKey("tweets.id"), nullable=False),
)
