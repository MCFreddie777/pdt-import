from pathlib import Path
import jsonlines
from geoalchemy2.elements import WKTElement
from base import Session
from models.account import Account
from models.country import Country
from models.hashtag import Hashtag
from models.tweet import Tweet


def get_input_files():
    """
    Loads all jsonl files from data folder
    :return: array of file paths
    """
    file_ext = '.jsonl'
    data_dir = Path('data')
    return (entry for entry in data_dir.iterdir() if entry.is_file() and entry.name.endswith(file_ext))


# parse each json line of the each file
def parse_each_file(files, func):
    """
    Parses each file from the
    :param files:
    :param func:
    """
    for file in files:
        parse_file(file, func)


def parse_file(file, func):
    """
    Parses each line of the file
    :param file: path of the jsonl file to be read
    :param func: function to be executed on each object
    """
    with jsonlines.open(file) as reader:
        for obj in reader:
            func(obj)


def save_tweet(obj):
    """
    Saves each tweet to the database
    :param obj:
    """
    tweet_id = obj['id_str']
    if not tweet_id in tweets_map:

        # dive into recursion until we hit the original tweet
        parent_tweet = None
        if 'retweeted_status' in obj and obj['retweeted_status'] is not None:
            parent_tweet = save_tweet(obj['retweeted_status'])

        location = None
        if obj['geo']:
            location = WKTElement(f"POINT({obj['geo']['coordinates'][0]} {obj['geo']['coordinates'][1]})", srid=4326)

        tweet = Tweet(
            id=obj['id_str'],
            content=obj['full_text'],
            location=location,
            retweet_count=obj['retweet_count'],
            favorite_count=obj['favorite_count'],
            happened_at=obj['created_at']
        )

        tweets_map[tweet_id] = True

        # if user is present in tweet
        if obj['user'] is not None:

            # if user is not previously added in hashmap of accounts create new user
            user_id = obj['user']['id']
            if not user_id in accounts_map:
                account = Account(
                    id=obj['user']['id'],
                    screen_name=obj['user']['screen_name'],
                    name=obj['user']['name'],
                    description=obj['user']['description'],
                    followers_count=obj['user']['followers_count'],
                    friends_count=obj['user']['friends_count'],
                    statuses_count=obj['user']['statuses_count']
                )
                accounts_map[account.id] = True
            else:
                # find user in database
                account = session.query(Account).filter(Account.id == user_id).scalar()

            # add user as an author of the tweet
            tweet.author = account

        # if place is present in tweet and has all fields present
        if (
                obj['place'] is not None and
                obj['place']['country_code'] and
                obj['place']['country_code']
        ):
            # if place is not previously added in hashmap of countries create a new country
            country_code = obj['place']['country_code']
            if not country_code in countries_map:
                country = Country(
                    code=obj['place']['country_code'],
                    name=obj['place']['country']
                )
                countries_map[country.code] = True
            else:
                # find country in database
                country = session.query(Country).filter(Country.code == country_code).scalar()

            # add place as an country of the tweet
            tweet.country = country

        if (
                obj['entities'] is not None and
                obj['entities']['hashtags'] is not None and
                len(obj['entities']['hashtags'])
        ):
            hashtags = []

            # map all hashtags
            for hashtag_obj in obj['entities']['hashtags']:

                # check whether the hashtag wasn't previously saved
                hashtag_id = hashtag_obj['text']

                # hashtag_id in hashtags of current tweet, not saved to the db yet, already in hashtag hashmap
                if hashtag_id in map(lambda x: x.value, hashtags):
                    continue

                if not hashtag_id in hashtags_map:
                    hashtags_map[hashtag_id] = True
                    hashtag = Hashtag(hashtag_obj['text'])
                else:
                    # find hashtag in database
                    hashtag = session.query(Hashtag).filter(Hashtag.value == hashtag_id).scalar()

                # append to the array of hashtags
                hashtags.append(hashtag)

            # associate hashtags array with tweet
            tweet.hashtags = hashtags

        # set the parent tweet from the recursion
        if parent_tweet:
            tweet.parent = parent_tweet

        # save tweet object into the db
        session.add(tweet)

        return tweet


# init session
session = Session()

# declare hashmaps for objects
accounts_map = {}
countries_map = {}
tweets_map = {}
hashtags_map = {}

# Debug mode
DEBUG = True

if (DEBUG):
    parse_file('data/test_2000.jsonl', save_tweet)
    print('len(accounts_map)', len(accounts_map))
    print('len(countries_map)', len(countries_map))
    print('len(tweets_map)', len(tweets_map))
    print('len(hashtags_map)', len(hashtags_map))
else:
    files = get_input_files()
    parse_each_file(files, save_tweet)

session.commit()
session.close()
