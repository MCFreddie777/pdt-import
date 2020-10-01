from pathlib import Path
import jsonlines
from geoalchemy2.elements import WKTElement
from base import Session
from models.account import Account, SavedAccountType
from models.country import Country
from models.hashtag import Hashtag
from models.tweet import Tweet
from datetime import datetime


# parse each json line of the each file
def parse_each_file(files, func):
    """
    Parses each file from the
    :param files:
    :param func:
    """
    for index, file in enumerate(files):
        if LOG:
            print(f"Reading file {index + 1}/{len(files)} ({file}) ...")

        parse_file(file, func)

        if LOG:
            print_stats()


def parse_file(file, func):
    """
    Parses each line of the file
    :param file: path of the jsonl file to be read
    :param func: function to be executed on each object
    """
    with jsonlines.open(file) as reader:
        for obj in reader:
            func(obj)

        if LOG:
            end_time = datetime.now()
            print(f'Duration: {end_time - start_time}\n')


def print_stats(additional_log=''):
    if additional_log:
        print(additional_log)
    print(len(accounts_map), 'accounts imported.')
    print(len(countries_map), 'countries imported.')
    print(len(tweets_map), 'tweets imported')
    print(len(hashtags_map), 'hashtags imported.')


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
        if obj['coordinates'] and obj['coordinates']['coordinates']:
            location = WKTElement(
                f"POINT({obj['coordinates']['coordinates'][0]} {obj['coordinates']['coordinates'][1]})", srid=4326)

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
                accounts_map[account.id] = SavedAccountType.FULL
            else:
                # find user in database
                account = session.query(Account).filter(Account.id == user_id).scalar()

                # user was previously saved as user_mention and needs to be updated with new attributes which are not present in user_mentions
                if accounts_map[user_id] == SavedAccountType.MENTION:
                    account.update(obj['user'])
                    accounts_map[account.id] = SavedAccountType.FULL

            # add user as an author of the tweet
            tweet.author = account

        # user mentions
        if (
                obj['entities'] is not None and
                obj['entities']['user_mentions'] is not None and
                len(obj['entities']['user_mentions'])
        ):
            mentions = []

            # map all hashtags
            for mentioned_user in obj['entities']['user_mentions']:

                user_id = mentioned_user['id']

                # if user is mentioned in the status multiple times (not saved to the db yet, already in accounts hashmap)
                # or the user mentions himself before being saved to db
                # (they're saved at the end of save_tweet function along the tweet itself)

                if (
                        user_id in map(lambda x: x.id, mentions) or
                        user_id == tweet.author.id
                ):
                    continue

                # check whether the hashtag wasn't previously saved
                if not user_id in accounts_map:
                    account = Account(
                        id=mentioned_user['id'],
                        screen_name=mentioned_user['screen_name'],
                        name=obj['user']['name'],
                        description=obj['user']['description'],
                    )
                    accounts_map[user_id] = SavedAccountType.MENTION
                else:
                    # find user in database
                    account = session.query(Account).filter(Account.id == user_id).scalar()

                # append to the array of mentions
                mentions.append(account)

            # associate hashtags array with tweet
            tweet.mentions = mentions

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
DEBUG = False

# Console logs
LOG = True
start_time = datetime.now()

if DEBUG:
    parse_file('data_test/test_10000.jsonl', save_tweet)
else:
    data_dir = Path('data')
    files = (entry for entry in data_dir.iterdir() if entry.is_file() and entry.name.endswith('.jsonl'))
    parse_each_file(list(files), save_tweet)

if LOG:
    print_stats('Total:')

session.commit()
session.close()
