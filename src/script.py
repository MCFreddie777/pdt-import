from pathlib import Path
import jsonlines
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
    account = Account(
        obj['user']['id'],
        obj['user']['screen_name'],
        obj['user']['name'],
        obj['user']['description'],
        obj['user']['followers_count'],
        obj['user']['friends_count'],
        obj['user']['statuses_count']
    )

    if not account.id in accounts_map:
        accounts_map[account.id] = True
        session.add(account)


# init session
session = Session()

# declare hashmaps for objects
accounts_map = {}
hashtags_map = {}
countries_map = {}
tweets_map = {}


# Debug mode
DEBUG = True

if (DEBUG):
    parse_file('data/test.jsonl', save_tweet)
else:
    files = get_input_files()
    parse_each_file(files, save_tweet)

session.commit()
session.close()
